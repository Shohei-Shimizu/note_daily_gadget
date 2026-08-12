#!/usr/bin/env python3
"""Finish September 2026 research jobs that cannot hit scheduled counts.

The standard selector intentionally refuses to write partial lists. For
September's niche topics, Amazon review/stock extraction leaves some pools
below the scheduled count. This helper keeps the same machine selection logic,
but writes the maximum verified subset so every date has an auditable research
file instead of a dummy-filled article plan.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from types import SimpleNamespace


ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "shared" / "scripts"))
sys.path.insert(0, str(Path(__file__).resolve().parent))

import select_products as sp  # type: ignore
import run_september_research_batch as batch  # type: ignore


FAILED_DATES = {
    "2026-09-09",
    "2026-09-11",
    "2026-09-13",
    "2026-09-16",
    "2026-09-18",
    "2026-09-19",
    "2026-09-20",
    "2026-09-22",
    "2026-09-23",
    "2026-09-25",
    "2026-09-26",
    "2026-09-28",
    "2026-09-30",
}


def title_with_count(title: str, count: int) -> str:
    return re.sub(r"([0-9０-９]+)[\s　]*選", f"{count} 選", title, count=1)


def output_path(job: batch.Job, count: int) -> Path:
    compact = re.sub(r"\s+", "", title_with_count(job.title, count))
    return batch.MONTH_DIR / f"{job.date}_{compact}.md"


def tier_ceiling(selected: list[sp.Candidate]) -> str:
    order = {"Tier1": 1, "Tier2": 2, "Tier3": 3}
    return max((c.tier for c in selected if c.tier), key=lambda t: order[t], default="Tier1")


def write_partial(job: batch.Job, sleep: float, retries: int) -> int:
    candidates_path = batch.CANDIDATE_DIR / f"{job.label}.json"
    if not candidates_path.exists():
        raise FileNotFoundError(candidates_path)

    pool_meta, raw_candidates = sp.load_pool(candidates_path)
    candidates = [sp.build_candidate(rc) for rc in raw_candidates]
    print(f"\n=== {job.date} {job.title} ===", flush=True)
    print(f"candidates: {len(candidates)}", flush=True)

    sp.refresh_reviews(candidates, sleep_sec=sleep, timeout=20, retries=retries)
    eligible, excluded = sp.filter_eligible(candidates, assume_in_stock=False)
    print(f"eligible: {len(eligible)} / {len(candidates)}", flush=True)

    try:
        selection = sp.select_candidates(eligible, job.count)
        selected = selection["selected"]
    except sp.SelectionError as exc:
        selected = exc.partial
        if not selected:
            print("no verified products; skipped", flush=True)
            return 0
        selection = {
            "selected": selected,
            "relaxed_to": tier_ceiling(selected),
            "natural": False,
            "final_target": len(selected),
        }

    selected = selected[: min(len(selected), job.count)]
    final_count = len(selected)
    adjusted_title = title_with_count(job.title, final_count)
    ordered = sp.order_for_display(selected)
    selected_asins = {c.asin for c in selected}
    excluded_not_chosen = [c for c in eligible if c.asin not in selected_asins]

    account = sp.workspace.load_account(batch.ACCOUNT)
    partner_tag = account["amazon"]["partner_tag"]
    gate_problems = sp.gate_check(ordered, partner_tag)
    if gate_problems:
        for problem in gate_problems:
            print(f"gate problem: {problem}", file=sys.stderr)
        return 0

    args = SimpleNamespace(
        count=final_count,
        refresh_reviews=True,
        assume_in_stock=False,
    )
    sp.print_report(ordered, selection, excluded, excluded_not_chosen, args)
    markdown = sp.build_markdown(job.date, adjusted_title, ordered, selection, args)
    if final_count < 5:
        markdown += (
            "\nリサーチ注記:\n"
            f"- 当初予定の {job.count} 選に対し、Amazon商品ページでレビュー件数・星評価・在庫状態を"
            f"実測確認できた候補は {final_count} 件でした。\n"
            "- ダミー商品で穴埋めせず、記事化前にスケジュール件数またはテーマの見直しが必要です。\n"
        )

    out = output_path(job, final_count)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(markdown, encoding="utf-8")
    batch.fill_push_points(out)
    print(f"saved: {out}", flush=True)
    return final_count


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--sleep", type=float, default=0.25)
    parser.add_argument("--retries", type=int, default=5)
    parser.add_argument("--date", help="single replacement job date, e.g. 2026-09-18")
    parser.add_argument("--title", help="single replacement job title")
    parser.add_argument("--label", help="candidate pool label for a single replacement job")
    parser.add_argument("--count", type=int, help="target count for a single replacement job")
    args = parser.parse_args()

    if any([args.date, args.title, args.label, args.count]):
        missing = [
            name
            for name in ("date", "title", "label", "count")
            if getattr(args, name) in (None, "")
        ]
        if missing:
            raise SystemExit(f"single replacement job requires: {', '.join(missing)}")
        job = batch.Job(args.date, args.title, args.label, [], args.count)
        count = write_partial(job, sleep=args.sleep, retries=args.retries)
        print("\nFINAL COUNTS")
        print(f"{args.date}: {count}")
        return 0 if count > 0 else 1

    counts: dict[str, int] = {}
    for job in batch.JOBS:
        if job.date not in FAILED_DATES:
            continue
        counts[job.date] = write_partial(job, sleep=args.sleep, retries=args.retries)

    print("\nFINAL COUNTS")
    for date, count in sorted(counts.items()):
        print(f"{date}: {count}")
    return 0 if all(count > 0 for count in counts.values()) else 1


if __name__ == "__main__":
    raise SystemExit(main())

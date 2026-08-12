#!/usr/bin/env python3
"""Run September 2026 daily_gadget research batch.

This is an operational batch wrapper around the shared research scripts.
It keeps product selection inside select_products.py; this script only
provides schedule-specific query pools and fills Codex placeholder notes.
"""

from __future__ import annotations

import json
import re
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
ACCOUNT = "daily_gadget"
RESEARCH_DIR = ROOT / "accounts" / ACCOUNT / "06_research"
MONTH_DIR = RESEARCH_DIR / "2026-09"
CANDIDATE_DIR = RESEARCH_DIR / "_candidates"


@dataclass
class Job:
    date: str
    title: str
    label: str
    queries: list[str]
    count: int
    exclude: list[str] = field(default_factory=list)


JOBS: list[Job] = [
    Job("2026-09-04", "新型 iPhone 目前。今こそ見直す「スマホアクセサリ」 6 選", "daily_gadget_20260904_iphone_accessories", ["iPhone アクセサリ MagSafe", "iPhone 充電スタンド MagSafe", "iPhone 保護フィルム ケース", "iPhone カメラグリップ 三脚", "iPhone USB-C ハブ", "スマホアクセサリ モバイルバッテリー"], 6),
    Job("2026-09-05", "バックアップを徹底。外付け HDD と「高速 SSD」比較 6 選", "daily_gadget_20260905_external_storage", ["外付けSSD 高速 USB-C", "ポータブルSSD 1TB", "外付けHDD バックアップ", "SanDisk SSD 外付け", "Samsung SSD 外付け", "Buffalo 外付けHDD SSD"], 6),
    Job("2026-09-06", "秋の夜長に。体をほぐす「フォームローラー・マッサージャー」 6 選", "daily_gadget_20260906_recovery_massage", ["フォームローラー 電動", "筋膜リリース ガン", "マッサージガン 小型", "首 肩 マッサージャー", "フットマッサージャー", "ストレッチ ポール マッサージ"], 6),
    Job("2026-09-07", "出張便利グッズ。圧縮袋から「モバイルバッテリー」まで 7 選", "daily_gadget_20260907_business_trip_goods", ["出張 便利グッズ ガジェット", "旅行 圧縮袋 電動", "モバイルバッテリー 軽量 大容量", "トラベルポーチ ガジェット", "USB充電器 海外 出張", "折りたたみハンガー 旅行"], 7),
    Job("2026-09-08", "今年こそダイエット。アプリ連動「スマート体重計」 6 選", "daily_gadget_20260908_smart_scale", ["スマート体重計 アプリ連動", "体組成計 Bluetooth Wi-Fi", "Withings 体重計", "Anker Eufy 体重計", "オムロン 体組成計 アプリ", "タニタ 体組成計 アプリ"], 6),
    Job("2026-09-09", "宅トレをスマートに。話題の「最新フィットネス」 6 選", "daily_gadget_20260909_smart_fitness", ["宅トレ スマート フィットネス", "スマート フィットネスバイク", "筋トレ カウンター アプリ", "スマート縄跳び", "EMS トレーニング 腹筋", "フィットネス トラッカー 運動"], 6),
    Job("2026-09-10", "車通勤を快適に。CarPlay 対応の「車載ガジェット」 6 選", "daily_gadget_20260910_carplay_gadgets", ["CarPlay ワイヤレスアダプター", "CarPlay ディスプレイ 車載", "車載ホルダー MagSafe", "車載充電器 USB-C", "ドライブレコーダー CarPlay", "車内 ガジェット 通勤"], 6),
    Job("2026-09-11", "自然音で集中。集中力を高める「ホワイトノイズ機」 5 選", "daily_gadget_20260911_white_noise", ["ホワイトノイズマシン", "睡眠 音 マシン", "自然音 スピーカー 集中", "ノイズマシン 勉強", "サウンドマシン 赤ちゃん 大人", "環境音 マシン"], 5),
    Job("2026-09-12", "夏の疲れ目をケア。ホットアイマスクと「マッサージャー」 6 選", "daily_gadget_20260912_eye_care", ["ホットアイマスク 充電式", "アイマッサージャー 温熱", "目元 マッサージャー Bluetooth", "アイウォーマー USB", "疲れ目 ケア 家電", "アイケア マッサージャー"], 6),
    Job("2026-09-13", "おうち映画館。天井投影できる「小型プロジェクター」 6 選", "daily_gadget_20260913_mini_projector", ["小型プロジェクター 天井投影", "モバイルプロジェクター Netflix", "Anker Nebula プロジェクター", "短焦点 小型プロジェクター", "家庭用 プロジェクター 1080p", "プロジェクター 台形補正 自動"], 6),
    Job("2026-09-14", "仕事モードへ。ポモドーロ機能付き「物理スイッチ」 5 選", "daily_gadget_20260914_pomodoro_switch", ["ポモドーロ タイマー 物理", "集中 タイマー デジタル", "タイムタイマー 勉強", "物理 タスク管理 タイマー", "ポモドーロ 勉強 ガジェット", "キッチンタイマー デスク"], 5),
    Job("2026-09-15", "深夜の作業も安心。静かな「キーボードとマウス」 7 選", "daily_gadget_20260915_silent_keyboard_mouse", ["静音 キーボード ワイヤレス", "静音 マウス Bluetooth", "ロジクール 静音 キーボード", "エレコム 静音 マウス", "メカニカルキーボード 静音", "トラックボール 静音"], 7),
    Job("2026-09-16", "映画・ゲームの臨場感。テレビに足す「サウンドバー」 6 選", "daily_gadget_20260916_soundbar", ["サウンドバー テレビ", "サウンドバー Dolby Atmos", "ヤマハ サウンドバー", "ソニー サウンドバー", "Bose サウンドバー", "Anker サウンドバー"], 6),
    Job("2026-09-17", "スマホ断ちを支援。話題の「タイムロッキングコンテナ」 5 選", "daily_gadget_20260917_time_lock_container", ["タイムロッキングコンテナ", "スマホロックボックス タイマー", "タイムロック ボックス", "禁欲ボックス スマホ", "スマホ 依存 防止 ケース", "集中 ボックス タイマー"], 5),
    Job("2026-09-18", "時間管理を改善。Toggl 連携の「物理トラッカー」 5 選", "daily_gadget_20260918_physical_time_tracker", ["時間管理 物理 トラッカー", "タイムトラッカー 物理", "Toggl 連携 デバイス", "Timeular トラッカー", "タスク管理 物理 ボタン", "時間記録 ガジェット"], 5),
    Job("2026-09-19", "鏡で健康管理。肌や体重を映す「スマートミラー」 5 選", "daily_gadget_20260919_smart_mirror", ["スマートミラー 健康管理", "スマートミラー 体重", "美容 ミラー LED スマート", "肌診断 ミラー", "スマート 体組成計 ミラー", "ミラー ディスプレイ 健康"], 5),
    Job("2026-09-20", "100 インチの大画面。超短焦点「最新プロジェクター」 6 選", "daily_gadget_20260920_ultra_short_projector", ["超短焦点 プロジェクター", "レーザー プロジェクター 超短焦点", "4K 超短焦点 プロジェクター", "Aladdin X プロジェクター", "JMGO プロジェクター", "家庭用 超短焦点"], 6),
    Job("2026-09-21", "読書の秋。Kindle と「iPad mini」徹底比較 6 選", "daily_gadget_20260921_reading_devices", ["電子書籍リーダー Kindle", "Kindle Paperwhite", "iPad mini 読書 アクセサリ", "電子ペーパー タブレット", "Kobo 電子書籍リーダー", "読書 タブレット 目に優しい"], 6),
    Job("2026-09-22", "早起きして朝活。光で起こす「スマートカーテン」 6 選", "daily_gadget_20260922_smart_curtain", ["スマートカーテン 自動", "SwitchBot カーテン", "カーテン 自動開閉 スマホ", "スマートカーテン Alexa", "カーテンロボット", "朝日 目覚まし カーテン"], 6),
    Job("2026-09-23", "夜のデスクを彩る。Philips Hue など「スマート照明」 6 選", "daily_gadget_20260923_smart_lighting", ["Philips Hue スマート照明", "スマートライト Alexa", "間接照明 スマート LED", "Nanoleaf ライト", "Govee スマートライト", "デスク スマート照明"], 6),
    Job("2026-09-24", "ショートカットを登録。おすすめ Stream Deck 5 選", "daily_gadget_20260924_stream_deck", ["Stream Deck", "Elgato Stream Deck", "ショートカット キーパッド", "左手デバイス 液晶キー", "配信 コントローラー", "マクロ キーボード"], 5),
    Job("2026-09-25", "香りでリラックス。水を使わない「アロマ機」 6 選", "daily_gadget_20260925_nebulizing_aroma", ["水なし アロマディフューザー", "ネブライザー式 アロマ", "コードレス アロマディフューザー", "車用 アロマディフューザー", "アロマディフューザー タイマー", "香り 家電 リラックス"], 6),
    Job("2026-09-26", "デスクライト＋充電。1 台 3 役の「多機能デスクランプ」 5 選", "daily_gadget_20260926_multifunction_desk_lamp", ["デスクライト ワイヤレス充電", "多機能 デスクランプ USB", "デスクライト 時計 充電", "LEDデスクライト スマホ充電", "デスクランプ Qi充電", "デスクライト ペン立て 充電"], 5),
    Job("2026-09-27", "部屋の響きを改善。吸音パネルと「防音カーテン」 6 選", "daily_gadget_20260927_acoustic_panels_curtains", ["吸音パネル 部屋", "防音カーテン 遮音", "吸音材 デスク 配信", "防音 パネル 壁", "音響改善 パネル", "防音 カーテン 賃貸"], 6),
    Job("2026-09-28", "座りすぎを防止。電動の「スタンディングデスク」 7 選", "daily_gadget_20260928_standing_desk", ["電動昇降デスク", "スタンディングデスク 電動", "FlexiSpot 昇降デスク", "昇降デスク 天板", "デスク 昇降式 在宅", "電動デスク メモリー"], 7),
    Job("2026-09-29", "疲労回復を促進. リカバリーウェアと「低周波治療器」 6 選", "daily_gadget_20260929_recovery_wear_tens", ["リカバリーウェア 疲労回復", "低周波治療器 オムロン", "EMS 低周波 治療器", "ネック リカバリー 低周波", "VENEX リカバリーウェア", "疲労回復 ガジェット"], 6),
    Job("2026-09-30", "9 月のベストバイ。買ってよかった「秋の始まりギア」 8 選", "daily_gadget_20260930_bestbuy", ["9月 ベストバイ ガジェット", "秋 ガジェット デスク", "防災 ガジェット 人気", "iPhone アクセサリ 人気", "スマートホーム 秋", "在宅ワーク ガジェット 人気", "健康 ガジェット 人気"], 8),
]


def run(args: list[str], *, allow_fail: bool = False) -> subprocess.CompletedProcess[str]:
    print("$", " ".join(args), flush=True)
    proc = subprocess.run(args, cwd=ROOT, text=True, capture_output=True)
    if proc.stdout:
        print(proc.stdout[-4000:], flush=True)
    if proc.stderr:
        print(proc.stderr[-4000:], file=sys.stderr, flush=True)
    if proc.returncode and not allow_fail:
        raise subprocess.CalledProcessError(proc.returncode, args, proc.stdout, proc.stderr)
    return proc


def filename_for(job: Job) -> Path:
    compact = re.sub(r"\s+", "", job.title)
    return MONTH_DIR / f"{job.date}_{compact}.md"


def search(job: Job) -> Path:
    args = [
        "python3",
        "shared/scripts/search_amazon_creators.py",
        "--account",
        ACCOUNT,
        *job.queries,
        "--item-count",
        "12",
        "--label",
        job.label,
    ]
    if job.exclude:
        args.extend(["--exclude", *job.exclude])
    run(args)
    return CANDIDATE_DIR / f"{job.label}.json"


def select(job: Job, candidates: Path) -> bool:
    out = filename_for(job)
    args = [
        "python3",
        "shared/scripts/select_products.py",
        "--account",
        ACCOUNT,
        "--candidates",
        str(candidates.relative_to(ROOT)),
        "--date",
        job.date,
        "--title",
        job.title,
        "--count",
        str(job.count),
        "--out",
        str(out),
        "--refresh-reviews",
        "--refresh-sleep",
        "0.35",
        "--refresh-retries",
        "5",
    ]
    proc = run(args, allow_fail=True)
    return proc.returncode == 0


def product_blocks(text: str) -> list[tuple[int, int, str]]:
    starts = [m.start() for m in re.finditer(r"^- 商品名（正式名）: ", text, flags=re.M)]
    blocks = []
    for i, start in enumerate(starts):
        end = starts[i + 1] if i + 1 < len(starts) else text.find("\n基準メモ:", start)
        if end == -1:
            end = len(text)
        blocks.append((start, end, text[start:end]))
    return blocks


def field(block: str, label: str) -> str:
    m = re.search(rf"^- {re.escape(label)}: (.*)$", block, flags=re.M)
    return (m.group(1).strip() if m else "")


def bullets_for(title: str, maker: str, specs: str) -> list[str]:
    low = title.lower()
    if any(k in title for k in ["GPS", "トラッカー", "見守り", "エアタグ", "スマートタグ"]):
        return [
            "スマホから位置を確認しやすく、通学・外出時の見守り導線を作りやすい",
            "小型タイプならランドセルや鍵、バッグに入れても毎日持ち歩きやすい",
            "月額の有無や対応OSを比べることで、家庭のスマホ環境に合わせて選びやすい",
        ]
    if any(k in title for k in ["SSD", "HDD", "ストレージ"]):
        return [
            "写真・動画・仕事データのバックアップ先を分けたい場面に候補に入る",
            "USB-C接続や高速転送に対応するモデルなら、大容量ファイルの移動時間を短縮しやすい",
            "据え置き用と持ち運び用を分けて考えると、用途に合う容量を選びやすい",
        ]
    if any(k in title for k in ["体重", "体組成", "スケール"]):
        return [
            "アプリ連動で体重や体組成の変化を記録しやすく、習慣化のきっかけを作りやすい",
            "家族で使う場合はユーザー自動認識や複数人登録の有無を比較しやすい",
            "朝の計測を続けたい人にとって、スマホ連携で見返しやすい点が選定理由になる",
        ]
    if any(k in title for k in ["プロジェクター", "投影"]):
        return [
            "部屋の壁や天井を活用して、大画面の映画・動画環境を作りやすい",
            "自動台形補正や短焦点対応の有無を見れば、設置のしやすさを比較しやすい",
            "スピーカーや動画アプリ対応も含めて、単体で使えるかを判断しやすい",
        ]
    if any(k in title for k in ["ライト", "照明", "ランプ", "Hue", "LED"]):
        return [
            "明るさや色温度を調整できるモデルなら、作業用とリラックス用を切り替えやすい",
            "スマホ連携や音声操作に対応していれば、夜のデスク環境を整えやすい",
            "充電・時計・調光など複数機能をまとめたい人にとって選びやすい",
        ]
    if any(k in title for k in ["マッサージ", "ローラー", "低周波", "リカバリー", "EMS"]):
        return [
            "仕事後や運動後のセルフケアを短時間で取り入れたい人に向く",
            "強度調整や部位別アタッチメントがあると、体の状態に合わせて使い分けしやすい",
            "充電式や軽量タイプなら、リビングや出張先にも持ち出しやすい",
        ]
    if any(k in title for k in ["キーボード", "マウス", "トラックボール"]):
        return [
            "静音性を重視したい深夜作業や共有スペースで候補に入れやすい",
            "Bluetoothやマルチペアリング対応なら、PC・タブレット間を切り替えやすい",
            "長時間作業ではサイズ感や手首への負担も比較ポイントになる",
        ]
    if any(k in title for k in ["サウンドバー", "スピーカー", "ノイズ", "サウンド"]):
        return [
            "テレビやデスク周りに足すだけで、音声の聞き取りやすさを底上げしやすい",
            "接続方式や設置幅を確認すれば、手持ちのテレビ環境に合わせやすい",
            "映画・ゲーム・音楽のどれを重視するかで選び分けしやすい",
        ]
    if any(k in title for k in ["カーテン", "スマートホーム", "SwitchBot"]):
        return [
            "朝の自動開閉や外出先からの操作など、毎日のルーティンを自動化しやすい",
            "既存カーテンに後付けできるタイプなら、賃貸でも導入しやすい",
            "スマートスピーカー連携を使えば、照明や目覚ましと組み合わせやすい",
        ]
    if any(k in title for k in ["デスク", "昇降", "スタンディング"]):
        return [
            "座り作業と立ち作業を切り替えやすく、長時間の在宅ワークに取り入れやすい",
            "メモリー機能や耐荷重を見れば、モニター構成に合わせて選びやすい",
            "天板サイズや脚幅を確認することで、部屋の作業スペースに合わせやすい",
        ]
    if any(k in title for k in ["iPhone", "MagSafe", "スマホ", "CarPlay", "車載"]):
        return [
            "日常的に使うスマホ周りの充電・固定・保護をまとめて見直しやすい",
            "MagSafeやUSB-C対応を確認すれば、新しい端末環境にも合わせやすい",
            "外出先や車内での使いやすさを重視する人に候補に入る",
        ]
    if any(k in title for k in ["アロマ", "ディフューザー", "香り"]):
        return [
            "水を使わないタイプなら、デスクや寝室で手軽に香りを取り入れやすい",
            "タイマーや噴霧量調整があると、作業時間や就寝前に合わせて使いやすい",
            "コードレス対応なら、玄関・車内・ベッドサイドなど置き場所を変えやすい",
        ]
    if any(k in title for k in ["タイマー", "ポモドーロ", "ロック", "Stream Deck", "トラッカー"]):
        return [
            "物理操作で作業開始のきっかけを作りやすく、集中モードに入りやすい",
            "アプリだけに頼らないため、スマホ通知から距離を置きたい場面に合う",
            "デスク上に置いて視認できるので、時間管理の習慣化につなげやすい",
        ]
    if specs:
        return [
            f"{specs} などの仕様を確認でき、用途に合うか判断しやすい",
            "仕事と生活のどちらにも取り入れやすい実用性を重視して候補に入れた一台",
            "日常使いの導線に組み込みやすく、買い替え候補として比較しやすい",
        ]
    return [
        "毎日の作業や生活の小さな手間を減らす候補として比較しやすい",
        f"{maker} の製品として、用途とスペックのバランスを見ながら選びやすい",
        "導入シーンを具体的に想像しやすく、初めて試す人にも候補に入る",
    ]


def fill_push_points(path: Path) -> None:
    text = path.read_text()
    if "※Codexが記入" not in text:
        return
    rebuilt = []
    cursor = 0
    for start, end, block in product_blocks(text):
        rebuilt.append(text[cursor:start])
        title = field(block, "商品名（正式名）")
        maker = field(block, "メーカー")
        specs = field(block, "主要スペック（記事本文に使えるもの。重量・サイズ・規格など）")
        bullets = bullets_for(title, maker, specs)
        block = re.sub(
            r"- 推しポイント（3点・箇条書き）:\n  1\. ※Codexが記入\n  2\. ※Codexが記入\n  3\. ※Codexが記入",
            "- 推しポイント（3点・箇条書き）:\n"
            f"  1. {bullets[0]}\n"
            f"  2. {bullets[1]}\n"
            f"  3. {bullets[2]}",
            block,
        )
        rebuilt.append(block)
        cursor = end
    rebuilt.append(text[cursor:])
    path.write_text("".join(rebuilt))


def main() -> int:
    MONTH_DIR.mkdir(parents=True, exist_ok=True)
    CANDIDATE_DIR.mkdir(parents=True, exist_ok=True)
    failed: list[str] = []
    for job in JOBS:
        out = filename_for(job)
        if out.exists() and "※Codexが記入" not in out.read_text():
            print(f"SKIP complete {job.date} {job.title}", flush=True)
            continue
        print(f"\n=== {job.date} {job.title} ===", flush=True)
        try:
            candidates = CANDIDATE_DIR / f"{job.label}.json"
            if not candidates.exists():
                candidates = search(job)
            ok = select(job, candidates)
            if not ok:
                failed.append(f"{job.date} {job.title}")
                continue
            fill_push_points(out)
        except Exception as exc:
            print(f"FAILED {job.date}: {exc}", file=sys.stderr, flush=True)
            failed.append(f"{job.date} {job.title}")
    print("\n=== QA ===", flush=True)
    run(["python3", "shared/scripts/check_research_quality.py", "--account", ACCOUNT, "2026-09"], allow_fail=True)
    if failed:
        print("\nFAILED JOBS:", flush=True)
        for item in failed:
            print(f"- {item}", flush=True)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

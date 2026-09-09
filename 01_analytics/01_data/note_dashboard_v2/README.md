# note ダッシュボード v2 データ（2026-09-08 大型アップデート版）

2026-09-08 に note のダッシュボードが刷新され、**インプレッション**と**流入元（リファラ）**が新たに取得できるようになった。
このディレクトリはその新APIから取得した生データ。

対象アカウント: `daily_gadget`（毎日ガジェット通信）
取得日: 2026-09-08

---

## 1. データソース

新ダッシュボード（`https://note.com/dashboard`）は Next.js + Apollo で、**`https://graphql.note.com/graphql` の GraphQL API** を叩いている。
旧 `/api/v1/stats/pv` 系の REST とは別系統。`note_dashboard_stats/` にある旧データとはスキーマが違う。

### 認証

- `Authorization: Bearer <JWT>` ヘッダが必須。Cookie だけでは通らない。
- JWT は **有効期限30分**（`exp - iat = 1800`）。ダッシュボードのフロントが自動で発行・更新している。
- `credentials: 'include'` を付けると **CORS で落ちる**。Apollo はデフォルト（`same-origin`）で送っており、認証はトークンのみ。ここを間違えると `TypeError: Failed to fetch` になる。

### トークンの取り方

発行エンドポイントは特定できていない（`/api/v3/*` の素直な候補はすべて404、localStorage / sessionStorage にも無い）。
現状は **ブラウザで `https://note.com/dashboard` を開き、`window.fetch` をラップして Apollo が送るリクエストの `authorization` ヘッダを拾う**のが確実。
期間セレクタを操作すると Apollo がリクエストを飛ばすので、それでトークンを更新できる。

---

## 2. GraphQL スキーマ（判明分）

`Query` 直下で使えるフィールド:

```
creatorByUrlname / dashboardInsights / dashboardMagazineListConnection
dashboardMembershipPlanListConnection / dashboardNoteListConnection
dashboardNoteReferrersChart / dashboardSummary / dashboardMetricChart
dashboardStatLastUpdatedTimes / dashboardStatsAdvices / dashboardUniversalAdvices
dashboardCreatorTrendTopics / dashboardBannerNotices
noteLikesConnectionByUrlname / notesByKeys / noteArchivesConnectionByUrlname
creatorNotesConnectionByUrlname / creatorNotesByPopularityConnectionByUrlname
userBadgeList / userBadgeByType / membershipList / viewer
```

### enum

| enum | 値 |
|---|---|
| `DashboardPeriodUnit` | `DAY` `WEEK` `MONTH` `YEAR` `ALL` `LAST_7_DAYS` `LAST_28_DAYS` `LAST_365_DAYS` `CUSTOM` |
| `DashboardMetricKind` | `IMPRESSION` `PAGE_VIEW` `LIKE` `COMMENT` `SALES` |
| `DashboardNoteListOrder` | `PUBLISHED_DATE_DESC` `IMPRESSION_COUNT_DESC` `PAGE_VIEW_COUNT_DESC` `LIKE_COUNT_DESC` `COMMENT_COUNT_DESC` `SALES_DESC` |

### 期間指定の注意

`date` は **期間の開始日**。
- `unit: MONTH` + `date: "2026-03-01T00:00:00.000Z"` → 2026年3月単月
- `unit: LAST_28_DAYS` + `date: <今日-28日>` → 直近28日
- `date` に今日を渡して `LAST_28_DAYS` にすると **範囲が潰れて7日/28日/365日が全部同じ値になる**（実際に踏んだ）

`unit: MONTH` は「その月に公開された記事」ではなく **全記事のその月の実績**を返す。だから記事別の月次時系列が取れる。

### `unit: ALL` は当月を含まない（2026-09-09に判明）

**`ALL` は「全期間」ではなく「前月末まで」。** 2アカウントとも、`ALL` の値が
当月を除いた月次合計と厳密に一致した。

| | ALL | 前月までの月次合計 | 当月(2026-09) |
|---|---|---|---|
| daily_gadget | 100,595 | 100,595（一致） | 4,455（ALLに含まれない） |
| gadget_ol | 12,109 | 12,109（一致） | 659（同上） |

**「全期間」と表示・記述しないこと。** 当月を足したいなら `M_<当月>` を別途取って加算する。

### 記事別APIは直近の記事を落とす（2026-09-09に判明）

**`dashboardSummary`（集計）と `dashboardNoteListConnection`（記事別）で対象がずれる。**

2026-09-08に収集した時点で、gadget_ol の9月分は
集計API **659 PV** に対し記事別の合計が **606 PV**（差 **+53**）。
差分は **9/01〜9/05 に公開された記事**で、note の公開API では
`status=published` を返すのに、記事別APIには1本も出てこなかった。

- 収集時点で 2026-08-31 公開（8日前）の記事は記事別APIに載っていた
- 2026-09-01 公開（7日前）は載っていなかった

**対策**: 月次で回すときは、集計APIと記事別APIの合計が一致するかを毎回突合する。
ズレていたら直近の記事が落ちている。**月初に前月分を取ると、前月末の数本が
欠ける可能性がある。** 数日おいてから取り直すか、翌月の収集で埋める。

突合は `shared/scripts/note_dashboard_report.py` が自動で行い、差があれば警告を出す。

### 主要クエリ

```graphql
# 記事別メトリクス（ページング必須。first は 100 まで確認済み）
query($unit:DashboardPeriodUnit!,$date:Datetime!,$endDate:Datetime,
      $order:DashboardNoteListOrder,$first:Int!,$after:String){
  dashboardNoteListConnection(unit:$unit,date:$date,endDate:$endDate,
                              order:$order,first:$first,after:$after){
    pageInfo{ hasNextPage endCursor }
    edges{ node{
      note{ title status publishedAt link{absoluteUrl} }
      metrics{ pageViewCount impressionCount likeCount commentCount salesAmount currency }
    }}
  }}

# 期間サマリ
query($unit:DashboardPeriodUnit!,$date:Datetime!){
  dashboardSummary(unit:$unit,date:$date){
    periodLabel periodUnit startDate endDate lastUpdatedAt
    metrics{ pageViewCount impressionCount likeCount commentCount salesAmount currency }}}

# 流入元（新規）
query($unit:DashboardPeriodUnit!,$date:Datetime!){
  dashboardNoteReferrersChart(unit:$unit,date:$date){
    legend{ name count color }
    pieChart{ labels data colors }
    timeSeriesBarChart{ labels data{ label data color } }}}

# 指標の時系列（MONTH指定なら日次、ALL/365日指定なら月次で返る）
query($unit:DashboardPeriodUnit!,$date:Datetime!,$metric:DashboardMetricKind!){
  dashboardMetricChart(unit:$unit,date:$date,metric:$metric){
    metric granularity points{ label value startDate endDate }}}
```

`dashboardInsights` と `dashboardStatsAdvices` は **union** なのでインラインフラグメントが要る。
- `DashboardInsight` = FollowerGrowth / Like / Comment / PastNoteRediscovery / SharedNote / Last28DaysRevenue / Last28DaysPublishedNoteCount
- `DashboardStatsAdvice` = BannerNotice / DashboardUniversalAdvice / DashboardCreatorTrendTopic

---

## 3. ファイル

| ファイル | 内容 |
|---|---|
| `summary_and_referrers.json` | 15期間（全期間/直近7・28・365日/月次11本）のサマリと流入元内訳 |
| `articles_all_period.csv` | 全期間の記事別 PV・インプレッション・スキ・コメント（303本、タイトル付き） |
| `monthly_page_view_by_article.csv` | 記事別 × 月次の PV 行列（303行 × 11か月） |
| `monthly_impression_by_article.csv` | 記事別 × 月次のインプレッション行列（同上） |

`note_key` で3つのCSVを結合できる。`shared/db/product.sqlite` の `article.note_id` とも突合可能。

### 検算

全期間の記事別合計はダッシュボード表示と一致することを確認済み:
PV 100,595 / インプレッション 413,582 / スキ 1,183 / コメント 3。

---

## 4. 未取得

- 日次の `dashboardMetricChart`（341日分 × 5指標）。取得は可能だが未保存
- `gadget_ol` / `personal` の同データ（別ログインが必要）
- 記事単位の流入元内訳（APIに引数が無く、アカウント単位のみ）

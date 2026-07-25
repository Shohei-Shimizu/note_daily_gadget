import sys
import json
import os
import re
import time

from search_amazon_creators import (
    COUNTRY,
    CREDENTIAL_ID,
    CREDENTIAL_SECRET,
    PARTNER_TAG,
    AmazonCreatorsApi,
    search_product,
)


TASKS = [
    {
        "date": "2026-08-01",
        "title": "実家のご両親へ。安心を贈る「見守り・簡単ガジェット」 7 選",
        "target_count": 7,
        "queries": [
            {"query": "Echo Show 8 第3世代", "include": ["Echo Show 8"], "exclude": ["スタンド", "フィルム"]},
            {"query": "Google Nest Hub 第2世代", "include": ["Google", "Nest Hub"], "exclude": ["スタンド"]},
            {"query": "SwitchBot 見守りカメラ Plus 5MP", "include": ["SwitchBot", "見守りカメラ"], "exclude": ["ブラケット"]},
            {"query": "TP-Link Tapo C210 見守りカメラ", "include": ["Tapo", "C210"], "exclude": ["ブラケット"]},
            {"query": "Tile Mate 探し物トラッカー", "include": ["Tile", "Mate"], "exclude": ["ケース"]},
            {"query": "Apple AirTag", "include": ["AirTag"], "exclude": ["ケース", "ホルダー"]},
            {"query": "SwitchBot ハブ2 スマートリモコン", "include": ["SwitchBot", "ハブ2"], "exclude": ["スタンド"]},
        ],
    },
    {
        "date": "2026-08-02",
        "title": "エアコンなしで涼しく。工事不要で使える「ポータブルクーラー」 6 選",
        "target_count": 6,
        "queries": [
            {"query": "アイリスオーヤマ ポータブルクーラー IPA", "include": ["ポータブルクーラー"], "exclude": ["窓パネル"]},
            {"query": "ナカトミ ミニクーラー MAC", "include": ["ナカトミ", "クーラー"], "exclude": ["ダクト"]},
            {"query": "山善 スポットクーラー YEC", "include": ["スポットクーラー"], "exclude": ["ダクト"]},
            {"query": "MAXZEN スポットエアコン JCF", "include": ["スポットエアコン"], "exclude": ["ダクト"]},
            {"query": "広電 移動式エアコン KEP252R", "include": ["KEP", "移動式"], "exclude": ["アクセサリー", "窓パネル"]},
            {"query": "EENOUR ポータブルエアコン PA800", "include": ["EENOUR"], "exclude": ["ダクト"]},
        ],
    },
    {
        "date": "2026-08-03",
        "title": "写真を AI で補正。夏の思い出を美しくする「編集ソフト」 6 選",
        "target_count": 6,
        "queries": [
            {"query": "Adobe Photoshop Elements 2026", "include": ["Photoshop Elements"], "exclude": ["教本"]},
            {"query": "Adobe Lightroom 写真編集 ソフト", "include": ["Lightroom"], "exclude": ["教本"]},
            {"query": "CyberLink PhotoDirector 365", "include": ["PhotoDirector"], "exclude": ["教本"]},
            {"query": "SILKYPIX Developer Studio Pro", "include": ["SILKYPIX"], "exclude": ["教本"]},
            {"query": "Luminar Neo 写真編集", "include": ["Luminar"], "exclude": ["教本"]},
            {"query": "Corel PaintShop Pro", "include": ["PaintShop"], "exclude": ["教本"]},
        ],
    },
    {
        "date": "2026-08-04",
        "title": "Vlog 制作を AI で時短。動画編集を楽にする「ツール」 6 選",
        "target_count": 6,
        "queries": [
            {"query": "Adobe Premiere Elements 2026", "include": ["Premiere Elements"], "exclude": ["教本"]},
            {"query": "CyberLink PowerDirector 365", "include": ["PowerDirector"], "exclude": ["教本"]},
            {"query": "VEGAS Pro 動画編集 ソフト", "include": ["VEGAS"], "exclude": ["教本"]},
            {"query": "DaVinci Resolve Studio", "include": ["DaVinci"], "exclude": ["教本"]},
            {"query": "Elgato Stream Deck Neo", "include": ["Stream Deck Neo"], "exclude": ["ケース"]},
            {"query": "Loupedeck Live S 編集コントローラー", "include": ["Loupedeck", "Live S"], "exclude": ["ケース"]},
        ],
    },
    {
        "date": "2026-08-05",
        "title": "プールでスマホを使う。最強クラスの「防水ポーチ」 6 選",
        "target_count": 6,
        "queries": [
            {"query": "JOTO 防水ケース スマホ IPX8", "include": ["防水ケース"], "exclude": ["ストラップのみ"]},
            {"query": "Case-Mate 防水ポーチ スマホ", "include": ["防水"], "exclude": ["フィルム"]},
            {"query": "サンワサプライ 防水ケース スマートフォン", "include": ["防水ケース"], "exclude": ["タブレット"]},
            {"query": "ELECOM スマホ 防水ケース IPX8", "include": ["防水ケース"], "exclude": ["フィルム"]},
            {"query": "Lamicall 防水ケース スマホ IPX8", "include": ["防水ケース"], "exclude": ["フィルム"]},
            {"query": "Hamee DIVAID 防水ケース スマホ", "include": ["DIVAID", "防水"], "exclude": ["ストラップ"]},
        ],
    },
    {
        "date": "2026-08-06",
        "title": "帰省の騒音をカット。最強の「ノイキャンヘッドホン」 6 選",
        "target_count": 6,
        "queries": [
            {"query": "Sony WH-1000XM6 ヘッドホン", "include": ["WH-1000XM6"], "exclude": ["ケース"]},
            {"query": "Sony WH-1000XM5 ヘッドホン", "include": ["WH-1000XM5"], "exclude": ["ケース"]},
            {"query": "Bose QuietComfort Ultra Headphones", "include": ["QuietComfort Ultra"], "exclude": ["ケース"]},
            {"query": "Sennheiser MOMENTUM 4 Wireless", "include": ["MOMENTUM 4"], "exclude": ["ケース"]},
            {"query": "Soundcore Space One Pro", "include": ["Space One Pro"], "exclude": ["ケース"]},
            {"query": "JBL Tour One M2", "include": ["Tour One M2"], "exclude": ["ケース"]},
        ],
    },
    {
        "date": "2026-08-07",
        "title": "文章作成を AI で。読書感想文も捗る「執筆サポート」 6 選",
        "target_count": 6,
        "queries": [
            {"query": "キングジム Pomera DM250", "include": ["DM250"], "exclude": ["ケース"]},
            {"query": "キングジム Pomera DM30", "include": ["DM30"], "exclude": ["ケース"]},
            {"query": "iFLYTEK VOITER SR502J", "include": ["VOITER"], "exclude": ["ケース"]},
            {"query": "PLAUD NOTE AI ボイスレコーダー", "include": ["PLAUD NOTE"], "exclude": ["ケース"]},
            {"query": "Notta Memo AI ボイスレコーダー", "include": ["Notta Memo"], "exclude": ["ケース"]},
            {"query": "Boox Palma 電子ペーパー", "include": ["BOOX", "Palma"], "exclude": ["ケース"]},
        ],
    },
    {
        "date": "2026-08-08",
        "title": "カフェ作業の必需品。覗き見を防ぐ「プライバシー幕」 5 選",
        "target_count": 5,
        "queries": [
            {"query": "キングジム デスク用 パーソナルパーティション 8020", "include": ["パーティション"], "exclude": ["交換"]},
            {"query": "コクヨ ワークブース デスク パーティション", "include": ["パーティション"], "exclude": ["交換"]},
            {"query": "ELECOM のぞき見防止 フィルター 14インチ", "include": ["のぞき見防止"], "exclude": ["スマホ"]},
            {"query": "3M プライバシーフィルター 14インチ", "include": ["プライバシーフィルター"], "exclude": ["スマホ"]},
            {"query": "Belkin プライバシーフィルター MacBook", "include": ["プライバシー"], "exclude": ["スマホ"]},
        ],
    },
    {
        "date": "2026-08-09",
        "title": "AI を身につける。日常生活を助ける「ウェアラブル」 6 選",
        "target_count": 6,
        "queries": [
            {"query": "Ray-Ban Meta スマートグラス", "include": ["Ray-Ban", "Meta"], "exclude": ["ケース"]},
            {"query": "XREAL Air 2 Pro", "include": ["XREAL"], "exclude": ["ケース"]},
            {"query": "RayNeo Air 4 Pro ARグラス", "include": ["RayNeo", "Air 4 Pro"], "exclude": ["ケース"]},
            {"query": "Galaxy Ring スマートリング", "include": ["Galaxy Ring"], "exclude": ["ケース"]},
            {"query": "Oura Ring 4 スマートリング", "include": ["Oura Ring"], "exclude": ["ケース"]},
            {"query": "Plaud NotePin AI ウェアラブル", "include": ["NotePin"], "exclude": ["ケース"]},
        ],
    },
    {
        "date": "2026-08-10",
        "title": "旅行から出張まで。ガジェットに強い「バックパック」 7 選",
        "target_count": 7,
        "queries": [
            {"query": "MATEIN ビジネスリュック USB", "include": ["MATEIN"], "exclude": ["カバー"]},
            {"query": "エレコム off toco バックパック", "include": ["off toco"], "exclude": ["ポーチ"]},
            {"query": "ace. ガジェタブル バックパック", "include": ["ガジェタブル"], "exclude": ["カバー"]},
            {"query": "サンワダイレクト ビジネスリュック 200-BAGBP035BK", "include": ["ビジネスリュック"], "exclude": ["カバー"]},
            {"query": "THULE Crossover 2 Backpack", "include": ["Crossover"], "exclude": ["ケース"]},
            {"query": "Incase A.R.C. Commuter Pack", "include": ["Incase"], "exclude": ["ケース"]},
            {"query": "Peak Design トラベルバックパック 30L", "include": ["トラベルバックパック"], "exclude": ["ポーチ"]},
        ],
    },
    {
        "date": "2026-08-11",
        "title": "車内を快適に。後部座席で使える「タブレットホルダー」 6 選",
        "target_count": 6,
        "queries": [
            {"query": "Lamicall 車載 タブレットホルダー 後部座席", "include": ["タブレットホルダー"], "exclude": ["スマホのみ"]},
            {"query": "サンワサプライ 車載 タブレットホルダー 後部座席", "include": ["タブレット"], "exclude": ["スマホのみ"]},
            {"query": "エレコム 車載 タブレットホルダー 後部座席", "include": ["タブレット"], "exclude": ["スマホのみ"]},
            {"query": "UGREEN 車載ホルダー タブレット 後部座席", "include": ["タブレット"], "exclude": ["スマホのみ"]},
            {"query": "Tryone 車載 タブレットホルダー ヘッドレスト", "include": ["タブレット"], "exclude": ["スマホのみ"]},
            {"query": "TFY 車載 タブレットホルダー ヘッドレスト", "include": ["タブレット"], "exclude": ["スマホのみ"]},
        ],
    },
    {
        "date": "2026-08-12",
        "title": "デジタルノマドの装備。ポーチの中身「2026 夏」 7 選",
        "target_count": 7,
        "queries": [
            {"query": "Native Union Stow Organizer ガジェットポーチ", "include": ["Organizer"], "exclude": ["ケーブル"]},
            {"query": "エレコム ガジェットポーチ BMA", "include": ["ガジェットポーチ"], "exclude": ["バッグ"]},
            {"query": "サンワダイレクト ガジェットポーチ 200-BAGIN", "include": ["ガジェットポーチ"], "exclude": ["バッグ"]},
            {"query": "Anker Nano Power Bank USB-C", "include": ["Anker", "Power Bank"], "exclude": ["ケース"]},
            {"query": "CIO NovaPort DUOII 67W", "include": ["CIO", "67W"], "exclude": ["ケーブル"]},
            {"query": "UGREEN Nexode 65W 充電器", "include": ["UGREEN", "65W"], "exclude": ["ケーブル"]},
            {"query": "Anker USB-C 2-in-1 カードリーダー", "include": ["カードリーダー"], "exclude": ["ケース"]},
        ],
    },
    {
        "date": "2026-08-13",
        "title": "MacBook をおしゃれに。理想の「保護ケース・スキン」 6 選",
        "target_count": 6,
        "queries": [
            {"query": "Incase MacBook Air 13 ケース", "include": ["MacBook"], "exclude": ["キーボードカバー"]},
            {"query": "tomtoc MacBook ケース 13インチ", "include": ["MacBook"], "exclude": ["キーボードカバー"]},
            {"query": "Native Union MacBook スリーブ", "include": ["MacBook"], "exclude": ["キーボードカバー"]},
            {"query": "MOFT MacBook ケース スタンド", "include": ["MacBook"], "exclude": ["キーボードカバー"]},
            {"query": "NIMASO MacBook Air ケース", "include": ["MacBook"], "exclude": ["フィルム"]},
            {"query": "wraplus MacBook スキンシール", "include": ["MacBook", "スキン"], "exclude": ["iPad"]},
        ],
    },
    {
        "date": "2026-08-14",
        "title": "ゲリラ豪雨を予測。気圧センサー付き「高機能時計」 5 選",
        "target_count": 5,
        "queries": [
            {"query": "Amazfit T-Rex 3 スマートウォッチ", "include": ["T-Rex 3"], "exclude": ["ベルト", "フィルム"]},
            {"query": "CASIO G-SHOCK RANGEMAN GW-9400", "include": ["RANGEMAN"], "exclude": ["ベルト"]},
            {"query": "Garmin Instinct 3 Tactical", "include": ["Instinct"], "exclude": ["フィルム"]},
            {"query": "Garmin fenix 8 Sapphire", "include": ["fenix"], "exclude": ["フィルム"]},
            {"query": "SUUNTO Vertical Black", "include": ["SUUNTO", "Vertical"], "exclude": ["フィルム"]},
        ],
    },
    {
        "date": "2026-08-15",
        "title": "停電への備えを。ソーラーランタンと「予備電源」 6 選",
        "target_count": 6,
        "queries": [
            {"query": "CARRY THE SUN ソーラーランタン", "include": ["ソーラーランタン"], "exclude": ["ケース"]},
            {"query": "Ledlenser ML4 LEDランタン", "include": ["ML4"], "exclude": ["ケース", "収納バッグ"]},
            {"query": "GENTOS LED ランタン Explorer", "include": ["LEDランタン"], "exclude": ["ケース"]},
            {"query": "Anker Solix C300 DC Portable Power Station", "include": ["Solix", "C300"], "exclude": ["ケース"]},
            {"query": "EcoFlow RIVER 3 ポータブル電源", "include": ["RIVER 3"], "exclude": ["ケース"]},
            {"query": "Jackery ポータブル電源 240 New", "include": ["Jackery", "240"], "exclude": ["ソーラーパネル"]},
        ],
    },
    {
        "date": "2026-08-16",
        "title": "汚れも水洗い OK。防水「スピーカーとキーボード」 6 選",
        "target_count": 6,
        "queries": [
            {"query": "JBL Flip 7 防水 Bluetooth スピーカー", "include": ["JBL", "Flip"], "exclude": ["ケース"]},
            {"query": "Soundcore Boom 2 防水 Bluetooth スピーカー", "include": ["Boom 2"], "exclude": ["ケース"]},
            {"query": "Sony ULT FIELD 1 防水 スピーカー", "include": ["ULT FIELD"], "exclude": ["ケース"]},
            {"query": "バッファロー 防水 キーボード BSKBU520BK", "include": ["防水", "キーボード"], "exclude": ["カバー"]},
            {"query": "エレコム 防水 キーボード", "include": ["防水", "キーボード"], "exclude": ["カバー"]},
            {"query": "サンワサプライ 防水 キーボード", "include": ["防水", "キーボード"], "exclude": ["カバー"]},
        ],
    },
    {
        "date": "2026-08-17",
        "title": "キャンプで家電を使う。大容量「ポータブル電源」 6 選",
        "target_count": 6,
        "queries": [
            {"query": "Anker Solix C1000 ポータブル電源", "include": ["Solix", "C1000"], "exclude": ["ケース"]},
            {"query": "EcoFlow DELTA 3 Plus ポータブル電源", "include": ["DELTA 3"], "exclude": ["ケース"]},
            {"query": "Jackery ポータブル電源 1000 New", "include": ["Jackery", "1000"], "exclude": ["ソーラーパネル"]},
            {"query": "BLUETTI AC180 ポータブル電源", "include": ["BLUETTI", "AC180"], "exclude": ["ケース"]},
            {"query": "JVC BN-RF1100 ポータブル電源", "include": ["BN-RF1100"], "exclude": ["ケース"]},
            {"query": "ALLPOWERS R1500 ポータブル電源", "include": ["ALLPOWERS", "R1500"], "exclude": ["ケース"]},
        ],
    },
    {
        "date": "2026-08-18",
        "title": "夏の眠りを快適に。睡眠を計測する「スマートリング」 6 選",
        "target_count": 6,
        "queries": [
            {"query": "Oura Ring 4 スマートリング", "include": ["Oura Ring"], "exclude": ["ケース"]},
            {"query": "Samsung Galaxy Ring スマートリング", "include": ["Galaxy Ring"], "exclude": ["ケース"]},
            {"query": "COLMI R02 スマートリング", "include": ["COLMI"], "exclude": ["ケース", "サイズキット"]},
            {"query": "Amazfit Helio Ring", "include": ["Helio Ring"], "exclude": ["ケース"]},
            {"query": "RingConn Gen 2 スマートリング", "include": ["RingConn"], "exclude": ["ケース"]},
            {"query": "SOXAI RING 1 スマートリング", "include": ["SOXAI"], "exclude": ["ケース"]},
        ],
    },
    {
        "date": "2026-08-19",
        "title": "登山をシネマティックに。軽量「カメラアクセサリー」 6 選",
        "target_count": 6,
        "queries": [
            {"query": "NEEWER GM34 カメラ クイックリリース", "include": ["NEEWER", "GM34"], "exclude": ["プレートのみ"]},
            {"query": "Ulanzi Falcam F38 Camera Clip", "include": ["F38"], "exclude": ["プレートのみ"]},
            {"query": "PGYTECH Beetle Camera Clip", "include": ["Beetle"], "exclude": ["プレートのみ"]},
            {"query": "HAKUBA カメラ リストストラップ", "include": ["リストストラップ"], "exclude": ["スマホ"]},
            {"query": "JOBY ゴリラポッド 3K", "include": ["ゴリラポッド"], "exclude": ["スマホ"]},
            {"query": "Ulanzi MT-44 カメラ三脚", "include": ["MT-44"], "exclude": ["スマホ"]},
        ],
    },
    {
        "date": "2026-08-20",
        "title": "GoPro を使い倒す。マウントと「必須アクセサリー」 7 選",
        "target_count": 7,
        "queries": [
            {"query": "GoPro Enduro バッテリー HERO13", "include": ["Enduro"], "exclude": ["ケース"]},
            {"query": "GoPro 3-Way 2.0", "include": ["3-Way"], "exclude": ["ケース"]},
            {"query": "GoPro チェストマウント ハーネス", "include": ["チェスト"], "exclude": ["ケース"]},
            {"query": "GoPro Handler Floating Hand Grip", "include": ["Handler"], "exclude": ["ケース"]},
            {"query": "GoPro Media Mod HERO13", "include": ["Media Mod"], "exclude": ["ケース"]},
            {"query": "TELESIN ネックレス式マウント GoPro", "include": ["ネックレス"], "exclude": ["ケース"]},
            {"query": "SanDisk Extreme PRO microSDXC 256GB", "include": ["Extreme PRO", "256GB"], "exclude": ["リーダー"]},
        ],
    },
    {
        "date": "2026-08-21",
        "title": "バーベキューを盛り上げる。タフな「大型スピーカー」 5 選",
        "target_count": 5,
        "queries": [
            {"query": "JBL Boombox 3 Bluetooth スピーカー", "include": ["Boombox"], "exclude": ["ケース"]},
            {"query": "Soundcore Boom 2 Pro Bluetooth スピーカー", "include": ["Boom 2 Pro"], "exclude": ["ケース"]},
            {"query": "Sony ULT FIELD 7 ワイヤレススピーカー", "include": ["ULT FIELD 7"], "exclude": ["ケース"]},
            {"query": "Marshall Kilburn III Bluetooth スピーカー", "include": ["Kilburn"], "exclude": ["ケース"]},
            {"query": "Bose SoundLink Max Portable Speaker", "include": ["SoundLink Max"], "exclude": ["ケース"]},
        ],
    },
    {
        "date": "2026-08-22",
        "title": "運動不足を可視化。自分に合う「活動量計」の選び方 6 選",
        "target_count": 6,
        "queries": [
            {"query": "Fitbit Charge 6", "include": ["Charge 6"], "exclude": ["バンド", "フィルム"]},
            {"query": "HUAWEI Band 10", "include": ["Band 10"], "exclude": ["バンド", "フィルム"]},
            {"query": "Amazfit Bip 6", "include": ["Bip 6"], "exclude": ["バンド", "フィルム", "フイルム"]},
            {"query": "Galaxy Fit3", "include": ["Galaxy Fit3"], "exclude": ["バンド", "フィルム", "フイルム"]},
            {"query": "Garmin Lily 2 Active", "include": ["Lily 2"], "exclude": ["バンド", "フィルム", "フイルム"]},
            {"query": "Redmi Watch 5 Active", "include": ["Redmi Watch 5"], "exclude": ["バンド", "フィルム", "フイルム"]},
        ],
    },
    {
        "date": "2026-08-23",
        "title": "旅の記録を自動化。GPS ロガーと「カメラ連携ギア」5 選",
        "target_count": 5,
        "queries": [
            {"query": "Garmin eTrex SE GPS", "include": ["eTrex"], "exclude": ["ケース", "フィルム"]},
            {"query": "Canon GP-E2 GPSレシーバー", "include": ["GP-E2"], "exclude": ["ケース"]},
            {"query": "Sony GP-VPT2BT シューティンググリップ", "include": ["GP-VPT2BT"], "exclude": ["ケース"]},
            {"query": "Nikon ML-L7 リモコン", "include": ["ML-L7"], "exclude": ["ケース"]},
            {"query": "GoPro Volta バッテリーグリップ", "include": ["Volta"], "exclude": ["ケース", "フィルム", "フイルム"]},
        ],
    },
    {
        "date": "2026-08-24",
        "title": "車中泊で仕事。車内を快適にする「インバーター」 6 選",
        "target_count": 6,
        "queries": [
            {"query": "BESTEK インバーター 300W 正弦波", "include": ["インバーター"], "exclude": ["ケーブル"]},
            {"query": "BAL インバーター 400W", "include": ["インバーター"], "exclude": ["ケーブル"]},
            {"query": "Meltec インバーター 300W", "include": ["インバーター"], "exclude": ["ケーブル"]},
            {"query": "セルスター インバーター 500W", "include": ["インバーター"], "exclude": ["ケーブル"]},
            {"query": "LVYUAN インバーター 正弦波 500W", "include": ["インバーター"], "exclude": ["ケーブル"]},
            {"query": "EDECOA インバーター 正弦波 1000W", "include": ["インバーター"], "exclude": ["ケーブル"]},
        ],
    },
    {
        "date": "2026-08-25",
        "title": "海外コンセントに対応。全世界対応「変換プラグ」 5 選",
        "target_count": 5,
        "queries": [
            {"query": "カシムラ 海外変換プラグ USB-C", "include": ["変換プラグ"], "exclude": ["ケース"]},
            {"query": "サンワサプライ 海外電源変換アダプタ", "include": ["変換"], "exclude": ["ケース"]},
            {"query": "ROAD WARRIOR ゴーコンW2", "include": ["ゴーコン"], "exclude": ["ケース"]},
            {"query": "MOMAX 変換プラグ 70W", "include": ["変換プラグ"], "exclude": ["ケース"]},
            {"query": "Zendure Passport III 変換プラグ", "include": ["Passport"], "exclude": ["ケース"]},
        ],
    },
    {
        "date": "2026-08-26",
        "title": "夏バテを計測。自律神経を整える「最新デバイス」 5 選",
        "target_count": 5,
        "queries": [
            {"query": "Oura Ring 4 スマートリング", "include": ["Oura Ring"], "exclude": ["ケース"]},
            {"query": "SOXAI RING 1.1 スマートリング", "include": ["SOXAI"], "exclude": ["ケース"]},
            {"query": "Garmin Venu 3 スマートウォッチ", "include": ["Venu 3"], "exclude": ["バンド", "フィルム"]},
            {"query": "Fitbit Sense 2", "include": ["Sense 2"], "exclude": ["バンド", "フィルム"]},
            {"query": "Pulsetto 迷走神経 ウェルネスデバイス", "include": ["Pulsetto"], "exclude": ["ケース"]},
        ],
    },
    {
        "date": "2026-08-27",
        "title": "旅行の防犯。スキミングを防ぐ「RFID ブロッキングウォレット」 6 選",
        "target_count": 6,
        "queries": [
            {"query": "Bellroy Travel Wallet RFID", "include": ["RFID"], "exclude": ["ケース"]},
            {"query": "SECRID Cardprotector RFID", "include": ["SECRID"], "exclude": ["ケース"]},
            {"query": "abrAsus 薄い財布 RFID", "include": ["財布"], "exclude": ["ケース"]},
            {"query": "TRAVANDO RFID 財布", "include": ["RFID"], "exclude": ["ケース"]},
            {"query": "ZERO GRID RFID パスポートケース", "include": ["RFID"], "exclude": ["ケースのみ"]},
            {"query": "TUMI RFID ウォレット", "include": ["RFID"], "exclude": ["ケース"]},
        ],
    },
    {
        "date": "2026-08-28",
        "title": "スポーツの秋に向けて。ジムで使いたい「時計とイヤホン」 7 選",
        "target_count": 7,
        "queries": [
            {"query": "Garmin Forerunner 265", "include": ["Forerunner 265"], "exclude": ["バンド", "フィルム"]},
            {"query": "HUAWEI WATCH FIT 4 Pro", "include": ["WATCH FIT 4"], "exclude": ["バンド", "フィルム", "フイルム", "整備済み"]},
            {"query": "Fitbit Charge 6", "include": ["Charge 6"], "exclude": ["バンド", "フィルム"]},
            {"query": "Shokz OpenRun Pro 2", "include": ["OpenRun Pro 2"], "exclude": ["ケース"]},
            {"query": "Soundcore Sport X20", "include": ["Sport X20"], "exclude": ["ケース"]},
            {"query": "Jabra Elite 8 Active Gen 2", "include": ["Elite 8 Active"], "exclude": ["ケース"]},
            {"query": "JBL Endurance Race 2", "include": ["Endurance Race"], "exclude": ["ケース"]},
        ],
    },
    {
        "date": "2026-08-29",
        "title": "ホテルの Wi-Fi を高速化。有線 LAN「変換ルーター」 5 選",
        "target_count": 5,
        "queries": [
            {"query": "GL.iNet Beryl AX GL-MT3000", "include": ["GL-MT3000"], "exclude": ["ケース"]},
            {"query": "GL.iNet Beryl 7 GL-MT3600BE", "include": ["GL-MT3600BE"], "exclude": ["ケース"]},
            {"query": "TP-Link TL-WR902AC トラベルルーター", "include": ["WR902AC"], "exclude": ["ケース"]},
            {"query": "TP-Link WR802N トラベルルーター", "include": ["WR802N"], "exclude": ["ケース"]},
            {"query": "BUFFALO WMR-433W2 トラベルルーター", "include": ["WMR-433W2"], "exclude": ["ケース"]},
        ],
    },
    {
        "date": "2026-08-30",
        "title": "涼しくなったら走り出す。最新「ランニングウォッチ」 6 選",
        "target_count": 6,
        "queries": [
            {"query": "Garmin Forerunner 970", "include": ["Forerunner 970"], "exclude": ["バンド", "フィルム"]},
            {"query": "Garmin Forerunner 265", "include": ["Forerunner 265"], "exclude": ["バンド", "フィルム"]},
            {"query": "COROS PACE 3 GPSウォッチ", "include": ["PACE 3"], "exclude": ["バンド", "フィルム", "フイルム"]},
            {"query": "Polar Vantage M3", "include": ["Vantage M3"], "exclude": ["バンド", "フィルム"]},
            {"query": "SUUNTO RUN GPS スポーツウォッチ", "include": ["SUUNTO RUN"], "exclude": ["バンド", "フィルム", "フイルム"]},
            {"query": "Amazfit Cheetah Pro", "include": ["Cheetah"], "exclude": ["バンド", "フィルム"]},
        ],
    },
    {
        "date": "2026-08-31",
        "title": "8 月のベストバイ。買ってよかった「夏の終わりギア」 8 選",
        "target_count": 8,
        "queries": [
            {"query": "Anker Solix C300 DC Portable Power Station", "include": ["Solix", "C300"], "exclude": ["ケース"]},
            {"query": "Oura Ring 4 スマートリング", "include": ["Oura Ring"], "exclude": ["ケース"]},
            {"query": "JBL Flip 7 防水 Bluetooth スピーカー", "include": ["JBL", "Flip"], "exclude": ["ケース"]},
            {"query": "GoPro 3-Way 2.0", "include": ["3-Way"], "exclude": ["ケース"]},
            {"query": "Garmin Forerunner 265", "include": ["Forerunner 265"], "exclude": ["バンド", "フィルム"]},
            {"query": "MATEIN ビジネスリュック USB", "include": ["MATEIN"], "exclude": ["カバー"]},
            {"query": "EENOUR ポータブルエアコン PA800", "include": ["EENOUR"], "exclude": ["ダクト"]},
            {"query": "GL.iNet Beryl AX GL-MT3000", "include": ["GL-MT3000"], "exclude": ["ケース"]},
        ],
    },
]


def main():
    requested_dates = set(sys.argv[1:]) if len(sys.argv) > 1 else None
    tasks = [
        task
        for task in TASKS
        if requested_dates is None or task["date"] in requested_dates
    ]
    if not tasks:
        raise SystemExit("No matching tasks.")
    api = AmazonCreatorsApi(
        credential_id=CREDENTIAL_ID,
        credential_secret=CREDENTIAL_SECRET,
        tag=PARTNER_TAG,
        country=COUNTRY,
        version="2.3",
    )
    for task in tasks:
        run_task(api, task)


def normalize_query_entry(entry):
    if isinstance(entry, str):
        return {"query": entry, "include": [], "exclude": []}
    return {
        "query": entry["query"],
        "include": entry.get("include", []),
        "exclude": entry.get("exclude", []),
    }


def audit_item(item):
    asin = item.get("asin", "")
    url = item.get("url", "")
    match = re.search(r"https://www\.amazon\.co\.jp/dp/([A-Z0-9]{10})\?tag=daily-gadget-22&linkCode=osi", url)
    if not match:
        raise ValueError(f"invalid amazon url: {url}")
    if match.group(1) != asin:
        raise ValueError(f"asin mismatch: url={match.group(1)} item={asin}")


def run_task(api, task):
    selected_items = []
    seen_asins = set()
    errors = []

    for raw_query in task["queries"]:
        query_entry = normalize_query_entry(raw_query)
        query = query_entry["query"]
        result = search_product(
            api,
            query,
            include=query_entry["include"],
            exclude=query_entry["exclude"],
            item_count=5,
        )
        if not result:
            errors.append({"query": query, "error": "no usable item found"})
            time.sleep(1)
            continue
        if not result.get("asin") or result["asin"] in seen_asins:
            errors.append({"query": query, "error": "missing asin or duplicate asin"})
            time.sleep(1)
            continue
        try:
            audit_item(result)
        except ValueError as exc:
            errors.append({"query": query, "error": str(exc)})
            time.sleep(1)
            continue
        selected_items.append(result)
        seen_asins.add(result["asin"])
        time.sleep(1)

    payload = {
        "date": task["date"],
        "title": task["title"],
        "queries": task["queries"],
        "selection_policy": {
            "default_tiers": {
                "tier1": "review_count >= 500 and star_rating >= 4.0",
                "tier2": "review_count >= 100 and star_rating >= 3.5",
                "tier3": "review_count >= 30 and star_rating >= 3.0",
            },
            "applied_tier": "fallback",
            "fallback_applied": True,
            "fallback_reason": "レビュー情報をCreators APIから安定取得できないため、Creators API検索上位 + 除外ワード + テーマ適合で選定",
            "fallback_policy": "Creators API検索上位・除外ワード排除・メーカー重複制限（特集テーマ除く）・URL/ASIN一致検証",
        },
        "search_execution": {
            "script": "05_script/run_research_august.py via 05_script/search_amazon_creators.py (Amazon Creators API)",
            "partner_tag": PARTNER_TAG,
            "status": "success" if len(selected_items) >= task["target_count"] else "partial",
            "errors": errors,
        },
        "target_count": task["target_count"],
        "fetched_count": len(selected_items),
        "dedup_count": 0,
        "selected_count": len(selected_items),
        "selected_items": selected_items,
        "all_candidates": [],
    }

    output_dir = os.path.join("06_research", task["date"][:7])
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, f"{task['date']}_research_data.json")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2, ensure_ascii=False)

    print(f"{task['date']}: {len(selected_items)}/{task['target_count']} saved to {output_path}")
    return payload


if __name__ == "__main__":
    main()

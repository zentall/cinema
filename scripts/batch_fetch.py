#!/usr/bin/env python3
"""
Movie Database Batch Fetch Script

TMDB APIから映画データを取得し、JSONファイルを生成します。
GitHub Actionsで定期実行することを想定しています。
"""

import json
import os
import sys
import argparse
from datetime import datetime, timedelta
from pathlib import Path

# .envファイルから環境変数を読み込み
from dotenv import load_dotenv

load_dotenv(Path(__file__).parent.parent / "config" / ".env")

# プロジェクトルートをPythonパスに追加
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from scripts.fetch_movie import fetch_movies_by_date


def main():
    """メイン処理"""
    parser = argparse.ArgumentParser(
        description="Fetch movies from TMDB API for a specified date range."
    )
    parser.add_argument(
        "--start-date",
        type=str,
        help="Start date in YYYY-MM-DD format. Defaults to first day of current month.",
    )
    parser.add_argument(
        "--end-date",
        type=str,
        help="End date in YYYY-MM-DD format. Defaults to last day of current month.",
    )
    args = parser.parse_args()

    try:
        # 現在の日付を取得
        now = datetime.now()

        # 開始日と終了日を設定
        if args.start_date:
            start_date = args.start_date
        else:
            start_date = now.replace(day=1).strftime("%Y-%m-%d")

        if args.end_date:
            end_date = args.end_date
        else:
            # 当月の最終日を計算（翌月の1日から1日引く）
            if now.month == 12:
                next_month = now.replace(year=now.year + 1, month=1, day=1)
            else:
                next_month = now.replace(month=now.month + 1, day=1)
            end_date = (next_month - timedelta(days=1)).strftime("%Y-%m-%d")

        print(f"Fetching movies from {start_date} to {end_date}")

        # 映画データを取得
        movies = fetch_movies_by_date(start_date, end_date)

        if not movies:
            print("Warning: No movies found for the specified period")
            return True

        # 出力ファイル名を生成
        if args.start_date or args.end_date:
            # 指定された期間の場合、開始日と終了日を使う
            start_obj = datetime.strptime(start_date, "%Y-%m-%d")
            end_obj = datetime.strptime(end_date, "%Y-%m-%d")
            output_filename = f"movies_raw_{start_obj.strftime('%Y_%m_%d')}_to_{end_obj.strftime('%Y_%m_%d')}.json"
        else:
            # デフォルトの場合、当月
            output_filename = f"movies_raw_{now.year}_{now.month:02d}.json"
        output_path = project_root / "data" / output_filename

        # dataディレクトリがなければ作成
        output_path.parent.mkdir(parents=True, exist_ok=True)

        # JSONファイルを書き込み（TMDBの生データ）
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(movies, f, ensure_ascii=False, indent=2)

        print(f"Successfully generated {len(movies)} movies to {output_path}")

        # 古いファイルをクリーンアップ（オプション、デフォルトの場合のみ）
        if not args.start_date and not args.end_date:
            cleanup_old_files(project_root / "data", now)

        return True

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return False


def cleanup_old_files(data_dir: Path, current_date: datetime, keep_months: int = 3):
    """古いJSONファイルを削除（生データと表示用データ両方）"""
    try:
        current_year_month = current_date.strftime("%Y_%m")

        # movies_*.json と movies_raw_*.json の両方をクリーンアップ
        for pattern in ["movies_*.json", "movies_raw_*.json"]:
            for json_file in data_dir.glob(pattern):
                # ファイル名から年月を抽出
                parts = json_file.stem.split("_")
                # movies_raw_YYYY_MM.json または movies_YYYY_MM.json
                year_month_idx = 2 if "raw" in json_file.stem else 1

                if len(parts) >= year_month_idx + 2:
                    file_year_month = (
                        f"{parts[year_month_idx]}_{parts[year_month_idx + 1]}"
                    )

                    # 現在の月と比較して古いファイルを削除
                    if file_year_month < current_year_month:
                        # 保持期間内のファイルのみ残す
                        file_date = datetime.strptime(file_year_month, "%Y_%m")
                        months_diff = (current_date.year - file_date.year) * 12 + (
                            current_date.month - file_date.month
                        )

                        if months_diff > keep_months:
                            json_file.unlink()
                            print(f"Cleaned up old file: {json_file.name}")

    except Exception as e:
        print(f"Warning: Failed to cleanup old files: {e}")


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

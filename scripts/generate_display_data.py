#!/usr/bin/env python3
"""
生データから表示用データを生成するスクリプト

movies_raw_YYYY_MM.json から movies_YYYY_MM.json を生成
"""

import json
import sys
from pathlib import Path
from datetime import datetime


def get_japanese_latest_release(release_dates_data):
    """日本の劇場公開日を取得（type=3のみ）

    劇場公開 (type=3) がある場合は、その最新日を返す
    劇場公開がない場合は None を返す（フィルタリング対象）
    """
    jp_release_date = None
    jp_release_type = None

    for country in release_dates_data:
        if country.get("iso_3166_1") == "JP":
            jp_releases = country.get("release_dates", [])

            # 劇場公開（type 3）のみを対象
            theatrical = [r for r in jp_releases if r.get("type") == 3]
            if theatrical:
                # 最新の劇場公開日
                latest = max(theatrical, key=lambda x: x.get("release_date", ""))
                jp_release_date = latest.get("release_date", "").split("T")[0]
                jp_release_type = 3
            break

    return jp_release_date, jp_release_type


def get_youtube_trailer(videos):
    """動画リストからYouTubeトレーラーを取得"""
    for v in videos:
        if v.get("site") == "YouTube" and v.get("type") in ("Trailer", "Teaser"):
            return f"https://www.youtube.com/watch?v={v.get('key')}"
    return None


def get_credits_info(credits_data):
    """クレジット情報から監督と主要キャストを取得"""
    directors = []
    cast = []

    if not credits_data:
        return directors, cast

    # 監督を取得
    crew = credits_data.get("crew", [])
    for person in crew:
        if person.get("job") == "Director":
            directors.append(
                {
                    "id": person.get("id"),
                    "name": person.get("name"),
                    "profilePath": person.get("profile_path"),
                }
            )

    # 主要キャスト（上位5名）を取得
    cast_list = credits_data.get("cast", [])
    for person in cast_list[:5]:
        cast.append(
            {
                "id": person.get("id"),
                "name": person.get("name"),
                "character": person.get("character"),
                "profilePath": person.get("profile_path"),
            }
        )

    return directors, cast


def get_credits_info(credits_data):
    """クレジット情報から監督と主要キャストを取得"""
    directors = []
    cast = []

    if not credits_data:
        return directors, cast

    # 監督を取得
    crew = credits_data.get("crew", [])
    for person in crew:
        if person.get("job") == "Director":
            directors.append(
                {
                    "id": person.get("id"),
                    "name": person.get("name"),
                    "profilePath": person.get("profile_path"),
                }
            )

    # 主要キャスト（上位5名）を取得
    cast_list = credits_data.get("cast", [])
    for person in cast_list[:5]:
        cast.append(
            {
                "id": person.get("id"),
                "name": person.get("name"),
                "character": person.get("character"),
                "profilePath": person.get("profile_path"),
            }
        )

    return directors, cast


def transform_movie_data(raw_movie):
    """生データを表示用データに変換"""
    movie_id = raw_movie.get("id")

    # 画像URL
    poster_path = raw_movie.get("poster_path")
    backdrop_path = raw_movie.get("backdrop_path")

    poster_url = (
        f"https://image.tmdb.org/t/p/w500{poster_path}" if poster_path else None
    )
    backdrop_url = (
        f"https://image.tmdb.org/t/p/original{backdrop_path}" if backdrop_path else None
    )

    # 日本の最新リリース日
    release_dates_data = raw_movie.get("release_dates", {}).get("results", [])
    jp_release_date, jp_release_type = get_japanese_latest_release(release_dates_data)

    # トレーラーURL
    videos = raw_movie.get("videos", {}).get("results", [])
    trailer_url = get_youtube_trailer(videos)

    # 監督とキャスト情報
    credits_data = raw_movie.get("credits")
    directors, cast = get_credits_info(credits_data)

    return {
        "id": movie_id,
        "title": raw_movie.get("title"),
        "originalTitle": raw_movie.get("original_title"),
        "overview": raw_movie.get("overview"),
        "releaseDate": raw_movie.get("release_date"),
        "jpReleaseDate": jp_release_date,
        "jpReleaseType": jp_release_type,
        "runtime": raw_movie.get("runtime"),
        "genres": raw_movie.get("genres", []),
        "voteAverage": raw_movie.get("vote_average"),
        "voteCount": raw_movie.get("vote_count"),
        "popularity": raw_movie.get("popularity"),
        "adult": raw_movie.get("adult", False),
        "posterUrl": poster_url,
        "backdropUrl": backdrop_url,
        "trailerUrl": trailer_url,
        "homepage": raw_movie.get("homepage"),
        "tagline": raw_movie.get("tagline"),
        "status": raw_movie.get("status"),
        "directors": directors,
        "cast": cast,
    }


def main():
    """メイン処理"""
    if len(sys.argv) > 1:
        raw_file = Path(sys.argv[1])
    else:
        # デフォルトは当月のファイル
        now = datetime.now()
        raw_file = (
            Path(__file__).parent.parent
            / "data"
            / f"movies_raw_{now.year}_{now.month:02d}.json"
        )

    if not raw_file.exists():
        print(f"Error: {raw_file} not found")
        return False

    # 生データを読み込み
    with open(raw_file, "r", encoding="utf-8") as f:
        raw_movies = json.load(f)

    print(f"Processing {len(raw_movies)} movies from {raw_file.name}")

    # 表示用データに変換
    display_movies = []
    filtered_count = 0
    for raw_movie in raw_movies:
        try:
            display_movie = transform_movie_data(raw_movie)

            # 劇場公開日がない映画は除外
            if (
                display_movie["jpReleaseDate"] is None
                or display_movie["jpReleaseType"] != 3
            ):
                filtered_count += 1
                print(
                    f"  Filtered out: {display_movie['title']} (no theatrical release)"
                )
                continue

            display_movies.append(display_movie)
        except Exception as e:
            print(f"Error processing movie {raw_movie.get('id')}: {e}")
            continue

    print(f"Filtered out {filtered_count} movies without theatrical release")

    # 出力ファイル名を生成（movies_raw_xxx.json -> movies_xxx.json）
    output_file = raw_file.parent / raw_file.name.replace("movies_raw_", "movies_")

    # JSONファイルを書き込み
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(display_movies, f, ensure_ascii=False, indent=2)

    print(f"Successfully generated {len(display_movies)} movies to {output_file}")
    return True


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

from scripts.api import tmdb


def fetch_movies_by_date(min_date="2025-12-01", max_date="2025-12-31"):
    """公開日の範囲で映画を取得し、TMDBの生データをそのまま返す"""

    # 日本での公開日で絞り込む
    params = {
        "release_date.gte": min_date,
        "release_date.lte": max_date,
        "sort_by": "release_date.asc",
        "language": "ja-JP",
        "region": "JP",
        "with_release_type": "2|3",  # 2=劇場限定公開, 3=劇場公開
    }

    # 全ページを取得
    all_movies = []
    page = 1
    while True:
        params["page"] = page
        result = tmdb.discover_movies(**params)
        movies_raw = result.get("results", [])

        if not movies_raw:
            break

        all_movies.extend(movies_raw)

        # 最後のページかチェック
        if page >= result.get("total_pages", 1):
            break

        page += 1
        print(f"Fetching page {page}...")

    print(f"Found {len(all_movies)} movies in total")
    movies = []

    for m in all_movies:
        movie_id = m.get("id")
        if not movie_id:
            continue

        # 詳細情報を一度に取得（日本語、リリース日、動画情報）
        try:
            detail = tmdb.movie(
                movie_id,
                language="ja-JP",
                append_to_response="release_dates,videos,credits",
            )
            movies.append(detail)
            print(f"Fetched: {detail.get('title', 'Unknown')}")
        except Exception as e:
            print(f"Error fetching movie {movie_id}: {e}")
            continue

    return movies


def main():
    movies = fetch_movies_by_date("2025-12-01", "2025-12-31")
    import json

    print(f"Fetched {len(movies)} movies")
    with open("movies_december_2025.json", "w", encoding="utf-8") as f:
        json.dump(movies, f, ensure_ascii=False, indent=2)
    print("Saved to movies_december_2025.json")


if __name__ == "__main__":
    main()

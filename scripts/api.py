import requests
import dotenv
import os


class TMDBApi:
    def __init__(self, api_key, base_url="https://api.themoviedb.org/3"):
        self.api_key = api_key
        self.base_url = base_url

    def _request(self, method: str, path: str, params: dict = None):
        if params is None:
            params = {}

        # 共通のパラメータ
        params["api_key"] = self.api_key

        # デフォルトで日本語を取得
        if "language" not in params:
            params["language"] = "ja-JP"

        url = f"{self.base_url}{path}"

        response = requests.request(method, url, params=params, timeout=10)
        response.raise_for_status()  # エラー時は例外
        return response.json()

    def videos(self, movie_id, **params):
        method = "GET"
        path = f"/movie/{movie_id}/videos"
        return self._request(method, path, params)

    def discover_movies(self, **params):
        method = "GET"
        path = "/discover/movie"
        return self._request(method, path, params)

    def movie(self, movie_id, **params):
        method = "GET"
        path = f"/movie/{movie_id}"
        return self._request(method, path, params)

    def release_dates(self, movie_id, **params):
        method = "GET"
        path = f"/movie/{movie_id}/release_dates"
        return self._request(method, path, params)

    def credits(self, movie_id, **params):
        method = "GET"
        path = f"/movie/{movie_id}/credits"
        return self._request(method, path, params)


dotenv.load_dotenv()
tmdb = TMDBApi(api_key=os.environ["TMDB_API_KEY"])

if __name__ == "__main__":
    from pprint import pprint

    # min_date = "2025-12-01"
    # max_date = "2025-12-31"
    # params = {
    #     "primary_release_date.gte": min_date,
    #     "primary_release_date.lte": max_date,
    #     "sort_by": "primary_release_date.asc",
    #     "language": "ja-JP",
    #     "region": "JP",
    #     "include_movie": True,
    # }

    # movies_raw = tmdb.discover_movies(params=params).get("results", [])
    movies_raw = tmdb.release_dates(1084242, language="ja-JP")
    pprint(movies_raw)

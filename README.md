# Movie Database Application

TMDB (The Movie Database) APIから映画データを定期的に取得し、静的Webページとして公開するアプリケーションです。

## 特徴

- 🎬 **自動データ更新**: GitHub Actionsで毎週映画データを自動取得
- 📱 **レスポンシブデザイン**: モバイル対応の映画ポスターグリッド
- 🎥 **ビデオ埋め込み**: YouTubeトレイラーのボトムシート表示
- 🚀 **高速配信**: GitHub Pagesによる静的ホスティング

## 技術スタック

- **Backend**: Python 3.9+ (データ取得)
- **Frontend**: HTML5/CSS3/JavaScript (表示)
- **API**: TMDB API v3
- **CI/CD**: GitHub Actions
- **Hosting**: GitHub Pages

## フォルダ構成

```
movie/
├── 📁 scripts/              # Pythonスクリプト
│   ├── __init__.py
│   ├── api.py              # TMDB APIクライアント
│   ├── fetch_movie.py      # データ取得ロジック
│   ├── batch_fetch.py      # バッチ実行スクリプト
│   └── generate_display_data.py  # 表示用データ生成
├── 📁 data/                # JSONデータ
│   ├── movies_raw_*.json   # TMDB生データ
│   └── movies_*.json       # 表示用データ
├── 📁 public/              # 公開ファイル（GitHub Pages）
│   ├── index.html          # メインHTML
│   ├── styles.css          # CSSスタイル
│   └── script.js           # JavaScript
├── 📁 config/              # 設定ファイル
│   ├── settings.json       # アプリ設定
│   └── .env               # 環境変数（APIキー）
├── 📁 docs/               # ドキュメント
│   └── ARCHITECTURE.md     # アーキテクチャ設計
├── 📁 .github/workflows/   # GitHub Actions
│   └── update-movies.yml
├── .gitignore
├── pyproject.toml
├── uv.lock
└── README.md
```

## セットアップ

### 1. リポジトリのクローン
```bash
git clone https://github.com/your-username/movie-database.git
cd movie-database
```

### 2. Python環境のセットアップ
```bash
# uvを使用する場合
curl -LsSf https://astral.sh/uv/install.sh | sh
uv sync

# またはpipを使用する場合
pip install -r requirements.txt
```

### 3. TMDB APIキーの設定
1. [TMDB](https://www.themoviedb.org/) でアカウントを作成
2. APIキーを取得
3. `config/.env` ファイルを作成:
   ```
   TMDB_API_KEY=your_api_key_here
   ```

### 4. GitHub Pagesの設定
1. リポジトリの **Settings > Pages**
2. **Source**: "GitHub Actions"
3. ワークフローが自動的にデプロイを実行

### 5. GitHub Secretsの設定
リポジトリの **Settings > Secrets and variables > Actions** で:
- `TMDB_API_KEY`: TMDB APIキー

## ローカル開発

### データ取得のテスト
```bash
# 当月の映画データを取得（デフォルト）
uv run python scripts/batch_fetch.py

# 指定した期間の映画データを取得
uv run python scripts/batch_fetch.py --start-date 2025-12-01 --end-date 2025-12-31

# 単体テスト
uv run python scripts/fetch_movie.py
```

### ローカルサーバー起動
```bash
cd public
python -m http.server 8000
# http://localhost:8000 でアクセス
```

## デプロイメント

### 自動デプロイ
- 毎週月曜日 00:00 UTCに自動実行
- 手動実行: GitHub Actionsタブから "update-movies" を実行

### 手動デプロイ
```bash
# データ更新
uv run python scripts/batch_fetch.py

# コミット
git add public/movies_*.json
git commit -m "Update movie data"
git push
```

## API使用量

- **無料枠**: 1秒あたり50リクエスト、1日あたり500リクエスト
- **現在の使用量**: 約100-200リクエスト/実行（映画50-100件）
- **監視**: GitHub Actionsログで確認

## トラブルシューティング

### データが更新されない
1. GitHub Actionsログを確認
2. TMDB APIキーが正しいか確認
3. `.env` ファイルの場所を確認

### ページが表示されない
1. GitHub Pages設定を確認
2. `public/` フォルダの内容を確認
3. ブラウザのキャッシュをクリア

### APIエラー
1. APIキーの有効性を確認
2. レート制限に達していないか確認
3. TMDBのステータスページを確認

## 拡張計画

- 🔍 **検索機能**: 映画タイトル検索
- ⭐ **評価機能**: ユーザーレビュー
- 📊 **統計**: 人気映画ランキング
- 🌐 **多言語**: 英語/日本語対応

## ライセンス

MIT License

## 貢献

1. Fork this repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

*最終更新: 2025-12-14*

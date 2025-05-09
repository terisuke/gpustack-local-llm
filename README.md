# GPUStack Local LLM Chatbot

このプロジェクトは、GPUStackを使用してローカル環境で動作するLLMチャットボットを構築するものです。GPUStackの基本的な機能であるモデルデプロイ、OpenAI互換APIの利用、Playground UIでのモデル管理を学ぶことができます。

## プロジェクトの概要

- GPUStackを使用してローカルに小〜中規模のLLMモデルをデプロイ
- GPUStackのOpenAI互換APIを利用したチャットインターフェースの構築
- Streamlitを使用した簡易WebUIの開発
- トークン使用量やAPIリクエスト数などのリソース監視方法の学習
- 依存関係の自動管理とセッション管理

## 構成

```
gpustack-local-llm/
├── README.md           # プロジェクト概要
├── app/                # Streamlitアプリケーション
│   ├── app.py          # メインアプリケーション
│   ├── GPUStack_API_Example.ipynb # API使用例
│   └── requirements.txt # アプリケーションの依存関係
├── scripts/            # インストールスクリプトとユーティリティ
│   ├── install.sh      # GPUStack インストールスクリプト
│   ├── fix_permissions.sh # 権限修正スクリプト
│   ├── start_gpustack.sh # GPUStack起動スクリプト
│   ├── update_dependencies.sh # 依存関係更新スクリプト
│   ├── session_start.sh # セッション起動スクリプト
│   └── model_setup.py  # モデルのセットアップスクリプト
└── docs/               # ドキュメント
    ├── setup_guide.md  # セットアップガイド
    └── usage_guide.md  # 使用方法ガイド
```

## 前提条件

- macOS または Linux 環境
- Python 3.10+ (GPUStackの要件)
- CUDA対応GPUまたはApple Siliconチップ (M1/M2/M3/M4シリーズ)

## セットアップ手順

1. リポジトリのクローン:
```bash
git clone https://github.com/terisuke/gpustack-local-llm.git
cd /Users/yourdirectory/gpustack-local-llm
```

2. GPUStackのインストール:
```bash
./scripts/install.sh
```

3. 権限の修正（必要な場合）:
```bash
./scripts/fix_permissions.sh
```

4. セッションの開始:
```bash
./scripts/session_start.sh
```

このスクリプトは以下の処理を行います：
- Gitリポジトリの更新確認
- 依存関係の更新
- GPUStackの起動

5. ブラウザで http://localhost:80 にアクセスしてGPUStackのWebインターフェースを開きます。

## 使用方法

詳細な使用方法は [使用方法ガイド](docs/usage_guide.md) を参照してください。

## 依存関係の管理

プロジェクトの依存関係は以下の方法で管理できます：

### 手動での更新
```bash
./scripts/update_dependencies.sh
```

### セッション起動時の自動更新
```bash
./scripts/session_start.sh
```

## 注意事項

- GPUStackの起動には`source`コマンドを使用してください（仮想環境の有効化のため）
- ポート80、10150、10151が使用可能であることを確認してください
- 初回起動時や権限エラーが発生した場合は`fix_permissions.sh`を実行してください
- 依存関係の更新後はGPUStackの再起動が必要です

## ライセンス

MIT License

# GPUStack セットアップガイド

このガイドでは、macOS環境（Apple Silicon）でGPUStackをセットアップする手順を説明します。

## 1. 前提条件

### 通常のインストール
- macOS（M1/M2/M3/M4 チップ搭載Mac）
- Homebrew がインストールされていること
- Python 3.10 以上がインストールされていること（GPUStackの要件）
- 十分なディスク容量（20GB以上推奨）

### Dockerを使用する場合
- Docker Desktop がインストールされていること
- 十分なディスク容量（20GB以上推奨）

## 2. プロジェクトのセットアップ

```bash
# プロジェクトディレクトリに移動
cd /Users/yourdirectory/gpustack-local-llm

# インストールスクリプトを実行
./scripts/install.sh
```

このスクリプトは以下の処理を行います：
- Python 3.10以上の確認
- 仮想環境の作成
- 必要なパッケージのインストール

## 3. 依存関係の管理

プロジェクトの依存関係は以下の方法で管理できます：

### 手動での更新
```bash
# 依存関係を更新
./scripts/update_dependencies.sh
```

このスクリプトは以下の処理を行います：
- pipのアップグレード
- GPUStackの更新
- アプリケーションの依存関係の更新

### セッション起動時の自動更新
```bash
# セッションを開始（Gitの更新確認と依存関係の更新を含む）
./scripts/session_start.sh
```

このスクリプトは以下の処理を行います：
- Gitリポジトリの更新確認
- 依存関係の更新
- GPUStackの起動

## 4. 権限の設定

GPUStackの実行に必要な権限を設定します：

```bash
# 権限修正スクリプトを実行
./scripts/fix_permissions.sh
```

このスクリプトは以下の処理を行います：
- データベースディレクトリの作成と権限設定
- サードパーティバイナリの実行権限設定
- Fastfetchとllama-box-rpc-serverの権限設定

## 5. GPUStackの起動

```bash
# GPUStackを起動
source ./scripts/start_gpustack.sh
```

このスクリプトは以下の処理を行います：
- 仮想環境の有効化
- GPUStackサーバーの起動
- Ctrl+Cでのクリーンな終了処理

GPUStackのUI（Playground）には、ブラウザから以下のURLでアクセスできます：
http://localhost:80

## 6. Streamlitアプリケーションの起動

```bash
# Streamlitアプリケーションを起動
source ./scripts/start_streamlit.sh
```

このスクリプトは以下の処理を行います：
- 仮想環境の有効化
- Streamlitアプリケーションの起動
- Ctrl+Cでのクリーンな終了処理

Streamlitアプリケーションには、ブラウザから以下のURLでアクセスできます：
http://localhost:8501

## 7. GPUStackとStreamlitの一括起動

```bash
# GPUStackとStreamlitを一括で起動
source ./scripts/run_all.sh
```

このスクリプトは以下の処理を行います：
- 仮想環境の有効化
- GPUStackサーバーの起動
- GPUStackの起動完了を待機
- モデルのデプロイ状態を確認
- Streamlitアプリケーションの起動
- Ctrl+Cで両方のサービスをクリーンに終了

## 6. APIキーの作成

GPUStack Playground UIにアクセスして、APIキーを作成します：

1. Playground UIにアクセス（http://localhost:80）
2. 設定アイコンをクリック
3. 「API Keys」タブを選択
4. 「Create API Key」ボタンをクリック
5. 生成されたAPIキーをコピーして安全な場所に保存（これは一度しか表示されないので注意）

## 7. モデルのダウンロードとデプロイ

GPUStackでLLMモデルをダウンロードしてデプロイします。以下の例では、軽量なLlamaモデルをダウンロードします：

```bash
# モデルのダウンロードとデプロイスクリプトを実行
python scripts/model_setup.py
```

または、Playground UIから直接モデルをデプロイすることもできます：

1. Playground UIにアクセス
2. 「Models」タブを選択
3. 「Deploy Model」ボタンをクリック
4. モデルタイプとして「LLM」を選択
5. モデルリストから目的のモデルを選択（例：Qwen2.5-0.5B-GGUF）
6. 「Deploy」ボタンをクリック

## 8. アプリケーションの依存関係のインストール

```bash
# アプリケーションディレクトリに移動
cd app

# 依存関係をインストール
pip install -r requirements.txt
```

## 9. Dockerを使用したセットアップ

Dockerを使用すると、依存関係のインストールやGPUStackの設定を自動化できます。

### Dockerイメージのビルドと実行

```bash
# プロジェクトディレクトリに移動
cd /Users/yourdirectory/gpustack-local-llm

# Docker Composeを使用してビルドと起動を行う
docker-compose up -d
```

このコマンドは以下の処理を行います：
- Dockerイメージのビルド
- コンテナの起動
- ポートのマッピング（80→80、8501→8501）
- 永続ボリュームの作成（モデルデータ用）

### Dockerサービスへのアクセス

Dockerコンテナが起動すると、以下のURLでサービスにアクセスできます：
- GPUStack Playground UI: http://localhost:80
- Streamlitチャットアプリ: http://localhost:8501

### 環境変数の設定

`docker-compose.yml`ファイルで以下の環境変数を設定できます：
- `DEPLOY_MODEL`: 起動時に小さなモデルを自動的にデプロイするかどうか（true/false）
- `MODEL_ID`: デプロイするモデルのID（例：TheBloke/TinyLlama-1.1B-Chat-v1.0-GGUF）

```yaml
environment:
  - DEPLOY_MODEL=true
  - MODEL_ID=TheBloke/TinyLlama-1.1B-Chat-v1.0-GGUF
```

### Dockerコンテナの管理

```bash
# コンテナの状態を確認
docker ps

# コンテナのログを表示
docker logs gpustack-local-llm_gpustack_1

# コンテナを停止
docker-compose down

# コンテナを再起動
docker-compose restart
```

## トラブルシューティング

### 権限関連のエラー

権限エラーが発生した場合は、以下のコマンドを実行してください：

```bash
./scripts/fix_permissions.sh
```

### ポートが使用中のエラー

ポート80、10150、10151が使用中の場合は、以下のコマンドでプロセスを確認して終了させることができます：

```bash
# 使用中のポートを確認
lsof -i :80,10150,10151

# プロセスを終了
kill <PID>
```

### GPU関連のエラー

Apple Silicon Macの場合、MPS（Metal Performance Shaders）がGPUアクセスに使用されます。以下の点を確認してください：

- Python 3.10以上を使用していること
- `torch`が正しくインストールされていること（MPS対応バージョン）

### APIアクセスの問題

APIキーが正しく設定されていない場合、以下を確認してください：

- APIキーが環境変数として正しく設定されていること
- GPUStackサーバーが実行中であること
- ファイアウォールがポート80をブロックしていないこと

### メモリ不足のエラー

大きなモデルを実行しようとしてメモリ不足になる場合は、以下の対策を試してください：

- より小さなモデルを使用する（例：Llama2-7b → Qwen2.5-0.5B）
- モデルの量子化バージョンを使用する（GGUFフォーマットなど）
- GPUメモリ使用量を制限する設定を調整する

## 次のステップ

セットアップが完了したら、[使用方法ガイド](usage_guide.md)を参照して、チャットボットアプリケーションの実行方法を確認してください。

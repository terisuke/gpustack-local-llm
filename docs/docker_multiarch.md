# マルチアーキテクチャDockerビルドガイド

このガイドでは、GPUStack Local LLMプロジェクトのDockerイメージを複数のアーキテクチャ（ARM64とAMD64）向けにビルドする方法を説明します。

## 前提条件

- Docker Desktop 最新版がインストールされていること
- Docker Buildxが有効になっていること（Docker Desktop 最新版では標準で有効）
- インターネット接続が利用可能であること

## マルチアーキテクチャビルドの実行

プロジェクトには、マルチアーキテクチャビルドを簡単に行うためのスクリプトが含まれています：

```bash
# プロジェクトディレクトリに移動
cd /Users/yourdirectory/gpustack-local-llm

# ビルドスクリプトを実行
./scripts/build_multiarch.sh
```

このスクリプトは以下の処理を行います：

1. Docker Buildx環境のセットアップ
2. QEMUエミュレーションのブートストラップ
3. ARM64（Apple Silicon）とAMD64（x86_64）向けのイメージビルド
4. ビルドしたイメージのプッシュ（Dockerレジストリへのログインが必要）

## 手動でのマルチアーキテクチャビルド

スクリプトを使用せずに手動でビルドする場合は、以下のコマンドを実行します：

```bash
# Buildxビルダーの作成
docker buildx create --name mybuilder --use

# ビルダーのブートストラップ
docker buildx inspect --bootstrap

# マルチアーキテクチャイメージのビルド
docker buildx build \
  --platform linux/amd64,linux/arm64 \
  --tag gpustack-local-llm:latest \
  --file Dockerfile \
  --push \
  .
```

## イメージの検証

ビルドしたイメージがマルチアーキテクチャに対応していることを確認するには：

```bash
# イメージのアーキテクチャ情報を表示
docker buildx imagetools inspect gpustack-local-llm:latest
```

## 注意事項

- `--push`フラグを使用する場合は、事前にDockerレジストリにログインしておく必要があります
- ローカルでのテスト用に`--load`フラグを使用する場合は、一度に1つのプラットフォームしかビルドできません
- ARM64アーキテクチャのビルドはx86_64マシンでは時間がかかる場合があります（QEMUエミュレーションを使用するため）

# GPUStack チャットボット 使用方法ガイド

このガイドでは、GPUStackを使用したローカルLLMチャットボットの使用方法について説明します。

## 1. GPUStackの起動

既にセットアップが完了している場合は、以下のコマンドでGPUStackを起動します：

```bash
# プロジェクトディレクトリに移動
cd /Users/yourdirectory/gpustack-local-llm

# GPUStackを起動
source ./scripts/start_gpustack.sh
```

このスクリプトは以下の処理を行います：
- 仮想環境の有効化
- GPUStackサーバーの起動
- Ctrl+Cでのクリーンな終了処理

GPUStackが起動すると、バックグラウンドでサービスが実行され、Playground UIにアクセスできるようになります。

## 2. Playground UIの使用

ブラウザでPlayground UIにアクセスします：
http://localhost:8080

### モデルのテスト

UIを使用してモデルの動作をテストできます：

1. UIの左側のメニューから「Playground」を選択
2. モデルドロップダウンから、使用するLLMモデルを選択
3. プロンプトを入力して、モデルの応答をテスト
4. 必要に応じてパラメータ（温度、最大トークン数など）を調整

### モデルのパラメータ調整

モデル応答の品質を向上させるために、以下のパラメータを調整できます：

- **Temperature**: 値が高いほど、モデルの応答はより創造的になります（範囲: 0.0〜1.0）
- **Max Tokens**: 生成するトークンの最大数を制限します
- **Top P**: 生成時に考慮するトークンの確率質量を制限します
- **Frequency Penalty**: 繰り返しを減らすためのペナルティを設定します
- **Presence Penalty**: 新しいトピックを導入する可能性を高めます

## 3. チャットボットアプリケーションの実行

プロジェクトに含まれるStreamlitベースのチャットアプリケーションを実行します：

```bash
# プロジェクトディレクトリに移動
cd /Users/yourdirectory/gpustack-local-llm

# 仮想環境を有効化（まだ有効化していない場合）
source venv/bin/activate

# Streamlitアプリケーションを起動
cd app
streamlit run app.py
```

ブラウザで自動的にStreamlitアプリケーションが開きます（デフォルト: http://localhost:8501）。

## 4. リソース使用量の監視

GPUStackのリソース使用状況を監視できます：

1. Playground UIにアクセス（http://localhost:8080）
2. 「Monitoring」タブを選択
3. GPUメモリ使用量、CPUメモリ使用量、リクエスト数などのメトリクスを確認

また、コマンドラインからもリソース情報を取得できます：

```bash
# GPUStackのリソース情報を表示
gpustack status
```

## 5. プロンプトエンジニアリングのヒント

チャットボットの応答品質を向上させるためのプロンプトエンジニアリングのヒント：

1. **明確で具体的な指示**: モデルに対して具体的なタスクと役割を与えます
2. **コンテキストの提供**: 必要な背景情報を提供して、モデルが適切な応答をできるようにします
3. **一貫した指示**: セッション全体で一貫したスタイルと指示を使用します
4. **段階的な指示**: 複雑なタスクは複数のステップに分けます
5. **例示**: 期待する回答のフォーマットや内容の例を示します

## 6. APIの使用方法

チャットボットをカスタマイズしたり、他のアプリケーションと統合したりする場合は、OpenAI互換APIを使用できます：

```python
import openai

# APIキーとエンドポイントを設定
openai.api_key = "YOUR_GPUSTACK_API_KEY"
openai.api_base = "http://localhost:8080/v1"

# モデルを使用して応答を生成
response = openai.ChatCompletion.create(
    model="YOUR_DEPLOYED_MODEL_NAME",
    messages=[
        {"role": "system", "content": "あなたは役立つアシスタントです。"},
        {"role": "user", "content": "こんにちは、今日の天気について教えてください。"}
    ],
    temperature=0.7,
    max_tokens=500
)

# 応答を表示
print(response.choices[0].message.content)
```

APIリクエストのパラメータは、Playground UIで調整したものと同じパラメータを使用できます。

## 7. モデルの更新とバージョン管理

新しいモデルをデプロイしたり、既存のモデルを更新したりする場合：

1. Playground UIの「Models」タブでモデルを選択
2. 「Update」または「Delete」を選択
3. 新しいモデルをデプロイする場合は「Deploy Model」をクリック

## 8. よくある問題と解決策

### 権限関連のエラー

権限エラーが発生した場合は、以下のコマンドを実行してください：

```bash
./scripts/fix_permissions.sh
```

### ポートが使用中のエラー

ポート8080、10150、10151が使用中の場合は、以下のコマンドでプロセスを確認して終了させることができます：

```bash
# 使用中のポートを確認
lsof -i :8080,10150,10151

# プロセスを終了
kill <PID>
```

### モデルのロードが遅い

- より小さなモデルを使用する
- 量子化されたモデルを使用する（GGUFフォーマット）
- GPUメモリの割り当てを最適化する

### 応答の品質が低い

- システムプロンプトを改善する
- 温度パラメータを調整する
- 別のモデルを試す（Qwen、Mistral、Llamaなど）

### APIリクエストが失敗する

- APIキーが正しいことを確認
- GPUStackサーバーが実行中であることを確認
- 正しいエンドポイントとパラメータを使用していることを確認

## 次のステップ

- より高度なRAGシステムの構築
- 複数のモデルを連携させたシステムの開発
- Embedding機能を使ったドキュメント検索システムの構築

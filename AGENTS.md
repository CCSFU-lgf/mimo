# MiMo-V2.5-ASR Demo

一个简单的 MiMo-V2.5-ASR 语音识别 API 调用示例。

## 功能

- 支持 WAV 音频文件转文字
- 自动处理音频格式转换（其他格式自动转 WAV）
- 支持长音频自动分片（超过 10MB 自动切分）

## 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 设置 API Key

设置环境变量：

```bash
# Windows
set MIMO_API_KEY=your-api-key-here

# Linux/Mac
export MIMO_API_KEY=your-api-key-here
```

或者在代码中直接设置 `api_key` 变量。

### 3. 运行示例

```bash
python demo.py
```

## API 说明

- **端点**: `https://token-plan-cn.xiaomimimo.com/v1/chat/completions`
- **协议**: OpenAI 兼容格式
- **模型**: `mimo-v2.5-asr`
- **支持格式**: WAV（其他格式会自动转换）

## 注意事项

- 最大请求体: 10MB
- 推荐采样率: 16kHz 单声道 16bit
- 长音频会自动分片处理

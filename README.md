# MiMo-V2.5-ASR Demo / MiMo-V2.5-ASR 示例

A simple example for calling MiMo-V2.5-ASR speech recognition API.

一个简单的 MiMo-V2.5-ASR 语音识别 API 调用示例。

## Features / 功能

- WAV audio to text / WAV 音频转文字
- Auto format conversion (other formats to WAV) / 自动音频格式转换
- Auto chunking for long audio (>10MB) / 长音频自动分片

## Quick Start / 快速开始

### 1. Install Dependencies / 安装依赖

```bash
pip install -r requirements.txt
```

### 2. Set API Key / 设置 API Key

```bash
# Windows
set MIMO_API_KEY=your-api-key-here

# Linux/Mac
export MIMO_API_KEY=your-api-key-here
```

Or set the `api_key` variable directly in code.

或者在代码中直接设置 `api_key` 变量。

### 3. Run / 运行

```bash
python demo.py
```

## API Info / API 说明

- **Endpoint**: `https://token-plan-cn.xiaomimimo.com/v1/chat/completions`
- **Protocol**: OpenAI compatible / OpenAI 兼容格式
- **Model**: `mimo-v2.5-asr`
- **Supported Format**: WAV (auto-converted) / WAV（自动转换）

## Notes / 注意事项

- Max request size: 10MB / 最大请求体: 10MB
- Recommended: 16kHz mono 16bit / 推荐采样率: 16kHz 单声道 16bit
- Long audio auto-chunked / 长音频会自动分片处理

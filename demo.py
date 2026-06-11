"""
MiMo-V2.5-ASR API 简单调用示例
"""
import os
import sys
import base64
import subprocess
import tempfile
import math
from pathlib import Path

from openai import OpenAI


# ============ 配置 ============
API_KEY = os.environ.get("MIMO_API_KEY", "your-api-key-here")
BASE_URL = "https://token-plan-cn.xiaomimimo.com/v1"
MODEL = "mimo-v2.5-asr"

MAX_AUDIO_SIZE_MB = 9
CHUNK_SECONDS = 240


def get_audio_duration(file_path: str) -> float:
    """用 ffmpeg 获取音频时长（秒）"""
    try:
        probe = subprocess.run(
            ["ffmpeg", "-i", file_path],
            capture_output=True, text=True
        )
        import re
        m = re.search(r"Duration:\s*(\d+):(\d+):(\d+(?:\.\d+)?)", probe.stderr)
        if m:
            return int(m[1]) * 3600 + int(m[2]) * 60 + float(m[3])
    except Exception:
        pass
    return 0


def convert_to_wav(input_path: str) -> str:
    """将音频转换为 WAV 格式"""
    if input_path.lower().endswith(".wav"):
        return input_path

    output = tempfile.mktemp(suffix=".wav")
    subprocess.run(
        ["ffmpeg", "-y", "-i", input_path,
         "-vn", "-ar", "16000", "-ac", "1",
         "-sample_fmt", "s16", "-f", "wav", output],
        capture_output=True
    )
    return output


def split_audio(wav_path: str, chunk_dir: str) -> list:
    """将长音频分片"""
    duration = get_audio_duration(wav_path)
    if duration <= 0:
        return [wav_path]

    n_chunks = math.ceil(duration / CHUNK_SECONDS)
    if n_chunks <= 1:
        return [wav_path]

    os.makedirs(chunk_dir, exist_ok=True)
    chunks = []
    for i in range(n_chunks):
        start = i * CHUNK_SECONDS
        chunk_path = os.path.join(chunk_dir, f"chunk_{i:03d}.wav")
        subprocess.run(
            ["ffmpeg", "-y", "-i", wav_path,
             "-ss", str(start), "-t", str(CHUNK_SECONDS),
             "-c", "copy", chunk_path],
            capture_output=True
        )
        chunks.append(chunk_path)
    return chunks


def audio_to_base64(file_path: str) -> str:
    """读取音频文件并转为 base64"""
    with open(file_path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")


def transcribe_single(client: OpenAI, wav_path: str) -> str:
    """转写单个音频文件"""
    b64_data = audio_to_base64(wav_path)

    resp = client.chat.completions.create(
        model=MODEL,
        messages=[{
            "role": "user",
            "content": [{
                "type": "input_audio",
                "input_audio": {
                    "data": f"data:audio/wav;base64,{b64_data}",
                    "format": "wav",
                },
            }],
        }],
        max_tokens=4096,
    )
    return resp.choices[0].message.content


def transcribe(audio_path: str, api_key: str = None) -> str:
    """
    转写音频文件

    Args:
        audio_path: 音频文件路径（支持 wav/mp3/mp4 等格式）
        api_key: API 密钥，不传则使用环境变量 MIMO_API_KEY

    Returns:
        识别出的文本
    """
    key = api_key or API_KEY
    client = OpenAI(base_url=BASE_URL, api_key=key)

    # 1. 转换为 WAV
    wav_path = convert_to_wav(audio_path)
    temp_dir = tempfile.mkdtemp() if wav_path != audio_path else None

    try:
        # 2. 检查文件大小，必要时分片
        file_size_mb = os.path.getsize(wav_path) / (1024 * 1024)

        if file_size_mb <= MAX_AUDIO_SIZE_MB:
            return transcribe_single(client, wav_path)

        # 超过 10MB，分片处理
        chunks = split_audio(wav_path, os.path.join(temp_dir or ".", "chunks"))
        results = []
        for i, chunk in enumerate(chunks):
            print(f"  处理分片 {i + 1}/{len(chunks)}...")
            text = transcribe_single(client, chunk)
            results.append(text)
        return "".join(results)

    finally:
        # 清理临时文件
        if temp_dir and os.path.exists(temp_dir):
            import shutil
            shutil.rmtree(temp_dir, ignore_errors=True)


# ============ 主程序 ============
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: python demo.py <音频文件路径>")
        print("示例: python demo.py test.wav")
        sys.exit(1)

    audio_file = sys.argv[1]
    if not os.path.exists(audio_file):
        print(f"错误: 文件不存在 - {audio_file}")
        sys.exit(1)

    print(f"识别音频: {audio_file}")
    result = transcribe(audio_file)
    print(f"\n识别结果:\n{result}")

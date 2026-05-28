from pathlib import Path

import numpy as np
from scipy.io.wavfile import write

SAMPLE_RATE = 44100


def db_to_amplitude(db: float) -> float:
    #將 dBFS 轉成振幅比例，振幅 = 10 ^ (分貝 / 20)
    return 10 ** (db / 20)


def apply_envelope(signal: np.ndarray, fade_time: float = 0.01) -> np.ndarray:
    #加入淡入淡出，避免開始/結束爆音。
    fade_samples = int(SAMPLE_RATE * fade_time)
    if fade_samples == 0 or fade_samples * 2 > len(signal):#避免音檔太短，淡入淡出後沒聲音
        return signal

    fade_in = np.linspace(0, 1, fade_samples)
    fade_out = np.linspace(1, 0, fade_samples)

    signal[:fade_samples] *= fade_in
    signal[-fade_samples:] *= fade_out
    return signal


def generate_tone(duration: float, db: float, freqs: list[float]) -> np.ndarray:
    #產生指定秒數、音量(dBFS)、多頻率混音訊號。

    t = np.linspace(0, duration, int(SAMPLE_RATE * duration), endpoint=False)
    signal = np.zeros_like(t)

    for freq in freqs:
        signal += np.sin(2 * np.pi * freq * t) #sin(2πft)

    #避免爆音，將訊號正規化到 -1 到 1
    max_value = np.max(np.abs(signal))
    if max_value > 0:
        signal = signal / max_value

    signal *= db_to_amplitude(db)
    signal = apply_envelope(signal)
    return signal


def save_wav(filename: str, signal: np.ndarray) -> None:
    #輸出 16-bit PCM WAV。
    clipped = np.clip(signal, -1.0, 1.0)
    audio = np.int16(clipped * 32767)
    write(filename, SAMPLE_RATE, audio)

#字串轉浮點數
def parse_freqs(freq_text: str) -> list[float]:
    return [float(x.strip()) for x in freq_text.split(",") if x.strip()]

#取檔名
def build_output_filename(duration_text: str, db_text: str, freq_text: str) -> str:
    return f"{duration_text}s_{db_text}db_{freq_text}hz.wav"

#執行音頻模式
def run_tone_mode(duration_text: str, db_text: str, freq_text: str) -> Path:
    duration = float(duration_text)
    db = float(db_text)
    freqs = parse_freqs(freq_text)

    signal = generate_tone(duration, db, freqs)
    output_path = Path(build_output_filename(duration_text, db_text, freq_text))
    save_wav(str(output_path), signal)
    return output_path

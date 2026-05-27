from pathlib import Path

from gtts import gTTS


def text_to_speech(text: str, output_file: str | None = None, lang: str = "zh-TW") -> Path:
    """將文字轉成語音 MP3 檔。"""
    clean_text = text.strip()
    if not clean_text:
        raise ValueError("文字內容不可為空")
    if output_file is None:
        output_file = text + ".mp3"
    output_path = Path(output_file)
    tts = gTTS(text=clean_text, lang=lang)
    tts.save(str(output_path))
    return output_path

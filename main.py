import argparse

from audio_generator import run_tone_mode
from tts_generator import text_to_speech


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="音檔工具：產生音頻或文字轉語音")
    parser.add_argument("--mode", type=str, help="模式：1是音頻模式 或 2是文字轉語音模式")
    parser.add_argument("--duration", type=float, help="秒數，例如 2")
    parser.add_argument("--db", type=float, help="音量 dBFS，例如 -6")
    parser.add_argument("--freqs", type=str, help="頻率列表，以逗號分隔，例如 800,2400")
    parser.add_argument("--text", type=str, help="要轉語音的文字")
    return parser


def run_tts_mode(text: str | None) -> None:
    if text is None:
        while True:
            text = input("請輸入要轉語音的文字: ").strip()
            if text:
                break
            print("文字內容不可為空，請重新輸入。")
    output_path = text_to_speech(text)
    print(f"已輸出 {output_path}")


def handle_tone_mode(args: argparse.Namespace) -> None:
    while True:
        duration_text = input("請輸入秒數: ").strip() if args.duration is None else str(args.duration)
        db_text = input("請輸入 dBFS，例如 -10(建議 -20 ~ -10): ").strip() if args.db is None else str(args.db)
        freq_text = (
            input("請輸入頻率，可用逗號分隔，例如 800 或 800,2400: ").strip()
            if args.freqs is None
            else args.freqs.strip()
        )

        if not duration_text or not db_text or not freq_text:
            print("所有欄位都必須填寫，請重新輸入。")
            continue

        try:
            duration = float(duration_text)
            db = float(db_text)
            freqs = [float(freq.strip()) for freq in freq_text.split(",")]
        except ValueError:
            print("秒數、dBFS 和頻率都必須是數字，請重新輸入。")
            continue

        if duration <= 0:
            print("秒數必須大於 0，請重新輸入。")
            continue

        if any(freq <= 0 for freq in freqs):
            print("頻率必須大於 0，請重新輸入。")
            continue

        break

    output_path = run_tone_mode(
        duration_text=str(duration),
        db_text=str(db),
        freq_text=",".join(str(freq) for freq in freqs)
    )

    print(f"已輸出 {output_path}")


def main() -> None:
    parser = build_arg_parser()
    args = parser.parse_args()
    while True:
        mode = input("請選擇模式：1=音頻模式, 2=拼音模式(TTS): ").strip() if args.mode is None else str(args.mode)
        if mode in ["1", "2"]:
            break
        print("模式輸入錯誤，請輸入 1 或 2")
    if mode == "1":
        handle_tone_mode(args)
    elif mode == "2":
        run_tts_mode(args.text)


if __name__ == "__main__":
    main()

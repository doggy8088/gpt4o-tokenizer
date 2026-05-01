"""Export a tiktoken vocabulary into per-language text files."""
import argparse
import sys
from pathlib import Path

from langdetect import DetectorFactory, detect
from langdetect.lang_detect_exception import LangDetectException

import tiktoken
import hanzidentifier

SUPPORTED_ENCODINGS = ("cl100k_base", "o200k_base")
SUPPORTED_DETECT_METHODS = ("langdetect", "hanzidentifier")

DetectorFactory.seed = 0


def configure_stdout() -> None:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Export all tokens from a tiktoken vocabulary into language buckets."
    )
    parser.add_argument(
        "--encoding-name",
        choices=SUPPORTED_ENCODINGS,
        default="o200k_base",
        help="Tokenizer encoding to inspect.",
    )
    parser.add_argument(
        "--detect-method",
        choices=SUPPORTED_DETECT_METHODS,
        default="hanzidentifier",
        help="Language detection method used to group decoded tokens.",
    )
    return parser.parse_args()


def detect_with_langdetect(term: str) -> str:
    if not term.strip():
        return "unknown"

    try:
        return detect(term)
    except LangDetectException:
        return "unknown"


def detect_with_hanzidentifier(term: str) -> str:
    lang = "others"

    if hanzidentifier.has_chinese(term):
        lang = "zh"

        if hanzidentifier.is_simplified(term):
            lang = "zh-cn"

        if hanzidentifier.is_traditional(term):
            lang = "zh-tw"

    return lang


def detect_language(term: str, detect_method: str) -> str:
    if detect_method == "langdetect":
        return detect_with_langdetect(term)

    return detect_with_hanzidentifier(term)


def prepare_output_dir(output_dir: Path) -> None:
    output_dir.mkdir(exist_ok=True)

    for output_file in output_dir.glob("*.txt"):
        output_file.unlink()


def export_tokens(encoding_name: str, detect_method: str) -> None:
    tokenizer = tiktoken.get_encoding(encoding_name)
    output_dir = Path(f"{encoding_name}-{detect_method}")

    prepare_output_dir(output_dir)

    for i in range(tokenizer.eot_token - 1):
        term = tokenizer.decode([i])
        lang = detect_language(term, detect_method)

        print(f"{i:06d} {lang} {term}")

        with (output_dir / f"{lang}.txt").open("a", encoding="utf-8") as file:
            file.write(f"{i:06d} {term}\n")


def main() -> None:
    configure_stdout()
    args = parse_args()
    export_tokens(args.encoding_name, args.detect_method)


if __name__ == "__main__":
    main()

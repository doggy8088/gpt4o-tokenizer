"""
This script tokenizes a given text using the 'o200k_base' tokenizer from the 'tiktoken' library.
It iterates over the range of tokens in the tokenizer and decodes each token into a string.
Then, it uses the 'langdetect' library to detect the language of the decoded token.
The detected language and the token itself are printed to the console.
Additionally, the token is appended to a file named based on the detected language.
The output files are stored in the 'output' directory.
"""
import os
import sys
import codecs
import tiktoken
import hanzidentifier

sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())

ENCODING_NAME = "o200k_base"
DETECT_METHOD = "hanzidentifier"

tokenizer = tiktoken.get_encoding(ENCODING_NAME)

if not os.path.exists(f"{ENCODING_NAME}-{DETECT_METHOD}"):
    os.makedirs(f"{ENCODING_NAME}-{DETECT_METHOD}")

for i in range(tokenizer.eot_token - 1):
    term: str = tokenizer.decode([i])
    lang: str = "others"

    if hanzidentifier.has_chinese(term):
        lang = "zh"

        if hanzidentifier.is_simplified(term):
            lang = "zh-cn"

        if hanzidentifier.is_traditional(term):
            lang = "zh-tw"

    print(f"{i:06d} {lang} {term}")

    with open(f"{ENCODING_NAME}-{DETECT_METHOD}/{lang}.txt", "a", encoding="utf-8") as file:
        file.write(f"{i:06d} {term}\n")

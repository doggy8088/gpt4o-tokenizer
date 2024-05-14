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
import langdetect

sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())

ENCODING_NAME = "o200k_base"

tokenizer = tiktoken.get_encoding(ENCODING_NAME)

if not os.path.exists(ENCODING_NAME):
    os.makedirs(ENCODING_NAME)

for i in range(tokenizer.eot_token - 1):
    term: str = tokenizer.decode([i])
    lang: str = "unknown"

    try:
        lang = langdetect.detect(term)
    except langdetect.lang_detect_exception.LangDetectException:
        pass

    print(f"{i:06d} {lang} {term}")

    with open(f"{ENCODING_NAME}/{lang}.txt", "a", encoding="utf-8") as file:
        file.write(f"{i:06d} {term}\n")

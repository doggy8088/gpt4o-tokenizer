# gpt4o-tokenizer

這個專案會把 `tiktoken` 裡某一套 tokenizer 的所有 token 逐一解碼，再依照不同的語言判斷方式，把結果輸出成多個文字檔，方便觀察 OpenAI tokenizer 對各種語言、尤其是中文的切分情況。

嚴格來說，這裡常講的「四種 tokenizer」其實不是四個完全不同的分詞器，而是 **2 種 tokenizer 編碼器 × 2 種語言判斷方式** 的四種分析組合：

1. `cl100k_base + langdetect`
2. `cl100k_base + hanzidentifier`
3. `o200k_base + langdetect`
4. `o200k_base + hanzidentifier`

## 先用白話理解這個專案

你可以把 tokenizer 想成「AI 在讀文字前，先拿來切小塊的刀法」。

- 切得越合理，模型通常越容易理解文字，也可能更省 token。
- 不同模型世代，使用的 tokenizer 也可能不同。
- 同一句中文、英文、日文或混合文字，換一套 tokenizer，切出來的塊數和方式都可能不一樣。

這個專案做的事，就是把 tokenizer 的「字典內容」翻出來看，然後再嘗試幫每個 token 貼上一個語言標籤，方便你觀察：

- 哪些 token 比較像繁中
- 哪些比較像簡中
- 哪些是英文、日文、韓文或其他語言
- 哪些其實只是符號、半個字、空白或難以判斷的片段

## 四種組合到底差在哪裡？

### 第一個維度：Tokenizer 編碼器

| 編碼器 | 白話理解 | 特性 |
| --- | --- | --- |
| `cl100k_base` | 較早一代、很多 OpenAI 模型常見的切法 | 很適合拿來當對照組，看舊一代 tokenizer 怎麼切文字 |
| `o200k_base` | 較新一代、偏向 GPT-4o 時代的切法 | 通常更能反映新模型對多語言內容的切分方式 |

最簡單的理解方式是：

- `cl100k_base` 像是「上一代字典」
- `o200k_base` 像是「較新的字典」

同樣一句話，`o200k_base` 有時會比 `cl100k_base` 切得更有效率，尤其在多語混合或現代用語上更值得觀察。

### 第二個維度：語言判斷方式

| 判斷方式 | 白話理解 | 優點 | 限制 |
| --- | --- | --- | --- |
| `langdetect` | 像「猜這一小段文字比較像哪個語言」 | 支援多語言，能把 token 分到英文、法文、日文等多種語言 | token 往往很短，可能只是一個符號、半個詞，這時很容易誤判或只能標成 `unknown` |
| `hanzidentifier` | 像「先看這段是不是漢字，再判斷偏簡中或繁中」 | 對中文特別直覺，尤其適合分 `zh-cn` 與 `zh-tw` | 它不是通用多語言偵測器，非中文內容大多只會落到 `others` |

如果你是一般使用者，可以這樣記：

- 想看「很多語言的大方向分布」：用 `langdetect`
- 想看「中文裡的繁中 / 簡中差異」：用 `hanzidentifier`

## 四種組合的實際用途

| 組合 | 最適合回答的問題 | 你會看到什麼 |
| --- | --- | --- |
| `cl100k_base + langdetect` | 舊一代 tokenizer 對各語言大致怎麼分？ | 語言種類多，但短 token 容易有誤判 |
| `cl100k_base + hanzidentifier` | 舊一代 tokenizer 對繁中 / 簡中的切分差異如何？ | 中文分類清楚，但非中文幾乎都進 `others` |
| `o200k_base + langdetect` | 新一代 tokenizer 對多語言切分是否有不同？ | 更接近 GPT-4o 時代的切分觀察方式 |
| `o200k_base + hanzidentifier` | 新一代 tokenizer 對繁中 / 簡中的支援看起來如何？ | 最適合專看中文，尤其是繁體中文與簡體中文 |

## 怎麼選才對？

### 如果你主要想研究中文

優先看這兩種：

1. `cl100k_base + hanzidentifier`
2. `o200k_base + hanzidentifier`

這樣你可以直接比較「舊字典」和「新字典」對中文 token 的分布差異。

### 如果你主要想研究多語言

優先看這兩種：

1. `cl100k_base + langdetect`
2. `o200k_base + langdetect`

這樣你會比較容易看到英文、日文、韓文、歐洲語言等的粗略分布。

### 如果你只想快速看 GPT-4o 比較接近哪種表現

直接先跑：

```sh
uv run python main.py --encoding-name o200k_base --detect-method hanzidentifier
```

如果你的重點是繁中 / 簡中，這通常會是最有感的一組。

## 使用 uv 管理專案

本專案已改成使用 `uv` 管理相依套件與虛擬環境。

### 1. 安裝 uv

如果你的系統還沒有 `uv`，可先參考官方文件安裝：<https://docs.astral.sh/uv/>

### 2. 安裝相依套件

```sh
git clone https://github.com/doggy8088/gpt4o-tokenizer.git
cd gpt4o-tokenizer
uv sync
```

`uv sync` 會根據 `pyproject.toml` 與 `uv.lock` 建立專案環境，不需要再手動 `pip install -r requirements.txt`。

## 執行方式

### 產生四種組合的其中一種

```sh
uv run python main.py --encoding-name o200k_base --detect-method hanzidentifier
```

### 四種常用指令

```sh
uv run python main.py --encoding-name cl100k_base --detect-method langdetect
uv run python main.py --encoding-name cl100k_base --detect-method hanzidentifier
uv run python main.py --encoding-name o200k_base --detect-method langdetect
uv run python main.py --encoding-name o200k_base --detect-method hanzidentifier
```

## 輸出結果在哪裡？

程式會輸出到對應名稱的資料夾：

- `cl100k_base-langdetect/`
- `cl100k_base-hanzidentifier/`
- `o200k_base-langdetect/`
- `o200k_base-hanzidentifier/`

每個資料夾裡會再依語言或分類建立檔案，例如：

- `zh-tw.txt`
- `zh-cn.txt`
- `en.txt`
- `ja.txt`
- `unknown.txt`
- `others.txt`

## 需要注意的地方

1. `langdetect` 面對很短的 token 時，本來就容易猜錯，這不是你操作錯誤，而是因為它看到的可能只是一個符號、單一字母，甚至是半個詞。
2. `hanzidentifier` 比較像中文專用分類器，所以它很適合比較繁中與簡中，但不適合拿來分析所有語言。
3. 每次執行時，程式會重新產生目標資料夾底下的 `.txt` 檔，避免重跑後資料重複追加。

## 這個專案最值得看的重點

如果你想快速得到一個直覺：

- 想比較「新舊 tokenizer」差異：比 `cl100k_base` 和 `o200k_base`
- 想比較「繁中 / 簡中」差異：用 `hanzidentifier`
- 想比較「多語言的大方向」：用 `langdetect`

所以這個專案最核心的價值，不只是列出 token，而是讓你能用更容易理解的方式，看見 **不同 tokenizer 怎麼切語言、怎麼切中文，以及新舊字典的差異**。

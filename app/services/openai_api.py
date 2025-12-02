"""
Summarize text using OpenAI.
"""

from openai import OpenAI

from app.configs.openai_config import OPENAI_API_KEY

client = OpenAI(api_key=OPENAI_API_KEY)

SUMMARIZE_PROMPT = """
以下のログから日記を作成してください。
堅すぎない口調で、ログ以外の情報を勝手に補填しないでください。
出力は本文のみで余分なものを含めないでください。

ログは以下です。

Text:
{text}
"""


def summarize(text: str) -> str:
    """Summarize text using OpenAI."""
    res = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": SUMMARIZE_PROMPT.format(text=text)}],
    )
    return res.choices[0].message.content

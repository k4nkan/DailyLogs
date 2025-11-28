"""
Summarize text using OpenAI.
"""

from openai import OpenAI

from app.configs.openai_config import OPENAI_API_KEY

client = OpenAI(api_key=OPENAI_API_KEY)

SUMMARIZE_PROMPT = """
以下のログから日記を作成してください。
堅すぎない口調で、長すぎないように要約してください。
本文のみを出力してください。

日記の入力者の情報は以下です。
- 大学生
- インターンとして、IT教育のメンターをしている
- フロントエンド、バックエンド、インフラなど幅広く興味を持っている

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

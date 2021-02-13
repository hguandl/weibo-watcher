"""
Copyright (c) 2021 Hao Guan

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
"""

import requests


def tgbot_notify(weibo: dict, bot: str, chats: list) -> None:
    """
    Send contents in <weibo> via Telegram <bot> to <chats>.
    """
    texts = "\n\n".join(weibo['content'])
    texts += f"\n\nhttps://m.weibo.cn/status/{weibo['id']}"

    for chat in chats:
        data = {
            "chat_id": chat,
            "text": texts
        }
        requests.post(f"https://api.telegram.org/bot{bot}/sendMessage",
                        data=data)

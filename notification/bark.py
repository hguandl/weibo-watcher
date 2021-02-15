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


def bark_notify(weibo: dict, api_tokens: list) -> None:
    """
    Notify <weibo> via Bark with tokens in <api_tokens>
    """

    for token in api_tokens:
        requests.get(
            f"https://api.day.app/{token}"
            f"/{weibo['name']}"
            f"/{weibo['content'][0][:128]}"
            f"?url=https://m.weibo.cn/status/{weibo['id']}"
        )


def custom_bark(weibo: dict, api_url: str) -> None:
    """
    Notify <weibo> via custom Bark server at <api_url>
    Customization example: https://github.com/hguandl/bark-server
    """

    requests.post(
        api_url,
        data={
            "title": {weibo['name']},
            "body": {weibo['content'][0][:128]},
            "url": f"https://m.weibo.cn/status/{weibo['id']}"
        }
    )

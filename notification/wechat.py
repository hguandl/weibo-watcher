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

import json

import requests


def work_wechat_notify(weibo: dict, corpid: str, agentid: int, corpsecret: str,
                       touser: str="@all"):
    """
    Send text card about <weibo> to work wechat <corpid> with <corpsecret>.
    """
    access_token = json.loads(
        requests.get("https://qyapi.weixin.qq.com/cgi-bin/gettoken"
                    f"?corpid={corpid}"
                    f"&corpsecret={corpsecret}").text
    )["access_token"]

    if len(weibo['content']) > 1:
        title = weibo['content'][0][:128]
        desciption = weibo['content'][1][:512]
    else:
        title = weibo['content'][0][:128]
        desciption = weibo['content'][0][:512]

    post_data = {
        "touser": touser,
        "msgtype": "textcard",
        "agentid": agentid,
        "textcard": {
            "title": title,
            "description": desciption,
            "url": f"https://m.weibo.cn/status/{weibo['id']}",
            "btntxt": "全文"
        }
    }
    requests.post("https://qyapi.weixin.qq.com/cgi-bin/message/send"
                 f"?access_token={access_token}", json=post_data)

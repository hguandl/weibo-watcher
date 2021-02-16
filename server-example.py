#!/usr/bin/env python3

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

from notification.bark import bark_notify, custom_bark
from notification.ifttt import ifttt_webhook
from notification.tgbot import tgbot_notify
from notification.wechat import work_wechat_notify
from watcher.akanno import ArknightsAnnounceWatcher
from watcher.weibo import WeiboWatcher


def callbacks(weibo):
    """
    Callback function triggered by new weibo.
    Stuffs such as push notifications, save to file can be put here.
    """
    if weibo is None:
        return

    bark_notify(weibo, ["token1", "token2"])

    custom_bark(weibo, "Custom Bark server")

    ifttt_webhook(weibo, [("key1", "event1"), ("key2", "event2")])

    tgbot_notify(weibo, "bot_api", ["chatid1", "chatid2"])

    work_wechat_notify(weibo, "corpid", "appid", "corpsecret")


def callbacks2(text):
    if text is None:
        return

    requests.post(
        "http://localhost:8585/feed",
        data={
            "text": text
        }
    )


if __name__ == "__main__":
    WeiboWatcher("6279793937").watch(callbacks)  # @明日方舟Arknights
    # ArknightsAnnounceWatcher().watch(callbacks2)

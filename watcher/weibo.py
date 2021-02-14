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
import random
import time
from datetime import datetime

import pytz
import requests
from dateutil import parser
from lxml import etree

UA_STRING = (
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6)'
    ' AppleWebKit/605.1.15 (KHTML, like Gecko)'
    ' Version/14.0.3 Safari/605.1.15'
)


class WeiboWatcher(object):
    """
    A watcher for new weibo published by user with <UID>.
    """
    def __init__(self, uid: int) -> None:
        super().__init__()
        self.uid = uid
        self.headers = WeiboWatcher._xhr_headers(uid)
        self.name = None
        self.weibo_cid = None
        self.latest_date = datetime.now(pytz.UTC)
        self.latest_id = None
        self.setup()

    @staticmethod
    def _api_url(value: str, containerid: str) -> str:
        ret = (
            "https://m.weibo.cn/api/container/getIndex?"
            "type=uid"
            f"&value={value}"
        )
        if containerid is not None:
            ret = f"{ret}&containerid={containerid}"
        return ret


    @staticmethod
    def _xhr_headers(uid: str) -> dict:
        return {
            'Accept': 'application/json, text/plain, */*',
            'Referer': f'https://m.weibo.cn/u/{uid}',
            'User-Agent': UA_STRING,
            'X-Requested-With': 'XMLHttpRequest',
            'MWeibo-Pwa': '1'
        }


    def setup(self) -> None:
        """
        Retrieve basic data for a user.
        """
        data = json.loads(
            requests.get(
                WeiboWatcher._api_url(self.uid, None),
                headers=self.headers
            ).text
        )
        self.name = data["data"]["userInfo"]["screen_name"]
        tabs = data["data"]["tabsInfo"]["tabs"]
        for tab in tabs:
            if tab["tab_type"] == "weibo":
                self.weibo_cid = tab["containerid"]
                break
        self.update()


    def update(self) -> bool:
        """
        Check for updates.
        Return True if a new weibo is published.
        """
        ret = False
        try:
            data = json.loads(
                requests.get(
                    WeiboWatcher._api_url(self.uid, self.weibo_cid),
                    headers = self.headers
                ).text
            )

            for card in data['data']['cards']:
                if card['card_type'] == 9:
                    datet = parser.parse(card['mblog']['created_at'])
                    if datet > self.latest_date:
                        ret = True
                        self.latest_date = datet
                        self.latest_id = card['mblog']['id']
        except requests.RequestException as req_err:
            print(req_err)
        except json.JSONDecodeError as json_err:
            print(json_err)
        return ret


    def watch(self, callback) -> None:
        """
        Run as a daemon to watch the user.
        """
        while True:
            wait_sec = random.randint(6, 12)
            if self.update():
                print(f"\nNew from {self.name}: {self.latest_date}")
                callback(self.parse_content(self.latest_id))
            else:
                print(f"[{datetime.now()}]: Waiting...", end='\r')
            time.sleep(wait_sec)


    def parse_content(self, mbid) -> dict:
        """
        Format the content to texts.
        """
        try:
            selector = etree.HTML(
                json.loads(
                    requests.get(
                        f"https://m.weibo.cn/statuses/extend?id={mbid}"
                    ).text
                )['data']['longTextContent']
                .replace("<br />", "\n")
            ).xpath("//text()")

            formated_content = []

            for element in selector:
                element = element.strip()
                if len(element) == 0:
                    continue
                if element == "#明日方舟#":
                    continue
                paras = element.split("\n\n")
                for para in paras:
                    formated_content.append(para)

            return {
                'id': mbid,
                'name': self.name,
                'content': formated_content
            }

        except requests.RequestException as req_err:
            print(req_err)
        except json.JSONDecodeError as json_err:
            print(json_err)

        return None

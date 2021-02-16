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

import requests

UA_STRING = (
    'arknights/385'
    ' CFNetwork/1220.1'
    ' Darwin/20.3.0'
)


class ArknightsAnnounceWatcher(object):
    """
    A watcher for new annmouncement in Arknights.
    """
    def __init__(self, debug: bool=False) -> None:
        super().__init__()
        self.headers = self._xhr_headers()
        self.latest_id = None
        self.latest_announce = None
        if not debug:
            self.setup()


    @staticmethod
    def _api_url() -> str:
        return (
            "https://ak-fs.hypergryph.com/announce/IOS/announcement.meta.json"
            "?sign="
        )


    @staticmethod
    def _xhr_headers() -> dict:
        return {
            'Connection': 'keep-alive',
            'Accept': '*/*',
            'User-Agent': UA_STRING,
            'Accept-Language': 'zh-cn',
            'Accept-Encoding': "gzip, deflate",
            'X-Unity-Version': '2017.4.39f1'
        }


    def setup(self) -> None:
        """
        Retrieve basic data for client.
        """
        data = json.loads(
            requests.get(
                self._api_url(),
                headers=self.headers
            ).text
        )
        self.latest_id = data["focusAnnounceId"]


    def update(self) -> bool:
        """
        Check for updates.
        Return True if the focused announcement changes.
        """
        ret = False
        try:
            data = json.loads(
                requests.get(
                    self._api_url(),
                    headers = self.headers
                ).text
            )

            if data["focusAnnounceId"] != self.latest_id:
                ret = True
                self.latest_id = data["focusAnnounceId"]
                for announce in data["announceList"]:
                    if announce["announceId"] == data["focusAnnounceId"]:
                        self.latest_announce = announce
                        break

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
                trimmed_title = self.latest_announce['title'].replace("\n", " ")
                print(f"\nNew announcement: {trimmed_title}")
                callback(self.parse_content(self.latest_announce))
            else:
                print(f"[{datetime.now()}]: Waiting...", end='\r')
            time.sleep(wait_sec)


    @staticmethod
    def parse_content(announce) -> str:
        """
        Format the content to texts.
        """
        return (
            f"{announce['title']}"
            "\n\n"
            f"{announce['webUrl']}"
        )

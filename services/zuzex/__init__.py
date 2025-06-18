from datetime import datetime
import base64
import json
import requests

from config import ZUZEX_BASE_URL
from utils.log_answer import sync_sys_log


class JiraZuzex:
    def __init__(self, headers, task_key=None):
        self.base_url = ZUZEX_BASE_URL
        self.task_key = task_key

        self.headers = headers
        self.check_credentials()

        self.worker = None

    @staticmethod
    def get_basic_auth_header(username: str, password: str):
        token = f"{username}:{password}"
        b64_token = base64.b64encode(token.encode("utf-8")).decode("utf-8")

        return {
            "Authorization": f"Basic {b64_token}",
            "Content-Type": "application/json",
        }

    def check_credentials(self):
        res = requests.get(f"{self.base_url}/api/2/myself", headers=self.headers)

        if res.status_code != 200:
            raise Exception("403")

        self.worker = res.json()["key"]

        sync_sys_log("Zuzex >> INFO: Success login")

    def get_current_timelog(self):
        today = datetime.today().strftime("%Y-%m-%d")
        payload = json.dumps({"from": today})

        res = requests.post(
            f"{self.base_url}/tempo-timesheets/4/worklogs/search",
            headers=self.headers,
            data=payload,
        )
        if res.status_code != 200:
            raise Exception(f"{res.status_code}")

        return res.json()

    def get_task_id_by_key(self, task_key):

        payload = json.dumps(
            {
                "jql": f"key = {task_key}",
                "fields": [],
                "startAt": 0,
                "maxResults": 200,
                "validateQuery": False,
            }
        )
        res = requests.post(
            f"{self.base_url}/api/2/search/", headers=self.headers, data=payload
        )

        if res.status_code != 200:
            raise Exception("403")

        if res.json()["total"] != 1:
            raise Exception("404")

        return res.json()["issues"][0]["id"]

    def log_full_day(self):
        has_log = len(self.get_current_timelog()) > 0
        today = datetime.today().strftime("%Y-%m-%d")

        if not has_log:
            payload = json.dumps(
                {
                    "worker": self.worker,
                    "comment": "Работа над проектом.",
                    "started": f"{today}T08:00:00.000",
                    "endDate": today,
                    "timeSpentSeconds": 3600 * 8,
                    "billableSeconds": None,
                    "originTaskId": self.get_task_id_by_key(self.task_key),
                    "remainingEstimate": 0,
                    "includeNonWorkingDays": False,
                    "attributes": {},
                }
            )

            res = requests.post(
                f"{self.base_url}/tempo-timesheets/4/worklogs",
                headers=self.headers,
                data=payload,
            )
            print(res.json())
            if res.status_code != 200:
                raise Exception(res.status_code)

        else:
            raise Exception(400)

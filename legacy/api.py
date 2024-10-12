import requests
import json
import os


def getJobObjects():
    pageNo = 1

    params = {
        "app_id": os.environ.get("APP_ID"),
        "app_key": os.environ.get("APP_KEY"),
        "results_per_page": 50,  # Capped at 50 results
        "content-type": "application/json",
    }

    resObj = {
        "count": 82516,  # Last known results count, will update based on updated data
        "results": [],
    }
    reqNo, reqReq = 1, resObj["count"] // 50

    # Check if the request was successful
    while reqReq > 0:
        try:
            url = f"https://api.adzuna.com/v1/api/jobs/sg/search/{pageNo}"
            print(f"Attemping request {reqNo}/{reqReq} to {url}")
            response = requests.get(url, params=params)
            response.raise_for_status()
            print(
                "[SUCCESS] Got ${} results from page ${}".format(
                    len(response.json()["results"]), pageNo
                )
            )
            resObj["results"].extend(response.json()["results"])
            reqNo += 1
            pageNo += 1
        except requests.exceptions.HTTPError as err:
            print(f"[ERROR] Request failed at round {reqNo}")
            print(err.args[0])
        except requests.exceptions.RequestException as err:
            print("[ERROR] Request failed")
            print(err.args[0])

    return resObj

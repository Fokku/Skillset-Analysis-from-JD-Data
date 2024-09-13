url = "https://jobdataapi.com/api/jobs/"

def get_jobs():
    jobDataObj = {'reqNo': 0, 'next': "https://jobdataapi.com/api/jobs/", 'results': []}
    # headers = {"Authorization": "Api-Key test"}
    reqNo = 0

    while jobDataObj["next"] != None or reqNo != 1:
        try:
            print(f"Attemping request {reqNo} to {jobDataObj['next']}")
            response = requests.get(jobDataObj['next'])
            response.raise_for_status()
            jobDataObj['reqNo'] = reqNo
            jobDataObj['next'] = response.json()['next']
            jobDataObj['results'].extend(response.json()['results'])
            reqNo += 1
            print("Request successful")
            print(f"Body: {response.json()}")
        except requests.exceptions.HTTPError as err:
            print(f"Request failed at round {reqNo}")
            print(err.args[0])
            break
        except requests.exceptions.RequestException as err:
            print("Request failed")
            print(err.args[0])
            break
    return jobDataObj
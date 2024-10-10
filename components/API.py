import os
import requests

# YOUTUBE KEY 
API_KEY = 'AIzaSyBR4Na2YRSiIabFPuorkBnZOUclzlUI_ss'

# LIGHTCAST TOKEN - POST METHOD TO https://auth.emsicloud.com/connect/token
LIGHTCAST_TOKEN= 'eyJhbGciOiJSUzI1NiIsImtpZCI6IjNDNjZCRjIzMjBGNkY4RDQ2QzJERDhCMjI0MEVGMTFENTZEQkY3MUYiLCJ0eXAiOiJKV1QiLCJ4NXQiOiJQR2FfSXlEMi1OUnNMZGl5SkE3eEhWYmI5eDgifQ.eyJuYmYiOjE3Mjg1NTA0NTMsImV4cCI6MTcyODU1NDA1MywiaXNzIjoiaHR0cHM6Ly9hdXRoLmVtc2ljbG91ZC5jb20iLCJhdWQiOlsiZW1zaV9vcGVuIiwiaHR0cHM6Ly9hdXRoLmVtc2ljbG91ZC5jb20vcmVzb3VyY2VzIl0sImNsaWVudF9pZCI6IjNiZWZscTZ3b3U2MjI4ZHkiLCJuYW1lIjoiTElOIFlVSEFPIiwiY29tcGFueSI6IlNJVCIsImVtYWlsIjoibHloMDQxNTMyQGdtYWlsLmNvbSIsImlhdCI6MTcyODU1MDQ1Mywic2NvcGUiOlsiZW1zaV9vcGVuIl19.FFyCcmWmeIUPCMPbaMaqPBKQlpYIvTh4Lwqu3DNiUuNttzD0Dnyu_DhmlZfXop_RG-aBpyUbQIGm5RaQ17OVITNmAxF_LAltY5FI-bCT3-kEOiGbviHRx4n2aHyo1DN-YUau6vZ21CucTjk86bEZrxAfvvsTenljW8I0BZuZwJ0vsAn-qtuqxNpI9s7WELrZ1ce_dhe2CL4AS4GIqbR128m5pGARZahemrNBTxhA4rXRNZlicOLrp3WIKBXCeK_avLuno2_iln4xwG6KDSVP3uzTi9sLATnFOUU7GyB-TRUYMo7v3zNLtg8UnDBBU5cdn5VHBiZt7b3tdDSGG8Ztlg'

# Define a function to retrieve YouTube videos related to a skill
def get_youtube_videos(skill_name):
    search_url = "https://www.googleapis.com/youtube/v3/search"
    params = {
        'part': 'snippet',
        'q': skill_name + ' course',  # Search for the skill with the keyword 'course'
        'type': 'video',
        'maxResults': 5,
        'key': API_KEY
    }

    response = requests.get(search_url, params=params)

    if response.status_code == 200:
        videos = response.json()['items']
        return videos
    else:
        return []

headers = {
    "Authorization": f"Bearer {LIGHTCAST_TOKEN}"
}


# Function to make the API call to get skill details by name
def get_skill_description(skill_name):
    url_list = "https://emsiservices.com/skills/versions/latest/skills"
    querystring = {
        "q": skill_name,
        "typeIds": "ST1,ST2",
        "fields": "id,name,type,infoUrl",
        "limit": "1"
    }

    response = requests.get(url_list, headers=headers, params=querystring)

    if response.status_code == 200:
        skills_data = response.json()  # Convert to JSON
        if skills_data and "data" in skills_data and len(skills_data["data"]) > 0:
            first_skill_id = skills_data["data"][0]["id"]

            # Second request to get the skill details using the ID
            url_details = f"https://emsiservices.com/skills/versions/latest/skills/{first_skill_id}"
            response_details = requests.get(url_details, headers=headers)

            if response_details.status_code == 200:
                skill_details = response_details.json()
                if "data" in skill_details and "description" in skill_details["data"]:
                    return skill_details["data"]["description"]
                else:
                    return "Description not found."
            else:
                return f"Error fetching skill details. Status code: {response_details.status_code}"
        else:
            return "No skills found for this search."
    else:
        return f"Error fetching skill data. Status code: {response.status_code}"




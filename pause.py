import requests
api_key = '' # Insert your API key

campaigns = [] # Insert comma separated list of campaign IDs

def pause_campaign(campaign_id):
    url = f"https://server.smartlead.ai/api/v1/campaigns/{campaign_id}/status?api_key={api_key}"
    payload = {"status": "PAUSED"}
    headers = {
        "accept": "application/json",
        "content-type": "application/json"
    }

    response = requests.post(url, json=payload, headers=headers)

    print(response.text)


def lambda_handler(event, context):
   for id in campaigns:
    pause_campaign(id) 

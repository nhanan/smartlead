import requests
api_key = ''

email_account_ids = []

def increase_message_per_day():
    for email_account_id in email_account_ids:
        url = f"https://server.smartlead.ai/api/v1/email-accounts/{email_account_id}?api_key={api_key}"
        headers = {"accept": "application/json"}
        response = requests.get(url, headers=headers).json()
        message_per_day = response['message_per_day'] + 4 # Increase number of emails sent per day by 4, up until 20/day
      
        if message_per_day < 20:
            payload = {"max_email_per_day": message_per_day,}
            headers = {"accept": "application/json", "content-type": "application/json"}
            response = requests.post(url, json=payload, headers=headers)
            print(response.text)


def lambda_handler(event, context):
    increase_message_per_day()

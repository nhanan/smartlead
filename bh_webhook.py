import logging, requests
from auth import start
from urllib.parse import urlparse


# Set up the initial values
swimlane = ""
corp_id = ""
rest_url = f"https://rest{swimlane}.bullhornstaffing.com/rest-services/{corp_id}"

BhRestToken = start()
headers = {"BhRestToken": BhRestToken}

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def lambda_handler(event, context):
    if event['event_type'] == 'EMAIL_SENT':
        email_sent(event)

    if event['event_type'] == 'EMAIL_REPLY':
        email_reply(event)


def email_sent(event):
    email = event['sent_message']['html']
    from_email = event.get('from_email')
    to_email = event.get('to_email')
    secret_key = event.get('secret_key')

    user_id = find_user(f"{from_email.split('@')[0]}@XXXXXXXXXX.com")
    dm_id = find_lead_bh_id(to_email)
    if user_id and dm_id:
        log = add_note_to_Bullhorn("EMAIL_SENT", user_id, dm_id, email)
    else:
        log = ("Missing User ID and/or DM ID")

    logger.info(f"Lambda response: {log}")
    return log

def email_reply(event):
    email = event['reply_message']['html']
    from_email = event.get('from_email')
    to_email = event.get('to_email')
    secret_key = event.get('secret_key')

    user_id = find_user(f"{from_email.split('@')[0]}@XXXXXXXXXX.com")
    dm_id = find_lead_bh_id(to_email)
    if user_id and dm_id:
        log = add_note_to_Bullhorn("EMAIL_REPLY", user_id, dm_id, email)
    else:
        log = ("Missing User ID and/or DM ID")

    logger.info(f"Lambda response: {log}")
    return log

def find_user(email):
    url = f"{rest_url}/query/CorporateUser?where=email='{email}'&fields=id,name&count=10"
    results = requests.request("GET", url, headers=headers).json()
    user_id = results['data'][0]['id']
    return user_id


def add_note_to_Bullhorn(webhook_type, user_id, dm_id, body):
    url = f"{rest_url}/entity/Note"
    
    if webhook_type == "EMAIL_SENT":
        payload = {
            "action": "",
            "comments": body,
            "commentingPerson": {"id": user_id},
            "personReference": {"id": dm_id}
        }
        log = {"user_id": user_id, "dm_id": dm_id, "email": body}

    if webhook_type == "EMAIL_REPLY":
        payload = {
            "action": "",
            "comments": body,
            "commentingPerson": {"id": user_id},
            "personReference": {"id": dm_id}
        }

        log = {"user_id": user_id, "dm_id": dm_id, "email": body}

    
    response = requests.put(url, headers=headers, json=payload).json()
    print(response)

    return log

def find_lead_bh_id(to_email):
    API_KEY = ""
    headers = {'Content-Type': 'application/json'}
    url = f"https://server.smartlead.ai/api/v1/leads/?api_key={API_KEY}&email={to_email}"
    response = requests.get(url, headers=headers).json()
    dm_id = response['custom_fields']['BHID']
    return dm_id

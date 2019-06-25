import logging
import azure.functions as func
from  azure.cosmos import cosmos_client
import json
import os


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# code for keyboard
BLACK      ="#000000"
WHITE      ="#FFFFFF"
RED        ="#FF0000"
GREEN      ="#00FF00"
BLUE       ="#0000FF"
PURPLE     ="#7D3C98"
YELLOW     ="#F7DC6F"
GRAY       ="#A6ACAF"
ORANGE     ="#F39C12"
DARK_GREEN ="#145A32"
LIGHT_GREEN="#82E0AA"
DARK_BLUE  ="#21618C"
LIGHT_BLUE ="#85C1E9"
MAUVE      ="#B784A7"

COLOR  ='SET_COLOR'
BLINK  ='BLINK'
BREATHE='BREATHE'
CYCLE  ='COLOR_CYCLE'

# known users
known_users = {
    "000000000":["bot",     "B",    DARK_GREEN, COLOR],
    "U33EMSR32":["Scott",   "S",    WHITE,      BREATHE],
    "U04DPNWDL":["Justin",  "J",    RED,        BREATHE],
    "U0JSKTXPV":["KC",      "K",    GREEN,      BREATHE],
    "UE1G5T4R0":["Ashley",  "A",    YELLOW,     BREATHE],
    "U04FRHGSH":["Allen",   "A",    PURPLE,     BREATHE],
    "UD2SM4AGN":["Andrew",  "A",    LIGHT_BLUE, BREATHE],
    "U2G0MS7DZ":["Alex",    "A",    BLUE,       BREATHE],
    "U04EBL0BU":["Taylor",  "T",    ORANGE,     BREATHE],
    "U04ECM3GM":["Mark",    "M",    GREEN,      CYCLE],
    "U9BEJRYP7":["Praveen", "P",    RED,        CYCLE],
    "U04J8AU4X":["Joe",     "J",    YELLOW,     CYCLE],
    "U6CN932JF":["Otter",   "O",    MAUVE,      BREATHE],
    "U04DPPAUL":["Chase",   "C",    ORANGE,     CYCLE],
    "U8CN30XC1":["Daniel",  "D",    YELLOW,     CYCLE]
}



def parse_slack_message(req):
    message = {"error" : "not processed"}
    logger.info('Python HTTP trigger function processed a request.')
    logger.info('request is ' + str(req))
    body = req.get_json()


    logger.info("request for body is " + str(body))
    if body['type'] == 'url_verification':
        logger.info("doing verification")
        message = {"challenge": body['challenge']}
    elif body['type'] in ["message", "event_callback"]:
        message = {"event": body['event']}
    return message


def extract_message(event):
    print("have message")
    print(event)
    # if 'text' not in event:
    #     logger.warn("missing text")
    #     logger.warn(event)
    #     return None
    
    user_id = event['user']
    text = event['text']
    event_time = event['event_ts']
    return user_id, text, event_time




def encode(user_id, text, timeof):
    if user_id in known_users:
        [user_name, key, color, effect] = known_users[user_id]
        item = dict()
        item['event_time'] = timeof
        item['user_name'] = user_name
        item['key'] = key
        item['color'] = color
        item['effect'] = effect
        item['text'] = text
        item['read'] = False  

        print(item)
        return item
    else:
        return None

def main(req: func.HttpRequest, cosmos: func.Out[func.Document]) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    message = parse_slack_message(req)
    if 'error' in message:
        return func.HttpResponse(message['error'], status_code = 500)
    elif 'challenge' in message:
        return func.HttpResponse(message['challenge'], status_code = 200)
    elif 'event' in message:
        user_id, text, time = extract_message(message['event'])
    das_msg = encode(user_id, text, time)
    if das_msg is not None:
        cosmos.set(func.Document.from_dict(das_msg))
        return func.HttpResponse(body=json.dumps(das_msg), status_code = 200, headers = {"Context-type":"application/json"})
    else:
        return func.HttpResponse(body='{ "result" : "unhandled" }', status_code = 200, headers = {"Context-type":"application/json"})

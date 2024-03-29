import logging
import azure.functions as func
from  azure.cosmos import cosmos_client
import azure.cosmos.documents as documents
import json

logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger(__name__)\


def main(req: func.HttpRequest, 
        documentsin: func.DocumentList,
        documentsout: func.Out[func.Document]) -> func.HttpResponse:
    
    body = list()
    body_bag = {"messages": body}
    for doc in documentsin:
        d = dict()
        for keep in ['user_name', 'key', 'color', 'effect', 'text']:
            d[keep] = doc[keep]
        body.append(d)
        logger.info(body)

        doc['read'] = 'T'
        documentsout.set(func.Document.from_dict(doc))
        body_bag = { "messages" : body }
    return func.HttpResponse(
        body = json.dumps(body_bag), 
        headers = {"Content-type":"application/json"}, 
        status_code=200)


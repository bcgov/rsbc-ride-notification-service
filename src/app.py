
import fastapi
from fastapi.responses import PlainTextResponse,JSONResponse
import os
from src.emailfunctions import EmailFunctions
from src.alertmanagerfunctions import AlertManagerFuncs
import logging


router = fastapi.APIRouter()

numeric_level = getattr(logging, os.getenv('LOG_LEVEL').upper(), 10)
# Set up logging
logging.basicConfig(
    # level=logging[os.getenv('LOG_LEVEL')],
    level=numeric_level,
    format='%(asctime)s %(levelname)s %(module)s:%(lineno)d [RIDE_EMAIL]: %(message)s'
)

alertmanager_alert_receivers=os.getenv('ALERTMANAGER_DIST_LIST')
alertmanager_email_templateid=os.getenv('ALERTMANAGER_EMAIL_TEMPLATE_ID')

@router.get('/ping')
async def pingmethod():
    return JSONResponse(status_code=200, content={"status":"working"})

@router.post('/sendbasicemail',response_class=JSONResponse)
async def sendbasicemail(payload: dict):
    respstatus = {"status": "failure"}
    status_code = 500
    try:
        payloadinput = payload.copy()
        templateid=payloadinput['templateid']
        receiver=payloadinput['receiver']
        emailobj=EmailFunctions(os.getenv('GC_API_KEY'),os.getenv('GC_BASE_URL'),logging)
        emailresp=emailobj.sendbasicemail(templateid,receiver)
        if emailresp['status_code']==201:
            respstatus = {"status": "success","resp_id":emailresp['resp_id']}
            status_code = 200
        else:
            raise Exception(emailresp['err_resp'] )
    except Exception as e:
        print(e)
        respstatus = {"status": "failure","error":str(e)}

    return JSONResponse(status_code=status_code, content=respstatus)

@router.post('/emailpayloadtest',response_class=JSONResponse)
async def emailpayloadtest(payload: dict):
    logging.debug(payload)
    respstatus = {"status": "success"}
    status_code = 200
    return JSONResponse(status_code=status_code, content=respstatus)

@router.post('/alertmanageralerts',response_class=JSONResponse)
async def alertmanageralert(payload: dict):
    respstatus = {"status": "failure"}
    status_code = 500
    try:
        payloadinput = payload.copy()
        templateid = alertmanager_email_templateid
        alertmanagerobj=AlertManagerFuncs(payload,alertmanager_alert_receivers,logging)
        alert_details=alertmanagerobj.parsePayload()
        logging.debug(alert_details)
        emailobj = EmailFunctions(os.getenv('GC_API_KEY'), os.getenv('GC_BASE_URL'), logging)
        emailresp = emailobj.sendalertmanageralert(templateid,alert_details['receiver'],alert_details['subject'],alert_details['message'])
        if emailresp['status_code']==201:
            respstatus = {"status": "success"}
            status_code = 200
        else:
            raise Exception(emailresp['err_resp'])
    except Exception as e:
        logging.error(e)
        respstatus = {"status": "failure","error":str(e)}
    return JSONResponse(status_code=status_code, content=respstatus)


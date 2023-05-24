

import requests
import json

class EmailFunctions:

    def __init__(self,api_key,base_url,logger):
        self.api_key=api_key
        self.base_url=base_url
        self.logger=logger

    def sendbasicemail(self,templateid,receiveremail):
        funcresp={}
        url = f'{self.base_url}/v2/notifications/email'
        data = { "email_address": receiveremail, "template_id": templateid }
        headers = {'Content-Type': 'application/json', 'Authorization': f'ApiKey-v1 {self.api_key}'}
        response = requests.post(url, json=data, headers=headers)
        if response.status_code==201:
            respjson=json.loads(response.text)
            funcresp['resp_id']=respjson['id']
            funcresp['status_code']=response.status_code
        else:
            respjson = json.loads(response.text)
            funcresp['resp_id'] = ''
            funcresp['status_code'] = response.status_code
            funcresp['err_resp'] = response.text
        return funcresp

    def sendalertmanageralert(self,templateid,receiveremails,alert_subject,alert_msg):
        funcresp = {'status_code':201}
        url = f'{self.base_url}/v2/notifications/email'
        for v in receiveremails:
            try:
                data = {"email_address": v, "template_id": templateid,"personalisation":{"alert_subject":alert_subject,"alert_msg":alert_msg}}
                headers = {'Content-Type': 'application/json', 'Authorization': f'ApiKey-v1 {self.api_key}'}
                response = requests.post(url, json=data, headers=headers)
                if response.status_code == 201:
                    respjson = json.loads(response.text)
                else:
                    respjson = json.loads(response.text)
                    funcresp['status_code'] = response.status_code
                    funcresp['err_resp'] = response.text
                    raise Exception('error in sending email')
            except Exception as e:
                self.logger.error(f'error in sending email to: {v}')
                self.logger.error(e)
                if funcresp['status_code']==201:
                    funcresp['status_code']=500
                    funcresp['err_resp']=str(e)
        return funcresp

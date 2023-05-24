



class AlertManagerFuncs:

    def __init__(self,payload,receivers,logger):
        self.payload=payload
        self.receivers=receivers
        self.logger=logger


    def parsePayload(self):
        receiver_list=self.receivers.split(',')
        # self.logger.debug(receiver_list)
        # self.logger.debug(self.payload['status'])
        receiver_emails=receiver_list
        alert_msg=self.payload['message']
        alert_subject=self.payload['title']
        # self.logger.debug(alert_msg)
        # self.logger.debug(alert_subject)
        return {"receiver":receiver_emails,"subject":alert_subject,"message":alert_msg}























        {'receiver': '', 'status': 'firing', 'alerts': [
            {'status': 'firing', 'labels': {'alertname': 'TestAlert', 'instance': 'Grafana'},
             'annotations': {'summary': 'Notification test'}, 'startsAt': '2023-05-09T19:33:02.044440931Z',
             'endsAt': '0001-01-01T00:00:00Z', 'generatorURL': '', 'fingerprint': '57c6d9296de2ad39',
             'silenceURL': 'http://localhost:3000/alerting/silence/new?alertmanager=grafana&matcher=alertname%3DTestAlert&matcher=instance%3DGrafana',
             'dashboardURL': '', 'panelURL': '', 'values': None,
             'valueString': "[ metric='foo' labels={instance=bar} value=10 ]"}], 'groupLabels': {},
         'commonLabels': {'alertname': 'TestAlert', 'instance': 'Grafana'},
         'commonAnnotations': {'summary': 'Notification test'}, 'externalURL': 'http://localhost:3000/', 'version': '1',
         'groupKey': '{alertname="TestAlert", instance="Grafana"}2023-05-09 19:33:02.044440931 +0000 UTC m=+452152.901748324',
         'truncatedAlerts': 0, 'orgId': 1, 'title': '[FIRING:1]  (TestAlert Grafana)', 'state': 'alerting',
         'message': '**Firing**\n\nValue: [no value]\nLabels:\n - alertname = TestAlert\n - instance = Grafana\nAnnotations:\n - summary = Notification test\nSilence: http://localhost:3000/alerting/silence/new?alertmanager=grafana&matcher=alertname%3DTestAlert&matcher=instance%3DGrafana\n'}
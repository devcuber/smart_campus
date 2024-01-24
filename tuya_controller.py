from tuya_iot import TuyaOpenAPI  
from datetime import datetime

class TuyaController:
    openapi = None
    def __init__(self,client_id, secret_key, username, password, endpoint):
        self.openapi = TuyaOpenAPI(endpoint,client_id,secret_key)
        self.openapi.connect(username,password,"52","tuyasmart")

    def get_logs (self, device_id):
        endpoint = f'/v1.0/iot-03/devices/{device_id}/status'
        request = self.openapi.get(endpoint)
        result = request.get('result', [] )
        result = [ { 
            "device_id" : device_id , 
            "code" : r.get('code'),
            "value" : r.get('value'),
            "datetime" : datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        } for r in result ]
        return result
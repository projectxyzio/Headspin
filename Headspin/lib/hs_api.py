from __future__ import absolute_import
from __future__ import print_function
import requests
import traceback
from time import sleep





class hsApi:
    # API for getting all devices and its details present in  an org
    device_list_url = "https://api-dev.headspin.io/v0/devices"
    get_auto_config = "https://api-dev.headspin.io/v0/devices/automation-config"
    url_root = "https://api-dev.headspin.io/v0/"
    # API for getting all devices and its details present in  an org

    def __init__(self, UDID, access_token):
        self.UDID = UDID
        self.access_token = access_token
        self.headers = {'Authorization': 'Bearer {}'.format(self.access_token)}
        # Get the deivce details
        r = requests.get(self.device_list_url, headers=self.headers)
        self.device_list_resp = self.parse_response(r)
        r = r.json()
        
        self.devices = r['devices']
        is_desired_device = False
        for device in self.devices:
            self.device_os = device['device_type']
            if self.device_os == "android" and device['serial'] == self.UDID:
                is_desired_device = True
            if self.device_os == "ios" and device['device_id'] == self.UDID:
                is_desired_device = True
            if is_desired_device:
                self.device_details = device
                self.device_hostname = device['hostname']
                self.device_address = "{}@{}".format(
                    self.UDID, self.device_hostname)
                self.device_os = device['device_type']
                break

    def get_session_video_metadata(self,session_id):
        request_url = f"https://api-dev.headspin.io/v0/sessions/{session_id}/video/metadata"
        response = requests.get(
                request_url, headers= self.headers)
        return response.json()

    #API call to get set labels in the performance session.
    def add_label(self, session_id, name, category, start_time, end_time, label_type='user', data=None):
        '''
        add annotations to session_id with name, category, start_time, end_time
        '''
        request_url = self.url_root + 'sessions/' + session_id + '/label/add'
        data_payload = {}
        data_payload['name'] = name
        data_payload['category'] = category
        data_payload['start_time'] = start_time/1000
        data_payload['end_time'] = end_time/1000
        data_payload['label_type'] = label_type
        data_payload['data'] = data
        data_payload['pinned'] = False
        response = requests.post(request_url, headers=self.headers, json=data_payload)
        response.raise_for_status()
        return self.parse_response(response)

    #API call  to upload the session details to the UI
    def add_session_data(self, session_data):
        request_url = self.url_root + "perftests/upload"
        response = requests.post(
            request_url, headers=self.headers, json=session_data, timeout=240)
        # print("session_data:",session_data)    
        return self.parse_response(response)

    #API call for  updates the description part of the performance session which is located in the top left.
    def update_session_name_and_description(self, session_id, name, description):
        request_url = self.url_root + 'sessions/' + session_id + '/description'
        data_payload = {}
        data_payload['name'] = name
        data_payload['description'] = description
        # print(request_url)
        response = requests.post(
            request_url, headers=self.headers, json=data_payload, timeout=240)
        return self.parse_response(response)

    #API  call to get the start timestamp of the session created. 
    def get_capture_timestamp(self, session_id):
        request_url = self.url_root + 'sessions/' + session_id+'/timestamps'
        response = requests.get(request_url, headers=self.headers)
        response.raise_for_status()
        return self.parse_response(response)

    #API call to get the pageload label created after pageload analysis.
    def get_pageloadtime(self, session_id, name, start_time, end_time, start_sensitivity=None, end_sensitivity=None):
        request_url = self.url_root + 'sessions/analysis/pageloadtime/'+session_id
        data_payload = {}
        region_times = []
        start_end = {}
        start_end['start_time'] = str((start_time)/1000)
        start_end['end_time'] = str((end_time)/1000)
        start_end['name'] = name
        region_times.append(start_end)
        data_payload['regions'] = region_times
        if(start_sensitivity is not None):
            data_payload['start_sensitivity'] = start_sensitivity
        if(end_sensitivity is not None):
            data_payload['end_sensitivity'] = end_sensitivity

        response = requests.post(
            request_url, headers=self.headers, json=data_payload)
        response.raise_for_status()
        results = self.parse_response(response)
        return results

    #API call to check weather Dashboard has been  allocated or not 
    def check_dashboard_allocated(self):
        req_url ='https://@api-dev.headspin.io/v0/grafana/dashboard/info'
        response = requests.get(url = req_url, headers=self.headers)
        results = self.parse_response(response)
        for dashboard in results['dashboards']:
            if "SpeedTest SandBox" == dashboard['name']:
                return dashboard['allocated']
    
    

    # Get the user flow id of the the given user flow.
    def get_userflow_id(self, user_flow_name):
        req_url ='https://@api-dev.headspin.io/v0/userflows' 
        
        response = requests.get(url = req_url, headers=self.headers)
        results = self.parse_response(response)
        for userflow in results['user_flows']:
            if user_flow_name == userflow['name']:
                return userflow["user_flow_id"]
        return False

    def update_userflow_status(self, session_id, status):
        req_url ='https://@api-dev.headspin.io/v0/perftests/upload'
        data_payload={}
        data_payload['session_id'] = session_id
        data_payload['status'] = status
        requests.post(url = req_url, headers=self.headers, json=data_payload)

    
    #API call to check autosync ON
    def check_auto_sync_on(self, user_flow_name):
        user_flow_id = self.get_userflow_id(user_flow_name)
        if user_flow_id:
            req_url ='https://@api-dev.headspin.io/v0/userflows/{}/settings'.format(user_flow_id)
            response = requests.get(url = req_url, headers=self.headers)
            userflow_settings = response.json()
            # return 1 if autosync is on Else None
            return userflow_settings['autosync'], user_flow_id

    #API call to turn ON autosync
    def turn_on_auto_sync(self,user_flow_id):
        print("\nTurning On Auto Sync ")
        req_url ='https://@api-dev.headspin.io/v0/userflows/{}/settings'.format(user_flow_id)
        data_payload = {"autosync": 1}
        response = requests.post(url = req_url, headers=self.headers, json=data_payload)
        results = self.parse_response(response)
        return results

    #API call to allocate dashboard for SB runs 
    def allocate_dashboard(self):
        req_url ='https://@api-dev.headspin.io/v0/grafana/dashboard/allocate'
        data ={"dashboard_name": "SpeedTest SandBox"}
        response = requests.post(url = req_url, headers=self.headers, json=data)
        results = self.parse_response(response)
        return results

    # Install app on Android device
    def install_apk(self, filename):
        data = open(filename, 'rb').read()
        request_url = 'https://api-dev.headspin.io/v0/adb/{}/install'.format(
            self.UDID)
        response = requests.post(request_url, data=data, headers=self.headers)
        print(response.text)

    # Install app on iOS devices
    def install_ipa(self, filename):
        data = open(filename, 'rb').read()
        request_url = 'https://api-dev.headspin.io/v0/idevice/{}/installer/install'.format(
            self.UDID)
        response = requests.post(request_url, data=data, headers=self.headers)
        print(response.text)

    # Lock a device in headspin platform.
    def lock_device(self):
        request_url = "https://api-dev.headspin.io/v0/devices/lock"
        response = requests.post(request_url, json={"device_id":self.UDID}, headers=self.headers)
        # print(response.text)

    # Unlock a device which is locked by the same user.
    def unlock_device(self):
        request_url = "https://api-dev.headspin.io/v0/devices/unlock"
        response  = requests.post(request_url, json={"device_id":self.UDID}, headers=self.headers)
        # print(response.text)

    def allocate_garafana(self):
        request_url = f"https://@api-dev.headspin.io/v0/grafana/allocate"
        response  = requests.post(request_url, headers=self.headers)
        return response.json()    
        

    def parse_response(self, response):
        try:
            if response.ok:
                try:
                    return response.json()
                except:
                    return response.text
            else:
                print(response.status_code)
                print('something went wrong')
                print(response.text)
        except:
            print(traceback.print_exc())
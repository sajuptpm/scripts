import base_manager
import utils
import xmltodict
import json
import os
from jcsclient import requestify 
from jcsclient import config 

class QuotaManager(base_manager.BaseManager):
    
    def __init__(self):
        self.url = config.get_service_url('vpc')
        self.headers = {}
        self.version = '2016-03-01'
        self.verb = 'GET'

    def show_vpc_all_resources_quota(self, account_id=None):
        params = {}
        params['Version']= self.version
        params['Action'] = 'ShowQuota'
        if account_id is not None:
           params['account'] = 'acc-'+account_id
        resp = requestify.make_request(self.url, self.verb,
                self.headers, params)
        if resp is not None:
            try:
                resp_dict = json.loads(resp.content)
            except:
                resp_dict = xmltodict.parse(resp.content)
                resp_json = json.dumps(resp_dict, indent=4, sort_keys=True)
                resp_dict = json.loads(resp_json)
            return resp_dict
        return 'FAIL'

    def update_vpc_resource_quota(self, resource, quota, account_id=None):
        params = {}
        params['Version']  = self.version
        params['Action']   = 'UpdateQuota'
        params['resource'] = resource
        params['quota']    = quota 
        if account_id is not None:
           params['account'] = 'acc-'+account_id
        resp = requestify.make_request(self.url, self.verb,
                self.headers, params)
        if resp is not None:
            try:
                resp_dict = json.loads(resp.content)
            except:
                resp_dict = xmltodict.parse(resp.content)
                resp_json = json.dumps(resp_dict, indent=4, sort_keys=True)
                resp_dict = json.loads(resp_json)
        return utils.get_item(('UpdateQuotaResponse', 'quota-update'),
                resp_dict)    

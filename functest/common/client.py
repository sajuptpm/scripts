from jcsclient import utils
from jcsclient import config
from jcsclient import requestify
from jcsclient.requestify import common_headers
from jcsclient import auth_handler
from jcsclient import exception
import json
import xmltodict
import os
import sys
import requests
def patch_make_request(url, verb, headers, params, path=None, data=None):
    return (url, verb, headers, params, path, data)
requestify.make_request = patch_make_request

def make_request(url, verb, headers, params, path=None, data=None, config_handler=None):
    """
    This method makes the actual request to JCS services. 
    The steps are:
        1. Create an AuthHandler object to add signature to the request.
        2. Add any common headers to request like Content.
        3. Use requests library to send the requests to JCS service.

    Benefit ot AuthHandler class is that we can modify the Signature
    generation mechanism under the hood.

    """
    access_key = config_handler.get_access_key()
    secret_key = config_handler.get_secret_key()
    # Always calculate signature without trailing '/' in url
    if url.endswith('/'):
        url = url[:-1]
    auth_obj = auth_handler.Authorization(url, verb, access_key,
                                          secret_key, headers)
    auth_obj.add_authorization(params)

    # Now restore the trailing '/' in url
    url += '/?'
    request_string = url
    for key, val in params.items():
        request_string += str(key) + '=' + str(val) + '&'
    request_string = request_string[:-1]
    global common_headers
    headers.update(common_headers)
    return requests.request(verb, request_string, data=data,
                            verify=config_handler.check_secure(),
                            headers=headers)

def wrapper(func, config_handler):
    def conv(*args, **kwargs):
        new_args = [func.__name__.replace('_', '-')]
        for (k, v,) in kwargs.items():
            new_args.extend(['--{option}'.format(option=k.replace('_', '-')), v])
        resp = func(tuple(new_args))
        resp = make_request(*resp, config_handler=config_handler)
        if resp is not None:
            try:
                resp_dict = json.loads(resp.content)
                resp_dict["Status"] = resp.status_code
            except:
                resp_dict = xmltodict.parse(resp.content)
                resp_json = json.dumps(resp_dict, indent=4, sort_keys=True)
                resp_dict = json.loads(resp_json)
                resp_dict["Status"] = resp.status_code
            return resp_dict
    return conv

def getattribute(obj, name):
    attr = object.__getattribute__(obj, name)
    if callable(attr):
        attr = wrapper(attr, obj.config_handler)
    return attr

class ClientConfigHandler(config.ConfigHandler):

    def __init__(self, access_key=None, secret_key=None):
        try:
            super(ClientConfigHandler, self).__init__(None)
        except:
            pass
        #self.secure = False
        self.access_key = access_key or os.environ.get('ACCESS_KEY')
        self.secret_key = secret_key or os.environ.get('SECRET_KEY')
        self.process_cli_specific_args(["--insecure"])
        if not self.access_key or not self.secret_key:
            raise exception.UnknownCredentials()

class Client(object):

    def __init__(self, access_key = None, secret_key = None):
        config_handler = ClientConfigHandler(access_key, secret_key)
        vpc_service_name = 'vpc'
        service = utils.load_service(vpc_service_name)
        self.vpc = utils.create_controller(service, vpc_service_name)
        self.vpc.config_handler = config_handler
        self.vpc.__class__.__getattribute__ = getattribute
        compute_service_name = 'compute'
        service = utils.load_service(compute_service_name)
        self.compute = utils.create_controller(service, compute_service_name)
        self.compute.config_handler = config_handler
        self.compute.__class__.__getattribute__ = getattribute



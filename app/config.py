import os
import json

class Config():
    config = None
    #general
    DEFAULT_APP_LOCATION = "/app/app/"

    #buckets
    USE_BUCKETS = False
    BUCKET = os.environ.get('BUCKET'),
    ENDPOINT_URL = os.environ.get('ENDPOINT_URL'),
    ACCESS_KEY = os.environ.get('ACCESS_KEY'),
    SECRET_KEY = os.environ.get('SECRET_KEY'),

    #CORE_VALUES
    DEFAULT_CORE_VALUES = [
        "TAKE THE NEXT STEP",
        "UPGRADE WITH A SINGLE CLICK",
        "RUN ANY APP AT ANY SCALE"
    ]

    #images
    IMAGE_MAPPING = {
        "nutanix_logo": "images/nutanix_logo.png",
        "nutanix_background": "images/nutanix_background.jpg",
        "nutanix_favicon": "images/nutanix_favicon.png"
    }
    
    #language mapping
    SOURCE_LANGUAGE = os.environ.get("SOURCE_LANGUAGE", "english")
    @property
    def DESTINATION_LANGUAGE(self): 
        return self.get("DESTINATION_LANGUAGE", "english")

    @property
    def CUSTOMER(self): 
        return self.get("CUSTOMER", "Customer")

    LANGUAGE_MAPPING = {
        "dutch": "nl",
        "english": "en",
        "german": "de",
        "italian": "it",
        "french": "fr"
    }

    RIGHTS_RESERVED = "Yannick Struyf. All rights reserved."
    DESIGNED_BY = "Designed by"

    def __init__(self):
        pass


    def get_core_values(self):
        core_values = os.environ.get('CORE_VALUES',None)
        if core_values:
            return json.loads(core_values)
        return self.DEFAULT_CORE_VALUES
    
    def get(self,key, default=None):
        print("get %s pre env" % key)
        config = self.__read_config()
        env_val = os.environ.get(key,None)
        print("get %s env_val %s" % (key,env_val))
        if env_val:
            return env_val
        config_val = config.get(key)
        print("get %s config_val %s" % (key,config_val))
        if config_val:
            return config_val 
        return default

    def __read_config(self, file='/app/app/config.json'):
        data = {}
        if os.path.isfile(file):
            with open(file) as f:
                data = json.load(f)
        return data

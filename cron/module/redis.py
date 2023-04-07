
import os
import json
import redis
from module.slack import *

from dotenv import load_dotenv
load_dotenv()

class Redis():

    def __init__(self):
        self.slack = Slack()

        with redis.StrictRedis(host=os.getenv('REDIS_HOST'), port=os.getenv('REDIS_PORT'), db=os.getenv('REDIS_DB')) as conn:
            self.redis = conn

    def get_keys(self, match, count):

        try : 
            match = f"*{match}*"

            key_list = []
            for key in self.redis.scan_iter(match, count):
                key_list.append(str(key.decode('utf-8')))

            return key_list

        except Exception as ex :
            pass

    def set_data(self, key, val, expire):

        try : 
            self.redis.set(key, val, expire)

        except Exception as ex :
            pass

    def get_data(self, key):

        try : 
            data = self.redis.get(key)
            if data is None:
                return {}

            ttl = self.redis.ttl(key)
            data_dict = {
                "val" : str(data.decode('utf-8')),
                "expire" : str(ttl)
            }
            return data_dict
    
        except Exception as ex :
            pass

    def get_json_data(self, key):

        try : 
            data = self.redis.get(key)
            if data is None:
                return {}
            
            val = json.loads(data.decode('utf-8'))
            return val
    
        except Exception as ex :
            pass


    def update_data(self, key, val, expire):

        try : 
            if self.redis.get(key):
                self.redis.delete(key)

            self.redis.set(key, val, expire)

        except Exception as ex :
            pass

    def delete_data(self, key):

        try : 
            if self.get_data(key):
                self.redis.delete(key)
        
        except Exception as ex :
            pass
    
    def hset_data(self, key, field, val):

        try : 
            if key and field and val:
                self.redis.hset(key, field, val)

        except Exception as ex :
           self.slack.post_to_slack(f"error on hset_data : {str(ex)}")

    def hget_data(self, key, field):

        try : 

            data = self.redis.hget(key, field)
            if data is None:
                return None
            
            return bytes.decode(data)
    
        except Exception as ex :
            pass

    def hget_json_data(self, key, field):

        try : 
            data = self.redis.hget(key, field)
            if data is None:
                return {}
            
            val = json.loads(data.decode('utf-8'))
            return val
    
        except Exception as ex :
            pass

    def hdel_data(self, key, field):
        
        try : 
            if self.redis.hget(key, field):
                self.redis.hdel(key, field)

        except Exception as ex :
           self.slack.post_to_slack(f"error on hdel_data : {str(ex)}")
    
    def hupd_date(self, key, field, val):   

        try : 
            #self.hdel_data(key, field)
            if key and field and val:
                self.hset_data(key, field, val)

        except Exception as ex :
           self.slack.post_to_slack(f"error on hupd_date : {str(ex)}")

    def flushall(self):

        try : 
            self.redis.flushdb()

        except Exception as ex :
            pass
    
    def replace_hyphen(self, target):

        if "-" in target:
            return target.replace("-", "_")

        return target


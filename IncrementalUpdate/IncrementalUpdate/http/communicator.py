import json
from util import Util
from config import config

class Communicator:
   
    @staticmethod
    def post_total_same(file):
        try:
            headers = [('Content-type','application/json')]
            uri = '/exists'
            struct = {'vp':file.virtual_path,'sha256':file.sha256}
            data = json.dumps(struct)
            status,res = Util.post(config.service_host,config.service_port,uri,headers,data)
            if res != None:
                res_data = json.loads(res)
                return res_data.exists
            else:
                return False
        except:
            return False

    @staticmethod
    def post_diff(diffs):
        try:
            headers = [('Content-type','application/json')]
            uri = '/diff'
            struct = {'diffs':diffs,'vp':file.virtual_path}
            #Upload multiple threads
        except:
            return False





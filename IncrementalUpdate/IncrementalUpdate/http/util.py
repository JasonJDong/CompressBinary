import httplib
import json
import urllib2
import urllib
import traceback
from config import log

class Util:
    
    @staticmethod
    def get(url,port,uri,timeout=30):
        client = None
        abs_url = ''
        try:
            abs_url = ''
            if port == -1:
                abs_url = 'http://' + url + uri
            else:
                abs_url = 'http://' + url + ':' + str(port) + uri
            request = urllib2.Request(abs_url)
            request.add_header('User-Agent','iceberg-client')
            reslut = urllib2.build_opener().open(request)
            return (None,reslut.read())
        except Exception,e:
            print e.message
            return (e,None)
        finally:
            if client:
                client.close()

    @staticmethod
    def post(url,port,uri,headers_list,data,timeout=30):
        client = None
        try:
            headers = {}
            for type_name,type in headers_list:
                headers[type_name] = type
            if port == -1:
                client = httplib.HTTPConnection(url,timeout=timeout)
            else:
                client = httplib.HTTPConnection(url,port,timeout=timeout)
            client.request('POST',uri,data,headers)
            
            response = client.getresponse()
            if response.status == 200:
                try:
                    data = response.read()
                    return (response.status,data)
                except:
                    return (response.status,None)
            else:
                return (response.status,None)
        except:
            log.error(traceback.print_exc())
            return (500,None)
        finally:
            if client:
                client.close()

    @staticmethod
    def put(url,port,uri,headers,data):
        try:
            abs_url = ''
            if port == -1:
                abs_url = 'http://' + url + uri
            else:
                abs_url = 'http://' + url + ':' + port + uri
            opener = urllib2.build_opener(urllib2.HTTPHandler)
            request = urllib2.Request(abs_url,data = data)
            [request.add_header(type_name,type) for type_name,type in headers]
            request.get_method = lambda: 'PUT'
            result = (True,opener.open(request).read())
            return result
        except Exception,e:
            print "==================PUT METHOD EXCEPTION===================="
            print e.message
            print "==================PUT METHOD EXCEPTION===================="
            return (False,None)

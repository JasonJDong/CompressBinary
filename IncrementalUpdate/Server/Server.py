from tornado import ioloop,web

class ServerDemoHandler(web.RequestHandler):
    
    def post(self):
        try:
            pass
        except:
            raise web.HTTPError(500)

application = web.Application([(r'/',ServerDemoHandler)])

def run_tonado():
    application.listen(3800)
    ioloop.IOLoop.instance().start()

if __name__ == '__main__':
    run_tonado()
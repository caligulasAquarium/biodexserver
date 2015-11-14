import tornado.ioloop
import tornado.web
import sqlite3

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, world")

class EntryHandler(tornado.web.RequestHandler):
    def post(self):
        self.write("hello")
        
class PicturesHandler(tornado.web.RequestHandler):
    def get(self, id, name):
        self.write("Hello " + name + " with id " + id)

def main():
    return tornado.web.Application([
        (r"/", MainHandler),
	(r"/addEntry", EntryHandler),
        (r"/pictures/([0-9]+)/([a-z]+)", PicturesHandler), 
    ])

if __name__ == "__main__":
    db = sqlite3.connect('biodex')
    app = main()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()

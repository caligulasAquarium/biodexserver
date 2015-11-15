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
    def get(self, name, item_id):
        self.write("Hello " + name + " with id " + item_id)
        db = sqlite3.connect('biodex')
        c = db.cursor()
# Add primary key into table      
        try:
            c.execute("SELECT {pt} ({ic}, {nc}), VALUES (item_id, name)".\
                format(pt=picture_table, ic=id_column, nc=name_column))
        except sqlite3.IntegrityError:
            print('ERROR: ID already exists in PRIMARY KEY column {}'.format(id_column))      
        db.commit()
        db.close()
        
def main():
    return tornado.web.Application([
        (r"/", MainHandler),
	(r"/addEntry/", EntryHandler),
        (r"/pictures/(.+)/([0-9]+)", PicturesHandler), 
    ])

if __name__ == "__main__":
    sqlite_file = 'biodex'
    picture_table = 'picture_table'
    id_column = 'id_column'
    name_column = 'name_column'
    db = sqlite3.connect('biodex')
    c = db.cursor()  
# Create table (w/ columns)
    c.execute('''CREATE TABLE IF NOT EXISTS picture_table
                (id_column integer PRIMARY KEY, name text, file_path text, latitude real, longitude real)''') 
    db.commit()
    db.close()
    app = main()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()

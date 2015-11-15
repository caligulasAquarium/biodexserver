import tornado.ioloop
import tornado.web
import sqlite3
from PIL import Image
import StringIO
import math

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, world")

class EntryHandler(tornado.web.RequestHandler):
    def post(self):
        file1 = self.request.files['file1'][0]
        f_name = file1['filename']
        file_body = file1['body']
        img = Image.open(StringIO.StringIO(file_body))
        img.save(f_name)
        #print(self.request.body)
        name = self.get_argument('name', None)
        latitude = self.get_argument('latitude', 0)
        longitude = self.get_argument('longitude', 0)
        description = self.get_argument('description', None)
        db = sqlite3.connect('biodex.db')
        cursor = db.cursor()
        cursor.execute('INSERT INTO picture_table VALUES (?, ?, ?, ?, ?, ?)', (None, name, float(latitude), float(longitude), f_name, description,))
        db.commit()
        db.close()
        
class PicturesHandler(tornado.web.RequestHandler):
    def get(self, name, item_id):
<<<<<<< HEAD
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
=======
        db = sqlite3.connect('biodex.db')
        c = db.cursor()
        c.execute("SELECT file_path FROM picture_table WHERE id = ?", (item_id,))
        f_path = c.fetchone()[0]
        print(f_path)
        ifile = open(f_path, "r")
        self.set_header('Content-Type', 'image/png')
        self.set_header('Content-Disposition', 'attach; filename='+f_path+'')
        self.write(ifile.read())
# Add primary key into table      
        #try:
        #    c.execute("SELECT {pt} ({ic}, {nc}), VALUES (item_id, name)".\
        #        format(pt=picture_table, ic=id_column, nc=name_column))
        #except sqlite3.IntegrityError:
        #    print('ERROR: ID already exists in PRIMARY KEY column {}'.format(id_column))    
        #db.commit()
        db.close()

class PictureRangeHandler(tornado.web.RequestHandler):
    def get(self, latitude, longitude, m_range):
        #self.write("I'm at " + latitude + " " + longitude + " and searching in a " + m_range + " mile radius")
        lat_range = float(m_range) / 68.70749821
        long_range = float(m_range) / (69.1710411 * math.cos(float(latitude)))
        max_lat = float(latitude) + lat_range
        min_lat = float(latitude) - lat_range
        max_long = float(longitude) + long_range
        min_long = float(longitude) - long_range
        true_max_lat = max(max_lat, min_lat)
        true_min_lat = min(max_lat, min_lat)
        true_max_long = max(max_long, min_long)
        true_min_long = min(max_long, min_long)
        #self.write("my lat range is " + str(true_max_lat) + " and my long is " + str(true_max_long))
        db = sqlite3.connect('biodex.db')
        c = db.cursor()
        c.execute("SELECT * FROM picture_table WHERE latitude BETWEEN ? AND ? AND longitude BETWEEN ? AND ?", (true_min_lat, true_max_lat, true_min_long, true_max_long,))
        for row in c:
            self.write(str(row))
        db.close()

class GetImageInfoHandler(tornado.web.RequestHandler):
    def get(self, id):
        db = sqlite3.connect('biodex.db')
        c = db.cursor()
        c.execute("SELECT * FROM picture_table WHERE id = ?", (id,))
        self.write(c.fetchone())
        db.close()
        
class GetImageInfoNameHandler(tornado.web.RequestHandler):
    def get(self, name):
        db = sqlite3.connect('biodex.db')
        c = db.cursor()
        c. execute("SELECT * FROM picture_table WHERE name = ?", (name,))
        self.write(c.fetchone())
        db.close()    

def main():
    return tornado.web.Application([
        (r"/", MainHandler),
	(r"/addEntry", EntryHandler),
        (r"/pictures/(.+)/([0-9]+)", PicturesHandler),
        (r"/picturerange/([-.0-9][^a-z\s]+)/([-.0-9][^a-z\s]+)/([.0-9][^a-z\s]+)", PictureRangeHandler),
        (r"/getimageinfo/([0-9]+)", GetImageInfoHandler),
        (r"/getimageinfoname/([\w]).+", GetImageInfoNameHandler),
>>>>>>> Skate310/master
    ])

if __name__ == "__main__":
    sqlite_file = 'biodex'
    picture_table = 'picture_table'
    id_column = 'id_column'
<<<<<<< HEAD
    name_column = 'name_column'
    db = sqlite3.connect('biodex')
    c = db.cursor()  
# Create table (w/ columns)
    c.execute('''CREATE TABLE IF NOT EXISTS picture_table
                (id_column integer PRIMARY KEY, name text, file_path text, latitude real, longitude real)''') 
=======
    column_type1 = 'INTEGER'
    name_column = 'name_column'
    column_type2 = 'TEXT'
    db = sqlite3.connect('biodex.db')
    c = db.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS picture_table (id INTEGER PRIMARY KEY, name TEXT, latitude REAL, longitude REAL, file_path TEXT, description TEXT)''')
>>>>>>> Skate310/master
    db.commit()
    db.close()
    app = main()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()

from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi

# import CRUD Operations
from database_setup import Restaurant, Base, MenuItem
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


#Create session and connect to DB
engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()



class webserverHandler(BaseHTTPRequestHandler):
    
    def do_GET(self):
        try:
            if self.path.endswith("/restaurants"):
                all_restaurants = session.query(Restaurant).all()
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                              
                output = ""
                output += "<html><body>"
                output += "<a href='/restaurants/new'>Make a New Restaurant Here</a>"
                output += "<br><br>"
                output += "<h1>List of the Restaurants:</h1> <br>"
                for all_res in all_restaurants:
                    output += all_res.name
                    output += "<br>"
                    output += "<a href='#'>Edit</a>"
                    output += "<br>"
                    output += "<a href='#'>Delete</a>"
                    output += "<br><br><br>"
                
                output += "</body></html>"
                self.wfile.write(output)
                print output
                return

            if self.path.endswith("/restaurants/new"):
                all_restaurants = session.query(Restaurant).all()
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                output = ""
                output += "<html><body>"
                output += "<h1>Make a New Restaurant</h1>"
                output += "<form method='POST' enctype= \
                        'multipart/form-data' action='/restaurants'> \
                        <input name= 'message' type='text'> <input type='submit' \
                        value='Submit'> </form>"
                output += "</body></html>"
                self.wfile.write(output)
                print output
                return

                
        except IOError:
            self.send_error(404, "File Not Found %s" % self.path)


    def do_POST(self):
        try:
            self.send_response(301)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            ctype, pdict = cgi.parse_header(self.headers.getheader( \
                'content-type'))
            if ctype == 'multipart/form-data':
               fields = cgi.parse_multipart(self.rfile, pdict)
               messagecontent = fields.get('message')

            new_restaurant = Restaurant(name = messagecontent)
            session.add(new_restaurant)
            session.commit()
            all_restaurants = session.query(Restaurant).all()
            output = ""
            output += "<html><body>"
            output += "<a href='/restaurants/new'>Make a New Restaurant Here</a>"
            output += "<br><br>"
            output += "<h1>List of the Restaurants:</h1> <br>"
            for all_res in all_restaurants:
                output += all_res.name
                output += "<br>"
                output += "<a href='#'>Edit</a>"
                output += "<br>"
                output += "<a href='#'>Delete</a>"
                output += "<br><br><br>"
                output += "</body></html>"
                self.wfile.write(output)
                print output
                
        except:
            pass


            
def main():
    try:
        port = 8080
        server = HTTPServer(('', port), webserverHandler)
        print "Web server running on port %s" % port
        server.serve_forever()
        

    except KeyboardInterrupt:
        print "^C entered, stopping web server..."
        server.socket.close()


if __name__ == '__main__':
    main()

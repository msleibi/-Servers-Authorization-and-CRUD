#!/usr/bin/env python

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker 
from database_setup import Restaurant, Base, MenuItem
 
engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


from flask import Flask
app = Flask(__name__)

@app.route('/')
@app.route('/restaurants/<int:restaurant_id>/')
def restaurantMenu(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id =
                restaurant_id).all()
    items = session.query(MenuItem).filter_by(restaurant_id =
                                              restaurant_id)
    output = ''
    for rest in restaurant:
        output += '<h3>' + str(rest.name) + '</h3>'
        output += '<br><br>'
        for i in items:
            output += i.name
            output += '<br>'
            output += i.price
            output += '<br>'
            output += i.description
            output += '<br>'
            output += '<br>'     

    return output

if __name__ == '__main__':
    app.debug = True
    app.run(host = '0.0.0.0', port = 5000)

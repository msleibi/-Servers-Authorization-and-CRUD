#!/usr/bin/env python

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker 
from database_setup import Restaurant, Base, MenuItem
 
engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


from flask import Flask, render_template, request, redirect, url_for
app = Flask(__name__)

@app.route('/')
@app.route('/restaurants/<int:restaurant_id>/')
def restaurantMenu(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id =
                 restaurant_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id =
                                              restaurant_id)
    return render_template('menu.html', restaurant = restaurant, items = items)

    '''                                       
    output = ''
    for rest in restaurant:
    output += '<h3>' + str(restaurant.name) + '</h3>'
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
     '''

    

# Task 1: Create route for newMenuItem function here
@app.route('/restaurants/<int:restaurant_id>/new/', methods = ['GET','POST'])
def newMenuItem(restaurant_id):
    
    if request.method == 'POST':
        newItem = MenuItem(name = request.form['name'],restaurant_id = restaurant_id)
        session.add(newItem)
        session.commit()
        return redirect(url_for('restaurantMenu', restaurant_id = restaurant_id))

    else:
        return render_template('newmenuitem.html',restaurant_id = restaurant_id)
                    

# Task 2: Create route for editMenuItem function here
@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/edit/',methods = ['GET','POST'])
def editMenuItem(restaurant_id, menu_id):
    editItem = session.query(MenuItem).filter_by(id = menu_id).one()
    if request.method == 'POST':
        editItem.name = request.form['newname']
        session.add(editItem)
        session.commit()
        return redirect(url_for('restaurantMenu', restaurant_id = restaurant_id))

    else:
        return render_template('editmenuitem.html',restaurant_id = restaurant_id,menu_id = menu_id, i = editItem)
    
    
# Task 3: Create a route for deleteMenuItem function here
@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/delete/',methods = ['GET','POST'])
def deleteMenuItem(restaurant_id, menu_id):
    deleteItem = session.query(MenuItem).filter_by(id = menu_id).one()
    if request.method == 'POST':
        session.delete(deleteItem)
        session.commit()
        return redirect(url_for('restaurantMenu', restaurant_id = restaurant_id))

    else:
        return render_template('deletemenuitem.html', i = deleteItem)


if __name__ == '__main__':
    app.debug = True
    app.run(host = '0.0.0.0', port = 5000)

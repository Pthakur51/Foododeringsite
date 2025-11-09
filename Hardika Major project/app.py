from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # For session management

# Ensure the database directory exists
DATABASE = 'database/foodie.db'

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/menu')
def menu():
    conn = get_db_connection()
    items = conn.execute('SELECT * FROM menu').fetchall()
    conn.close()
    return render_template('menu.html', items=items)


@app.route('/add_to_cart/<int:item_id>', methods=['POST'])
def add_to_cart(item_id):
    cart = session.get('cart', {})
    cart[str(item_id)] = cart.get(str(item_id), 0) + 1
    session['cart'] = cart
    return redirect(url_for('cart'))

@app.route('/cart')
def cart():
    cart = session.get('cart', {})
    if not cart:
        return render_template('cart.html', items=[], total=0)

    conn = get_db_connection()
    items = []
    total = 0
    for item_id, quantity in cart.items():
        item = conn.execute('SELECT * FROM menu WHERE id = ?', (item_id,)).fetchone()
        if item:
            item_dict = dict(item)
            item_dict['quantity'] = quantity
            item_dict['subtotal'] = quantity * item['price']
            total += item_dict['subtotal']
            items.append(item_dict)
    conn.close()
    return render_template('cart.html', items=items, total=total)

from flask import request, redirect, url_for

@app.route('/remove_from_cart', methods=['POST'])
def remove_from_cart():
    item_id = str(request.form['item_id'])
    cart = session.get('cart', {})

    if item_id in cart:
        del cart[item_id]
        session['cart'] = cart

    return redirect(url_for('cart'))


import uuid  # to generate a unique order ID

@app.route('/order', methods=['GET', 'POST'])
def order():
    # Get the cart from session
    cart = session.get('cart', {})

    if not cart:
        return redirect(url_for('menu'))  # If the cart is empty, redirect to the menu page

    # Get user details (for now using hardcoded address, you can make it dynamic)
    # For example, these values could be coming from a form submitted by the user
    
    delivery_address = "123 Street Name, City"  # You can replace this with dynamic data from a form
    delivery_method = "Home Delivery"  # Same as above
    payment_method = "Credit Card"  # Or use data from a form

    items_ordered = []
    total_price = 0

    # Loop through cart items to get their details and calculate the total
    conn = get_db_connection()
    for item_id, quantity in cart.items():
        item = conn.execute('SELECT * FROM menu WHERE id = ?', (item_id,)).fetchone()
        if item:
            item_name = item['name']
            item_price = item['price']
            item_total = item_price * quantity
            total_price += item_total
            items_ordered.append(f"{item_name} x{quantity} - ₹{item_total}")

    conn.close()

    # Join items ordered into a string
    items_ordered = ", ".join(items_ordered)

    # Static order ID (you can implement logic to increment this as per your requirements)
    # Here we're simply using a fixed static order ID or you can manage an incremental counter
    static_order_id = 12345  # For example, use a static value, or you could increment it using a counter

    # Pass dynamic values to the template
    return render_template('order.html', 
                           order_id=static_order_id,  # Static order ID
                           items_ordered=items_ordered,
                           delivery_address=delivery_address,
                           delivery_method=delivery_method,
                           payment_method=payment_method,
                           total_price=total_price)






@app.route('/admin')
def admin():
    conn = get_db_connection()
    orders = conn.execute('SELECT * FROM orders ORDER BY order_date DESC').fetchall()
    conn.close()
    return render_template('admin.html', orders=orders)

@app.route('/about')
def about():
    return render_template('about_us.html')

if __name__ == '__main__':
    if not os.path.exists('database'):
        os.makedirs('database')
    app.run(debug=True)

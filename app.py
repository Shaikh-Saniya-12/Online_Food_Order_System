from flask import Flask, render_template, request, redirect, session, send_from_directory, url_for
import mysql.connector
import os
app = Flask(__name__)
app.secret_key = "secret123"
app.config['SESSION_COOKIE_SECURE'] = False

# ---------------- DATABASE CONNECTION ----------------
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Your_Password",
    database="food_order"
)


@app.route('/uploads/<filename>')
def uploads(filename):
    return send_from_directory('uploads', filename)


# ---------------- HOME ----------------
@app.route('/')
def home():
    return render_template('index.html')

# ---------------- REGISTER ----------------
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        print(request.form)
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']

        cursor = db.cursor()
        cursor.execute(
            "INSERT INTO users (name, email, password) VALUES (%s, %s, %s)",
            (name, email, password)
        )
        db.commit()

        return redirect('/login')

    return render_template('register.html')

# ---------------- LOGIN ----------------
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        cursor = db.cursor(dictionary=True)
        cursor.execute(
            "SELECT * FROM users WHERE email=%s AND password=%s",
            (email, password)
        )
        user = cursor.fetchone()
        print(user)

        if user:
            session['user_id'] = user['id']
            return redirect('/menu')
        else:
            return "Invalid credentials"

    return render_template('login.html')

# ---------------- LOGOUT ----------------
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

# ---------------- MENU ----------------
@app.route('/menu')
def menu():
    search=request.args.get('search')
    cursor = db.cursor(dictionary=True)
    if search:
        cursor.execute(
            "SELECT*FROM products WHERE name LIKE %s",
            ('%'+search+'%',)
        )
    else:
        cursor.execute("SELECT * FROM products")
    products = cursor.fetchall()

    return render_template("menu.html", products=products)

# ---------------- ADD TO CART ----------------
@app.route('/add_to_cart/<int:product_id>')
def add_to_cart(product_id):
    if 'user_id' not in session:
        return redirect('/login')

    user_id = session['user_id']
    cursor = db.cursor()

    cursor.execute(
        "INSERT INTO cart (user_id, product_id, quantity) VALUES (%s, %s, %s)",
        (user_id, product_id, 1)
    )

    db.commit()

    return redirect('/cart')   # 👈 goes to cart page

# ---------------- VIEW CART ----------------
@app.route('/cart')
def cart():
    if 'user_id' not in session:
        return redirect('/login')

    user_id = session['user_id']
    cursor = db.cursor(dictionary=True)

    cursor.execute("""
        SELECT products.id, products.name, products.price, cart.quantity
        FROM cart
        JOIN products ON cart.product_id = products.id
        WHERE cart.user_id = %s
    """, (user_id,))

    items = cursor.fetchall()

    total = sum(item['price'] * item['quantity'] for item in items)

    return render_template('cart.html', items=items, total=total)

# ----------------Remove-----------------
@app.route('/remove/<int:product_id>')
def remove(product_id):
    if 'user_id' not in session:
        return redirect('/login')

    cursor = db.cursor()
    cursor.execute(
        "DELETE FROM cart WHERE product_id=%s AND user_id=%s",
        (product_id, session['user_id'])
    )
    db.commit()

    return redirect('/cart')



# ---------------- PLACE ORDER ----------------
@app.route('/place_order')
def place_order():
    if 'user_id' not in session:
        return redirect('/login')

    user_id = session['user_id']
    cursor = db.cursor(dictionary=True)

    # Get cart items
    cursor.execute("""
        SELECT cart.product_id, cart.quantity, products.price
        FROM cart
        JOIN products ON cart.product_id = products.id
        WHERE cart.user_id = %s
    """, (user_id,))
    items = cursor.fetchall()
    print(items)

    if not items:
        return "Cart is empty"

    # Calculate total
    total = sum(i['price'] * i['quantity'] for i in items)

    cursor2 = db.cursor()

    # Insert into orders table
    cursor2.execute(
        "INSERT INTO orders (user_id, total) VALUES (%s, %s)",
        (user_id, total)
    )

    order_id = cursor2.lastrowid

    # Insert each item into order_items
    for i in items:
        cursor2.execute("""
            INSERT INTO order_items (order_id, product_id, quantity, price)
            VALUES (%s, %s, %s, %s)
        """, (order_id, i['product_id'], i['quantity'], i['price']))

    # Clear cart
    cursor2.execute("DELETE FROM cart WHERE user_id=%s", (user_id,))

    db.commit()

    return redirect('/payment')   # 👈 goes to payment


# ---------------- PAYMENT PAGE ----------------
@app.route('/payment')
def payment():
    return render_template('payment.html')


# ---------------- PAYMENT SUCCESS ----------------
@app.route('/payment_success', methods=['POST'])
def payment_success():
    user_id = session.get('user_id')

    if not user_id:
        return redirect('/login')
    
    payment_method = request.form.get('payment_method')

    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="SAnu@1101",
        database="food_order"
    )
    cursor = db.cursor(dictionary=True)

    # Get cart items
    cursor.execute("""
        SELECT cart.product_id, cart.quantity, products.price
        FROM cart
        JOIN products ON cart.product_id = products.id
        WHERE cart.user_id = %s
    """, (user_id,))
    
    items = cursor.fetchall()

    if not items:
        return "Cart is empty!"

    total = sum(i['price'] * i['quantity'] for i in items)

    # Create order
    cursor2 = db.cursor()
    cursor2.execute(
        "INSERT INTO orders (user_id, total, payment_method) VALUES (%s, %s, %s)",
        (user_id, total, payment_method)
    )

    order_id = cursor2.lastrowid

    # Insert order items
    for i in items:
        cursor2.execute("""
            INSERT INTO order_items (order_id, product_id, quantity, price)
            VALUES (%s, %s, %s, %s)
        """, (order_id, i['product_id'], i['quantity'], i['price']))

    # Clear cart
    cursor2.execute("DELETE FROM cart WHERE user_id=%s", (user_id,))

    db.commit()

    return redirect('/orders')

# ---------------- ORDER HISTORY ----------------
@app.route('/orders')
def orders():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    user_id = session['user_id']
    cursor = db.cursor(dictionary=True)

    try:
        query = """
            SELECT
                o.id AS order_id,
                o.total,
                o.payment_method,
                o.created_at,
                oi.quantity,
                oi.price AS item_price,
                p.name AS product_name
            FROM orders o
            LEFT JOIN order_items oi
                ON o.id = oi.order_id
            LEFT JOIN products p
                ON oi.product_id = p.id
            WHERE o.user_id = %s
            ORDER BY o.created_at DESC
        """


        cursor.execute(query, (user_id,))
        rows = cursor.fetchall()

        #Group multiple food items under one order
        orders_list = {}

        for row in rows:
            order_id = int(row['order_id'])

            order = orders_list.setdefault(order_id, {
                'id': order_id,
                'total': row['total'],
                'payment_method': row['payment_method'],
                'created_at': row['created_at'],
                'order_items': []
            })

            if row['product_name'] is not None:
                order['order_items'].append({
                    'name': row['product_name'],
                    'quantity': row['quantity'],
                    'price': row['item_price']
                })
        return render_template(
            'orders.html',
            orders=list(orders_list.values())
        )
    finally:
        cursor.close()

# ---------------- ADMIN ----------------
@app.route('/admin')
def admin():
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM orders")
    orders = cursor.fetchall()

    return render_template('admin_dashboard.html', orders=orders)

# ---------------- RUN ----------------
if __name__ == "__main__":
    app.run(debug=True)
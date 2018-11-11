import sqlite3 as sql
from passlib.hash import sha256_crypt

def create_customer(request):
    con = sql.connect("digin.db")
   
    sqlQuery = "select username from customer where (username ='" + request.form['username'] + "')"
    cur = con.cursor()
    cur.execute(sqlQuery)
    row = cur.fetchone()
    
    if not row:
        cur.execute("INSERT INTO customer (name,address,phone,email,username,password) VALUES (?,?,?,?,?,?)", (request.form['name'],
        request.form['address'],request.form['phone'],request.form['email'],
        request.form['username'],sha256_crypt.encrypt(request.form['password'])))
        con.commit()
        print "added user successfully"
       
    con.close()
    return not row

def authenticate(request):
    con = sql.connect("digin.db")
    t=(request.form['username'],)
    sqlQuery = "select password from customer where username = ?"  
    cursor = con.cursor()
    cursor.execute(sqlQuery,t)
    row = cursor.fetchone()
    con.close()
    if row:
        return sha256_crypt.verify(request.form['password'], row[0])
    else:
        return False
    
def create_restaurant(request):  # create the restaurant called when rest. signs up
    con = sql.connect("digin.db")

    sqlQuery = "select name from restaurant where (name ='" + request.form['name'] + "')"
    cur = con.cursor()
    cur.execute(sqlQuery)
    row = cur.fetchone()

    if not row:
        cur.execute("INSERT INTO restaurant (name,address,contact,description,rating,picture,password) VALUES (?,?,?,?,?,?,?)", (
        request.form['name'], request.form['address'], request.form['contact'], request.form['description'],
        request.form['rating'],request.form['picture'], request.form['password']))
        con.commit()
        print("added restaurant successfully")

    con.close()
    return not row


# def get_order_for_restaurant():  # returns a dictionary of orders which has order id, cost and dictionary of products
#     con = sql.connect("digin.db")
#
#     sqlQuery = "select name from restaurant where (name ='" + request.form['name'] + "')"
#     cur = con.cursor()
#     cur.execute(sqlQuery)
#     row = cur.fetchone()
#
#     if not row:
#         cur.execute(
#             "INSERT INTO restaurant (name,address,contact,description,rating,picture,password) VALUES (?,?,?,?,?,?,?)",
#             (
#                 request.form['name'], request.form['address'], request.form['contact'], request.form['description'],
#                 request.form['rating'], request.form['picture'], request.form['password']))
#         con.commit()
#         print
#         "added restaurant successfully"
#
#     con.close()
#     return not row


def get_restaurant_by_name(restaurant_name): # returant restaurant details as dictionary
    con = sql.connect("digin.db")
    # Uncomment line below if you want output in dictionary format

    
    sqlQuery = "select * from restaurant where (name ='" + restaurant_name + "')"
    cur = con.cursor()
    cur.execute(sqlQuery)
    rows = cur.fetchone()
    con.close()

    return rows

def get_all_restaurant(): # returant restaurant details as dictionary
    con = sql.connect("digin.db")
    # Uncomment line below if you want output in dictionary format
    sqlQuery = "select * from restaurant "
    cur = con.cursor()
    cur.execute(sqlQuery)
    rows = cur.fetchall()
    con.close()
    return rows

def add_product_to_menu(restaurant_id,request):
    con = sql.connect("digin.db")
    t=(request.form['name'],restaurant_id)
    sqlQuery = "select name from product where name = ? and restaurant_id= ?"
    cur = con.cursor()
    cur.execute(sqlQuery,t)
    row = cur.fetchone()

    if not row:
        cur.execute(
            "INSERT INTO product (name,description,price,type,picture,restaurant_id) VALUES (?,?,?,?,?,?,?)",
            (
                request.form['name'], request.form['description'],
                request.form['price'], request.form['type'], request.form['picture'], request.form['restaurant_id']))
        con.commit()
        print("added product to menu successfully")

    con.close()
    return not row

# def delete_product_from_menu(restaurant_id,request):
#     con = sql.connect("digin.db")
#     t=(request.form['name'],restaurant_id)
#     #sqlQuery = "select name from product where name = ? and restaurant_id= ?"
#     sqlQuery = "DELETE FROM customers WHERE name = ? and restaurant_id= ?"
#     cur = con.cursor()
#     cur.execute(sqlQuery,t)
#     row = cur.fetchone()


def get_product_from_menu(product_id):
    con = sql.connect("digin.db")
    con.row_factory = sql.Row
    t=(product_id,)
    sqlQuery = "select * from product where id= ?"
    cur = con.cursor()
    cur.execute(sqlQuery,t)
    row = cur.fetchone()
    return  row

def update_product_in_menu(product_id, request):
    con = sql.connect("digin.db")
    con.row_factory = sql.Row
    sqlQuery = "UPDATE product SET name= ?,description= ?,price=?,type= ?,picture= ?,restaurant_id= ? WHERE id = ?",(request.form['name'], request.form['description'],request.form['price'], request.form['type'], request.form['picture'], request.form['restaurant_id'],product_id)
    cur = con.cursor()
    cur.execute(sqlQuery)
    row = cur.fetchone()
    return  row
def review_customer_orders(customer_id): # R part of CRUD
    conn = sql.connect("digin.db")
#    df_order = pd.read_sql_query(
#        "select * from order where (customer_id = '" + customer_id + "');", conn)
#    df_order_mapping = pd.read_sql_query(
#        "select * from order_product_mapping ;", conn)
#

#    all_orders = pd.merge(df_order, df_order_mapping, left_on=['id'], right_on=['order_id'], how='inner')
    conn.close()
#    return all_orders

# def update_customer_orders(request): # U part of CRUD
#     conn = sql.connect("digin.db")
#     df_order = pd.read_sql_query(
#         "select * from order where (customer_id = '" + request.form['customer_id'] + "');", conn)
#     df_order_mapping = pd.read_sql_query(
#         "select * from order_product_mapping ;", conn)


#     all_orders = pd.merge(df_order, df_order_mapping, left_on=['id'], right_on=['order_id'], how='inner')
#     conn.close()
#     return all_orders

def create_customer_orders(request): # C part of CRUD
    con = sql.connect("digin.db")
    cur = con.cursor()
    cur.execute("INSERT INTO order (restaurant_id,customer_id,status,description,cost,review) VALUES (?,?,?,?,?,?)",
                    (request.form['restaurant_id'], request.form['customer_id'], request.form['status'], request.form['description'], request.form['cost'], request.form['review']))
    con.commit()
    print "added user successfully"

    con.close()

##cart code
def add_to_cart(user_id,request):
    con = sql.connect("digin.db")
    t = (request.form['product_id'], user_id)
    sqlQuery = "select user_id from cart where product_id = ? and user_id= ?"
    cur = con.cursor()
    cur.execute(sqlQuery, t)
    row = cur.fetchone()

    if not row:  #newly added to cart
        cur.execute(
            "INSERT INTO cart (user_id,product_id,quantity) VALUES (?,?,?)",
            (
                user_id, request.form['product_id'],
                request.form['quantity']))
        con.commit()
        print("added product to menu successfully")
    else:#update quantity
        sqlQuery = "UPDATE cart SET quantity= ? WHERE user_id = ?, product_id=?", (
        request.form['quantity'] , user_id, request.form['product_id'])

    con.close()

def view_cart(user_id,request):
    con = sql.connect("digin.db")
    con.row_factory = sql.Row
    t = (user_id,)
    sqlQuery = "select * from cart where user_id= ?"
    cur = con.cursor()
    cur.execute(sqlQuery, t)
    rows = cur.fetchall()
    return rows

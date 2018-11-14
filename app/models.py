import sqlite3 as sql
from passlib.hash import sha256_crypt
import pandas as pd

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

def restaurant_authenticate(request):
    con = sql.connect("digin.db")
    t=(request.form['username'],)
    sqlQuery = "select password from restaurant where username = ?"
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

    sqlQuery = "select username from restaurant where (username ='" + request.form['username'] + "')"
    cur = con.cursor()
    cur.execute(sqlQuery)
    row = cur.fetchone()

    if not row:
        cur.execute("INSERT INTO restaurant (name,address,phone,email,description,username,password,picture) VALUES (?,?,?,?,?,?,?,?)", (
        request.form['name'], request.form['address'], request.form['phone'],request.form['email'], request.form['description'],
        request.form['username'], sha256_crypt.encrypt(request.form['password']),"images/p1.jpg"))
        con.commit()
        print("added restaurant successfully")

    con.close()
    return not row

def get_customer_from_username(username):
    con = sql.connect("digin.db")

    sqlQuery = "select * from customer where (username ='" + username + "')"
    cur = con.cursor()
    cur.execute(sqlQuery)
    row = cur.fetchone()
    return row
    
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

def get_customer_id_by_username(username):
    con = sql.connect("digin.db")
    # Uncomment line below if you want output in dictionary format

    sqlQuery = "select * from customer where (username ='" + username + "')"
    cur = con.cursor()
    cur.execute(sqlQuery)
    rows = cur.fetchone()
    con.close()

    return rows

def get_restaurant_id_by_username(username):
    con = sql.connect("digin.db")
    # Uncomment line below if you want output in dictionary format

    sqlQuery = "select * from restaurant where (username ='" + username + "')"
    cur = con.cursor()
    cur.execute(sqlQuery)
    rows = cur.fetchone()
    con.close()

    return rows

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
            "INSERT INTO product (name,description,price,type,picture,restaurant_id) VALUES (?,?,?,?,?,?)",
            (
                request.form['name'], request.form['description'],
                request.form['price'], request.form['type'], "images/cuisine6.jpg", restaurant_id))
        con.commit()
        print("added product to menu successfully")

    con.close()
    return not row

def delete_product_from_menu(restaurant_id,request):
    con = sql.connect("digin.db")
    t=(request.form['product_id'],restaurant_id)
    sqlQuery = "select name from product where id = ? and restaurant_id= ?"
    cur = con.cursor()
    cur.execute(sqlQuery,t)
    row = cur.fetchone()

    if row:
        cur.execute("DELETE from product where id = ? and restaurant_id = ?",t)
        con.commit()
        print("product deleted from menu successfully")

    con.close()
    return row

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

def get_menu(restaurant_id):
    con = sql.connect("digin.db")
    con.row_factory = sql.Row
    t=(restaurant_id,)
    sqlQuery = "select * from product where restaurant_id= ?"
    cur = con.cursor()
    cur.execute(sqlQuery,t)
    rows = cur.fetchall()
    return  rows

def update_product_in_menu(product_id, request):
    con = sql.connect("digin.db")
    con.row_factory = sql.Row
    sqlQuery = "UPDATE product SET name= ?,description= ?,price=?,type= ?,picture= ?,restaurant_id= ? WHERE id = ?",(request.form['name'], request.form['description'],request.form['price'], request.form['type'], request.form['picture'], request.form['restaurant_id'],product_id)
    cur = con.cursor()  
    cur.execute(sqlQuery)
    row = cur.fetchone()
    return  row

def create_customer_orders(request): # C part of CRUD
    con = sql.connect("digin.db")
    cur = con.cursor()
    cur.execute("INSERT INTO order (restaurant_id,customer_id,status,description,cost,review) VALUES (?,?,?,?,?,?)",
                    (request.form['restaurant_id'], request.form['customer_id'], request.form['status'], request.form['description'], request.form['cost'], request.form['review']))
    con.commit()
    print "added user successfully"

    con.close()

##cart code
def add_to_cart(customer_id,request):
    con = sql.connect("digin.db")
    sqlQuery = "select restaurant_id from cart where customer_id= ?"
    t=(customer_id,)
    cur = con.cursor()
    cur.execute(sqlQuery, t)
    row = cur.fetchone()
    
    if row:
        restaurant_id_from_customer = request.form['restaurant_id']
        current_restaurant_id = row[0]
        if(restaurant_id_from_customer!=str(current_restaurant_id)):
            return "ERR:DIFFERENT_RESTAURANT_ID"
        
    
    
    
    t = (request.form['product_id'], customer_id)
    sqlQuery = "select customer_id, restaurant_id from cart where product_id = ? and customer_id= ?"
    cur = con.cursor()
    cur.execute(sqlQuery, t)
    row = cur.fetchone()
    
    quantity = int(request.form['quantity'])
    cost = float(request.form['cost'])
    total_cost = str(quantity*cost)

    if not row:  #newly added to cart
        cur.execute(
            "INSERT INTO cart (customer_id,product_id,quantity,cost,restaurant_id) VALUES (?,?,?,?,?)",
            (
                customer_id, request.form['product_id'],
                request.form['quantity'],total_cost,request.form['restaurant_id']))
        con.commit()
        print("added product to menu successfully")
    else:#update quantity
        sqlQuery = "UPDATE cart SET quantity= ?, cost=? WHERE customer_id = ? and product_id=?"
        cur = con.cursor()
        t = (request.form['quantity'], total_cost, customer_id,request.form['product_id'])
        cur.execute(sqlQuery, t)
        con.commit()
    con.close()
    return "SUCCESS"

def view_cart(customer_id):
    con = sql.connect("digin.db")
    con.row_factory = sql.Row
    t = (customer_id,)
    sqlQuery ="SELECT cart.customer_id,cart.product_id,cart.quantity,cart.cost,product.name,product.picture,product.price,product.restaurant_id FROM cart INNER JOIN product ON cart.product_id =product.id where cart.customer_id= ?"
    cur = con.cursor()
    cur.execute(sqlQuery, t)
    rows = cur.fetchall()
    con.close()
    return rows

def delete_from_cart(customer_id, product_id):
    con = sql.connect("digin.db")
    t = (customer_id,product_id)
    
    sqlQuery = "DELETE from cart where customer_id = ? and product_id = ?"
    cur = con.cursor()
    cur.execute(sqlQuery,t)
    con.commit()
    
def review_customer_orders(customer_id): # R part of CRUD
    conn = sql.connect("digin.db")
    sqlQuery = "select * from 'order' where customer_id = ? "
    t=(customer_id,)
    cur = conn.cursor()
    cur.execute(sqlQuery,t)
    rows = cur.fetchall()
    conn.close()
    return rows

def get_order_products(customer_id):
    conn = sql.connect("digin.db")
    df_order = pd.read_sql_query( "select * from 'order' where (customer_id ='" + str(customer_id) + "')", conn)
    df_order_mapping = pd.read_sql_query("select * from prod_order_mapping", conn)
    all_orders = pd.merge(df_order, df_order_mapping, left_on=['id'], right_on=['order_id'], how='inner')
    df_product_mapping = pd.read_sql_query("select * from product", conn)
    df_product_mapping.rename(inplace = True, columns={'id': 'prod_id'})
    orders = pd.merge( all_orders, df_product_mapping, left_on=['product_id'], right_on=['prod_id'], how='inner')
    conn.close()
    return orders


def placeorder(customer_id,total_cost,description):
    receipt_rows = view_cart(customer_id)
    conn = sql.connect("digin.db")
    sqlQuery = "SELECT * from cart where customer_id = ?"
    t=(customer_id,)
    cur = conn.cursor()
    cur.execute(sqlQuery,t)
    rows = cur.fetchall()
    
    row = rows[0]
    #total_cost = row[3]
    restaurant_id=row[4]
    cur.execute("INSERT INTO 'order' (restaurant_id,customer_id,status,cost,description) VALUES (?,?,?,?,?)",
                (restaurant_id,customer_id,"WAITING",total_cost,description))
    
    conn.commit()
    order_id = cur.lastrowid #it will return the most recent id of the row that the cursor instance inserted
    
    for row in rows:
        product_id = row[1]
        quantity = row[2]
        cur.execute("INSERT INTO 'prod_order_mapping' (order_id,product_id,quantity) VALUES (?,?,?)",
                    (order_id,product_id,quantity))
        conn.commit()
    
    deleteCartQuery = "DELETE from cart where customer_id = ?"
    t=(customer_id,)
    cur = conn.cursor()
    cur.execute(deleteCartQuery,t)
    conn.commit()
    
    conn.close()
    
    return receipt_rows

def search_restaurant(request):
    conn = sql.connect("digin.db")
    t=('%'+request.form['restaurant_name']+'%',)
    sqlQuery = "select * from restaurant where lower(name) LIKE lower(?)"
    cur = conn.cursor()
    cur.execute(sqlQuery,t)
    rows = cur.fetchall()
    conn.close()
    return rows

def get_orders_for_restaurant(restaurant_id):
    conn = sql.connect("digin.db")
    t=(restaurant_id,)
    sqlQuery = "select * from 'order' where restaurant_id = ?"
    cur = conn.cursor()
    cur.execute(sqlQuery,t)
    rows = cur.fetchall()
    conn.close()
    return rows

def get_order_product_details(order_id):
    conn = sql.connect("digin.db")
    t = (order_id,)
    #sqlQuery = "SELECT prod_order_mapping.quantity,product.name FROM prod_order_mapping INNER JOIN product ON prod_order_mapping.product_id =product.id where prod_order_mapping.order_id= ?"
    sqlQuery = "SELECT * FROM prod_order_mapping INNER JOIN product ON prod_order_mapping.product_id =product.id where prod_order_mapping.order_id= ?"
    cur = conn.cursor()
    cur.execute(sqlQuery, t)
    rows = cur.fetchall()
    conn.close()
    return rows

def get_customer_details(customer_id):
    conn = sql.connect("digin.db")
    t = (customer_id,)
    sqlQuery = "select * from customer where id = ?"
    cur = conn.cursor()
    cur.execute(sqlQuery, t)
    row = cur.fetchone()
    conn.close()
    return row

def get_order_status(order_id):
    conn = sql.connect("digin.db")
    t = (order_id,)
    sqlQuery = "select status from 'order' where id = ?"
    cur = conn.cursor()
    cur.execute(sqlQuery, t)
    row = cur.fetchone()
    conn.close()
    return row


def confirm_order(restaurant_id,order_id):
    conn = sql.connect("digin.db")
    t = ("CONFIRMED",int(order_id))
    sqlQuery = "UPDATE 'order' SET status= ? WHERE id = ?"
    cur = conn.cursor()
    cur.execute(sqlQuery, t)
    conn.commit()
    conn.close()    

def decline_order(restaurant_id,order_id):
    conn = sql.connect("digin.db")
    t = ("DECLINED",int(order_id))
    sqlQuery = "UPDATE 'order' SET status= ? WHERE id = ?"
    cur = conn.cursor()
    cur.execute(sqlQuery, t)
    conn.commit()
    conn.close()

def review_order(order_review,order_id):
    conn = sql.connect("digin.db")
    t = (order_review,int(order_id))
    sqlQuery = "UPDATE 'order' SET review= ? WHERE id = ?"
    cur = conn.cursor()
    cur.execute(sqlQuery, t)
    conn.commit()
    conn.close()

def get_order_review(order_id):
    conn = sql.connect("digin.db")
    t = (order_id,)
    sqlQuery = "select review from 'order' where id = ?"
    cur = conn.cursor()
    cur.execute(sqlQuery, t)
    row = cur.fetchone()
    conn.close()
    return row

def get_pending_orders(restaurant_id):
    conn = sql.connect("digin.db")
    t = (restaurant_id,"WAITING")
    sqlQuery = "select * from 'order' where restaurant_id = ? AND status = ?"
    cur = conn.cursor()
    cur.execute(sqlQuery, t)
    row = cur.fetchall()
    conn.close()
    return row
     
def get_revenue(restaurant_id):
    conn = sql.connect("digin.db")
    t = (restaurant_id,"CONFIRMED")
    sqlQuery = "select * from 'order' where restaurant_id = ? AND status = ?"
    cur = conn.cursor()
    cur.execute(sqlQuery, t)
    rows = cur.fetchall()
    revenue = 0
    for row in rows:
        revenue = revenue + row[5] 
    conn.close()
    return revenue

def modify_product(restaurant_id,request):
    con = sql.connect("digin.db")
    t=(request.form['description'],request.form['cost'], request.form['product_id'])
    sqlQuery = "UPDATE product SET description= ?, price=? where id = ?"
    cur = con.cursor()
    cur.execute(sqlQuery,t)
    con.commit()

    con.close()
    


def upload_product_image(product_id, file_name):
    con = sql.connect("digin.db")
    sqlQuery = "UPDATE product SET picture= ? where id=?"
    t=(file_name, product_id)
    cur = con.cursor()
    cur.execute(sqlQuery,t)
    con.commit()

    con.close()
    
    
    
    
    
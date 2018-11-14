from flask import Flask
from flask import request
from flask import url_for
from flask.templating import render_template
import models as dbHandler
from flask import session
from flask import redirect

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

@app.route('/')
def welcome():
    rest = dbHandler.get_all_restaurant()
    if 'username' in session:
        return render_template('index.html',restaurants=rest, logged_in=True)
    return render_template('index.html',restaurants=rest)

@app.route('/order', methods=['GET', 'POST'])
def order():
    if 'username' in session:
        return render_template('order.html',logged_in=True)
    else:
        return render_template('order.html')

@app.route('/restaurants', methods=['GET', 'POST'])
def restaurants():
    if 'username' in session:
        rest_list = dbHandler.get_all_restaurant()
        return render_template('restaurants.html',restaurants=rest_list,logged_in = True)
    else:
        rest_list = dbHandler.get_all_restaurant()
        return render_template('restaurants.html',restaurants=rest_list)

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if 'username' in session:
        return render_template('contact.html',logged_in=True)
    else:
        return render_template('contact.html')

@app.route('/search_restaurant', methods=['GET', 'POST'])
def search_restaurant():
    if(request.method=='POST'):
        if 'username' in session:
            rest = dbHandler.search_restaurant(request)
            return render_template('restaurants.html',restaurants=rest,logged_in = True)
        else:
            rest = dbHandler.search_restaurant(request)
            return render_template('restaurants.html',restaurants=rest)  

@app.route('/orderslist', methods=['GET', 'POST'])
def orderslist():
    return render_template('orders-list.html')

@app.route('/menu', methods=['GET', 'POST'])
def menu():
    if 'username' in session:
        logged_in = True
    else:
        logged_in = False
    
    restaurant_id = request.args.get('restaurant_id')
    menu = dbHandler.get_menu(restaurant_id)
    return render_template('menu.html',menu=menu,logged_in=logged_in)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if(request.method=='POST'):
        if dbHandler.create_customer(request):
            msg="<p style=\"color:red\">Account successfully created</p>"
        else:
            msg="<p style=\"color:red\">Could not create user user account</p>"
        return render_template('register.html',message_customer=msg)
    return render_template('register.html')

@app.route('/index', methods=['GET', 'POST'])
def index():
    rest = dbHandler.get_all_restaurant()
    if 'username' in session:
        return render_template('index.html', restaurants=rest, logged_in=True)
    else:
        return render_template('index.html', restaurants=rest)

@app.route('/checkout',methods=['GET','POST'])
def checkout():
    if 'username' in session:
        return render_template('checkout.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if(request.method=='POST'):
        if dbHandler.create_customer(request):
            msg="user successfully added"
        else:
            msg="could not add user"
        return render_template('result.html',message=msg)
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if(request.method=='GET'):
        if 'username' in session:
            msg = "Welcome " + session['username'] + "!"
            rest = dbHandler.get_all_restaurant()
            render_template("index.html", restaurants=rest, logged_in=True, message=msg)
        else:
            return render_template("login.html")

    elif(request.method=='POST'):
        if dbHandler.authenticate(request):
            session['username'] = request.form['username']
            row = dbHandler.get_customer_from_username(request.form['username'])

            session['id'] = row[0]
            msg = "Welcome "+session['username']+"!"
            rest = dbHandler.get_all_restaurant()
        else:
            
            msg = "Incorrect Credentials."
            return render_template("login.html",message=msg)
    return render_template("index.html",restaurants=rest,logged_in=True,message=msg)
        


@app.route('/restaurant_register', methods=['GET', 'POST'])
def restaurant_register():
    if(request.method=='POST'):
        if dbHandler.create_restaurant(request):
            msg="<p style=\"color:red\">restaurant successfully added</p>"
        else:
            msg="<p style=\"color:red\">could not add restaurant</p>"
        return render_template('register.html', message_restaurant=msg)
    return render_template('register.html')


@app.route('/restaurant_login', methods=['GET', 'POST'])
def restaurant_login():
    if(request.method=='GET'):
        if 'username' in session:
            return render_template("restaurant_main.html",logged_in=True,message="Welcome "+session['username']+"!")

        else:
            return render_template("login.html",message="")
    elif request.method=='POST':
        if dbHandler.restaurant_authenticate(request):
            session['username'] = request.form['username']
            row = dbHandler.get_restaurant_id_by_username(request.form['username'])
            #row=dbHandler.get_restaurant_by_name(request.form['name'])
            session['id'] = row[0]


            msg = "Welcome "+session['username']+"!"
        else:

            msg = "Incorrect Credentials."
            return render_template("login.html",message="Invalid credentials")
    return render_template("restaurant_main.html",logged_in=True,message=msg)


@app.route('/logout')
def logout():
    # remove the username from the session if it is there
    session.pop('username', None)
    session.pop('id',None)
    return redirect(url_for('index'))


def get_menu_of_restaurant(restaurant_id):
    menu = dbHandler.get_menu(restaurant_id)
    return menu

@app.route('/add_product_to_menu', methods=['GET', 'POST'])
def add_product_to_menu():
    if (request.method == 'GET'):
        if 'username' in session:
            return render_template("add_to_menu.html", message="Welcome " + session['username'] + "!")
        else:
            return render_template("restaurant_login.html",message="")
    elif request.method == 'POST':
        if dbHandler.add_product_to_menu(session['id'],request):
            msg = "product successfully added"
        else:
            msg = "could not add product"
        return render_template('add_to_menu.html', message=msg)

@app.route('/delete_product_from_menu', methods=['GET', 'POST'])
def delete_product_from_menu():
    if (request.method == 'GET'):
        if 'username' in session:
            menu = get_menu_of_restaurant(session['id'])
            return render_template("delete_from_menu.html", menu=menu)
        else:
            return render_template("login.html",message="")
    elif request.method == 'POST':
        if dbHandler.delete_product_from_menu(session['id'],request):
            msg = "product successfully deleted"
        else:
            msg = "could not delete product"
        menu = get_menu_of_restaurant(session['id'])
        return render_template("delete_from_menu.html", menu=menu,message=msg)
        #return render_template('delete_from_menu.html', message=msg)

@app.route('/add_to_cart',methods=['POST'])
def add_to_cart():
    if 'username' in session:
        row = dbHandler.get_customer_from_username(session['username'])
        restaurant_id = request.form['restaurant_id']
        status_code = dbHandler.add_to_cart(row[0],request)
        if(status_code=="ERR:DIFFERENT_RESTAURANT_ID"):
            return redirect(url_for('menu', restaurant_id=restaurant_id,err=True,err_message="Looks like you chose a different restaurant this time. Empty your cart and then try again!"))
        menu = dbHandler.get_menu(restaurant_id)
        return redirect(url_for('menu', restaurant_id=restaurant_id))
    else:
        return render_template('login.html')
     

@app.route('/view_cart',methods=['GET','POST'])
def view_cart():
    if 'username' in session:
        customer = dbHandler.get_customer_from_username(session['username'])
        rows=dbHandler.view_cart(customer[0])

        return render_template('view_cart.html', items=rows, logged_in = True)
    else:
        return render_template('login.html')

@app.route('/update_cart',methods=['POST'])
def update_cart():
    if 'username' in session:
        customer_id = request.form['customer_id']
        dbHandler.add_to_cart(customer_id,request)
        rows=dbHandler.view_cart(customer_id)
        return render_template('view_cart.html', items=rows)
    else:
        return render_template('login.html')

@app.route('/delete_from_cart',methods=['POST'])
def delete_from_cart():
    if 'username' in session:
        customer_id = request.form['customer_id']
        product_id = request.form['product_id']
        dbHandler.delete_from_cart(customer_id, product_id)
        rows=dbHandler.view_cart(customer_id)
        return render_template('view_cart.html', items=rows)
    else:
        return render_template('login.html')

@app.route('/vieworders', methods=['GET', 'POST'])
def vieworders():
    if 'username' in session:
        customer_id = session['id']
        ordr = dbHandler.review_customer_orders(customer_id)
        prod = dbHandler.get_order_products(customer_id)
        return render_template('vieworders.html',orders=ordr,products = prod,logged_in = True )
    else:
        return render_template('index.html')

@app.route('/placeorder/<total_cost>', methods=['GET'])
def placeorder(total_cost):
    if 'username' in session:
        customer_id = session['id']
        dbHandler.placeorder(customer_id,total_cost)
        return render_template('place_order.html')


@app.route('/view_orders_for_restaurant', methods=['GET','POST'])
def view_orders_for_restaurant():
    if 'username' in session:
        restaurant_id = session['id']
        ordr = dbHandler.get_orders_for_restaurant(restaurant_id)
        return render_template('restaurant_view_orders.html',orders=ordr,logged_in = True )
    else:
        return render_template('index.html')


@app.route('/view_details_of_order', methods=['GET' , 'POST'])
def view_details_of_order():
    if 'username' in session:
        
        order_status = dbHandler.get_order_status(request.form['order_id'])
        order_product_details = dbHandler.get_order_product_details(request.form['order_id'])
        customer_details=dbHandler.get_customer_details(request.form['c_id'])
        #print(order_product_details)
        #print(customer_details[1])
        return render_template('view_order_details_by_restaurant.html',order_status=order_status[0],customer_details=customer_details,order_product_details=order_product_details,logged_in = True )
    else:
        return render_template('index.html')

@app.route('/confirm_order', methods=['GET','POST'])
def confirm_order():
    if 'username' in session:
        restaurant_id = session['id']
        dbHandler.confirm_order(restaurant_id,request.form['order_id'])
        #print("order id",request.form['order_id'])
        ordr = dbHandler.get_orders_for_restaurant(restaurant_id)
        return render_template('restaurant_view_orders.html', orders=ordr, logged_in=True)
    else:
        return render_template('index.html')


if __name__ == "__main__":
    app.debug=True
    app.run()

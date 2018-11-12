from flask import Flask
from flask import request
from flask.templating import render_template
import models as dbHandler
from flask import session

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

@app.route('/')
def welcome():
    rest = dbHandler.get_all_restaurant()
    return render_template('index.html',restaurants=rest)

@app.route('/order', methods=['GET', 'POST'])
def order():
    return render_template('order.html')

@app.route('/restaurants', methods=['GET', 'POST'])
def restaurants():
    return render_template('restaurants.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    return render_template('contact.html')

@app.route('/orderslist', methods=['GET', 'POST'])
def orderslist():
    return render_template('orders-list.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if(request.method=='POST'):
        if dbHandler.create_customer(request):
            msg="Account successfully created"
        else:
            msg="<p style=\"color:red\">Could not create user user account</p>"
        return render_template('register.html',message=msg)
    return render_template('register.html')

@app.route('/index', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

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
        return render_template("login.html")
    elif(request.method=='POST'):
        if dbHandler.authenticate(request):
            session['username'] = request.form['username']
            
            msg = "Welcome "+session['username']+"!"
            rest = dbHandler.get_all_restaurant()
        else:
            
            msg = "Incorrect Credentials."
            return render_template("login.html",message=msg)
    return render_template("index.html",restaurants=rest,logged_in=True,message=msg)
        


@app.route('/restaurant/signup', methods=['GET', 'POST'])
def signup_restaurant():
    if(request.method=='POST'):
        if dbHandler.create_customer(request):
            msg="restaurant successfully added"
        else:
            msg="could not add restaurant"
        return render_template('result.html', message=msg)
    return render_template('restaurant_signup.html')


@app.route('/restaurant/login', methods=['GET', 'POST'])
def login_restaurant():
    if(request.method=='GET'):
        if 'restaurant_name' in session:
            return render_template("restaurant_main.html",message="Welcome "+session['restaurant_name']+"!")
        else:
            return render_template("restaurant_login.html",message="")
    elif request.method=='POST':
        if dbHandler.authenticate(request):
            session['restaurant_name'] = request.form['restaurant_name']
            row=dbHandler.get_restaurant_by_name(request.form['restaurant_name'])
            session['restaurant_id'] = row['id']

            log_in = True
            msg = "Welcome "+session['restaurant_name']+"!"
        else:
            log_in = False
            msg = "Incorrect Credentials."
            return render_template("restaurant_login.html",message="Invalid credentials")
    return render_template("restaurant_main.html",message=msg)


@app.route('/restaurant/add_to_menu', methods=['GET', 'POST'])
def add_product_to_menu():
    if (request.method == 'GET'):
        if 'restaurant_name' in session:
            return render_template("add_to_menu.html", message="Welcome " + session['restaurant_name'] + "!")
        else:
            return render_template("restaurant_login.html",message="")
    elif request.method == 'POST':
        if dbHandler.add_product_to_menu(session['restaurant_id'],request):
            msg = "product successfully added"
        else:
            msg = "could not add product"
        return render_template('add_to_menu.html', message=msg)

@app.route('/restaurant/add_to_menu', methods=['GET', 'POST'])
def delete_product_from_menu():
    if (request.method == 'GET'):
        if 'restaurant_name' in session:
            return render_template("add_to_menu.html", message="Welcome " + session['restaurant_name'] + "!")
        else:
            return render_template("restaurant_login.html",message="")
    elif request.method == 'POST':
        if dbHandler.add_product_to_menu(session['restaurant_id'],request):
            msg = "product successfully added"
        else:
            msg = "could not add product"
        return render_template('add_to_menu.html', message=msg)

@app.route('/add_to_cart',methods=['POST'])
def add_to_cart():
    if 'username' in session:
        if dbHandler.add_to_cart(session['user_id'],request):
            msg = "product successfully added to cart"
        else:
            msg = "could not add product to cart"
        return render_template('add_to_cart.html', message=msg)
    else:
        return render_template("login.html", message="")

@app.route('/view_cart',methods=['POST'])
def view_cart():
    if 'username' in session:
        rows=dbHandler.view_cart(session['user_id'],request)
        #rows contains uid,pid,qnty
        return render_template('view_cart.html', rows)


if __name__ == "__main__":
    app.debug=True
    app.run()

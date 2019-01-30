from flask import Flask, render_template, request, redirect
from flask import jsonify, url_for, flash
from sqlalchemy import create_engine, asc
from sqlalchemy import *
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Brand, Product, User
from flask import session as login_session
import random
import string
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests

app = Flask(__name__)

CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Technology Brands"


# Connect to Database and create database session
engine = create_engine('postgresql:///catalog.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    return render_template('login.html', STATE=state)


@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('''Current user is
        already connected.'''),
                                 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']
    user_id = getUserID(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ''' " style = "width: 300px; height:
    300px;border-radius: 150px;-webkit-border-radius:
    150px;-moz-border-radius: 150px;"> '''
    flash("you are now logged in as %s" % login_session['username'])
    print "done!"
    return output

    # DISCONNECT - Revoke a current user's token and reset their login_session


def createUser(login_session):
    newUser = User(name=login_session['username'], email=login_session[
                   'email'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id


def getUserInfo(user_id):
    user = session.query(User).filter_by(id=user_id).one()
    return user


def getUserID(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except Exception:
        return None


@app.route('/gdisconnect')
def gdisconnect():
    access_token = login_session.get('access_token')
    if access_token is None:
        print 'Access Token is None'
        response = make_response(json.dumps('''Current user not
        connected.'''), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    print 'In gdisconnect access token is %s', access_token
    print 'User name is: '
    print login_session['username']
    u = 'https://accounts.google.com/o/oauth2/revoke?token=%s'
    url = u % login_session['access_token']
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    print 'result is '
    print result
    if result['status'] == '200':
        del login_session['access_token']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        # del login_session['picture']
        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return redirect('/')
    else:
        response = make_response(json.dumps('''Failed to revoke token
         for given user.''', 400))
        response.headers['Content-Type'] = 'application/json'
        return response


@app.route('/techbrands/<int:brand_id>/products/JSON')
def showProductsJSON(brand_id):
    products = session.query(Product).filter_by(brand_id=brand_id).all()
    return jsonify(Product=[i.serialize for i in products])


@app.route('/techbrands/<int:brand_id>/products/<int:product_id>/JSON')
def specificProductJSON(brand_id, product_id):
    product = session.query(Product).filter_by(id=product_id).one()
    if brand_id != product.brand_id:
        return "nonvalid url"
    else:
        return jsonify(Product=product.serialize)


@app.route('/techbrands/JSON')
def brandsJSON():
    brands = session.query(Brand).all()
    return jsonify(Brand=[i.serialize for i in brands])


@app.route('/')
@app.route('/techbrands/')
def showBrnds():
    brands = session.query(Brand).all()
    products = session.query(Product).order_by(desc(Product.id)).limit(8)
    return render_template('showbrands.html', brands=brands, products=products)


@app.route('/techbrands/<int:brand_id>/')
@app.route('/techbrands/<int:brand_id>/products/')
def showProducts(brand_id):
    brand = session.query(Brand).filter_by(id=brand_id).one()
    products = session.query(Product).filter_by(brand_id=brand_id).all()
    return render_template('showproducts.html', brand=brand, products=products)


@app.route('/techbrands/<int:brand_id>/products/<int:product_id>/')
def specificProduct(brand_id, product_id):
    brand = session.query(Brand).filter_by(id=brand_id).one()
    products = session.query(Product).filter_by(id=product_id).one()
    creator = getUserInfo(products.user_id)
    if brand.id == products.brand_id:
        if 'username' not in login_session or creator.id != login_session[
                'user_id']:
                return render_template(
                    'publicspecificproduct.html',
                    brand=brand, product=products,
                    product_id=product_id, brand_id=brand_id)
        else:
            return render_template(
                'specificproduct.html',
                brand=brand, product=products,
                product_id=product_id, brand_id=brand_id)
    else:
        return "Error in url " + """<a href='/'>Back to main page </a>"""


@app.route(
    '/techbrands/<int:brand_id>/products/new/', methods=['GET', 'POST'])
def newProduct(brand_id):
    if 'username' not in login_session:
        return redirect('/login')

    if request.method == 'POST':
        newProduct = Product(name=request.form[
            'name'], description=request.form[
                'description'], price=request.form[
                    'price'], brand_id=brand_id, user_id=login_session[
                        'user_id'])
        flash('New Product %s Successfully Added' % newProduct.name)
        session.add(newProduct)
        session.commit()
        return redirect(url_for('showProducts', brand_id=brand_id))
    else:
        return render_template('newproduct.html', brand_id=brand_id)


@app.route(
    '/techbrands/<int:brand_id>/products/<int:product_id>/edit/',
    methods=['GET', 'POST'])
def editProduct(brand_id, product_id):
    editedProduct = session.query(Product).filter_by(id=product_id).one()
    if 'username' not in login_session:
        return redirect('/login')

    if editedProduct.user_id != login_session['user_id']:
        return """You are not authorized
        to edit this Product. Please create your own Product in order to
        edit."""

    if request.method == 'POST':
        if request.form['name']:
            editedProduct.name = request.form['name']
        if request.form['description']:
            editedProduct.description = request.form['description']
        if request.form['price']:
            editedProduct.price = request.form['price']
        flash('Product %s Successfully Edited' % editedProduct.name)
        session.add(editedProduct)
        session.commit()
        return redirect(url_for('showProducts', brand_id=brand_id))
    else:
        return render_template(
            'editproduct.html', brand_id=brand_id, product_id=product_id)


@app.route(
    '/techbrands/<int:brand_id>/products/<int:product_id>/delete/',
    methods=['GET', 'POST'])
def deleteProduct(brand_id, product_id):
    productToDelet = session.query(Product).filter_by(id=product_id).one()

    if 'username' not in login_session:
        return redirect('/login')

    if productToDelet.user_id != login_session['user_id']:
        return """You are not authorized
        to delete this Product. Please create your own Product in order to
        delete."""
    if request.method == 'POST':
        flash('Product %s Successfully Deleted' % productToDelet.name)
        session.delete(productToDelet)
        session.commit()
        return redirect(url_for('showProducts', brand_id=brand_id))
    else:
        return render_template(
            'deleteproduct.html', brand_id=brand_id, product_id=product_id)


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)

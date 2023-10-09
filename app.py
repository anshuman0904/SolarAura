from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify, abort
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re

import stripe


app = Flask(__name__)

app.config['STRIPE_PUBLIC_KEY'] = 'pk_test_51NHjYsSFPzAEdpQfGp5nECydBZVoQfwtVCq3zF9I46UdzDgNSXfgXRL6s0hdxzFRaSacVroAeQXgqMAaEiIsCgdT00Fawb0Dh4'
app.config['STRIPE_SECRET_KEY'] = 'sk_test_51NHjYsSFPzAEdpQf56ttCb9yLl5BK6ECZLFX9BcxUVKzVmNwvbNP3RPJ1XdOSYYRTQi5IXWMVoHxm5kUp9GbNJZl00RgXlvS7W'

stripe.api_key = app.config['STRIPE_SECRET_KEY']

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'solaraura'

app.config['SECRET_KEY'] = '8d3c2c136be85cf7de1435eb'

mysql = MySQL(app)

@app.route("/")
@app.route("/home")
def home_page():
    return render_template('home.html')


@app.route('/login', methods =['GET', 'POST'])
def login():
	msg = ''
	if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
		email = request.form['email']
		password = request.form['password']
		cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute('SELECT * FROM accounts WHERE email = % s AND password = % s', (email, password, ))
		account = cursor.fetchone()
		if account:
			session['loggedin'] = True
			session['email'] = account['email']
			session['fname'] = account['fname']
			return render_template('home.html')
		else:
			msg = 'Incorrect email / password !'
	return render_template('login1.html', msg = msg)

@app.route('/logout')
def logout():
	session.pop('loggedin', None)
	session.pop('email', None)
	session.pop('fname', None)
	return redirect(url_for('home_page'))

@app.route('/register', methods =['GET', 'POST'])
def register():
	msg = ''
	if request.method == 'POST' and 'email' in request.form and 'password' in request.form :
		email = request.form['email']
		password = request.form['password']
		fname = request.form['fname']
		lname = request.form['lname']
		country = request.form.get('country')
		cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute('SELECT * FROM accounts WHERE email = %s', (email, ))
		account = cursor.fetchone()
		if account:
			msg = 'Account already exists !'
			return render_template('login1.html', msg = msg)

		else:
			cursor.execute('INSERT INTO accounts VALUES (%s, %s, %s, %s, %s)', (fname, lname, email, country, password))
			mysql.connection.commit()
			msg = 'You have successfully registered !'
			cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
			cursor.execute('SELECT * FROM accounts WHERE email = % s', (email, ))
			account = cursor.fetchone()
			if account:
				session['loggedin'] = True
				session['email'] = email
				session['fname'] = fname
				msg = 'Logged in successfully !'
				return render_template('home.html', msg = msg)
	elif request.method == 'POST':
		msg = 'Please fill out the form !'
	return render_template('register1.html', msg = msg)

@app.route('/about')
def about():
	return render_template('aboutus.html')

@app.route('/commercial')
def commercial():
	return render_template('commercial.html')

@app.route('/residential')
def residential():
    '''
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price': 'price_1GtKWtIdX0gthvYPm4fJgrOr',
            'quantity': 1,
        }],
        mode='payment',
        success_url=url_for('thanks', _external=True) + '?session_id={CHECKOUT_SESSION_ID}',
        cancel_url=url_for('index', _external=True),
    )
    '''
    return render_template(
        'residential.html', 
        #checkout_session_id=session['id'], 
        #checkout_public_key=app.config['STRIPE_PUBLIC_KEY']
    )

@app.route('/stripe_pay')
def stripe_pay():
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price': 'price_1NyqstSFPzAEdpQf3AKmu26L',
            'quantity': 1,
        }],
        mode='payment',
        success_url=url_for('thanks', _external=True) + '?session_id={CHECKOUT_SESSION_ID}',
        cancel_url=url_for('residential', _external=True),
    )
    return {
        'checkout_session_id': session['id'], 
        'checkout_public_key': app.config['STRIPE_PUBLIC_KEY']
    }

@app.route('/thanks')
def thanks():
    return render_template('thanks.html')

@app.route('/stripe_webhook', methods=['POST'])
def stripe_webhook():
    print('WEBHOOK CALLED')

    if request.content_length > 1024 * 1024:
        print('REQUEST TOO BIG')
        abort(400)
    payload = request.get_data()
    sig_header = request.environ.get('HTTP_STRIPE_SIGNATURE')
    endpoint_secret = 'YOUR_ENDPOINT_SECRET'
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        # Invalid payload
        print('INVALID PAYLOAD')
        return {}, 400
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        print('INVALID SIGNATURE')
        return {}, 400

    # Handle the checkout.session.completed event
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        print(session)
        line_items = stripe.checkout.Session.list_line_items(session['id'], limit=1)
        print(line_items['data'][0]['description'])

    return {}

@app.route('/get_location', methods=['POST'])
def get_location():
    data = request.get_json()
    latitude = data.get('latitude')
    longitude = data.get('longitude')
    # You can use a geocoding service here to get the location information
    location = f"Latitude: {latitude}, Longitude: {longitude}"
    return jsonify({'location': location})

@app.route('/careers')
def careers():
	return render_template('careers.html')

@app.route('/contact')
def contact():
	return render_template('contact.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
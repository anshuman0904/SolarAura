# SolarAura Web Application Documentation

Welcome to the documentation for the SolarAura web application. This Flask-based project serves as a platform for managing residential and commercial solar energy solutions. The application includes features such as user authentication, registration, and forms for capturing information about both residential and commercial clients. Additionally, it integrates with Stripe for payment processing.

# Installation

To run the SolarAura web application locally, follow these steps:

## 1. Clone the Repository

```bash
git clone https://github.com/anshuman0904/SolarAura.git
cd SolarAura
```

## 2. Create a Virtual Environment
It's recommended to use a virtual environment to isolate project dependencies. If you don't have virtualenv installed, you can install it using:
```bash
pip install virtualenv
```
Now, create and activate the virtual environment:
```bash
# On Windows
python -m venv venv
.\venv\Scripts\activate

# On macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

## 3. Install Dependencies
Install the project dependencies listed in the requirements.txt file:
```bash
pip install -r requirements.txt
```
This command will install all the necessary libraries and packages needed for the project.

## 4. Configure the Application
```bash
# app.py
app.config['SECRET_KEY'] = "your_secret_key"
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = "your_password"
app.config['MYSQL_DATABASE_DB'] = 'solaraura'

app.config['STRIPE_PUBLIC_KEY'] = "your_api_key"
app.config['STRIPE_SECRET_KEY'] = "your_secret_key"

stripe.api_key = app.config['STRIPE_SECRET_KEY']
```
## 5. Run the Application
```bash
python app.py
# This project is developed and tested with Python 3.11. Make sure you have a compatible version of Python installed before proceeding.
```

# Authentication and Authorization

The SolarAura application uses a Flask session for user authentication. Users can log in, register, and log out using the provided routes. The application uses MySQL to store user account information.

## Login

The `/login` route allows users to log in using their email and password.

## Registration

The `/register` route handles user registration, ensuring that accounts are unique.

## Logout

Users can log out using the `/logout` route.

# Forms and Data Submission

The SolarAura application uses forms to collect information from users. Here are examples of routes that handle data submission:

## Commercial Form

- Route: `/commercial`
- View: `commercial`
- Method: POST
- Fields: `bizName`, `contactName`, `bizType`, `phone`, `energy`, `roofArea`, `address`, `comments`, `latitude`, `longitude`

## Residential Form

- Route: `/residential`
- View: `residential`
- Method: POST
- Fields: `Name`, `roofArea`, `electric`, `phone`, `address`, `choice`, `latitude`, `longitude`

# Payment Integration

SolarAura uses Stripe for payment processing. When users submit certain forms (e.g., residential or commercial forms), they are redirected to the `/payment` route. From there, they can proceed with the payment using the `/stripe_pay` route.

## Payment Route

- Route: `/payment`
- View: `payment`
- Method: GET
- Integrates with Stripe for payment processing.

## Stripe Payment Route

- Route: `/stripe_pay`
- View: `stripe_pay`
- Method: GET
- Generates a Stripe checkout session for handling payments.

# Webhooks

The SolarAura application includes a webhook endpoint (`/stripe_webhook`) for handling events from Stripe. Currently, it listens for the `checkout.session.completed` event to process completed payments.

## Webhook Route

- Route: `/stripe_webhook`
- View: `stripe_webhook`
- Method: POST
- Listens for Stripe events and processes them accordingly.

# Location Information

The application allows users to submit location information through the `/get_location` route. This information is used to capture latitude and longitude data.

## Get Location Route

- Route: `/get_location`
- View: `get_location`
- Method: POST
- Handles JSON data containing latitude and longitude.

# Additional Features and Pages

In addition to the core functionalities, the SolarAura application includes other features and pages:

## Thanks Page

- Route: `/thanks`
- View: `thanks`
- Displays a thank you message after a successful payment.

## Careers Page

- Route: `/careers`
- View: `careers`
- Provides information about career opportunities at SolarAura.

## Contact Page

- Route: `/contact`
- View: `contact`
- Displays contact information for users to get in touch.


## Conclusion:

```markdown
# Conclusion

Congratulations! You've successfully set up and explored the SolarAura web application. If you have any questions, encounter issues, or want to contribute to the project, feel free to reach out to our team.

Thank you for choosing SolarAura!

"""Route President"""
from flask import Flask, render_template, url_for, redirect, flash, session
from forms import LoginForm, RegistrationForm
import os
import json
import requests
from requests.exceptions import ConnectionError

# a few gloabls
app = Flask(__name__)
host_url = """https://ghastly-vault-37613.herokuapp.com/"""
headers = {
        'content-type': "application/json",
        'cache-control': "no-cache"
        }

app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') or 'YT\x89\xc9\xed\x88K>}\t\x01\xf0\xe6\xc94\\\xde\x85\x96H\x11\x88\xe7\x8b'

@app.route('/')
def start():
    """the home page"""
    return redirect(url_for('home'))

@app.route('/landing')
def home():
    """landing page render -> change of plan the landing page will display tables that display the last 2 advisories"""
    return render_template('landing_page.html')

@app.route('/admin')
def admin():
    """display the admin's tips approval page"""
    # here we connect to the api using authentication data provided and then receive the response and parse it on to the template
    headers = {}
    headers['x-access-token'] = session['token']
    pred_url = host_url + '''predictions/'''
    response = requests.get(pred_url, headers=headers)
    if response.status_code == 200:
        # success
        preds = response.json()  # -> a dictionary with list of dictionaries
        predictions = preds['predictions']
    if response.status_code == 401:
        # unauthorized attempt
        flash("Session expired please login again", 'info')
        return redirect(url_for('login'))
    return render_template('admin/admin.html', predictions=predictions)

@app.route("/users")
def user_predictions():
    """Renders the approved predictions"""
    token = session['token']
    headers = {
        'x-access-token' : token
    }
    pred_url = host_url + '''predictions/'''
    response = requests.get(pred_url, headers=headers)
    if response.status_code == 200:
        # success
        preds = response.json()  # -> a dictionary with list of dictionaries
        predictions = preds['predictions']
    if response.status_code == 403:
        # unauthorized attempt
        flash("Session expired please login again", 'info')
        return redirect(url_for('login'))
    else:
        flash("Problem logging in", 'danger')
        return redirect(url_for('login'))
    return render_template('user/user.html', predictions=predictions)

@app.route("/login", methods=['GET', 'POST'])
def login():
    """authenticate account with the api so as to receive the api token"""
    form = LoginForm()
    login_endpoint = host_url + """users/login"""
    if form.validate_on_submit():
        # form data processing
        data = {
          'user_name': form.user_name.data,
          'password': form.password.data
        }
        try:
            response = requests.post(login_endpoint, data=json.dumps(data), headers=headers)
        except ConnectionError:
            # failed to connect to the api due to netwrok issues
            flash("Problem connecting to Ghastly API", 'warning')
            return "Try AGain LATer", 500
        if response.status_code == 200:
            # successfully verified-> retrieve the json data and get token
            response_data = response.json()
            token = response_data['token']
            admin = response_data['admin']
            # add the user to session and redirect to users/dashboard
            session['user_name'] = form.user_name.data
            session['token'] = token
            # should only redirect to users if the logged in person is not an administrator -> how do we know that a user is an admin
            if admin:
                return redirect(url_for('admin'))
            else:
                return redirect(url_for('user_predictions'))
        flash('{}'.format(response.status_code), 'danger')
    return render_template('user/login.html', form=form)


@app.route('/logout')
def logout():
    """disowns an in session token"""
    session.pop('user_name', None)
    session.pop('token', None)
    return redirect(url_for('home'))

@app.route("/register", methods=['GET', 'POST'])
def register():
    """Post new user data to the api"""
    # render a registration form and parse data to backend fields: name, user name, email, and pasword
    form = RegistrationForm()
    if form.validate_on_submit():
        # we have the validate go
        data = {
            'name' : form.name.data,
            'user_name' : form.user_name.data,
            'email' : form.email.data,
            'password' : form.password.data
        }
        # send the data to api await response and return template accordingly
        reg_endpoint = host_url + '''users/register'''
        try:
            response = requests.post(reg_endpoint, data=json.dumps(data), headers=headers)
        except ConnectionError:
            # failed to connect to the api due to netwrok issues
            flash("Problem connecting to Ghastly API", 'warning')
            return "Try AGain LATer", 500
        if response.status_code == 201:
            flash("Account Created Succesfully", 'success')
            return redirect(url_for('login'))
        # ****************** else condition ********************** like say a condition in which the user has already been registered
        elif response.status_code == 400:
            flash("Bad request", 'danger')
            # problem with the submitted field data -> this very unlikely to occur
            return render_template('user/register.html', form=form)
        else:
            # unknown problems : -> eradicate using tests..> u r such a rookie programmer
            flash("unknown problem {}".format(response.status_code), 'danger')
            return render_template('user/register.html', form=form)
      
    return render_template('user/register.html', form=form)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')




def log_in():
    """For as long as someone's token is valid their account should be active as well-> their email should be inside the session variable"""

if __name__ == '__main__':
    app.run(debug=True)
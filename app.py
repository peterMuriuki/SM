"""Route President"""
from flask import Flask, render_template, url_for, redirect, flash
from forms import LoginForm, RegistrationForm
import os
import requests


app = Flask(__name__)
host_url = """https://ghastly-vault-37613.herokuapp.com/"""
token = None

app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') or 'YT\x89\xc9\xed\x88K>}\t\x01\xf0\xe6\xc94\\\xde\x85\x96H\x11\x88\xe7\x8b'

@app.route('/')
def start():
    """the home page"""
    return redirect(url_for('home'))

@app.route('/landing')
def home():
    """landing page render"""
    return render_template('admin/landing_page.html')

@app.route('/admin')
def admin():
    """display the admin's tips approval page"""
    # here we connect to the api using authentication data provided and then receive the response and parse it on to the template
    headers = {
        'x-access-token' : token
    }
    pred_url = host_url + '''predictions/'''
    response = requests.get(pred_url, headers=headers)
    if response.status_code == 200:
        # success
        preds = response.json()  # -> a dictionary with list of dictionaries
        predictions = pred['predictions']
    
    return render_template('admin/admin.html', predictions=predictions)

@app.route("/users")
def user_predictions():
    """Renders the approved predictions"""
    return render_template('admin/user.html')

@app.route("/login")
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
        response = requests.post(login_endpoint, data=data)
        if response.status_code == 200:
            # succesfully verified-> retrieve the json data and get token
            respose_data = response.json()
            token = response_data['token']
            # add the user to session and redirect to users/dashboard
            session['token'] = token
            # should only redirect to users if the logged in person is not an administrator
            return redirect(url_for('admin'))
    return render_template('admin/login.html', form=form)


@app.route('/logout')
def logout():
    """disowns an in session token"""
    session.pop('token', None)
    return redirect(url_for('home'))

@app.route("/register")
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
        response = requests.post(reg_endpoint, data=data)
        if response.status_code == 201:
            flash("Account Created Succesfully")
            return redirect(url_for('login'))
        # ****************** else condition ********************** like say a condition in which the user has already been registered
        elif response.status_code == 400:
            # problem with the submitted field data -> this verry unlikely to occur
            return render_template('admin/register.html', form=form)
        else:
            # unknown problems : -> eradicate using tests. u r such a rookie programmer
            return render_template('admin/register.html', form=form)
      
    return render_template('admin/register.html', form=form)

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
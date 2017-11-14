"""Route President"""
from flask import Flask, render_template, url_for, redirect
from forms import Loginform, Registrationform
import os
import requests


app = Flask(__name__)
host_url = """https://ghastly-vault-37613.herokuapp.com/"""

app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')

app.route('/')
def start():
    """the home page"""
    return redirect(url_for('home'))

app.route('/landing')
def home():
    """landing page render"""
    return render_template('admin/landing_page.html')

app.route('/admin')
def admin():
    """display the admin's tips approval page"""
    # here we connect to the api using authentication data provided and then receive the response and parse it on to the template
    return render_template('admin/admin.html', predictions= predictions)

app.route("/users")
def user_predictions():
    """Renders the approved predictions"""
    return render_template('admin/user.html')

app.route("/login")
def login():
    """authenticate account with the api so as to receive the api token"""
    form = Loginform()
    login_endpoint = host_url + """users/login"""
    if form.validate_on_submit():
      # form data processing
      data = {
        'user_name': form.user_name.data
        'password': form.password.data
      }
      response = requests.post(login_endpoint, data=data)
      if response.satatus_code == 200:
        # succesfully verified-> retrieve the json data and get token
        respose_data = response.json()
        token = response_data['token']
        # add the user to session and redirect to users/dashboard
      return render_template('admin/login.html', form=form)


app.route("/register")
def register():
    """Post new user data to the api"""
    # render a registration form and parse data to backend fields: name, user name, email, and pasword
    form = Registrationform()
    if form.validate_on_submit():
      # we have the validate go
      data = {
        'name' = form.name.data
        'user_name' = form.user_name.data
        'email' = form.email.data
        'password' = form.password.data
      }
      # send the data to api await response and return template accordingly
      reg_endpoint = host_url + '''users/register'''
      response = requests.post(reg_endpoint, data=data)
      if response.status_code == 200:
        flash("Account Created Succesfully")
        return redirect(url_for('login'))
      # ****************** else condition **********************
    return render_template('admin/register.html' form=form)

if __name__ == '__main__':
    app.run(debug=True)
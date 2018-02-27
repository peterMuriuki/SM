from flask import render_template, redirect, url_for, flash
from . import auth
from .forms import RegistrationForm, LoginForm
from flask_login import login_user, login_required, logout_user, current_user
from ..gear import Gear


gear = Gear()


@auth.route("/login", methods=['GET', 'POST'])
def login():
    """authenticate account with the api so as to receive the api token"""
    form = LoginForm()
    if form.validate_on_submit():
        # form data processing
        data = {
            'user_name': form.user_name.data,
            'password': form.password.data,
            'remember': form.rem.data
        }
        user = gear.load_user_by_user_name(data['user_name'])
        if user and user.verify_password(data['password']):
            # we have a valid user
            login_user(user, remember=data['remember'])
            if user.admin:
                return redirect('main.admin')
            else:
                return redirect('main.user_predictions')
        else:
            flash("Could not find the user", 'danger')
            return redirect('auth.login')
    return render_template('user/login.html', form=form)


@auth.route('/log_out')
@login_required
def logout():
    logout_user()  # removes and resets a user session
    return redirect(url_for('main.home'))


@auth.route("/register", methods=['GET', 'POST'])
def register():
    """Post new user data to the api"""
    # render a registration form and parse data to backend fields: name, user name, email, and password
    form = RegistrationForm()
    if form.validate_on_submit():
        # we have the validate go
        data = {
            'name': form.name.data,
            'user_name': form.user_name.data,
            'email': form.email.data,
            'password': form.password.data
        }
        registered_user = gear.register_user(data)
        if registered_user:
            # redirect to the login page
            return redirect('auth.login')
        else:
            return redirect('auth.register')
    return render_template('user/register.html', form=form)

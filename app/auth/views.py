from flask import render_template, redirect, url_for, flash
from . import auth
from .forms import RegistrationForm, LoginForm, GeneralProfile, PasswordProfile, SecondaryProfile, EmailProfile
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
                return redirect(url_for('main.admin'))
            else:
                return redirect(url_for('main.user_predictions'))
        else:
            flash("Could not find the user", 'danger')
            return redirect(url_for('auth.login'))
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
            return redirect(url_for('auth.login'))
        else:
            return redirect(url_for('auth.register'))
    return render_template('user/register.html', form=form)

@auth.route('/profile', methods=["POST", "GET"])
@login_required
def profile():
    """:
    : modify a users db details  
    """
    #forms
    general_form = GeneralProfile()
    password_form = PasswordProfile()
    email_form = EmailProfile()
    secondary_form = SecondaryProfile()
    
    if general_form.validate_on_submit() and general_form.submit.data:
        # this has disabled functionality for the time being
        pass
    if password_form.validate_on_submit() and password_form.submit.data:
        current_password = password_form.old_password.data
        new_password = password_form.new_password.data
        # we need to change the password and relogin the user and redirect them to the profile page
        user = gear.load_user_by_user_name(current_user.user_name)
        if user is not None:
            if user.verify_password(current_password):
                gear.modify_user_data(user, password=new_password)
                return redirect(url_for('auth.profile'))
    if email_form.validate_on_submit() and eamil_form.submit.data:
        user = gear.load_user_by_user_name(current_user.user_name)
        if user is not None:
            if user.verify_password(email_form.password.data):
                gear.modify_user_data(user, email=email_form.email.data)
                return redirect(url_for('auth.profile'))
            else:
                flash("Authentication error")
                return redirect(url('auth.profile'))
        else:
            #this should never happen, logically.
            pass
    if secondary_form.validate_on_submit() and secondary_form.submit.data:
        user = gear.load_user_by_user_name(current_user.user_name)
        if user is not None:
            gear.modify_user_data(user, plan=secondary_form.plan.data)
            return redirect(url_for('auth.profile'))
    user = gear.load_user_by_user_name('dapet')    
    return render_template('user/profile.html', general_form=general_form, password_form=password_form, email_form=email_form, secondary_form=secondary_form, user=user)
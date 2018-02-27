"""Route President"""
from flask import Flask, render_template, url_for, redirect, flash, session, request, Blueprint, current_app
from .forms import LoginForm, RegistrationForm, ConfirmationForm, FilterForm, AdminFilterForm
import os
import json
import requests
from requests.exceptions import ConnectionError
import datetime
from .._globals import headers, host_url

main = Blueprint('main', __name__)

@main.route('/')
def home():
    """landing page render -> change of plan the landing page will display tables that display the last several
     advisories"""
    today = datetime.date.today()
    past = today - datetime.timedelta(days=5)
    end_date = today.strftime('%d-%m-%Y')
    start_date = past.strftime('%d-%m-%Y')
    payload={
        '_from': start_date,
        '_to': end_date,
        'approved': 2
    }
    pred_url = host_url + '''predictions/'''
    response = requests.get(pred_url, headers=headers, params=payload)
    if response.status_code == 200:
        return render_template('landing_page.html', past_predictions=response.json()['predictions'])
        # that returns a list of dictionaries with keys as datetime.strftime and values as list of predictions
    else:
        #return an error page
        abort(404)


@main.route('/admin', methods=['GET', 'POST'])
def admin():
    """display the admin's tips approval page"""
    #here we connect to the api using authentication data provided and then receive the response and parse it on to the template
    form = ConfirmationForm()
    filter_form = AdminFilterForm()
    headers = {}
    filtered = True
    try:
        headers['x-access-token'] = session['token']
    except KeyError as error:
        return redirect(url_for('main.login'))
    pred_url = host_url + '''predictions/'''
    if filter_form.validate_on_submit() and filter_form.submit.data:
        """filter paramaters: """
        date_ = filter_form.date.data # This is a string of the form yyyy-mm-dd,
        #  but we need to change it to the form dd-mm-yyyy
        date_filter = date_.strftime('%d-%m-%Y')
        payload = {'q': date_filter}
        _response = requests.get(pred_url, params=payload)

        if _response.status_code == 200:
            # success
            preds = _response.json()  # -> a dictionary with list of dictionaries
            predictions = preds['predictions']
            #separate the predictions into sections: all - >predictions, staged -> ?, and approved-> approved
            approved = []
            staged = []
            fields = {}
            fields['odds'] = 1
            fields['comment'] = ''
            for pred in predictions:
                if pred['approved'] == 2:
                    approved.append(pred)
                    fields['odds'] *= pred['odds']
                    fields['comment'] += str(pred['comment'])
                elif pred['approved'] == 1:
                    staged.append(pred)
            if date_ == datetime.date.today():
                filtered = False
            else:
                filtered = True
            return render_template('admin/admin.html', predictions=predictions, approved=approved, staged=staged,
                               form=form, fields=fields, filtered=filtered, filter_form=filter_form)
        else:
            return "<h2>Problem with filtered data.</h2>"

    if form.validate_on_submit() and form.submit.data:
        # there is some admin actions taking place
        q = request.args['pred_id']
        if q is None:
            # we have an error
            raise Exception('WE have an error or abort')
        else:
            # retrieve the form details and put
            data = {
                "comment": form.confirmation_text.data,
                "approved": 2
            }
            print(data)
            pred_url += "{}".format(q)
            _response = requests.put(pred_url, data=json.dumps(data), headers=headers)
            print(_response.request.__repr__)
            if _response.status_code == 201:
                # success
                flash("Prediction approved")
                return redirect(url_for('main.admin'))
            else:
                flash("Prediction not approved")
                return redirect(url_for('main.admin'))

    response = requests.get(pred_url, headers=headers)
    if response.status_code == 200:
        # success
        preds = response.json()  # -> a dictionary with list of dictionaries
        predictions = preds['predictions']
        #separate the predictions into sections: all - >predictions, staged -> ?, and approved-> approved
        approved = []
        staged = []
        fields = {}
        fields['odds'] = 1
        fields['comment'] = ''
        for pred in predictions:
            if pred['approved'] == 2:
                approved.append(pred)
                fields['odds'] *= pred['odds']
                fields['comment'] += str(pred['comment'])
            elif pred['approved'] == 1:
                staged.append(pred)
        return render_template('admin/admin.html', predictions=predictions, approved=approved, staged=staged,
                               form=form, fields=fields, filter_form=filter_form, filtered=filtered)
    if response.status_code == 401:
        # unauthorized attempt
        flash("Session expired please login again", 'info')
        return redirect(url_for('main.logout'))
    else:
        return redirect(url_for('main.logout'))

@main.route('/invalidate/<pred_id>')
def invalidate(pred_id):
    """:param the prediction id of the prediction instance to be invalidated
    the prediction moves from approved to staged"""
    pred_url = host_url + '''predictions/{}'''.format(pred_id)
    data = {
            "comment": "",
            "approved": 1
        }
    _response = requests.put(pred_url, data=json.dumps(data), headers=headers)
    if _response.status_code == 201:
        # succesful modification return to admin
        flash("Prediction unapproved", "success")
        return redirect(url_for('main.admin'))
    else:
        flash("Prediction still valid", 'danger')
        flash("{}".format(_response.status_code))
        return redirect(url_for('main.admin'))


@main.route('/stage/<pred_id>')
def stage(pred_id):
    """"""
    pred_url = host_url + '''predictions/{}'''.format(pred_id)
    data = {
            "comment": "",
            "approved": 1
        }
    _response = requests.put(pred_url, data=json.dumps(data), headers=headers)
    if _response.status_code == 201:
        # succesful modification return to admin
        flash("Prediction unapproved", "success")
        return redirect(url_for('main.admin'))
    else:
        flash("Prediction still valid", 'danger')
        flash("{}".format(_response.status_code))
        return redirect(url_for('main.admin'))


@main.route('/unstage/<pred_id>')
def unstage(pred_id):
    """"""
    pred_url = host_url + '''predictions/{}'''.format(pred_id)
    data = {
            "comment": "",
            "approved": 0
        }
    _response = requests.put(pred_url, data=json.dumps(data), headers=headers)
    if _response.status_code == 201:
        # succesful modification return to admin
        flash("Prediction unapproved", "success")
        return redirect(url_for('main.admin'))
    else:
        flash("Prediction still valid", 'danger')
        flash("{}".format(_response.status_code))
        return redirect(url_for('main.admin'))
    
def api_authenticate():
    """authenticates to the api and saves the token response to the session"""
    query_url = host_url + """users/login"""
    app = current_app._get_current_object()
    if app.config['CONFIGURATION'] != 'heroku':
        data = {
            'user_name': app.config['EANMBLE_ADMIN_USER_NAME'],
            'password': app.config['EANMBLE_ADMIN_PASSWORD']
        }
    else:
        data = {
            'user_name': os.environ.get('EANMBLE_ADMIN_USER_NAME'),
            'password': os.environ.get('EANMBLE_ADMIN_PASSWORD')
        }
    try:
        response = requests.post(login_endpoint, data=json.dumps(data), headers=headers)
        if response.status_code == 200:
            token = response.json()['token']
            session['token'] = token
    except ConnectionError:
        raise Exception("Problem connecting to Ghastly API")
    

@main.route("/users")
def user_predictions():
    """Renders the approved predictions"""
    filter_form = FilterForm()
    _from, _to = '', ''
    try:
        token = session['token']
    except KeyError as error:
        # if we do not have a token we re- authenticate to the api
        try:
            api_authenticate()
        except Exception as error:
            flash(error, 'danger')
            return redirect('auth.logout')
            
    headers['x-access-token'] = session['token']
    pred_url = host_url + '''predictions/'''
    payload = {
        '_from':datetime.datetime.today().strftime(%d-%m-%Y)
        '_to':datetime.datetime.today().strftime(%d-%m-%Y),
        'approved': 2
    }
    response = requests.get(pred_url, headers=headers, params=payload)
    today = datetime.date.today()
    past = today - datetime.timedelta(days=7)
    start_date = today.strftime('%d-%m-%Y')
    if filter_form.validate_on_submit() and filter_form.submit.data:
        _from = filter_form.first_date.data.strftime('%d-%m-%Y')
        _to = filter_form.second_date.data.strftime('%d-%m-%Y')
    else:
        _from = past.strftime('%Y-%m-%d')
        _to = today.strftime('%Y-%m-%d')
    query = {
            '_from': _from,
            '_to': _to
        }
    preds_url = host_url + '''predictions/'''
    _response = requests.get(preds_url, headers=headers, params=query)
    ##############################################################################################################
    if response.status_code == 200 and _response.status_code==200:
        # success
        preds = response.json()  # -> a dictionary with list of dictionaries
        past_predictions = _response.json()['predictions']
        predictions = preds['predictions']
        return render_template('user/user.html', predictions=predictions, filter_form=filter_form,
                               past_predictions= past_predictions, _from=_from, _to=_to)
    elif response.status_code == 401:
        # unauthorized attempt
        info = response.json()
        flash("Session expired please login again,. {}".format(info), 'info')
        return redirect(url_for('main.login'))
    else:
        flash("Problem logging in, {}".format(response.status_code), 'danger')
        return redirect(url_for('main.login'))



@main.route('/contact')
def contact():
    return render_template('contact.html')


@main.route('/confirm')
def confirm():
    """invokes call to email functions that send approved predictions to the users"""
    request_url = host_url + """/confirm"""
    try:
        token = session['token']
    except KeyError as error:
        return redirect('main.login')
    headers['x-access-token'] = session['token']
    response = requests.get(request_url, headers=headers)
    if response.status_code == 200:
        flash("Emails sent", 'success')
        return redirect('main.admin')
    else:
        flash("emails not sent", 'danger')
        return redirect('main.admin')

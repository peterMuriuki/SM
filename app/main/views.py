"""Route President"""
from flask import Flask, render_template, url_for, redirect, flash, session, request, Blueprint, current_app, abort
from .forms import ConfirmationForm, FilterForm, AdminFilterForm
import os
import json
import requests
from requests.exceptions import ConnectionError
import datetime
from .._globals import headers, host_url
from . import main


def set_header_token():
    try:
        headers['x-access-token'] = session['token']
    except KeyError as error:
        try:
            api_authenticate()
        except ConnectionError as e:
            flash(e, "danger")
            abort(500)
    headers['x-access-token'] = session['token']
    return


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

    set_header_token()

    pred_url = host_url + '''predictions/'''
    response = requests.get(pred_url, headers=headers, params=payload)
    if response.status_code == 200:
        return render_template('landing_page.html', past_predictions=response.json()['predictions'])
        # that returns a list of dictionaries with keys as datetime.strftime and values as list of predictions
    else:
        # return an error page
        abort(404)


def api_authenticate():
    """authenticates to the api and saves the token response to the session"""
    query_url = host_url + """users/login"""
    app = current_app._get_current_object()
    if os.environ.get('CONFIGURATION') != 'heroku':
        payload = {
            'user_name': app.config['EANMBLE_ADMIN_USER_NAME'],
            'password': app.config['EANMBLE_ADMIN_PASSWORD']
        }
    else:
        payload = {
            'user_name': os.environ.get('EANMBLE_ADMIN_USER_NAME'),
            'password': os.environ.get('EANMBLE_ADMIN_PASSWORD')
        }
    try:
        response = requests.post(query_url, data=json.dumps(payload))
        if response.status_code == 200:
            token = response.json()['token']
            session['token'] = token
        else:
            raise Exception(str(response.status_code) + str(response.json()))
    except ConnectionError:
        raise ConnectionError("Problem connecting to Ghastly API")


def parse_predictions(predictions):
    """:parameter: a list of predictions
    :returns a tuple consisting of approved, staged, comments of approved, and odds of approved"""
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
    return approved, staged, fields


@main.route('/admin', methods=['GET', 'POST'])
def admin():
    """display the admin's tips approval page"""
    #  here we connect to the api using authentication data provided and then
    #  receive the response and parse it on to the template
    form = ConfirmationForm()
    filter_form = AdminFilterForm()
    filtered = True

    set_header_token()

    pred_url = host_url + '''predictions/'''
    if filter_form.validate_on_submit() and filter_form.submit.data:
        """filter paramaters: """
        date_ = filter_form.date.data # this is a datetime class object
        date_filter = date_.strftime('%d-%m-%Y')
        payload = {'_from': date_filter,
                   '_to': date_filter
                   }
        _response = requests.get(pred_url, params=payload, headers=headers)

        if _response.status_code == 200:
            # success
            preds = _response.json()  # -> a dictionary with list of dictionaries
            predictions = preds['predictions'][payload['_from']]
            #separate the predictions into sections: all - >predictions, staged -> ?, and approved-> approved
            approved, staged, fields = parse_predictions(predictions)
            if date_ == datetime.date.today():
                filtered = False
            else:
                filtered = True
            return render_template('admin/admin.html', predictions=predictions, approved=approved, staged=staged,
                               form=form, fields=fields, filtered=filtered, filter_form=filter_form)
        else:
            flash("<h2>Problem with filtered data.</h2>", 'danger')
            abort(404)

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
            _pred_url = pred_url + "{}".format(q)
            _response = requests.put(_pred_url, data=json.dumps(data), headers=headers)
            if _response.status_code == 201:
                # success
                flash("Prediction approved")
                return redirect(url_for('main.admin'))
            else:
                flash("Prediction not approved")
                return redirect(url_for('main.admin'))

    date_ = datetime.datetime.today()
    date_filter = date_.strftime('%d-%m-%Y')
    payload = {
        '_from': date_filter,
        '_to': date_filter
        }
    response = requests.get(pred_url, headers=headers, params=payload)
    if response.status_code == 200:
        # success
        preds = response.json()  # -> a dictionary with list of dictionaries
        predictions = preds['predictions'][payload['_from']]
        #separate the predictions into sections: all - >predictions, staged -> ?, and approved-> approved
        approved, staged, fields = parse_predictions(predictions)
        return render_template('admin/admin.html', predictions=predictions, approved=approved, staged=staged,
                               form=form, fields=fields, filter_form=filter_form, filtered=filtered)
    if response.status_code == 401:
        # unauthorized attempt
        set_header_token()
        return redirect('main.admin')
    else:
        abort(404)


@main.route('/invalidate/<pred_id>')
def invalidate(pred_id):
    """:param the prediction id of the prediction instance to be invalidated
    the prediction moves from approved to staged"""
    pred_url = host_url + '''predictions/{}'''.format(pred_id)
    data = {
            "comment": "",
            "approved": 1
        }

    set_header_token()

    headers['token'] = session['token']
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

    set_header_token()

    headers['token'] = session['token']
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

    set_header_token()

    headers['token'] = session['token']
    _response = requests.put(pred_url, data=json.dumps(data), headers=headers)
    if _response.status_code == 201:
        # succesful modification return to admin
        flash("Prediction unapproved", "success")
        return redirect(url_for('main.admin'))
    else:
        flash("Prediction still valid", 'danger')
        flash("{}".format(_response.status_code))
        return redirect(url_for('main.admin'))


@main.route("/users")
def user_predictions():
    """Renders the approved predictions"""
    filter_form = FilterForm()
    _from, _to = '', ''

    set_header_token()

    headers['x-access-token'] = session['token']
    pred_url = host_url + '''predictions/'''
    payload = {
        '_from': datetime.datetime.today().strftime('%d-%m-%Y'),
        '_to': datetime.datetime.today().strftime('%d-%m-%Y'),
        'approved': 2
    }
    response = requests.get(pred_url, headers=headers, params=payload)
    today = datetime.date.today()
    past = today - datetime.timedelta(days=5)
    if filter_form.validate_on_submit() and filter_form.submit.data:
        _from = filter_form.first_date.data.strftime('%d-%m-%Y')
        _to = filter_form.second_date.data.strftime('%d-%m-%Y')
    else:
        _from = past.strftime('%Y-%m-%d')
        _to = today.strftime('%Y-%m-%d')
    query = {
            '_from': _from,
            '_to': _to,
            'approved': 2
        }
    preds_url = host_url + '''predictions/'''
    _response = requests.get(preds_url, headers=headers, params=query)
    if response.status_code == 200 and _response.status_code==200:
        # success
        preds = response.json()  # -> a dictionary with list of dictionaries
        past_predictions = _response.json()['predictions']
        predictions = preds['predictions'][payload['_from']]
        return render_template('user/user.html', predictions=predictions, filter_form=filter_form,
                               past_predictions= past_predictions, _from=_from, _to=_to)
    elif response.status_code == 401:
        # unauthorized attempt
        set_header_token()
        return redirect('main.user_predictions')
    else:
        abort(404)


@main.route('/contact')
def contact():
    return render_template('contact.html')


@main.route('/confirm')
def confirm():
    """invokes call to email functions that send approved predictions to the users"""
    pass

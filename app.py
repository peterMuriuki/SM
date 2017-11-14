from flask import Flask, render_template, url_for, redirect


app = Flask(__name__)
host_url = """https://ghastly-vault-37613.herokuapp.com/"""

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


app.route("/register")
def register():
    """Post new user data to the api"""

if __name__ == '__main__':
    app.run(debug=True)
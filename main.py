from flask import Flask, request, redirect
import cgi
import os
import jinja2

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape=True)


app = Flask(__name__)
app.config['DEBUG'] = True

@app.route("/")
def index():
    template = jinja_env.get_template('form.html')
    return template.render()

@app.route("/", methods=['POST'])
def validate_input():

    username=request.form['username']
    password=request.form['password']
    verify=request.form['verify']
    email=request.form['email']

    username_error = ''
    password_error = ''
    verify_error = ''
    email_error = ''

    if (len(username) < 3) or (" " in username):
        username_error = 'Not a valid username'
        username = ''

    if (len(password) < 3) or (" " in password):
        password_error = 'Not a valid password'
        password = ''

    if not password == verify:
        verify_error = 'Passwords do not match'
        verify = ''

    if len(email) > 0:
        if not ("@" in email) or not ("." in email):
            email_error = 'Not a valid email'
            email = ''

    if not username_error and not password_error and not verify_error and not email_error:
        username = username
        return redirect('/success?username={0}'.format(username))
    else:
        template = jinja_env.get_template('form.html')
        return template.render(username_error=username_error, password_error=password_error, verify_error=verify_error, email_error=email_error, username=username, password=password, verify=verify, email=email)

    


@app.route('/success')
def valid_username():
    username = request.args.get('username')
    return '<h1>Welcome, {0}.</h1>'.format(username)



app.run()
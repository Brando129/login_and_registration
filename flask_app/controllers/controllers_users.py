from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models import models_user
# Bcrypt import
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app) # We are creating an object called bcrypt,
# which is made by invoking the function Bcrypt with our app as an argument.

# Get Routes
# Route for rendering the "Dashboard Page"
@app.route('/')
def index():
    return render_template('dashboard.html')

# Route for checking if a user is in session.
@app.route('/dashboard')
def check_session():
    print('Checking if user is in session route...')
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id": session['user_id']
    }
    return render_template('dashboard.html', user=models_user.User.get_by_id(data))

# Route for logging a user out
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

# Post Routes
# Route for registering a user
@app.route('/register', methods=['POST'])
def register():
    print("Registering user route...")
    if not models_user.User.validate_user(request.form):
        # We redirect to the template with the form.
        return redirect('/')
    # Create data object for hashing a user's password.
    data = {
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "first_name": request.form['first_name'],
        "email": request.form['email'],
        "password": bcrypt.generate_password_hash(request.form['password']) # Function for generating the hash.
    }
    """We save the data to the database and are returned a user's id. We put
    this user id into session because when we go back to the dashboard we want
    to check if the user is in session and if they are not we redirect them.
    This is how we keep our applications safe."""
    id = models_user.User.save(data)
    session['user_id'] = id
    return redirect('/dashboard')

# Route for logging a user in.
@app.route('/login', methods=['POST'])
def login():
    print("Logging in")
    user = models_user.User.get_by_email(request.form)
    if not user:
        flash("Invalid email address.", "login")
        return redirect('/')
    if not bcrypt.check_password_hash(user.password, request.form['password']):
        flash("Invalid password.", "login")
        return redirect('/')
    session['user_id'] = user.id
    print("Log in successful.")
    return redirect('/dashboard')


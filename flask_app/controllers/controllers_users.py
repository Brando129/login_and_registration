from flask_app import app
from flask import render_template, redirect, request, session
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

# Post Routes
# Route for registering a user
@app.route('/register', methods=['POST'])
def register():
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

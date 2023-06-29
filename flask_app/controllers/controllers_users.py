from flask_app import app
from flask import render_template, redirect, request
from flask_app.models import models_user


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

    return redirect('/dashboard')
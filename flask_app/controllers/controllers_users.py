from flask_app import app
from flask import render_template, redirect, request


# Route for rendering the "Dashboard Page"
@app.route('/')
def index():
    return render_template('dashboard.html')
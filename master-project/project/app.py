from flask import Blueprint, render_template, request, Flask
from . import db
from flask_login import login_required, current_user

app = Flask(__name__)
@app.route('/')
def index():
    app.config['SHARED'].record_click()
    return render_template('index.html')
    
@app.route('/profile', methods=['POST', 'GET'])
@login_required
def profile():
    if request.method == 'POST':
        print(request.form['info3'])
    return render_template('profile.html', name=current_user.name) 
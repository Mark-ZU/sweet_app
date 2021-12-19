from flask import Blueprint
from . import db

auth = Blueprint('auth',__name__)

@auth.route('/')
def index():
    return "Index"

@auth.route('/signup')
def signup():
    return "Signups"

@auth.route('/logout')
def logout():
    return "Logout"
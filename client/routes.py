from flask import render_template, session
from flask_login import login_user, login_required, logout_user, current_user

from . import client_bp

@client_bp.route("/customer")
@login_required
def customer():
    return render_template("customer.html", username = session['username'])
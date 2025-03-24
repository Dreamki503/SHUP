from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user

from config import db

from . import login_bp
from auth.model import Users
from admin import admin_bp

@login_bp.route("/login",methods=['POST', 'GET'])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        user = Users.query.filter_by(email=email).first()

        if user and user.verify_password(password):
            login_user(user)
            flash('Logged in Successfull!!', 'success')

            if user.role == 'admin':
                return redirect(url_for("admin_bp.dashboard"))
            
            else:
                return redirect(url_for('customer'))
        
        else:
            flash("Invalid email or password", "danger")
        
    return render_template("login.html")

@login_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        username = request.form.get("username")

        if Users.query.filter_by(email=email, username=username).first():
            flash("Email already registered. Please log in.", "danger")
            return redirect(url_for("login_bp.register"))
        
        else:
            new_user = Users(email=email,username=username)
            new_user.password = password
            db.session.add(new_user)
            db.session.commit()

            flash("Registration successful! You can now log in.","success")
            return redirect(url_for("login_bp.login"))

    return render_template("login.html")

@login_bp.route("/logout")
def logout() :
    logout_user()
    flash("Successfully logged out!!", "success")
    return redirect(url_for('login_bp.login'))
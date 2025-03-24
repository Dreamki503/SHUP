from flask import redirect, render_template, request, url_for,flash
from config import db, app
from flask_login import login_required, current_user
import os
from werkzeug.utils import secure_filename

from auth.model import Users
from auth import login_bp
from . import admin_bp
from admin.model import category_category, store_product, orders_order
from config import UPLOAD_FOLDER

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@admin_bp.route("/admin")
@login_required
def dashboard():
    if not current_user.is_authenticated or current_user.role != 'admin':
        flash("Unauthorized access!", "danger")
        return redirect(url_for('login_bp.login'))
    
    else :
        users = Users.query.all()
        pending = orders_order.query.filter_by(status="new").count()
        approved = orders_order.query.filter_by(status="approved").count()
        completed = orders_order.query.filter_by(status="completed").count()
        return render_template("dashboard.html", users=users, pending = pending, approved = approved, completed = completed)
    
@admin_bp.route('/delete/<int:id>', methods = ['POST'])
def delete(id):
    user_to_delete = Users.query.get_or_404(id)
    try:
        db.session.delete(user_to_delete)
        db.session.commit()
        flash("Deleted successfully!!", "success")
    except:
        flash("whoops!")

    return redirect(url_for('admin_bp.user'))

@admin_bp.route('/update/<int:id>', methods=['POST', 'GET'])
def update(id):
    user_to_update = Users.query.get_or_404(id)

    if request.method == 'POST':
        # Get form data safely
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip()
        role = request.form.get('role', '').strip()
        phone = request.form.get('phone', '').strip()

        if not username or not email or not role:
            flash("All fields are required!", "danger")
            return render_template('update.html', user=user_to_update)

        try:
            user_to_update.username = username
            user_to_update.email = email
            user_to_update.role = role
            user_to_update.phone = phone

            db.session.commit()
            flash("User updated successfully!", "success")
            return redirect(url_for('admin_bp.user'))
        except Exception as e:
            db.session.rollback()  # Rollback in case of failure
            flash(f"An error occurred: {str(e)}", "danger")
            return render_template('update.html', user=user_to_update)

    return render_template('update.html', user=user_to_update)



@admin_bp.route("/add", methods=["POST","GET"])
@login_required
def add():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        username = request.form.get("username")
        role = request.form.get('role')
        phone = request.form.get('phone')

        if Users.query.filter_by(email=email, username=username).first():
            flash("Email already registered. Please log in.")
            return redirect(url_for("admin_bp.admin"))
        
        else:
            new_user = Users(email=email,username=username,phone = phone, role = role)
            new_user.password = password
            db.session.add(new_user)
            db.session.commit()

            flash("Registration successful!!")
            return redirect(url_for("admin_bp.user"))
        
    else:
        return render_template("add.html")

@admin_bp.route('/setting', methods=['POST', 'GET'])
@login_required
def setting():
    return render_template('setting.html')

def allowed_file(filename):
    """Check if the uploaded file has a valid extension."""
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

@admin_bp.route('/setting-update', methods = ['POST', 'GET'])
def setting_update():
    user_to_update = Users.query.get_or_404(current_user.id)
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        ph = request.form.get('ph')
        profile_pic = request.files.get('profile_pic')

        try:
            # Update text fields
            user_to_update.username = username
            user_to_update.email = email
            user_to_update.phone = ph

            # Handle profile picture upload
            if profile_pic and allowed_file(profile_pic.filename):
                filename = secure_filename(profile_pic.filename)
                file_path = os.path.join(UPLOAD_FOLDER, f"user_{current_user.id}_{filename}")
                profile_pic.save(file_path)

                # Store relative path in database (for easy access in templates)
                user_to_update.profile_pic = file_path.replace("static/", "")

            db.session.commit()
            flash("Profile updated successfully!!", "success")
            return redirect(url_for('admin_bp.setting'))

        except Exception as e:
            db.session.rollback()  # Rollback in case of error
            flash(f"An error occurred: {str(e)}", "danger")
            return render_template('setting.html', user=user_to_update)


@admin_bp.route('/users', methods=['POST', 'GET'])
@login_required
def user():
    search_query = request.args.get('search', '')

    if search_query:
        users = Users.query.filter(
            (Users.username.ilike(f"%{search_query}%")) |
            (Users.email.ilike(f"%{search_query}%")) |
            (Users.role.ilike(f"%{search_query}%"))
        ).all()
    else:
        users = Users.query.all()

    return render_template('user.html' , users = users)

@admin_bp.route('/pending', methods=['POST', 'GET'])
@login_required
def pending():
    search_query = request.args.get('search', '')

    if search_query:
        new_orders = orders_order.query.filter(
            (orders_order.first_name.ilike(f"%{search_query}%")) |
            (orders_order.email.ilike(f"%{search_query}%")) |
            (orders_order.order_number.ilike(f"%{search_query}%"))
        ).all()
    else:
        new_orders = orders_order.query.filter_by(status="new").all()

    return render_template('pending.html', pending = new_orders)

@admin_bp.route("/approve_order/<int:id>", methods = ["POST", 'GET'])
def approve_order(id):
    order = orders_order.query.get_or_404(id)
    if request.method == 'POST':
        order.status = "Approved"
        db.session.commit()
        flash("Order successfully approved!!", "success")
        return redirect(url_for('admin_bp.pending'))
    
    else:
        return render_template('pending.html')

@admin_bp.route('/approved', methods=['POST', 'GET'])
@login_required
def approved():
    search_query = request.args.get('search', '')

    if search_query:
        approved_orders = orders_order.query.filter(
            (orders_order.first_name.ilike(f"%{search_query}%")) |
            (orders_order.email.ilike(f"%{search_query}%")) |
            (orders_order.order_number.ilike(f"%{search_query}%"))
        ).all()
    else:
        approved_orders = orders_order.query.filter_by(status = 'approved').all()

    return render_template('approved.html', approved = approved_orders)

@admin_bp.route("/complete_order/<int:id>", methods = ["POST", 'GET'])
def complete_order(id):
    order = orders_order.query.get_or_404(id)
    if request.method == 'POST':
        order.status = "Completed"
        db.session.commit()
        flash("Order successfully completed!!", "success")
        return redirect(url_for('admin_bp.approved'))
    
    else:
        return render_template('approved.html')

@admin_bp.route('/completed', methods=['POST', 'GET'])
@login_required
def completed():
    search_query = request.args.get('search', '')

    if search_query:
        completed_orders = orders_order.query.filter(
            (orders_order.first_name.ilike(f"%{search_query}%")) |
            (orders_order.email.ilike(f"%{search_query}%")) |
            (orders_order.order_number.ilike(f"%{search_query}%"))
        ).all()
    else:
        completed_orders = orders_order.query.filter_by(status = 'completed').all()
    return render_template('completed.html', completed = completed_orders)

@admin_bp.route('/delete_order/<int:id>', methods = ['POST','GET'])
def delete_order(id):
    user_to_delete = Users.query.get_or_404(id)
    try:
        db.session.delete(user_to_delete)
        db.session.commit()
        flash("Deleted successfully!!", "success")
    except:
        flash("whoops!")

    return redirect(url_for('admin_bp.pending'))

@admin_bp.route('/category', methods=['POST', 'GET'])
@login_required
def category():
    categories = category_category.query.all()
    return render_template('category.html', categories = categories)

@admin_bp.route('/category_products/<int:category_id>')
def category_products(category_id):
    category = category_category.query.get_or_404(category_id)
    products = store_product.query.filter_by(category_id=category_id).all()
    return render_template('category_products.html', category=category, products=products)

@admin_bp.route('/add_category', methods=['POST', 'GET'])
def add_category():
    if request.method == "POST":
        category_name = request.form.get("category_name")
        slug = request.form.get("slug")

        if category_category.query.filter_by(category_name = category_name).first():
            # flash("Email already registered. Please log in.")
            return redirect(url_for("admin_bp.category"))
        
        else:
            new_category = category_category(category_name=category_name, slug=slug)
            db.session.add(new_category)
            db.session.commit()

            flash("Category added!")
            return redirect(url_for("admin_bp.category"))
        
    else:
        return render_template("add_category.html")

@admin_bp.route('/inventory', methods=['POST', 'GET'])
@login_required
def inventory():
    return render_template('inventory.html')
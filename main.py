from config import app, db, login_manager
from auth.model import Users

from home import home_bp
from auth import login_bp
from admin import admin_bp
from client import client_bp

login_manager.login_view = 'login_bp.login'
login_manager.login_message = 'Please Login to access this page'

app.register_blueprint(home_bp)
app.register_blueprint(login_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(client_bp)

@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()

    app.run(debug=True)
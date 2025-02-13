from flask import redirect, render_template, flash, Blueprint, request, url_for

from flask_login import login_required, logout_user, current_user, login_user

from flask import current_app as app 

from werkzeug.security import generate_password_hash 
from .assets import complite_auth_access
from .forms import LoginForm, SignupForm 
from .models import db, User 
from .import login_manager 

auth_bp= Blueprint('auth_bp', __name__, template_folder='templates', static_folder='static')

complite_auth_assets(app)

@auth_bp.route('/login', methods=['GET,'POST'])
def login_page():

    if current_user.is_authenticated:

        return redirect(url_for('main_bp.dashboard'))
    login_form=LoginForm(request.form)

    if request.method=='POST':
        if login_form.validate():

            email=request.form.get('email')
            password=request.form.get('password')

            user=User.query.filter_by(email=email).first()

            if user:
                if user.check_password(password=password):
                    login_user(user)
                    next=request.args.get('next')
                    return redirect(next or url_for('main_bp.dashboard'))
        flash('Invalid username/password entered')
        return redirect(url_for('auth_bp.login_page'))

    return render_template('login.html', 
                            form=LoginForm(),
                            title='Log in| Braven.',
                            template='login-page',
                            body="Login with your User account.")

@auth_bp.route('/signup',methods=['GET','POST'])

def signup_page():

    signup_form=SignupForm(request.form)

    if request.method =='POST':
        if signup_form.validate():

            name =request.form.get('name')
            email=request.form.get('email')
            password=request.form.get('password')
            website=request.form.get('website')
            existing_user=User.query.filter_by(email=email).first()
            if existing_user is None:
                user=User(name=name,email=email,password=generate_password_hash(password,method='sha256'),website=website)

                db.session.add(user)
                db.session.commit()
                login_user(user)
                return redirect(url_for('auth_bp.signup_page'))
    return render_template('/signup.html', title='Create an account | Braven.',form=SignupFOrm(),template='signup-page',body="Sign up for a user account.")


@auth_bp.route("/logout")
@login_required
def logout_page():
    """User log-out logic."""
    logout_user()
    return redirect(url_for('auth_bp.login_page'))


@login_manager.user_loader
def load_user(user_id):
    """Check if user is logged-in on every page load."""
    if user_id is not None:
        return User.query.get(user_id)
    return None


@login_manager.unauthorized_handler
def unauthorized():
    """Redirect unauthorized users to Login page."""
    flash('You must be logged in to view that page.')
    return redirect(url_for('auth_bp.login_page'))

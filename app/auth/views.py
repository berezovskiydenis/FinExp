from flask import flash, redirect, render_template, url_for
from flask_login import login_user, login_required, logout_user, current_user
from sqlalchemy.exc import IntegrityError
from datetime import datetime

from app import db
from app.auth import bp
from app.auth.forms import RegisterForm, SignInForm
from app.models import User


@bp.route('/signup', methods=['GET', 'POST'])
def sign_up():
    if current_user.is_authenticated:
        flash('Log out to create new account', 'warning')
        return redirect(url_for('main.index'))

    form = RegisterForm()

    if form.validate_on_submit():
        # Lookup for an existing user
        user_exist = User.query.filter_by(username=form.username.data).first()
        if user_exist:
            flash('This name is already registered', 'warning')
        else:
            user = User()
            user.username = form.username.data
            user.set_password(form.password.data)
            try:
                db.session.add(user)
                db.session.commit()
                flash('Registered successfully', 'success')
                return redirect(url_for('auth.sign_in'))
            except IntegrityError as e:
                flash('Some errors occured, try later', 'warning')
                db.session.rollback()
    return render_template('auth/signup.html', form=form)


@bp.route('/signin', methods=['GET', 'POST'])
def sign_in():
    if current_user.is_authenticated:
        set_visit(current_user)
        return redirect(url_for('main.index'))

    form = SignInForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()

        if user and user.check_password(form.password.data):
            # User login succesfully
            login_user(user, remember=form.remember_me.data)
            set_visit(user)
            return redirect(url_for('main.index'))

        flash("Invalid name or password")
    return render_template('auth/signin.html', form=form)


@bp.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.sign_in'))


# ----------------------------- Helper Functions ----------------------------
def set_visit(user):
    user.last_seen = datetime.utcnow()
    user.times_used = user.times_used + 1
    db.session.commit()

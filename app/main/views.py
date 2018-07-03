from flask import flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from sqlalchemy import asc
from sqlalchemy.exc import IntegrityError

from app import db
from app.main import bp
from app.models import Account, Transaction

from datetime import datetime


@bp.route('/', methods=['GET', 'POST'])
@login_required
def index():
    accounts = get_accounts()
    inc = get_income_statistics()
    return render_template('index.html', accounts=accounts, inc=inc)


# ----------------------------- HELPER FUNCTIONS -----------------------------

def get_accounts():
    accounts = db.session.query(Account).filter(
            Account.user_id == current_user.id,
            Account.is_active == True
        ).order_by(
            asc(Account.account)
        ).all()
    return accounts


def get_income_statistics():
    stat = db.session.query(Transaction).filter(
            Transaction.user_id == current_user.id,
            Transaction.minus == False,
            Transaction.tdate >= datetime.today().replace(day=1).date()
        ).all()

    current_month = sum(t.amount for t in stat)
    return current_month

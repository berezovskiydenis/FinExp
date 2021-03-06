from flask import flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from sqlalchemy import asc, func
from sqlalchemy.exc import IntegrityError

from app import db
from app.main import bp
from app.models import Account, Transaction, Category

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
    stat = db.session.query(
            Transaction.category_id,
            func.sum(Transaction.amount)
        ).filter(
            Transaction.user_id == current_user.id,
            Transaction.minus == False,
            Transaction.tdate >= datetime.today().replace(day=1).date()
        ).group_by(
            Transaction.category_id
        ).all()

    categories = db.session.query(Category).filter(
            Category.user_id == current_user.id
        ).all()

    categories_dict = {c.id: c.category for c in categories}

    result = [(categories_dict[x[0]], '{:,.2f}'.format(x[1])) for x in stat]

    return result

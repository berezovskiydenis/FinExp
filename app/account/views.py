from flask import render_template, redirect, url_for, flash, abort
from flask_login import current_user, login_required

from app import db
from app.account import bp
from app.models import Account, Currency

from app.account.forms import NewAccountForm, EditAccountForm


@bp.route('/accounts')
@login_required
def accounts():
    accounts = current_user.accounts.all()
    return render_template('account/accounts.html', accounts=accounts)


@bp.route('/account/', methods=['GET', 'POST'])
@login_required
def new_account():
    currency = Currency.query.all()
    form = NewAccountForm()
    form.currency.choices = [(c.id, c.currency) for c in currency]
    if form.validate_on_submit():
        new_account = Account(
            account=form.account.data.strip(),
            balance=round(float(form.balance.data), 2),
            currency_id=form.currency.data,
            user_id=current_user.id
        )
        db.session.add(new_account)
        db.session.commit()
        flash('Account created', 'success')
        return redirect(url_for('main.index'))
    return render_template('account/account.html', form=form)


@bp.route('/account/<int:account_id>', methods=['GET', 'POST'])
@login_required
def account(account_id):
    an_account = Account.query.filter_by(owner=current_user,
                                         id=account_id).first()
    if an_account is None:
        abort(404)

    form = EditAccountForm(obj=an_account)

    if form.validate_on_submit():
        form.populate_obj(an_account)
        db.session.commit()
        flash('Account has been changed', 'success')
        return redirect(url_for('account.accounts'))
    return render_template('account/account.html', form=form)

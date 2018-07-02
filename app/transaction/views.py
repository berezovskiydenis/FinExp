from flask import flash, redirect, render_template, url_for, abort
from flask_login import current_user, login_required
from sqlalchemy import asc, desc
from sqlalchemy.exc import IntegrityError
from datetime import date

from app import db
from app.models import Account, Category, Group, Party, Transaction, Transfer
from app.transaction import bp
from app.transaction.forms import TransactionForm, TransactionEditForm
from app.transaction.forms import TransferForm


@bp.route('/transaction/<tr_type>', methods=['GET', 'POST'])
@login_required
def transaction(tr_type):
    """Create new transaction."""

    if tr_type == 'minus':
        tr_type = True
    else:
        tr_type = False

    dbs = db.session

    form = TransactionForm()
    # form.tdate.data = date.today()
    form.account_id.choices = active_accounts(True)
    form.group_id.choices = active_groups(True)
    form.category_id.choices = active_categories(True)
    form.party_id.choices = active_parties(True)

    if form.validate_on_submit():
        tr = Transaction()
        tr.tdate = form.tdate.data
        tr.amount = round(float(form.amount.data), 2)
        tr.minus = tr_type
        tr.owner = current_user
        tr.account_id = form.account_id.data
        tr.group_id = form.group_id.data
        tr.category_id = form.category_id.data
        tr.party_id = form.party_id.data
        tr.comment = form.comment.data.strip()

        try:
            # Save transaction to databse
            dbs.add(tr)
            dbs.commit()
            # Increase time_used for account
            tr.account.times_used += 1

            # Increase times_used for group
            tr.group.times_used += 1

            # Increase times_used for category
            tr.category.times_used += 1

            # Increase times_used for party
            tr.party.times_used += 1

            # Subtract expense or add balance from balance
            if tr_type:
                # a.balance = a.balance - tr.amount
                tr.account.balance = tr.account.balance - tr.amount
            else:
                # a.balance = a.balance + tr.amount
                tr.account.balance = tr.account.balance + tr.amount

            dbs.commit()
            flash('Transaction created!', 'success')
            return redirect(url_for('main.index'))
        except IntegrityError:
            dbs.rollback()
            flash('Transaction was not created', 'warning')

    return render_template('transactions/transaction.html', form=form)


@bp.route('/transactions')
@login_required
def transactions():
    """Show all active transactions."""
    transactions = db.session.query(Transaction).filter(
            Transaction.user_id == current_user.id
        ).order_by(
            asc(Transaction.tdate)
        ).all()
    return render_template('transactions/transactions.html',
                           transactions=transactions)


@bp.route('/transaction/<int:tr_id>', methods=['GET', 'POST'])
@login_required
def transaction_edit(tr_id):
    # Get currenct transaction for current user
    t = db.session.query(Transaction).filter(
            Transaction.id == tr_id,
            Transaction.user_id == current_user.id
        ).first()

    # If no such transaction - error
    if t is None:
        abort(404)

    # Fill transaction data to the form
    form = TransactionEditForm(obj=t)

    # Now we need to fill choices for the fields in order
    # that user filled before
    # Account id
    account_choices = [(t.account_id, '{} ({})'.format(t.account.account,
                        t.account.currency.currency))]
    accounts = active_accounts(True)
    for a in accounts:
        if a[0] != t.account_id:
            account_choices.append(a)
    form.account_id.choices = account_choices

    # Group id
    group_choices = [(t.group_id, t.group.group)]
    groups = active_groups(True)
    for g in groups:
        if g[0] != t.group_id:
            group_choices.append(g)
    form.group_id.choices = group_choices

    # Category id
    categories = active_categories(True)
    category_choices = [(t.category_id, t.category.category)]
    for c in categories:
        if c[0] != t.category_id:
            category_choices.append(c)
    form.category_id.choices = category_choices

    # Party id
    party_choices = [(t.party_id, t.party.party)]
    parties = active_parties(True)
    for p in parties:
        if p[0] != t.party_id:
            party_choices.append(p)
    form.party_id.choices = party_choices

    # Temporarily store data for current transaction to correct balans after
    # edition
    amount_before = t.amount
    action_before = t.minus
    account_before = t.account_id
    group_before = t.group
    category_before = t.category
    party_before = t.party

    # Now check if form validation is ok
    if form.validate_on_submit():
        # Collect new data from form and put it to the transaction t
        try:
            form.populate_obj(t)
            db.session.commit()
            flash('Transaction changed', 'success')

            # Now we have to correct data related to current transaction
            # ... balance in Account
            amount_after = round(float(form.amount.data), 2)
            action_after = form.minus.data
            account_after = form.account_id.data

            # ... take account before and correct balans
            ac = Account.query.get(account_before)
            if action_before:
                ac.balance = ac.balance + amount_before
            else:
                ac.balance = ac.balance - amount_before
            ac.times_used -= 1
            db.session.add(ac)
            db.session.commit()

            # ... take account after and correct balans
            ac = Account.query.get(account_after)
            if action_after:
                ac.balance = ac.balance - amount_after
            else:
                ac.balance = ac.balance + amount_after
            ac.times_used += 1
            db.session.add(ac)
            db.session.commit()

            # Update usage statistics for groups categories and parties
            group_before.times_used -= 1
            category_before.times_used -= 1
            party_before.times_used -= 1
            db.session.add_all([group_before, category_before, party_before])

            group_after = form.group_id.data
            category_after = form.category_id.data
            party_after = form.party_id.data

            gai = Group.query.get(int(group_after))
            cai = Category.query.get(int(category_after))
            pai = Party.query.get(int(party_after))

            gai.times_used += 1
            cai.times_used += 1
            pai.times_used += 1

            db.session.add_all([gai, cai, pai])
            db.session.commit()

            return redirect(url_for('transaction.transactions'))
        except IntegrityError:
            db.session.rollback()
            flash('Transaction NOT changed', 'error')
    return render_template('transactions/transaction.html', form=form)


@bp.route('/transaction/delete/<int:tr_id>', methods=['GET'])
@login_required
def transaction_delete(tr_id):
    t = db.session.query(Transaction).filter(
            Transaction.id == tr_id,
            Transaction.user_id == current_user.id
        ).first()

    if t is None:
        abort(404)

    try:
        # Correct balans and statistics
        if t.minus:
            t.account.balance = t.account.balance + t.amount
        else:
            t.account.balance = t.account.balance - t.amount

        t.account.times_used -= 1
        t.group.times_used -= 1
        t.category.times_used -= 1
        t.party.times_used -= 1

        # Delete transaction
        db.session.delete(t)
        db.session.commit()
        flash('Transaction deleted', 'warning')
        return redirect(url_for('transaction.transactions'))
    except IntegrityError:
        db.session.rollback()
        flash('Transaction NOT deleted', 'error')


@bp.route('/transfer', methods=['GET', 'POST'])
@login_required
def transfer():
    form = TransferForm()

    # Prefill form fields
    form.tdate.data = date.today()
    form.from_account_id.choices = active_accounts(True)
    form.to_account_id.choices = active_accounts(True)

    if form.validate_on_submit():
        tf = Transfer(
                from_account_id=form.from_account_id.data,
                to_account_id=form.to_account_id.data,
                tdate=form.tdate.data,
                amount=round(float(form.amount.data), 2),
                coef=float(form.coef.data),
                user_id=current_user.id
            )
        f = Account.query.get(tf.from_account)
        t = Account.query.get(tf.to_account)

        f.balance = f.balance - tf.amount
        t.balance = t.balance + tf.amount * tf.coef

        db.session.add_all([tf, t, f])
        db.session.commit()
        flash('Transfer complete!', 'success')
        return redirect(url_for('main.index'))
    return render_template('transactions/transfer.html', form=form)


@bp.route('/transfers', methods=['GET'])
@login_required
def transfers():
    """Show all transfers"""
    transfers = db.session.query(Transfer).filter(
            Transfer.user_id == current_user.id
        ).order_by(
            desc(Transfer.tdate)
        ).all()
    return render_template('transactions/transfers.html',
                           transfers=transfers)


# ----------------------------- HELPER FUNCTIONS ----------------------------
def active_accounts(for_form=False):
    """Return list of active accounts for current user.
    If 'for_form' is True, then return list of tuples containing
    (account id, account name and currency)
    """
    accounts = db.session.query(Account).filter(
            Account.is_active == True,
            Account.user_id == current_user.id
        ).order_by(
            desc(Account.times_used)
        ).all()

    if for_form:
        as_tuples = []
        for a in accounts:
            as_tuples.append(
                    (a.id, '{} ({})'.format(
                            a.account,
                            a.currency.currency))
                )
        return as_tuples

    return accounts


def active_groups(for_form=False):
    """Return list of active groups.
    If 'for_form' is True, then return list of tuple of (group id, group name).
    """
    groups = db.session.query(Group).filter(
            Group.user_id == current_user.id,
            Group.is_active == True
        ).order_by(
            desc(Group.times_used)
        ).all()

    if for_form:
        as_tuples = []
        for g in groups:
            as_tuples.append((g.id, g.group))
        return as_tuples

    return groups


def active_categories(for_form=False):
    """Return list of active categories.
    If 'for_form' is True, then return list of tuples
    of (category id, category name).
    """
    categories = db.session.query(Category).filter(
            Category.user_id == current_user.id,
            Category.is_active == True
        ).order_by(
            desc(Category.times_used)
        ).all()

    if for_form:
        as_tuples = []
        for c in categories:
            as_tuples.append((c.id, c.category))
        return as_tuples

    return categories


def active_parties(for_form=False):
    """Return list of active parties.
    If 'for_form' is True, then return list of tuple of (party id, party name).
    """
    parties = db.session.query(Party).filter(
            Party.user_id == current_user.id,
            Party.is_active == True
        ).order_by(
            desc(Party.times_used)
        ).all()

    if for_form:
        as_tuples = []
        for p in parties:
            as_tuples.append((p.id, p.party))
        return as_tuples

    return parties

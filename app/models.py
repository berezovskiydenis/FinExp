from datetime import datetime

from app import db, login_manager
from flask_login import UserMixin
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.ext.hybrid import hybrid_property
from werkzeug.security import check_password_hash, generate_password_hash


class BaseFields(object):
    """The base class for 'ID' field to be inherited by subclasses."""
    @declared_attr
    def id(self):
        return db.Column(db.Integer(), primary_key=True)

    @declared_attr
    def created_at(self):
        return db.Column(db.DateTime(), nullable=False,
                         default=datetime.utcnow)

    def fancy_created(self):
        """Return date as string in format dd.mm.yyyy"""
        return datetime.strftime(self.created_at, '%d.%m.%Y')


class ExtraFields(object):
    """Extra fields for model."""
    @declared_attr
    def times_used(self):
        return db.Column(db.Integer(), default=0, nullable=False)

    @declared_attr
    def is_active(self):
        return db.Column(db.Boolean(), default=True, nullable=False)


class User(db.Model, BaseFields, ExtraFields, UserMixin):
    __tablename__ = 'users'
    # Every user identidied by mobile phone number
    phone = db.Column(db.String(20), index=True, nullable=False, unique=True)
    password_hash = db.Column(db.String(128), nullable=False)
    last_seen = db.Column(db.DateTime(), nullable=False,
                          default=datetime.utcnow)
    # References
    accounts = db.relationship('Account', backref='owner', lazy='dynamic',
                               cascade="save-update, merge, delete")
    categories = db.relationship('Category', backref='owner', lazy='dynamic',
                                 cascade="save-update, merge, delete")
    groups = db.relationship('Group', backref='owner', lazy='dynamic',
                             cascade="save-update, merge, delete")
    parties = db.relationship('Party', backref='owner', lazy='dynamic',
                              cascade="save-update, merge, delete")
    transactions = db.relationship('Transaction', backref='owner',
                                   lazy='dynamic',
                                   cascade="save-update, merge, delete")
    transfers = db.relationship('Transfer', backref='owner', lazy='dynamic',
                                cascade="save-update, merge, delete")

    def set_password(self, new_password):
        self.password_hash = generate_password_hash(new_password)

    def check_password(self, a_password):
        return check_password_hash(self.password_hash, a_password)


class Account(db.Model, BaseFields, ExtraFields):
    """Current account for user. User has zero to many accounts."""
    __tablename__ = 'accounts'
    account = db.Column(db.String(128), index=True, nullable=False)
    balance = db.Column(db.Float(), default=0.0, nullable=False)
    currency_id = db.Column(db.Integer(), db.ForeignKey('currency.id'),
                            nullable=False)
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id'),
                        nullable=False)
    # References
    transactions = db.relationship('Transaction', backref='account',
                                   lazy='dynamic')

    @hybrid_property
    def full_balance(self):
        return '{:,.2f} {}'.format(self.balance, self.currency.currency)

    @hybrid_property
    def full_account(self):
        return "{} ({})".format(self.account, self.currency.currency)


class Currency(db.Model, BaseFields):
    __tablename__ = 'currency'
    currency = db.Column(db.String(10), index=True, unique=True)
    # References
    accounts = db.relationship('Account', backref='currency', lazy='dynamic')

    @staticmethod
    def create():
        db.session.add_all([
                Currency(currency='EUR'),
                Currency(currency='USD'),
                Currency(currency='KZT')
            ])
        db.session.commit()


class Group(db.Model, BaseFields, ExtraFields):
    """Names of income and expenses. Used as general name."""
    __tablename__ = 'groups'
    group = db.Column(db.String(128), index=True, nullable=False)
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id'),
                        nullable=False)
    # References
    transactions = db.relationship('Transaction', backref='group',
                                   lazy='dynamic')


class Category(db.Model, BaseFields, ExtraFields):
    """Subname for income and expenses. Used as subname for groups."""
    __tablename__ = 'categories'
    category = db.Column(db.String(128), index=True, nullable=False)
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id'),
                        nullable=False)
    # References
    transactions = db.relationship('Transaction', backref='category',
                                   lazy='dynamic')


class Party(db.Model, BaseFields, ExtraFields):
    __tablename__ = 'parties'
    party = db.Column(db.String(128), index=True, nullable=False)
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id'),
                        nullable=False)
    # References
    transactions = db.relationship('Transaction', backref='party',
                                   lazy='dynamic')


class Transaction(db.Model, BaseFields):
    __tablename__ = 'transactions'
    tdate = db.Column(db.Date(), nullable=False)
    amount = db.Column(db.Float(), default=0.0, nullable=False)
    # If minus=True then it is expense
    minus = db.Column(db.Boolean(), default=True, nullable=False)
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id'),
                        nullable=False)
    account_id = db.Column(db.Integer(), db.ForeignKey('accounts.id'),
                           nullable=False)
    group_id = db.Column(db.Integer(), db.ForeignKey('groups.id'),
                         nullable=False)
    category_id = db.Column(db.Integer(), db.ForeignKey('categories.id'),
                            nullable=False)
    party_id = db.Column(db.Integer(), db.ForeignKey('parties.id'),
                         nullable=False)
    comment = db.Column(db.String(128))

    @hybrid_property
    def fancy_date(self):
        return datetime.strftime(self.tdate, '%d.%m.%Y')

    @hybrid_property
    def fancy_amount(self):
        return '{:,.2f}'.format(self.amount)


class Transfer(db.Model, BaseFields):
    __tablename__ = 'transfers'
    from_account_id = db.Column(db.Integer(), db.ForeignKey('accounts.id'),
                                nullable=False)
    to_account_id = db.Column(db.Integer(), db.ForeignKey('accounts.id'),
                              nullable=False)
    tdate = db.Column(db.Date(), nullable=False)
    amount = db.Column(db.Float(), default=0.0, nullable=False)
    coef = db.Column(db.Float(), default=1.0, nullable=False)
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id'),
                        nullable=False)
    # References
    from_account = db.relationship('Account', foreign_keys=[from_account_id])
    to_account = db.relationship('Account', foreign_keys=[to_account_id])

    @hybrid_property
    def fancy_date(self):
        return datetime.strftime(self.tdate, '%d.%m.%Y')

    @hybrid_property
    def fancy_amount(self):
        return '{:,.2f}'.format(self.amount)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

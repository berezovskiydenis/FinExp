from flask_wtf import FlaskForm
from wtforms import (DateTimeField, DecimalField, SelectField,
                     StringField, SubmitField, BooleanField)
from wtforms.validators import DataRequired, Length, NumberRange


class TransactionForm(FlaskForm):
    tdate = DateTimeField(
            label='Date',
            validators=[DataRequired()],
            format='%d.%m.%Y',
            id='datepicker',
            render_kw={'class': 'form-control'}
        )

    amount = DecimalField(
            label="Amount",
            validators=[NumberRange(min=0.0), DataRequired()],
            id='amountInput',
            render_kw={'type': 'number', 'step': '0.01',
                       'class': 'form-control'}
        )

    account_id = SelectField(
            label='Account',
            coerce=int,
            id='accountInput',
            render_kw={'class': 'form-control'}
        )

    group_id = SelectField(
            label='Group',
            coerce=int,
            id='groupInput',
            render_kw={'class': 'form-control'}
        )

    category_id = SelectField(
            label='Category',
            coerce=int,
            id='categoryInput',
            render_kw={'class': 'form-control'}
        )

    party_id = SelectField(
            label='Party',
            coerce=int,
            id='partyInput',
            render_kw={'class': 'form-control'}
        )

    comment = StringField(
            label='Comment',
            validators=[Length(max=128)],
            id='commentInput',
            render_kw={'placeholder': 'Comment', 'class': 'form-control'}
        )

    submit = SubmitField('Save', render_kw={'class': 'btn btn-primary'})


class TransactionEditForm(TransactionForm):
    minus = BooleanField('Expense')


class TransferForm(FlaskForm):
    from_account_id = SelectField(
            label='From account',
            coerce=int,
            id='accountFromInput',
            render_kw={'class': 'form-control'}
        )

    to_account_id = SelectField(
            label='To account',
            coerce=int,
            id='accountToInput',
            render_kw={'class': 'form-control'}
        )

    tdate = DateTimeField(
            label='Date',
            validators=[DataRequired()],
            format='%d.%m.%Y',
            id='datepicker',
            render_kw={'class': 'form-control'}
        )

    amount = DecimalField(
            label="Amount",
            validators=[NumberRange(min=0.0), DataRequired()],
            id='amountInput',
            render_kw={'type': 'number', 'step': '0.01',
                       'class': 'form-control'}
        )

    coef = DecimalField(
            label="Coefficient",
            validators=[NumberRange(min=0.0), DataRequired()],
            id='coefInput',
            render_kw={'type': 'number', 'step': '0.01',
                       'class': 'form-control'}
        )

    submit = SubmitField('Send', render_kw={'class': 'btn btn-primary'})

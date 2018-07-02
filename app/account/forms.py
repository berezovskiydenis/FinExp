from flask_wtf import FlaskForm
from wtforms import (BooleanField, DecimalField, SelectField, StringField,
                     SubmitField)
from wtforms.validators import Length, NumberRange


class AccountForm(FlaskForm):
    account = StringField(
            label='Account',
            validators=[Length(min=1, max=128)],
            render_kw={'placeholder': 'Account name', 'class': 'form-control'},
            id='InputAccountName'
        )
    submit = SubmitField(
            label='Save',
            render_kw={'class': 'btn btn-primary'}
        )


class NewAccountForm(AccountForm):
    balance = DecimalField(
            label='Balance',
            validators=[NumberRange(min=0.0)],
            id='inputBalance',
            render_kw={'class': 'form-control', 'type': 'number',
                       'step': '0.01'}
        )
    currency = SelectField(
            label='Currency',
            coerce=int,
            id='currencyInput',
            render_kw={'class': 'form-control'}
        )


class EditAccountForm(AccountForm):
    is_active = BooleanField(
            label='Active',
            false_values=('false', 'FALSE', 'n', '0'),
            id='isActiveInput'
        )

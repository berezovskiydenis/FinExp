import string

from flask_wtf import FlaskForm
from wtforms import BooleanField, PasswordField, StringField, SubmitField
from wtforms.validators import (DataRequired, EqualTo, Length, Regexp,
                                ValidationError)


def ascii_username(form, field):
    # Only ascii letters are allowed for username
    for i in field.data:
        if i not in string.ascii_letters:
            raise ValidationError(
                    'Only latin letters are allowed for name')


class AuthForm(FlaskForm):
    username = StringField(
            label="Name",
            validators=[DataRequired(), Length(min=1, max=128),
                        ascii_username],
            render_kw={'placeholder': 'Enter your name',
                       'class': 'form-control'},
            id="nameInput"
        )
    password = PasswordField(
            label='Password',
            validators=[DataRequired(), Length(min=3, max=128)],
            id='passwordInput',
            render_kw={'placeholder': 'Password', 'class': 'form-control'}
        )
    submit = SubmitField('Sign In', render_kw={'class': 'btn btn-primary'})


class SignInForm(AuthForm):
    remember_me = BooleanField(
        label='Remember me', false_values=('false', 'FALSE', '0')
    )


class RegisterForm(AuthForm):
    confirm = PasswordField(
            label='Confirm Password',
            validators=[EqualTo('password')],
            id="repeatPassword",
            render_kw={'placeholder': 'Repeat password',
                       'class': 'form-control'}
        )
    submit = SubmitField('Register', render_kw={'class': 'btn btn-primary'})


class EditUserForm(FlaskForm):
    username = StringField(
            label="Name",
            validators=[DataRequired(), Length(min=1, max=128),
                        ascii_username],
            render_kw={'placeholder': 'Enter your name',
                       'class': 'form-control'},
            id="nameInput"
        )
    phone = StringField(
            label="Mobile phone",
            validators=[DataRequired(), Regexp("[0-9]{11}")],
            render_kw={"placeholder": "Phone number", 'class': 'form-control'},
            id="phoneInput"
        )
    submit = SubmitField("Save", render_kw={'class': 'btn btn-primary'})

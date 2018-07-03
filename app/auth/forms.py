import string

from flask_wtf import FlaskForm
from wtforms import BooleanField, PasswordField, StringField, SubmitField
from wtforms.validators import (DataRequired, EqualTo, Length, Regexp,
                                ValidationError)


class AuthForm(FlaskForm):
    phone = StringField(
            label="Mobile phone",
            validators=[DataRequired(), Length(min=1, max=20),
                        Regexp("[0-9]{11}")],
            render_kw={'placeholder': 'Enter your phone',
                       'class': 'form-control'},
            id="phoneInput"
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
    phone = StringField(
            label="Mobile phone",
            validators=[DataRequired(), Length(min=1, max=20),
                        Regexp("[0-9]{11}")],
            render_kw={'placeholder': 'Enter your phone',
                       'class': 'form-control'},
            id="phoneInput"
        )
    submit = SubmitField("Save", render_kw={'class': 'btn btn-primary'})

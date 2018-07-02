from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length


# ---------------------------------- Group ----------------------------------
class GroupForm(FlaskForm):
    group = StringField(
            label='Group',
            validators=[DataRequired(), Length(max=128)],
            id='groupInput',
            render_kw={'class': 'form-control'}
        )
    submit = SubmitField(
            label='Save',
            render_kw={'class': 'btn btn-primary'}
        )


class GroupEditForm(GroupForm):
    is_active = BooleanField(
            label='Active',
            false_values=('False', 'FALSE', 'n', 'N', '0', 'no'),
            id='isActiveInput'
        )


# --------------------------------- Category ---------------------------------
class CategoryForm(FlaskForm):
    category = StringField(
            label='Category',
            validators=[DataRequired(), Length(max=128)],
            id='categoryInput',
            render_kw={'class': 'form-control'}
        )
    submit = SubmitField(
            label='Save',
            render_kw={'class': 'btn btn-primary'}
        )


class CategoryEditForm(FlaskForm):
    category = StringField(
            label='Category',
            validators=[DataRequired(), Length(max=128)],
            id='categoryInput',
            render_kw={'class': 'form-control'}
        )
    is_active = BooleanField(
            label='Active',
            false_values=('False', 'FALSE', 'n', 'N', '0', 'no'),
            id='isActiveInput'
        )
    submit = SubmitField('Save', render_kw={'class': 'btn btn-primary'})


# ---------------------------------- Party ----------------------------------
class PartyForm(FlaskForm):
    party = StringField(
            label='Party',
            validators=[DataRequired(), Length(max=128)],
            id='partyInput',
            render_kw={'class': 'form-control'}
        )
    submit = SubmitField('Save', render_kw={'class': 'btn btn-primary'})


class PartyEditForm(PartyForm):
    is_active = BooleanField(
            label='Active',
            false_values=('False', 'FALSE', 'n', 'N', '0', 'no'),
            id='isActiveInput'
        )

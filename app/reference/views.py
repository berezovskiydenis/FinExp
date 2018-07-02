from flask import render_template, redirect, url_for, abort, flash
from flask_login import current_user, login_required
from app import db
from app.reference import bp
from app.models import Group, Category, Party
from app.reference.forms import GroupForm, GroupEditForm
from app.reference.forms import CategoryForm, CategoryEditForm
from app.reference.forms import PartyForm, PartyEditForm
from sqlalchemy.exc import IntegrityError
from sqlalchemy import desc


# ---------------------------------- Group ----------------------------------
@bp.route('/group', methods=['GET', 'POST'])
@login_required
def group():
    form = GroupForm()
    if form.validate_on_submit():
        a_group = Group(group=form.group.data.strip(), owner=current_user)
        db.session.add(a_group)
        try:
            db.session.commit()
            flash('Group created', 'success')
            return redirect(url_for('main.index'))
        except IntegrityError:
            db.session.rollback()
            flash('Group NOT created', 'warning')
    return render_template('references/ref.html', form=form, title='Group')


@bp.route('/group/<int:group_id>', methods=['GET', 'POST'])
def group_edit(group_id):
    existing_group = Group.query.filter_by(
            owner=current_user,
            id=group_id
        ).first()
    if existing_group is None:
        abort(404)
    form = GroupEditForm(obj=existing_group)
    if form.validate_on_submit():
        form.populate_obj(existing_group)
        try:
            db.session.commit()
            flash('Group updated', 'success')
            return redirect(url_for('main.index'))
        except IntegrityError:
            db.session.rollback()
            flash('Group NOT updated')
    return render_template('references/ref.html', form=form, title='Group')


@bp.route('/groups')
@login_required
def groups():
    groups = db.session.query(Group).filter(
            Group.user_id == current_user.id
        ).order_by(
            desc(Group.times_used)
        )
    return render_template('references/groups.html', groups=groups)


# --------------------------------- Category --------------------------------
@bp.route('/category', methods=['GET', 'POST'])
@login_required
def category():
    form = CategoryForm()
    if form.validate_on_submit():
        category = Category(
                category=form.category.data.strip(),
                owner=current_user
            )
        try:
            db.session.add(category)
            db.session.commit()
            flash('Category created', 'success')
            return redirect(url_for('main.index'))
        except IntegrityError:
            db.session.rollback()
            flash('Category not created', 'warning')
    return render_template('references/ref.html', form=form, title='Category')


@bp.route('/category/<int:category_id>', methods=['GET', 'POST'])
def category_edit(category_id):
    existing_category = Category.query.filter_by(
            owner=current_user,
            id=category_id
        ).first()
    if existing_category is None:
        abort(404)
    form = CategoryEditForm(obj=existing_category)
    if form.validate_on_submit():
        form.populate_obj(existing_category)
        try:
            db.session.commit()
            flash('Category updated', 'success')
            return redirect(url_for('main.index'))
        except IntegrityError:
            db.session.rollback()
            flash('Category not updated', 'warning')
    return render_template('references/ref.html', form=form, title='Category')


@bp.route('/categories')
@login_required
def categories():
    categories = db.session.query(Category).filter(
            Category.user_id == current_user.id
        ).order_by(
            desc(Category.times_used)
        )
    return render_template('references/categories.html', categories=categories)


# ---------------------------------- Party ----------------------------------
@bp.route('/party', methods=['GET', 'POST'])
@login_required
def party():
    form = PartyForm()
    if form.validate_on_submit():
        party = Party(party=form.party.data.strip(), owner=current_user)
        try:
            db.session.add(party)
            db.session.commit()
            flash('Party created', 'success')
            return redirect(url_for('main.index'))
        except IntegrityError:
            db.session.rollback()
            flash('Party not created', 'warning')
    return render_template('references/ref.html', form=form, title='Party')


@bp.route('/party/<int:party_id>', methods=['GET', 'POST'])
def party_edit(party_id):
    existing_party = Party.query.filter_by(
            owner=current_user,
            id=party_id
        ).first()
    if existing_party is None:
        abort(404)
    form = PartyEditForm(obj=existing_party)
    if form.validate_on_submit():
        form.populate_obj(existing_party)
        try:
            db.session.commit()
            flash('Party updates', 'success')
            return redirect(url_for('main.index'))
        except IntegrityError:
            db.session.rollback()
            flash('Party not updates', 'warning')
    return render_template('references/ref.html', form=form, title='Party')


@bp.route('/parties')
@login_required
def parties():
    parties = db.session.query(Party).filter(
            Party.user_id == current_user.id
        ).order_by(
            desc(Party.times_used)
        )
    return render_template('references/parties.html', parties=parties)

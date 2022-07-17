from datetime import datetime
from flask import render_template, session, redirect, url_for
from flask_login import login_required
from . import main
from .forms import NameForm
from .. import db
from ..models import User, Permission
from ..decorators import admin_required, permission_required



@main.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        # ...
        return redirect(url_for('.index'))
    return render_template('index.html',
                        form=form, name=session.get('name'),
                        known=session.get('known', False),
                        current_time=datetime.utcnow())


@main.route('/admin')
@login_required
@admin_required
def for_admins_only():
    return "For administrators!"


@main.route('/moderator')
@login_required
@permission_required(Permission.MODERATE_COMMENTS)
def for_moderators_only():
    return "For comment moderators!"


@main.route('/user/<username>')
def user(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        abort(404)
    return render_template('user.html', user=user)


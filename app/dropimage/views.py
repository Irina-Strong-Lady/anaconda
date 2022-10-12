import os
from flask import Flask, render_template, request, redirect, url_for, abort, \
    send_from_directory, current_app
from werkzeug.utils import secure_filename
from .validate import create_folder, default_image
from . import dropimage
from flask_login import current_user, login_required
from .. import db
from ..models import User


@dropimage.route('/')
def avatars():
    files = os.listdir(create_folder())
    return render_template('avatar.html', files=files)


@dropimage.route('/avatars', methods=['POST'])
@login_required
def upload_avatars():
    if current_user.avatar in os.listdir(create_folder()):
        os.remove(os.path.join(create_folder(), current_user.avatar))
    uploaded_file = request.files['file']
    filename = uploaded_file.filename
    if filename != '':
        file_ext = os.path.splitext(filename)[1]
        if file_ext not in current_app.config['UPLOAD_EXTENSIONS']:
            return "Invalid image", 400
        filename = current_user.username + file_ext.upper()
        uploaded_file.save(os.path.join(create_folder(), filename))
        current_user.avatar = filename
        db.session.add(current_user._get_current_object())
        db.session.commit()
    return '', 204


@dropimage.route('/static/<path:filename>', methods=['GET'])
@login_required
def download_avatars(filename):
    return send_from_directory(create_folder(), filename)
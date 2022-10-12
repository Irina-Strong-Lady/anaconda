import os
import imghdr
from datetime import date
from flask import current_app


def validate_image(stream):
	header = stream.read(512)
	stream.seek(0)
	format = imghdr.what(None, header)
	if not format:
	    return None
	return '.' + (format if format != 'jpeg' else 'jpg')


def create_folder():	
	folder_path = current_app.config['UPLOAD_PATH'] + '/' + 'avatars'
	
	if not os.path.exists(folder_path):
		os.mkdir(folder_path)
	return folder_path


def default_image():
	default_files = os.listdir(current_app.config['UPLOAD_PATH'] + '/' + 'default')
	random_avatar = random.choice(default_files)
	return random_avatar
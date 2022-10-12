from flask import render_template, request, jsonify
from . import dropimage


@dropimage.errorhandler(413)
def too_large(e):
    return "File is too large", 413
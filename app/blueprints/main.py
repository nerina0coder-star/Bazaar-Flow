import datetime

from flask import Blueprint, render_template, abort, flash, redirect, url_for, request
from flask_login import login_required, current_user

from app import db

main_bp = Blueprint('main', __name__)

@main_bp.route('/ping')
@login_required
def ping():
    if request.headers.get('X-Fetch-Request') != 't':
        print("rejected request ping")
        return abort(404) # For security purposes and pervention of leak of data.
    current_user.last_seen = datetime.datetime.now(datetime.UTC)
    db.session.commit()
    return 'pong', 204

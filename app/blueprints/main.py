import datetime

from flask import Blueprint, render_template, abort, request, current_app
from flask_login import login_required, current_user

from app import db, limiter
from app.repositories.user_repository import UserRepository

main_bp = Blueprint('main', __name__)


@main_bp.before_request
def before_request():
    if request.path.startswith('/api/') or request.path.startswith('/chambers/'):
        origin = request.headers.get('Origin')
        if not origin or origin not in current_app.config.get('origin'):
            return abort(403)

@main_bp.route('/ping')
@login_required
@limiter.exempt
def ping():
    if request.headers.get('X-Fetch-Request') != 't':
        return abort(404) # For security purposes and pervention of leak of data.
    current_user.last_seen = datetime.datetime.now(datetime.UTC)
    db.session.commit()
    return 'pong', 204


@main_bp.route('/')
@limiter.limit('5000 per hour')
def home():
    if current_user.is_authenticated:
        if current_user.description == None:
            return render_template('home.html', user_matching_error=True)
        umatches = UserRepository.get_related(current_user)
        if not umatches:
            return render_template('home.html', no_matches=True)
        return render_template('home.html', umatches=umatches)
    return render_template('home.html')

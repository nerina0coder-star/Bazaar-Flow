import datetime

from flask import Blueprint, render_template, abort, request, send_from_directory, g
from flask_babel import get_locale
from flask_login import login_required, current_user

from app.extensions import db, limiter
from app.repositories.chamber_repository import ChamberRepository
from app.repositories.user_repository import UserRepository

main_bp = Blueprint('main', __name__)

@main_bp.route('/robots.txt')
def robots():
    return send_from_directory(main_bp.static_folder, 'robots.txt')

@main_bp.route('/ping')
@login_required
@limiter.exempt
def ping():
    if request.headers.get('X-Fetch-Request') != 't':
        return abort(403)
    current_user.last_seen = datetime.datetime.now(datetime.UTC)
    db.session.commit()
    return 'pong', 204


@main_bp.route('/')
@limiter.limit('5000 per hour')
def home():
    if current_user.is_authenticated:
        print("Locale is", get_locale())
        user_matching_error = False
        if current_user.description is None:
            user_matching_error = True
        umatches = []
        cmatches = []
        if not user_matching_error:
            umatches = UserRepository.get_related(current_user)
            cmatches = ChamberRepository.get_related(current_user)
        if not umatches:
            return render_template('home_loggedin.html', user_matching_error=user_matching_error, umatches=umatches, cmatches=cmatches)
        return render_template('home_loggedin.html', umatches=umatches, cmatches=cmatches)
    return render_template('home.html')

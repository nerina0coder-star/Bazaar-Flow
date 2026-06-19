from flask import Blueprint, render_template

from app import limiter

error_bp = Blueprint('errors', __name__)


@error_bp.app_errorhandler(404)
@limiter.exempt
def not_found(_error):
    return render_template("errors/error.html", type=404, message="صفحه موردنظر یافت نشد"), 404

@error_bp.app_errorhandler(403)
@limiter.exempt
def forbidden(_error):
    return render_template('errors/error.html', type=403, message='صفحه موردنظر برای شما ممنوع است'), 403

@error_bp.app_errorhandler(400)
@limiter.exempt
def bad_request(_error):
    return render_template('errors/error.html', type=400, message='اطلاعات ارسالی از طرف شما قابل قبول نیست')

@error_bp.app_errorhandler(408)
@limiter.exempt
def timeout(_error):
    return render_template('errors/error.html', type=408, message='نتوانستیم به سرور دسترسی پیدا کنیم')

@error_bp.app_errorhandler(413)
@limiter.exempt
def payload_too_large(_error):
    return render_template('errors/error.html', type=413, message='اطلاعات بیش از آن هستند که سرور بتواند تحمل کند')

@error_bp.app_errorhandler(429)
@limiter.exempt
def too_many_requests(_error):
    return render_template('errors/error.html', type=429, message='تعداد درخواست‌ها بیش از حد است')

@error_bp.app_errorhandler(401)
@limiter.exempt
def unauthorized(_error):
    return render_template('errors/error.html', type=401, message='احراز حویت نیاز است')

@error_bp.app_errorhandler(405)
@limiter.exempt
def method_not_allowed(_error):
    return render_template('errors/error.html', type=405, message='مشکلی در نحوه تبادل اطلاعات وجود داشت')

@error_bp.app_errorhandler(500)
@limiter.exempt
def internal_server_error(_error):
    return render_template('errors/error.html', type=500, message='مشکلی در سرور به وجود آمد')

@error_bp.app_errorhandler(501)
@limiter.exempt
def service_unavailable(_error):
    return render_template('errors/error.html', type=501, message='متد استفاده شده برای صفحه موردنظر قابل استفاده نیست')

@error_bp.app_errorhandler(502)
@limiter.exempt
def gateway_error(_error):
    return render_template('errors/error.html', type=502, message='سرور ما جواب غیرقابل قبولی ارسال کرد')
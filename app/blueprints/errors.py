from flask import Blueprint, render_template, request
from flask_login import login_required, current_user

error_bp = Blueprint('errors', __name__)


@error_bp.app_errorhandler(404)
def not_found(error):
    return render_template("errors/error.html", type=404, message="صفحه موردنظر یافت نشد"), 404

@error_bp.app_errorhandler(403)
def forbidden(error):
    return render_template('errors/error.html', type=403, message='صفحه موردنظر برای شما ممنوع است'), 403

@error_bp.app_errorhandler(400)
def bad_request(error):
    return render_template('errors/error.html', type=400, message='اطلاعات ارسالی از طرف شما قابل قبول نیست')

@error_bp.app_errorhandler(408)
def timeout(error):
    return render_template('errors/error.html', type=408, message='نتوانستیم به سرور دسترسی پیدا کنیم')

@error_bp.app_errorhandler(413)
def Payload_too_large(error):
    return render_template('errors/error.html', type=413, message='اطلاعات بیش از آن هستند که سرور بتواند تحمل کند')

@error_bp.app_errorhandler(429)
def too_many_requests(error):
    return render_template('errors/error.html', type=429, message='تعداد درخواست‌ها بیش از حد است')

@error_bp.app_errorhandler(401)
def unauthorized(error):
    return render_template('errors/error.html', type=401, message='احراز حویت نیاز است')

@error_bp.app_errorhandler(405)
def method_not_allowed(error):
    return render_template('errors/error.html', type=405, message='مشکلی در نحوه تبادل اطلاعات وجود داشت')

@error_bp.app_errorhandler(500)
def internal_server_error(error):
    return render_template('errors/error.html', type=500, message='مشکلی در سرور به وجود آمد')

@error_bp.app_errorhandler(501)
def service_unavailable(error):
    return render_template('errors/error.html', type=501, message='متد استفاده شده برای صفحه موردنظر قابل استفاده نیست')

@error_bp.app_errorhandler(502)
def gateway_error(error):
    return render_template('errors/error.html', type=502, message='سرور ما جواب غیرقابل قبولی ارسال کرد')
from flask import Blueprint, render_template

from flask_babel import gettext as _

error_bp = Blueprint('errors', __name__)


@error_bp.app_errorhandler(404)
def not_found(_error):
    return (render_template("errors/error.html", type=404,
                            message=_("صفحه موردنظر یافت نشد"))
                , 404
            )


@error_bp.app_errorhandler(403)
def forbidden(_error):
    return (render_template('errors/error.html', type=403,
                            message=_('صفحه موردنظر برای شما ممنوع است')),
            403
            )


@error_bp.app_errorhandler(400)
def bad_request(_error):
    return (render_template('errors/error.html', type=400,
                            message=_('اطلاعات ارسالی از طرف شما قابل قبول نیست')),
            400
            )


@error_bp.app_errorhandler(408)
def timeout(_error):
    return (render_template('errors/error.html', type=408,
                            message=_('نتوانستیم به سرور دسترسی پیدا کنیم')),
            408
            )


@error_bp.app_errorhandler(413)
def payload_too_large(_error):
    return (render_template('errors/error.html', type=413,
                            message=_('اطلاعات بیش از آن هستند که سرور بتواند تحمل کند')),
            413
            )


@error_bp.app_errorhandler(429)
def too_many_requests(_error):
    return (render_template('errors/error.html', type=429,
                            message=_('تعداد درخواست‌ها بیش از حد است')),
            429
            )


@error_bp.app_errorhandler(401)
def unauthorized(_error):
    return (render_template('errors/error.html', type=401,
                            message=_('احراز هویت نیاز است')),
            401
            )


@error_bp.app_errorhandler(405)
def method_not_allowed(_error):
    return (render_template('errors/error.html', type=405,
                            message=_('مشکلی در نحوه تبادل اطلاعات وجود داشت')),
            405
            )


@error_bp.app_errorhandler(500)
def internal_server_error(_error):
    return (render_template('errors/error.html', type=500,
                            message=_('مشکلی در سرور به وجود آمد')),
            500
            )


@error_bp.app_errorhandler(501)
def service_unavailable(_error):
    return (render_template('errors/error.html', type=501,
                            message=_('متد استفاده شده برای صفحه موردنظر قابل استفاده نیست')),
            501
            )


@error_bp.app_errorhandler(502)
def gateway_error(_error):
    return (render_template('errors/error.html', type=502,
                            message=_('سرور ما جواب غیرقابل قبولی ارسال کرد')),
            502
            )

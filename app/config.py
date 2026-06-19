import dotenv, redis

class Config:
    SECRET_KEY = dotenv.get_key(key_to_get='SECRET_KEY', dotenv_path='.env')
    HCAPTCHA_SITE_KEY = dotenv.get_key(key_to_get='HCAPTCHA_SITE', dotenv_path='.env')
    HCAPTCHA_SECRET_KEY = dotenv.get_key(key_to_get='HCAPTCHA_SECRET', dotenv_path='.env')
    
    SESSION_TYPE = 'redis'
    SESSION_REDIS = redis.from_url('redis://localhost:6379')
    SESSION_PERMANENT = False
    SESSION_COOKIE_SAMESITE = "Lax"
    SESSION_COOKIE_HTTPONLY = True

    MAX_CONTENT_LENGTH = 10 * 1024 * 1024
    CONTENT_SECURITY_POLICY = {
        'default-src' : "'self'",
        'style-src' : ["'self'", "'unsafe-inline'"],
        'img-src' : ["'self'", "data:"]
    }
 
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    CORS_ORIGINS = [dotenv.get_key(key_to_get='ORIGIN', dotenv_path='.env')]

    origin = dotenv.get_key(key_to_get='ORIGIN', dotenv_path='.env')
    use_captcha = False


class DevelopmentConfig(Config):
    DEBUG = True

    SESSION_COOKIE_SECURE = False


    TALISMAN_SESSION_COOKIE_SECURE = False
    TALISMAN_FORCE_HTTPS = False
    TALISMAN_STRICT_TRANSPORT_SECURITY = False
    SQLALCHEMY_DATABASE_URI = dotenv.get_key(key_to_get='DB_DEVELOPMENT_URI', dotenv_path='.env')

class ProductionConfig(Config):

    SESSION_COOKIE_SECURE = True

    TALISMAN_SESSION_COOKIE_SECURE = True
    TALISMAN_FORCE_HTTPS = True
    TALISMAN_STRICT_TRANSPORT_SECURITY = True
    DEBUG = False
    TALISMAN_STRICT = True
    SQLALCHEMY_DATABASE_URI = (f"postgresql://"
                               f"{dotenv.get_key(key_to_get='DB_USER', dotenv_path='.env')}:"
                               f"{dotenv.get_key(key_to_get='DB_PASS', dotenv_path='.env')}@"
                               f"{dotenv.get_key(key_to_get='DB_HOST', dotenv_path='.env')}:"
                               f"{dotenv.get_key(key_to_get='DB_PORT', dotenv_path='.env')}/"
                               f"{dotenv.get_key(key_to_get='DB_NAME', dotenv_path='.env')}")


config = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,


    "default": DevelopmentConfig
}

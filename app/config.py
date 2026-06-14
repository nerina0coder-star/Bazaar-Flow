import dotenv, redis

class Config:
    SECRET_KEY = dotenv.get_key(key_to_get='SECRET_KEY', dotenv_path='.env')
    HCAPTCHA_SITE_KEY = dotenv.get_key(key_to_get='HCAPTCHA_SITE', dotenv_path='.env')
    HCAPTCHA_SECRET_KEY = dotenv.get_key(key_to_get='HCAPTCHA_SECRET', dotenv_path='.env')
    SESSION_TYPE = 'redis'
    SESSION_REDIS = redis.from_url('redis://localhost:6379')
    SESSION_PERMANENT = False


    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(Config):
    DEBUG = True

    SQLALCHEMY_DATABASE_URI = dotenv.get_key(key_to_get='DB_DEVELOPMENT_URI', dotenv_path='.env')

class ProductionConfig(Config):
    DEBUG = False
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

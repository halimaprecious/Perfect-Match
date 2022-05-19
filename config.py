import os
class Config():

    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://vonetta:von123@localhost/perfect'

    SECRET_KEY = 'SECRET_KEY'

class DevConfig(Config):
    DEBUG= True
    
class ProdConfig(Config):
    pass

class TestConfig(Config):
    pass

config_options = {
    'development': DevConfig,
    'production': ProdConfig,
    'test': TestConfig
    
}  
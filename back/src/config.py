class TestingConfig:
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'  # BD en memoria para tests
    SQLALCHEMY_TRACK_MODIFICATIONS = False






class DevelopmentConfig:
    TESTING = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'  # BD en memoria para tests
    SQLALCHEMY_TRACK_MODIFICATIONS = False
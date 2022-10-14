import os
SECRET_KEY = "lp |i(.'F<sfuEbCVx\n3,RDt"

# Database initialization
if os.environ.get('DATABASE_URL') is None:
    basedir = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'database.db')
else:
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    # MYSQLHOST = "containers-us-west-143.railway.app"
    # MYSQLPORT = "6012"
    # MYSQLUSER = "root"
    # MYSQLPASSWORD = "iXoMTNqprheqbqfvBSWa"
    # MYSQLDATABASE = "railway"
    # MYSQL_URL = "mysql://root:iXoMTNqprheqbqfvBSWa@containers-us-west-143.railway.app:6012/railway"
    HOST = "containers-us-west-45.railway.app"
    DATABASE = "railway"
    USERNAME = "root"
    PASSWORD = "Ypjio39MCrIeKSvnE3nN"
    PORT = "7712"
    JWT_SECRET_KEY = str(os.environ.get("JWT_SECRET"))
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://'+USERNAME+':'+PASSWORD+'@'+HOST+':'+PORT+'/'+DATABASE
    # SQLALCHEMY_DATABASE_URI = 'postgresql://keyhjbritoyqcj:804aadb24179eb9cbee788f80dea8929dd5d41030c271942fefb01f488d35ec4@ec2-35-173-83-57.compute-1.amazonaws.com:5432/dek1mr5jkf2kj9'

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_RECORD_QUERIES = True

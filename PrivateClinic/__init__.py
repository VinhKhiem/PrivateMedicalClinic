from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from urllib.parse import quote

app = Flask(__name__)
app.secret_key="sacfasfgwgwgwgwgwegehehehehru5hrt"
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:%s@localhost/privateclinicdb?charset=utf8mb4" % quote(
    "Admin@123")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
db = SQLAlchemy(app=app)
admin= Admin(app=app, name='ADMIN', template_mode='bootstrap4')

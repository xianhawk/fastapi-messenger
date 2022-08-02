from flask import Flask
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_sqlalchemy import SQLAlchemy

from models import User, Message, Contact
from database import SessionLocal

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URL'] = "sqlite:///../db/messenger.db"
# app.config['SQLALCHEMY_DATABASE_URL'] = "sqlite:///:memory:"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['FLASK_ADMIN_SWATCH'] = 'flatly'
app.config['SECRET_KEY'] = 'secret'

db = SQLAlchemy(app)
        
admin = Admin(app, name='Messenger', template_mode='bootstrap3')
admin.add_view(ModelView(User, SessionLocal()))
admin.add_view(ModelView(Message, SessionLocal()))
admin.add_view(ModelView(Contact, SessionLocal()))

if __name__ == "__main__":
    app.run(debug=True)
    
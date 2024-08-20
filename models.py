from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from datetime import  date
import enum
from flask_login import UserMixin
from sqlalchemy.orm import relationship
import enum

# database = SQLAlchemy(app)
from . import database


class UserStatusEnum(enum.Enum):
    client = 'client'
    admin = 'admin'

class User(UserMixin,database.Model):
    id = database.Column(database.Integer, primary_key=True )
    first_name = database.Column(database.String(100), nullable=False)
    last_name = database.Column(database.String(100), nullable=False)
    email = database.Column( database.String(80),unique=True, nullable=False)
    phone = database.Column( database.String(15),unique=True, nullable=False)
    password = database.Column(database.String(8))
    role = database.Column(
        database.Enum(UserStatusEnum), 
        default=UserStatusEnum.client,
        nullable=False
    )
    def __repr__(self):
        return f'<User {self.first_name}>'
 
class Service(database.Model):
    id = database.Column(database.Integer, primary_key=True,autoincrement=True)
    name = database.Column(database.String(100), nullable=False)
    description = database.Column(database.Text, nullable=True)
    updated = database.Column(database.Date,default = date.today())
    author = database.Column(database.Integer, database.ForeignKey(User.id) ) 
    publisher = relationship('User', backref='publisher_service')
     
    def __repr__(self):
        return f'<Service {self.name}>'

class ServiceRequestForm(database.Model):
    id = database.Column(database.Integer, primary_key=True,autoincrement=True)
    service_id  = database.Column(database.Integer, database.ForeignKey('service.id'))
    reason = database.Column(database.String(100), nullable=False)
    updated = database.Column(database.Date,default = date.today())
    client = database.Column(database.Integer, database.ForeignKey(User.id) ) 
    active = database.Column(database.Boolean, default=False)
    nrc_number = database.Column('nrc_number', database.String(15), unique=True, nullable=True)
    district = database.Column('district', database.String(200), nullable=False) 
    pdf_file  = database.Column(database.LargeBinary)
    file_name = database.Column(database.String(255), nullable=True)  
    service = relationship('Service', backref='service_requests')
    user = relationship('User', backref='user_requests')
     
    def __repr__(self):
        return f'<ServiceRequestForm {self.id}>'
    
    def get_status(self):
        return self.active

    def get_status_text(self):
        if self.active:
            return 'Approved'
        return 'Not Approved'
from datetime import datetime
from RetailBank import db,login_manager
from flask_login import UserMixin
from sqlalchemy import Table,ForeignKey

@login_manager.user_loader
def load_user(user_id):
    return userstore.query.get(int(user_id))

class userstore(db.Model,UserMixin):
	id=db.Column(db.Integer,primary_key=True)
	login=db.Column(db.String(20),unique=True,nullable=False)
	password=db.Column(db.String(60),nullable=False)
	date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

	def __repr__(self):
		return f"userstore('{self.login}','{self.password}','{self.date_posted}')"

class Customer(db.Model):
	__tablename__ = 'customer'
	ssd_id=db.Column(db.Integer,primary_key=True)
	customer_name=db.Column(db.String(60),nullable=False)
	customer_age=db.Column(db.Integer,nullable=False)
	customer_address=db.Column(db.String(100),nullable=False)
	customer_state=db.Column(db.String(20),nullable=False)
	customer_city=db.Column(db.String(20),nullable=False)

	def __repr__(self):
		return f"Customer('{self.ssd_id}','{self.customer_name}','{self.customer_age}','{self.customer_address}','{self.customer_state}','{self.customer_city}')"

class Account(db.Model):
	account_no = db.Column(db.String(22),primary_key=True)
	ssd_id = db.Column(db.Integer,ForeignKey('customer.ssd_id')) 
	account_type = db.Column(db.String(10),nullable=False)
	deposit_amount = db.Column(db.Integer,nullable=False)

	def __repr__(self):
		return f"Account('{self.account_no}','{self.ssd_id}','{self.account_type}','{self.deposit_amount}'"
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField,IntegerField,DecimalField,SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from RetailBank.models import userstore,Customer,Account

class Loginform(FlaskForm):
	login = StringField('Login',validators=[DataRequired(),Length(min=2, max=20)])
	password = PasswordField('Password', validators=[DataRequired()])
	submit = SubmitField('Login')

class NewCustomerForm(FlaskForm):
	ssd_id=IntegerField('Customer SSD Id',validators=[DataRequired()])
	customer_name=StringField('Customer Name',validators=[DataRequired()])
	customer_age=IntegerField('Customer Age', validators=[DataRequired()])
	customer_address=StringField('Customer Address',validators=[DataRequired()])
	customer_state=StringField('Customer State',validators=[DataRequired()])
	customer_city=StringField('Customer City',validators=[DataRequired()])
	submit = SubmitField('Create')

class DeleteCustomerForm(FlaskForm):
	cus_id=IntegerField('Delete Customer Account',validators=[DataRequired()])
	submit = SubmitField('Delete')

class AccountForm(FlaskForm):
	account_no = StringField('Account No')
	ssd_id = IntegerField('SSN No',validators=[DataRequired()])
	account_type = SelectField(u'Account Type',choices=[('Current','Current'),('Saving','Saving')],validators=[DataRequired()])
	deposit_amount = IntegerField('Deposit Amount',validators=[DataRequired()])
	submit = SubmitField('Create Account')
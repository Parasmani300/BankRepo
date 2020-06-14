from flask import render_template, url_for, flash, redirect,request
from RetailBank.models import userstore,Customer
from RetailBank import app,db,bcrypt
from RetailBank.forms import Loginform,NewCustomerForm,DeleteCustomerForm

from flask_login import login_user,current_user,logout_user,login_required


@app.route('/home',methods=['GET', 'POST'])
def home():
	return render_template('home.html',title='Home')

@app.route('/index',methods=['GET','POST'])
@login_required
def index():
	return render_template('home.html')

@app.route('/',methods=['GET', 'POST'])
@app.route('/login',methods=['GET', 'POST'])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('index'))
	form=Loginform()
	if form.validate_on_submit():
		user=userstore.query.filter_by(login=form.login.data).first()
		if user and bcrypt.check_password_hash(user.password,form.password.data):
			login_user(user)
			next_page = request.args.get('next')
			flash('Login Successful', 'success')
			return redirect(next_page) if next_page else redirect(url_for('login'))
            #return"<h1>Login Successful</h1>"
		else:
			flash('Login Unsuccessful. Please check username and password', 'danger')
			#flash('Login Unsuccessful. Please check username and password', 'danger')
	return render_template('login.html',title='Login',form=form)

@app.route('/create_customer',methods=['GET','POST'])
@login_required
def create_customer():
	form = NewCustomerForm()
	if form.validate_on_submit():
		print(form.ssd_id.data,form.customer_name.data,form.customer_age.data,form.customer_address.data,form.customer_state.data,form.customer_city.data)
		cust = Customer(ssd_id=form.ssd_id.data,customer_name=form.customer_name.data,customer_age=form.customer_age.data,
			customer_address=form.customer_address.data,
			customer_state=form.customer_state.data,customer_city=form.customer_city.data)
		db.session.add(cust)
		db.session.commit()
		flash(f'Account created for {form.customer_name.data}!', 'success')
		return redirect(url_for('index'))
	return render_template('create_customer.html',title='New Customer',form=form)

@app.route('/delete',methods=['GET','POST'])
@login_required
def delete():
	form = DeleteCustomerForm()
	if form.validate_on_submit():
		ssd_id_1 = form.cus_id.data
		cust = Customer.query.filter_by(ssd_id=ssd_id_1).first()
		cust_name=cust.customer_name
		db.session.delete(cust)
		db.session.commit()
		flash(f'Account delete for {cust_name}!', 'success')

	return render_template('delete_customers.html',title='Delete',form=form)

@app.route('/customer_info',methods=['GET','POST'])
@login_required
def customer_info():
	info = Customer.query.all()
	return render_template('customers.html',info=info)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('login'))
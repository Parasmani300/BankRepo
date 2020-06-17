from flask import render_template, url_for, flash, redirect,request
from RetailBank.models import userstore,Customer,Account
from RetailBank import app,db,bcrypt
from RetailBank.forms import Loginform,NewCustomerForm,DeleteCustomerForm,AccountForm,DeleteAccountForm

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

@app.route('/update_customer',methods=['GET','POST'])
@login_required
def update_customer():
	if request.method == "POST":
		cust_ssn_id = request.form.get('customer_ssnid')
		customer_id = request.form.get('customer_id')
		cust = Customer.query.filter_by(ssd_id=cust_ssn_id).first()
		if cust:
			return redirect(url_for('finish_update',ssnid=cust.ssd_id))
	return render_template('update_customer.html')

@app.route('/finish_update',methods=['GET','POST'])
@login_required
def finish_update():
	ssn_id = request.args['ssnid']
	cust = Customer.query.filter_by(ssd_id=ssn_id).first()
	if request.method == "POST":
		new_name = request.form.get('new_customer_name')
		new_address = request.form.get('new_address')
		new_age = request.form.get('new_age')
		if new_name != "":
			cust.customer_name = new_name
		if new_address != "":
			cust.customer_address = new_address
		if new_age != "": 
			cust.customer_age = new_age
		db.session.commit()
		return redirect(url_for('update_customer'))
	return render_template('finish_update.html',cust=cust)

@app.route('/create_account',methods=['GET','POST'])
@login_required
def create_account():
	form = AccountForm()
	if form.validate_on_submit():
		ssn_no = form.ssd_id.data
		cust = Customer.query.filter_by(ssd_id=ssn_no).first()
		if cust:
			account_type = form.account_type.data
			deposit_amount = form.deposit_amount.data
			cust_count = Customer.query.filter_by(ssd_id=ssn_no).count()
			account_no = "FEDBNK"+str(ssn_no) + str(account_type) + str(cust_count + 10)
			db.create_all()
			account = Account(account_no=account_no,ssd_id=ssn_no,account_type=account_type,deposit_amount=deposit_amount)
			db.session.add(account)
			db.session.commit()
			flash(f'Account Created Successfully','success')
		else:
			flash(f'Check if ssn id exists for customer','danger')
	return render_template('create_account.html',form = form)

@app.route('/delete_account',methods=['GET','POST'])
@login_required
def delete_account():
	form = DeleteAccountForm()
	if form.validate_on_submit():
		ssn_no = form.ssd_id.data
		account_no = form.account_no.data
		acc = Account.query.filter_by(ssd_id=ssn_no,account_no=account_no).first()
		if acc:
			Account.query.filter_by(ssd_id=ssn_no,account_no=account_no).delete()
			db.session.commit()
			flash('Account deleted Successfully','danger')
			return redirect('/')
	return render_template('deleteAccount.html',form=form)

@app.route('/account_status',methods=['GET','POST'])
@login_required
def account_status():
	accounts = Account.query.all()
	return render_template('accountStatus.html',accounts=accounts)

@app.route('/customer_status',methods=['GET','POST'])
@login_required
def customer_status():
	customers = Customer.query.all()
	return render_template('customerStatus.html',customers=customers)

@app.route('/deposit_money',methods=['GET','POST'])
@login_required
def deposit_money():
	if request.form.get('account_no'):
		account_no = request.form.get('account_no')
		acc = Account.query.filter_by(account_no=account_no).first()
		if acc:
			ssn_no = acc.ssd_id
			account_type = acc.account_type
			balance = acc.deposit_amount
			return redirect(url_for('finish_transfer',account_no=account_no))
	return render_template('search_customer.html')

@app.route('/finish_transfer',methods=['GET','POST'])
@login_required
def finish_transfer():
	account_no = request.args.get('account_no')
	acc = Account.query.filter_by(account_no=account_no).first()
	ssn_no = acc.ssd_id
	account_type = acc.account_type
	balance = acc.deposit_amount
	account_type = acc.account_type
	if request.form.get('deposit_amount'):
		deposit_amount = int(request.form.get('deposit_amount'))
		acc.deposit_amount = acc.deposit_amount + deposit_amount
		try:
			db.session.commit()
			flash("Amount deposited successfully",'success')
		except:
			flash('Some error occured, Please try again!','danger')
	return render_template('deposit_money.html',account_no=account_no,ssn_no=ssn_no,account_type=account_type,balance=balance)

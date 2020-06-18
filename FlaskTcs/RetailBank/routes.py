from flask import render_template, url_for, flash, redirect,request
from RetailBank.models import userstore,Customer,Account,Transactions
from RetailBank import app,db,bcrypt
from RetailBank.forms import Loginform,NewCustomerForm,DeleteCustomerForm,AccountForm,DeleteAccountForm

from flask_login import login_user,current_user,logout_user,login_required
from datetime import datetime
from sqlalchemy import Table,ForeignKey,create_engine


@app.route('/home',methods=['GET', 'POST'])
def home():
	if request.method == "POST":
		ssd_id_1=request.form["id"]
		cust=Customer.query.filter_by(ssd_id=ssd_id_1).first()
		if not cust:
			flash(f'{ssd_id_1} not present in the database.','danger')
			return redirect(url_for('home'))
		else:
			return render_template('customer_info.html',cust=cust)
	return render_template("home.html")
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
			cust_count = Account.query.count()
			account_no = "FEDBNK"+str(ssn_no) + str(account_type) + str(cust_count + 100)
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
			return redirect(url_for('finish_deposit',account_no=account_no))
	return render_template('search_customer.html')

@app.route('/finish_deposit',methods=['GET','POST'])
@login_required
def finish_deposit():
	account_no = request.args.get('account_no')
	acc = Account.query.filter_by(account_no=account_no).first()
	ssn_no = acc.ssd_id
	account_type = acc.account_type
	balance = acc.deposit_amount
	account_type = acc.account_type
	if request.form.get('deposit_amount'):
		deposit_amount = int(request.form.get('deposit_amount'))
		acc.deposit_amount = acc.deposit_amount + deposit_amount
		db.create_all()
		trns = Transactions(transaction_id=str(Transactions.query.count()+10),account_no=account_no,description="Deposited",amount=deposit_amount)
		db.session.add(trns)
		try:
			db.session.commit()
			flash("Amount deposited successfully",'success')
		except:
			flash('Some error occured, Please try again!','danger')
	return render_template('deposit_money.html',account_no=account_no,ssn_no=ssn_no,account_type=account_type,balance=balance)

@app.route('/withdraw_money',methods=['GET','POST'])
@login_required
def withdraw_money():
	if request.form.get('account_no'):
		account_no = request.form.get('account_no')
		acc = Account.query.filter_by(account_no=account_no).first()
		if acc:
			ssn_no = acc.ssd_id
			account_type = acc.account_type
			balance = acc.deposit_amount
			return redirect(url_for('finish_withdraw',account_no=account_no))
	return render_template('search_customer.html')

@app.route('/finish_withdraw',methods=['GET','POST'])
@login_required
def finish_withdraw():
	account_no = request.args.get('account_no')
	acc = Account.query.filter_by(account_no=account_no).first()
	ssn_no = acc.ssd_id
	account_type = acc.account_type
	balance = acc.deposit_amount
	account_type = acc.account_type
	if request.form.get('deposit_amount'):
		withdraw_amount = int(request.form.get('deposit_amount'))
		if withdraw_amount < acc.deposit_amount:
			acc.deposit_amount = acc.deposit_amount - withdraw_amount
			db.create_all()
			trns = Transactions(transaction_id=str(Transactions.query.count()+10),account_no=account_no,description="Withdraw",amount=withdraw_amount)
			db.session.add(trns)
			try:
				db.session.commit()
				flash("Amount withdrawn successfully",'success')
			except:
				flash('Some error occured, Please try again!','danger')
		else:
			flash("Oh!!!! Insufficent Balance, Try with some smaller amount","warning")
	return render_template('withdraw_money.html',account_no=account_no,ssn_no=ssn_no,account_type=account_type,balance=balance)

@app.route('/transfer_money',methods=['GET','POST'])
@login_required
def transfer_money():
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
	if request.form.get('deposit_amount') and request.form.get('account_no') and request.form.get('deposit_amount') and request.form.get('account_type'):
		transfer_amount = int(request.form.get('deposit_amount'))
		rec_account_type = request.form.get('account_type')
		rec_account_no = request.form.get('account_no')
		rec_acc  = Account.query.filter_by(account_no= rec_account_no,account_type= rec_account_type).first()
		if rec_acc:
			if transfer_amount < acc.deposit_amount:
				acc.deposit_amount = acc.deposit_amount - transfer_amount
				rec_acc.deposit_amount = rec_acc.deposit_amount + transfer_amount
				db.create_all()
				trns = Transactions(transaction_id=str(Transactions.query.count()+10),account_no=account_no,description="Transferred to "+str(rec_account_no),amount=transfer_amount)
				db.session.add(trns)
				trns1 = Transactions(transaction_id=str(Transactions.query.count()+10),account_no=rec_account_no,description="Recieved from"+str(account_no),amount=transfer_amount)
				db.session.add(trns1)
				try:
					db.session.commit()
					flash("Amount transferred successfully",'success')
				except:
					flash('Some error occured, Please try again!','danger')
			else:
				flash("Oh!!!! Insufficent Balance, Try with some smaller amount","warning")
	return render_template('transfer_money.html',account_no=account_no,ssn_no=ssn_no,account_type=account_type,balance=balance)

@app.route('/account_statment',methods=['GET','POST'])
@login_required
def account_statment():
	trns=None
	if request.form.get('account_no') and request.form.get('last_n_trans'):
		account_no = request.form.get('account_no')
		trns = Transactions.query.filter_by(account_no=account_no).limit(int(request.form.get('last_n_trans'))).all()
		print(trns)
	elif request.form.get('account_no') and request.form.get('start_date') and request.form.get('end_date'):
		account_no = request.form.get('account_no')
		start_date = request.form.get('start_date')
		end_date = request.form.get('end_date')
		trns = Transactions.query.filter(Transactions.account_no==account_no,Transactions.date_posted >= datetime.strptime(start_date,'%Y-%m-%d'),Transactions.date_posted <= datetime.strptime(end_date,'%Y-%m-%d')).all()
		# trns = Transactions.query.filter_by(date_posted >= datetime.strptime(start_date,'%Y-%m-%d'),date_posted <= datetime.strptime(start_date,'%Y-%m-%d')).all()
		print(trns)
	return render_template('account_statment.html',trns=trns)


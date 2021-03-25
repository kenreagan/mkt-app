from flask import Blueprint, render_template, redirect, url_for, request, flash, current_app
from src.models import User, Product
from flask_login import current_user, login_required, login_user, logout_user
from src import db
import datetime
from werkzeug.security import check_password_hash, generate_password_hash
import secrets
import os
from functools import wraps


def superadminsonly():
	# the super adminstrator has the power to delete users and add other users in
    def restrict(f):
        @wraps(f)
        def wrapperfunc(*args, **kwargs):
            if current_user.is_authenticated and current_user.is_admin == False:
                abort(403)
            return f(*args, **kwargs)
        return wrapperfunc
    return restrict


def adminsonly():
# once paid one can access the dashboard 
	def restrict(f):
		@wraps(f)
		def wrapperfunc(*args, **kwargs):
			if current_user.is_authenticated and current_user.is_admin ==False:
				abort(403)
			elif current_user.is_authenticated and current_user.is_paid == True:
				return f(*args, **kwargs)
			return wrapperfunc
		return restrict

users = Blueprint(__name__, 'users')

def validate_file(name):
	name, extension = os.path.splitext(name)
	if extension.lower() not in current_app.config['ALLOWED_IMAGES']:
		flash('File format is not accepted please contact the adminstrator', "danger")
		return redirect(url_for('src.views.addProducts', email=current_user.email))
	name = secrets.token_hex(10) + extension
	return name


@users.route('/')
def index():
	return render_template('homepage.html')


@users.route('/home')
def home():
	prod = Product.query.filter_by().all()
	return render_template('index.html', prod=prod)

@users.route('/view/product/<id>')
def eachproduct(id):
	product = Product.query.filter_by(id=id).first()
	return render_template('each.html', product=product)

@users.route('/logout')
@login_required
def logout():
	logout_user()
	flash("You have been logged out successfully", "info")
	return redirect(url_for('src.views.home'))
	
@users.route('/login', methods=['GET', 'POST'])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('src.views.home'))
	nxt = request.args.get("next")
	if request.method=='POST':
		email = request.form.get('email')
		password = request.form.get('password')
		user = User.query.filter_by(email=email).first()
		if user:
			if check_password_hash(user.password,password):
				login_user(user)
				if nxt:
					return redirect(nxt)
				return redirect(url_for('src.views.home'))
			flash('you have entered the incorrect credentials ensure you enter the correct details', 'danger')
			return redirect(url_for('src.views.login'))
		flash('The user requested does not exist please create an account in order to login', 'danger')
		return redirect(url_for('src.views.register'))
	return render_template('login.html')

@users.route('/register', methods=['GET', 'POST'])
def register():
	if current_user.is_authenticated:
		return redirect(url_for('src.views.home'))
		
	if request.method == 'POST':
		password = request.form.get('password')
		firstname = request.form.get('firstname')
		lastname = request.form.get('lastname')
		phone = int(request.form.get('phone'))
		email = request.form.get('email')
		user = User.query.filter_by(email=email).first()
		if user:
			flash('The user with this email already exists choose a different name or sign in to the existing acount', 'warning')
			return redirect(url_for('src.views.login'))
		item = User(email=email, first_name=firstname,last_name=lastname, phone=phone,password=generate_password_hash(password, method='sha256'))
		db.session.add(item)
		db.session.commit()
		flash("account created successfully you can now sign in", 'success')
		return redirect(url_for('src.views.login'))
	return render_template('register.html')

#adminstrator
@users.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')


@users.route('/add/products/admin/<email>', methods=['GET', 'POST'])
@login_required
def addProducts(email):
	if request.method == 'POST':
		name = request.form.get("name")
		price = request.form.get("price")
		description = request.form.get("description")
		quantity = request.form.get("quantity")
		productImage = request.files.get("image")
		name = validate_file(productImage.filename)
		data = Product(name=name, price=price, description=description, available=quantity, path=name)
		try:
			productImage.save(os.path.join(current_app.config['UPLOAD_FOLDER'], name))
			db.session.add(data)
			db.session.commit()
			flash("product added successfully", "success")
			return redirect(url_for('src.views.addProducts', email=current_user.email))
		except:
			db.session.rollback()
			flash("Failed to add your product please try again", "danger")
			return redirect(url_for('src.views.addProducts', email=current_user.email))
	return render_template('products.html')


@users.route('/delete/product/<int>/<email>', methods=['POST'])
@login_required
def delete(id, email):
	pass


@users.route('/edit/product/<int>/<email>', methods=['GET', 'POST'])
@login_required
def edit(id, email):
	pass

from flask import Flask, render_template, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from models import db, User, Car, Booking

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///car_rental.db'
db.init_app(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.before_first_request
def create_tables():
    db.create_all()

@app.route('/')
def home():
    cars = Car.query.filter_by(is_available=True).all()
    return render_template('home.html', cars=cars)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        hashed_pw = bcrypt.generate_password_hash(request.form['password']).decode('utf-8')
        user = User(username=request.form['username'], password=hashed_pw)
        db.session.add(user)
        db.session.commit()
        flash('Registered successfully!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(username=request.form['username']).first()
        if user and bcrypt.check_password_hash(user.password, request.form['password']):
            login_user(user)
            return redirect(url_for('dashboard'))
        else:
            flash('Login Failed', 'danger')
    return render_template('login.html')

@app.route('/dashboard')
@login_required
def dashboard():
    bookings = Booking.query.filter_by(user_id=current_user.id).all()
    return render_template('dashboard.html', bookings=bookings)

@app.route('/book/<int:car_id>')
@login_required
def book_car(car_id):
    car = Car.query.get_or_404(car_id)
    if car.is_available:
        booking = Booking(user_id=current_user.id, car_id=car.id)
        car.is_available = False
        db.session.add(booking)
        db.session.commit()
        flash('Car booked successfully!', 'success')
    else:
        flash('Car is not available', 'danger')
    return redirect(url_for('dashboard'))

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)

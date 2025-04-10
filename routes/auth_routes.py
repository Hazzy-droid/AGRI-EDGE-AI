import os
import logging
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email
from datetime import datetime

from models import db, User, Farm

# Define login form using Flask-WTF
class LoginForm(FlaskForm):
    email = StringField('Email or Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Log In')

logger = logging.getLogger(__name__)

# Create blueprint
auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """Handle user registration"""
    if request.method == 'POST':
        # Get form data
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        phone = request.form.get('phone')
        location = request.form.get('location')
        farm_name = request.form.get('farm_name')
        farm_size = request.form.get('farm_size')
        farming_activities = request.form.getlist('farming_activities')
        agree_terms = request.form.get('agree_terms')
        
        # Validate form data
        error = None
        
        # Check if username already exists
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            error = "Username already exists. Please choose a different username."
        
        # Check if email already exists
        existing_email = User.query.filter_by(email=email).first()
        if existing_email:
            error = "Email already registered. Please use a different email or log in."
        
        # Check if passwords match
        if password != confirm_password:
            error = "Passwords do not match."
        
        # Check if terms are agreed
        if not agree_terms:
            error = "You must agree to the Terms of Service and Privacy Policy."
        
        if error:
            return render_template('auth/register.html', error=error)
        
        try:
            # Create new user
            new_user = User(
                username=username,
                email=email,
                password_hash=generate_password_hash(password),
                phone=phone,
                location=location,
                language='en',  # Default language
                created_at=datetime.utcnow()
            )
            
            # Add user to database
            db.session.add(new_user)
            db.session.flush()  # Get user ID without committing
            
            # Create farm if farm name provided
            if farm_name:
                new_farm = Farm(
                    name=farm_name,
                    size=float(farm_size) if farm_size else None,
                    location=location,
                    user_id=new_user.id,
                    created_at=datetime.utcnow()
                )
                db.session.add(new_farm)
            
            # Commit changes
            db.session.commit()
            
            # Log user in
            login_user(new_user)
            
            # Redirect to dashboard
            flash("Account created successfully! Welcome to the Climate-Smart Agriculture Platform.", "success")
            return redirect(url_for('main.dashboard'))
            
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error creating user: {str(e)}")
            error = "An error occurred while creating your account. Please try again."
            return render_template('auth/register.html', error=error)
    
    # GET request - display registration form
    return render_template('auth/register.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Handle user login"""
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
        
    # Create login form
    form = LoginForm()
    
    if form.validate_on_submit():
        # Find user by email or username
        user = User.query.filter((User.email == form.email.data) | 
                                (User.username == form.email.data)).first()
        
        # Check if user exists and password is correct
        if not user or not check_password_hash(user.password_hash, form.password.data):
            flash("Invalid email/username or password.", "error")
            return render_template('auth/login.html', form=form)
        
        # Log user in
        login_user(user, remember=form.remember.data)
        
        # Redirect to requested page or dashboard
        next_page = request.args.get('next')
        if next_page:
            return redirect(next_page)
        return redirect(url_for('main.dashboard'))
    
    # GET request - display login form
    return render_template('auth/login.html', form=form)

@auth_bp.route('/logout')
@login_required
def logout():
    """Handle user logout"""
    logout_user()
    flash("You have been logged out.", "info")
    return redirect(url_for('main.index'))

@auth_bp.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    """Handle forgot password requests"""
    if request.method == 'POST':
        email = request.form.get('email')
        
        # Check if user exists
        user = User.query.filter_by(email=email).first()
        if not user:
            return render_template('auth/forgot_password.html', error="No account found with that email address.")
        
        # In a real implementation, generate reset token and send email
        # For demonstration purposes, we'll just show a success message
        
        success = "Password reset instructions have been sent to your email. Please check your inbox."
        return render_template('auth/forgot_password.html', success=success)
    
    # GET request - display forgot password form
    return render_template('auth/forgot_password.html')

@auth_bp.route('/reset-password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    """Handle password reset with token"""
    # In a real implementation, verify token and allow password reset
    # For demonstration purposes, we'll redirect to login
    
    flash("This feature is not implemented in the demo. Please contact support for password resets.", "info")
    return redirect(url_for('auth.login'))

@auth_bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    """Display and update user profile"""
    if request.method == 'POST':
        # Update user profile
        # Implementation would go here
        flash("Profile updated successfully.", "success")
        return redirect(url_for('auth.profile'))
    
    # GET request - display profile page
    return render_template('auth/profile.html', user=current_user)
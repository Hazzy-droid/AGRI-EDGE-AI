import os
import json
import logging
from datetime import datetime
from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from flask_login import login_required, current_user
from models import db, User
from utils.ai_assistant import get_ai_response
from utils.sms_alerts import send_sms

logger = logging.getLogger(__name__)

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/admin/service-config', methods=['GET'])
@login_required
def service_config():
    """Display service configuration page"""
    # Check if user is an admin
    if not current_user.is_admin:
        flash('Access denied. Admin privileges required.', 'danger')
        return redirect(url_for('main.dashboard'))
    
    # Test service status
    ai_service_status = test_ai_service()
    sms_service_status = test_sms_service()
    
    # Get current config
    config = {
        'USE_PROXY_SERVICE': current_app.config.get('USE_PROXY_SERVICE', False),
        'SERVICE_PROXY_URL': current_app.config.get('SERVICE_PROXY_URL', ''),
        'SERVICE_PROXY_KEY': current_app.config.get('SERVICE_PROXY_KEY', ''),
        'PERPLEXITY_API_KEY': current_app.config.get('PERPLEXITY_API_KEY', ''),
        'TWILIO_ACCOUNT_SID': current_app.config.get('TWILIO_ACCOUNT_SID', ''),
        'TWILIO_AUTH_TOKEN': current_app.config.get('TWILIO_AUTH_TOKEN', ''),
        'TWILIO_PHONE_NUMBER': current_app.config.get('TWILIO_PHONE_NUMBER', '')
    }
    
    return render_template('admin/service_config.html', 
                          config=config, 
                          ai_service_status=ai_service_status,
                          sms_service_status=sms_service_status)

@admin_bp.route('/admin/service-config', methods=['POST'])
@login_required
def update_service_config():
    """Update service configuration"""
    # Check if user is an admin
    if not current_user.is_admin:
        flash('Access denied. Admin privileges required.', 'danger')
        return redirect(url_for('main.dashboard'))
    
    # Get form data
    use_proxy_service = 'use_proxy_service' in request.form
    service_proxy_url = request.form.get('service_proxy_url', '')
    service_proxy_key = request.form.get('service_proxy_key', '')
    perplexity_api_key = request.form.get('perplexity_api_key', '')
    twilio_account_sid = request.form.get('twilio_account_sid', '')
    twilio_auth_token = request.form.get('twilio_auth_token', '')
    twilio_phone_number = request.form.get('twilio_phone_number', '')
    
    # Update environment variables (this will only last for current session)
    os.environ['USE_PROXY_SERVICE'] = 'true' if use_proxy_service else 'false'
    
    if use_proxy_service:
        os.environ['SERVICE_PROXY_URL'] = service_proxy_url
        os.environ['SERVICE_PROXY_KEY'] = service_proxy_key
    else:
        os.environ['PERPLEXITY_API_KEY'] = perplexity_api_key
        os.environ['TWILIO_ACCOUNT_SID'] = twilio_account_sid
        os.environ['TWILIO_AUTH_TOKEN'] = twilio_auth_token
        os.environ['TWILIO_PHONE_NUMBER'] = twilio_phone_number
    
    # Update application config
    current_app.config['USE_PROXY_SERVICE'] = use_proxy_service
    current_app.config['SERVICE_PROXY_URL'] = service_proxy_url
    current_app.config['SERVICE_PROXY_KEY'] = service_proxy_key
    current_app.config['PERPLEXITY_API_KEY'] = perplexity_api_key
    current_app.config['TWILIO_ACCOUNT_SID'] = twilio_account_sid
    current_app.config['TWILIO_AUTH_TOKEN'] = twilio_auth_token
    current_app.config['TWILIO_PHONE_NUMBER'] = twilio_phone_number
    
    # Save configuration to file (optional, more advanced approach)
    # This would require implementing a persistent storage mechanism
    
    flash('Service configuration updated successfully', 'success')
    return redirect(url_for('admin.service_config'))

@admin_bp.route('/admin/test-services', methods=['GET'])
@login_required
def test_services():
    """Test external services and return results"""
    # Check if user is an admin
    if not current_user.is_admin:
        flash('Access denied. Admin privileges required.', 'danger')
        return redirect(url_for('main.dashboard'))
    
    # Test services
    ai_result = test_ai_service()
    sms_result = test_sms_service()
    
    # Display results
    if ai_result:
        flash('AI Service test successful', 'success')
    else:
        flash('AI Service test failed', 'danger')
        
    if sms_result:
        flash('SMS Service test successful', 'success')
    else:
        flash('SMS Service test failed', 'danger')
    
    return redirect(url_for('admin.service_config'))

@admin_bp.route('/admin/service-proxy-docs', methods=['GET'])
@login_required
def service_proxy_docs():
    """Display documentation for setting up a service proxy"""
    # Check if user is an admin
    if not current_user.is_admin:
        flash('Access denied. Admin privileges required.', 'danger')
        return redirect(url_for('main.dashboard'))
    
    return render_template('admin/service_proxy_docs.html')

def test_ai_service():
    """Test AI service connectivity and functionality"""
    try:
        # Simple query to test service
        response = get_ai_response("What's the current date?", context="platform_help")
        return response.get('success', False)
    except Exception as e:
        logger.error(f"AI service test error: {str(e)}")
        return False

def test_sms_service():
    """Test SMS service connectivity (without actually sending SMS)"""
    try:
        # We only verify the configuration without sending actual SMS
        if current_app.config.get('USE_PROXY_SERVICE'):
            # Check if proxy URL is configured
            return bool(current_app.config.get('SERVICE_PROXY_URL'))
        else:
            # Check if Twilio credentials are configured
            return all([
                current_app.config.get('TWILIO_ACCOUNT_SID'),
                current_app.config.get('TWILIO_AUTH_TOKEN'),
                current_app.config.get('TWILIO_PHONE_NUMBER')
            ])
    except Exception as e:
        logger.error(f"SMS service test error: {str(e)}")
        return False
import os
import logging
from datetime import datetime
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException
from utils.service_proxy import send_sms_proxy, send_weather_alert_proxy, send_crop_alert_proxy

logger = logging.getLogger(__name__)

# Twilio configuration
TWILIO_ACCOUNT_SID = os.environ.get("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.environ.get("TWILIO_AUTH_TOKEN")
TWILIO_PHONE_NUMBER = os.environ.get("TWILIO_PHONE_NUMBER")

# Service configuration
USE_PROXY_SERVICE = os.environ.get("USE_PROXY_SERVICE", "false").lower() == "true"

def send_sms(to_phone_number, message):
    """
    Send SMS using Twilio or proxy service
    
    Args:
        to_phone_number (str): Recipient's phone number
        message (str): Message content
        
    Returns:
        dict: Status of the SMS sending operation
    """
    if USE_PROXY_SERVICE:
        # Use proxy service to send SMS
        logger.info(f"Using proxy service to send SMS to {to_phone_number}")
        return send_sms_proxy(to_phone_number, message)
    
    # Direct Twilio API approach
    if not all([TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_PHONE_NUMBER]):
        logger.error("Twilio credentials not configured")
        return {
            "success": False,
            "error": "SMS service not configured. Please contact administrator."
        }
    
    try:
        # Initialize Twilio client
        client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
        
        # Send message
        twilio_message = client.messages.create(
            body=message,
            from_=TWILIO_PHONE_NUMBER,
            to=to_phone_number
        )
        
        logger.info(f"SMS sent successfully to {to_phone_number}, SID: {twilio_message.sid}")
        
        return {
            "success": True,
            "message_sid": twilio_message.sid,
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except TwilioRestException as e:
        logger.error(f"Twilio error: {str(e)}")
        return {
            "success": False,
            "error": f"Error sending SMS: {str(e)}"
        }
    except Exception as e:
        logger.error(f"Unexpected error sending SMS: {str(e)}")
        return {
            "success": False,
            "error": "An unexpected error occurred. Please try again later."
        }

def send_weather_alert(user, weather_alert):
    """
    Send weather alert SMS to user
    
    Args:
        user (User): User object with contact information
        weather_alert (dict): Weather alert details
        
    Returns:
        dict: Status of the SMS sending operation
    """
    if USE_PROXY_SERVICE:
        # Use proxy service for weather alerts
        logger.info(f"Using proxy service to send weather alert to user {user.id}")
        return send_weather_alert_proxy(user, weather_alert)
    
    # Format message
    message = f"WEATHER ALERT: {weather_alert['type']} expected in {user.location} "\
              f"on {weather_alert['date']}. {weather_alert['recommendation']}"
    
    # Get user's phone number
    phone_number = getattr(user, 'phone', None)
    if not phone_number:
        logger.error(f"Cannot send weather alert: no phone number for user {user.id}")
        return {
            "success": False,
            "error": "User has no phone number registered"
        }
    
    # Send SMS
    return send_sms(phone_number, message)

def send_crop_alert(user, farm, crop_alert):
    """
    Send crop health alert SMS to user
    
    Args:
        user (User): User object with contact information
        farm (Farm): Farm object
        crop_alert (dict): Crop alert details
        
    Returns:
        dict: Status of the SMS sending operation
    """
    if USE_PROXY_SERVICE:
        # Use proxy service for crop alerts
        logger.info(f"Using proxy service to send crop alert to user {user.id}")
        return send_crop_alert_proxy(user, farm, crop_alert)
    
    # Format message
    message = f"CROP ALERT for {farm.name}: {crop_alert['issue']} detected in your "\
              f"{crop_alert['crop_type']}. {crop_alert['recommendation']}"
    
    # Get user's phone number
    phone_number = getattr(user, 'phone', None)
    if not phone_number:
        logger.error(f"Cannot send crop alert: no phone number for user {user.id}")
        return {
            "success": False,
            "error": "User has no phone number registered"
        }
    
    # Send SMS
    return send_sms(phone_number, message)

def send_marketplace_notification(user, notification_type, item_details):
    """
    Send marketplace activity notification SMS
    
    Args:
        user (User): User object with contact information
        notification_type (str): Type of notification (new_offer, item_sold, etc.)
        item_details (dict): Details about the marketplace item
        
    Returns:
        dict: Status of the SMS sending operation
    """
    # Format message based on notification type
    if notification_type == "new_offer":
        message = f"NEW OFFER: Someone is interested in your {item_details['title']}. "\
                 f"Offer: {item_details['currency']} {item_details['price']}. "\
                 f"Check your messages for details."
    elif notification_type == "item_sold":
        message = f"ITEM SOLD: Your listing '{item_details['title']}' has been marked as sold. "\
                 f"Transaction amount: {item_details['currency']} {item_details['price']}."
    elif notification_type == "price_drop":
        message = f"PRICE DROP: An item you're watching '{item_details['title']}' has dropped in price. "\
                 f"New price: {item_details['currency']} {item_details['price']}."
    else:
        message = f"MARKETPLACE UPDATE: There's new activity related to '{item_details['title']}'. "\
                 f"Login to the platform for details."
    
    # Get user's phone number
    phone_number = getattr(user, 'phone', None)
    if not phone_number:
        logger.error(f"Cannot send marketplace notification: no phone number for user {user.id}")
        return {
            "success": False,
            "error": "User has no phone number registered"
        }
    
    # Send SMS
    return send_sms(phone_number, message)
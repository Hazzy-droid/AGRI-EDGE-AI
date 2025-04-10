import os
import json
import logging
import requests
from datetime import datetime
from urllib.parse import urljoin

logger = logging.getLogger(__name__)

class ServiceProxy:
    """
    Proxy service for making API calls to external services that handle authenticated requests
    This allows us to avoid storing API keys directly in this application by using external microservices
    """
    
    def __init__(self, base_url=None):
        """
        Initialize the service proxy
        
        Args:
            base_url (str): The base URL for the external service proxy
        """
        # Use environment variable or default to the provided base_url
        self.base_url = os.environ.get("SERVICE_PROXY_URL", base_url)
        self.service_key = os.environ.get("SERVICE_PROXY_KEY", "")
        
    def make_request(self, endpoint, method="POST", payload=None, params=None, headers=None):
        """
        Make a request to the external service proxy
        
        Args:
            endpoint (str): The endpoint to call
            method (str): HTTP method (GET, POST, etc.)
            payload (dict): The request payload
            params (dict): URL parameters
            headers (dict): Custom headers
            
        Returns:
            dict: Response from the external service
        """
        if not self.base_url:
            logger.error("Service proxy URL not configured")
            return {
                "success": False,
                "error": "Service proxy not configured. Please set SERVICE_PROXY_URL."
            }
            
        # Build full URL
        url = urljoin(self.base_url, endpoint)
        
        # Set up headers
        if headers is None:
            headers = {}
        
        # Add authentication if service key is provided
        if self.service_key:
            headers["Authorization"] = f"Bearer {self.service_key}"
        
        # Set content type
        headers["Content-Type"] = "application/json"
        
        try:
            # Make the request
            if method.upper() == "GET":
                response = requests.get(url, params=params, headers=headers)
            elif method.upper() == "POST":
                response = requests.post(url, json=payload, params=params, headers=headers)
            elif method.upper() == "PUT":
                response = requests.put(url, json=payload, params=params, headers=headers)
            elif method.upper() == "DELETE":
                response = requests.delete(url, json=payload, params=params, headers=headers)
            else:
                logger.error(f"Unsupported HTTP method: {method}")
                return {
                    "success": False,
                    "error": f"Unsupported HTTP method: {method}"
                }
                
            # Check response
            if response.status_code == 200:
                return response.json()
            else:
                logger.error(f"Error from service proxy: {response.status_code}, {response.text}")
                return {
                    "success": False,
                    "error": f"Error from service proxy: {response.status_code}",
                    "details": response.text
                }
                
        except requests.RequestException as e:
            logger.error(f"Request error: {str(e)}")
            return {
                "success": False,
                "error": f"Error connecting to service proxy: {str(e)}"
            }
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            return {
                "success": False,
                "error": f"An unexpected error occurred: {str(e)}"
            }

# Create proxy service instances for different services
ai_proxy = ServiceProxy()
sms_proxy = ServiceProxy()

def get_ai_response_proxy(query, context="general_farming", conversation_history=None):
    """
    Get AI-generated response using the external AI service proxy
    
    Args:
        query (str): The user's question or message
        context (str): The context for the conversation
        conversation_history (list): Previous messages in the conversation
        
    Returns:
        dict: Response containing the assistant's message and metadata
    """
    if conversation_history is None:
        conversation_history = []
        
    payload = {
        "query": query,
        "context": context,
        "conversation_history": conversation_history
    }
    
    return ai_proxy.make_request("/ai/chat", method="POST", payload=payload)

def send_sms_proxy(to_phone_number, message, message_type="alert"):
    """
    Send SMS using the external SMS service proxy
    
    Args:
        to_phone_number (str): The recipient's phone number
        message (str): The message content
        message_type (str): Type of message (alert, notification, etc.)
        
    Returns:
        dict: Status and details of the SMS send operation
    """
    payload = {
        "to_phone_number": to_phone_number,
        "message": message,
        "message_type": message_type
    }
    
    return sms_proxy.make_request("/sms/send", method="POST", payload=payload)

def send_weather_alert_proxy(user, weather_alert):
    """
    Send weather alert SMS using the external service proxy
    
    Args:
        user (User): The user object containing contact information
        weather_alert (dict): Weather alert information
        
    Returns:
        dict: Status and details of the SMS send operation
    """
    # Format message
    message = f"WEATHER ALERT: {weather_alert['type']} expected in {user.location} "\
              f"on {weather_alert['date']}. {weather_alert['recommendation']}"
    
    # Send SMS
    return send_sms_proxy(user.phone, message, message_type="weather_alert")

def send_crop_alert_proxy(user, farm, crop_alert):
    """
    Send crop health alert SMS using the external service proxy
    
    Args:
        user (User): The user object containing contact information
        farm (Farm): The farm object
        crop_alert (dict): Crop alert information
        
    Returns:
        dict: Status and details of the SMS send operation
    """
    # Format message
    message = f"CROP ALERT for {farm.name}: {crop_alert['issue']} detected in your "\
              f"{crop_alert['crop_type']}. {crop_alert['recommendation']}"
    
    # Send SMS
    return send_sms_proxy(user.phone, message, message_type="crop_alert")
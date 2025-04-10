import os
import json
import logging
import requests
from datetime import datetime
from utils.service_proxy import get_ai_response_proxy

logger = logging.getLogger(__name__)

# Constants
PERPLEXITY_API_KEY = os.environ.get("PERPLEXITY_API_KEY")
PERPLEXITY_API_URL = "https://api.perplexity.ai/chat/completions"
DEFAULT_MODEL = "llama-3.1-sonar-small-128k-online"

# Service configuration
USE_PROXY_SERVICE = os.environ.get("USE_PROXY_SERVICE", "false").lower() == "true"

# System messages for different contexts
SYSTEM_MESSAGES = {
    "general_farming": """
You are an expert agricultural AI assistant for the Climate-Smart Agriculture Platform.
Provide accurate, practical farming advice to African farmers, with a focus on:
1. Climate-smart agriculture practices that enhance resilience
2. Sustainable farming techniques adapted to local conditions
3. Resource optimization (water, soil, inputs)
4. Pest and disease management with minimal environmental impact
5. Post-harvest handling to reduce losses
6. Market information and value addition

Keep responses concise, practical, and appropriate for smallholder farmers in Africa.
Consider local context, limited resources, and traditional knowledge.
When discussing new technologies or advanced techniques, focus on low-cost, 
accessible solutions that can be implemented with minimal external inputs.
    """,
    
    "weather": """
You are a specialized agricultural weather advisor for the Climate-Smart Agriculture Platform.
Provide insights on weather patterns and their implications for farming activities:
1. Interpret weather forecasts in relation to farming decisions
2. Recommend timing for planting, irrigation, fertilization, and harvesting
3. Advise on managing weather-related risks (drought, floods, frost, etc.)
4. Explain climate change impacts on local agriculture
5. Suggest adaptive strategies for changing weather patterns

Make recommendations that are practical, locally relevant, and actionable.
Focus on resilience-building measures and risk mitigation strategies.
    """,
    
    "soil_health": """
You are a soil health specialist for the Climate-Smart Agriculture Platform.
Provide expert advice on soil management and improvement:
1. Interpret soil test results and sensor data
2. Recommend organic and sustainable soil improvement practices
3. Advise on appropriate fertilization based on crop needs and soil conditions
4. Suggest crop rotation and intercropping for soil health
5. Address soil erosion, compaction, and degradation issues
6. Promote conservation agriculture principles

Focus on low-cost, locally available solutions that build long-term soil fertility.
Consider the specific soil challenges faced in different African regions.
    """,
    
    "crop_advice": """
You are a crop management expert for the Climate-Smart Agriculture Platform.
Provide specialized guidance on crop production:
1. Recommend appropriate crop varieties based on local conditions
2. Advise on optimal planting, care, and harvesting practices
3. Suggest efficient irrigation and water management techniques
4. Identify and address nutrient deficiencies
5. Provide integrated pest and disease management solutions
6. Recommend sustainable intensification practices

Tailor advice to both staple and high-value crops relevant to African farmers.
Focus on practical techniques that maximize yields while minimizing environmental impact.
    """,
    
    "livestock": """
You are a livestock management specialist for the Climate-Smart Agriculture Platform.
Provide expert guidance on sustainable animal husbandry:
1. Advise on animal nutrition and sustainable feed sources
2. Recommend appropriate healthcare and disease prevention
3. Suggest housing and management systems suited to local conditions
4. Provide information on breeding and genetic improvement
5. Recommend waste management and utilization techniques
6. Integrate livestock with crop production systems

Focus on practices that improve productivity while enhancing animal welfare.
Consider smallholder contexts where livestock serve multiple functions 
(food, income, savings, draft power, social status).
    """,
    
    "platform_help": """
You are a helpful guide for the Climate-Smart Agriculture Platform.
Assist users in navigating and utilizing the platform effectively:
1. Explain platform features and how to access them
2. Guide users on interpreting data and recommendations
3. Troubleshoot common issues users might encounter
4. Suggest relevant platform features based on user needs
5. Explain how to customize settings and preferences
6. Direct users to appropriate resources and support channels

Be patient, clear, and supportive, recognizing that users may have varying 
levels of technical and digital literacy. Focus on making the platform 
accessible and valuable to all users.
    """
}

def get_ai_response(user_query, context="general_farming", conversation_history=None):
    """
    Get AI-generated response using Perplexity API or external proxy service
    
    Args:
        user_query (str): The user's question or message
        context (str): The context for the conversation (determines system message)
        conversation_history (list): Previous messages in the conversation
        
    Returns:
        dict: Response containing the assistant's message and metadata
    """
    # Initialize conversation history if not provided
    if conversation_history is None:
        conversation_history = []
    
    # Check if we should use proxy service
    if USE_PROXY_SERVICE:
        # Use proxy service to get AI response
        logger.info(f"Using proxy service for AI response (context: {context})")
        return get_ai_response_proxy(user_query, context, conversation_history)
    
    # Direct API approach (requires API key)
    if not PERPLEXITY_API_KEY:
        logger.error("Perplexity API key not configured")
        return {
            "success": False,
            "error": "AI assistant service not configured. Please contact administrator."
        }
    
    # Prepare messages for the API
    messages = []
    
    # Add system message based on context
    system_message = SYSTEM_MESSAGES.get(context, SYSTEM_MESSAGES["general_farming"])
    messages.append({"role": "system", "content": system_message})
    
    # Add conversation history
    for msg in conversation_history:
        messages.append(msg)
    
    # Add the current user query
    messages.append({"role": "user", "content": user_query})
    
    # Prepare request payload
    payload = {
        "model": DEFAULT_MODEL,
        "messages": messages,
        "temperature": 0.7,
        "top_p": 0.9,
        "max_tokens": 1000,
        "search_domain_filter": [],
        "return_images": False,
        "return_related_questions": False,
        "search_recency_filter": "month",
        "top_k": 0,
        "stream": False,
        "presence_penalty": 0,
        "frequency_penalty": 1
    }
    
    # Set up headers with API key
    headers = {
        "Authorization": f"Bearer {PERPLEXITY_API_KEY}",
        "Content-Type": "application/json"
    }
    
    try:
        # Make request to Perplexity API
        response = requests.post(
            PERPLEXITY_API_URL,
            headers=headers,
            json=payload
        )
        
        # Check if request was successful
        if response.status_code == 200:
            response_data = response.json()
            
            # Extract assistant message
            assistant_message = response_data["choices"][0]["message"]["content"]
            
            # Extract citations if available
            citations = response_data.get("citations", [])
            
            return {
                "success": True,
                "message": assistant_message,
                "citations": citations,
                "timestamp": datetime.utcnow().isoformat()
            }
        else:
            logger.error(f"Perplexity API error: {response.status_code}, {response.text}")
            return {
                "success": False,
                "error": f"Error communicating with AI service: {response.status_code}",
                "details": response.text
            }
            
    except Exception as e:
        logger.error(f"Exception calling Perplexity API: {str(e)}")
        return {
            "success": False,
            "error": "An unexpected error occurred. Please try again later."
        }

def get_farming_advice(crop_type, location, issue=None):
    """
    Get farming advice for specific crop and location
    
    Args:
        crop_type (str): The type of crop
        location (str): The location/region
        issue (str, optional): Specific issue or question
        
    Returns:
        dict: AI response with farming advice
    """
    # Construct a targeted query
    if issue:
        query = f"I'm growing {crop_type} in {location} and facing this issue: {issue}. What should I do?"
    else:
        query = f"I'm growing {crop_type} in {location}. What are the best practices for this crop in my region?"
    
    return get_ai_response(query, context="crop_advice")

def get_soil_recommendations(soil_data):
    """
    Get soil management recommendations based on soil data
    
    Args:
        soil_data (dict): Soil sensor or test data
        
    Returns:
        dict: AI response with soil recommendations
    """
    # Construct a detailed query based on soil data
    query = f"Based on my soil test results: pH {soil_data.get('ph', 'unknown')}, "
    query += f"Nitrogen {soil_data.get('nitrogen', 'unknown')} ppm, "
    query += f"Phosphorus {soil_data.get('phosphorus', 'unknown')} ppm, "
    query += f"Potassium {soil_data.get('potassium', 'unknown')} ppm, "
    query += f"soil moisture {soil_data.get('moisture', 'unknown')}%, "
    query += f"and electrical conductivity {soil_data.get('electrical_conductivity', 'unknown')} dS/m. "
    query += "What soil management practices should I implement and what crops would grow well?"
    
    return get_ai_response(query, context="soil_health")

def get_weather_interpretation(weather_data, crop_type):
    """
    Get agricultural interpretation of weather forecast
    
    Args:
        weather_data (dict): Weather forecast data
        crop_type (str): The type of crop
        
    Returns:
        dict: AI response with weather interpretation
    """
    # Format weather data into a readable query
    query = f"Here's a 5-day weather forecast for my farm: "
    
    for day in weather_data.get('forecast', [])[:5]:
        query += f"{day.get('date')}: {day.get('condition')}, "
        query += f"temperature {day.get('temp_min')}°C to {day.get('temp_max')}°C, "
        query += f"precipitation {day.get('precipitation')}mm, "
        query += f"humidity {day.get('humidity')}%, "
        query += f"wind {day.get('wind_speed')}m/s. "
    
    query += f"I'm growing {crop_type}. How should I adjust my farming activities based on this forecast?"
    
    return get_ai_response(query, context="weather")

def get_platform_help(feature):
    """
    Get help with using platform features
    
    Args:
        feature (str): The platform feature the user needs help with
        
    Returns:
        dict: AI response with platform usage help
    """
    query = f"How do I use the {feature} feature of the Climate-Smart Agriculture Platform?"
    return get_ai_response(query, context="platform_help")

def get_pest_disease_recommendations(crop_type, symptoms):
    """
    Get recommendations for pest and disease management
    
    Args:
        crop_type (str): The type of crop
        symptoms (str): Description of the pest/disease symptoms
        
    Returns:
        dict: AI response with pest/disease management recommendations
    """
    query = f"My {crop_type} plants are showing these symptoms: {symptoms}. "
    query += "What could be the problem and how should I manage it using integrated pest management approaches?"
    
    return get_ai_response(query, context="crop_advice")
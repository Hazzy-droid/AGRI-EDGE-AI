import os
import logging
from flask import Blueprint, render_template, request, jsonify, redirect, url_for, flash, session
from flask_login import login_required, current_user
from datetime import datetime, timedelta
import json

from utils.satellite_processing import SatelliteProcessor
from utils.weather_forecasting import WeatherForecaster
from utils.soil_sensor import SoilSensorManager
from utils.data_fusion import DataFusionEngine
from ai_models.edge_models import EdgeModelManager

logger = logging.getLogger(__name__)

# Create blueprint
main_bp = Blueprint('main', __name__)

# Initialize utilities
satellite_processor = SatelliteProcessor()
weather_forecaster = WeatherForecaster()
soil_sensor_manager = SoilSensorManager()
data_fusion_engine = DataFusionEngine()
edge_model_manager = EdgeModelManager()

@main_bp.route('/')
def index():
    """Redirect to login page"""
    return redirect(url_for('auth.login'))

@main_bp.route('/dashboard')
@login_required
def dashboard():
    """Render the main dashboard"""
    # Initialize default data
    farm_id = request.args.get('farm_id', '1')
    
    # Get farm location (default to Kenya)
    farm_location = (0.0236, 37.9062)  # Kenya coordinates
    
    # Get current date
    current_date = datetime.now().strftime('%B %d, %Y')
    
    # Get weather data for the farm location
    weather_data = weather_forecaster.get_current_weather(farm_location[0], farm_location[1])
    weather_forecast = weather_forecaster.get_weather_forecast(farm_location[0], farm_location[1], days=7)
    
    # Get soil data
    soil_data = soil_sensor_manager.get_sensor_data(f"sensor_{farm_id}")
    
    # Mock farms and crops data for user dashboard
    farms = [
        {'id': 1, 'name': 'Main Farm', 'location': 'Nakuru, Kenya', 'size': 5.2},
        {'id': 2, 'name': 'River Plot', 'location': 'Nakuru, Kenya', 'size': 2.8}
    ]
    
    crops = [
        {'id': 1, 'name': 'Maize', 'variety': 'H614', 'health_status': 'Good', 'area': 3.5},
        {'id': 2, 'name': 'Beans', 'variety': 'KK8', 'health_status': 'Moderate', 'area': 1.7},
        {'id': 3, 'name': 'Sweet Potatoes', 'variety': 'SPK004', 'health_status': 'Good', 'area': 2.8}
    ]
    
    # Mock achievement data
    achievements = [
        {'id': 1, 'name': 'Soil Expert', 'category': 'learning'},
        {'id': 2, 'name': 'Water Wise', 'category': 'learning'},
        {'id': 3, 'name': 'Early Adopter', 'category': 'platform'},
        {'id': 4, 'name': 'Community Contributor', 'category': 'community'},
        {'id': 5, 'name': 'Sustainable Farmer', 'category': 'farming'}
    ]
    
    # Calculate total farm area
    total_area = sum(farm['size'] for farm in farms)
    
    # Mock gamification level data
    level_progress = 75  # Percentage to next level
    points_to_next_level = 80
    points_to_next_level_percent = 75
    
    # Prepare data for the modern dashboard
    context = {
        'farm_id': farm_id,
        'current_date': current_date,
        'farms': farms,
        'crops': crops,
        'total_area': total_area,
        'achievements': achievements,
        'level_progress': level_progress,
        'points_to_next_level': points_to_next_level,
        'points_to_next_level_percent': points_to_next_level_percent,
        'recommendations': get_sample_recommendations(farm_id)
    }
    
    # Use our new dashboard template
    return render_template('dashboard/index.html', **context)

@main_bp.route('/satellite')
@login_required
def satellite():
    """Render the satellite imagery page"""
    # Initialize default data
    farm_id = request.args.get('farm_id', '1')
    
    # Get farm location (default to Kenya)
    farm_location = (0.0236, 37.9062)  # Kenya coordinates
    
    # Get satellite data
    try:
        # In a real implementation, this would call satellite_processor.get_satellite_image()
        ndvi_series = [
            {"date": "2023-01-01", "average_ndvi": 0.35},
            {"date": "2023-02-01", "average_ndvi": 0.42},
            {"date": "2023-03-01", "average_ndvi": 0.56},
            {"date": "2023-04-01", "average_ndvi": 0.68},
            {"date": "2023-05-01", "average_ndvi": 0.72},
            {"date": "2023-06-01", "average_ndvi": 0.65},
            {"date": "2023-07-01", "average_ndvi": 0.58}
        ]
        
        satellite_data = {
            'farm_id': farm_id,
            'ndvi_series': ndvi_series,
            'current_ndvi': ndvi_series[-1]["average_ndvi"],
            'crop_health': {
                'overall_status': 'Good',
                'poor_percent': 10,
                'fair_percent': 20,
                'good_percent': 50,
                'excellent_percent': 20
            },
            'water_stress': {
                'overall_status': 'Low Water Stress',
                'severe_percent': 5,
                'moderate_percent': 15,
                'low_percent': 30,
                'no_stress_percent': 50
            }
        }
        
        logger.info(f"Successfully retrieved satellite data for farm {farm_id}")
        return render_template('satellite_new.html', satellite_data=satellite_data)
        
    except Exception as e:
        logger.error(f"Error retrieving satellite data: {str(e)}")
        satellite_data = {
            'farm_id': farm_id,
            'ndvi_series': [],
            'current_ndvi': 0.65,  # Default value
            'crop_health': {
                'overall_status': 'Unknown',
                'poor_percent': 0,
                'fair_percent': 0,
                'good_percent': 0,
                'excellent_percent': 0
            },
            'water_stress': {
                'overall_status': 'Unknown',
                'severe_percent': 0,
                'moderate_percent': 0,
                'low_percent': 0,
                'no_stress_percent': 0
            }
        }
        flash("Unable to retrieve satellite data. Please try again later.", "error")
        return render_template('satellite_new.html', satellite_data=satellite_data)

@main_bp.route('/satellite/old')
@login_required
def satellite_old():
    """Render the old satellite imagery page"""
    # Initialize default data
    farm_id = request.args.get('farm_id', '1')
    
    # Get farm location (default to Kenya)
    farm_location = (0.0236, 37.9062)  # Kenya coordinates
    
    # Sample satellite data for demo
    # In a real implementation, this would call satellite_processor.get_satellite_image()
    ndvi_series = [
        {"date": "2023-01-01", "average_ndvi": 0.65},
        {"date": "2023-01-15", "average_ndvi": 0.67},
        {"date": "2023-02-01", "average_ndvi": 0.70},
        {"date": "2023-02-15", "average_ndvi": 0.72},
        {"date": "2023-03-01", "average_ndvi": 0.75},
        {"date": "2023-03-15", "average_ndvi": 0.73},
        {"date": "2023-04-01", "average_ndvi": 0.71}
    ]
    
    satellite_data = {
        'farm_id': farm_id,
        'ndvi_series': ndvi_series,
        'current_ndvi': ndvi_series[-1]["average_ndvi"],
        'crop_health': {
            'overall_status': 'Good',
            'poor_percent': 10,
            'fair_percent': 20,
            'good_percent': 50,
            'excellent_percent': 20
        },
        'water_stress': {
            'overall_status': 'Low Water Stress',
            'severe_percent': 5,
            'moderate_percent': 15,
            'low_percent': 30,
            'no_stress_percent': 50
        }
    }
    
    return render_template('satellite.html', satellite_data=satellite_data)

@main_bp.route('/weather')
@login_required
def weather():
    """Render the weather forecasting page"""
    # Get farm location (default to Kenya)
    farm_location = (0.0236, 37.9062)  # Kenya coordinates
    
    # Get current weather
    current_weather = weather_forecaster.get_current_weather(farm_location[0], farm_location[1])
    
    # Get 7-day forecast
    forecast = weather_forecaster.get_weather_forecast(farm_location[0], farm_location[1], days=7)
    
    # Get hourly forecast for the next 24 hours
    hourly_forecast = weather_forecaster.get_hourly_forecast(farm_location[0], farm_location[1], hours=24)
    
    # Get planting recommendations
    planting_recommendations = weather_forecaster.generate_planting_recommendation(
        farm_location, 
        crop_types=["maize", "rice", "sorghum", "millet", "cassava"]
    )
    
    # Prepare data for the weather page
    context = {
        'current_weather': current_weather,
        'daily_forecast': forecast,
        'hourly_forecast': hourly_forecast,
        'planting_recommendations': planting_recommendations
    }
    
    return render_template('weather.html', **context)

@main_bp.route('/soil')
@login_required
def soil():
    """Render the soil monitoring page"""
    # Initialize default data
    farm_id = request.args.get('farm_id', '1')
    crop_type = request.args.get('crop_type', 'maize')
    
    # Get soil data
    soil_data = soil_sensor_manager.get_sensor_data(f"sensor_{farm_id}")
    
    # Analyze soil moisture for the specified crop
    moisture_analysis = soil_sensor_manager.analyze_soil_moisture(soil_data, crop_type)
    
    # Analyze soil fertility for the specified crop
    fertility_analysis = soil_sensor_manager.analyze_soil_fertility(soil_data, crop_type)
    
    # Prepare data for the soil page
    context = {
        'farm_id': farm_id,
        'crop_type': crop_type,
        'soil_data': soil_data,
        'moisture_analysis': moisture_analysis,
        'fertility_analysis': fertility_analysis
    }
    
    return render_template('soil.html', **context)

@main_bp.route('/recommendations')
@login_required
def recommendations():
    """Render the recommendations page"""
    # Initialize default data
    farm_id = request.args.get('farm_id', '1')
    
    # Get farm location (default to Kenya)
    farm_location = (0.0236, 37.9062)  # Kenya coordinates
    
    # Get weather forecast
    weather_forecast = weather_forecaster.get_weather_forecast(farm_location[0], farm_location[1], days=7)
    
    # Get soil data
    soil_data = soil_sensor_manager.get_sensor_data(f"sensor_{farm_id}")
    
    # Generate recommendations
    all_recommendations = []
    
    # Add crop recommendations
    crop_recommendations = [
        {
            "category": "irrigation",
            "description": "Irrigation recommended within the next 48 hours. Soil moisture is below optimal levels.",
            "priority": "medium"
        },
        {
            "category": "fertilization",
            "description": "Apply nitrogen-rich fertilizer to address deficiency detected in soil samples.",
            "priority": "high"
        },
        {
            "category": "pest_control",
            "description": "Monitor for fall armyworm infestation. Current conditions favor pest development.",
            "priority": "medium"
        },
        {
            "category": "crop_health",
            "description": "Areas of poor crop health detected in southeastern section of field. Investigate possible causes.",
            "priority": "high"
        },
        {
            "category": "planting",
            "description": "Optimal planting conditions expected in 7-10 days for maize.",
            "priority": "low"
        }
    ]
    
    all_recommendations.extend(crop_recommendations)
    
    # Sort recommendations by priority
    priority_order = {"high": 0, "medium": 1, "low": 2}
    all_recommendations.sort(key=lambda x: priority_order[x["priority"]])
    
    # Prepare data for the recommendations page
    context = {
        'farm_id': farm_id,
        'recommendations': all_recommendations,
        'now': datetime.now()  # Add current datetime for date calculations in template
    }
    
    return render_template('recommendations.html', **context)

@main_bp.route('/community')
@login_required
def community():
    """Render the community page for farmer interaction"""
    # Get all community posts, ordered by most recent
    from models import CommunityPost, User, PostComment
    
    # Current datetime for template
    now = datetime.now()
    
    # Get query parameters for filtering
    category = request.args.get('category', 'all')
    sort_by = request.args.get('sort_by', 'recent')
    
    # Sample posts for demonstration
    sample_posts = [
        {
            'id': 1,
            'user': {
                'id': 1,
                'username': 'JohnFarmer',
                'farm_name': 'Green Valley Farm'
            },
            'title': 'Successful Maize Harvest Using Climate-Smart Techniques',
            'content': 'I had a great maize harvest this season using the irrigation recommendations from the platform. The soil moisture sensors helped me save water while maximizing yield.',
            'image_url': 'https://images.unsplash.com/photo-1471193945509-9ad0617afabf?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1170&q=80',
            'category': 'success_story',
            'location': 'Nakuru, Kenya',
            'likes': 24,
            'comment_count': 8,
            'created_at': datetime.now() - timedelta(days=2)
        },
        {
            'id': 2,
            'user': {
                'id': 2,
                'username': 'MaryHarvest',
                'farm_name': 'Sunrise Farms'
            },
            'title': 'Question about Rice Paddy Irrigation',
            'content': 'Has anyone used the platform for rice paddy management? I\'m curious about the accuracy of the water stress detection for flooded fields.',
            'image_url': 'https://images.unsplash.com/photo-1596473537025-319df114df00?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1170&q=80',
            'category': 'question',
            'location': 'Mwea, Kenya',
            'likes': 8,
            'comment_count': 12,
            'created_at': datetime.now() - timedelta(days=5)
        },
        {
            'id': 3,
            'user': {
                'id': 3,
                'username': 'DavidAgritech',
                'farm_name': 'Tech Farms'
            },
            'title': 'Workshop on Soil Sensor Installation - This Weekend',
            'content': 'I\'m hosting a workshop this weekend on how to properly install and maintain soil sensors for optimal readings. Join us at Nairobi Agricultural Training Center.',
            'image_url': 'https://images.unsplash.com/photo-1628352081066-3a8a64cd8014?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1008&q=80',
            'category': 'event',
            'location': 'Nairobi, Kenya',
            'likes': 32,
            'comment_count': 15,
            'created_at': datetime.now() - timedelta(days=1)
        },
        {
            'id': 4,
            'user': {
                'id': 4,
                'username': 'SarahOrganic',
                'farm_name': 'Nature\'s Bounty'
            },
            'title': 'Organic Pest Control Techniques for Climate Change',
            'content': 'With changing climate patterns, I\'ve found these organic pest control methods to be effective. The satellite pest risk assessment combined with these techniques has improved my crop health dramatically.',
            'image_url': 'https://images.unsplash.com/photo-1571930722033-277cbd896797?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1130&q=80',
            'category': 'knowledge_sharing',
            'location': 'Machakos, Kenya',
            'likes': 47,
            'comment_count': 23,
            'created_at': datetime.now() - timedelta(days=7)
        },
        {
            'id': 5,
            'user': {
                'id': 5,
                'username': 'MichaelMarket',
                'farm_name': 'Harvest Market Farms'
            },
            'title': 'Fresh Tomatoes and Onions Available - Direct from Farm',
            'content': 'We have fresh, pesticide-free tomatoes and onions available for sale. Grown using climate-smart techniques with optimal irrigation based on soil moisture data.',
            'image_url': 'https://images.unsplash.com/photo-1467825487722-2a7c4cd62e75?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1170&q=80',
            'category': 'market',
            'location': 'Kisumu, Kenya',
            'likes': 18,
            'comment_count': 5,
            'created_at': datetime.now() - timedelta(days=3)
        }
    ]
    
    # Filter posts by category if specified
    if category != 'all':
        filtered_posts = [post for post in sample_posts if post['category'] == category]
    else:
        filtered_posts = sample_posts
    
    # Sort posts by specified criteria
    if sort_by == 'popular':
        filtered_posts.sort(key=lambda x: x['likes'], reverse=True)
    elif sort_by == 'comments':
        filtered_posts.sort(key=lambda x: x['comment_count'], reverse=True)
    else:  # recent
        filtered_posts.sort(key=lambda x: x['created_at'], reverse=True)
    
    # Sample categories for the community
    categories = {
        'all': 'All Posts',
        'knowledge_sharing': 'Knowledge Sharing',
        'question': 'Questions',
        'market': 'Marketplace',
        'event': 'Events',
        'success_story': 'Success Stories'
    }
    
    # Prepare context for the community page
    context = {
        'posts': filtered_posts,
        'categories': categories,
        'selected_category': category,
        'sort_by': sort_by,
        'now': now,
        'user': {
            'id': 1,
            'username': 'CurrentUser',
            'farm_name': 'Your Farm'
        }
    }
    
    return render_template('community.html', **context)
    
@main_bp.route('/messages')
@login_required
def messages():
    """Render the messaging page for user communication"""
    # Current datetime for template
    now = datetime.now()
    
    # In a real implementation, this would fetch conversations from the database
    
    return render_template('messages.html', now=now)

@main_bp.route('/messages/<int:seller_id>')
@login_required
def messages_with_seller(seller_id):
    """Render the messaging page with a specific seller"""
    # Current datetime for template
    now = datetime.now()
    
    # Get the item_id from query parameters (if it exists)
    item_id = request.args.get('item_id')
    
    # In a real implementation, this would fetch the conversation with the seller
    # and the marketplace item information if item_id is provided
    
    # Setup context with all necessary data
    context = {
        'now': now,
        'seller_id': seller_id
    }
    
    # Add item_id to context if it exists
    if item_id:
        # In a real implementation, fetch the item details from the database
        context['item_id'] = item_id
        # Mock item details for demonstration
        context['item'] = {
            'id': item_id,
            'title': 'Tomato Seedlings - Roma Variety',
            'price': '$5.00 per tray',
            'image_url': 'https://via.placeholder.com/60'
        }
    
    return render_template('messages.html', **context)

@main_bp.route('/messages/item/<int:item_id>')
@login_required
def messages_about_item(item_id):
    """Redirect to messages with the seller of a specific marketplace item"""
    # In a real implementation, this would fetch the item and its seller from the database
    
    # For demonstration, we'll use a simple mapping of items to sellers
    item_seller_map = {
        1: 1,  # Item 1 belongs to Seller 1
        2: 3,  # Item 2 belongs to Seller 3
        3: 5,  # Item 3 belongs to Seller 5
        4: 4   # Item 4 belongs to Seller 4
    }
    
    # Get the seller ID for this item
    seller_id = item_seller_map.get(item_id, 1)  # Default to seller 1 if not found
    
    # Redirect to the messages page with the seller, passing the item_id as a query parameter
    return redirect(url_for('main.messages_with_seller', seller_id=seller_id, item_id=item_id))

@main_bp.route('/marketplace')
@login_required
def marketplace():
    """Render the marketplace page for buying/selling agricultural products"""
    # Current datetime for template
    now = datetime.now()
    
    # Get query parameters for filtering
    category = request.args.get('category', 'all')
    sort_by = request.args.get('sort_by', 'recent')
    
    # Sample marketplace items
    sample_items = [
        {
            'id': 1,
            'user': {
                'id': 1,
                'username': 'JohnFarmer',
                'farm_name': 'Green Valley Farm'
            },
            'title': 'Certified Maize Seeds - Climate Resilient Variety',
            'description': 'Drought-resistant maize seeds perfect for regions with inconsistent rainfall. These seeds have been tested with our climate prediction models.',
            'category': 'seeds',
            'price': 1250.00,
            'currency': 'KES',
            'location': 'Nakuru, Kenya',
            'image_url': 'https://images.unsplash.com/photo-1557636222-d6924f30a4e4?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1170&q=80',
            'status': 'available',
            'created_at': datetime.now() - timedelta(days=2)
        },
        {
            'id': 2,
            'user': {
                'id': 3,
                'username': 'DavidAgritech',
                'farm_name': 'Tech Farms'
            },
            'title': 'Soil Moisture Sensors - Compatible with Platform',
            'description': 'Professional-grade soil moisture sensors that connect directly to your climate-smart agriculture platform for real-time soil data.',
            'category': 'equipment',
            'price': 8500.00,
            'currency': 'KES',
            'location': 'Nairobi, Kenya',
            'image_url': 'https://images.unsplash.com/photo-1604047421986-ad5374916f0f?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1170&q=80',
            'status': 'available',
            'created_at': datetime.now() - timedelta(days=5)
        },
        {
            'id': 3,
            'user': {
                'id': 5,
                'username': 'MichaelMarket',
                'farm_name': 'Harvest Market Farms'
            },
            'title': 'Fresh Organic Tomatoes - Wholesale Quantities',
            'description': 'Pesticide-free tomatoes grown with precision irrigation based on soil moisture data. Available in wholesale quantities.',
            'category': 'produce',
            'price': 120.00,
            'currency': 'KES',
            'location': 'Kisumu, Kenya',
            'image_url': 'https://images.unsplash.com/photo-1561136594-7f68413baa99?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1170&q=80',
            'status': 'available',
            'created_at': datetime.now() - timedelta(days=1)
        },
        {
            'id': 4,
            'user': {
                'id': 4,
                'username': 'SarahOrganic',
                'farm_name': 'Nature\'s Bounty'
            },
            'title': 'Precision Farming Consultation Service',
            'description': 'Offering consultation services for setting up precision farming systems, including sensor placement and data interpretation.',
            'category': 'service',
            'price': 5000.00,
            'currency': 'KES',
            'location': 'Machakos, Kenya',
            'image_url': 'https://images.unsplash.com/photo-1631464326823-ef50db1575ef?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1170&q=80',
            'status': 'available',
            'created_at': datetime.now() - timedelta(days=4)
        }
    ]
    
    # Filter items by category if specified
    if category != 'all':
        filtered_items = [item for item in sample_items if item['category'] == category]
    else:
        filtered_items = sample_items
    
    # Sort items by specified criteria
    if sort_by == 'price_asc':
        filtered_items.sort(key=lambda x: x['price'])
    elif sort_by == 'price_desc':
        filtered_items.sort(key=lambda x: x['price'], reverse=True)
    else:  # recent
        filtered_items.sort(key=lambda x: x['created_at'], reverse=True)
    
    # Sample categories for the marketplace
    categories = {
        'all': 'All Items',
        'seeds': 'Seeds & Plants',
        'equipment': 'Equipment & Tools',
        'produce': 'Farm Produce',
        'service': 'Services'
    }
    
    # Prepare context for the marketplace page
    context = {
        'items': filtered_items,
        'categories': categories,
        'selected_category': category,
        'sort_by': sort_by,
        'now': now,
        'user': {
            'id': 1,
            'username': 'CurrentUser',
            'farm_name': 'Your Farm'
        }
    }
    
    return render_template('marketplace.html', **context)

@main_bp.route('/report-fraud', methods=['GET', 'POST'])
@login_required
def report_fraud():
    """Handle fraud reporting"""
    if request.method == 'POST':
        # Process form submission
        report_type = request.form.get('report_type')
        user_reported = request.form.get('user_reported')
        transaction_date = request.form.get('transaction_date')
        transaction_id = request.form.get('transaction_id')
        amount = request.form.get('amount')
        description = request.form.get('description')
        contact_phone = request.form.get('contact_phone')
        preferred_contact = request.form.get('preferred_contact')
        
        # Process file uploads if present
        evidence_files = request.files.getlist('evidence')
        
        # In a real implementation, this would be stored in a database
        # and potentially forwarded to authorities
        
        # For demonstration, just show a success message
        success = "Your fraud report has been submitted successfully. Our team will review it and may contact you for additional information."
        return render_template('report_fraud.html', success=success)
    
    # GET request - display fraud reporting form
    return render_template('report_fraud.html')

@main_bp.route('/create-listing', methods=['POST'])
@login_required
def create_listing():
    """Handle creating a new marketplace listing"""
    if request.method == 'POST':
        # Process form submission
        title = request.form.get('title')
        category = request.form.get('category')
        price = request.form.get('price')
        currency = request.form.get('currency')
        description = request.form.get('description')
        location = request.form.get('location')
        
        # Process images
        images = request.files.getlist('images')
        
        # In a real implementation, validate and save to database
        # For now, return success JSON response
        return jsonify({'success': True, 'message': 'Listing created successfully'})

@main_bp.route('/settings')
@login_required
def settings():
    """Render the settings page"""
    # Get supported languages from config
    supported_languages = {
        'en': 'English',
        'fr': 'French',
        'sw': 'Swahili',
        'ha': 'Hausa',
        'yo': 'Yoruba',
        'am': 'Amharic',
        'ar': 'Arabic'
    }
    
    # Get current language (default to English)
    current_language = session.get('language', 'en')
    
    # Prepare data for the settings page
    context = {
        'supported_languages': supported_languages,
        'current_language': current_language
    }
    
    return render_template('settings.html', **context)

@main_bp.route('/set_language', methods=['POST'])
@login_required
def set_language():
    """Set the user's preferred language"""
    language = request.form.get('language', 'en')
    session['language'] = language
    
    # Redirect back to the referring page
    return redirect(request.referrer or url_for('main.dashboard'))

def get_sample_recommendations(farm_id):
    """Get sample recommendations for the dashboard"""
    return [
        {
            "category": "irrigation",
            "description": "Irrigation recommended within the next 48 hours. Soil moisture is below optimal levels.",
            "priority": "medium"
        },
        {
            "category": "fertilization",
            "description": "Apply nitrogen-rich fertilizer to address deficiency detected in soil samples.",
            "priority": "high"
        },
        {
            "category": "pest_control",
            "description": "Monitor for fall armyworm infestation. Current conditions favor pest development.",
            "priority": "medium"
        }
    ]

@main_bp.route('/learning')
@login_required
def learning_dashboard():
    """Render the learning dashboard with all available modules"""
    # Get user's learning progress
    # In a real application, this would be fetched from a database
    
    # Mock completed modules data
    completed_modules = 2
    user_points = 240
    badges_earned = 5
    
    # Mock current module data
    current_module_name = "Soil Health Fundamentals"
    current_module_progress = 75
    
    # Prepare data for the learning dashboard
    context = {
        'completed_modules': completed_modules,
        'user_points': user_points,
        'badges_earned': badges_earned,
        'current_module_name': current_module_name,
        'current_module_progress': current_module_progress
    }
    
    return render_template('learning/dashboard.html', **context)

@main_bp.route('/learning/module/<int:module_id>')
@login_required
def learning_module(module_id):
    """Render a specific learning module"""
    # In a real application, module data would be fetched from the database
    
    # Sample module data
    modules = {
        1: {
            'id': 1,
            'title': 'Soil Health Fundamentals',
            'description': 'Learn about soil composition, testing methods, and strategies to improve soil health for optimal crop growth.',
            'difficulty': 'Intermediate',
            'points': 100,
            'lessons': [
                {'id': 1, 'title': 'Introduction to Soil Science', 'completed': True},
                {'id': 2, 'title': 'Soil Composition and Structure', 'completed': True},
                {'id': 3, 'title': 'Soil pH and Nutrient Availability', 'completed': True},
                {'id': 4, 'title': 'Soil Organic Matter', 'completed': True},
                {'id': 5, 'title': 'Soil Testing Methods', 'completed': True},
                {'id': 6, 'title': 'Interpreting Soil Test Results', 'completed': False},
                {'id': 7, 'title': 'Soil Health Improvement Strategies', 'completed': False},
                {'id': 8, 'title': 'Case Studies: Successful Soil Management', 'completed': False}
            ],
            'progress': 75,
            'next_lesson_id': 6
        },
        2: {
            'id': 2,
            'title': 'Water Conservation Techniques',
            'description': 'Master efficient irrigation methods and water management strategies to conserve water while maintaining crop health.',
            'difficulty': 'Beginner',
            'points': 75,
            'lessons': [
                {'id': 1, 'title': 'Water Cycle and Agriculture', 'completed': True},
                {'id': 2, 'title': 'Water Requirements of Different Crops', 'completed': True},
                {'id': 3, 'title': 'Irrigation Systems Overview', 'completed': True},
                {'id': 4, 'title': 'Drip Irrigation Techniques', 'completed': True},
                {'id': 5, 'title': 'Rainwater Harvesting', 'completed': True},
                {'id': 6, 'title': 'Soil Moisture Conservation', 'completed': True}
            ],
            'progress': 100,
            'next_lesson_id': None
        }
    }
    
    # Check if the requested module exists
    if module_id not in modules:
        flash('Module not found', 'error')
        return redirect(url_for('main.learning_dashboard'))
    
    module = modules[module_id]
    
    # Prepare context data
    context = {
        'module': module
    }
    
    return render_template('learning/module.html', **context)

@main_bp.route('/learning/lesson/<int:module_id>/<int:lesson_id>')
@login_required
def learning_lesson(module_id, lesson_id):
    """Render a specific lesson within a learning module"""
    # In a real application, lesson data would be fetched from the database
    
    # Sample lesson content
    lessons = {
        # Module 1, Lesson 6
        (1, 6): {
            'id': 6,
            'module_id': 1,
            'title': 'Interpreting Soil Test Results',
            'content': """
                <h2>Interpreting Soil Test Results</h2>
                <p>In this lesson, you will learn how to interpret soil test results and make informed decisions about soil amendments and fertilizers based on these results.</p>
                
                <h3>Key Learning Objectives:</h3>
                <ul>
                    <li>Understand the different components of a soil test report</li>
                    <li>Interpret soil nutrient levels (N, P, K, and micronutrients)</li>
                    <li>Analyze soil pH and soil organic matter results</li>
                    <li>Develop appropriate soil amendment plans based on test results</li>
                </ul>
                
                <h3>Soil Test Report Components</h3>
                <p>A typical soil test report includes:</p>
                <ul>
                    <li>Soil pH</li>
                    <li>Soil organic matter content</li>
                    <li>Macronutrient levels (N, P, K)</li>
                    <li>Secondary nutrients (Ca, Mg, S)</li>
                    <li>Micronutrient levels (Zn, Mn, Fe, Cu, B)</li>
                    <li>Cation exchange capacity (CEC)</li>
                    <li>Recommendations for amendments</li>
                </ul>
                
                <h3>Interpreting Nutrient Levels</h3>
                <p>Nutrient levels are typically reported in parts per million (ppm) or kg/ha. The optimal ranges for different crops may vary, but general guidelines include:</p>
                
                <table class="table table-bordered">
                    <thead>
                        <tr>
                            <th>Nutrient</th>
                            <th>Low</th>
                            <th>Medium</th>
                            <th>Optimal</th>
                            <th>High</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td>Nitrogen (N)</td>
                            <td>&lt;10 ppm</td>
                            <td>10-20 ppm</td>
                            <td>20-30 ppm</td>
                            <td>&gt;30 ppm</td>
                        </tr>
                        <tr>
                            <td>Phosphorus (P)</td>
                            <td>&lt;15 ppm</td>
                            <td>15-30 ppm</td>
                            <td>30-60 ppm</td>
                            <td>&gt;60 ppm</td>
                        </tr>
                        <tr>
                            <td>Potassium (K)</td>
                            <td>&lt;100 ppm</td>
                            <td>100-150 ppm</td>
                            <td>150-250 ppm</td>
                            <td>&gt;250 ppm</td>
                        </tr>
                    </tbody>
                </table>
                
                <h3>Practice Exercise</h3>
                <p>Using the sample soil test report provided below, identify which nutrients are deficient and which are at optimal levels:</p>
                
                <div class="card mb-4">
                    <div class="card-header">Sample Soil Test Report</div>
                    <div class="card-body">
                        <p><strong>pH:</strong> 6.2</p>
                        <p><strong>Organic Matter:</strong> 2.1%</p>
                        <p><strong>Nitrogen (N):</strong> 12 ppm</p>
                        <p><strong>Phosphorus (P):</strong> 8 ppm</p>
                        <p><strong>Potassium (K):</strong> 180 ppm</p>
                        <p><strong>Calcium (Ca):</strong> 1200 ppm</p>
                        <p><strong>Magnesium (Mg):</strong> 150 ppm</p>
                        <p><strong>Zinc (Zn):</strong> 0.8 ppm</p>
                    </div>
                </div>
                
                <h3>Next Steps</h3>
                <p>After completing this lesson, you should be able to analyze your own soil test results and develop appropriate amendment strategies for your farm.</p>
            """,
            'is_completed': False,
            'next_lesson_id': 7,
            'quiz': {
                'id': 6,
                'questions': [
                    {
                        'id': 1,
                        'question': 'What does a soil pH of 5.5 indicate?',
                        'options': [
                            'Alkaline soil',
                            'Neutral soil',
                            'Acidic soil',
                            'Cannot be determined from pH alone'
                        ],
                        'correct_answer': 2  # 0-indexed, so 2 = "Acidic soil"
                    },
                    {
                        'id': 2,
                        'question': 'Based on the sample report, which nutrient is most deficient?',
                        'options': [
                            'Nitrogen',
                            'Phosphorus',
                            'Potassium',
                            'Calcium'
                        ],
                        'correct_answer': 1  # 0-indexed, so 1 = "Phosphorus"
                    }
                ]
            }
        }
    }
    
    # Check if the requested lesson exists
    if (module_id, lesson_id) not in lessons:
        flash('Lesson not found', 'error')
        return redirect(url_for('main.learning_module', module_id=module_id))
    
    lesson = lessons[(module_id, lesson_id)]
    
    # Prepare context data
    context = {
        'lesson': lesson
    }
    
    return render_template('learning/lesson.html', **context)

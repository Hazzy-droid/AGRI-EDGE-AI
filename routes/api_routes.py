import os
import logging
from flask import Blueprint, request, jsonify, current_app
from datetime import datetime, timedelta
import json

from utils.satellite_processing import SatelliteProcessor
from utils.weather_forecasting import WeatherForecaster
from utils.soil_sensor import SoilSensorManager
from utils.data_fusion import DataFusionEngine
from ai_models.edge_models import EdgeModelManager
from ai_models.model_utils import preprocess_satellite_data, preprocess_weather_data, preprocess_soil_data, combine_features

logger = logging.getLogger(__name__)

# Create blueprint
api_bp = Blueprint('api', __name__)

# Initialize utilities
satellite_processor = SatelliteProcessor()
weather_forecaster = WeatherForecaster()
soil_sensor_manager = SoilSensorManager()
data_fusion_engine = DataFusionEngine()
edge_model_manager = EdgeModelManager()

@api_bp.route('/satellite_data', methods=['GET'])
def get_satellite_data():
    """API endpoint to get satellite data for a farm"""
    try:
        # Get parameters
        farm_id = request.args.get('farm_id', '1')
        bbox = request.args.get('bbox')
        if bbox:
            bbox = [float(x) for x in bbox.split(',')]
        else:
            # Default bbox for Kenya
            bbox = [36.0, -1.0, 38.0, 1.0]
            
        date_from = request.args.get('date_from', (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d'))
        date_to = request.args.get('date_to', datetime.now().strftime('%Y-%m-%d'))
        
        # Get satellite image
        image_data = satellite_processor.get_satellite_image(bbox, date_from, date_to)
        
        # Get historical NDVI series
        ndvi_series = satellite_processor.get_historical_ndvi_series(bbox, date_from, date_to)
        
        # Calculate current NDVI (using latest value from series if available)
        current_ndvi = ndvi_series[-1]['average_ndvi'] if ndvi_series else 0.5
        
        # Analyze crop health based on NDVI
        mock_ndvi_values = np.array([current_ndvi] * 100)  # Create array for analysis
        crop_health = satellite_processor.analyze_crop_health(mock_ndvi_values)
        
        # Create response
        response = {
            'farm_id': farm_id,
            'bbox': bbox,
            'date_from': date_from,
            'date_to': date_to,
            'ndvi_series': ndvi_series,
            'current_ndvi': current_ndvi,
            'crop_health': crop_health
        }
        
        return jsonify(response)
    
    except Exception as e:
        logger.error(f"Error getting satellite data: {str(e)}")
        return jsonify({'error': str(e)}), 500

@api_bp.route('/weather_data', methods=['GET'])
def get_weather_data():
    """API endpoint to get weather data for a location"""
    try:
        # Get parameters
        lat = request.args.get('lat', '0.0236')  # Default to Kenya
        lon = request.args.get('lon', '37.9062')  # Default to Kenya
        
        # Convert to float
        lat = float(lat)
        lon = float(lon)
        
        # Get current weather
        current_weather = weather_forecaster.get_current_weather(lat, lon)
        
        # Get daily forecast
        daily_forecast = weather_forecaster.get_weather_forecast(lat, lon, days=7)
        
        # Get hourly forecast
        hourly_forecast = weather_forecaster.get_hourly_forecast(lat, lon, hours=24)
        
        # Create response
        response = {
            'location': {'lat': lat, 'lon': lon},
            'current_weather': current_weather,
            'daily_forecast': daily_forecast,
            'hourly_forecast': hourly_forecast
        }
        
        return jsonify(response)
    
    except Exception as e:
        logger.error(f"Error getting weather data: {str(e)}")
        return jsonify({'error': str(e)}), 500

@api_bp.route('/soil_data', methods=['GET'])
def get_soil_data():
    """API endpoint to get soil sensor data"""
    try:
        # Get parameters
        sensor_id = request.args.get('sensor_id', 'sensor_1')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        # Get soil data
        soil_data = soil_sensor_manager.get_sensor_data(sensor_id, start_date, end_date)
        
        return jsonify(soil_data)
    
    except Exception as e:
        logger.error(f"Error getting soil data: {str(e)}")
        return jsonify({'error': str(e)}), 500

@api_bp.route('/soil_analysis', methods=['GET'])
def get_soil_analysis():
    """API endpoint to get soil data analysis"""
    try:
        # Get parameters
        sensor_id = request.args.get('sensor_id', 'sensor_1')
        crop_type = request.args.get('crop_type', 'maize')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        # Get soil data
        soil_data = soil_sensor_manager.get_sensor_data(sensor_id, start_date, end_date)
        
        # Analyze soil moisture
        moisture_analysis = soil_sensor_manager.analyze_soil_moisture(soil_data, crop_type)
        
        # Analyze soil fertility
        fertility_analysis = soil_sensor_manager.analyze_soil_fertility(soil_data, crop_type)
        
        # Create response
        response = {
            'sensor_id': sensor_id,
            'crop_type': crop_type,
            'moisture_analysis': moisture_analysis,
            'fertility_analysis': fertility_analysis
        }
        
        return jsonify(response)
    
    except Exception as e:
        logger.error(f"Error analyzing soil data: {str(e)}")
        return jsonify({'error': str(e)}), 500

@api_bp.route('/planting_recommendation', methods=['GET'])
def get_planting_recommendation():
    """API endpoint to get planting recommendations based on weather trends"""
    try:
        # Get parameters
        lat = request.args.get('lat', '0.0236')  # Default to Kenya
        lon = request.args.get('lon', '37.9062')  # Default to Kenya
        crop_types = request.args.get('crop_types', 'maize,rice,sorghum,millet,cassava')
        
        # Convert to float
        lat = float(lat)
        lon = float(lon)
        
        # Split crop types
        crop_types = crop_types.split(',')
        
        # Generate planting recommendation
        recommendation = weather_forecaster.generate_planting_recommendation((lat, lon), crop_types)
        
        return jsonify(recommendation)
    
    except Exception as e:
        logger.error(f"Error getting planting recommendation: {str(e)}")
        return jsonify({'error': str(e)}), 500

@api_bp.route('/irrigation_recommendation', methods=['GET'])
def get_irrigation_recommendation():
    """API endpoint to get irrigation recommendations"""
    try:
        # Get parameters
        lat = request.args.get('lat', '0.0236')  # Default to Kenya
        lon = request.args.get('lon', '37.9062')  # Default to Kenya
        soil_moisture = request.args.get('soil_moisture', '50')
        crop_type = request.args.get('crop_type', 'maize')
        
        # Convert to float
        lat = float(lat)
        lon = float(lon)
        soil_moisture = float(soil_moisture)
        
        # Get weather forecast
        weather_forecast = weather_forecaster.get_weather_forecast(lat, lon)
        
        # Analyze irrigation needs
        irrigation_recommendation = weather_forecaster.analyze_irrigation_needs(
            weather_forecast,
            soil_moisture,
            crop_type
        )
        
        return jsonify(irrigation_recommendation)
    
    except Exception as e:
        logger.error(f"Error getting irrigation recommendation: {str(e)}")
        return jsonify({'error': str(e)}), 500

@api_bp.route('/yield_prediction', methods=['GET'])
def get_yield_prediction():
    """API endpoint to predict crop yield"""
    try:
        # Get parameters
        farm_id = request.args.get('farm_id', '1')
        crop_type = request.args.get('crop_type', 'maize')
        lat = request.args.get('lat', '0.0236')  # Default to Kenya
        lon = request.args.get('lon', '37.9062')  # Default to Kenya
        
        # Convert to float
        lat = float(lat)
        lon = float(lon)
        
        # Get NDVI time series (mock or real data)
        bbox = [lon-0.1, lat-0.1, lon+0.1, lat+0.1]
        date_from = (datetime.now() - timedelta(days=90)).strftime('%Y-%m-%d')
        date_to = datetime.now().strftime('%Y-%m-%d')
        
        ndvi_series = satellite_processor.get_historical_ndvi_series(bbox, date_from, date_to)
        ndvi_values = [item['average_ndvi'] for item in ndvi_series] if ndvi_series else [0.6, 0.65, 0.7]
        
        # Get weather data
        weather_data = weather_forecaster.get_weather_forecast(lat, lon)[0]  # Use first day
        
        # Get soil data
        soil_data = soil_sensor_manager.get_sensor_data(f"sensor_{farm_id}")['data'][-1]  # Use latest data
        
        # Predict yield
        yield_prediction = edge_model_manager.predict_yield(
            ndvi_values,
            soil_data,
            weather_data,
            crop_type
        )
        
        return jsonify(yield_prediction)
    
    except Exception as e:
        logger.error(f"Error predicting yield: {str(e)}")
        return jsonify({'error': str(e)}), 500

@api_bp.route('/pest_disease_risk', methods=['GET'])
def get_pest_disease_risk():
    """API endpoint to get pest and disease risk assessment"""
    try:
        # Get parameters
        farm_id = request.args.get('farm_id', '1')
        crop_type = request.args.get('crop_type', 'maize')
        lat = request.args.get('lat', '0.0236')  # Default to Kenya
        lon = request.args.get('lon', '37.9062')  # Default to Kenya
        
        # Convert to float
        lat = float(lat)
        lon = float(lon)
        
        # Get weather forecast
        weather_forecast = weather_forecaster.get_weather_forecast(lat, lon)
        
        # Get current NDVI (mock or real data)
        ndvi = 0.65  # Default value
        
        # Predict pest/disease risk
        risk_assessment = edge_model_manager.predict_pest_disease_risk(
            weather_forecast,
            ndvi,
            crop_type
        )
        
        return jsonify(risk_assessment)
    
    except Exception as e:
        logger.error(f"Error assessing pest/disease risk: {str(e)}")
        return jsonify({'error': str(e)}), 500

@api_bp.route('/fused_recommendations', methods=['GET'])
def get_fused_recommendations():
    """API endpoint to get fused recommendations from multiple data sources"""
    try:
        # Get parameters
        farm_id = request.args.get('farm_id', '1')
        crop_type = request.args.get('crop_type', 'maize')
        lat = request.args.get('lat', '0.0236')  # Default to Kenya
        lon = request.args.get('lon', '37.9062')  # Default to Kenya
        
        # Convert to float
        lat = float(lat)
        lon = float(lon)
        
        # Get satellite data
        bbox = [lon-0.1, lat-0.1, lon+0.1, lat+0.1]
        date_from = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')
        date_to = datetime.now().strftime('%Y-%m-%d')
        
        ndvi_series = satellite_processor.get_historical_ndvi_series(bbox, date_from, date_to)
        current_ndvi = ndvi_series[-1]['average_ndvi'] if ndvi_series else 0.65
        
        mock_ndvi_values = np.array([current_ndvi] * 100)  # Create array for analysis
        crop_health = satellite_processor.analyze_crop_health(mock_ndvi_values)
        
        satellite_data = {
            'average_ndvi': current_ndvi,
            'ndvi_series': ndvi_series,
            'overall_status': crop_health['overall_status']
        }
        
        # Get weather data
        weather_data = weather_forecaster.get_weather_forecast(lat, lon)[0]  # Use first day
        
        # Get soil data
        soil_data = soil_sensor_manager.get_sensor_data(f"sensor_{farm_id}")['data'][-1]  # Use latest data
        
        # Fuse data
        fused_data = data_fusion_engine.fuse_satellite_weather_soil(
            satellite_data,
            weather_data,
            soil_data
        )
        
        # Generate crop recommendations
        recommendations = data_fusion_engine.generate_crop_recommendations(
            fused_data,
            crop_type
        )
        
        # Create response
        response = {
            'farm_id': farm_id,
            'crop_type': crop_type,
            'fused_data': fused_data,
            'recommendations': recommendations
        }
        
        return jsonify(response)
    
    except Exception as e:
        logger.error(f"Error generating fused recommendations: {str(e)}")
        return jsonify({'error': str(e)}), 500

@api_bp.route('/chat', methods=['POST'])
def chat():
    """API endpoint for the AI chatbot assistant"""
    data = request.get_json()
    
    if not data:
        return jsonify({
            'success': False,
            'error': 'Invalid request data'
        }), 400
    
    query = data.get('query')
    context = data.get('context', 'general_farming')
    conversation_history = data.get('conversation_history', [])
    
    if not query:
        return jsonify({
            'success': False,
            'error': 'Query is required'
        }), 400
        
    # Get AI response
    from utils.ai_assistant import get_ai_response
    
    # Log user query for monitoring (in a real app, might be stored in a database)
    current_app.logger.info(f"AI Assistant Query: {query} (Context: {context})")
    
    try:
        response = get_ai_response(query, context, conversation_history)
        return jsonify(response)
    except Exception as e:
        current_app.logger.error(f"Error getting AI response: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'An error occurred while processing your request.'
        }), 500

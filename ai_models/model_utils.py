import os
import logging
import numpy as np
import json
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

def preprocess_satellite_data(satellite_data):
    """
    Preprocess satellite data for machine learning models
    
    Args:
        satellite_data (dict): Raw satellite data
        
    Returns:
        dict: Preprocessed satellite data
    """
    try:
        # Extract relevant features
        features = {}
        
        # Extract NDVI time series if available
        if "ndvi_series" in satellite_data:
            features["ndvi_values"] = [item["average_ndvi"] for item in satellite_data["ndvi_series"]]
            features["ndvi_dates"] = [item["date"] for item in satellite_data["ndvi_series"]]
            
            # Calculate NDVI statistics
            features["mean_ndvi"] = np.mean(features["ndvi_values"])
            features["min_ndvi"] = np.min(features["ndvi_values"])
            features["max_ndvi"] = np.max(features["ndvi_values"])
            features["std_ndvi"] = np.std(features["ndvi_values"])
            
            # Calculate NDVI trends
            if len(features["ndvi_values"]) > 1:
                # Simple linear regression for trend
                x = np.arange(len(features["ndvi_values"]))
                y = np.array(features["ndvi_values"])
                
                A = np.vstack([x, np.ones(len(x))]).T
                m, c = np.linalg.lstsq(A, y, rcond=None)[0]
                
                features["ndvi_trend"] = m
            else:
                features["ndvi_trend"] = 0
        else:
            # Use single NDVI value if available
            features["mean_ndvi"] = satellite_data.get("average_ndvi", 0)
            features["min_ndvi"] = features["mean_ndvi"]
            features["max_ndvi"] = features["mean_ndvi"]
            features["std_ndvi"] = 0
            features["ndvi_trend"] = 0
            
        return features
        
    except Exception as e:
        logger.error(f"Error preprocessing satellite data: {str(e)}")
        return {}

def preprocess_weather_data(weather_data):
    """
    Preprocess weather data for machine learning models
    
    Args:
        weather_data (dict): Raw weather data
        
    Returns:
        dict: Preprocessed weather data
    """
    try:
        # Extract relevant features
        features = {}
        
        # Handle different weather data formats
        if isinstance(weather_data, list):
            # Daily forecast format
            
            # Calculate temperature statistics
            if "temperature" in weather_data[0]:
                temp_values = []
                
                for day in weather_data:
                    if isinstance(day["temperature"], dict):
                        temp_values.append(day["temperature"].get("day", 0))
                    else:
                        temp_values.append(day["temperature"])
                
                features["mean_temp"] = np.mean(temp_values)
                features["min_temp"] = np.min(temp_values)
                features["max_temp"] = np.max(temp_values)
            
            # Calculate precipitation statistics
            rain_values = [day.get("rain", 0) for day in weather_data]
            features["total_rain"] = np.sum(rain_values)
            features["mean_rain"] = np.mean(rain_values)
            
            # Calculate humidity statistics
            if "humidity" in weather_data[0]:
                humidity_values = [day["humidity"] for day in weather_data]
                features["mean_humidity"] = np.mean(humidity_values)
                features["min_humidity"] = np.min(humidity_values)
                features["max_humidity"] = np.max(humidity_values)
        else:
            # Current weather format
            if "temperature" in weather_data:
                if isinstance(weather_data["temperature"], dict):
                    features["mean_temp"] = weather_data["temperature"].get("day", 0)
                else:
                    features["mean_temp"] = weather_data["temperature"]
                
                features["min_temp"] = features["mean_temp"]
                features["max_temp"] = features["mean_temp"]
            
            features["total_rain"] = weather_data.get("rain", 0)
            features["mean_rain"] = features["total_rain"]
            
            if "humidity" in weather_data:
                features["mean_humidity"] = weather_data["humidity"]
                features["min_humidity"] = features["mean_humidity"]
                features["max_humidity"] = features["mean_humidity"]
                
        return features
        
    except Exception as e:
        logger.error(f"Error preprocessing weather data: {str(e)}")
        return {}

def preprocess_soil_data(soil_data):
    """
    Preprocess soil data for machine learning models
    
    Args:
        soil_data (dict): Raw soil data
        
    Returns:
        dict: Preprocessed soil data
    """
    try:
        # Extract relevant features
        features = {}
        
        # Handle different soil data formats
        if "data" in soil_data and isinstance(soil_data["data"], list):
            # Time series soil data
            
            # Use the most recent soil data point
            latest_data = soil_data["data"][-1]
            
            features["moisture"] = latest_data.get("moisture", 0)
            features["temperature"] = latest_data.get("temperature", 0)
            features["ph"] = latest_data.get("ph", 7)
            features["electrical_conductivity"] = latest_data.get("electrical_conductivity", 0)
            features["nitrogen"] = latest_data.get("nitrogen", 0)
            features["phosphorus"] = latest_data.get("phosphorus", 0)
            features["potassium"] = latest_data.get("potassium", 0)
            
            # Calculate soil moisture statistics
            moisture_values = [item.get("moisture", 0) for item in soil_data["data"]]
            features["mean_moisture"] = np.mean(moisture_values)
            features["min_moisture"] = np.min(moisture_values)
            features["max_moisture"] = np.max(moisture_values)
            features["std_moisture"] = np.std(moisture_values)
            
            # Calculate soil temperature statistics
            temp_values = [item.get("temperature", 0) for item in soil_data["data"]]
            features["mean_soil_temp"] = np.mean(temp_values)
            features["min_soil_temp"] = np.min(temp_values)
            features["max_soil_temp"] = np.max(temp_values)
        else:
            # Single soil data point
            features["moisture"] = soil_data.get("moisture", 0)
            features["temperature"] = soil_data.get("temperature", 0)
            features["ph"] = soil_data.get("ph", 7)
            features["electrical_conductivity"] = soil_data.get("electrical_conductivity", 0)
            features["nitrogen"] = soil_data.get("nitrogen", 0)
            features["phosphorus"] = soil_data.get("phosphorus", 0)
            features["potassium"] = soil_data.get("potassium", 0)
            
            features["mean_moisture"] = features["moisture"]
            features["min_moisture"] = features["moisture"]
            features["max_moisture"] = features["moisture"]
            features["std_moisture"] = 0
            
            features["mean_soil_temp"] = features["temperature"]
            features["min_soil_temp"] = features["temperature"]
            features["max_soil_temp"] = features["temperature"]
                
        return features
        
    except Exception as e:
        logger.error(f"Error preprocessing soil data: {str(e)}")
        return {}

def combine_features(satellite_features, weather_features, soil_features):
    """
    Combine features from different data sources
    
    Args:
        satellite_features (dict): Preprocessed satellite features
        weather_features (dict): Preprocessed weather features
        soil_features (dict): Preprocessed soil features
        
    Returns:
        list: Combined feature vector
    """
    try:
        # Define the feature structure (in a specific order)
        feature_names = [
            # Satellite features
            "mean_ndvi", "min_ndvi", "max_ndvi", "std_ndvi", "ndvi_trend",
            # Weather features
            "mean_temp", "min_temp", "max_temp", "total_rain", "mean_rain",
            "mean_humidity", "min_humidity", "max_humidity",
            # Soil features
            "moisture", "temperature", "ph", "electrical_conductivity",
            "nitrogen", "phosphorus", "potassium",
            "mean_moisture", "min_moisture", "max_moisture", "std_moisture",
            "mean_soil_temp", "min_soil_temp", "max_soil_temp"
        ]
        
        # Combine all features
        all_features = {**satellite_features, **weather_features, **soil_features}
        
        # Create feature vector with default values
        feature_vector = []
        for name in feature_names:
            feature_vector.append(all_features.get(name, 0))
            
        return feature_vector
        
    except Exception as e:
        logger.error(f"Error combining features: {str(e)}")
        return []

def format_recommendation(recommendation_type, recommendation_data):
    """
    Format recommendation data for user presentation
    
    Args:
        recommendation_type (str): Type of recommendation
        recommendation_data (dict): Raw recommendation data
        
    Returns:
        dict: Formatted recommendation
    """
    try:
        formatted = {
            "type": recommendation_type,
            "timestamp": datetime.now().isoformat(),
            "data": recommendation_data
        }
        
        # Add summary based on recommendation type
        if recommendation_type == "yield_prediction":
            formatted["summary"] = f"Predicted yield: {recommendation_data['predicted_yield']} {recommendation_data['yield_unit']} ({recommendation_data['yield_quality']})"
        elif recommendation_type == "irrigation":
            formatted["summary"] = recommendation_data["recommendation"]
        elif recommendation_type == "pest_disease":
            if recommendation_data["overall_risk"] == "High":
                formatted["summary"] = f"High risk of {recommendation_data['specific_risks'][0]['pest_disease']}. Immediate action recommended."
            elif recommendation_data["overall_risk"] == "Medium":
                formatted["summary"] = f"Medium risk of {recommendation_data['specific_risks'][0]['pest_disease']}. Monitor and prepare for treatment."
            else:
                formatted["summary"] = "Low pest/disease risk. Continue regular monitoring."
        
        return formatted
        
    except Exception as e:
        logger.error(f"Error formatting recommendation: {str(e)}")
        return {"type": recommendation_type, "timestamp": datetime.now().isoformat(), "data": recommendation_data}

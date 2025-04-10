import os
import logging
import numpy as np
import pickle
import json
from datetime import datetime

logger = logging.getLogger(__name__)

class EdgeModelManager:
    """Manager class for Edge AI models"""
    
    def __init__(self, model_dir="ai_models/saved_models"):
        self.model_dir = model_dir
        self.logger = logging.getLogger(__name__)
        self.models = {}
        
        # Check if model directory exists, if not create it
        if not os.path.exists(model_dir):
            os.makedirs(model_dir)
            
    def load_model(self, model_name):
        """
        Load a model (simplified version without TensorFlow)
        
        Args:
            model_name (str): Name of the model to load
            
        Returns:
            dict: Model metadata and parameters
        """
        try:
            # For demonstration purposes, we'll use a simplified approach
            # In a real implementation, this would load an actual model file
            
            # Create model parameters based on model_name
            if model_name == "crop_yield":
                model_params = {
                    "type": "yield_prediction",
                    "crops_supported": ["maize", "rice", "sorghum", "millet", "cassava"],
                    "input_features": ["ndvi_time_series", "soil_data", "weather_data"],
                    "version": "1.0"
                }
            elif model_name == "irrigation":
                model_params = {
                    "type": "irrigation_recommendation",
                    "crops_supported": ["maize", "rice", "sorghum", "millet", "cassava"],
                    "input_features": ["soil_moisture", "weather_forecast", "crop_type", "crop_stage"],
                    "version": "1.0"
                }
            elif model_name == "pest_disease":
                model_params = {
                    "type": "pest_disease_risk",
                    "crops_supported": ["maize", "rice", "sorghum", "millet", "cassava"],
                    "input_features": ["weather_forecast", "ndvi", "crop_type"],
                    "version": "1.0"
                }
            else:
                model_params = {
                    "type": "unknown",
                    "version": "1.0"
                }
            
            self.models[model_name] = model_params
            self.logger.info(f"Model {model_name} loaded successfully")
            
            return model_params
            
        except Exception as e:
            self.logger.error(f"Error loading model {model_name}: {str(e)}")
            return None
            
    def predict_yield(self, ndvi_time_series, soil_data, weather_data, crop_type):
        """
        Predict crop yield based on NDVI time series, soil data, and weather data
        
        Args:
            ndvi_time_series (list): List of NDVI values over time
            soil_data (dict): Soil sensor data
            weather_data (dict): Weather data
            crop_type (str): Type of crop
            
        Returns:
            dict: Yield prediction results
        """
        # This is a simplified model for edge deployment
        # In real implementation, this would use an actual TensorFlow Lite model
        
        try:
            # Crop-specific parameters
            crop_params = {
                "maize": {"base_yield": 3.5, "ndvi_weight": 0.6, "soil_weight": 0.2, "weather_weight": 0.2},
                "rice": {"base_yield": 4.0, "ndvi_weight": 0.5, "soil_weight": 0.3, "weather_weight": 0.2},
                "sorghum": {"base_yield": 2.5, "ndvi_weight": 0.5, "soil_weight": 0.2, "weather_weight": 0.3},
                "millet": {"base_yield": 1.5, "ndvi_weight": 0.5, "soil_weight": 0.2, "weather_weight": 0.3},
                "cassava": {"base_yield": 10.0, "ndvi_weight": 0.4, "soil_weight": 0.4, "weather_weight": 0.2},
                "default": {"base_yield": 3.0, "ndvi_weight": 0.5, "soil_weight": 0.25, "weather_weight": 0.25}
            }
            
            # Get parameters for the specified crop
            params = crop_params.get(crop_type.lower(), crop_params["default"])
            
            # Calculate NDVI component
            avg_ndvi = np.mean(ndvi_time_series)
            ndvi_component = (avg_ndvi / 0.7) * params["ndvi_weight"]  # Normalize NDVI to 0-1 range
            
            # Calculate soil component
            soil_moisture = soil_data.get("moisture", 50)
            soil_temp = soil_data.get("temperature", 25)
            nitrogen = soil_data.get("nitrogen", 20)
            phosphorus = soil_data.get("phosphorus", 10)
            potassium = soil_data.get("potassium", 15)
            
            # Normalize soil parameters
            moisture_score = 1.0 - abs((soil_moisture - 60) / 60)
            temp_score = 1.0 - abs((soil_temp - 25) / 25)
            n_score = min(1.0, nitrogen / 30)
            p_score = min(1.0, phosphorus / 15)
            k_score = min(1.0, potassium / 25)
            
            soil_score = (moisture_score + temp_score + n_score + p_score + k_score) / 5
            soil_component = soil_score * params["soil_weight"]
            
            # Calculate weather component
            avg_temp = weather_data.get("temperature", {}).get("day", 25)
            precipitation = weather_data.get("rain", 0)
            humidity = weather_data.get("humidity", 60)
            
            # Normalize weather parameters
            temp_score = 1.0 - abs((avg_temp - 25) / 25)
            rain_score = min(1.0, precipitation / 20)
            humidity_score = 1.0 - abs((humidity - 60) / 60)
            
            weather_score = (temp_score + rain_score + humidity_score) / 3
            weather_component = weather_score * params["weather_weight"]
            
            # Calculate final yield prediction
            yield_factor = ndvi_component + soil_component + weather_component
            base_yield = params["base_yield"]
            predicted_yield = base_yield * yield_factor
            
            # Add some random variation to simulate model uncertainty
            predicted_yield *= (0.9 + 0.2 * np.random.random())
            
            # Determine yield quality based on the predicted yield
            if predicted_yield > base_yield * 1.2:
                quality = "Excellent"
            elif predicted_yield > base_yield:
                quality = "Good"
            elif predicted_yield > base_yield * 0.8:
                quality = "Average"
            else:
                quality = "Poor"
                
            return {
                "crop_type": crop_type,
                "predicted_yield": round(predicted_yield, 2),
                "yield_unit": "tons/hectare",
                "yield_quality": quality,
                "confidence": 0.7,
                "contribution": {
                    "ndvi": round(ndvi_component / yield_factor * 100, 1),
                    "soil": round(soil_component / yield_factor * 100, 1),
                    "weather": round(weather_component / yield_factor * 100, 1)
                }
            }
            
        except Exception as e:
            self.logger.error(f"Error predicting yield: {str(e)}")
            return None
            
    def predict_irrigation_needs(self, soil_moisture, weather_forecast, crop_type, crop_stage):
        """
        Predict irrigation needs based on soil moisture and weather forecast
        
        Args:
            soil_moisture (float): Current soil moisture percentage
            weather_forecast (list): List of daily weather forecasts
            crop_type (str): Type of crop
            crop_stage (str): Growth stage of the crop
            
        Returns:
            dict: Irrigation recommendation
        """
        try:
            # Crop-specific parameters for different growth stages
            crop_params = {
                "maize": {
                    "germination": {"min_moisture": 50, "optimal_moisture": 70, "daily_et": 2.5},
                    "vegetative": {"min_moisture": 45, "optimal_moisture": 65, "daily_et": 4.0},
                    "reproductive": {"min_moisture": 55, "optimal_moisture": 75, "daily_et": 6.0},
                    "maturity": {"min_moisture": 40, "optimal_moisture": 60, "daily_et": 3.0}
                },
                "rice": {
                    "germination": {"min_moisture": 70, "optimal_moisture": 90, "daily_et": 3.0},
                    "vegetative": {"min_moisture": 80, "optimal_moisture": 100, "daily_et": 5.0},
                    "reproductive": {"min_moisture": 80, "optimal_moisture": 100, "daily_et": 6.0},
                    "maturity": {"min_moisture": 70, "optimal_moisture": 90, "daily_et": 4.0}
                },
                "default": {
                    "germination": {"min_moisture": 50, "optimal_moisture": 70, "daily_et": 2.5},
                    "vegetative": {"min_moisture": 45, "optimal_moisture": 65, "daily_et": 4.0},
                    "reproductive": {"min_moisture": 50, "optimal_moisture": 70, "daily_et": 5.0},
                    "maturity": {"min_moisture": 40, "optimal_moisture": 60, "daily_et": 3.0}
                }
            }
            
            # Get parameters for the specified crop and stage
            crop_specifics = crop_params.get(crop_type.lower(), crop_params["default"])
            stage_params = crop_specifics.get(crop_stage.lower(), crop_specifics["vegetative"])
            
            # Calculate expected precipitation from forecast
            expected_rain = sum(day.get("rain", 0) for day in weather_forecast[:3])
            
            # Calculate expected evapotranspiration
            expected_et = stage_params["daily_et"] * 3  # For the next 3 days
            
            # Calculate water deficit
            current_deficit = stage_params["optimal_moisture"] - soil_moisture
            expected_deficit = current_deficit + expected_et - expected_rain
            
            # Determine irrigation recommendation
            if expected_deficit <= 0:
                # No irrigation needed
                irrigation_status = "not_needed"
                irrigation_amount = 0
                days_until_irrigation = 3
                priority = "low"
                recommendation = "No irrigation needed in the next 3 days due to sufficient soil moisture and expected rainfall."
            else:
                # Calculate irrigation amount (mm)
                irrigation_amount = expected_deficit * 0.1  # Convert percentage to mm (simplified)
                
                if soil_moisture < stage_params["min_moisture"]:
                    # Urgent irrigation needed
                    irrigation_status = "urgent"
                    days_until_irrigation = 0
                    priority = "high"
                    recommendation = f"Urgent irrigation of {irrigation_amount:.1f} mm needed. Soil moisture is below minimum threshold."
                elif expected_deficit > 15:
                    # Irrigation needed soon
                    irrigation_status = "needed_soon"
                    days_until_irrigation = 1
                    priority = "medium"
                    recommendation = f"Irrigation of {irrigation_amount:.1f} mm recommended within 24 hours. Significant water deficit expected."
                else:
                    # Irrigation needed later
                    irrigation_status = "needed_later"
                    days_until_irrigation = 2
                    priority = "low"
                    recommendation = f"Irrigation of {irrigation_amount:.1f} mm recommended within 2-3 days. Moderate water deficit expected."
                    
            return {
                "crop_type": crop_type,
                "crop_stage": crop_stage,
                "current_soil_moisture": soil_moisture,
                "optimal_soil_moisture": stage_params["optimal_moisture"],
                "irrigation_status": irrigation_status,
                "irrigation_amount": round(irrigation_amount, 1),
                "days_until_irrigation": days_until_irrigation,
                "expected_rain_3days": round(expected_rain, 1),
                "expected_et_3days": round(expected_et, 1),
                "priority": priority,
                "recommendation": recommendation
            }
            
        except Exception as e:
            self.logger.error(f"Error predicting irrigation needs: {str(e)}")
            return None
            
    def predict_pest_disease_risk(self, weather_forecast, ndvi, crop_type):
        """
        Predict pest and disease risk based on weather conditions and crop health
        
        Args:
            weather_forecast (list): List of daily weather forecasts
            ndvi (float): Current NDVI value
            crop_type (str): Type of crop
            
        Returns:
            dict: Pest and disease risk assessment
        """
        try:
            # Common pest and disease conditions for different crops
            pest_disease_conditions = {
                "maize": [
                    {
                        "name": "Fall Armyworm",
                        "temp_range": (20, 32),
                        "humidity_range": (60, 95),
                        "rain_threshold": 5,
                        "ndvi_threshold": 0.6
                    },
                    {
                        "name": "Maize Streak Virus",
                        "temp_range": (25, 35),
                        "humidity_range": (70, 100),
                        "rain_threshold": 0,
                        "ndvi_threshold": 0.5
                    },
                    {
                        "name": "Gray Leaf Spot",
                        "temp_range": (22, 30),
                        "humidity_range": (85, 100),
                        "rain_threshold": 10,
                        "ndvi_threshold": 0.55
                    }
                ],
                "rice": [
                    {
                        "name": "Rice Blast",
                        "temp_range": (24, 30),
                        "humidity_range": (85, 100),
                        "rain_threshold": 5,
                        "ndvi_threshold": 0.6
                    },
                    {
                        "name": "Brown Plant Hopper",
                        "temp_range": (25, 32),
                        "humidity_range": (70, 95),
                        "rain_threshold": 0,
                        "ndvi_threshold": 0.65
                    }
                ],
                "default": [
                    {
                        "name": "Aphids",
                        "temp_range": (20, 30),
                        "humidity_range": (60, 90),
                        "rain_threshold": 0,
                        "ndvi_threshold": 0.6
                    },
                    {
                        "name": "Fungal Diseases",
                        "temp_range": (18, 28),
                        "humidity_range": (80, 100),
                        "rain_threshold": 5,
                        "ndvi_threshold": 0.55
                    }
                ]
            }
            
            # Get pest and disease conditions for the specified crop
            conditions = pest_disease_conditions.get(crop_type.lower(), pest_disease_conditions["default"])
            
            # Extract weather parameters for the next 5 days
            avg_temp = np.mean([day["temperature"]["day"] for day in weather_forecast[:5]])
            max_temp = max([day["temperature"]["max"] for day in weather_forecast[:5]])
            min_temp = min([day["temperature"]["min"] for day in weather_forecast[:5]])
            avg_humidity = np.mean([day["humidity"] for day in weather_forecast[:5]])
            max_humidity = max([day["humidity"] for day in weather_forecast[:5]])
            total_rain = sum([day.get("rain", 0) for day in weather_forecast[:5]])
            rain_days = sum([1 for day in weather_forecast[:5] if day.get("rain", 0) > 1])
            
            # Calculate risk for each pest/disease
            risks = []
            
            for condition in conditions:
                # Check if temperature is in range
                temp_in_range = (condition["temp_range"][0] <= avg_temp <= condition["temp_range"][1])
                
                # Check if humidity is in range
                humidity_in_range = (condition["humidity_range"][0] <= max_humidity <= condition["humidity_range"][1])
                
                # Check rainfall condition
                rain_condition = (total_rain >= condition["rain_threshold"])
                
                # Check NDVI condition (lower NDVI indicates more vulnerable plants)
                ndvi_condition = (ndvi < condition["ndvi_threshold"])
                
                # Calculate risk score (0-100)
                risk_score = 0
                
                if temp_in_range:
                    risk_score += 30
                
                if humidity_in_range:
                    risk_score += 30
                
                if rain_condition:
                    risk_score += 20
                
                if ndvi_condition:
                    risk_score += 20
                
                # Determine risk level
                if risk_score >= 80:
                    risk_level = "High"
                elif risk_score >= 50:
                    risk_level = "Medium"
                else:
                    risk_level = "Low"
                
                # Only include medium or high risks
                if risk_score >= 50:
                    risks.append({
                        "pest_disease": condition["name"],
                        "risk_level": risk_level,
                        "risk_score": risk_score,
                        "factors": {
                            "temperature": temp_in_range,
                            "humidity": humidity_in_range,
                            "rainfall": rain_condition,
                            "crop_health": ndvi_condition
                        },
                        "recommendations": self._get_pest_disease_recommendations(condition["name"], risk_level)
                    })
            
            # Sort risks by score (descending)
            risks.sort(key=lambda x: x["risk_score"], reverse=True)
            
            # Determine overall risk level
            if any(risk["risk_level"] == "High" for risk in risks):
                overall_risk = "High"
            elif any(risk["risk_level"] == "Medium" for risk in risks):
                overall_risk = "Medium"
            else:
                overall_risk = "Low"
                
            return {
                "crop_type": crop_type,
                "overall_risk": overall_risk,
                "weather_conditions": {
                    "avg_temperature": round(avg_temp, 1),
                    "max_temperature": round(max_temp, 1),
                    "min_temperature": round(min_temp, 1),
                    "avg_humidity": round(avg_humidity, 1),
                    "max_humidity": round(max_humidity, 1),
                    "total_rainfall": round(total_rain, 1),
                    "rainy_days": rain_days
                },
                "crop_health_ndvi": round(ndvi, 2),
                "specific_risks": risks
            }
            
        except Exception as e:
            self.logger.error(f"Error predicting pest/disease risk: {str(e)}")
            return None
    
    def _get_pest_disease_recommendations(self, pest_disease, risk_level):
        """Get recommendations for pest/disease control based on risk level"""
        recommendations = {
            "Fall Armyworm": {
                "High": "Immediate scouting and application of appropriate insecticides. Consider biological controls like Bacillus thuringiensis.",
                "Medium": "Regular scouting for early signs of infestation. Prepare for possible treatment."
            },
            "Maize Streak Virus": {
                "High": "Control leafhoppers with appropriate insecticides. Remove infected plants to prevent spread.",
                "Medium": "Monitor for leafhoppers and symptoms. Consider preventive insecticide application."
            },
            "Gray Leaf Spot": {
                "High": "Apply fungicide treatment. Consider crop rotation in future seasons.",
                "Medium": "Monitor for symptoms. Plan for fungicide application if conditions worsen."
            },
            "Rice Blast": {
                "High": "Apply fungicide treatment. Manage water levels to reduce humidity in the field.",
                "Medium": "Monitor for symptoms. Ensure balanced fertilization to improve plant resistance."
            },
            "Brown Plant Hopper": {
                "High": "Apply appropriate insecticides. Drain fields intermittently to disrupt the pest's lifecycle.",
                "Medium": "Regular field scouting. Consider preventive insecticide application."
            },
            "Aphids": {
                "High": "Apply insecticidal soap or neem oil. Introduce natural predators if available.",
                "Medium": "Monitor population levels. Prepare for treatment if populations increase."
            },
            "Fungal Diseases": {
                "High": "Apply appropriate fungicide. Improve air circulation around plants if possible.",
                "Medium": "Monitor for symptoms. Avoid overhead irrigation to reduce leaf wetness."
            }
        }
        
        default_recs = {
            "High": "Consult with local agricultural extension officer for appropriate treatment options.",
            "Medium": "Monitor closely for symptoms and prepare for possible treatment."
        }
        
        pest_recs = recommendations.get(pest_disease, default_recs)
        return pest_recs.get(risk_level, "Monitor for symptoms and signs of infestation.")

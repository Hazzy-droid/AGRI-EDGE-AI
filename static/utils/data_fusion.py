import os
import logging
import numpy as np
from datetime import datetime, timedelta
import json

logger = logging.getLogger(__name__)

class DataFusionEngine:
    """Class for implementing data fusion algorithms to combine multiple data sources"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def fuse_satellite_weather_soil(self, satellite_data, weather_data, soil_data):
        """
        Fuse satellite imagery, weather data, and soil sensor data
        
        Args:
            satellite_data (dict): Satellite imagery data and analysis
            weather_data (dict): Weather data and forecasts
            soil_data (dict): Soil sensor data and analysis
            
        Returns:
            dict: Fused data and insights
        """
        try:
            # Check if we have all required data
            if not satellite_data or not weather_data or not soil_data:
                self.logger.warning("Missing data for fusion")
                return None
                
            # Extract key metrics from each data source
            fused_data = {
                "timestamp": datetime.now().isoformat(),
                "satellite": {
                    "ndvi": satellite_data.get("average_ndvi", 0),
                    "crop_health_status": satellite_data.get("overall_status", "Unknown"),
                    "water_stress": satellite_data.get("water_stress", {}).get("overall_status", "Unknown")
                },
                "weather": {
                    "temperature": weather_data.get("temperature", {}).get("day", 0),
                    "precipitation": weather_data.get("rain", 0),
                    "humidity": weather_data.get("humidity", 0)
                },
                "soil": {
                    "moisture": soil_data.get("moisture", 0),
                    "temperature": soil_data.get("temperature", 0),
                    "ph": soil_data.get("ph", 0),
                    "nitrogen": soil_data.get("nitrogen", 0),
                    "phosphorus": soil_data.get("phosphorus", 0),
                    "potassium": soil_data.get("potassium", 0)
                }
            }
            
            # Generate integrated insights
            insights = self._generate_integrated_insights(fused_data)
            
            return {
                "fused_data": fused_data,
                "insights": insights
            }
            
        except Exception as e:
            self.logger.error(f"Error in data fusion: {str(e)}")
            return None
    
    def _generate_integrated_insights(self, fused_data):
        """Generate integrated insights from fused data"""
        insights = []
        
        # Example: Detect water stress by combining NDVI, soil moisture, and weather
        ndvi = fused_data["satellite"]["ndvi"]
        soil_moisture = fused_data["soil"]["moisture"]
        precipitation = fused_data["weather"]["precipitation"]
        
        if ndvi < 0.4 and soil_moisture < 30 and precipitation < 5:
            insights.append({
                "type": "warning",
                "category": "water_stress",
                "description": "Critical water stress detected. Immediate irrigation recommended.",
                "confidence": "high"
            })
        elif ndvi < 0.5 and soil_moisture < 40 and precipitation < 10:
            insights.append({
                "type": "warning",
                "category": "water_stress",
                "description": "Moderate water stress detected. Consider irrigation in the next 1-2 days.",
                "confidence": "medium"
            })
            
        # Example: Detect nutrient deficiency by combining NDVI and soil nutrient levels
        nitrogen = fused_data["soil"]["nitrogen"]
        phosphorus = fused_data["soil"]["phosphorus"]
        potassium = fused_data["soil"]["potassium"]
        
        if ndvi < 0.4 and nitrogen < 15:
            insights.append({
                "type": "warning",
                "category": "nutrient_deficiency",
                "description": "Nitrogen deficiency detected. Apply nitrogen-rich fertilizer.",
                "confidence": "medium"
            })
            
        if ndvi < 0.4 and phosphorus < 10:
            insights.append({
                "type": "warning",
                "category": "nutrient_deficiency",
                "description": "Phosphorus deficiency detected. Apply phosphorus-rich fertilizer.",
                "confidence": "medium"
            })
            
        if ndvi < 0.4 and potassium < 15:
            insights.append({
                "type": "warning",
                "category": "nutrient_deficiency",
                "description": "Potassium deficiency detected. Apply potassium-rich fertilizer.",
                "confidence": "medium"
            })
            
        # Example: Detect optimal conditions for planting
        soil_temp = fused_data["soil"]["temperature"]
        air_temp = fused_data["weather"]["temperature"]
        
        if 20 <= soil_temp <= 30 and 20 <= air_temp <= 30 and 40 <= soil_moisture <= 60:
            insights.append({
                "type": "opportunity",
                "category": "planting_conditions",
                "description": "Optimal conditions for planting. Consider planting in the next few days.",
                "confidence": "high"
            })
            
        # Example: Detect pest/disease risk based on weather and crop health
        humidity = fused_data["weather"]["humidity"]
        crop_health = fused_data["satellite"]["crop_health_status"]
        
        if humidity > 80 and 22 <= air_temp <= 28 and crop_health in ["Fair", "Poor"]:
            insights.append({
                "type": "warning",
                "category": "pest_disease_risk",
                "description": "High risk of fungal disease due to high humidity and temperature. Consider preventive fungicide application.",
                "confidence": "medium"
            })
            
        return insights
    
    def generate_crop_recommendations(self, fused_data, crop_type):
        """
        Generate crop-specific recommendations based on fused data
        
        Args:
            fused_data (dict): Fused data from multiple sources
            crop_type (str): Type of crop
            
        Returns:
            list: List of recommendations
        """
        try:
            recommendations = []
            
            # Extract key metrics
            ndvi = fused_data["fused_data"]["satellite"]["ndvi"]
            soil_moisture = fused_data["fused_data"]["soil"]["moisture"]
            soil_temp = fused_data["fused_data"]["soil"]["temperature"]
            air_temp = fused_data["fused_data"]["weather"]["temperature"]
            precipitation = fused_data["fused_data"]["weather"]["precipitation"]
            nitrogen = fused_data["fused_data"]["soil"]["nitrogen"]
            phosphorus = fused_data["fused_data"]["soil"]["phosphorus"]
            potassium = fused_data["fused_data"]["soil"]["potassium"]
            ph = fused_data["fused_data"]["soil"]["ph"]
            
            # Define crop-specific thresholds
            crop_thresholds = {
                "maize": {
                    "optimal_soil_moisture": (40, 60),
                    "optimal_soil_temp": (18, 32),
                    "optimal_air_temp": (18, 32),
                    "optimal_nitrogen": (20, 30),
                    "optimal_phosphorus": (10, 15),
                    "optimal_potassium": (15, 25),
                    "optimal_ph": (5.8, 7.0)
                },
                "rice": {
                    "optimal_soil_moisture": (60, 80),
                    "optimal_soil_temp": (20, 30),
                    "optimal_air_temp": (20, 32),
                    "optimal_nitrogen": (15, 25),
                    "optimal_phosphorus": (8, 13),
                    "optimal_potassium": (15, 25),
                    "optimal_ph": (5.5, 6.5)
                },
                # Default thresholds for other crops
                "default": {
                    "optimal_soil_moisture": (40, 60),
                    "optimal_soil_temp": (18, 30),
                    "optimal_air_temp": (18, 30),
                    "optimal_nitrogen": (15, 25),
                    "optimal_phosphorus": (10, 15),
                    "optimal_potassium": (15, 20),
                    "optimal_ph": (6.0, 7.0)
                }
            }
            
            # Get thresholds for the specified crop
            thresholds = crop_thresholds.get(crop_type.lower(), crop_thresholds["default"])
            
            # Irrigation recommendation
            if soil_moisture < thresholds["optimal_soil_moisture"][0]:
                if soil_moisture < thresholds["optimal_soil_moisture"][0] - 10:
                    priority = "high"
                    description = f"Critical soil moisture level ({soil_moisture}%). Immediate irrigation required."
                else:
                    priority = "medium"
                    description = f"Low soil moisture level ({soil_moisture}%). Irrigation recommended in the next 1-2 days."
                
                recommendations.append({
                    "category": "irrigation",
                    "description": description,
                    "priority": priority
                })
            elif soil_moisture > thresholds["optimal_soil_moisture"][1]:
                if soil_moisture > thresholds["optimal_soil_moisture"][1] + 10:
                    priority = "medium"
                    description = f"Excessive soil moisture level ({soil_moisture}%). Avoid irrigation and improve drainage if possible."
                else:
                    priority = "low"
                    description = f"High soil moisture level ({soil_moisture}%). Delay irrigation until moisture decreases."
                
                recommendations.append({
                    "category": "irrigation",
                    "description": description,
                    "priority": priority
                })
                
            # Fertilization recommendations
            if nitrogen < thresholds["optimal_nitrogen"][0]:
                if nitrogen < thresholds["optimal_nitrogen"][0] - 5:
                    priority = "high"
                    description = f"Severe nitrogen deficiency detected ({nitrogen} ppm). Apply nitrogen-rich fertilizer as soon as possible."
                else:
                    priority = "medium"
                    description = f"Nitrogen deficiency detected ({nitrogen} ppm). Apply nitrogen-rich fertilizer."
                
                recommendations.append({
                    "category": "fertilization",
                    "description": description,
                    "priority": priority
                })
                
            if phosphorus < thresholds["optimal_phosphorus"][0]:
                if phosphorus < thresholds["optimal_phosphorus"][0] - 3:
                    priority = "high"
                    description = f"Severe phosphorus deficiency detected ({phosphorus} ppm). Apply phosphorus-rich fertilizer as soon as possible."
                else:
                    priority = "medium"
                    description = f"Phosphorus deficiency detected ({phosphorus} ppm). Apply phosphorus-rich fertilizer."
                
                recommendations.append({
                    "category": "fertilization",
                    "description": description,
                    "priority": priority
                })
                
            if potassium < thresholds["optimal_potassium"][0]:
                if potassium < thresholds["optimal_potassium"][0] - 5:
                    priority = "high"
                    description = f"Severe potassium deficiency detected ({potassium} ppm). Apply potassium-rich fertilizer as soon as possible."
                else:
                    priority = "medium"
                    description = f"Potassium deficiency detected ({potassium} ppm). Apply potassium-rich fertilizer."
                
                recommendations.append({
                    "category": "fertilization",
                    "description": description,
                    "priority": priority
                })
                
            # pH management
            if ph < thresholds["optimal_ph"][0]:
                if ph < thresholds["optimal_ph"][0] - 0.5:
                    priority = "medium"
                    description = f"Soil pH is too acidic ({ph}). Apply agricultural lime to increase pH."
                else:
                    priority = "low"
                    description = f"Soil pH is slightly acidic ({ph}). Consider applying lime to increase pH."
                
                recommendations.append({
                    "category": "soil_amendment",
                    "description": description,
                    "priority": priority
                })
            elif ph > thresholds["optimal_ph"][1]:
                if ph > thresholds["optimal_ph"][1] + 0.5:
                    priority = "medium"
                    description = f"Soil pH is too alkaline ({ph}). Apply sulfur or acidic organic matter to decrease pH."
                else:
                    priority = "low"
                    description = f"Soil pH is slightly alkaline ({ph}). Consider applying acidic organic matter to decrease pH."
                
                recommendations.append({
                    "category": "soil_amendment",
                    "description": description,
                    "priority": priority
                })
                
            # Crop health recommendations based on NDVI
            if ndvi < 0.3:
                priority = "high"
                description = f"Critical crop health issue detected (NDVI: {ndvi:.2f}). Check for pests, diseases, or severe nutrient deficiencies."
                
                recommendations.append({
                    "category": "crop_health",
                    "description": description,
                    "priority": priority
                })
            elif ndvi < 0.5:
                priority = "medium"
                description = f"Potential crop health issue detected (NDVI: {ndvi:.2f}). Monitor for pests, diseases, or nutrient deficiencies."
                
                recommendations.append({
                    "category": "crop_health",
                    "description": description,
                    "priority": priority
                })
                
            # Sort recommendations by priority
            priority_order = {"high": 0, "medium": 1, "low": 2}
            recommendations.sort(key=lambda x: priority_order[x["priority"]])
            
            return recommendations
            
        except Exception as e:
            self.logger.error(f"Error generating crop recommendations: {str(e)}")
            return []

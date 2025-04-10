import os
import logging
import requests
import numpy as np
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

class WeatherForecaster:
    """Class for hyper-local weather forecasting"""
    
    def __init__(self, api_key=None):
        self.api_key = api_key or os.environ.get('WEATHER_API_KEY', '')
        self.base_url = "https://api.openweathermap.org/data/2.5"
        self.logger = logging.getLogger(__name__)
    
    def get_current_weather(self, lat, lon):
        """
        Get current weather data for a specific location
        
        Args:
            lat (float): Latitude
            lon (float): Longitude
            
        Returns:
            dict: Current weather data
        """
        if not self.api_key:
            self.logger.warning("No weather API key provided")
            return None
            
        try:
            response = requests.get(
                f"{self.base_url}/weather",
                params={
                    "lat": lat,
                    "lon": lon,
                    "appid": self.api_key,
                    "units": "metric"
                }
            )
            
            if response.status_code == 200:
                data = response.json()
                
                # Extract relevant information
                return {
                    "temperature": data["main"]["temp"],
                    "humidity": data["main"]["humidity"],
                    "pressure": data["main"]["pressure"],
                    "wind_speed": data["wind"]["speed"],
                    "wind_direction": data["wind"]["deg"],
                    "weather_description": data["weather"][0]["description"],
                    "icon": data["weather"][0]["icon"],
                    "clouds": data.get("clouds", {}).get("all", 0),
                    "rain": data.get("rain", {}).get("1h", 0),
                    "timestamp": datetime.utcfromtimestamp(data["dt"]).isoformat()
                }
            else:
                self.logger.error(f"Failed to get current weather: {response.status_code}")
                return None
                
        except Exception as e:
            self.logger.error(f"Error getting current weather: {str(e)}")
            return None
    
    def get_weather_forecast(self, lat, lon, days=7):
        """
        Get weather forecast for a specific location
        
        Args:
            lat (float): Latitude
            lon (float): Longitude
            days (int): Number of days for forecast (max 7)
            
        Returns:
            list: List of daily weather forecasts
        """
        if not self.api_key:
            self.logger.warning("No weather API key provided")
            return None
            
        try:
            response = requests.get(
                f"{self.base_url}/onecall",
                params={
                    "lat": lat,
                    "lon": lon,
                    "exclude": "minutely",
                    "appid": self.api_key,
                    "units": "metric"
                }
            )
            
            if response.status_code == 200:
                data = response.json()
                
                # Process daily forecasts
                daily_forecasts = []
                
                for i, day_data in enumerate(data["daily"]):
                    if i >= days:
                        break
                        
                    forecast = {
                        "date": datetime.utcfromtimestamp(day_data["dt"]).strftime('%Y-%m-%d'),
                        "temperature": {
                            "min": day_data["temp"]["min"],
                            "max": day_data["temp"]["max"],
                            "day": day_data["temp"]["day"],
                            "night": day_data["temp"]["night"]
                        },
                        "humidity": day_data["humidity"],
                        "pressure": day_data["pressure"],
                        "wind_speed": day_data["wind_speed"],
                        "wind_direction": day_data["wind_deg"],
                        "weather_description": day_data["weather"][0]["description"],
                        "icon": day_data["weather"][0]["icon"],
                        "clouds": day_data.get("clouds", 0),
                        "rain": day_data.get("rain", 0),
                        "probability_precipitation": day_data.get("pop", 0) * 100,
                        "uvi": day_data.get("uvi", 0)
                    }
                    
                    daily_forecasts.append(forecast)
                
                return daily_forecasts
            else:
                self.logger.error(f"Failed to get weather forecast: {response.status_code}")
                return None
                
        except Exception as e:
            self.logger.error(f"Error getting weather forecast: {str(e)}")
            return None
    
    def get_hourly_forecast(self, lat, lon, hours=24):
        """
        Get hourly weather forecast for a specific location
        
        Args:
            lat (float): Latitude
            lon (float): Longitude
            hours (int): Number of hours for forecast (max 48)
            
        Returns:
            list: List of hourly weather forecasts
        """
        if not self.api_key:
            self.logger.warning("No weather API key provided")
            return None
            
        try:
            response = requests.get(
                f"{self.base_url}/onecall",
                params={
                    "lat": lat,
                    "lon": lon,
                    "exclude": "minutely,daily",
                    "appid": self.api_key,
                    "units": "metric"
                }
            )
            
            if response.status_code == 200:
                data = response.json()
                
                # Process hourly forecasts
                hourly_forecasts = []
                
                for i, hour_data in enumerate(data["hourly"]):
                    if i >= hours:
                        break
                        
                    forecast = {
                        "time": datetime.utcfromtimestamp(hour_data["dt"]).strftime('%Y-%m-%d %H:%M'),
                        "temperature": hour_data["temp"],
                        "humidity": hour_data["humidity"],
                        "pressure": hour_data["pressure"],
                        "wind_speed": hour_data["wind_speed"],
                        "wind_direction": hour_data["wind_deg"],
                        "weather_description": hour_data["weather"][0]["description"],
                        "icon": hour_data["weather"][0]["icon"],
                        "clouds": hour_data.get("clouds", 0),
                        "rain": hour_data.get("rain", {}).get("1h", 0),
                        "probability_precipitation": hour_data.get("pop", 0) * 100
                    }
                    
                    hourly_forecasts.append(forecast)
                
                return hourly_forecasts
            else:
                self.logger.error(f"Failed to get hourly forecast: {response.status_code}")
                return None
                
        except Exception as e:
            self.logger.error(f"Error getting hourly forecast: {str(e)}")
            return None
    
    def analyze_irrigation_needs(self, weather_data, soil_moisture, crop_type):
        """
        Analyze irrigation needs based on weather forecast and soil moisture
        
        Args:
            weather_data (list): Weather forecast data
            soil_moisture (float): Current soil moisture percentage
            crop_type (str): Type of crop
            
        Returns:
            dict: Irrigation recommendation
        """
        try:
            # Define crop-specific parameters
            crop_params = {
                "maize": {"min_moisture": 40, "optimal_moisture": 60, "max_moisture": 80},
                "rice": {"min_moisture": 60, "optimal_moisture": 80, "max_moisture": 100},
                "sorghum": {"min_moisture": 35, "optimal_moisture": 55, "max_moisture": 75},
                "millet": {"min_moisture": 30, "optimal_moisture": 50, "max_moisture": 70},
                "cassava": {"min_moisture": 35, "optimal_moisture": 55, "max_moisture": 75},
                "yam": {"min_moisture": 45, "optimal_moisture": 65, "max_moisture": 85},
                "sweet_potato": {"min_moisture": 40, "optimal_moisture": 60, "max_moisture": 80},
                "groundnut": {"min_moisture": 35, "optimal_moisture": 55, "max_moisture": 75},
                "cowpea": {"min_moisture": 30, "optimal_moisture": 50, "max_moisture": 70},
                "soybean": {"min_moisture": 40, "optimal_moisture": 60, "max_moisture": 80},
                # Default parameters for other crops
                "default": {"min_moisture": 40, "optimal_moisture": 60, "max_moisture": 80}
            }
            
            # Get crop parameters
            params = crop_params.get(crop_type, crop_params["default"])
            
            # Calculate expected precipitation in the next 3 days
            precipitation_3days = sum(day["rain"] for day in weather_data[:3] if "rain" in day)
            
            # Calculate average temperature in the next 3 days
            avg_temp_3days = np.mean([day["temperature"]["day"] for day in weather_data[:3]])
            
            # Estimate daily evapotranspiration (simplified)
            # A very basic estimate using temperature
            daily_et = 0.5 * (avg_temp_3days / 20)  # in mm
            
            # Calculate water balance for the next 3 days
            water_balance = precipitation_3days - (daily_et * 3)
            
            # Determine irrigation needs
            if soil_moisture < params["min_moisture"]:
                # Urgent irrigation needed
                irrigation_status = "urgent"
                irrigation_needed = True
                recommendation = "Urgent irrigation needed. Soil moisture is below the minimum threshold."
            elif soil_moisture < params["optimal_moisture"] and water_balance < 0:
                # Irrigation recommended
                irrigation_status = "recommended"
                irrigation_needed = True
                recommendation = "Irrigation recommended. Soil moisture is below optimal level and insufficient rainfall is expected."
            elif soil_moisture > params["max_moisture"]:
                # No irrigation, drain if possible
                irrigation_status = "excess"
                irrigation_needed = False
                recommendation = "Excess soil moisture. No irrigation needed, consider drainage if available."
            else:
                # No irrigation needed
                irrigation_status = "sufficient"
                irrigation_needed = False
                recommendation = "Sufficient soil moisture. No irrigation needed at this time."
            
            return {
                "irrigation_status": irrigation_status,
                "irrigation_needed": irrigation_needed,
                "recommendation": recommendation,
                "expected_precipitation_3days": precipitation_3days,
                "expected_evapotranspiration_3days": daily_et * 3,
                "water_balance_3days": water_balance,
                "current_soil_moisture": soil_moisture,
                "optimal_soil_moisture": params["optimal_moisture"]
            }
            
        except Exception as e:
            self.logger.error(f"Error analyzing irrigation needs: {str(e)}")
            return None
    
    def generate_planting_recommendation(self, location, crop_types=None):
        """
        Generate planting recommendations based on weather trends
        
        Args:
            location (tuple): Latitude and longitude (lat, lon)
            crop_types (list): List of potential crop types to consider
            
        Returns:
            dict: Planting recommendations
        """
        if crop_types is None:
            crop_types = ["maize", "rice", "sorghum", "millet", "cassava"]
            
        try:
            lat, lon = location
            
            # Get 7-day forecast
            forecast = self.get_weather_forecast(lat, lon, days=7)
            
            if not forecast:
                return None
                
            # Calculate relevant metrics
            avg_temp = np.mean([day["temperature"]["day"] for day in forecast])
            min_temp = min([day["temperature"]["min"] for day in forecast])
            max_temp = max([day["temperature"]["max"] for day in forecast])
            avg_humidity = np.mean([day["humidity"] for day in forecast])
            total_precipitation = sum([day.get("rain", 0) for day in forecast])
            precipitation_days = sum([1 for day in forecast if day.get("rain", 0) > 1])
            
            # Define optimal conditions for different crops
            crop_conditions = {
                "maize": {
                    "min_temp": 10, "optimal_temp": 25, "max_temp": 35,
                    "min_rain": 10, "max_rain": 50
                },
                "rice": {
                    "min_temp": 15, "optimal_temp": 30, "max_temp": 35,
                    "min_rain": 20, "max_rain": 100
                },
                "sorghum": {
                    "min_temp": 12, "optimal_temp": 27, "max_temp": 38,
                    "min_rain": 5, "max_rain": 40
                },
                "millet": {
                    "min_temp": 12, "optimal_temp": 28, "max_temp": 40,
                    "min_rain": 5, "max_rain": 30
                },
                "cassava": {
                    "min_temp": 18, "optimal_temp": 28, "max_temp": 35,
                    "min_rain": 10, "max_rain": 60
                },
                "yam": {
                    "min_temp": 20, "optimal_temp": 30, "max_temp": 35,
                    "min_rain": 15, "max_rain": 70
                },
                "sweet_potato": {
                    "min_temp": 15, "optimal_temp": 24, "max_temp": 35,
                    "min_rain": 10, "max_rain": 50
                },
                "groundnut": {
                    "min_temp": 15, "optimal_temp": 28, "max_temp": 35,
                    "min_rain": 5, "max_rain": 40
                },
                "cowpea": {
                    "min_temp": 18, "optimal_temp": 28, "max_temp": 35,
                    "min_rain": 5, "max_rain": 30
                },
                "soybean": {
                    "min_temp": 15, "optimal_temp": 26, "max_temp": 35,
                    "min_rain": 10, "max_rain": 50
                }
            }
            
            # Evaluate each crop
            recommendations = []
            
            for crop in crop_types:
                if crop not in crop_conditions:
                    continue
                    
                conditions = crop_conditions[crop]
                
                # Calculate temperature suitability (0 to 1)
                if min_temp < conditions["min_temp"] or max_temp > conditions["max_temp"]:
                    temp_suitability = 0
                else:
                    temp_distance = abs(avg_temp - conditions["optimal_temp"])
                    max_distance = max(conditions["optimal_temp"] - conditions["min_temp"],
                                      conditions["max_temp"] - conditions["optimal_temp"])
                    temp_suitability = max(0, 1 - (temp_distance / max_distance))
                
                # Calculate precipitation suitability (0 to 1)
                if total_precipitation < conditions["min_rain"] or total_precipitation > conditions["max_rain"]:
                    rain_suitability = 0
                else:
                    if total_precipitation <= conditions["optimal_rain"]:
                        rain_distance = conditions["optimal_rain"] - total_precipitation
                        max_distance = conditions["optimal_rain"] - conditions["min_rain"]
                    else:
                        rain_distance = total_precipitation - conditions["optimal_rain"]
                        max_distance = conditions["max_rain"] - conditions["optimal_rain"]
                    
                    rain_suitability = max(0, 1 - (rain_distance / max_distance))
                
                # Overall suitability score
                suitability = 0.7 * temp_suitability + 0.3 * rain_suitability
                
                # Recommendation threshold
                if suitability >= 0.7:
                    status = "Highly Recommended"
                elif suitability >= 0.5:
                    status = "Recommended"
                elif suitability >= 0.3:
                    status = "Marginally Suitable"
                else:
                    status = "Not Recommended"
                
                recommendations.append({
                    "crop": crop,
                    "suitability_score": suitability,
                    "status": status,
                    "temperature_suitability": temp_suitability,
                    "precipitation_suitability": rain_suitability,
                    "notes": self._generate_recommendation_notes(crop, temp_suitability, rain_suitability)
                })
            
            # Sort by suitability score (descending)
            recommendations.sort(key=lambda x: x["suitability_score"], reverse=True)
            
            return {
                "weather_summary": {
                    "avg_temp": avg_temp,
                    "min_temp": min_temp,
                    "max_temp": max_temp,
                    "avg_humidity": avg_humidity,
                    "total_precipitation": total_precipitation,
                    "precipitation_days": precipitation_days
                },
                "recommendations": recommendations
            }
            
        except Exception as e:
            self.logger.error(f"Error generating planting recommendation: {str(e)}")
            return None
    
    def _generate_recommendation_notes(self, crop, temp_suitability, rain_suitability):
        """Generate recommendation notes based on suitability scores"""
        notes = []
        
        if temp_suitability < 0.3:
            notes.append("Temperature conditions are unfavorable.")
        elif temp_suitability < 0.7:
            notes.append("Temperature conditions are marginal.")
        else:
            notes.append("Temperature conditions are favorable.")
            
        if rain_suitability < 0.3:
            notes.append("Precipitation conditions are unfavorable.")
        elif rain_suitability < 0.7:
            notes.append("Precipitation conditions are marginal.")
        else:
            notes.append("Precipitation conditions are favorable.")
            
        if crop == "maize":
            notes.append("Maize requires well-drained soil with good fertility.")
        elif crop == "rice":
            notes.append("Rice typically requires waterlogged conditions for optimal growth.")
        elif crop == "sorghum":
            notes.append("Sorghum is drought-tolerant and suitable for water-limited environments.")
        elif crop == "millet":
            notes.append("Millet is highly drought-tolerant and suitable for sandy soils.")
        elif crop == "cassava":
            notes.append("Cassava is drought-tolerant once established and grows well in poor soils.")
            
        return " ".join(notes)

import os
import logging
import requests
import json
import numpy as np
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

class SoilSensorManager:
    """Class for managing and analyzing data from IoT soil sensors"""
    
    def __init__(self, api_key=None):
        self.api_key = api_key or os.environ.get('SOIL_API_KEY', '')
        self.base_url = "https://api.soil-sensors.com/v1"  # Placeholder API endpoint
        self.logger = logging.getLogger(__name__)
        
    def get_sensor_data(self, sensor_id, start_date=None, end_date=None):
        """
        Get data from a specific soil sensor
        
        Args:
            sensor_id (str): Unique identifier for the sensor
            start_date (str): Start date in format 'YYYY-MM-DD'
            end_date (str): End date in format 'YYYY-MM-DD'
            
        Returns:
            dict: Sensor data
        """
        # In a real implementation, this would fetch data from an actual API
        # For this example, we'll generate realistic soil sensor data
        
        # Convert string dates to datetime objects or use defaults
        if start_date:
            start = datetime.strptime(start_date, '%Y-%m-%d')
        else:
            start = datetime.now() - timedelta(days=7)
            
        if end_date:
            end = datetime.strptime(end_date, '%Y-%m-%d')
        else:
            end = datetime.now()
            
        # Generate a date range
        date_range = []
        current_date = start
        while current_date <= end:
            date_range.append(current_date)
            current_date += timedelta(hours=1)
            
        # Generate sensor data for each date
        sensor_data = []
        
        for date in date_range:
            # Create realistic patterns with some random noise
            hour = date.hour
            day_of_year = date.timetuple().tm_yday
            
            # Moisture varies throughout the day (lower during hot hours)
            moisture_base = 45 + 5 * np.sin(day_of_year / 15)  # Seasonal variation
            moisture_daily = moisture_base - 5 * np.sin(hour / 24 * 2 * np.pi)  # Daily variation
            moisture = max(5, min(99, moisture_daily + np.random.normal(-2, 2)))  # Add noise
            
            # Temperature follows daily patterns
            temp_base = 25 + 5 * np.sin(day_of_year / 30)  # Seasonal variation
            temp_daily = temp_base + 5 * np.sin((hour - 14) / 24 * 2 * np.pi)  # Daily variation, peaks at 2pm
            temperature = max(5, min(45, temp_daily + np.random.normal(-1, 1)))  # Add noise
            
            # pH typically stable but can vary slightly
            ph = 6.5 + np.random.normal(0, 0.1)
            
            # Electrical conductivity (proxy for nutrients)
            ec_base = 0.8 + 0.1 * np.sin(day_of_year / 60)  # Seasonal variation
            ec = max(0.1, min(2.0, ec_base + np.random.normal(0, 0.05)))
            
            # Generate NPK values
            nitrogen = 20 + 5 * np.random.random()  # ppm
            phosphorus = 10 + 3 * np.random.random()  # ppm
            potassium = 15 + 4 * np.random.random()  # ppm
            
            sensor_data.append({
                "timestamp": date.isoformat(),
                "moisture": round(moisture, 1),
                "temperature": round(temperature, 1),
                "ph": round(ph, 2),
                "electrical_conductivity": round(ec, 3),
                "nitrogen": round(nitrogen, 1),
                "phosphorus": round(phosphorus, 1),
                "potassium": round(potassium, 1)
            })
            
        return {
            "sensor_id": sensor_id,
            "location": f"Farm {sensor_id[:2]}",
            "data": sensor_data
        }
    
    def analyze_soil_moisture(self, sensor_data, crop_type):
        """
        Analyze soil moisture levels for a specific crop
        
        Args:
            sensor_data (dict): Soil sensor data
            crop_type (str): Type of crop
            
        Returns:
            dict: Analysis results
        """
        try:
            # Define optimal moisture ranges for different crops
            moisture_ranges = {
                "maize": (40, 60),
                "rice": (60, 80),
                "sorghum": (35, 55),
                "millet": (30, 50),
                "cassava": (35, 55),
                "yam": (45, 65),
                "sweet_potato": (40, 60),
                "groundnut": (35, 55),
                "cowpea": (30, 50),
                "soybean": (40, 60),
                # Default range for other crops
                "default": (40, 60)
            }
            
            # Get optimal range for the specified crop
            optimal_range = moisture_ranges.get(crop_type, moisture_ranges["default"])
            
            # Extract moisture values from sensor data
            moisture_values = [item["moisture"] for item in sensor_data["data"]]
            
            # Calculate average moisture
            avg_moisture = np.mean(moisture_values)
            
            # Calculate the percentage of time moisture was below, within, and above optimal range
            below_optimal = sum(1 for m in moisture_values if m < optimal_range[0]) / len(moisture_values) * 100
            within_optimal = sum(1 for m in moisture_values if optimal_range[0] <= m <= optimal_range[1]) / len(moisture_values) * 100
            above_optimal = sum(1 for m in moisture_values if m > optimal_range[1]) / len(moisture_values) * 100
            
            # Determine moisture status
            if avg_moisture < optimal_range[0]:
                if avg_moisture < optimal_range[0] - 10:
                    status = "Severely Under-watered"
                else:
                    status = "Under-watered"
            elif avg_moisture > optimal_range[1]:
                if avg_moisture > optimal_range[1] + 10:
                    status = "Severely Over-watered"
                else:
                    status = "Over-watered"
            else:
                status = "Optimal"
                
            # Generate recommendation
            if status == "Severely Under-watered":
                recommendation = "Immediate irrigation needed. Soil moisture is significantly below optimal levels for the crop."
            elif status == "Under-watered":
                recommendation = "Irrigation recommended. Soil moisture is below optimal levels for the crop."
            elif status == "Severely Over-watered":
                recommendation = "Avoid irrigation. Consider improving drainage to reduce excess soil moisture."
            elif status == "Over-watered":
                recommendation = "Delay irrigation. Current soil moisture is above optimal levels for the crop."
            else:
                recommendation = "Maintain current irrigation practices. Soil moisture is at optimal levels for the crop."
                
            return {
                "average_moisture": round(avg_moisture, 1),
                "minimum_moisture": round(min(moisture_values), 1),
                "maximum_moisture": round(max(moisture_values), 1),
                "optimal_range": optimal_range,
                "below_optimal_percentage": round(below_optimal, 1),
                "within_optimal_percentage": round(within_optimal, 1),
                "above_optimal_percentage": round(above_optimal, 1),
                "moisture_status": status,
                "recommendation": recommendation
            }
            
        except Exception as e:
            self.logger.error(f"Error analyzing soil moisture: {str(e)}")
            return None
    
    def analyze_soil_fertility(self, sensor_data, crop_type):
        """
        Analyze soil fertility based on NPK levels and pH
        
        Args:
            sensor_data (dict): Soil sensor data
            crop_type (str): Type of crop
            
        Returns:
            dict: Analysis results
        """
        try:
            # Define optimal NPK ranges and pH for different crops
            fertility_ranges = {
                "maize": {
                    "nitrogen": (20, 30),
                    "phosphorus": (10, 15),
                    "potassium": (15, 25),
                    "ph": (5.8, 7.0)
                },
                "rice": {
                    "nitrogen": (15, 25),
                    "phosphorus": (8, 13),
                    "potassium": (15, 25),
                    "ph": (5.5, 6.5)
                },
                "sorghum": {
                    "nitrogen": (15, 25),
                    "phosphorus": (10, 15),
                    "potassium": (15, 20),
                    "ph": (5.5, 7.5)
                },
                # Default ranges for other crops
                "default": {
                    "nitrogen": (15, 25),
                    "phosphorus": (10, 15),
                    "potassium": (15, 20),
                    "ph": (6.0, 7.0)
                }
            }
            
            # Get optimal ranges for the specified crop
            optimal_ranges = fertility_ranges.get(crop_type, fertility_ranges["default"])
            
            # Extract latest fertility values from sensor data
            latest_data = sensor_data["data"][-1]
            
            # Analyze each nutrient and pH
            fertility_analysis = {}
            
            # Nitrogen analysis
            n_value = latest_data["nitrogen"]
            n_range = optimal_ranges["nitrogen"]
            
            if n_value < n_range[0]:
                if n_value < n_range[0] * 0.7:
                    n_status = "Severely Deficient"
                    n_recommendation = "Apply nitrogen-rich fertilizer as soon as possible."
                else:
                    n_status = "Deficient"
                    n_recommendation = "Consider applying nitrogen-rich fertilizer."
            elif n_value > n_range[1]:
                if n_value > n_range[1] * 1.3:
                    n_status = "Excess"
                    n_recommendation = "Avoid applying nitrogen fertilizer."
                else:
                    n_status = "High"
                    n_recommendation = "Reduce nitrogen fertilizer application."
            else:
                n_status = "Optimal"
                n_recommendation = "Maintain current nitrogen fertilization practices."
                
            fertility_analysis["nitrogen"] = {
                "value": n_value,
                "optimal_range": n_range,
                "status": n_status,
                "recommendation": n_recommendation
            }
            
            # Phosphorus analysis
            p_value = latest_data["phosphorus"]
            p_range = optimal_ranges["phosphorus"]
            
            if p_value < p_range[0]:
                if p_value < p_range[0] * 0.7:
                    p_status = "Severely Deficient"
                    p_recommendation = "Apply phosphorus-rich fertilizer as soon as possible."
                else:
                    p_status = "Deficient"
                    p_recommendation = "Consider applying phosphorus-rich fertilizer."
            elif p_value > p_range[1]:
                if p_value > p_range[1] * 1.3:
                    p_status = "Excess"
                    p_recommendation = "Avoid applying phosphorus fertilizer."
                else:
                    p_status = "High"
                    p_recommendation = "Reduce phosphorus fertilizer application."
            else:
                p_status = "Optimal"
                p_recommendation = "Maintain current phosphorus fertilization practices."
                
            fertility_analysis["phosphorus"] = {
                "value": p_value,
                "optimal_range": p_range,
                "status": p_status,
                "recommendation": p_recommendation
            }
            
            # Potassium analysis
            k_value = latest_data["potassium"]
            k_range = optimal_ranges["potassium"]
            
            if k_value < k_range[0]:
                if k_value < k_range[0] * 0.7:
                    k_status = "Severely Deficient"
                    k_recommendation = "Apply potassium-rich fertilizer as soon as possible."
                else:
                    k_status = "Deficient"
                    k_recommendation = "Consider applying potassium-rich fertilizer."
            elif k_value > k_range[1]:
                if k_value > k_range[1] * 1.3:
                    k_status = "Excess"
                    k_recommendation = "Avoid applying potassium fertilizer."
                else:
                    k_status = "High"
                    k_recommendation = "Reduce potassium fertilizer application."
            else:
                k_status = "Optimal"
                k_recommendation = "Maintain current potassium fertilization practices."
                
            fertility_analysis["potassium"] = {
                "value": k_value,
                "optimal_range": k_range,
                "status": k_status,
                "recommendation": k_recommendation
            }
            
            # pH analysis
            ph_value = latest_data["ph"]
            ph_range = optimal_ranges["ph"]
            
            if ph_value < ph_range[0]:
                if ph_value < ph_range[0] - 0.5:
                    ph_status = "Too Acidic"
                    ph_recommendation = "Apply lime to increase soil pH."
                else:
                    ph_status = "Mildly Acidic"
                    ph_recommendation = "Consider applying lime to increase soil pH slightly."
            elif ph_value > ph_range[1]:
                if ph_value > ph_range[1] + 0.5:
                    ph_status = "Too Alkaline"
                    ph_recommendation = "Apply sulfur or acidic organic matter to decrease soil pH."
                else:
                    ph_status = "Mildly Alkaline"
                    ph_recommendation = "Consider applying acidic organic matter to decrease soil pH slightly."
            else:
                ph_status = "Optimal"
                ph_recommendation = "Maintain current soil pH management practices."
                
            fertility_analysis["ph"] = {
                "value": ph_value,
                "optimal_range": ph_range,
                "status": ph_status,
                "recommendation": ph_recommendation
            }
            
            # Overall fertility assessment
            status_scores = {
                "Severely Deficient": 0,
                "Deficient": 1,
                "Mildly Acidic": 2,
                "Mildly Alkaline": 2,
                "High": 2,
                "Optimal": 3,
                "Excess": 1,
                "Too Acidic": 0,
                "Too Alkaline": 0
            }
            
            statuses = [
                fertility_analysis["nitrogen"]["status"],
                fertility_analysis["phosphorus"]["status"],
                fertility_analysis["potassium"]["status"],
                fertility_analysis["ph"]["status"]
            ]
            
            scores = [status_scores.get(status, 0) for status in statuses]
            avg_score = sum(scores) / len(scores)
            
            if avg_score >= 2.5:
                overall_status = "Good"
                overall_recommendation = "Maintain current soil fertility management practices."
            elif avg_score >= 1.5:
                overall_status = "Fair"
                overall_recommendation = "Follow specific nutrient recommendations to improve soil fertility."
            else:
                overall_status = "Poor"
                overall_recommendation = "Significant soil fertility issues detected. Follow specific recommendations for each nutrient and consider consulting an agronomist."
                
            return {
                "timestamp": latest_data["timestamp"],
                "overall_status": overall_status,
                "overall_recommendation": overall_recommendation,
                "nutrients": fertility_analysis
            }
            
        except Exception as e:
            self.logger.error(f"Error analyzing soil fertility: {str(e)}")
            return None

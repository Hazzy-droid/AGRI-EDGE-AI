import os
import logging
import numpy as np
from datetime import datetime, timedelta
import requests
from io import BytesIO

logger = logging.getLogger(__name__)

class SatelliteProcessor:
    """Class for processing satellite imagery for agricultural insights"""
    
    def __init__(self, api_key=None):
        self.api_key = api_key or os.environ.get('SATELLITE_API_KEY', '')
        self.base_url = "https://api.sentinel-hub.com/oauth/token"
        self.sentinel_hub_url = "https://services.sentinel-hub.com/api/v1/process"
        self.logger = logging.getLogger(__name__)
        
    def get_auth_token(self):
        """Get authentication token for Sentinel Hub API"""
        if not self.api_key:
            self.logger.warning("No Sentinel Hub API key provided")
            return None
            
        try:
            response = requests.post(
                self.base_url,
                data={
                    'grant_type': 'client_credentials',
                    'client_id': self.api_key.split(':')[0],
                    'client_secret': self.api_key.split(':')[1]
                }
            )
            if response.status_code == 200:
                return response.json().get('access_token')
            else:
                self.logger.error(f"Failed to get auth token: {response.status_code}")
                return None
        except Exception as e:
            self.logger.error(f"Error getting auth token: {str(e)}")
            return None
    
    def get_satellite_image(self, bbox, date_from, date_to, cloud_coverage_max=20):
        """
        Get satellite image for a specific bounding box and date range
        
        Args:
            bbox (list): Bounding box coordinates [min_lon, min_lat, max_lon, max_lat]
            date_from (str): Start date in format 'YYYY-MM-DD'
            date_to (str): End date in format 'YYYY-MM-DD'
            cloud_coverage_max (int): Maximum cloud coverage percentage
            
        Returns:
            dict: Dictionary with image data and metadata
        """
        token = self.get_auth_token()
        if not token:
            return None
            
        try:
            # Example request for Sentinel-2 L2A data
            payload = {
                "input": {
                    "bounds": {
                        "bbox": bbox
                    },
                    "data": [
                        {
                            "dataFilter": {
                                "timeRange": {
                                    "from": f"{date_from}T00:00:00Z",
                                    "to": f"{date_to}T23:59:59Z"
                                },
                                "maxCloudCoverage": cloud_coverage_max
                            },
                            "type": "sentinel-2-l2a"
                        }
                    ]
                },
                "output": {
                    "width": 512,
                    "height": 512,
                    "responses": [
                        {
                            "identifier": "default",
                            "format": {
                                "type": "image/png"
                            }
                        }
                    ]
                },
                "evalscript": """
                    //VERSION=3
                    function setup() {
                        return {
                            input: ["B02", "B03", "B04", "B08", "SCL"],
                            output: { bands: 4 }
                        };
                    }
                    
                    function evaluatePixel(sample) {
                        // Calculate NDVI: (NIR - RED) / (NIR + RED)
                        var ndvi = (sample.B08 - sample.B04) / (sample.B08 + sample.B04);
                        
                        // Return RGBA
                        return [sample.B04 * 2.5, sample.B03 * 2.5, sample.B02 * 2.5, ndvi];
                    }
                """
            }
            
            headers = {
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json"
            }
            
            response = requests.post(
                self.sentinel_hub_url,
                json=payload,
                headers=headers
            )
            
            if response.status_code == 200:
                return {
                    "image": BytesIO(response.content),
                    "date_acquired": date_to,
                    "cloud_coverage": cloud_coverage_max
                }
            else:
                self.logger.error(f"Failed to get satellite image: {response.status_code}")
                return None
                
        except Exception as e:
            self.logger.error(f"Error getting satellite image: {str(e)}")
            return None
    
    def calculate_ndvi(self, nir_band, red_band):
        """
        Calculate Normalized Difference Vegetation Index
        
        Args:
            nir_band (numpy.ndarray): Near-infrared band
            red_band (numpy.ndarray): Red band
            
        Returns:
            numpy.ndarray: NDVI values
        """
        try:
            # Avoid division by zero
            denominator = nir_band + red_band
            ndvi = np.where(
                denominator > 0,
                (nir_band - red_band) / denominator,
                0
            )
            return ndvi
        except Exception as e:
            self.logger.error(f"Error calculating NDVI: {str(e)}")
            return None
    
    def calculate_ndmi(self, nir_band, swir_band):
        """
        Calculate Normalized Difference Moisture Index
        
        Args:
            nir_band (numpy.ndarray): Near-infrared band
            swir_band (numpy.ndarray): Short-wave infrared band
            
        Returns:
            numpy.ndarray: NDMI values
        """
        try:
            # Avoid division by zero
            denominator = nir_band + swir_band
            ndmi = np.where(
                denominator > 0,
                (nir_band - swir_band) / denominator,
                0
            )
            return ndmi
        except Exception as e:
            self.logger.error(f"Error calculating NDMI: {str(e)}")
            return None
    
    def analyze_crop_health(self, ndvi_values):
        """
        Analyze crop health based on NDVI values
        
        Args:
            ndvi_values (numpy.ndarray): NDVI values
            
        Returns:
            dict: Dictionary with crop health analysis
        """
        try:
            # NDVI thresholds for different crop health levels
            poor_threshold = 0.2
            fair_threshold = 0.4
            good_threshold = 0.6
            
            # Calculate percentage of each health level
            total_pixels = ndvi_values.size
            poor_pixels = np.sum(ndvi_values < poor_threshold)
            fair_pixels = np.sum((ndvi_values >= poor_threshold) & (ndvi_values < fair_threshold))
            good_pixels = np.sum((ndvi_values >= fair_threshold) & (ndvi_values < good_threshold))
            excellent_pixels = np.sum(ndvi_values >= good_threshold)
            
            poor_percent = (poor_pixels / total_pixels) * 100
            fair_percent = (fair_pixels / total_pixels) * 100
            good_percent = (good_pixels / total_pixels) * 100
            excellent_percent = (excellent_pixels / total_pixels) * 100
            
            # Determine overall health status
            if excellent_percent > 60:
                overall_status = "Excellent"
            elif good_percent > 60:
                overall_status = "Good"
            elif fair_percent > 60:
                overall_status = "Fair"
            else:
                overall_status = "Poor"
                
            return {
                "overall_status": overall_status,
                "poor_percent": poor_percent,
                "fair_percent": fair_percent,
                "good_percent": good_percent,
                "excellent_percent": excellent_percent,
                "average_ndvi": np.mean(ndvi_values)
            }
        except Exception as e:
            self.logger.error(f"Error analyzing crop health: {str(e)}")
            return None
    
    def detect_water_stress(self, ndmi_values):
        """
        Detect water stress based on NDMI values
        
        Args:
            ndmi_values (numpy.ndarray): NDMI values
            
        Returns:
            dict: Dictionary with water stress analysis
        """
        try:
            # NDMI thresholds for different water stress levels
            severe_threshold = 0.0
            moderate_threshold = 0.2
            low_threshold = 0.4
            
            # Calculate percentage of each stress level
            total_pixels = ndmi_values.size
            severe_pixels = np.sum(ndmi_values < severe_threshold)
            moderate_pixels = np.sum((ndmi_values >= severe_threshold) & (ndmi_values < moderate_threshold))
            low_pixels = np.sum((ndmi_values >= moderate_threshold) & (ndmi_values < low_threshold))
            no_stress_pixels = np.sum(ndmi_values >= low_threshold)
            
            severe_percent = (severe_pixels / total_pixels) * 100
            moderate_percent = (moderate_pixels / total_pixels) * 100
            low_percent = (low_pixels / total_pixels) * 100
            no_stress_percent = (no_stress_pixels / total_pixels) * 100
            
            # Determine overall water stress status
            if severe_percent > 30:
                overall_status = "Severe Water Stress"
            elif moderate_percent > 30:
                overall_status = "Moderate Water Stress"
            elif low_percent > 30:
                overall_status = "Low Water Stress"
            else:
                overall_status = "No Water Stress"
                
            return {
                "overall_status": overall_status,
                "severe_percent": severe_percent,
                "moderate_percent": moderate_percent,
                "low_percent": low_percent,
                "no_stress_percent": no_stress_percent,
                "average_ndmi": np.mean(ndmi_values)
            }
        except Exception as e:
            self.logger.error(f"Error detecting water stress: {str(e)}")
            return None

    def get_historical_ndvi_series(self, bbox, start_date, end_date, interval_days=15):
        """
        Get historical NDVI time series for a specific area
        
        Args:
            bbox (list): Bounding box coordinates [min_lon, min_lat, max_lon, max_lat]
            start_date (str): Start date in format 'YYYY-MM-DD'
            end_date (str): End date in format 'YYYY-MM-DD'
            interval_days (int): Interval between images in days
            
        Returns:
            list: List of dictionaries with date and average NDVI
        """
        try:
            # Convert string dates to datetime objects
            start = datetime.strptime(start_date, '%Y-%m-%d')
            end = datetime.strptime(end_date, '%Y-%m-%d')
            
            ndvi_series = []
            current_date = start
            
            while current_date <= end:
                # Format the current date and the date after interval_days
                date_from = current_date.strftime('%Y-%m-%d')
                date_to = (current_date + timedelta(days=interval_days)).strftime('%Y-%m-%d')
                
                # Get image for the current time interval
                image_data = self.get_satellite_image(bbox, date_from, date_to)
                
                if image_data:
                    # Process the image to get NDVI
                    # This is a simplified example - in a real system we would extract 
                    # the bands and calculate actual NDVI
                    
                    # For demo purposes, generate a random NDVI value between 0 and 1
                    # In real implementation, we would calculate this from the image data
                    average_ndvi = 0.3 + 0.4 * np.random.random()
                    
                    ndvi_series.append({
                        "date": date_to,
                        "average_ndvi": average_ndvi
                    })
                
                # Move to the next interval
                current_date += timedelta(days=interval_days)
            
            return ndvi_series
            
        except Exception as e:
            self.logger.error(f"Error getting historical NDVI series: {str(e)}")
            return None

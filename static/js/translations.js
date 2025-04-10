// Translations for Climate-Smart Agriculture Platform

// Define available languages and translations
const translations = {
    'en': {
        // Common elements
        'dashboard': 'Dashboard',
        'satellite_imagery': 'Satellite Imagery',
        'weather_forecast': 'Weather Forecast',
        'soil_monitoring': 'Soil Monitoring',
        'recommendations': 'Recommendations',
        'settings': 'Settings',
        'dashboard_desc': 'Overview of your farm\'s current status and key metrics',
        'satellite_desc': 'Monitor your crops using multi-spectral satellite imagery',
        'weather_desc': 'Hyper-local weather forecasting for your farm',
        'soil_desc': 'Monitor soil health with real-time sensor data',
        'recommendations_desc': 'Personalized agricultural recommendations for your farm',
        'settings_desc': 'Customize your platform experience',
        
        // Weather-related
        'current_weather': 'Current Weather',
        'weather': 'Weather',
        'temperature': 'Temperature',
        'humidity': 'Humidity',
        'precipitation': 'Precipitation',
        'wind': 'Wind',
        'pressure': 'Pressure',
        'clouds': 'Clouds',
        '7_day_forecast': '7-Day Forecast',
        'hourly_forecast': 'Hourly Forecast',
        'today': 'Today',
        'tomorrow': 'Tomorrow',
        'updated_at': 'Updated at',
        'weather_unavailable': 'Weather data unavailable',
        'view_forecast': 'View Forecast',
        'weather_map': 'Weather Map',
        'rain': 'Rain',
        
        // Satellite-related
        'satellite_view': 'Satellite View',
        'ndvi_scale': 'NDVI Scale',
        'low': 'Low',
        'high': 'High',
        'current_ndvi': 'Current NDVI',
        'crop_health_analysis': 'Crop Health Analysis',
        'crop_health_breakdown': 'Crop Health Breakdown',
        'excellent': 'Excellent',
        'good': 'Good',
        'fair': 'Fair',
        'poor': 'Poor',
        'water_stress_analysis': 'Water Stress Analysis',
        'no_stress': 'No Stress',
        'low_stress': 'Low',
        'moderate_stress': 'Moderate',
        'severe_stress': 'Severe',
        'recommended_actions': 'Recommended Actions',
        'irrigation_recommended': 'Irrigation recommended in areas with water stress',
        'inspect_poor_areas': 'Inspect areas with poor crop health',
        'consider_fertilizer': 'Consider additional nutrients in areas with fair crop health',
        'ndvi_trend': 'NDVI Trend Over Time',
        'select_farm': 'Select Farm',
        'date_range': 'Date Range',
        'image_type': 'Image Type',
        
        // Soil-related
        'soil_moisture': 'Soil Moisture',
        'soil_temperature': 'Soil Temperature',
        'soil_ph': 'Soil pH',
        'soil_ec': 'Electrical Conductivity',
        'soil_fertility': 'Soil Fertility',
        'nitrogen': 'Nitrogen',
        'phosphorus': 'Phosphorus',
        'potassium': 'Potassium',
        'low_moisture': 'Low',
        'optimal_moisture': 'Optimal',
        'high_moisture': 'High',
        'soil_data_unavailable': 'Soil data unavailable',
        'view_soil_data': 'View Soil Data',
        'moisture_status': 'Moisture Status',
        'fertility_status': 'Fertility Status',
        'sensor_readings': 'Sensor Readings',
        'nutrient_levels': 'Nutrient Levels',
        
        // Crop-related
        'crop_health': 'Crop Health',
        'crop_type': 'Crop Type',
        'crop_stage': 'Crop Stage',
        'crop_calendar': 'Crop Calendar',
        'planting_date': 'Planting Date',
        'harvest_date': 'Harvest Date',
        'days_to_harvest': 'Days to Harvest',
        'crop_health_good': 'Your crops are in good health',
        'view_details': 'View Details',
        'farm_map': 'Farm Map',
        
        // Recommendations-related
        'irrigation': 'Irrigation',
        'fertilization': 'Fertilization',
        'pest_control': 'Pest Control',
        'planting': 'Planting',
        'harvesting': 'Harvesting',
        'high_priority': 'High Priority',
        'medium_priority': 'Medium Priority',
        'low_priority': 'Low Priority',
        'no_recommendations': 'No recommendations available',
        'view_all_recommendations': 'View All',
        'implementation_status': 'Implementation Status',
        'mark_as_implemented': 'Mark as Implemented',
        'mark_as_pending': 'Mark as Pending',
        'date_recommended': 'Date Recommended',
        'upcoming_activities': 'Upcoming Activities',
        
        // Settings-related
        'language': 'Language',
        'notification_settings': 'Notification Settings',
        'units': 'Units',
        'metric': 'Metric',
        'imperial': 'Imperial',
        'account_settings': 'Account Settings',
        'data_sync': 'Data Sync',
        'last_sync': 'Last Sync',
        'offline_data': 'Offline Data',
        'clear_cache': 'Clear Cache',
        'save_settings': 'Save Settings',
        
        // Planting recommendations
        'planting_recommendations': 'Planting Recommendations',
        'planting_recommendations_desc': 'Based on current and forecasted weather conditions, here are planting recommendations for your region:',
        'crop': 'Crop',
        'suitability': 'Suitability',
        'score': 'Score',
        'notes': 'Notes',
        
        // Status terms
        'favorable': 'Favorable',
        'unfavorable': 'Unfavorable',
        'moderate': 'Moderate',
        'high': 'High',
        'low': 'Low',
        
        // Agricultural impact
        'agricultural_impact': 'Agricultural Impact',
        'irrigation_needs': 'Irrigation Needs',
        'pest_risk': 'Pest Risk',
        'growing_conditions': 'Growing Conditions',
        'spraying_conditions': 'Spraying Conditions',
        'irrigation_detail': 'Consider irrigation in the next 2-3 days due to low expected rainfall',
        'pest_risk_detail': 'High humidity and moderate temperatures increase risk of fungal diseases',
        'growing_conditions_detail': 'Temperatures and light conditions are optimal for crop development',
        'spraying_conditions_detail': 'High winds and chance of rain make it unsuitable for pesticide application',
        
        // Misc
        'zone': 'Zone',
        'average_ndvi': 'Average NDVI',
        'health_status': 'Health Status',
        'download_data': 'Download Data',
        'download_desc': 'Download satellite imagery and analysis reports',
        'satellite_image': 'Satellite Image',
        'ndvi_data': 'NDVI Data',
        'analysis_report': 'Analysis Report',
        'shapefile': 'Shapefile',
        'update_forecast': 'Update Forecast'
    },
    
    'fr': {
        // Common elements
        'dashboard': 'Tableau de Bord',
        'satellite_imagery': 'Imagerie Satellite',
        'weather_forecast': 'Prévisions Météo',
        'soil_monitoring': 'Surveillance du Sol',
        'recommendations': 'Recommandations',
        'settings': 'Paramètres',
        'dashboard_desc': 'Aperçu de l\'état actuel de votre exploitation et des indicateurs clés',
        'satellite_desc': 'Surveillez vos cultures à l\'aide d\'imagerie satellite multispectrale',
        'weather_desc': 'Prévisions météorologiques hyper-locales pour votre exploitation',
        'soil_desc': 'Surveillez la santé du sol avec des données de capteur en temps réel',
        'recommendations_desc': 'Recommandations agricoles personnalisées pour votre exploitation',
        'settings_desc': 'Personnalisez votre expérience de plateforme',
        
        // Weather-related
        'current_weather': 'Météo Actuelle',
        'weather': 'Météo',
        'temperature': 'Température',
        'humidity': 'Humidité',
        'precipitation': 'Précipitations',
        'wind': 'Vent',
        'pressure': 'Pression',
        'clouds': 'Nuages',
        '7_day_forecast': 'Prévisions sur 7 Jours',
        'hourly_forecast': 'Prévisions Horaires',
        'today': 'Aujourd\'hui',
        'tomorrow': 'Demain',
        'updated_at': 'Mis à jour à',
        'weather_unavailable': 'Données météo indisponibles',
        'view_forecast': 'Voir les Prévisions',
        'weather_map': 'Carte Météo',
        'rain': 'Pluie',
        
        // More translations would follow the same pattern
        // This is a subset for demonstration purposes
        'crop_health': 'Santé des Cultures',
        'soil_moisture': 'Humidité du Sol',
        'view_details': 'Voir les Détails',
        'farm_map': 'Carte de l\'Exploitation',
        'view_all_recommendations': 'Voir Tout'
    },
    
    'sw': {
        // Common elements (Swahili)
        'dashboard': 'Dashibodi',
        'satellite_imagery': 'Picha za Satelaiti',
        'weather_forecast': 'Utabiri wa Hali ya Hewa',
        'soil_monitoring': 'Ufuatiliaji wa Udongo',
        'recommendations': 'Mapendekezo',
        'settings': 'Mipangilio',
        
        // This is a subset for demonstration purposes
        'crop_health': 'Afya ya Mazao',
        'soil_moisture': 'Unyevu wa Udongo',
        'view_details': 'Ona Maelezo',
        'farm_map': 'Ramani ya Shamba',
        'view_all_recommendations': 'Ona Yote'
    }
    
    // Additional languages would be added here
};

// Get current language from local storage or default to English
function getCurrentLanguage() {
    return localStorage.getItem('language') || 'en';
}

// Translate a single key
function translateKey(key, language) {
    const currentLang = language || getCurrentLanguage();
    
    // If the language is available and the key exists in that language
    if (translations[currentLang] && translations[currentLang][key]) {
        return translations[currentLang][key];
    }
    
    // Fallback to English
    if (translations['en'] && translations['en'][key]) {
        return translations['en'][key];
    }
    
    // If no translation is found, return the key itself
    return key;
}

// Translate all elements with translate class
function translatePage(language) {
    const currentLang = language || getCurrentLanguage();
    const translateElements = document.querySelectorAll('.translate');
    
    translateElements.forEach(element => {
        const key = element.getAttribute('data-key');
        if (key) {
            element.textContent = translateKey(key, currentLang);
        }
    });
}

// Export functions for use in other modules
window.translations = {
    getCurrentLanguage,
    translateKey,
    translatePage
};

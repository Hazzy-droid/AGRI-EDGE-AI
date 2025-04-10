// Offline functionality for Climate-Smart Agriculture Platform

// Service Worker registration
if ('serviceWorker' in navigator) {
    window.addEventListener('load', function() {
        navigator.serviceWorker.register('/static/js/service-worker.js')
            .then(function(registration) {
                console.log('ServiceWorker registration successful with scope: ', registration.scope);
            })
            .catch(function(error) {
                console.log('ServiceWorker registration failed: ', error);
            });
    });
}

// Offline data management
class OfflineDataManager {
    constructor() {
        this.localStorageKeys = {
            weatherData: 'weatherData',
            soilData: 'soilData',
            satelliteData: 'satelliteData',
            recommendations: 'recommendations',
            lastSyncTime: 'lastSyncTime'
        };
        
        // Set up synchronization when online
        window.addEventListener('online', this.syncDataWhenOnline.bind(this));
    }
    
    // Save data to localStorage
    saveData(key, data) {
        try {
            localStorage.setItem(key, JSON.stringify({
                data: data,
                timestamp: new Date().toISOString()
            }));
            return true;
        } catch (error) {
            console.error(`Error saving offline data (${key}):`, error);
            return false;
        }
    }
    
    // Get data from localStorage
    getData(key) {
        try {
            const storedData = localStorage.getItem(key);
            if (!storedData) return null;
            
            return JSON.parse(storedData);
        } catch (error) {
            console.error(`Error retrieving offline data (${key}):`, error);
            return null;
        }
    }
    
    // Check if we have valid cached data that's not too old
    hasValidData(key, maxAgeHours = 24) {
        const data = this.getData(key);
        if (!data) return false;
        
        const timestamp = new Date(data.timestamp);
        const now = new Date();
        const hoursDiff = (now - timestamp) / (1000 * 60 * 60);
        
        return hoursDiff <= maxAgeHours;
    }
    
    // Save weather data for offline use
    saveWeatherData(weatherData) {
        return this.saveData(this.localStorageKeys.weatherData, weatherData);
    }
    
    // Get cached weather data
    getWeatherData() {
        const data = this.getData(this.localStorageKeys.weatherData);
        return data ? data.data : null;
    }
    
    // Save soil data for offline use
    saveSoilData(soilData) {
        return this.saveData(this.localStorageKeys.soilData, soilData);
    }
    
    // Get cached soil data
    getSoilData() {
        const data = this.getData(this.localStorageKeys.soilData);
        return data ? data.data : null;
    }
    
    // Save satellite data for offline use
    saveSatelliteData(satelliteData) {
        return this.saveData(this.localStorageKeys.satelliteData, satelliteData);
    }
    
    // Get cached satellite data
    getSatelliteData() {
        const data = this.getData(this.localStorageKeys.satelliteData);
        return data ? data.data : null;
    }
    
    // Save recommendations for offline use
    saveRecommendations(recommendations) {
        return this.saveData(this.localStorageKeys.recommendations, recommendations);
    }
    
    // Get cached recommendations
    getRecommendations() {
        const data = this.getData(this.localStorageKeys.recommendations);
        return data ? data.data : null;
    }
    
    // Determine if we should fetch from API or use cached data
    shouldFetchFromAPI(key, maxAgeHours = 6) {
        // If offline, always use cached data
        if (!navigator.onLine) return false;
        
        // If we don't have valid data, fetch from API
        if (!this.hasValidData(key, maxAgeHours)) return true;
        
        // Check if it's been a while since last sync
        const lastSync = localStorage.getItem(this.localStorageKeys.lastSyncTime);
        if (!lastSync) return true;
        
        const syncTime = new Date(lastSync);
        const now = new Date();
        const hoursDiff = (now - syncTime) / (1000 * 60 * 60);
        
        // Sync if it's been more than the specified time
        return hoursDiff > maxAgeHours;
    }
    
    // Update last sync time
    updateLastSyncTime() {
        localStorage.setItem(this.localStorageKeys.lastSyncTime, new Date().toISOString());
    }
    
    // Sync data when online
    syncDataWhenOnline() {
        if (navigator.onLine) {
            console.log('Device is online, syncing data...');
            
            // For each data type, check if we should sync it
            if (this.shouldFetchFromAPI(this.localStorageKeys.weatherData)) {
                this.fetchAndSaveWeatherData();
            }
            
            if (this.shouldFetchFromAPI(this.localStorageKeys.soilData)) {
                this.fetchAndSaveSoilData();
            }
            
            if (this.shouldFetchFromAPI(this.localStorageKeys.satelliteData)) {
                this.fetchAndSaveSatelliteData();
            }
            
            if (this.shouldFetchFromAPI(this.localStorageKeys.recommendations)) {
                this.fetchAndSaveRecommendations();
            }
            
            this.updateLastSyncTime();
        }
    }
    
    // Fetch and save weather data
    fetchAndSaveWeatherData() {
        // In a real implementation, this would fetch from API
        // For now, we'll implement a placeholder that would be replaced
        console.log('Fetching and saving weather data...');
        // fetch('/api/weather_data').then(/* ... */);
    }
    
    // Fetch and save soil data
    fetchAndSaveSoilData() {
        console.log('Fetching and saving soil data...');
        // fetch('/api/soil_data').then(/* ... */);
    }
    
    // Fetch and save satellite data
    fetchAndSaveSatelliteData() {
        console.log('Fetching and saving satellite data...');
        // fetch('/api/satellite_data').then(/* ... */);
    }
    
    // Fetch and save recommendations
    fetchAndSaveRecommendations() {
        console.log('Fetching and saving recommendations...');
        // fetch('/api/fused_recommendations').then(/* ... */);
    }
    
    // Submit cached requests when back online
    submitCachedRequests() {
        const pendingRequests = this.getData('pendingRequests');
        if (!pendingRequests || !pendingRequests.data || !pendingRequests.data.length) return;
        
        console.log('Submitting cached requests...');
        
        pendingRequests.data.forEach(request => {
            fetch(request.url, {
                method: request.method,
                headers: request.headers,
                body: request.body
            })
            .then(response => {
                console.log('Cached request submitted successfully:', request.url);
            })
            .catch(error => {
                console.error('Error submitting cached request:', error);
            });
        });
        
        // Clear pending requests
        this.saveData('pendingRequests', []);
    }
    
    // Queue a request for later submission when offline
    queueRequest(url, method, headers, body) {
        let pendingRequests = this.getData('pendingRequests');
        
        if (!pendingRequests || !pendingRequests.data) {
            pendingRequests = { data: [] };
        }
        
        pendingRequests.data.push({
            url,
            method,
            headers,
            body,
            timestamp: new Date().toISOString()
        });
        
        this.saveData('pendingRequests', pendingRequests.data);
        console.log('Request queued for later submission:', url);
    }
}

// Initialize the offline manager
const offlineManager = new OfflineDataManager();

// Function to handle API fetches with offline capability
async function fetchWithOffline(url, options = {}, cacheKey, maxAgeHours = 6) {
    // If we have a valid cache and should use it, return cached data
    if (cacheKey && !offlineManager.shouldFetchFromAPI(cacheKey, maxAgeHours)) {
        const cachedData = offlineManager.getData(cacheKey);
        if (cachedData) {
            console.log(`Using cached data for ${url}`);
            return cachedData.data;
        }
    }
    
    // If offline and no valid cache, handle gracefully
    if (!navigator.onLine) {
        if (options.method && options.method !== 'GET') {
            // Queue non-GET requests for later
            offlineManager.queueRequest(url, options.method, options.headers, options.body);
            return { success: false, offline: true, message: 'Request queued for submission when online' };
        }
        
        // For GET requests with no cache, return error
        return { success: false, offline: true, message: 'No data available offline' };
    }
    
    // Online, make the actual fetch
    try {
        const response = await fetch(url, options);
        if (!response.ok) {
            throw new Error(`HTTP error ${response.status}`);
        }
        
        const data = await response.json();
        
        // Cache the result if we have a cache key
        if (cacheKey) {
            offlineManager.saveData(cacheKey, data);
        }
        
        return data;
    } catch (error) {
        console.error('Fetch error:', error);
        
        // Try to use cached data as fallback
        if (cacheKey) {
            const cachedData = offlineManager.getData(cacheKey);
            if (cachedData) {
                console.log(`Fetch failed, using cached data for ${url}`);
                return {
                    ...cachedData.data,
                    fromCache: true,
                    cacheDate: cachedData.timestamp
                };
            }
        }
        
        return { 
            success: false, 
            error: error.message,
            message: 'Failed to fetch data and no offline data available'
        };
    }
}

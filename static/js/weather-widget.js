/**
 * Interactive Weather Visualization
 * Provides dynamic weather visualization for the dashboard
 */

document.addEventListener('DOMContentLoaded', function() {
    // Initialize the weather widget if it exists on the page
    const weatherWidgetContainer = document.getElementById('weatherWidget');
    if (!weatherWidgetContainer) return;
    
    // Weather icons mapping based on condition
    const weatherIcons = {
        'clear': 'fas fa-sun',
        'sunny': 'fas fa-sun',
        'partly-cloudy': 'fas fa-cloud-sun',
        'cloudy': 'fas fa-cloud',
        'rain': 'fas fa-cloud-rain',
        'showers': 'fas fa-cloud-showers-heavy',
        'thunderstorm': 'fas fa-bolt',
        'snow': 'fas fa-snowflake',
        'fog': 'fas fa-smog',
        'windy': 'fas fa-wind',
        'default': 'fas fa-cloud'
    };
    
    // Weather data for demonstration (would be replaced by API data)
    const sampleWeatherData = [
        { day: 'Today', temp: 28, condition: 'clear', humidity: 65, wind: 12, rain: 0 },
        { day: 'Tomorrow', temp: 27, condition: 'partly-cloudy', humidity: 70, wind: 10, rain: 20 },
        { day: 'Wednesday', temp: 25, condition: 'cloudy', humidity: 75, wind: 8, rain: 40 },
        { day: 'Thursday', temp: 23, condition: 'rain', humidity: 85, wind: 15, rain: 80 },
        { day: 'Friday', temp: 24, condition: 'partly-cloudy', humidity: 80, wind: 12, rain: 30 },
        { day: 'Saturday', temp: 26, condition: 'clear', humidity: 60, wind: 8, rain: 10 },
        { day: 'Sunday', temp: 29, condition: 'sunny', humidity: 55, wind: 6, rain: 0 }
    ];
    
    function getWeatherIcon(condition) {
        return weatherIcons[condition] || weatherIcons.default;
    }
    
    // Create the forecast cards
    function renderForecast(data) {
        weatherWidgetContainer.innerHTML = ''; // Clear container
        
        // Create current weather panel (first item in data)
        const currentWeather = data[0];
        const currentWeatherPanel = document.createElement('div');
        currentWeatherPanel.className = 'current-weather p-3 mb-3 rounded bg-gradient';
        currentWeatherPanel.style.background = 'linear-gradient(135deg, #1e4d92, #2c3e50)';
        
        currentWeatherPanel.innerHTML = `
            <div class="d-flex align-items-center justify-content-between">
                <div>
                    <h4 class="mb-0 text-white">Today's Weather</h4>
                    <p class="text-light mb-2">Your farm location</p>
                    <div class="d-flex align-items-center">
                        <span class="display-4 text-white">${currentWeather.temp}°C</span>
                        <div class="ms-3">
                            <div class="text-white mb-1">Humidity: ${currentWeather.humidity}%</div>
                            <div class="text-white mb-1">Wind: ${currentWeather.wind} km/h</div>
                            <div class="text-white">Rain probability: ${currentWeather.rain}%</div>
                        </div>
                    </div>
                </div>
                <div class="text-center">
                    <i class="${getWeatherIcon(currentWeather.condition)} weather-icon fa-4x text-light"></i>
                    <div class="text-white mt-2">${currentWeather.condition.replace('-', ' ').toUpperCase()}</div>
                </div>
            </div>
        `;
        
        weatherWidgetContainer.appendChild(currentWeatherPanel);
        
        // Create weekly forecast row
        const forecastRow = document.createElement('div');
        forecastRow.className = 'row g-2 mt-2';
        
        // Start from index 1 (tomorrow) since we've already shown today's weather
        for (let i = 1; i < data.length; i++) {
            const dayData = data[i];
            const dayCard = document.createElement('div');
            dayCard.className = 'col-6 col-md-2';
            
            dayCard.innerHTML = `
                <div class="forecast-day p-2 text-center rounded" style="background-color: rgba(255, 255, 255, 0.1);">
                    <div class="day-name text-white mb-2">${dayData.day}</div>
                    <i class="${getWeatherIcon(dayData.condition)} fa-2x text-light mb-2"></i>
                    <div class="temp text-white">${dayData.temp}°C</div>
                    <div class="rain-chance small text-light">
                        <i class="fas fa-tint me-1"></i> ${dayData.rain}%
                    </div>
                </div>
            `;
            
            forecastRow.appendChild(dayCard);
        }
        
        weatherWidgetContainer.appendChild(forecastRow);
        
        // Add a weather insights panel
        const insightsPanel = document.createElement('div');
        insightsPanel.className = 'mt-3 p-3 rounded';
        insightsPanel.style.backgroundColor = 'rgba(255, 255, 255, 0.1)';
        
        let farmingAdvice = '';
        const rainProb = currentWeather.rain;
        
        if (rainProb > 70) {
            farmingAdvice = 'Heavy rain expected. Consider postponing any outdoor activities and ensure proper drainage.';
        } else if (rainProb > 30) {
            farmingAdvice = 'Light to moderate rain possible. Good conditions for planting but monitor soil moisture levels.';
        } else if (currentWeather.temp > 30) {
            farmingAdvice = 'Hot conditions expected. Ensure crops have adequate water and consider shade for sensitive plants.';
        } else {
            farmingAdvice = 'Favorable farming conditions. Good time for field work and regular maintenance.';
        }
        
        insightsPanel.innerHTML = `
            <h5 class="text-white"><i class="fas fa-lightbulb me-2 text-warning"></i>Weather Insights</h5>
            <p class="text-light mb-0">${farmingAdvice}</p>
        `;
        
        weatherWidgetContainer.appendChild(insightsPanel);
    }
    
    // Initialize with sample data
    renderForecast(sampleWeatherData);
    
    // Add interactivity - toggle between temperature and precipitation view
    const viewToggleContainer = document.createElement('div');
    viewToggleContainer.className = 'btn-group btn-group-sm mb-3';
    viewToggleContainer.innerHTML = `
        <button type="button" class="btn btn-primary active" id="tempView">Temperature</button>
        <button type="button" class="btn btn-outline-primary" id="rainView">Precipitation</button>
    `;
    
    weatherWidgetContainer.parentNode.insertBefore(viewToggleContainer, weatherWidgetContainer);
    
    // Add event listeners for the toggle buttons
    document.getElementById('tempView').addEventListener('click', function() {
        this.classList.add('active');
        this.classList.remove('btn-outline-primary');
        this.classList.add('btn-primary');
        
        document.getElementById('rainView').classList.remove('active');
        document.getElementById('rainView').classList.remove('btn-primary');
        document.getElementById('rainView').classList.add('btn-outline-primary');
        
        // Update view to show temperature (already the default)
        const tempElements = document.querySelectorAll('.temp');
        const rainElements = document.querySelectorAll('.rain-chance');
        
        tempElements.forEach(el => el.style.display = 'block');
        rainElements.forEach(el => el.style.display = 'block');
    });
    
    document.getElementById('rainView').addEventListener('click', function() {
        this.classList.add('active');
        this.classList.remove('btn-outline-primary');
        this.classList.add('btn-primary');
        
        document.getElementById('tempView').classList.remove('active');
        document.getElementById('tempView').classList.remove('btn-primary');
        document.getElementById('tempView').classList.add('btn-outline-primary');
        
        // Update view to emphasize rain probability
        const tempElements = document.querySelectorAll('.temp');
        const rainElements = document.querySelectorAll('.rain-chance');
        
        tempElements.forEach(el => el.style.display = 'none');
        rainElements.forEach(el => {
            el.style.display = 'block';
            el.style.fontSize = '1.2rem';
            el.style.fontWeight = 'bold';
        });
    });
});
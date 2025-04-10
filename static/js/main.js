// Main JavaScript for Climate-Smart Agriculture Platform

document.addEventListener('DOMContentLoaded', function() {
    console.log('Climate-Smart Agriculture Platform initialized');
    
    // Initialize tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
    
    // Initialize popovers
    const popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });
    
    // Toggle sidebar on mobile
    const sidebarToggle = document.getElementById('sidebarToggle');
    const sidebar = document.getElementById('sidebar');
    const mainContent = document.querySelector('.main-content');
    
    if (sidebarToggle && sidebar) {
        sidebarToggle.addEventListener('click', function() {
            sidebar.classList.toggle('show');
            mainContent.classList.toggle('sidebar-shown');
        });
    }
    
    // Update last updated time
    updateLastUpdated();
    
    // Set up language selector
    setupLanguageSelector();
    
    // Initialize all translation elements
    translatePage();
    
    // Test connectivity and update connection status
    checkConnectivity();
    
    // Update temperature preview in navbar
    updateTempPreview();
});

// Update the last updated time in the footer
function updateLastUpdated() {
    const lastUpdatedElement = document.getElementById('lastUpdated');
    if (lastUpdatedElement) {
        const now = new Date();
        const formattedTime = now.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
        lastUpdatedElement.textContent = `Last updated: ${formattedTime}`;
    }
}

// Set up language selector dropdown
function setupLanguageSelector() {
    const languageSelector = document.getElementById('languageSelector');
    if (languageSelector) {
        // Get current language from session/local storage or use default
        const currentLanguage = localStorage.getItem('language') || 'en';
        languageSelector.value = currentLanguage;
        
        // Apply translations when language is changed
        languageSelector.addEventListener('change', function() {
            const selectedLanguage = this.value;
            localStorage.setItem('language', selectedLanguage);
            
            // Submit form to update language on server-side if the form exists
            const languageForm = document.getElementById('languageForm');
            if (languageForm) {
                languageForm.submit();
            } else {
                // If no form, just apply translations client-side
                translatePage(selectedLanguage);
            }
        });
    }
}

// Check connectivity and update status indicator
function checkConnectivity() {
    const connectionStatus = document.getElementById('connectionStatus');
    
    function updateStatus() {
        if (navigator.onLine) {
            connectionStatus.className = 'badge bg-success';
            connectionStatus.innerHTML = '<i class="fas fa-wifi me-1"></i> Online';
        } else {
            connectionStatus.className = 'badge bg-danger';
            connectionStatus.innerHTML = '<i class="fas fa-wifi-slash me-1"></i> Offline';
            
            // Show offline alert
            showOfflineAlert();
        }
    }
    
    // Initial check
    updateStatus();
    
    // Listen for online/offline events
    window.addEventListener('online', updateStatus);
    window.addEventListener('offline', updateStatus);
    
    // Check connectivity every 30 seconds
    setInterval(updateStatus, 30000);
}

// Show an alert when the app goes offline
function showOfflineAlert() {
    const offlineAlert = document.createElement('div');
    offlineAlert.className = 'alert alert-warning alert-dismissible fade show offline-alert';
    offlineAlert.role = 'alert';
    offlineAlert.innerHTML = `
        <i class="fas fa-exclamation-triangle me-2"></i>
        You are currently offline. The app will continue to work with limited functionality.
        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
    `;
    
    // If not already shown, add to the top of the main content
    if (!document.querySelector('.offline-alert')) {
        const mainContent = document.querySelector('.main-content .container-fluid');
        if (mainContent) {
            mainContent.prepend(offlineAlert);
            
            // Auto-remove after 5 seconds
            setTimeout(() => {
                offlineAlert.remove();
            }, 5000);
        }
    }
}

// Update temperature preview in navbar
function updateTempPreview() {
    const tempPreview = document.getElementById('tempPreview');
    
    if (tempPreview) {
        // Try to get current temperature from storage
        let currentTemp = localStorage.getItem('currentTemp');
        
        // If not available, use default value
        if (!currentTemp) {
            currentTemp = '25°C';
            localStorage.setItem('currentTemp', currentTemp);
        }
        
        tempPreview.textContent = currentTemp;
    }
}

// For farm selector dropdown in dashboard
const farmSelector = document.getElementById('farmSelector');
if (farmSelector) {
    farmSelector.addEventListener('change', function() {
        const farmId = this.value;
        window.location.href = `?farm_id=${farmId}`;
    });
}

// For date display on dashboard
function updateCurrentDate() {
    const currentDateElement = document.getElementById('currentDate');
    if (currentDateElement) {
        const now = new Date();
        const options = { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' };
        const formattedDate = now.toLocaleDateString(undefined, options);
        currentDateElement.textContent = formattedDate;
    }
}

// Initialize date display
updateCurrentDate();

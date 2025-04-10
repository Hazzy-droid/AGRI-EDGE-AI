/**
 * Video Tutorials Configuration
 * 
 * This file contains the configuration for all video tutorials across the platform.
 * Each page has its own default video tutorial that explains the functionality.
 */

// Main platform video tutorials
const VIDEO_TUTORIALS = {
    // Main platform overview video - shown on login page
    welcome: {
        path: "/static/videos/welcome.mp4",
        title: "Welcome to Climate-Smart Agriculture Platform",
        description: `<p>This video provides an overview of our platform, explaining how it integrates satellite imagery, 
        IoT soil sensors, and weather data to provide actionable agricultural insights for African farmers.</p>
        <p>Developed by high school students from Moi Forces Academy Nairobi, this platform aims to address food 
        security challenges through technology innovation.</p>`
    },
    
    // Dashboard page tutorial
    dashboard: {
        path: "/static/videos/dashboard.mp4",
        title: "Dashboard Tutorial",
        description: `<p>The dashboard provides a comprehensive overview of your farm's status, including weather conditions, 
        soil health, and crop recommendations.</p>
        <p>This video explains how to interpret the data visualizations and how to navigate to detailed sections.</p>`
    },
    
    // Satellite imagery page tutorial
    satellite: {
        path: "/static/videos/satellite.mp4",
        title: "Satellite Imagery Tutorial",
        description: `<p>Learn how to use the satellite imagery features to monitor your crops' health through NDVI (Normalized 
        Difference Vegetation Index) visualization.</p>
        <p>This video explains how to interpret the color-coded maps and historical data to make informed decisions.</p>`
    },
    
    // Weather forecasting page tutorial
    weather: {
        path: "/static/videos/weather.mp4",
        title: "Weather Forecasting Tutorial",
        description: `<p>The weather page provides detailed forecasts specifically calibrated for your farm location.</p>
        <p>This tutorial explains how to interpret the forecasts and use them for planning irrigation, 
        planting, and other farming activities.</p>`
    },
    
    // Soil monitoring page tutorial
    soil: {
        path: "/static/videos/soil.mp4",
        title: "Soil Monitoring Tutorial",
        description: `<p>Learn how to interpret soil moisture, fertility, and other key soil health indicators 
        on the soil monitoring page.</p>
        <p>This video explains how the IoT sensors work and how to use the data to optimize fertilization and irrigation.</p>`
    },
    
    // Recommendations page tutorial
    recommendations: {
        path: "/static/videos/recommendations.mp4",
        title: "Recommendations Tutorial",
        description: `<p>Our AI-powered recommendation system analyzes all available data to provide 
        specific advice for your farm.</p>
        <p>This tutorial explains how the recommendations are generated and how to implement them 
        for maximum crop yield and sustainability.</p>`
    },
    
    // Community page tutorial
    community: {
        path: "/static/videos/community.mp4",
        title: "Community Platform Tutorial",
        description: `<p>The community platform allows you to connect with other farmers, share knowledge, 
        and learn from their experiences.</p>
        <p>This tutorial shows how to create posts, comment, and filter content by category.</p>`
    },
    
    // Marketplace page tutorial
    marketplace: {
        path: "/static/videos/marketplace.mp4",
        title: "Marketplace Tutorial",
        description: `<p>The marketplace allows you to buy and sell agricultural products, equipment, and services.</p>
        <p>This video explains how to browse listings, create your own listings, and communicate with other users.</p>`
    },
    
    // Messaging page tutorial
    messages: {
        path: "/static/videos/messages.mp4",
        title: "Messaging System Tutorial",
        description: `<p>The messaging system allows secure communication between farmers, buyers, and sellers.</p>
        <p>This tutorial explains how to send messages, attach images, and manage conversations.</p>`
    },
    
    // Settings page tutorial
    settings: {
        path: "/static/videos/settings.mp4",
        title: "Settings Page Tutorial",
        description: `<p>The settings page allows you to customize your profile, notification preferences, 
        and farm information.</p>
        <p>This video shows how to update your details and set your preferences for the platform.</p>`
    },
    
    // Learning module tutorial
    learning: {
        path: "/static/videos/learning.mp4",
        title: "Learning Module Tutorial",
        description: `<p>Our learning module provides educational content about climate-smart agriculture practices.</p>
        <p>This tutorial explains how to navigate courses, complete quizzes, and earn achievements.</p>`
    }
};

// Handle video loading errors
function handleVideoError(videoPath) {
    const playerContainer = document.getElementById('videoPlayerContainer');
    if (playerContainer) {
        playerContainer.innerHTML = `
            <div class="text-center p-4">
                <i class="fas fa-film fa-3x mb-4 text-primary"></i>
                <h4>Video Tutorial Content</h4>
                <p class="mb-3 lead">This is a placeholder for the tutorial video that would be shown here.</p>
                <small class="text-muted">${videoPath}</small>
            </div>
        `;
    }
}

// Initialize the page-specific video tutorial
document.addEventListener("DOMContentLoaded", function() {
    // Try to determine which page we're on based on URL or page class
    const path = window.location.pathname;
    let pageName = "welcome"; // Default to welcome video
    
    // Map URL paths to video tutorial keys
    if (path.includes("dashboard")) {
        pageName = "dashboard";
    } else if (path.includes("satellite")) {
        pageName = "satellite";
    } else if (path.includes("weather")) {
        pageName = "weather";
    } else if (path.includes("soil")) {
        pageName = "soil";
    } else if (path.includes("recommendations")) {
        pageName = "recommendations";
    } else if (path.includes("community")) {
        pageName = "community";
    } else if (path.includes("marketplace")) {
        pageName = "marketplace";
    } else if (path.includes("messages")) {
        pageName = "messages";
    } else if (path.includes("settings")) {
        pageName = "settings";
    } else if (path.includes("learning")) {
        pageName = "learning";
    }
    
    // Get the tutorial data for this page
    const tutorial = VIDEO_TUTORIALS[pageName];
    
    // If we have setPageDefaultVideo function available, set the default video
    if (typeof setPageDefaultVideo === "function" && tutorial) {
        setPageDefaultVideo(tutorial.path, tutorial.title, tutorial.description);
    }
});
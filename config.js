// Environment configuration for Christopher Corbin Portfolio
// This file manages API endpoints and environment-specific settings

const CONFIG = {
    // API Endpoints
    CONTACT_API_URL: 'https://9rau1nnkg3.execute-api.us-east-1.amazonaws.com/prod/contact',
    
    // Environment settings
    ENVIRONMENT: 'production',  // 'development' | 'staging' | 'production'
    
    // Feature flags
    ENABLE_ANALYTICS: true,
    ENABLE_ERROR_LOGGING: true,
    
    // Form validation settings
    CONTACT_FORM: {
        MIN_MESSAGE_LENGTH: 10,
        MAX_MESSAGE_LENGTH: 1000,
        MAX_NAME_LENGTH: 100,
        REQUIRED_FIELDS: ['name', 'email', 'message']
    },
    
    // UI Settings
    NOTIFICATION_TIMEOUT: 5000,
    FORM_SUBMIT_TIMEOUT: 30000,
    
    // Analytics (if using Google Analytics)
    GOOGLE_ANALYTICS_ID: null, // Replace with your GA4 measurement ID if using analytics
    
    // Development settings (only used in development)
    DEV_SETTINGS: {
        MOCK_API_DELAY: 2000,
        ENABLE_CONSOLE_LOGS: true
    }
};

// Export for use in other files
if (typeof module !== 'undefined' && module.exports) {
    module.exports = CONFIG;
}

// Make available globally for browser
if (typeof window !== 'undefined') {
    window.PORTFOLIO_CONFIG = CONFIG;
}
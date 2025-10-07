// Development Environment Configuration for Christopher Corbin Portfolio
// This file manages API endpoints and environment-specific settings for DEV

const CONFIG = {
    // API Endpoints - DEV BACKEND
    CONTACT_API_URL: 'https://cdmwb9tdlj.execute-api.us-east-1.amazonaws.com/prod/contact',
    
    // Environment settings
    ENVIRONMENT: 'development',  // 'development' | 'staging' | 'production'
    
    // Feature flags
    ENABLE_ANALYTICS: false,  // Disabled in dev
    ENABLE_ERROR_LOGGING: true,
    ENABLE_DEBUG_MODE: true,  // Extra logging for dev
    
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
    
    // Analytics (disabled in dev)
    GOOGLE_ANALYTICS_ID: null, 
    
    // Development settings
    DEV_SETTINGS: {
        MOCK_API_DELAY: 1000,  // Shorter delay for dev testing
        ENABLE_CONSOLE_LOGS: true,
        SHOW_DEBUG_INFO: true,  // Show debug panel
        API_TIMEOUT: 10000
    }
};

// Development-specific functions
CONFIG.isDevelopment = () => CONFIG.ENVIRONMENT === 'development';
CONFIG.isProduction = () => CONFIG.ENVIRONMENT === 'production';

// Add dev environment indicator to page
if (CONFIG.isDevelopment()) {
    // Add dev banner to page
    const addDevBanner = () => {
        const banner = document.createElement('div');
        banner.style.cssText = `
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            background: linear-gradient(45deg, #ff6b35, #f7931e);
            color: white;
            text-align: center;
            padding: 5px 10px;
            font-size: 12px;
            font-weight: bold;
            z-index: 10000;
            box-shadow: 0 2px 5px rgba(0,0,0,0.2);
        `;
        banner.innerHTML = '🚧 DEVELOPMENT ENVIRONMENT - Testing Backend Integration 🚧';
        document.body.insertBefore(banner, document.body.firstChild);
        
        // Adjust body padding to account for banner
        document.body.style.paddingTop = '30px';
    };
    
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', addDevBanner);
    } else {
        addDevBanner();
    }
}

// Export for use in other files
if (typeof module !== 'undefined' && module.exports) {
    module.exports = CONFIG;
}

// Make available globally for browser
if (typeof window !== 'undefined') {
    window.PORTFOLIO_CONFIG = CONFIG;
    
    // Add debug logging in development
    if (CONFIG.isDevelopment()) {
        console.log('🔧 Development Environment Loaded');
        console.log('📡 API Endpoint:', CONFIG.CONTACT_API_URL);
        console.log('⚙️ Config:', CONFIG);
    }
}
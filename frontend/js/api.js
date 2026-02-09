/**
 * API Communication Layer
 * Handles all FastAPI backend interactions
 */

const API_BASE_URL = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1'
    ? 'http://localhost:8000'
    : ''; // Provide your production backend URL here, e.g., 'https://your-backend-service.onrender.com'


// API Key Management
const ApiKeyManager = {
    STORAGE_KEY: 'cyber_suraksha_api_key',

    get() {
        return localStorage.getItem(this.STORAGE_KEY) || '';
    },

    set(key) {
        localStorage.setItem(this.STORAGE_KEY, key);
    },

    clear() {
        localStorage.removeItem(this.STORAGE_KEY);
    },

    isConfigured() {
        return !!this.get();
    }
};

const API = {
    /**
     * Get headers with API key if configured
     */
    getHeaders() {
        const headers = {
            'Content-Type': 'application/json',
        };

        const apiKey = ApiKeyManager.get();
        if (apiKey) {
            headers['X-API-Key'] = apiKey;
        }

        return headers;
    },

    /**
     * Run the complete 4-node fraud analysis workflow
     */
    async analyzeFraud(data) {
        try {
            const response = await fetch(`${API_BASE_URL}/api/analyze`, {
                method: 'POST',
                headers: this.getHeaders(),
                body: JSON.stringify(data),
            });

            if (!response.ok) {
                const error = await response.json().catch(() => ({}));
                throw new Error(error.detail || `API error: ${response.status}`);
            }

            return await response.json();
        } catch (error) {
            console.error('Analyze fraud error:', error);
            throw error;
        }
    },

    /**
     * Quick triage analysis only
     */
    async triageOnly(complaint) {
        try {
            const response = await fetch(`${API_BASE_URL}/api/triage`, {
                method: 'POST',
                headers: this.getHeaders(),
                body: JSON.stringify({ complaint }),
            });

            if (!response.ok) {
                throw new Error(`API error: ${response.status}`);
            }

            return await response.json();
        } catch (error) {
            console.error('Triage error:', error);
            throw error;
        }
    },

    /**
     * Lookup nodal officers for a bank
     */
    async lookupNodalOfficer(bankName) {
        try {
            const response = await fetch(`${API_BASE_URL}/api/lookup-nodal`, {
                method: 'POST',
                headers: this.getHeaders(),
                body: JSON.stringify({ bank_name: bankName }),
            });

            if (!response.ok) {
                throw new Error(`API error: ${response.status}`);
            }

            return await response.json();
        } catch (error) {
            console.error('Nodal lookup error:', error);
            throw error;
        }
    },

    /**
     * Check suspect in I4C repository
     */
    async checkSuspect(suspectType, value) {
        try {
            const response = await fetch(`${API_BASE_URL}/api/check-suspect`, {
                method: 'POST',
                headers: this.getHeaders(),
                body: JSON.stringify({ suspect_type: suspectType, value }),
            });

            if (!response.ok) {
                throw new Error(`API error: ${response.status}`);
            }

            return await response.json();
        } catch (error) {
            console.error('Suspect check error:', error);
            throw error;
        }
    },

    /**
     * Get all scam types
     */
    async getScamTypes() {
        try {
            const response = await fetch(`${API_BASE_URL}/api/scam-types`);

            if (!response.ok) {
                throw new Error(`API error: ${response.status}`);
            }

            return await response.json();
        } catch (error) {
            console.error('Get scam types error:', error);
            throw error;
        }
    },

    /**
     * Get all banks
     */
    async getBanks() {
        try {
            const response = await fetch(`${API_BASE_URL}/api/banks`);

            if (!response.ok) {
                throw new Error(`API error: ${response.status}`);
            }

            return await response.json();
        } catch (error) {
            console.error('Get banks error:', error);
            throw error;
        }
    },

    /**
     * Get all nodal officers
     */
    async getAllNodalOfficers() {
        try {
            const response = await fetch(`${API_BASE_URL}/api/nodal-officers`);

            if (!response.ok) {
                throw new Error(`API error: ${response.status}`);
            }

            return await response.json();
        } catch (error) {
            console.error('Get nodal officers error:', error);
            throw error;
        }
    },

    /**
     * Health check with optional API key test
     */
    async healthCheck(testApiKey = null) {
        try {
            const headers = {};
            if (testApiKey) {
                headers['X-API-Key'] = testApiKey;
            } else if (ApiKeyManager.isConfigured()) {
                headers['X-API-Key'] = ApiKeyManager.get();
            }

            const response = await fetch(`${API_BASE_URL}/api/health`, { headers });
            return await response.json();
        } catch (error) {
            console.error('Health check error:', error);
            return { status: 'offline', error: error.message };
        }
    },

    /**
     * Test API key validity
     */
    async testApiKey(apiKey) {
        try {
            const response = await fetch(`${API_BASE_URL}/api/test-key`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-API-Key': apiKey
                }
            });
            return await response.json();
        } catch (error) {
            return { valid: false, error: error.message };
        }
    }
};

// Make API and ApiKeyManager available globally
window.API = API;
window.ApiKeyManager = ApiKeyManager;

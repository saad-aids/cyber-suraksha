/**
 * Cyber-Suraksha Main Application
 * Initialization and global functionality
 */

document.addEventListener('DOMContentLoaded', () => {
    initializeApp();
});

/**
 * Initialize the application
 */
async function initializeApp() {
    // Initialize components
    initNavigation();
    initGoldenTimer();
    initCharCounter();
    initSettingsModal();
    await loadBanks();
    await loadNodalDirectory();

    // Check API health
    checkAPIHealth();
    updateApiKeyWarning();
}

/**
 * Initialize navigation
 */
function initNavigation() {
    // Mobile menu toggle
    const mobileMenuBtn = document.getElementById('mobileMenuBtn');
    const navLinks = document.getElementById('navLinks');

    if (mobileMenuBtn && navLinks) {
        mobileMenuBtn.addEventListener('click', () => {
            navLinks.classList.toggle('active');
        });
    }

    // Smooth scroll for nav links
    document.querySelectorAll('.nav-link').forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            const targetId = link.getAttribute('href').substring(1);
            const target = document.getElementById(targetId);

            if (target) {
                target.scrollIntoView({ behavior: 'smooth' });

                // Close mobile menu
                navLinks.classList.remove('active');

                // Update active link
                document.querySelectorAll('.nav-link').forEach(l => l.classList.remove('active'));
                link.classList.add('active');
            }
        });
    });

    // Update active link on scroll
    window.addEventListener('scroll', () => {
        const sections = ['home', 'report', 'directory', 'how-it-works'];
        const scrollPos = window.scrollY + 100;

        sections.forEach(sectionId => {
            const section = document.getElementById(sectionId);
            if (section) {
                const top = section.offsetTop;
                const height = section.offsetHeight;

                if (scrollPos >= top && scrollPos < top + height) {
                    document.querySelectorAll('.nav-link').forEach(l => {
                        l.classList.remove('active');
                        if (l.getAttribute('href') === `#${sectionId}`) {
                            l.classList.add('active');
                        }
                    });
                }
            }
        });
    });
}

/**
 * Initialize Golden Hour Timer
 */
function initGoldenTimer() {
    let minutes = 60;
    let seconds = 0;

    const timerMinutes = document.getElementById('timerMinutes');
    const timerSeconds = document.getElementById('timerSeconds');

    if (!timerMinutes || !timerSeconds) return;

    const updateTimer = () => {
        timerMinutes.textContent = String(minutes).padStart(2, '0');
        timerSeconds.textContent = String(seconds).padStart(2, '0');

        if (seconds === 0) {
            if (minutes === 0) {
                // Timer expired
                document.querySelector('.timer-message').textContent =
                    '⚠️ Golden Hour expired - Still report to prevent further fraud!';
                return;
            }
            minutes--;
            seconds = 59;
        } else {
            seconds--;
        }

        // Change color when time is low
        if (minutes < 15) {
            timerMinutes.style.color = 'var(--danger)';
            timerSeconds.style.color = 'var(--danger)';
        }
    };

    // Update every second
    setInterval(updateTimer, 1000);
}

/**
 * Initialize character counter for complaint textarea
 */
function initCharCounter() {
    const complaint = document.getElementById('complaint');
    const charCount = document.getElementById('charCount');

    if (!complaint || !charCount) return;

    complaint.addEventListener('input', () => {
        const count = complaint.value.length;
        charCount.textContent = count;

        if (count >= 200) {
            charCount.style.color = 'var(--success)';
        } else if (count >= 100) {
            charCount.style.color = 'var(--warning)';
        } else {
            charCount.style.color = 'var(--text-muted)';
        }
    });
}

/**
 * Load banks into dropdown
 */
async function loadBanks() {
    const bankSelect = document.getElementById('bankName');
    if (!bankSelect) return;

    try {
        const response = await API.getBanks();

        if (response.success && response.banks) {
            response.banks.forEach(bank => {
                const option = document.createElement('option');
                option.value = bank;
                option.textContent = bank;
                bankSelect.appendChild(option);
            });
        }
    } catch (error) {
        console.error('Failed to load banks:', error);
        // Add fallback banks
        const fallbackBanks = [
            'State Bank of India',
            'HDFC Bank',
            'ICICI Bank',
            'Axis Bank',
            'Bank of Maharashtra',
            'Punjab National Bank',
            'Kotak Mahindra Bank',
            'Canara Bank',
            'Union Bank of India',
            'Paytm Payments Bank',
            'PhonePe',
            'Google Pay (GPay)'
        ];

        fallbackBanks.forEach(bank => {
            const option = document.createElement('option');
            option.value = bank;
            option.textContent = bank;
            bankSelect.appendChild(option);
        });
    }
}

/**
 * Load nodal officers directory
 */
async function loadNodalDirectory() {
    const nodalGrid = document.getElementById('nodalGrid');
    if (!nodalGrid) return;

    let officers = [];

    try {
        const response = await API.getAllNodalOfficers();
        if (response.success && response.officers) {
            officers = response.officers;
        }
    } catch (error) {
        console.error('Failed to load nodal officers:', error);
        // Use fallback data
        officers = getFallbackNodalOfficers();
    }

    renderNodalDirectory(officers);
    initNodalSearch(officers);
}

/**
 * Render nodal directory
 */
function renderNodalDirectory(officers) {
    const nodalGrid = document.getElementById('nodalGrid');
    if (!nodalGrid) return;

    nodalGrid.innerHTML = '';

    officers.forEach(officer => {
        const card = document.createElement('div');
        card.className = 'nodal-card';
        card.innerHTML = `
            <div class="nodal-card-header">
                <div class="bank-icon">🏦</div>
                <div>
                    <h4>${officer.bank_name}</h4>
                    <span class="region">${officer.region}</span>
                </div>
            </div>
            <div class="nodal-card-body">
                <div class="contact-row">
                    <span>👤</span>
                    <span>${officer.officer_name}</span>
                </div>
                <div class="contact-row">
                    <span>📧</span>
                    <a href="mailto:${officer.email}">${officer.email}</a>
                </div>
                <div class="contact-row">
                    <span>📞</span>
                    <a href="tel:${officer.phone}">${officer.phone}</a>
                </div>
            </div>
        `;
        nodalGrid.appendChild(card);
    });
}

/**
 * Initialize nodal officer search
 */
function initNodalSearch(officers) {
    const searchInput = document.getElementById('bankSearch');
    if (!searchInput) return;

    searchInput.addEventListener('input', (e) => {
        const query = e.target.value.toLowerCase();

        if (!query) {
            renderNodalDirectory(officers);
            return;
        }

        const filtered = officers.filter(officer =>
            officer.bank_name.toLowerCase().includes(query) ||
            officer.region.toLowerCase().includes(query)
        );

        renderNodalDirectory(filtered);
    });
}

/**
 * Check API health and show status
 */
async function checkAPIHealth() {
    try {
        const health = await API.healthCheck();

        if (health.status === 'healthy') {
            console.log('✅ Backend connected');
        } else if (health.status === 'degraded') {
            console.warn('⚠️ Backend running but LLM not configured');
        } else {
            console.error('❌ Backend offline');
        }
    } catch (error) {
        console.warn('⚠️ Backend not reachable - using offline mode');
    }
}

/**
 * Initialize Settings Modal
 */
function initSettingsModal() {
    const modal = document.getElementById('settingsModal');
    const settingsBtn = document.getElementById('settingsBtn');
    const closeBtn = document.getElementById('closeSettingsModal');
    const apiKeyInput = document.getElementById('apiKeyInput');
    const toggleVisibilityBtn = document.getElementById('toggleApiKeyVisibility');
    const saveBtn = document.getElementById('saveApiKey');
    const clearBtn = document.getElementById('clearApiKey');

    if (!modal || !settingsBtn) return;

    // Open modal
    settingsBtn.addEventListener('click', () => {
        modal.classList.add('active');
        // Load existing key
        const existingKey = ApiKeyManager.get();
        if (existingKey) {
            apiKeyInput.value = existingKey;
            updateApiStatus('configured', 'API key configured');
        }
    });

    // Close modal
    closeBtn.addEventListener('click', () => {
        modal.classList.remove('active');
    });

    // Close on overlay click
    modal.addEventListener('click', (e) => {
        if (e.target === modal) {
            modal.classList.remove('active');
        }
    });

    // Toggle password visibility
    toggleVisibilityBtn.addEventListener('click', () => {
        if (apiKeyInput.type === 'password') {
            apiKeyInput.type = 'text';
            toggleVisibilityBtn.textContent = '🔒';
        } else {
            apiKeyInput.type = 'password';
            toggleVisibilityBtn.textContent = '👁️';
        }
    });

    // Save API key
    saveBtn.addEventListener('click', async () => {
        const apiKey = apiKeyInput.value.trim();

        if (!apiKey) {
            updateApiStatus('error', 'Please enter an API key');
            return;
        }

        updateApiStatus('pending', 'Testing API key...');

        // Save the key
        ApiKeyManager.set(apiKey);

        // Test the key
        try {
            const health = await API.healthCheck(apiKey);
            if (health.llm_configured || health.status === 'healthy') {
                updateApiStatus('success', '✓ API key saved and verified');
                updateApiKeyWarning();
                showToast('API key saved successfully!');
            } else {
                updateApiStatus('success', '✓ API key saved (verification pending)');
                updateApiKeyWarning();
            }
        } catch (error) {
            updateApiStatus('success', '✓ API key saved');
            updateApiKeyWarning();
        }
    });

    // Clear API key
    clearBtn.addEventListener('click', () => {
        ApiKeyManager.clear();
        apiKeyInput.value = '';
        updateApiStatus('error', 'API key cleared');
        updateApiKeyWarning();
        showToast('API key cleared');
    });
}

/**
 * Update API status indicator in modal
 */
function updateApiStatus(status, message) {
    const indicator = document.getElementById('statusIndicator');
    const text = document.getElementById('statusText');

    if (!indicator || !text) return;

    indicator.className = 'status-indicator ' + status;
    text.textContent = message;
}

/**
 * Update API key warning banner
 */
function updateApiKeyWarning() {
    const warning = document.getElementById('apiWarning');
    if (!warning) return;

    if (ApiKeyManager.isConfigured()) {
        warning.style.display = 'none';
    } else {
        warning.style.display = 'flex';
    }
}

/**
 * Show toast notification
 */
function showToast(message, type = 'success') {
    const toast = document.getElementById('toast');
    const toastMessage = document.getElementById('toastMessage');

    if (!toast || !toastMessage) return;

    toastMessage.textContent = message;
    toast.style.background = type === 'error' ? 'var(--danger)' : 'var(--success)';
    toast.classList.add('show');

    setTimeout(() => {
        toast.classList.remove('show');
    }, 3000);
}

/**
 * Fallback nodal officers data
 */
function getFallbackNodalOfficers() {
    return [
        {
            bank_name: "Bank of Maharashtra",
            region: "Head Office (Recovery)",
            officer_name: "CGM Recovery",
            email: "cgmrecovery@bankofmaharashtra.bank.in",
            phone: "020-25614252"
        },
        {
            bank_name: "Bank of Maharashtra",
            region: "Mumbai City Zone",
            officer_name: "DZM Mumbai",
            email: "dzmmcz@bankofmaharashtra.bank.in",
            phone: "022-22671568"
        },
        {
            bank_name: "State Bank of India",
            region: "Nodal Officer (Cyber)",
            officer_name: "AGM Nodal Cyber",
            email: "agm.nodcyb@sbi.co.in",
            phone: "1800-111-109"
        },
        {
            bank_name: "HDFC Bank",
            region: "Pension/Nodal Dept",
            officer_name: "Ajay Prabhakar",
            email: "ajay.prabhakar@hdfcbank.com",
            phone: "022-61606161"
        },
        {
            bank_name: "ICICI Bank",
            region: "Corporate Head Office",
            officer_name: "Vinayak More",
            email: "vinayak.more@icicibank.com",
            phone: "022-26536536"
        },
        {
            bank_name: "Axis Bank",
            region: "Nodal Officer Cyber",
            officer_name: "Nodal Officer",
            email: "nodal.officer@axisbank.com",
            phone: "1800-419-5555"
        },
        {
            bank_name: "Punjab National Bank",
            region: "Cyber Cell",
            officer_name: "Chief Manager Cyber",
            email: "cybercell@pnb.co.in",
            phone: "1800-180-2222"
        },
        {
            bank_name: "Kotak Mahindra Bank",
            region: "Nodal Officer",
            officer_name: "Nodal Officer",
            email: "nodal.officer@kotak.com",
            phone: "1800-266-2666"
        },
        {
            bank_name: "Paytm Payments Bank",
            region: "Fraud Prevention",
            officer_name: "Nodal Officer",
            email: "nodalofficer@paytm.com",
            phone: "0120-4456456"
        },
        {
            bank_name: "PhonePe",
            region: "Trust & Safety",
            officer_name: "Grievance Officer",
            email: "grievance@phonepe.com",
            phone: "080-68727374"
        },
        {
            bank_name: "Google Pay (GPay)",
            region: "User Safety",
            officer_name: "Grievance Officer India",
            email: "support-in@google.com",
            phone: "1800-419-0157"
        }
    ];
}

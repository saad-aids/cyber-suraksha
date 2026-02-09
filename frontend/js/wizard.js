/**
 * Wizard Controller
 * Handles multi-step fraud reporting wizard
 */

let currentStep = 1;
let analysisResult = null;

/**
 * Navigate to next step
 */
function nextStep(fromStep) {
    if (fromStep === 1) {
        // Validate step 1
        const complaint = document.getElementById('complaint').value.trim();
        if (complaint.length < 10) {
            showToast('Please describe the fraud incident (minimum 10 characters)', 'error');
            return;
        }
    }

    if (fromStep === 3 && !analysisResult) {
        showToast('Analysis not complete yet', 'error');
        return;
    }

    const toStep = fromStep + 1;
    goToStep(toStep);
}

/**
 * Navigate to previous step
 */
function prevStep(fromStep) {
    const toStep = fromStep - 1;
    if (toStep >= 1) {
        goToStep(toStep);
    }
}

/**
 * Go to specific step
 */
function goToStep(step) {
    // Hide all steps
    document.querySelectorAll('.wizard-step').forEach(s => {
        s.classList.remove('active');
    });

    // Show target step
    document.getElementById(`step${step}`).classList.add('active');

    // Update progress
    document.querySelectorAll('.progress-step').forEach((s, index) => {
        s.classList.remove('active', 'completed');
        if (index + 1 < step) {
            s.classList.add('completed');
        } else if (index + 1 === step) {
            s.classList.add('active');
        }
    });

    currentStep = step;

    // Scroll to wizard
    document.getElementById('report').scrollIntoView({ behavior: 'smooth' });
}

/**
 * Run AI analysis workflow
 */
async function runAnalysis() {
    // Collect form data
    const formData = {
        complaint: document.getElementById('complaint').value.trim(),
        incident_date: document.getElementById('incidentDate').value || new Date().toISOString().split('T')[0],
        amount: parseFloat(document.getElementById('amount').value) || 0,
        utr: document.getElementById('utr').value.trim(),
        bank_name: document.getElementById('bankName').value,
        suspect_phone: document.getElementById('suspectPhone').value.trim(),
        suspect_url: document.getElementById('suspectUrl').value.trim(),
        victim_name: document.getElementById('victimName').value.trim(),
        victim_phone: document.getElementById('victimPhone').value.trim()
    };

    // Validate minimum requirements
    if (!formData.complaint) {
        showToast('Please describe the fraud incident', 'error');
        return;
    }

    // Go to step 3
    goToStep(3);

    // Show loading state
    document.getElementById('analysisLoading').style.display = 'block';
    document.getElementById('analysisResults').style.display = 'none';
    document.getElementById('step3Actions').style.display = 'none';

    // Simulate node progression for visual feedback
    await simulateNodeProgression();

    try {
        // Call API
        const result = await API.analyzeFraud(formData);
        analysisResult = result;

        // Display results
        displayAnalysisResults(result);

    } catch (error) {
        console.error('Analysis error:', error);
        showToast('Analysis failed. Please check if the backend is running.', 'error');

        // Use fallback mock data for demo
        analysisResult = getMockAnalysisResult(formData);
        displayAnalysisResults(analysisResult);
    }
}

/**
 * Simulate node progression for visual feedback
 */
async function simulateNodeProgression() {
    const nodes = ['nodeTriage', 'nodeEvidence', 'nodeRouter', 'nodeReporter'];
    const statuses = [
        'Classifying scam type...',
        'Validating evidence...',
        'Finding nodal officers...',
        'Generating report...'
    ];

    for (let i = 0; i < nodes.length; i++) {
        const nodeEl = document.getElementById(`${nodes[i]}Status`);

        // Activate current node
        nodeEl.classList.remove('pending');
        nodeEl.classList.add('active');
        nodeEl.querySelector('.node-status').textContent = statuses[i];

        // Add spinner
        if (!nodeEl.querySelector('.node-spinner')) {
            const spinner = document.createElement('div');
            spinner.className = 'node-spinner';
            nodeEl.appendChild(spinner);
        }

        await delay(800);

        // Complete node
        nodeEl.classList.remove('active');
        nodeEl.classList.add('completed');
        nodeEl.querySelector('.node-status').textContent = 'Complete ✓';
        const spinner = nodeEl.querySelector('.node-spinner');
        if (spinner) spinner.remove();
    }
}

/**
 * Display analysis results
 */
function displayAnalysisResults(result) {
    const data = result.data || result;

    // Hide loading, show results
    document.getElementById('analysisLoading').style.display = 'none';
    document.getElementById('analysisResults').style.display = 'flex';
    document.getElementById('step3Actions').style.display = 'flex';

    // Triage results
    const triage = data.triage || {};
    const scamType = (triage.scam_type || 'unknown').replace(/_/g, ' ').toUpperCase();
    document.getElementById('scamTypeBadge').textContent = scamType;
    document.getElementById('scamConfidence').textContent =
        `${Math.round((triage.confidence || 0.5) * 100)}%`;

    const urgencyEl = document.getElementById('scamUrgency');
    urgencyEl.textContent = (triage.urgency || 'medium').toUpperCase();
    urgencyEl.className = `detail-value urgency-badge ${triage.urgency || 'medium'}`;

    document.getElementById('scamReasoning').textContent =
        triage.reasoning || 'Analysis based on provided complaint.';

    // Evidence results
    const evidence = data.evidence || {};
    const scoreCircle = document.getElementById('evidenceScoreCircle');
    const score = evidence.evidence_score || 50;
    document.getElementById('evidenceScore').textContent = score;
    scoreCircle.style.background = score > 70 ? 'var(--success)' :
        score > 40 ? 'var(--warning)' : 'var(--danger)';

    // Suspect checks
    const suspectChecksEl = document.getElementById('suspectChecks');
    suspectChecksEl.innerHTML = '';

    if (evidence.suspect_checks && evidence.suspect_checks.length > 0) {
        evidence.suspect_checks.forEach(check => {
            const isFlagged = check.result && check.result.found;
            const div = document.createElement('div');
            div.className = `suspect-check-item ${isFlagged ? 'flagged' : ''}`;
            div.innerHTML = `
                <span>${check.type === 'phone' ? '📱' : '🌐'}</span>
                <span>${check.value}</span>
                <span>${isFlagged ? `⚠️ FLAGGED (${check.result.reports} reports)` : '✓ Not flagged'}</span>
            `;
            suspectChecksEl.appendChild(div);
        });
    } else {
        suspectChecksEl.innerHTML = '<div class="suspect-check-item">No suspects checked</div>';
    }

    // Nodal officers
    const routing = data.routing || {};
    const nodalListEl = document.getElementById('nodalOfficersList');
    nodalListEl.innerHTML = '';

    if (routing.nodal_officers && routing.nodal_officers.length > 0) {
        routing.nodal_officers.forEach(officer => {
            const div = document.createElement('div');
            div.className = 'nodal-officer-card';
            div.innerHTML = `
                <div class="officer-icon">🏦</div>
                <div class="officer-info">
                    <div class="officer-name">${officer.bank_name}</div>
                    <div class="officer-details">${officer.region} - ${officer.officer_name}</div>
                    <div class="officer-contact">📧 ${officer.email}</div>
                    <div class="officer-contact">📞 ${officer.phone}</div>
                </div>
            `;
            nodalListEl.appendChild(div);
        });
    } else {
        nodalListEl.innerHTML = `
            <div class="nodal-officer-card">
                <div class="officer-icon">📞</div>
                <div class="officer-info">
                    <div class="officer-name">National Cyber Crime Helpline</div>
                    <div class="officer-details">Call 1930 immediately</div>
                </div>
            </div>
        `;
    }

    // Store for step 4
    window.currentReport = data.report || {};
}

/**
 * Display report in step 4
 */
function displayReport() {
    const report = window.currentReport || {};

    document.getElementById('reportTitle').textContent =
        report.title || 'Cyber Fraud Complaint Report';

    document.getElementById('reportBody').textContent =
        report.body || 'Report generation failed. Please provide more details.';

    const length = (report.body || '').length;
    document.getElementById('reportLength').textContent = `${length} characters`;

    const statusEl = document.getElementById('reportStatus');
    if (length >= 200) {
        statusEl.textContent = '✓ Meets minimum (200 chars)';
        statusEl.style.color = 'var(--success)';
    } else {
        statusEl.textContent = '✗ Below minimum (200 chars)';
        statusEl.style.color = 'var(--danger)';
    }

    // Actions
    const actionsEl = document.getElementById('reportActions');
    actionsEl.innerHTML = '<h5>Recommended Actions:</h5><ul></ul>';
    const ul = actionsEl.querySelector('ul');

    const actions = report.recommended_actions || ['Call 1930', 'File report on cybercrime.gov.in'];
    actions.forEach(action => {
        const li = document.createElement('li');
        li.textContent = action;
        ul.appendChild(li);
    });

    // Email draft
    document.getElementById('emailDraft').textContent =
        report.email_draft || 'Email draft not available.';
}

/**
 * Copy email to clipboard
 */
function copyEmail() {
    const emailText = document.getElementById('emailDraft').textContent;
    navigator.clipboard.writeText(emailText).then(() => {
        showToast('Email copied to clipboard!');
    }).catch(err => {
        showToast('Failed to copy email', 'error');
    });
}

/**
 * Download report as text file
 */
function downloadReport() {
    const report = window.currentReport || {};
    const content = `CYBER FRAUD COMPLAINT REPORT
=============================

${report.title || 'Cyber Fraud Report'}

${report.body || 'No report content'}

----------------------------------------
EMAIL DRAFT FOR NODAL OFFICER:
----------------------------------------

${report.email_draft || ''}

----------------------------------------
Generated by Cyber-Suraksha
Date: ${new Date().toLocaleString()}
`;

    const blob = new Blob([content], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `cyber-fraud-report-${Date.now()}.txt`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);

    showToast('Report downloaded!');
}

/**
 * Mock analysis result for offline demo
 */
function getMockAnalysisResult(formData) {
    return {
        success: true,
        workflow_complete: true,
        data: {
            triage: {
                scam_type: 'digital_arrest',
                confidence: 0.85,
                urgency: 'critical',
                reasoning: 'Based on the description, this appears to be a Digital Arrest scam where fraudsters impersonate law enforcement officials.',
                indicators: ['Police impersonation', 'Threat of arrest', 'Demand for money']
            },
            evidence: {
                evidence_score: 65,
                utr_validated: true,
                suspect_checks: [
                    { type: 'phone', value: formData.suspect_phone || '9876543210', result: { found: true, reports: 45 } }
                ]
            },
            routing: {
                routing_success: true,
                nodal_officers: [
                    {
                        bank_name: formData.bank_name || 'State Bank of India',
                        region: 'Nodal Officer (Cyber)',
                        officer_name: 'AGM Nodal Cyber',
                        email: 'agm.nodcyb@sbi.co.in',
                        phone: '1800-111-109'
                    }
                ]
            },
            report: {
                title: 'Cyber Fraud Complaint - Digital Arrest Scam',
                body: `I am filing this complaint regarding a cyber fraud incident that occurred on ${formData.incident_date}. ${formData.complaint}\n\nTransaction Details:\n- Amount Lost: ₹${formData.amount}\n- UTR/Reference: ${formData.utr}\n- Bank: ${formData.bank_name}\n\nSuspect Information:\n- Phone: ${formData.suspect_phone}\n- Website/App: ${formData.suspect_url}\n\nI request immediate action to freeze the fraudulent transaction as this falls within the Cyber Golden Hour window.`,
                recommended_actions: [
                    'Call 1930 helpline immediately',
                    'File FIR at nearest cyber police station',
                    'Contact bank nodal officer with this report',
                    'Submit complaint on cybercrime.gov.in'
                ],
                email_draft: `Subject: URGENT: Cyber Fraud Report - Digital Arrest Scam - ₹${formData.amount}\n\nDear Nodal Officer,\n\n${formData.complaint}\n\nTransaction Details:\n- UTR: ${formData.utr}\n- Amount: ₹${formData.amount}\n\nRegards,\n${formData.victim_name || 'Complainant'}`
            }
        }
    };
}

/**
 * Utility: Delay function
 */
function delay(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

/**
 * Utility: Show toast notification
 */
function showToast(message, type = 'success') {
    const toast = document.getElementById('toast');
    const toastMessage = document.getElementById('toastMessage');

    toastMessage.textContent = message;
    toast.style.background = type === 'error' ? 'var(--danger)' : 'var(--success)';
    toast.classList.add('show');

    setTimeout(() => {
        toast.classList.remove('show');
    }, 3000);
}

// Watch for step 4 to display report
const observer = new MutationObserver((mutations) => {
    mutations.forEach((mutation) => {
        if (mutation.target.id === 'step4' && mutation.target.classList.contains('active')) {
            displayReport();
        }
    });
});

document.addEventListener('DOMContentLoaded', () => {
    const step4 = document.getElementById('step4');
    if (step4) {
        observer.observe(step4, { attributes: true, attributeFilter: ['class'] });
    }
});

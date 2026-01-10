// LLM Council Frontend - Main JavaScript

// API endpoints (relative to frontend server)
const API = {
    health: '/health',
    council: '/council',
    config: '/config'
};

// DOM elements
const elements = {
    queryInput: document.getElementById('query-input'),
    submitBtn: document.getElementById('submit-btn'),
    clearBtn: document.getElementById('clear-btn'),
    loading: document.getElementById('loading'),
    loadingText: document.getElementById('loading-text'),
    resultsSection: document.getElementById('results-section'),
    errorSection: document.getElementById('error-section'),
    errorContent: document.getElementById('error-content'),
    displayQuery: document.getElementById('display-query'),
    stage1Content: document.getElementById('stage1-content'),
    stage2Content: document.getElementById('stage2-content'),
    stage3Content: document.getElementById('stage3-content'),
    stage1Count: document.getElementById('stage1-count'),
    stage2Count: document.getElementById('stage2-count'),
    pc1Status: document.getElementById('pc1-status'),
    pc2Status: document.getElementById('pc2-status')
};

// Initialize app
document.addEventListener('DOMContentLoaded', () => {
    initTabs();
    checkHealth();
    loadConfig();

    // Event listeners
    elements.submitBtn.addEventListener('click', submitQuery);
    elements.clearBtn.addEventListener('click', clearResults);
    elements.queryInput.addEventListener('keydown', (e) => {
        if (e.ctrlKey && e.key === 'Enter') {
            submitQuery();
        }
    });

    // Auto-refresh health status
    setInterval(checkHealth, 30000); // Every 30 seconds
});

// Tab functionality
function initTabs() {
    const tabButtons = document.querySelectorAll('.tab-btn');
    const tabPanels = document.querySelectorAll('.tab-panel');

    tabButtons.forEach(button => {
        button.addEventListener('click', () => {
            const targetTab = button.getAttribute('data-tab');

            // Remove active class from all
            tabButtons.forEach(btn => btn.classList.remove('active'));
            tabPanels.forEach(panel => panel.classList.remove('active'));

            // Add active class to clicked
            button.classList.add('active');
            document.getElementById(targetTab).classList.add('active');
        });
    });
}

// Check health of all services
async function checkHealth() {
    try {
        const response = await fetch(API.health);
        const data = await response.json();

        // Update PC1 status
        updateStatus(elements.pc1Status, data.pc1_chairman);

        // Update PC2 status
        updateStatus(elements.pc2Status, data.pc2_council);

    } catch (error) {
        console.error('Health check failed:', error);
        updateStatus(elements.pc1Status, 'error');
        updateStatus(elements.pc2Status, 'error');
    }
}

function updateStatus(element, status) {
    element.classList.remove('healthy', 'error', 'unknown');

    if (status === 'healthy') {
        element.classList.add('healthy');
        element.textContent = '✓ Healthy';
    } else if (status && status.includes('error')) {
        element.classList.add('error');
        element.textContent = '✗ Error';
    } else {
        element.classList.add('unknown');
        element.textContent = '⚫ Unknown';
    }
}

// Load configuration
async function loadConfig() {
    try {
        const response = await fetch(API.config);
        const config = await response.json();
        console.log('Configuration:', config);
    } catch (error) {
        console.error('Failed to load config:', error);
    }
}

// Submit query to council
async function submitQuery() {
    const query = elements.queryInput.value.trim();

    if (!query) {
        alert('Please enter a query');
        return;
    }

    // Disable submit button
    elements.submitBtn.disabled = true;
    elements.submitBtn.textContent = 'Processing...';

    // Show loading
    elements.loading.classList.remove('hidden');
    elements.resultsSection.classList.add('hidden');
    elements.errorSection.classList.add('hidden');

    // Get progress stage elements
    const progressStages = document.querySelectorAll('.progress-stage');

    // Reset all stages
    progressStages.forEach(stage => {
        stage.classList.remove('active', 'completed');
    });

    // Start progress updates
    let stage = 1;
    progressStages[0].classList.add('active'); // Activate first stage

    const progressInterval = setInterval(() => {
        if (stage === 1) {
            updateLoadingText('⏳ Stage 1/3: Council LLMs generating independent answers...');
            progressStages[0].classList.remove('active');
            progressStages[0].classList.add('completed');
            progressStages[1].classList.add('active');
            stage = 2;
        } else if (stage === 2) {
            updateLoadingText('⏳ Stage 2/3: Council LLMs reviewing and ranking answers...');
            progressStages[1].classList.remove('active');
            progressStages[1].classList.add('completed');
            progressStages[2].classList.add('active');
            stage = 3;
        } else if (stage === 3) {
            updateLoadingText('⏳ Stage 3/3: Chairman synthesizing final answer...');
            stage = 4;
        } else {
            updateLoadingText('⏳ Finalizing results...');
        }
    }, 8000); // Update every 8 seconds

    try {
        // Initial message
        updateLoadingText('⏳ Stage 1/3: Council LLMs generating independent answers...');

        const response = await fetch(API.council, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ query })
        });

        // Stop progress updates
        clearInterval(progressInterval);

        if (!response.ok) {
            throw new Error(`HTTP ${response.status}: ${response.statusText}`);
        }

        const data = await response.json();

        // Mark all stages as completed
        progressStages.forEach(stage => {
            stage.classList.remove('active');
            stage.classList.add('completed');
        });

        // Success message
        updateLoadingText('✅ All stages completed! Displaying results...');

        // Small delay to show success message
        await new Promise(resolve => setTimeout(resolve, 1000));

        // Hide loading
        elements.loading.classList.add('hidden');

        // Display results
        displayResults(data);

        // Scroll to results
        elements.resultsSection.scrollIntoView({ behavior: 'smooth' });

    } catch (error) {
        clearInterval(progressInterval);
        elements.loading.classList.add('hidden');
        showError(`Failed to complete council workflow: ${error.message}`);
    } finally {
        elements.submitBtn.disabled = false;
        elements.submitBtn.textContent = 'Submit to Council';
    }
}

function updateLoadingText(text) {
    elements.loadingText.textContent = text;
}

// Display results
function displayResults(data) {
    // Show results section
    elements.resultsSection.classList.remove('hidden');

    // Display query
    elements.displayQuery.textContent = data.query;

    // Stage 1: Answers
    displayAnswers(data.stage1_answers);

    // Stage 2: Reviews
    displayReviews(data.stage2_reviews);

    // Stage 3: Final answer
    displayFinalAnswer(data.stage3_final, data.chairman_model);

    // Display errors if any
    if (data.errors && data.errors.length > 0) {
        showError(data.errors.join('\n'));
    }
}

function displayAnswers(answers) {
    elements.stage1Count.textContent = answers.length;
    elements.stage1Content.innerHTML = '';

    if (!answers || answers.length === 0) {
        elements.stage1Content.innerHTML = '<p>No answers received.</p>';
        return;
    }

    answers.forEach((answer, index) => {
        const card = document.createElement('div');
        card.className = 'answer-card';
        card.innerHTML = `
            <div class="answer-header">
                <span class="model-name">🤖 ${answer.model}</span>
            </div>
            <div class="answer-text">${escapeHtml(answer.response)}</div>
        `;
        elements.stage1Content.appendChild(card);
    });
}

function displayReviews(reviews) {
    elements.stage2Count.textContent = reviews.length;
    elements.stage2Content.innerHTML = '';

    if (!reviews || reviews.length === 0) {
        elements.stage2Content.innerHTML = '<p>No reviews received.</p>';
        return;
    }

    reviews.forEach((review, index) => {
        const card = document.createElement('div');
        card.className = 'review-card';
        card.innerHTML = `
            <div class="reviewer-name">📋 Reviewer: ${review.reviewer}</div>
            <div class="review-text">${escapeHtml(review.review_text || 'No review text available')}</div>
        `;
        elements.stage2Content.appendChild(card);
    });
}

function displayFinalAnswer(finalAnswer, chairmanModel) {
    elements.stage3Content.innerHTML = '';

    if (!finalAnswer) {
        elements.stage3Content.innerHTML = '<p>No final answer received.</p>';
        return;
    }

    const answerDiv = document.createElement('div');
    answerDiv.innerHTML = `
        <div class="chairman-label">👔 Chairman: ${chairmanModel}</div>
        <div class="final-text">${escapeHtml(finalAnswer)}</div>
    `;
    elements.stage3Content.appendChild(answerDiv);
}

function showError(message) {
    elements.errorSection.classList.remove('hidden');
    elements.errorContent.textContent = message;
}

function clearResults() {
    elements.queryInput.value = '';
    elements.resultsSection.classList.add('hidden');
    elements.errorSection.classList.add('hidden');
    elements.loading.classList.add('hidden');

    // Clear content
    elements.stage1Content.innerHTML = '';
    elements.stage2Content.innerHTML = '';
    elements.stage3Content.innerHTML = '';
    elements.displayQuery.textContent = '';

    // Reset counts
    elements.stage1Count.textContent = '0';
    elements.stage2Count.textContent = '0';

    // Reset to Stage 1 tab
    const firstTab = document.querySelector('.tab-btn[data-tab="stage1"]');
    firstTab.click();
}

// Utility: Escape HTML to prevent XSS
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// Export for debugging
window.CouncilApp = {
    checkHealth,
    submitQuery,
    clearResults,
    API
};

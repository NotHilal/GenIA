// LLM Council Frontend - Main JavaScript

// API endpoints (relative to frontend server)
const API = {
    health: '/health',
    council: '/council',
    stage1: '/stage1',
    stage2: '/stage2',
    stage3: '/stage3',
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
    pc2Status: document.getElementById('pc2-status'),
    themeToggle: document.getElementById('theme-toggle'),
    themeIcon: document.querySelector('.theme-icon'),
    pc1Model: document.getElementById('pc1-model'),
    pc2Models: document.getElementById('pc2-models'),
    pc1Ollama: document.getElementById('pc1-ollama'),
    pc2Ollama: document.getElementById('pc2-ollama'),
    perfStage1: document.getElementById('perf-stage1'),
    perfStage2: document.getElementById('perf-stage2'),
    perfStage3: document.getElementById('perf-stage3'),
    perfTotal: document.getElementById('perf-total'),
    performanceSection: document.getElementById('performance-section'),
    historySection: document.getElementById('history-section'),
    historyList: document.getElementById('history-list'),
    copyFinalBtn: document.getElementById('copy-final-btn')
};

// Performance tracking
let performanceTimes = {
    stage1Start: 0,
    stage1End: 0,
    stage2Start: 0,
    stage2End: 0,
    stage3Start: 0,
    stage3End: 0,
    totalStart: 0,
    totalEnd: 0
};

// Initialize app
document.addEventListener('DOMContentLoaded', () => {
    initTabs();
    initTheme();
    initHistory();
    checkHealth();
    loadConfig();

    // Event listeners
    elements.submitBtn.addEventListener('click', submitQuery);
    elements.clearBtn.addEventListener('click', clearResults);
    elements.themeToggle.addEventListener('click', toggleTheme);
    elements.copyFinalBtn.addEventListener('click', copyFinalAnswer);

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

// Dark Mode Functions
function initTheme() {
    const savedTheme = localStorage.getItem('theme') || 'light';
    if (savedTheme === 'dark') {
        document.body.classList.add('dark-mode');
        elements.themeIcon.textContent = '☀️';
    }
}

function toggleTheme() {
    document.body.classList.toggle('dark-mode');
    const isDark = document.body.classList.contains('dark-mode');
    elements.themeIcon.textContent = isDark ? '☀️' : '🌙';
    localStorage.setItem('theme', isDark ? 'dark' : 'light');
}

// Query History Functions
function initHistory() {
    loadHistory();
}

function loadHistory() {
    const history = getQueryHistory();
    if (history.length > 0) {
        elements.historySection.classList.remove('hidden');
        renderHistory(history);
    }
}

function getQueryHistory() {
    const history = localStorage.getItem('queryHistory');
    return history ? JSON.parse(history) : [];
}

function saveQueryToHistory(query) {
    let history = getQueryHistory();
    const newEntry = {
        query: query,
        timestamp: new Date().toISOString()
    };

    // Add to beginning, limit to 10
    history.unshift(newEntry);
    history = history.slice(0, 10);

    localStorage.setItem('queryHistory', JSON.stringify(history));
    loadHistory();
}

function renderHistory(history) {
    elements.historyList.innerHTML = '';
    history.forEach((entry, index) => {
        const item = document.createElement('div');
        item.className = 'history-item';

        const text = document.createElement('span');
        text.className = 'history-text';
        text.textContent = entry.query;

        const time = document.createElement('span');
        time.className = 'history-time';
        const date = new Date(entry.timestamp);
        time.textContent = date.toLocaleString();

        item.appendChild(text);
        item.appendChild(time);

        item.addEventListener('click', () => {
            elements.queryInput.value = entry.query;
            elements.queryInput.focus();
        });

        elements.historyList.appendChild(item);
    });
}

// Copy to Clipboard Function
async function copyToClipboard(text) {
    try {
        await navigator.clipboard.writeText(text);
        return true;
    } catch (err) {
        console.error('Failed to copy:', err);
        return false;
    }
}

function copyFinalAnswer() {
    const finalText = elements.stage3Content.textContent;
    copyToClipboard(finalText).then(success => {
        if (success) {
            elements.copyFinalBtn.textContent = '✅ Copied!';
            elements.copyFinalBtn.classList.add('copied');
            setTimeout(() => {
                elements.copyFinalBtn.textContent = '📋 Copy Final Answer';
                elements.copyFinalBtn.classList.remove('copied');
            }, 2000);
        }
    });
}

function copyAnswerText(button) {
    const answerCard = button.closest('.answer-card');
    const answerText = answerCard.querySelector('.answer-text').textContent;
    copyToClipboard(answerText).then(success => {
        if (success) {
            button.textContent = '✅ Copied!';
            setTimeout(() => {
                button.textContent = '📋 Copy';
            }, 2000);
        }
    });
}

// Make copyAnswerText globally available
window.copyAnswerText = copyAnswerText;

// Performance Tracking Functions
function formatTime(milliseconds) {
    if (milliseconds < 1000) {
        return `${milliseconds}ms`;
    }
    const seconds = (milliseconds / 1000).toFixed(1);
    return `${seconds}s`;
}

function updatePerformanceMetrics() {
    const stage1Time = performanceTimes.stage1End - performanceTimes.stage1Start;
    const stage2Time = performanceTimes.stage2End - performanceTimes.stage2Start;
    const stage3Time = performanceTimes.stage3End - performanceTimes.stage3Start;
    const totalTime = performanceTimes.totalEnd - performanceTimes.totalStart;

    elements.perfStage1.textContent = formatTime(stage1Time);
    elements.perfStage2.textContent = formatTime(stage2Time);
    elements.perfStage3.textContent = formatTime(stage3Time);
    elements.perfTotal.textContent = formatTime(totalTime);

    elements.performanceSection.classList.remove('hidden');
}

// Check health of all services
async function checkHealth() {
    try {
        const response = await fetch(API.health);
        const data = await response.json();

        // Update PC1 status
        updateStatus(elements.pc1Status, data.pc1_chairman);

        // Update PC1 details
        if (data.chairman_data) {
            elements.pc1Model.textContent = data.chairman_data.model || '-';
            elements.pc1Ollama.textContent = data.chairman_data.ollama_url || '-';
        }

        // Update PC2 status
        updateStatus(elements.pc2Status, data.pc2_council);

        // Update PC2 details
        if (data.council_data) {
            const models = data.council_data.models || [];
            elements.pc2Models.textContent = `${models.length} models`;
            elements.pc2Ollama.textContent = data.council_data.ollama_url || '-';
        }

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

    // Save query to history
    saveQueryToHistory(query);

    // Start total timer
    performanceTimes.totalStart = Date.now();

    try {
        let answers = [];
        let reviews = [];
        let finalAnswer = '';
        let chairmanModel = '';

        // STAGE 1: Get answers
        progressStages[0].classList.add('active');
        updateLoadingText('⏳ Stage 1/3: Council LLMs generating independent answers...');
        performanceTimes.stage1Start = Date.now();

        const stage1Response = await fetch(API.stage1, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ query })
        });

        if (!stage1Response.ok) {
            throw new Error(`Stage 1 failed: ${stage1Response.status}`);
        }

        const stage1Data = await stage1Response.json();
        answers = stage1Data.answers || [];

        // Stage 1 complete
        performanceTimes.stage1End = Date.now();
        progressStages[0].classList.remove('active');
        progressStages[0].classList.add('completed');

        // STAGE 2: Get reviews
        progressStages[1].classList.add('active');
        updateLoadingText('⏳ Stage 2/3: Council LLMs reviewing and ranking answers...');
        performanceTimes.stage2Start = Date.now();

        const stage2Response = await fetch(API.stage2, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ query, answers })
        });

        if (!stage2Response.ok) {
            throw new Error(`Stage 2 failed: ${stage2Response.status}`);
        }

        const stage2Data = await stage2Response.json();
        reviews = stage2Data.reviews || [];

        // Stage 2 complete
        performanceTimes.stage2End = Date.now();
        progressStages[1].classList.remove('active');
        progressStages[1].classList.add('completed');

        // STAGE 3: Get synthesis
        progressStages[2].classList.add('active');
        updateLoadingText('⏳ Stage 3/3: Chairman synthesizing final answer...');
        performanceTimes.stage3Start = Date.now();

        const stage3Response = await fetch(API.stage3, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ query, answers, reviews })
        });

        if (!stage3Response.ok) {
            throw new Error(`Stage 3 failed: ${stage3Response.status}`);
        }

        const stage3Data = await stage3Response.json();
        finalAnswer = stage3Data.final_answer || '';
        chairmanModel = stage3Data.chairman_model || '';

        // Stage 3 complete
        performanceTimes.stage3End = Date.now();
        performanceTimes.totalEnd = Date.now();
        progressStages[2].classList.remove('active');
        progressStages[2].classList.add('completed');

        // Success message
        updateLoadingText('✅ All stages completed! Displaying results...');

        // Small delay to show success message
        await new Promise(resolve => setTimeout(resolve, 500));

        // Update performance metrics
        updatePerformanceMetrics();

        // Hide loading
        elements.loading.classList.add('hidden');

        // Show copy button
        elements.copyFinalBtn.classList.remove('hidden');

        // Display results
        const fullResults = {
            query: query,
            stage1_answers: answers,
            stage2_reviews: reviews,
            stage3_final: finalAnswer,
            chairman_model: chairmanModel,
            errors: []
        };
        displayResults(fullResults);

        // Scroll to results
        elements.resultsSection.scrollIntoView({ behavior: 'smooth' });

    } catch (error) {
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
                <button class="answer-copy-btn" onclick="copyAnswerText(this)">📋 Copy</button>
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
    elements.performanceSection.classList.add('hidden');
    elements.copyFinalBtn.classList.add('hidden');

    // Clear content
    elements.stage1Content.innerHTML = '';
    elements.stage2Content.innerHTML = '';
    elements.stage3Content.innerHTML = '';
    elements.displayQuery.textContent = '';

    // Reset counts
    elements.stage1Count.textContent = '0';
    elements.stage2Count.textContent = '0';

    // Reset performance times
    performanceTimes = {
        stage1Start: 0,
        stage1End: 0,
        stage2Start: 0,
        stage2End: 0,
        stage3Start: 0,
        stage3End: 0,
        totalStart: 0,
        totalEnd: 0
    };

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

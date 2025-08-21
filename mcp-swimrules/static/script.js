/**
 * Swim Rules Agent Frontend JavaScript
 * Handles user interactions and API communication
 */

class SwimRulesAgent {
    constructor() {
        this.scenarioInput = document.getElementById('scenarioInput');
        this.analyzeBtn = document.getElementById('analyzeBtn');
        this.clearBtn = document.getElementById('clearBtn');
        this.exampleBtn = document.getElementById('exampleBtn');
        this.charCount = document.getElementById('charCount');
        this.loadingIndicator = document.getElementById('loadingIndicator');
        this.resultsSection = document.getElementById('resultsSection');
        this.exampleModal = document.getElementById('exampleModal');
        this.closeModal = document.getElementById('closeModal');
        this.errorToast = document.getElementById('errorToast');
        this.closeError = document.getElementById('closeError');
        
        this.initializeEventListeners();
        this.loadExampleScenarios();
    }

    /**
     * Initialize all event listeners
     */
    initializeEventListeners() {
        // Input handling
        this.scenarioInput.addEventListener('input', () => this.updateCharacterCount());
        this.scenarioInput.addEventListener('keydown', (e) => this.handleKeyDown(e));
        
        // Button handling
        this.analyzeBtn.addEventListener('click', () => this.analyzeScenario());
        this.clearBtn.addEventListener('click', () => this.clearInput());
        this.exampleBtn.addEventListener('click', () => this.showExampleModal());
        
        // Modal handling
        this.closeModal.addEventListener('click', () => this.hideExampleModal());
        this.exampleModal.addEventListener('click', (e) => {
            if (e.target === this.exampleModal) this.hideExampleModal();
        });
        
        // Error toast handling
        this.closeError.addEventListener('click', () => this.hideError());
        
        // Escape key handling
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape') {
                this.hideExampleModal();
                this.hideError();
            }
        });
    }

    /**
     * Update character count display
     */
    updateCharacterCount() {
        const length = this.scenarioInput.value.length;
        this.charCount.textContent = length;
        
        // Update styling based on character count
        const counter = this.charCount.parentElement;
        counter.classList.remove('warning', 'danger');
        
        if (length > 1800) {
            counter.classList.add('danger');
        } else if (length > 1500) {
            counter.classList.add('warning');
        }
        
        // Enable/disable analyze button
        this.analyzeBtn.disabled = length === 0 || length > 2000;
    }

    /**
     * Handle keyboard shortcuts
     */
    handleKeyDown(e) {
        // Ctrl/Cmd + Enter to analyze
        if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
            e.preventDefault();
            if (!this.analyzeBtn.disabled) {
                this.analyzeScenario();
            }
        }
    }

    /**
     * Analyze the scenario using the API
     */
    async analyzeScenario() {
        const scenario = this.scenarioInput.value.trim();
        
        if (!scenario) {
            this.showError('Please enter a scenario description');
            return;
        }

        if (scenario.length > 2000) {
            this.showError('Scenario description is too long (maximum 2000 characters)');
            return;
        }

        try {
            this.showLoading(true);
            this.hideResults();
            
            const response = await fetch('/api/analyze', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ scenario: scenario })
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.detail || `HTTP ${response.status}: ${response.statusText}`);
            }

            const result = await response.json();
            this.displayResults(result);
            
        } catch (error) {
            console.error('Analysis error:', error);
            this.showError(`Analysis failed: ${error.message}`);
        } finally {
            this.showLoading(false);
        }
    }

    /**
     * Display analysis results as specified in PRD Section 4.3.2
     */
    displayResults(result) {
        // Update decision banner
        const decisionBanner = document.getElementById('decisionBanner');
        const decisionIcon = document.getElementById('decisionIcon');
        const decisionText = document.getElementById('decisionText');
        
        decisionBanner.className = 'decision-banner';
        
        if (result.decision === 'DISQUALIFICATION') {
            decisionBanner.classList.add('disqualification');
            decisionIcon.textContent = '🚫';
            decisionText.textContent = 'DISQUALIFICATION';
        } else {
            decisionBanner.classList.add('allowed');
            decisionIcon.textContent = '✅';
            decisionText.textContent = 'ALLOWED';
        }
        
        // Update rationale
        const rationaleText = document.getElementById('rationaleText');
        rationaleText.textContent = result.rationale;
        
        // Update citations
        this.displayCitations(result.rule_citations);
        
        // Show results section
        this.showResults();
        
        // Scroll to results
        this.resultsSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }

    /**
     * Display rule citations as simple identifiers per PRD Section 4.3.2
     */
    displayCitations(citations) {
        const citationsContent = document.getElementById('citationsContent');
        
        if (!citations || citations.length === 0) {
            citationsContent.innerHTML = '<p>No specific rule citations available.</p>';
            return;
        }
        
        // Create formatted citation list
        let html = `
            <div class="citation-category">
                <h5>Rule Citations:</h5>
                <ul class="citation-list">
                    ${citations.map(citation => `
                        <li class="citation-item">
                            <span class="citation-number">${citation}</span>
                        </li>
                    `).join('')}
                </ul>
            </div>
        `;
        
        citationsContent.innerHTML = html;
    }

    /**
     * Clear input and results
     */
    clearInput() {
        this.scenarioInput.value = '';
        this.updateCharacterCount();
        this.hideResults();
        this.scenarioInput.focus();
    }

    /**
     * Load and display example scenarios
     */
    async loadExampleScenarios() {
        try {
            const response = await fetch('/api/scenario-examples');
            const examples = await response.json();
            this.populateExampleModal(examples);
        } catch (error) {
            console.error('Failed to load examples:', error);
        }
    }

    /**
     * Populate the example modal with scenarios
     */
    populateExampleModal(examples) {
        const categories = document.querySelectorAll('.example-list');
        
        categories.forEach(categoryElement => {
            const category = categoryElement.dataset.category;
            const scenarios = examples[category] || [];
            
            categoryElement.innerHTML = scenarios.map(scenario => `
                <div class="example-item" data-scenario="${this.escapeHtml(scenario)}">
                    ${scenario}
                </div>
            `).join('');
            
            // Add click handlers for example items
            categoryElement.addEventListener('click', (e) => {
                if (e.target.classList.contains('example-item')) {
                    const scenario = e.target.dataset.scenario;
                    this.loadExample(scenario);
                }
            });
        });
    }

    /**
     * Load an example scenario into the input
     */
    loadExample(scenario) {
        this.scenarioInput.value = scenario;
        this.updateCharacterCount();
        this.hideExampleModal();
        this.scenarioInput.focus();
        
        // Scroll to input
        this.scenarioInput.scrollIntoView({ behavior: 'smooth', block: 'center' });
    }

    /**
     * Show/hide loading indicator
     */
    showLoading(show) {
        if (show) {
            this.loadingIndicator.classList.remove('hidden');
            this.analyzeBtn.disabled = true;
            this.analyzeBtn.textContent = 'Analyzing...';
        } else {
            this.loadingIndicator.classList.add('hidden');
            this.analyzeBtn.disabled = this.scenarioInput.value.trim().length === 0;
            this.analyzeBtn.textContent = 'Analyze';
        }
    }

    /**
     * Show/hide results section
     */
    showResults() {
        this.resultsSection.classList.remove('hidden');
    }

    hideResults() {
        this.resultsSection.classList.add('hidden');
    }

    /**
     * Show/hide example modal
     */
    showExampleModal() {
        this.exampleModal.classList.remove('hidden');
        document.body.style.overflow = 'hidden';
    }

    hideExampleModal() {
        this.exampleModal.classList.add('hidden');
        document.body.style.overflow = '';
    }

    /**
     * Show error message
     */
    showError(message) {
        const errorMessage = document.getElementById('errorMessage');
        errorMessage.textContent = message;
        this.errorToast.classList.remove('hidden');
        
        // Auto-hide after 5 seconds
        setTimeout(() => {
            this.hideError();
        }, 5000);
    }

    /**
     * Hide error message
     */
    hideError() {
        this.errorToast.classList.add('hidden');
    }

    /**
     * Escape HTML for safe insertion
     */
    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }
}

// Initialize the application when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new SwimRulesAgent();
});

// Service Worker registration for offline functionality (optional)
if ('serviceWorker' in navigator) {
    window.addEventListener('load', () => {
        navigator.serviceWorker.register('/static/sw.js')
            .then(registration => {
                console.log('SW registered: ', registration);
            })
            .catch(registrationError => {
                console.log('SW registration failed: ', registrationError);
            });
    });
}

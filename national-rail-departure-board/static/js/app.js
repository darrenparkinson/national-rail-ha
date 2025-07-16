/**
 * National Rail Departure Board - Frontend JavaScript
 */

class DepartureBoard {
    constructor() {
        this.currentStation = 'PAD';
        this.refreshInterval = null;
        this.isLoading = false;
        this.autoRefreshEnabled = true;
        
        this.init();
    }

    init() {
        this.updateCurrentTime();
        this.setupEventListeners();
        this.loadDepartures();
        this.startAutoRefresh();
        
        // Update time every second
        setInterval(() => this.updateCurrentTime(), 1000);
    }

    setupEventListeners() {
        // Station selector
        const stationSelect = document.getElementById('stationSelect');
        if (stationSelect) {
            stationSelect.addEventListener('change', (e) => {
                this.currentStation = e.target.value;
                this.loadDepartures();
            });
        }

        // Refresh button
        const refreshBtn = document.getElementById('refreshBtn');
        if (refreshBtn) {
            refreshBtn.addEventListener('click', () => {
                this.loadDepartures();
            });
        }

        // Auto-refresh toggle
        const autoRefreshCheckbox = document.getElementById('autoRefresh');
        if (autoRefreshCheckbox) {
            autoRefreshCheckbox.addEventListener('change', (e) => {
                this.autoRefreshEnabled = e.target.checked;
                if (this.autoRefreshEnabled) {
                    this.startAutoRefresh();
                } else {
                    this.stopAutoRefresh();
                }
            });
        }
    }

    updateCurrentTime() {
        const now = new Date();
        const timeString = now.toLocaleTimeString('en-GB', {
            hour: '2-digit',
            minute: '2-digit',
            second: '2-digit'
        });
        
        const currentTimeElement = document.getElementById('currentTime');
        if (currentTimeElement) {
            currentTimeElement.textContent = timeString;
        }
    }

    async loadDepartures() {
        if (this.isLoading) return;
        
        this.isLoading = true;
        this.showLoading(true);
        this.hideError();

        try {
            // Use relative path for API calls - this works with any ingress setup
            const response = await fetch('./api/departures?station=' + this.currentStation);
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            const data = await response.json();
            this.displayDepartures(data.departures);
            this.updateLastUpdated();
            this.updateStationName();
            this.updateMockDataNotice(data.is_mock_data);
            
        } catch (error) {
            console.error('Error loading departures:', error);
            this.showError('Failed to load departures. Please try again.');
        } finally {
            this.isLoading = false;
            this.showLoading(false);
        }
    }

    displayDepartures(departures) {
        const departuresList = document.getElementById('departuresList');
        if (!departuresList) return;

        if (!departures || departures.length === 0) {
            departuresList.innerHTML = `
                <div class="departure-item" style="grid-column: 1 / -1; text-align: center; padding: 2rem;">
                    <p style="color: var(--text-secondary); font-size: 1.1rem;">
                        No departures found for this station.
                    </p>
                </div>
            `;
            return;
        }

        const departuresHTML = departures.map(departure => this.createDepartureHTML(departure)).join('');
        departuresList.innerHTML = departuresHTML;
    }

    createDepartureHTML(departure) {
        const statusClass = this.getStatusClass(departure.status);
        const statusIcon = this.getStatusIcon(departure.status);
        const delayText = departure.delay > 0 ? ` (+${departure.delay}m)` : '';
        
        const itemClass = `departure-item ${departure.cancelled ? 'cancelled' : ''} ${departure.status === 'Delayed' ? 'delayed' : ''}`;
        
        return `
            <div class="${itemClass}">
                <div class="departure-time">
                    ${departure.estimated_departure}
                    ${delayText}
                </div>
                <div class="departure-destination">
                    ${departure.destination}
                </div>
                <div class="departure-operator">
                    ${departure.operator}
                </div>
                <div class="departure-platform">
                    ${departure.platform}
                </div>
                <div class="departure-status ${statusClass}">
                    <i class="${statusIcon}"></i>
                    ${departure.status}
                </div>
            </div>
        `;
    }

    getStatusClass(status) {
        const statusMap = {
            'On Time': 'status-on-time',
            'Delayed': 'status-delayed',
            'Cancelled': 'status-cancelled',
            'Platform Change': 'status-platform-change'
        };
        return statusMap[status] || 'status-on-time';
    }

    getStatusIcon(status) {
        const iconMap = {
            'On Time': 'fas fa-check-circle',
            'Delayed': 'fas fa-clock',
            'Cancelled': 'fas fa-times-circle',
            'Platform Change': 'fas fa-exchange-alt'
        };
        return iconMap[status] || 'fas fa-info-circle';
    }

    updateLastUpdated() {
        const now = new Date();
        const timeString = now.toLocaleTimeString('en-GB', {
            hour: '2-digit',
            minute: '2-digit'
        });
        
        const lastUpdatedElement = document.getElementById('lastUpdated');
        if (lastUpdatedElement) {
            lastUpdatedElement.textContent = `Last updated: ${timeString}`;
        }
    }

    updateStationName() {
        const stationSelect = document.getElementById('stationSelect');
        const stationNameElement = document.getElementById('stationName');
        
        if (stationSelect && stationNameElement) {
            const selectedOption = stationSelect.options[stationSelect.selectedIndex];
            const stationName = selectedOption ? selectedOption.text.split(' (')[0] : 'Departures';
            stationNameElement.textContent = `${stationName} Departures`;
        }
    }

    updateMockDataNotice(isMockData) {
        const mockDataNotice = document.getElementById('mockDataNotice');
        if (mockDataNotice) {
            mockDataNotice.style.display = isMockData ? 'flex' : 'none';
        }
    }

    showLoading(show) {
        const loadingElement = document.getElementById('loading');
        if (loadingElement) {
            loadingElement.style.display = show ? 'flex' : 'none';
        }
    }

    showError(message) {
        const errorElement = document.getElementById('errorMessage');
        const errorTextElement = document.getElementById('errorText');
        
        if (errorElement && errorTextElement) {
            errorTextElement.textContent = message;
            errorElement.style.display = 'flex';
        }
    }

    hideError() {
        const errorElement = document.getElementById('errorMessage');
        if (errorElement) {
            errorElement.style.display = 'none';
        }
    }

    startAutoRefresh() {
        if (this.refreshInterval) {
            clearInterval(this.refreshInterval);
        }
        
        // Refresh every 60 seconds
        this.refreshInterval = setInterval(() => {
            if (this.autoRefreshEnabled) {
                this.loadDepartures();
            }
        }, 60000);
    }

    stopAutoRefresh() {
        if (this.refreshInterval) {
            clearInterval(this.refreshInterval);
            this.refreshInterval = null;
        }
    }
}

// Initialize the departure board when the DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new DepartureBoard();
});

// Handle page visibility changes to pause/resume auto-refresh
document.addEventListener('visibilitychange', () => {
    const autoRefreshCheckbox = document.getElementById('autoRefresh');
    if (autoRefreshCheckbox && !autoRefreshCheckbox.checked) {
        return; // Don't manage auto-refresh if it's disabled
    }
    
    if (document.hidden) {
        // Page is hidden, could pause auto-refresh here if needed
        console.log('Page hidden');
    } else {
        // Page is visible again, refresh data
        console.log('Page visible');
        // Trigger a refresh when the page becomes visible
        setTimeout(() => {
            const departureBoard = window.departureBoard;
            if (departureBoard) {
                departureBoard.loadDepartures();
            }
        }, 1000);
    }
}); 
// Main JavaScript for Stock Trading Assistant

// Global variables
let searchTimeout;
let selectedStockSymbol = '';
let selectedExchange = 'NSE';

// Initialize stock search functionality
function initializeStockSearch() {
    const searchInput = document.getElementById('stockSearch');
    const exchangeSelect = document.getElementById('exchangeSelect');
    const searchForm = document.getElementById('stockSearchForm');
    const searchDropdown = document.getElementById('searchDropdown');

    // Initialize watchlist search
    initializeWatchlistSearch();

    if (!searchInput) return;

    // Handle search input
    searchInput.addEventListener('input', function() {
        const query = this.value.trim();
        
        if (query.length < 2) {
            hideSearchDropdown();
            return;
        }

        // Clear previous timeout
        clearTimeout(searchTimeout);
        
        // Set new timeout to debounce API calls
        searchTimeout = setTimeout(() => {
            searchStocks(query);
        }, 300);
    });

    // Handle form submission
    if (searchForm) {
        searchForm.addEventListener('submit', function(e) {
            e.preventDefault();
            analyzeSelectedStock();
        });
    }

    // Handle exchange selection
    if (exchangeSelect) {
        exchangeSelect.addEventListener('change', function() {
            selectedExchange = this.value;
        });
    }

    // Handle clicking outside to close dropdown
    document.addEventListener('click', function(e) {
        if (!searchInput.contains(e.target) && !searchDropdown.contains(e.target)) {
            hideSearchDropdown();
        }
    });

    // Handle keyboard navigation in dropdown
    searchInput.addEventListener('keydown', function(e) {
        const activeItem = searchDropdown.querySelector('.dropdown-item.active');
        const items = searchDropdown.querySelectorAll('.dropdown-item');
        
        switch(e.key) {
            case 'ArrowDown':
                e.preventDefault();
                if (activeItem) {
                    const nextItem = activeItem.nextElementSibling;
                    if (nextItem) {
                        activeItem.classList.remove('active');
                        nextItem.classList.add('active');
                    }
                } else if (items.length > 0) {
                    items[0].classList.add('active');
                }
                break;
                
            case 'ArrowUp':
                e.preventDefault();
                if (activeItem) {
                    const prevItem = activeItem.previousElementSibling;
                    if (prevItem) {
                        activeItem.classList.remove('active');
                        prevItem.classList.add('active');
                    }
                } else if (items.length > 0) {
                    items[items.length - 1].classList.add('active');
                }
                break;
                
            case 'Enter':
                e.preventDefault();
                if (activeItem) {
                    selectStock(activeItem);
                } else {
                    analyzeSelectedStock();
                }
                break;
                
            case 'Escape':
                hideSearchDropdown();
                break;
        }
    });
}

// Search for stocks using API
async function searchStocks(query) {
    try {
        showSearchLoading();
        
        const response = await fetch(`/api/search_stocks?q=${encodeURIComponent(query)}`);
        
        if (!response.ok) {
            throw new Error('Failed to fetch search results');
        }
        
        const suggestions = await response.json();
        displaySearchResults(suggestions);
        
    } catch (error) {
        console.error('Error searching stocks:', error);
        showSearchError();
    }
}

// Display search results in dropdown
function displaySearchResults(suggestions) {
    const dropdown = document.getElementById('searchDropdown');
    
    if (!suggestions || suggestions.length === 0) {
        dropdown.innerHTML = '<div class="dropdown-item text-muted">No stocks found</div>';
        showSearchDropdown();
        return;
    }

    let html = '';
    suggestions.forEach((stock, index) => {
        html += `
            <div class="dropdown-item search-result" 
                 data-symbol="${stock.symbol}" 
                 data-nse="${stock.nse_symbol}" 
                 data-bse="${stock.bse_symbol}"
                 onclick="selectStock(this)">
                <div class="d-flex justify-content-between align-items-start">
                    <div class="flex-grow-1">
                        <div class="search-result-symbol">${stock.symbol}</div>
                        <div class="search-result-name small">${stock.name}</div>
                    </div>
                    <div class="text-end">
                        <div class="search-result-exchange small">
                            <span class="badge bg-primary me-1">NSE</span>
                            <span class="badge bg-secondary">BSE</span>
                        </div>
                    </div>
                </div>
            </div>
        `;
    });

    dropdown.innerHTML = html;
    showSearchDropdown();
}

// Show search loading state
function showSearchLoading() {
    const dropdown = document.getElementById('searchDropdown');
    dropdown.innerHTML = `
        <div class="dropdown-item text-center">
            <div class="loading-spinner me-2"></div>
            Searching stocks...
        </div>
    `;
    showSearchDropdown();
}

// Show search error
function showSearchError() {
    const dropdown = document.getElementById('searchDropdown');
    dropdown.innerHTML = `
        <div class="dropdown-item text-danger">
            <i data-feather="alert-circle" class="me-2"></i>
            Error searching stocks
        </div>
    `;
    showSearchDropdown();
    feather.replace();
}

// Select a stock from search results
function selectStock(element) {
    const symbol = element.dataset.symbol;
    const nseSymbol = element.dataset.nse;
    const bseSymbol = element.dataset.bse;
    
    // Update search input
    const searchInput = document.getElementById('stockSearch');
    searchInput.value = symbol;
    
    // Store selected stock info
    selectedStockSymbol = selectedExchange === 'BSE' ? bseSymbol : nseSymbol;
    
    hideSearchDropdown();
}

// Analyze the selected stock
function analyzeSelectedStock() {
    const searchInput = document.getElementById('stockSearch');
    let symbol = searchInput.value.trim().toUpperCase();
    
    if (!symbol) {
        showAlert('Please enter a stock symbol', 'warning');
        return;
    }
    
    // If we have a selected symbol from dropdown, use it
    if (selectedStockSymbol) {
        symbol = selectedStockSymbol;
    } else {
        // Format symbol for selected exchange
        if (!symbol.endsWith('.NS') && !symbol.endsWith('.BO')) {
            symbol = selectedExchange === 'BSE' ? `${symbol}.BO` : `${symbol}.NS`;
        }
    }
    
    // Show loading state
    showAnalysisLoading();
    
    // Navigate to analysis page
    window.location.href = `/analyze/${symbol}`;
}

// Show/hide search dropdown
function showSearchDropdown() {
    const dropdown = document.getElementById('searchDropdown');
    dropdown.style.display = 'block';
}

function hideSearchDropdown() {
    const dropdown = document.getElementById('searchDropdown');
    dropdown.style.display = 'none';
    
    // Clear active items
    dropdown.querySelectorAll('.dropdown-item.active').forEach(item => {
        item.classList.remove('active');
    });
}

// Show analysis loading state
function showAnalysisLoading() {
    const form = document.getElementById('stockSearchForm');
    const submitBtn = form.querySelector('button[type="submit"]');
    
    if (submitBtn) {
        submitBtn.disabled = true;
        submitBtn.innerHTML = `
            <div class="loading-spinner me-2"></div>
            Analyzing...
        `;
    }
}

// Show alert message
function showAlert(message, type = 'info') {
    const alertContainer = document.createElement('div');
    alertContainer.className = `alert alert-${type} alert-dismissible fade show`;
    alertContainer.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    // Insert at top of main content
    const main = document.querySelector('main');
    if (main && main.firstChild) {
        main.insertBefore(alertContainer, main.firstChild);
    }
    
    // Auto-dismiss after 5 seconds
    setTimeout(() => {
        if (alertContainer && alertContainer.parentNode) {
            alertContainer.remove();
        }
    }, 5000);
}

// Format number with commas
function formatNumber(num) {
    return num.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ',');
}

// Format currency
function formatCurrency(amount, currency = '₹') {
    return `${currency}${formatNumber(amount.toFixed(2))}`;
}

// Format percentage
function formatPercentage(value) {
    return `${value.toFixed(2)}%`;
}

// Copy to clipboard functionality
function copyToClipboard(text) {
    navigator.clipboard.writeText(text).then(() => {
        showAlert('Copied to clipboard!', 'success');
    }).catch(err => {
        console.error('Error copying to clipboard:', err);
        showAlert('Failed to copy to clipboard', 'danger');
    });
}

// Initialize tooltips
function initializeTooltips() {
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
}

// Initialize popovers
function initializePopovers() {
    const popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });
}

// Handle page visibility change
document.addEventListener('visibilitychange', function() {
    if (document.visibilityState === 'visible') {
        // Page became visible - could refresh data
        console.log('Page became visible');
    } else {
        // Page became hidden
        console.log('Page became hidden');
    }
});

// Initialize everything when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    initializeTooltips();
    initializePopovers();
    
    // Initialize Feather icons
    if (typeof feather !== 'undefined') {
        feather.replace();
    }
    
    // Log that the app is ready
    console.log('Stock Trading Assistant initialized');
});

// Initialize watchlist search functionality
function initializeWatchlistSearch() {
    const watchlistInput = document.getElementById('watchlistSymbol');
    const watchlistDropdown = document.getElementById('watchlistSearchDropdown');
    let watchlistTimeout;

    if (!watchlistInput) return;

    // Handle watchlist search input
    watchlistInput.addEventListener('input', function() {
        const query = this.value.trim();
        
        if (query.length < 2) {
            hideWatchlistDropdown();
            return;
        }

        // Clear previous timeout
        clearTimeout(watchlistTimeout);
        
        // Set new timeout to debounce API calls
        watchlistTimeout = setTimeout(() => {
            searchStocksForWatchlist(query);
        }, 300);
    });

    // Handle clicking outside to close dropdown
    document.addEventListener('click', function(e) {
        if (!watchlistInput.contains(e.target) && !watchlistDropdown.contains(e.target)) {
            hideWatchlistDropdown();
        }
    });

    // Handle keyboard navigation
    watchlistInput.addEventListener('keydown', function(e) {
        const activeItem = watchlistDropdown.querySelector('.dropdown-item.active');
        const items = watchlistDropdown.querySelectorAll('.dropdown-item');
        
        switch(e.key) {
            case 'ArrowDown':
                e.preventDefault();
                if (activeItem) {
                    const nextItem = activeItem.nextElementSibling;
                    if (nextItem) {
                        activeItem.classList.remove('active');
                        nextItem.classList.add('active');
                    }
                } else if (items.length > 0) {
                    items[0].classList.add('active');
                }
                break;
                
            case 'ArrowUp':
                e.preventDefault();
                if (activeItem) {
                    const prevItem = activeItem.previousElementSibling;
                    if (prevItem) {
                        activeItem.classList.remove('active');
                        prevItem.classList.add('active');
                    }
                } else if (items.length > 0) {
                    items[items.length - 1].classList.add('active');
                }
                break;
                
            case 'Enter':
                e.preventDefault();
                if (activeItem) {
                    selectWatchlistStock(activeItem);
                }
                break;
                
            case 'Escape':
                hideWatchlistDropdown();
                break;
        }
    });
}

// Search stocks for watchlist
async function searchStocksForWatchlist(query) {
    try {
        const response = await fetch(`/api/search_stocks?q=${encodeURIComponent(query)}`);
        
        if (!response.ok) {
            throw new Error('Failed to fetch search results');
        }
        
        const suggestions = await response.json();
        displayWatchlistSearchResults(suggestions);
        
    } catch (error) {
        console.error('Error searching stocks for watchlist:', error);
        showWatchlistSearchError();
    }
}

// Display watchlist search results
function displayWatchlistSearchResults(suggestions) {
    const dropdown = document.getElementById('watchlistSearchDropdown');
    
    if (!suggestions || suggestions.length === 0) {
        dropdown.innerHTML = '<div class="dropdown-item text-muted">No stocks found</div>';
        showWatchlistDropdown();
        return;
    }

    let html = '';
    suggestions.forEach((stock, index) => {
        html += `
            <div class="dropdown-item search-result" 
                 data-symbol="${stock.symbol}" 
                 data-nse="${stock.nse_symbol}" 
                 data-bse="${stock.bse_symbol}"
                 onclick="selectWatchlistStock(this)">
                <div class="d-flex justify-content-between align-items-start">
                    <div class="flex-grow-1">
                        <div class="search-result-symbol">${stock.symbol}</div>
                        <div class="search-result-name small">${stock.name}</div>
                    </div>
                    <div class="text-end">
                        <div class="search-result-exchange small">
                            <span class="badge bg-primary me-1">NSE</span>
                            <span class="badge bg-secondary">BSE</span>
                        </div>
                    </div>
                </div>
            </div>
        `;
    });

    dropdown.innerHTML = html;
    showWatchlistDropdown();
}

// Select stock for watchlist
function selectWatchlistStock(element) {
    const symbol = element.dataset.symbol;
    const watchlistInput = document.getElementById('watchlistSymbol');
    watchlistInput.value = symbol;
    hideWatchlistDropdown();
}

// Show/hide watchlist dropdown
function showWatchlistDropdown() {
    const dropdown = document.getElementById('watchlistSearchDropdown');
    dropdown.style.display = 'block';
}

function hideWatchlistDropdown() {
    const dropdown = document.getElementById('watchlistSearchDropdown');
    dropdown.style.display = 'none';
    
    // Clear active items
    dropdown.querySelectorAll('.dropdown-item.active').forEach(item => {
        item.classList.remove('active');
    });
}

// Show watchlist search error
function showWatchlistSearchError() {
    const dropdown = document.getElementById('watchlistSearchDropdown');
    dropdown.innerHTML = `
        <div class="dropdown-item text-danger">
            <i data-feather="alert-circle" class="me-2"></i>
            Error searching stocks
        </div>
    `;
    showWatchlistDropdown();
    feather.replace();
}

// Export functions for use in other scripts
window.StockAssistant = {
    searchStocks,
    selectStock,
    analyzeSelectedStock,
    showAlert,
    formatNumber,
    formatCurrency,
    formatPercentage,
    copyToClipboard
};

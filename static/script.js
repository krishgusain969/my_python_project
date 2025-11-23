// Enhanced JavaScript for Lost & Found Portal

// Form validation and enhancement
document.addEventListener('DOMContentLoaded', function() {
    // Animate elements on load
    animateOnLoad();
    
    // Form validation
    setupFormValidation();
    
    // Search functionality
    setupSearch();
    
    // Auto-dismiss alerts
    autoDismissAlerts();
    
    // Smooth scrolling
    setupSmoothScroll();
    
    // Item card animations
    setupItemCardAnimations();
    
    // Real-time search
    setupRealTimeSearch();
});

// Animate elements on page load
function animateOnLoad() {
    const cards = document.querySelectorAll('.option-card, .action-card, .item-card');
    cards.forEach((card, index) => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(20px)';
        setTimeout(() => {
            card.style.transition = 'all 0.5s ease';
            card.style.opacity = '1';
            card.style.transform = 'translateY(0)';
        }, index * 100);
    });
}

// Form validation
function setupFormValidation() {
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            let isValid = true;
            const inputs = form.querySelectorAll('input[required], textarea[required]');
            
            inputs.forEach(input => {
                if (!input.value.trim()) {
                    isValid = false;
                    input.classList.add('error');
                    showFieldError(input, 'This field is required');
                } else {
                    input.classList.remove('error');
                    removeFieldError(input);
                }
            });
            
            // Password confirmation validation
            const password = form.querySelector('#password');
            const confirmPassword = form.querySelector('#confirm_password');
            if (password && confirmPassword) {
                if (password.value !== confirmPassword.value) {
                    isValid = false;
                    confirmPassword.classList.add('error');
                    showFieldError(confirmPassword, 'Passwords do not match');
                } else {
                    confirmPassword.classList.remove('error');
                    removeFieldError(confirmPassword);
                }
            }
            
            // Password strength check
            if (password && password.value.length < 6) {
                isValid = false;
                password.classList.add('error');
                showFieldError(password, 'Password must be at least 6 characters');
            }
            
            if (!isValid) {
                e.preventDefault();
            }
        });
        
        // Real-time validation
        const inputs = form.querySelectorAll('input, textarea');
        inputs.forEach(input => {
            input.addEventListener('blur', function() {
                if (input.hasAttribute('required') && !input.value.trim()) {
                    input.classList.add('error');
                    showFieldError(input, 'This field is required');
                } else {
                    input.classList.remove('error');
                    removeFieldError(input);
                }
            });
            
            input.addEventListener('input', function() {
                if (input.value.trim()) {
                    input.classList.remove('error');
                    removeFieldError(input);
                }
            });
        });
    });
}

// Show field error
function showFieldError(input, message) {
    removeFieldError(input);
    const errorDiv = document.createElement('div');
    errorDiv.className = 'field-error';
    errorDiv.textContent = message;
    input.parentNode.appendChild(errorDiv);
}

// Remove field error
function removeFieldError(input) {
    const error = input.parentNode.querySelector('.field-error');
    if (error) {
        error.remove();
    }
}

// Search functionality
function setupSearch() {
    const searchInputs = document.querySelectorAll('.search-input');
    searchInputs.forEach(input => {
        input.addEventListener('input', function() {
            const query = this.value.toLowerCase();
            const items = document.querySelectorAll('.item-card');
            
            items.forEach(item => {
                const text = item.textContent.toLowerCase();
                if (text.includes(query)) {
                    item.style.display = '';
                    item.style.animation = 'fadeIn 0.3s ease';
                } else {
                    item.style.display = 'none';
                }
            });
            
            // Show no results message
            const visibleItems = Array.from(items).filter(item => item.style.display !== 'none');
            const noResults = document.querySelector('.no-results');
            if (visibleItems.length === 0 && query) {
                if (!noResults) {
                    const msg = document.createElement('p');
                    msg.className = 'no-results';
                    msg.textContent = 'No items found matching your search.';
                    msg.style.textAlign = 'center';
                    msg.style.padding = '20px';
                    msg.style.color = '#666';
                    const container = document.querySelector('.items-grid') || document.querySelector('.items-section');
                    if (container) {
                        container.appendChild(msg);
                    }
                }
            } else if (noResults) {
                noResults.remove();
            }
        });
    });
}

// Real-time search with API
function setupRealTimeSearch() {
    const searchInput = document.querySelector('#real-time-search');
    if (!searchInput) return;
    
    let searchTimeout;
    searchInput.addEventListener('input', function() {
        clearTimeout(searchTimeout);
        const query = this.value;
        
        searchTimeout = setTimeout(() => {
            if (query.length >= 2 || query.length === 0) {
                performSearch(query);
            }
        }, 300);
    });
}

function performSearch(query) {
    const params = new URLSearchParams();
    if (query) params.append('q', query);
    
    const typeFilter = document.querySelector('#filter-type');
    if (typeFilter && typeFilter.value !== 'all') {
        params.append('type', typeFilter.value);
    }
    
    const categoryFilter = document.querySelector('#filter-category');
    if (categoryFilter && categoryFilter.value !== 'all') {
        params.append('category', categoryFilter.value);
    }
    
    fetch(`/api/search?${params.toString()}`)
        .then(response => response.json())
        .then(data => {
            updateSearchResults(data);
        })
        .catch(error => console.error('Search error:', error));
}

function updateSearchResults(items) {
    const container = document.querySelector('.items-grid');
    if (!container) return;
    
    container.innerHTML = '';
    
    if (items.length === 0) {
        container.innerHTML = '<p class="no-items">No items found.</p>';
        return;
    }
    
    items.forEach(item => {
        const card = createItemCard(item);
        container.appendChild(card);
    });
}

function createItemCard(item) {
    const card = document.createElement('div');
    card.className = `item-card status-${item.status}`;
    card.innerHTML = `
        <div class="item-header">
            <span class="item-type">${item.type.toUpperCase()}</span>
            <span class="item-status status-${item.status}">${item.status.toUpperCase()}</span>
        </div>
        <h3>${item.item_name}</h3>
        <div class="item-details">
            <p><strong>Color:</strong> ${item.color}</p>
            <p><strong>Location:</strong> ${item.location}</p>
            ${item.description ? `<p><strong>Description:</strong> ${item.description}</p>` : ''}
            <p><strong>Date:</strong> ${item.date}</p>
        </div>
    `;
    return card;
}

// Auto-dismiss alerts
function autoDismissAlerts() {
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            alert.style.transition = 'opacity 0.5s ease';
            alert.style.opacity = '0';
            setTimeout(() => alert.remove(), 500);
        }, 5000);
    });
}

// Smooth scrolling
function setupSmoothScroll() {
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            const href = this.getAttribute('href');
            if (href !== '#') {
                e.preventDefault();
                const target = document.querySelector(href);
                if (target) {
                    target.scrollIntoView({ behavior: 'smooth' });
                }
            }
        });
    });
}

// Item card animations
function setupItemCardAnimations() {
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.animation = 'fadeInUp 0.5s ease forwards';
                observer.unobserve(entry.target);
            }
        });
    }, { threshold: 0.1 });
    
    document.querySelectorAll('.item-card').forEach(card => {
        observer.observe(card);
    });
}

// Filter functionality
function setupFilters() {
    const filterButtons = document.querySelectorAll('.filter-btn');
    filterButtons.forEach(btn => {
        btn.addEventListener('click', function() {
            filterButtons.forEach(b => b.classList.remove('active'));
            this.classList.add('active');
            
            const filter = this.dataset.filter;
            const items = document.querySelectorAll('.item-card');
            
            items.forEach(item => {
                if (filter === 'all' || item.classList.contains(`status-${filter}`)) {
                    item.style.display = '';
                } else {
                    item.style.display = 'none';
                }
            });
        });
    });
}

// Match highlighting
function highlightMatches(itemCard, matches) {
    if (matches && matches.length > 0) {
        const matchDiv = document.createElement('div');
        matchDiv.className = 'matches-section';
        matchDiv.innerHTML = `
            <h4>🎯 Potential Matches (${matches.length})</h4>
            <div class="matches-list">
                ${matches.map(match => `
                    <div class="match-item">
                        <strong>${match.item_name}</strong> - ${match.type} at ${match.location}
                        <span class="match-score">Match: ${Math.round(match.match_score)}%</span>
                    </div>
                `).join('')}
            </div>
        `;
        itemCard.appendChild(matchDiv);
    }
}

// Loading spinner
function showLoading() {
    const spinner = document.createElement('div');
    spinner.className = 'loading-spinner';
    spinner.innerHTML = '<div class="spinner"></div>';
    document.body.appendChild(spinner);
}

function hideLoading() {
    const spinner = document.querySelector('.loading-spinner');
    if (spinner) spinner.remove();
}

// Confirmation dialogs
function confirmAction(message, callback) {
    if (confirm(message)) {
        callback();
    }
}

// Initialize filters on page load
if (document.querySelector('.filter-btn')) {
    setupFilters();
}


// YouTube Clone - Main JavaScript

console.log('SCRIPT_JS_LOADED_TEST_v3');
document.addEventListener('DOMContentLoaded', function () {
    // Elements
    const menuBtn = document.getElementById('menuBtn');
    const sidebar = document.getElementById('sidebar');
    const mainContent = document.getElementById('mainContent');
    const categoryChips = document.querySelectorAll('.category-chip');

    // Sidebar toggle
    menuBtn.addEventListener('click', function () {
        sidebar.classList.toggle('open');

        // Create or toggle overlay for mobile
        let overlay = document.querySelector('.sidebar-overlay');
        if (!overlay) {
            overlay = document.createElement('div');
            overlay.className = 'sidebar-overlay';
            document.body.appendChild(overlay);

            overlay.addEventListener('click', function () {
                sidebar.classList.remove('open');
                overlay.classList.remove('active');
            });
        }

        if (sidebar.classList.contains('open')) {
            overlay.classList.add('active');
        } else {
            overlay.classList.remove('active');
        }

        // Toggle Settings Visibility
        const settingsSection = document.getElementById('settingsSection');
        if (settingsSection) {
            settingsSection.classList.toggle('visible');
        }
    });

    // Category chip selection
    categoryChips.forEach(chip => {
        chip.addEventListener('click', function () {
            // Remove active class from all chips
            categoryChips.forEach(c => c.classList.remove('active'));
            // Add active class to clicked chip
            this.classList.add('active');

            // Add a subtle pulse animation
            this.style.transform = 'scale(0.95)';
            setTimeout(() => {
                this.style.transform = 'scale(1)';
            }, 100);
        });
    });

    // Search input focus animation
    const searchInput = document.querySelector('.search-input');
    if (searchInput) {
        searchInput.addEventListener('focus', function () {
            this.parentElement.style.boxShadow = '0 0 0 1px #1c62b9';
        });

        searchInput.addEventListener('blur', function () {
            this.parentElement.style.boxShadow = 'none';
        });
    }

    // Video card hover effects
    const videoCards = document.querySelectorAll('.video-card');
    videoCards.forEach(card => {
        card.addEventListener('mouseenter', function () {
            const thumbnail = this.querySelector('.thumbnail');
            if (thumbnail) {
                // Could add preview functionality here in the future
            }
        });
    });

    // Shorts horizontal scroll with mouse wheel
    const shortsContainer = document.querySelector('.shorts-container');
    if (shortsContainer) {
        shortsContainer.addEventListener('wheel', function (e) {
            if (e.deltaY !== 0) {
                e.preventDefault();
                this.scrollLeft += e.deltaY;
            }
        }, { passive: false });
    }

    // Lazy loading simulation for thumbnails
    const observerOptions = {
        root: null,
        rootMargin: '50px',
        threshold: 0.1
    };

    const imageObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const img = entry.target;
                if (img.dataset.src) {
                    img.src = img.dataset.src;
                    img.removeAttribute('data-src');
                }
                observer.unobserve(img);
            }
        });
    }, observerOptions);

    // Observe all images with data-src attribute
    document.querySelectorAll('img[data-src]').forEach(img => {
        imageObserver.observe(img);
    });

    // Keyboard navigation
    document.addEventListener('keydown', function (e) {
        // Focus search on '/' key
        if (e.key === '/' && document.activeElement !== searchInput) {
            e.preventDefault();
            searchInput.focus();
        }

        // Close sidebar on Escape
        if (e.key === 'Escape') {
            sidebar.classList.remove('open');
            const overlay = document.querySelector('.sidebar-overlay');
            if (overlay) {
                overlay.classList.remove('active');
            }
        }
    });

    // Sidebar active state logic
    const currentPath = window.location.pathname;
    const sidebarItems = document.querySelectorAll('.sidebar-item');

    sidebarItems.forEach(item => {
        const itemPath = item.getAttribute('href');
        if (itemPath === currentPath) {
            sidebarItems.forEach(i => i.classList.remove('active'));
            item.classList.add('active');
        } else if (currentPath === '/' && itemPath === '/') {
            item.classList.add('active');
        } else if (currentPath.startsWith('/watch/') && itemPath === '/') {
            // Keep Home active or nothing if watch page
            // Actually YouTube usually keeps Home active if you came from there but let's be precise
        }
    });

    // Unified Subscribe Logic
    function handleSubscription(btn, bell = null) {
        const name = btn.getAttribute('data-channel-name');
        const avatar = btn.getAttribute('data-channel-avatar');
        const isSubscribed = btn.classList.contains('subscribed');

        if (!isSubscribed) {
            // Subscribe
            btn.classList.add('subscribed');
            btn.textContent = 'Subscribed';
            if (bell) {
                bell.classList.add('show-bell'); // Shorts bell
                setTimeout(() => bell.classList.remove('show-bell'), 2500);
            } else if (bellNotification) {
                bellNotification.classList.add('show'); // Watch page bell
            }
        } else {
            // Unsubscribe
            btn.classList.remove('subscribed');
            btn.textContent = 'Subscribe';
            if (bellNotification) bellNotification.classList.remove('show');
        }

        // AJAX Persistence
        if (name && avatar) {
            fetch('/toggle-subscription/', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ name: name, avatar: avatar })
            }).then(response => response.json())
                .then(data => console.log('Subscription toggled:', data));
        }
    }

    const subscribeBtn = document.getElementById('subscribeBtn');
    if (subscribeBtn) {
        subscribeBtn.addEventListener('click', () => handleSubscription(subscribeBtn));
    }

    const shortsSubscribeBtns = document.querySelectorAll('.shorts-subscribe-btn');
    shortsSubscribeBtns.forEach(btn => {
        btn.addEventListener('click', function () {
            const parent = this.closest('.shorts-channel-info');
            const bell = parent.querySelector('.shorts-bell-icon');
            handleSubscription(this, bell);
        });
    });

    // Like/Dislike Button Logic
    function handleLikeDislike() {
        const likeBtns = document.querySelectorAll('.like-btn, .shorts-action-btn:nth-child(1)');
        const dislikeBtns = document.querySelectorAll('.dislike-btn, .shorts-action-btn:nth-child(2)');

        function applyGlow(btn) {
            btn.classList.add('btn-glow');
            setTimeout(() => {
                btn.classList.remove('btn-glow');
            }, 1000);
        }

        document.addEventListener('click', function (e) {
            const likeBtn = e.target.closest('.like-btn') ||
                (e.target.closest('.shorts-action-btn') && e.target.closest('.shorts-action-btn').querySelector('path[d*="M18.77 11h-4.23"]')?.parentElement?.parentElement);
            const dislikeBtn = e.target.closest('.dislike-btn') ||
                (e.target.closest('.shorts-action-btn') && e.target.closest('.shorts-action-btn').querySelector('path[d*="M17 4h-1H6.57"]')?.parentElement?.parentElement);

            if (likeBtn) {
                const container = likeBtn.closest('.like-dislike-container') || likeBtn.parentElement;
                const dislikeInGroup = container.querySelector('.dislike-btn') || container.querySelector('.shorts-action-btn:nth-child(2)');
                const videoId = container.getAttribute('data-video-id');

                if (likeBtn.classList.contains('liked')) {
                    likeBtn.classList.remove('liked');
                } else {
                    likeBtn.classList.add('liked');
                    if (dislikeInGroup) dislikeInGroup.classList.remove('disliked');
                    applyGlow(likeBtn);
                }

                if (videoId) {
                    fetch('/toggle-like/', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify({ video_id: videoId })
                    }).then(response => response.json())
                        .then(data => console.log('Like toggled:', data));
                }
            }

            if (dislikeBtn) {
                const container = dislikeBtn.closest('.like-dislike-container') || dislikeBtn.parentElement;
                const likeInGroup = container.querySelector('.like-btn') || container.querySelector('.shorts-action-btn:nth-child(1)');

                if (dislikeBtn.classList.contains('disliked')) {
                    dislikeBtn.classList.remove('disliked');
                } else {
                    dislikeBtn.classList.add('disliked');
                    if (likeInGroup) likeInGroup.classList.remove('liked');
                    applyGlow(dislikeBtn);
                }
            }
        });
    }

    handleLikeDislike();

    // Save (Watch Later) Button Logic
    const saveBtn = document.querySelector('.save-btn');
    if (saveBtn) {
        saveBtn.addEventListener('click', function () {
            const videoId = this.getAttribute('data-video-id');
            if (!videoId) return;

            // Apply 1-second glow
            this.classList.add('btn-glow');
            setTimeout(() => {
                this.classList.remove('btn-glow');
            }, 1000);

            // Toggle visual state
            this.classList.toggle('saved');
            const span = this.querySelector('span');
            if (this.classList.contains('saved')) {
                span.textContent = 'Saved';
            } else {
                span.textContent = 'Save';
            }

            // AJAX Persistence
            fetch('/toggle-watch-later/', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ video_id: videoId })
            }).then(response => response.json())
                .then(data => console.log('Watch later toggled:', data));
        });
    }

    // Bell click logic (toggle "all notifications")
    if (bellNotification) {
        bellNotification.addEventListener('click', function () {
            this.classList.toggle('active');
            const bellIcon = this.querySelector('.bell-icon');
            if (this.classList.contains('active')) {
                bellIcon.style.color = '#3ea6ff';
            } else {
                bellIcon.style.color = 'var(--accent-red)';
            }
        });
    }

    // Console welcome message
    console.log('%c YouTube Clone v3 ', 'background: #ff0000; color: white; font-size: 24px; font-weight: bold; padding: 10px 20px; border-radius: 4px;');
    console.log('Welcome to YouTube Clone! Built with Django.');
});


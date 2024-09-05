document.addEventListener("DOMContentLoaded", () => {
    const sidebar = document.querySelector('.sidebar');
    const toggleSidebarBtn = document.createElement('div');
    const loadingOverlay = document.getElementById('loading');
    const minLoadingTime = 800;
    const transitionDuration = 0.5; 
    const badges = document.querySelectorAll('.badge-outline-pill');
    const mainContent = document.querySelector('.main-content');
    const navLinks = document.querySelectorAll('.nav-link');
    const tableRows = document.querySelectorAll('.table-hover tbody tr');
    const deleteButtons = document.querySelectorAll('[data-bs-toggle="modal"][data-bs-target="#deleteModal"]');
    const modals = document.querySelectorAll('.modal');
    const forms = document.querySelectorAll('form');

    toggleSidebarBtn.classList.add('toggle-sidebar-btn');
    toggleSidebarBtn.innerHTML = '<span class="material-icons">menu</span>';
    sidebar.appendChild(toggleSidebarBtn);

    // Toggle sidebar
    toggleSidebarBtn.addEventListener('click', () => {
        sidebar.classList.toggle('collapsed');
        mainContent.classList.toggle('expanded');
        mainContent.style.transition = `margin-left ${transitionDuration}s ease`;
    });

    // Expand sidebar when dropdown is clicked
    document.querySelectorAll('.sidebar .nav-link.dropdown-toggle').forEach(link => {
        link.addEventListener('click', () => {
            if (sidebar.classList.contains('collapsed')) {
                sidebar.classList.remove('collapsed');
                mainContent.classList.remove('expanded');
            }
        });
    });

    // Update active nav link based on current URL
    const updateActiveNavLink = () => {
        const currentLocation = window.location.href;
        navLinks.forEach(item => {
            item.classList.toggle('nav-pills-link-active', item.href === currentLocation);
        });
    };

    // Show loading overlay and redirect
    const showLoadingAndRedirect = (url) => {
        loadingOverlay.style.display = 'flex';
        setTimeout(() => {
            loadingOverlay.style.opacity = '1';
            fetch(url, { method: 'GET', headers: { 'X-Requested-With': 'XMLHttpRequest' } })
                .then(response => response.ok ? response.text() : Promise.reject('Erro ao carregar a página'))
                .then(() => {
                    setTimeout(() => {
                        loadingOverlay.style.opacity = '0';
                        setTimeout(() => {
                            loadingOverlay.style.display = 'none';
                            window.location.href = url;
                        }, 300);
                    }, minLoadingTime);
                })
                .catch(error => {
                    console.error('Erro:', error);
                    loadingOverlay.style.display = 'none';
                });
        }, 300);
    };

    // Debounced scroll handler
    const debounce = (func, wait) => {
        let timeout;
        return function(...args) {
            clearTimeout(timeout);
            timeout = setTimeout(() => func.apply(this, args), wait);
        };
    };

    const handleScroll = debounce(() => {
        // Your scroll logic here
    }, 200);

    window.addEventListener('scroll', handleScroll);

    // Handle various events
    const handleEvents = () => {
        // Handle link clicks
        document.addEventListener('click', (event) => {
            const target = event.target;
            if (target.tagName === 'A' && !target.hasAttribute('data-no-loading') && !target.classList.contains('dropdown-toggle')) {
                event.preventDefault();
                showLoadingAndRedirect(target.href);
            }
        });

        // Handle form submissions
        forms.forEach(form => {
            form.addEventListener('submit', () => {
                if (form.querySelector('button[type="submit"]').classList.contains('btn-jump')) {
                    loadingOverlay.style.display = 'flex';
                }
            });
        });

        // Handle table row hover effect
        tableRows.forEach(row => {
            row.addEventListener('mouseover', () => {
                row.style.backgroundColor = '#e9ecef';
                row.style.transition = `background-color ${transitionDuration}s ease`;
            });
            row.addEventListener('mouseout', () => {
                row.style.backgroundColor = '';
            });
        });

        // Handle delete modal confirmation
        deleteButtons.forEach(button => {
            button.addEventListener('click', () => {
                const deleteUrl = button.getAttribute('data-url');
                const confirmDeleteBtn = document.getElementById('confirmDeleteBtn');
                if (confirmDeleteBtn) {
                    confirmDeleteBtn.onclick = () => window.location.href = deleteUrl;
                }
            });
        });

        // Handle modal show/hide animations
        modals.forEach(modal => {
            modal.addEventListener('show.bs.modal', () => {
                modal.style.transition = `opacity ${transitionDuration}s ease, transform ${transitionDuration}s ease`;
                modal.style.opacity = '0';
                modal.style.transform = 'scale(0.95)';
                requestAnimationFrame(() => {
                    modal.style.opacity = '1';
                    modal.style.transform = 'scale(1)';
                });
            });
            modal.addEventListener('hide.bs.modal', () => {
                modal.style.transition = `opacity ${transitionDuration}s ease, transform ${transitionDuration}s ease`;
                modal.style.opacity = '1';
                modal.style.transform = 'scale(1)';
                requestAnimationFrame(() => {
                    modal.style.opacity = '0';
                    modal.style.transform = 'scale(0.95)';
                });
            });
        });

        // Initialize AOS animations
        AOS.init();

        // Handle custom form submission spinner
        forms.forEach(form => {
            form.addEventListener('submit', () => {
                showSpinner();
                setTimeout(hideSpinner, 2000);
            });
        });

        // Handle toggle button click
        document.querySelector('.toggle-button').addEventListener('click', () => {
            document.querySelector('.toggle-element').classList.toggle('active');
        });
    };

    // Apply custom class based on user area
    const applyUserAreaBadge = () => {
        const userArea = "{{ user.area }}";
        badges.forEach(badge => {
            if (userArea) {
                badge.classList.add(`area-${userArea}`);
            }
        });
    };

    updateActiveNavLink();
    handleEvents();
    applyUserAreaBadge();

    document.body.classList.add('page-transition');
    document.body.classList.add('page-transition-loaded');
});

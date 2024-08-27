document.addEventListener("DOMContentLoaded", () => {
    const sidebar = document.querySelector('.sidebar');
    const toggleSidebarBtn = document.createElement('div');
    const loadingOverlay = document.getElementById('loading');
    const minLoadingTime = 800;
    const transitionDuration = 0.5; 
    const badges = document.querySelectorAll('.badge-outline-pill');

    toggleSidebarBtn.classList.add('toggle-sidebar-btn');
    toggleSidebarBtn.innerHTML = '<span class="material-icons">menu</span>';
    sidebar.appendChild(toggleSidebarBtn);

    toggleSidebarBtn.addEventListener('click', () => {
        sidebar.classList.toggle('collapsed');
        document.querySelector('.main-content').classList.toggle('expanded');
        document.querySelector('.main-content').style.transition = `margin-left ${transitionDuration}s ease`;
    });

    document.querySelectorAll('.sidebar .nav-link.dropdown-toggle').forEach(link => {
        link.addEventListener('click', () => {
            if (sidebar.classList.contains('collapsed')) {
                sidebar.classList.remove('collapsed');
                document.querySelector('.main-content').classList.remove('expanded');
            }
        });
    });

    const updateActiveNavLink = () => {
        const currentLocation = window.location.href;
        document.querySelectorAll('.nav-link').forEach(item => {
            item.classList.toggle('nav-pills-link-active', item.href === currentLocation);
        });
    };

    const showLoadingAndRedirect = (url) => {
        loadingOverlay.style.opacity = '0';
        loadingOverlay.style.display = 'flex';
        setTimeout(() => {
            loadingOverlay.style.opacity = '1';
            fetch(url, { method: 'GET', headers: { 'X-Requested-With': 'XMLHttpRequest' } })
                .then(response => response.ok ? response.text() : Promise.reject('Erro ao carregar a página'))
                .then(() => setTimeout(() => {
                    loadingOverlay.style.opacity = '0';
                    setTimeout(() => {
                        loadingOverlay.style.display = 'none';
                        window.location.href = url;
                    }, 300);
                }, minLoadingTime))
                .catch(error => {
                    console.error('Erro:', error);
                    loadingOverlay.style.display = 'none';
                });
        }, 300);
    };

    const handleEvents = () => {
        document.addEventListener('click', (event) => {
            const target = event.target;

            if (target.tagName === 'A' && !target.hasAttribute('data-no-loading') && !target.classList.contains('dropdown-toggle')) {
                event.preventDefault();
                showLoadingAndRedirect(target.href);
            }
        });

        document.querySelectorAll('form').forEach(form => {
            form.addEventListener('submit', (event) => {
                if (form.querySelector('button[type="submit"]').classList.contains('btn-jump')) {
                    loadingOverlay.style.display = 'flex';
                }
            });
        });

        document.querySelectorAll('.table-hover tbody tr').forEach(row => {
            row.addEventListener('mouseover', () => {
                row.style.backgroundColor = '#e9ecef';
                row.style.transition = `background-color ${transitionDuration}s ease`;
            });
            row.addEventListener('mouseout', () => {
                row.style.backgroundColor = '';
            });
        });

        document.querySelectorAll('[data-bs-target="#deleteModal"]').forEach(button => {
            button.addEventListener('click', () => {
                const deleteUrl = button.getAttribute('data-url');
                document.getElementById('confirmDeleteBtn').onclick = () => window.location.href = deleteUrl;
            });
        });

        document.querySelectorAll('.modal').forEach(modal => {
            modal.addEventListener('show.bs.modal', () => {
                modal.style.transition = `opacity ${transitionDuration}s ease, transform ${transitionDuration}s ease`;
                modal.style.opacity = '0';
                modal.style.transform = 'scale(0.95)';
                setTimeout(() => {
                    modal.style.opacity = '1';
                    modal.style.transform = 'scale(1)';
                }, 10);
            });
            modal.addEventListener('hide.bs.modal', () => {
                modal.style.transition = `opacity ${transitionDuration}s ease, transform ${transitionDuration}s ease`;
                modal.style.opacity = '1';
                modal.style.transform = 'scale(1)';
                setTimeout(() => {
                    modal.style.opacity = '0';
                    modal.style.transform = 'scale(0.95)';
                }, 10);
            });
        });

        AOS.init();

        document.querySelector('form').addEventListener('submit', () => {
            showSpinner();
            setTimeout(hideSpinner, 2000);
        });

        document.querySelector('.toggle-button').addEventListener('click', () => {
            document.querySelector('.toggle-element').classList.toggle('active');
        });
    };

    updateActiveNavLink();
    handleEvents();

    document.body.classList.add('page-transition');
    document.body.classList.add('page-transition-loaded');

    const userArea = "{{ user.area }}";
    const badge = document.querySelector('.badge-outline-pill');
    if (userArea) {
        badge.classList.add(`area-${userArea}`);
    }
});
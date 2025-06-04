// static/js/pantalla_inicio.js
document.addEventListener('DOMContentLoaded', function() {
    const sidebar = document.getElementById('sidebar');
    const toggleSidebarBtn = document.getElementById('toggle-sidebar');
    const tabBar = document.getElementById('tab-bar');
    const tabContentArea = document.getElementById('tab-content-area');
    const welcomeMessage = document.getElementById('welcome-message');
    
    // Selectores para enlaces de pestañas y toggles de acordeón
    const sidebarLinks = sidebar.querySelectorAll('.nav-options a');

    let activeTabId = null;

    // Función para ocultar/mostrar la barra lateral
    if (toggleSidebarBtn && sidebar) {
        toggleSidebarBtn.addEventListener('click', () => {
            sidebar.classList.toggle('collapsed');
            // Si colapsamos, cerramos todos los submenús abiertos para evitar problemas de layout
            if (sidebar.classList.contains('collapsed')) {
                document.querySelectorAll('#sidebar .menu.nested.open').forEach(submenu => {
                    submenu.classList.remove('open');
                });
                document.querySelectorAll('#sidebar a.has-submenu.submenu-active').forEach(link => {
                    link.classList.remove('submenu-active');
                });
            }
        });
    }

    // Funciones de manejo de pestañas (activateTab, openTab) - SIN CAMBIOS, se mantienen como en tu versión anterior
    function activateTab(tabButton, contentPaneId) {
        document.querySelectorAll('#tab-bar .tab-button').forEach(btn => btn.classList.remove('active'));
        document.querySelectorAll('#tab-content-area .tab-pane').forEach(pane => pane.style.display = 'none');
        if (tabButton) {
            tabButton.classList.add('active');
        }
        const activeContentPane = document.getElementById(contentPaneId);
        if (activeContentPane) {
            activeContentPane.style.display = 'block';
            activeTabId = contentPaneId;
            if (welcomeMessage) welcomeMessage.style.display = 'none';
        } else if (welcomeMessage) {
            if (tabBar.children.length === 0) { // Solo muestra bienvenida si no hay otras pestañas
                 welcomeMessage.style.display = 'block';
            }
        }
    }

    function openTab(id, title, url) {
        const contentPaneId = `pane-${id}`;
        const tabButtonId = `tab-${id}`;
        const existingTabButton = document.getElementById(tabButtonId);
        if (existingTabButton) {
            activateTab(existingTabButton, contentPaneId);
            return;
        }
        const tabButton = document.createElement('button');
        tabButton.id = tabButtonId;
        tabButton.className = 'tab-button';
        tabButton.textContent = title;
        const closeButton = document.createElement('span');
        closeButton.className = 'close-tab';
        closeButton.innerHTML = '&times;';
        closeButton.title = 'Cerrar pestaña';
        tabButton.appendChild(closeButton);
        tabBar.appendChild(tabButton);
        const contentPane = document.createElement('div');
        contentPane.id = contentPaneId;
        contentPane.className = 'tab-pane';
        contentPane.style.display = 'none';
        const iframe = document.createElement('iframe');
        iframe.src = url;
        iframe.style.width = '100%';
        iframe.style.height = '100%';
        iframe.style.border = 'none';
        contentPane.appendChild(iframe);
        tabContentArea.appendChild(contentPane);
        tabButton.addEventListener('click', function(event) {
            if (event.target !== closeButton) {
                activateTab(tabButton, contentPaneId);
            }
        });
        closeButton.addEventListener('click', function(event) {
            event.stopPropagation();
            tabBar.removeChild(tabButton);
            tabContentArea.removeChild(contentPane);
            if (activeTabId === contentPaneId) {
                const lastTabButton = tabBar.querySelector('.tab-button:last-child');
                if (lastTabButton) {
                    // Simular clic para activar la última pestaña
                    const clickEvent = new MouseEvent('click', { bubbles: true, cancelable: true });
                    lastTabButton.dispatchEvent(clickEvent);
                } else {
                    activeTabId = null;
                    if (welcomeMessage) welcomeMessage.style.display = 'block';
                }
            }
        });
        activateTab(tabButton, contentPaneId);
    }

    // Event listeners para TODOS los enlaces en la barra lateral
    sidebarLinks.forEach(link => {
        link.addEventListener('click', function(event) {
            // Si la barra lateral está colapsada, no hacer NADA (ni acordeón ni pestaña)
            if (sidebar.classList.contains('collapsed')) {
                event.preventDefault();
                return;
            }

            const parentLi = this.closest('li.nav-item');
            const submenu = parentLi ? parentLi.querySelector('ul.menu.nested') : null;

            // Lógica del Acordeón
            if (this.classList.contains('has-submenu') && submenu) {
                event.preventDefault(); // Prevenir navegación si es un toggle de acordeón
                submenu.classList.toggle('open');
                this.classList.toggle('submenu-active'); // Para la flecha
            }

            // Lógica para Abrir Pestaña (solo si tiene data-url y no es solo un toggle de un acordeón que ya se previno)
            const url = this.dataset.url;
            const title = this.dataset.title;
            const id = this.dataset.id;

            if (url && url !== "#" && title && id) {
                // Si no es un toggle de acordeón (o si un toggle también puede abrir una pestaña),
                // y no se previno antes, se previene ahora.
                // Si fue un toggle de acordeón, event.preventDefault() ya se llamó.
                if (!this.classList.contains('has-submenu') || !submenu) { // Si no es un padre de submenu
                    event.preventDefault();
                } else if (this.classList.contains('has-submenu') && submenu && this.dataset.url && this.dataset.url !== '#') {
                    // Si es un padre de submenu Y tiene data-url, el preventDefault anterior ya aplicó.
                    // Se permite que también abra la pestaña.
                }
                openTab(id, title, url);
            }
        });
    });

    // Mensaje de bienvenida inicial
    if (tabBar.children.length === 0 && welcomeMessage) {
        welcomeMessage.style.display = 'block';
    } else if (welcomeMessage) {
        welcomeMessage.style.display = 'none';
    }
});
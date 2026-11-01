/** Responsive navigation and in-page smooth scrolling. */

const MOBILE_BREAKPOINT = 768;

export function initNav() {
    const toggle = document.querySelector('[data-nav-toggle]');
    const menu = document.querySelector('[data-nav-menu]');
    const navbar = document.querySelector('.navbar');

    const closeMenu = () => {
        if (!menu) return;
        menu.classList.remove('open');
        if (toggle) toggle.setAttribute('aria-expanded', 'false');
    };

    if (toggle && menu) {
        toggle.addEventListener('click', () => {
            const open = menu.classList.toggle('open');
            toggle.setAttribute('aria-expanded', String(open));
        });
    }

    if (menu) {
        menu.querySelectorAll('a').forEach((link) => link.addEventListener('click', closeMenu));
    }

    document.addEventListener('click', (event) => {
        if (menu && menu.classList.contains('open') && !event.target.closest('.navbar')) {
            closeMenu();
        }
    });

    window.addEventListener('resize', () => {
        if (window.innerWidth > MOBILE_BREAKPOINT) closeMenu();
    });

    // Smooth scroll for in-page anchors, offset by the fixed navbar height.
    document.querySelectorAll('a[href^="#"]').forEach((anchor) => {
        anchor.addEventListener('click', (event) => {
            const target = document.querySelector(anchor.getAttribute('href'));
            if (!target) return;
            event.preventDefault();
            const offset = (navbar ? navbar.offsetHeight : 60) + 20;
            const top = target.getBoundingClientRect().top + window.pageYOffset - offset;
            window.scrollTo({ top, behavior: 'smooth' });
        });
    });
}

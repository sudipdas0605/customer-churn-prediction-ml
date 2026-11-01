/** Entry point: boots each UI module once the DOM is ready. */

import { initNav } from './modules/nav.js';
import { initForms } from './modules/forms.js';
import { initResult } from './modules/result.js';

function boot() {
    initNav();
    initForms();
    initResult();
}

if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', boot);
} else {
    boot();
}

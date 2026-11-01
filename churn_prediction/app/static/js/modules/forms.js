/**
 * Prediction form behaviour, driven entirely by data attributes emitted by
 * the Jinja form macro:
 *
 *   data-derives="age"                       -> date of birth fills age
 *   data-auto-check-from="age"               -> radio group follows age
 *   data-locked-when="has_credit_card=0"     -> dependent field is locked
 */

import { uiStore } from './state.js';

function calculateAge(value) {
    if (!value) return null;
    const dob = new Date(value);
    if (Number.isNaN(dob.getTime())) return null;

    const today = new Date();
    let age = today.getFullYear() - dob.getFullYear();
    const monthDelta = today.getMonth() - dob.getMonth();
    if (monthDelta < 0 || (monthDelta === 0 && today.getDate() < dob.getDate())) {
        age -= 1;
    }
    return age >= 0 ? age : null;
}

function initDerivedAge() {
    document.querySelectorAll('[data-derives]').forEach((source) => {
        const target = document.getElementById(`field-${source.dataset.derives}`);
        const sync = () => {
            const age = calculateAge(source.value);
            if (age === null) return;
            if (target) target.value = age;
            uiStore.setState({ age });
        };
        source.addEventListener('change', sync);

        if (target) {
            target.addEventListener('input', () => {
                const typed = Number(target.value);
                uiStore.setState({ age: Number.isFinite(typed) && target.value ? typed : null });
            });
        }
    });
}

function initAutoCheck() {
    const groups = [...document.querySelectorAll('[data-auto-check-from]')];

    uiStore.subscribe((state) => {
        if (state.age === null) return;
        groups.forEach((group) => {
            const threshold = Number(group.dataset.autoCheckThreshold || 0);
            const value = state.age > threshold ? 'Yes' : 'No';
            const radio = group.querySelector(`input[value="${value}"]`);
            if (radio) radio.checked = true;
        });
    });
}

function initLockedFields() {
    const selects = [...document.querySelectorAll('[data-locked-when]')];

    selects.forEach((select) => {
        const [sourceName, lockedValue] = select.dataset.lockedWhen.split('=');
        const update = () => {
            const checked = document.querySelector(`input[name="${sourceName}"]:checked`);
            const locked = Boolean(checked && checked.value === lockedValue);
            uiStore.setState((state) => ({ locks: { ...state.locks, [select.name]: locked } }));
        };

        document
            .querySelectorAll(`input[name="${sourceName}"]`)
            .forEach((radio) => radio.addEventListener('change', update));
        update();
    });

    uiStore.subscribe((state) => {
        selects.forEach((select) => {
            const locked = Boolean(state.locks[select.name]);
            if (locked) select.value = select.dataset.lockedValue;
            select.classList.toggle('is-locked', locked);
            select.setAttribute('aria-disabled', String(locked));
            select.tabIndex = locked ? -1 : 0;
        });
    });
}

function initSubmitState() {
    document.querySelectorAll('form[data-predict-form]').forEach((form) => {
        form.addEventListener('submit', () => {
            const button = form.querySelector('.submit-btn');
            if (!button) return;
            button.dataset.label = button.textContent;
            button.textContent = 'Predicting...';
            button.disabled = true;
        });
    });
}

export function initForms() {
    initDerivedAge();
    initAutoCheck();
    initLockedFields();
    initSubmitState();
}

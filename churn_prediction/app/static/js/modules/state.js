/**
 * Minimal observable store.
 *
 * Vanilla JS has no built-in state container, so UI modules share one tiny
 * pub/sub store instead of poking each other's DOM directly.
 */

export function createStore(initialState = {}) {
    let state = { ...initialState };
    const listeners = new Set();

    return {
        getState() {
            return state;
        },

        setState(patch) {
            const next = typeof patch === 'function' ? patch(state) : patch;
            state = { ...state, ...next };
            listeners.forEach((listener) => listener(state));
        },

        subscribe(listener) {
            listeners.add(listener);
            listener(state);
            return () => listeners.delete(listener);
        },
    };
}

/** Shared UI state: derived age and per-field lock flags. */
export const uiStore = createStore({ age: null, locks: {} });

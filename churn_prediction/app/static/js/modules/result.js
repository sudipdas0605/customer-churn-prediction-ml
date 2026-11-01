/** Animate the probability bar on the result page. */

export function initResult() {
    const fill = document.querySelector('.probability-fill[data-probability]');
    if (!fill) return;

    const target = `${fill.dataset.probability}%`;
    fill.style.width = '0%';

    requestAnimationFrame(() => {
        requestAnimationFrame(() => {
            fill.style.width = target;
        });
    });
}

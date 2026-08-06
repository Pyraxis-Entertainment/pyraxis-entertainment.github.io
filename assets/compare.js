/* Before/after comparison slider.
 *
 * First-party, no library, no CDN, no build step — the same terms as the
 * rest of the site. This is the only JavaScript on it; keep it that way
 * unless there is as good a reason as this one.
 *
 * The markup works without this file. Each [data-compare] block renders as
 * two labelled panes under a single caption, which reads fine on its own.
 * All this does is upgrade that into a comparison the reader operates:
 * it injects a range input and a divider, then sets --compare-pos.
 *
 * A real <input type="range"> is used rather than pointer handlers so that
 * arrow-key control and screen-reader semantics come for free.
 */
(function () {
    'use strict';

    var blocks = document.querySelectorAll('[data-compare]');

    Array.prototype.forEach.call(blocks, function (block) {
        var stack = block.querySelector('.compare-stack');
        var after = block.querySelector('[data-compare-pane="after"]');
        if (!stack || !after) {
            return;   // markup is not what we expect; leave it stacked
        }

        // Only upgrade once both panes actually hold an image. While a shot is
        // still awaiting capture the panes hold empty frames, and a divider
        // dragged across two identical empty frames says nothing — worse, the
        // two frames' labels would sit on top of each other. Left alone they
        // render side by side, labelled, which is the honest picture. The
        // slider then turns itself on the moment the files land.
        if (!block.querySelector('[data-compare-pane="before"] img') ||
            !block.querySelector('[data-compare-pane="after"] img')) {
            return;
        }

        var range = document.createElement('input');
        range.type = 'range';
        range.min = '0';
        range.max = '100';
        range.step = '1';
        range.value = '50';
        range.className = 'compare-range';
        range.setAttribute('aria-label', block.getAttribute('data-compare-label') ||
            'Drag to compare the before and after images');

        var divider = document.createElement('span');
        divider.className = 'compare-divider';
        divider.setAttribute('aria-hidden', 'true');

        function apply() {
            block.style.setProperty('--compare-pos', range.value + '%');
        }

        range.addEventListener('input', apply);

        stack.appendChild(range);
        stack.appendChild(divider);
        apply();
        block.classList.add('compare--ready');
    });
}());

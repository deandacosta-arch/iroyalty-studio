// Minimal one-at-a-time player for the individual sound buttons.
(function () {
  var current = null, currentBtn = null;
  document.querySelectorAll('.sound button[data-src]').forEach(function (btn) {
    btn.addEventListener('click', function () {
      if (currentBtn === btn && current && !current.paused) { current.pause(); reset(); return; }
      if (current) { current.pause(); reset(); }
      document.querySelectorAll('audio').forEach(function (a) { a.pause(); });
      current = new Audio(btn.dataset.src); currentBtn = btn;
      btn.setAttribute('aria-pressed', 'true'); btn.textContent = '\u25A0';
      current.addEventListener('ended', reset);
      current.play();
    });
  });
  function reset() { if (currentBtn) { currentBtn.setAttribute('aria-pressed', 'false'); currentBtn.textContent = '\u25B6'; } current = null; currentBtn = null; }
})();

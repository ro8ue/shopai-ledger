/* Local controls keep every stored price in the document. */
(() => {
  const legacy = { '#support': 'shopify-ai-support-apps.html', '#search': 'shopify-ai-search-apps.html' };
  if ((location.pathname === '/' || location.pathname.endsWith('/index.html')) && legacy[location.hash]) {
    location.replace(legacy[location.hash]);
    return;
  }
  document.querySelectorAll('.size-compare').forEach((comparison) => {
    comparison.querySelectorAll('[data-size-select]').forEach((button) => {
      button.addEventListener('click', () => {
        comparison.dataset.selectedSize = button.dataset.sizeSelect;
        comparison.querySelectorAll('[data-size-select]').forEach((option) => {
          option.setAttribute('aria-pressed', String(option === button));
        });
      });
    });
  });
})();

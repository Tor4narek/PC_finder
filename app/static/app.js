(function () {
  if (window.Telegram && window.Telegram.WebApp) {
    try {
      window.Telegram.WebApp.ready();
      window.Telegram.WebApp.expand();
    } catch (_) {
      // Keep browser mode working too.
    }
  }

  const classifyBtn = document.getElementById('classifyBtn');
  if (!classifyBtn) return;

  classifyBtn.addEventListener('click', async () => {
    const queryEl = document.getElementById('query');
    const resultEl = document.getElementById('classifyResult');
    const query = (queryEl?.value || '').trim();
    if (!query) {
      resultEl.textContent = 'Please describe your task first.';
      return;
    }

    classifyBtn.disabled = true;
    resultEl.textContent = 'Detecting category...';

    try {
      const response = await fetch('/api/classify', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query }),
      });
      if (!response.ok) throw new Error('Request failed');
      const data = await response.json();
      resultEl.textContent = `Detected: ${data.category}`;
      window.location.href = `/catalog?category=${encodeURIComponent(data.category)}`;
    } catch (error) {
      resultEl.textContent = 'Classification failed. Please try again.';
    } finally {
      classifyBtn.disabled = false;
    }
  });
})();

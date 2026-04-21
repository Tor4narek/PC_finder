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
      resultEl.textContent = 'Сначала опишите вашу задачу.';
      return;
    }

    classifyBtn.disabled = true;
    resultEl.textContent = 'Определяем категорию...';

    try {
      const response = await fetch('/api/classify', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query }),
      });
      if (!response.ok) throw new Error('Ошибка запроса');
      const data = await response.json();
      resultEl.textContent = `Определено: ${data.category}`;
      window.location.href = `/catalog?category=${encodeURIComponent(data.category)}`;
    } catch (error) {
      resultEl.textContent = 'Не удалось определить категорию. Попробуйте ещё раз.';
    } finally {
      classifyBtn.disabled = false;
    }
  });
})();

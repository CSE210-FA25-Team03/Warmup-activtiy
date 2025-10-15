const API_BASE = "http://127.0.0.1:8000"

    const input = document.getElementById('input');
    const output = document.getElementById('output');
    const btn = document.getElementById('convertBtn');
    const clear = document.getElementById('clearBtn');
    const statusEl = document.getElementById('status');

    function setStatus(text, show=true) {
      statusEl.textContent = text;
      statusEl.hidden = !show;
    }

    clear.addEventListener('click', () => {
      input.value = '';
      output.value = '';
      setStatus('cleared');
      setTimeout(() => setStatus('', false), 700);
    });

    btn.addEventListener('click', async () => {
      const text = input.value.trim();
      if (!text) { output.value = ''; return; }
      setStatus('converting…');
      btn.disabled = true;

      try {
        const res = await fetch(`${API_BASE}/api/convert`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ text: text, mode: "auto" })
        });
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        const data = await res.json();

        output.value = data.output || '';
        setStatus(`${data.source} • ${data.reason}`);
      } catch (err) {
        output.value = '';
        setStatus('error');
        alert('Conversion failed. Check backend is running.\n\n' + err);
      } finally {
        btn.disabled = false;
        setTimeout(() => setStatus('', false), 2000);
      }
    });

input.addEventListener('keydown', (event) => {
  if (event.key === 'Enter' && !event.shiftKey) {
    event.preventDefault();
    translateText();
    btn.classList.add('active');
    setTimeout(() => btn.classList.remove('active'), 150);
  }
});

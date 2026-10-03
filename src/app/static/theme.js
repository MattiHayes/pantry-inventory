(() => {
  const defaults = { accent: '#52705d', background: '#f5f4ef', card: '#ffffff' };
  const variables = { accent: '--accent', background: '--page-bg', card: '--card' };
  const panel = document.getElementById('appearance-panel');
  const toggle = document.getElementById('appearance-toggle');
  const close = document.getElementById('appearance-close');

  if (!panel || !toggle) return;

  function applyTheme(theme) {
    for (const [key, variable] of Object.entries(variables)) {
      const value = theme[key] || defaults[key];
      document.documentElement.style.setProperty(variable, value);
      const input = document.querySelector(`[data-theme-color="${key}"]`);
      if (input) input.value = value;
    }
    const accent = theme.accent || defaults.accent;
    document.documentElement.style.setProperty('--accent-dark', shade(accent, -24));
    document.documentElement.style.setProperty('--accent-soft', tint(accent, '#ffffff', 0.86));
  }

  function shade(hex, amount) {
    const channels = hex.match(/[0-9a-f]{2}/gi)?.map(part => parseInt(part, 16)) || [82, 112, 93];
    return `#${channels.map(channel => Math.max(0, Math.min(255, channel + amount)).toString(16).padStart(2, '0')).join('')}`;
  }

  function tint(hex, other, ratio) {
    const a = hex.match(/[0-9a-f]{2}/gi)?.map(part => parseInt(part, 16)) || [82, 112, 93];
    const b = other.match(/[0-9a-f]{2}/gi)?.map(part => parseInt(part, 16)) || [255, 255, 255];
    return `#${a.map((channel, i) => Math.round(channel * (1 - ratio) + b[i] * ratio).toString(16).padStart(2, '0')).join('')}`;
  }

  let saved = {};
  try { saved = JSON.parse(localStorage.getItem('pantry-theme') || '{}'); } catch { saved = {}; }
  applyTheme(saved);

  document.querySelectorAll('[data-theme-color]').forEach(input => {
    input.addEventListener('input', () => {
      saved[input.dataset.themeColor] = input.value;
      applyTheme(saved);
      localStorage.setItem('pantry-theme', JSON.stringify(saved));
    });
  });

  toggle.addEventListener('click', () => {
    panel.hidden = !panel.hidden;
    toggle.setAttribute('aria-expanded', String(!panel.hidden));
  });
  close.addEventListener('click', () => {
    panel.hidden = true;
    toggle.setAttribute('aria-expanded', 'false');
    toggle.focus();
  });
  document.getElementById('theme-reset').addEventListener('click', () => {
    saved = {};
    localStorage.removeItem('pantry-theme');
    applyTheme(saved);
  });
  document.addEventListener('keydown', event => {
    if (event.key === 'Escape' && !panel.hidden) {
      panel.hidden = true;
      toggle.setAttribute('aria-expanded', 'false');
      toggle.focus();
    }
  });
})();

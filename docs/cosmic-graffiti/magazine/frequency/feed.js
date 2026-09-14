(async function () {
  const rail = document.getElementById('freq-rail');
  const stream = document.getElementById('freq-stream');
  if (!rail && !stream) return;
  const script = document.currentScript;
  const feedUrl = new URL('feed.json', script.src);
  const magRoot = new URL('../', feedUrl);
  let data;
  try {
    const res = await fetch(feedUrl.href, { cache: 'no-store' });
    if (!res.ok) throw new Error('feed ' + res.status);
    data = await res.json();
  } catch (e) {
    return;
  }
  const items = (data.items || []).slice().sort((a, b) => (b.date || '').localeCompare(a.date || ''));
  function hrefFor(it) {
    const h = String(it.href || 'frequency/').replace(/^\//, '');
    return new URL(h, magRoot).href;
  }
  const lane = new URL('frequency/', magRoot).href;
  if (rail) {
    rail.innerHTML = items.slice(0, 4).map(it => `
      <a class="freq-chip" href="${hrefFor(it)}">
        <span class="freq-chip-kicker">${it.kicker || 'the Frequency'}</span>
        <span class="freq-chip-title">${it.title || ''}</span>
      </a>`).join('') +
      `<a class="freq-more" href="${lane}">Open the Frequency →</a>`;
  }
  if (stream) {
    stream.innerHTML = items.map(it => `
      <article class="freq-item">
        <p class="kicker">${it.kicker || 'the Frequency'} · ${it.date || ''}</p>
        <h3><a href="${hrefFor(it)}">${it.title || 'Untitled'}</a></h3>
        <p class="freq-body">${it.body || ''}</p>
        <p class="freq-credit">${it.credit || 'Val8000 · AI commentator'}</p>
      </article>`).join('');
  }
})();

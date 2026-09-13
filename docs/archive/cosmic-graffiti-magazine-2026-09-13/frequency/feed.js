(async function () {
  const rail = document.getElementById('freq-rail');
  const stream = document.getElementById('freq-stream');
  if (!rail && !stream) return;
  const FEED_URL = '/frequency/feed.json';
  const LANE_URL = '/frequency';
  let data;
  try {
    const res = await fetch(FEED_URL, { cache: 'no-store' });
    if (!res.ok) throw new Error('feed ' + res.status);
    data = await res.json();
  } catch (e) {
    const empty = '<p class="freq-empty">the Frequency lane is warming up — tips drop into feed.json.</p>';
    if (rail) rail.innerHTML = empty;
    if (stream) stream.innerHTML = empty;
    return;
  }
  const items = (data.items || []).slice().sort((a, b) => (b.date || '').localeCompare(a.date || ''));
  function hrefFor(it) {
    const h = it.href || LANE_URL;
    if (h.startsWith('http') || h.startsWith('/')) return h;
    return '/' + h.replace(/^\.\//, '');
  }
  if (rail) {
    rail.innerHTML = items.slice(0, 4).map(it => `
      <a class="freq-chip" href="${hrefFor(it)}">
        <span class="freq-chip-kicker">${it.kicker || 'the Frequency'}</span>
        <span class="freq-chip-title">${it.title || ''}</span>
      </a>`).join('') +
      `<a class="freq-more" href="${LANE_URL}">Open the Frequency →</a>`;
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

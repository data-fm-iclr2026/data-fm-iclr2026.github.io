(function () {
  const container = document.getElementById('accepted-papers-list');
  if (!container) return;

  const papers = window.PAPERS;
  if (!Array.isArray(papers)) {
    container.innerHTML =
      '<p style="color:#c62828;">Unable to load accepted papers list. Please view on ' +
      '<a href="https://openreview.net/group?id=ICLR.cc/2026/Workshop/DATA-FM" target="_blank" rel="noopener">OpenReview</a>.</p>';
    return;
  }

  const esc = (s) =>
    String(s).replace(/[&<>"']/g, (c) => ({
      '&': '&amp;',
      '<': '&lt;',
      '>': '&gt;',
      '"': '&quot;',
      "'": '&#39;',
    }[c]));

  const items = papers
    .map((p) => {
      const oralTag =
        p.decision === 'Accept (Oral)'
          ? ' <span style="background:#ffe9a8;color:#8a6d00;padding:1px 6px;border-radius:3px;font-size:0.8em;font-weight:600;">Oral</span>'
          : '';
      const authors = Array.isArray(p.authors) ? p.authors.join(', ') : '';
      return (
        '<li style="margin-bottom:10px;">' +
        '<a href="' +
        esc(p.forum_url) +
        '" target="_blank" rel="noopener">' +
        esc(p.title) +
        '</a>' +
        oralTag +
        '<br><i>' +
        esc(authors) +
        '</i>' +
        '</li>'
      );
    })
    .join('');

  container.innerHTML =
    '<details>' +
    '<summary style="cursor:pointer;color:#007bff;font-weight:600;font-size:1.05em;">' +
    'Show all ' +
    papers.length +
    ' accepted papers' +
    '</summary>' +
    '<ol style="margin-top:15px;">' +
    items +
    '</ol>' +
    '</details>';
})();

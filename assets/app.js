/* Skills Library — zero-dependency website.
   Data comes from data/catalog.js (window.__SKILLS_LIBRARY__). */

(() => {
  'use strict';

  const CAT = window.__SKILLS_LIBRARY__;
  const $ = (sel) => document.querySelector(sel);
  const $$ = (sel) => Array.from(document.querySelectorAll(sel));

  const I18N = {
    pl: {
      brandTag: 'otwarty indeks skilli dla agentów AI',
      github: 'GitHub ↗', json: 'JSON API ↗', toggleTheme: 'Przełącz motyw', switchLang: 'Zmień język',
      pageTitle: 'Skills Library — katalog najlepszych skilli dla agentów AI',
      metaDescription: 'Zweryfikowany katalog open-source skilli SKILL.md z GitHuba: wyszukiwanie, licencje, pakiety startowe i komendy instalacji.',
      heroBadge: 'Generowane z GitHub API', heroTitle1: 'Najlepsze skille', heroTitleAccent: 'dla agentów AI', heroTitle2: 'w jednym, zweryfikowanym miejscu.',
      heroSubtitle: 'Przeszukujemy GitHub, sprawdzamy prawdziwe pliki SKILL.md, licencje i świeżość repozytoriów — a potem dajemy Ci gotową komendę instalacji do Claude Code, Codex, Cursor, Gemini CLI i innych agentów.',
      ctaBrowse: 'Przeglądaj skille →', ctaInstall: 'Jak instalować',
      trust1: 'Tylko metadane, linki do źródeł', trust2: 'Zero telemetrii, zero zależności', trust3: 'Licencje i ryzyka widoczne',
      statRepos: 'repozytoriów', statFiles: 'plików SKILL.md', statCollections: 'kolekcji', statSkills: 'zaindeksowanych skilli',
      statsFoot: 'Dane odświeżane co tydzień przez GitHub Actions',
      searchPlaceholder: 'Szukaj: pdf, react, security audit, TDD…', searchHint: 'Szukamy po nazwie, opisie, repozytorium i tagach. Wpisz np. „code review" albo „pdf".', clearSearch: 'Wyczyść wyszukiwanie',
      viewSkills: 'Skille', viewCollections: 'Kolekcje', viewPacks: 'Pakiety startowe', viewGuide: 'Jak używać',
      sortLabel: 'Sortuj', sortRelevance: 'Trafność', sortStars: 'Gwiazdki', sortFresh: 'Aktualność', sortSkills: 'Liczba skilli', sortName: 'Nazwa A–Z',
      toggleOfficial: 'Tylko oficjalne', toggleClear: 'Jasna licencja', toggleCurated: 'Tylko kuratowane', toggleHideReview: 'Ukryj wymagające przeglądu', toggleSaved: 'Zapisane',
      reset: 'Wyczyść filtry', noResults: 'Nic nie znaleziono', noResultsHint: 'Spróbuj innego zapytania, wyłącz filtry albo przejrzyj kolekcje.',
      guideKicker: 'PRZEWODNIK', guideTitle: 'Od katalogu do działającego agenta w 3 krokach',
      guideIntro: 'Skill to folder z plikiem SKILL.md. Ten sam format czytają Claude Code, Codex, Cursor, Gemini CLI, GitHub Copilot i dziesiątki innych agentów. Różnią się tylko foldery, w których go szukają.',
      step1Title: 'Wybierz i sprawdź źródło', step1Body: 'Otwórz kartę skilla, kliknij „Źródło" i przeczytaj cały SKILL.md. Zwróć uwagę na dołączone skrypty, allowed-tools i licencję upstream. Nasze znaczniki to wskazówki, nie certyfikat bezpieczeństwa.', readSecurity: 'Model zaufania →',
      step2Title: 'Zainstaluj jedną komendą', step2Body: 'Najpewniejsza forma wskazuje bezpośrednio na folder skilla — działa też w repozytoriach z zagnieżdżonymi pluginami. Wymaga Node.js 22.20+.',
      step3Title: 'Bez Node.js: ręcznie', step3Body: 'Sklonuj repozytorium i skopiuj folder skilla do katalogu agenta. Nazwa folderu musi zgadzać się z polem name w frontmatterze. Potem uruchom nową sesję agenta.',
      compatTitle: 'Gdzie agent szuka skilli', compatBody: 'CLI wykrywa zainstalowane agenty. Jeśli pracujesz w zespole na różnych narzędziach, wybierz wspólny katalog .agents/skills/.',
      colAgent: 'Agent', colProject: 'Projekt', colGlobal: 'Globalnie', fullMatrix: 'Pełna macierz 75+ agentów →',
      apiTitle: 'Dane dla Twojego agenta', apiBody: 'Katalog jest zwykłym plikiem JSON. Możesz go wczytać w skrypcie, w AGENTS.md albo zainstalować nasz skill-finder, żeby agent sam proponował skille.', apiDocs: 'Dokumentacja API ↗',
      methodTitle: 'Skąd te dane?', methodBody: 'GitHub Search API → metadane repozytoriów → rekursywne drzewa git → prawdziwy frontmatter SKILL.md. Gwiazdki, licencje i daty nie są wpisywane ręcznie.', methodLink: 'Metodyka →',
      footerText: 'Otwarty katalog metadanych. Skille pozostają własnością swoich autorów i na swoich licencjach.', contribute: 'Dodaj źródło', security: 'Bezpieczeństwo', noTelemetry: 'bez telemetrii',
      noscript: 'Ta strona potrzebuje JavaScriptu do wyszukiwania. Pełna lista jest dostępna w CATALOG.md i data/catalog.json.',
      all: 'Wszystkie', resultsSkills: '{n} skilli', resultsCollections: '{n} kolekcji', resultsPacks: '{n} pakietów', sortedBy: '· {mode}',
      official: 'Oficjalne', editorsPick: 'Wybór redakcji', essential: 'Fundament', curated: 'Kuratowane', discovered: 'Odkryte automatycznie', reviewed: 'Sprawdzone', spec: 'Zgodny ze spec', needsReview: 'Przejrzyj źródło',
      licenseCheck: 'Licencja do sprawdzenia', licenseUnknown: 'Brak licencji', licensePerSkill: 'Licencje per-skill', licenseHint: 'Licencja rozpoznana przez GitHub API',
      securityUse: 'Tylko autoryzowane testy', chineseUse: 'Opis po chińsku', safeUse: 'Bezpieczne użycie',
      active: 'Aktywne', maintained: 'Utrzymywane', stale: 'Nieaktualne', unknown: 'Nieznane',
      stars: '★ {n}', skillsCount: '{n} skilli', filesCount: '{n} plików', updated: 'Aktualizacja', today: 'dzisiaj', yesterday: 'wczoraj', daysAgo: '{n} dni temu',
      repo: 'Repozytorium', path: 'Ścieżka', license: 'Licencja', category: 'Kategoria', tier: 'Warstwa', source: 'Źródło SKILL.md', details: 'Szczegóły', save: 'Zapisz', saved: 'Zapisane', close: 'Zamknij',
      copy: 'Kopiuj', copied: 'Skopiowano!', copyFailed: 'Nie udało się skopiować', share: 'Kopiuj link', shareDone: 'Link skopiowany',
      commands: 'Komendy instalacji', directCmd: 'Bezpośrednio (polecane)', shorthandCmd: 'Skrót repo + --skill', globalCmd: 'Globalnie', useCmd: 'Bez instalacji', manualCmd: 'Ręcznie', collectionCmd: 'Cała kolekcja',
      related: 'Inne skille z tego repo', indexedSkills: 'Zaindeksowane skille', noRelated: 'Brak innych zaindeksowanych skilli.',
      reviewNotice: 'Ten skill zawiera skrypty, deklaruje allowed-tools lub wspomina komendy shell/sieć. Przeczytaj źródło przed instalacją.',
      licenseNotice: 'Licencja tego repozytorium jest niejasna lub wymaga sprawdzenia. Zweryfikuj ją u źródła przed użyciem.',
      discoveredNotice: 'To repozytorium znaleziono automatycznie i nie zostało ręcznie sprawdzone.',
      packFilter: 'Pakiet: {name}', clear: 'Wyczyść', showPackSkills: 'Pokaż skille', copyBundle: 'Kopiuj zestaw', packSkills: '{n} skilli',
      openCollection: 'Otwórz repozytorium', viewSource: 'Źródło SKILL.md', tools: 'Narzędzia', scripts: 'Skrypty', size: 'Rozmiar',
      skillCountLabel: 'Unikalne skille', fileCountLabel: 'Ścieżki SKILL.md', directory: 'Katalog / lista',
      showing: 'wyświetlano {shown} z {total}', loadMore: 'Pokaż więcej ↓',
      resultsHidden: 'Ukryto {n} wyników przez filtry', dataMissing: 'Brak danych katalogu', dataMissingBody: 'Wygeneruj data/catalog.js poleceniem: python3 scripts/build_catalog.py',
    },
    en: {
      brandTag: 'open-source index for AI agents',
      github: 'GitHub ↗', json: 'JSON API ↗', toggleTheme: 'Toggle theme', switchLang: 'Switch language',
      pageTitle: 'Skills Library — the best open-source skills for AI agents',
      metaDescription: 'A verified catalog of open-source SKILL.md agent skills on GitHub: search, licenses, starter packs and install commands.',
      heroBadge: 'Generated from the GitHub API', heroTitle1: 'The best skills', heroTitleAccent: 'for AI agents', heroTitle2: 'in one verified place.',
      heroSubtitle: 'We search GitHub, verify real SKILL.md files, licenses and repository freshness — then hand you a ready install command for Claude Code, Codex, Cursor, Gemini CLI and other agents.',
      ctaBrowse: 'Browse skills →', ctaInstall: 'How to install',
      trust1: 'Metadata only, links to sources', trust2: 'No telemetry, no dependencies', trust3: 'Licenses and risks visible',
      statRepos: 'repositories', statFiles: 'SKILL.md files', statCollections: 'collections', statSkills: 'indexed skills',
      statsFoot: 'Data refreshed weekly by GitHub Actions',
      searchPlaceholder: 'Search: pdf, react, security audit, TDD…', searchHint: 'Searches names, descriptions, repositories and tags. Try “code review” or “pdf”.', clearSearch: 'Clear search',
      viewSkills: 'Skills', viewCollections: 'Collections', viewPacks: 'Starter packs', viewGuide: 'How to use',
      sortLabel: 'Sort', sortRelevance: 'Relevance', sortStars: 'Stars', sortFresh: 'Freshness', sortSkills: 'Skill count', sortName: 'Name A–Z',
      toggleOfficial: 'Official only', toggleClear: 'Clear license', toggleCurated: 'Curated only', toggleHideReview: 'Hide review-flagged', toggleSaved: 'Saved',
      reset: 'Reset filters', noResults: 'Nothing found', noResultsHint: 'Try another query, disable filters or browse the collections.',
      guideKicker: 'GUIDE', guideTitle: 'From catalog to a working agent in 3 steps',
      guideIntro: 'A skill is a folder containing SKILL.md. Claude Code, Codex, Cursor, Gemini CLI, GitHub Copilot and dozens of other agents read the same format — only the directories differ.',
      step1Title: 'Pick and inspect the source', step1Body: 'Open a skill card, click “Source” and read the whole SKILL.md. Watch for bundled scripts, allowed-tools and the upstream license. Our badges are hints, not a security certificate.', readSecurity: 'Trust model →',
      step2Title: 'Install with one command', step2Body: 'The most robust form points directly at the skill folder — it also works in repos with nested plugin layouts. Requires Node.js 22.20+.',
      step3Title: 'No Node.js: do it manually', step3Body: 'Clone the repository and copy the skill folder into your agent directory. The folder name must match the frontmatter name field. Then start a new agent session.',
      compatTitle: 'Where agents look for skills', compatBody: 'The CLI detects installed agents. If your team uses different tools, pick the shared .agents/skills/ directory.',
      colAgent: 'Agent', colProject: 'Project', colGlobal: 'Global', fullMatrix: 'Full matrix of 75+ agents →',
      apiTitle: 'Data for your own agent', apiBody: 'The catalog is a plain JSON file. Load it in a script or AGENTS.md, or install our skill-finder so your agent suggests skills on its own.', apiDocs: 'API docs ↗',
      methodTitle: 'Where do the numbers come from?', methodBody: 'GitHub Search API → repository metadata → recursive git trees → real SKILL.md frontmatter. Stars, licenses and dates are never typed by hand.', methodLink: 'Methodology →',
      footerText: 'An open metadata catalog. Skills remain the property of their authors under their own licenses.', contribute: 'Add a source', security: 'Security', noTelemetry: 'no telemetry',
      noscript: 'This page needs JavaScript for search. The full list is available in CATALOG.md and data/catalog.json.',
      all: 'All', resultsSkills: '{n} skills', resultsCollections: '{n} collections', resultsPacks: '{n} packs', sortedBy: '· {mode}',
      official: 'Official', editorsPick: "Editor's pick", essential: 'Essential', curated: 'Curated', discovered: 'Auto-discovered', reviewed: 'Reviewed', spec: 'Spec-compliant', needsReview: 'Review source',
      licenseCheck: 'Check license', licenseUnknown: 'No license', licensePerSkill: 'Per-skill licenses', licenseHint: 'License recognized by the GitHub API',
      securityUse: 'Authorized testing only', chineseUse: 'Chinese description', safeUse: 'Safe use',
      active: 'Active', maintained: 'Maintained', stale: 'Stale', unknown: 'Unknown',
      stars: '★ {n}', skillsCount: '{n} skills', filesCount: '{n} files', updated: 'Last push', today: 'today', yesterday: 'yesterday', daysAgo: '{n} days ago',
      repo: 'Repository', path: 'Path', license: 'License', category: 'Category', tier: 'Tier', source: 'SKILL.md source', details: 'Details', save: 'Save', saved: 'Saved', close: 'Close',
      copy: 'Copy', copied: 'Copied!', copyFailed: 'Copy failed', share: 'Copy link', shareDone: 'Link copied',
      commands: 'Install commands', directCmd: 'Direct (recommended)', shorthandCmd: 'Repo + --skill shorthand', globalCmd: 'Global', useCmd: 'Use without installing', manualCmd: 'Manual', collectionCmd: 'Whole collection',
      related: 'More skills from this repo', indexedSkills: 'Indexed skills', noRelated: 'No other indexed skills.',
      reviewNotice: 'This skill ships scripts, declares allowed-tools or mentions shell/network commands. Read the source before installing.',
      licenseNotice: 'This repository has an unclear or unverified license. Check it at the source before use.',
      discoveredNotice: 'This repository was found automatically and has not been manually reviewed.',
      packFilter: 'Pack: {name}', clear: 'Clear', showPackSkills: 'Show skills', copyBundle: 'Copy bundle', packSkills: '{n} skills',
      openCollection: 'Open repository', viewSource: 'SKILL.md source', tools: 'Tools', scripts: 'Scripts', size: 'Size',
      skillCountLabel: 'Unique skills', fileCountLabel: 'SKILL.md paths', directory: 'Directory / list',
      showing: 'showing {shown} of {total}', loadMore: 'Load more ↓',
      resultsHidden: '{n} results hidden by filters', dataMissing: 'Catalog data missing', dataMissingBody: 'Generate data/catalog.js with: python3 scripts/build_catalog.py',
    },
  };

  const defaults = {
    official: false, clearLicense: false, curatedOnly: true, hideReview: false, savedOnly: false,
  };

  const state = {
    lang: localStorage.getItem('sl-lang') || 'pl',
    theme: localStorage.getItem('sl-theme') || 'dark',
    view: 'skills', q: '', category: 'all', sort: 'relevance',
    ...defaults,
    packFilter: null, packFilterLabel: null,
    saved: new Set(JSON.parse(localStorage.getItem('sl-saved') || '[]')),
    open: null,
    visible: 60, _loadingMore: false,
  };
  if (!['pl', 'en'].includes(state.lang)) state.lang = 'pl';
  if (!['dark', 'light'].includes(state.theme)) state.theme = 'dark';

  let pendingDrawer = null;
  let lastFocused = null;

  const skillById = new Map();
  const collectionById = new Map();
  if (CAT) {
    CAT.skills.forEach((s) => skillById.set(s.id, s));
    CAT.collections.forEach((c) => collectionById.set(c.id, c));
  }

  function t(key, vars) {
    let text = (I18N[state.lang] && I18N[state.lang][key]) || I18N.en[key] || key;
    if (vars) Object.entries(vars).forEach(([k, v]) => { text = text.replaceAll('{' + k + '}', String(v)); });
    return text;
  }

  function esc(value) {
    return String(value ?? '').replace(/[&<>"']/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
  }

  function fmt(n) {
    return new Intl.NumberFormat(state.lang === 'pl' ? 'pl-PL' : 'en-US').format(n || 0);
  }

  function compact(n) {
    return new Intl.NumberFormat(state.lang === 'pl' ? 'pl-PL' : 'en-US', { notation: 'compact', maximumFractionDigits: 1 }).format(n || 0);
  }

  function fmtDate(iso) {
    if (!iso) return '—';
    try {
      return new Intl.DateTimeFormat(state.lang === 'pl' ? 'pl-PL' : 'en-US', { year: 'numeric', month: 'short', day: 'numeric' }).format(new Date(iso));
    } catch { return String(iso).slice(0, 10); }
  }

  function timeAgo(days) {
    if (days == null) return t('unknown');
    if (days <= 0) return t('today');
    if (days === 1) return t('yesterday');
    return t('daysAgo', { n: days });
  }

  function catLabel(id) {
    const c = CAT && CAT.categories.find((x) => x.id === id);
    return c ? (c[state.lang] || c.en) : id;
  }

  function badge(text, cls, title) {
    return `<span class="badge ${cls || 'badge-muted'}"${title ? ` title="${esc(title)}"` : ''}>${esc(text)}</span>`;
  }

  function licenseBadge(lic) {
    if (!lic) return '';
    if (lic.status === 'clear') return badge(lic.label || 'MIT', 'badge-clear', t('licenseHint'));
    if (lic.status === 'per-skill') return badge(t('licensePerSkill'), 'badge-muted', lic.label);
    if (lic.status === 'check') return badge(t('licenseCheck'), 'badge-warn', lic.label);
    return badge(t('licenseUnknown'), 'badge-danger', lic.label || t('licenseNotice'));
  }

  function safeUseBadge(n) {
    const icon = n.code === 'security' ? '⚠ ' : '文 ';
    const label = t(n.code === 'security' ? 'securityUse' : 'chineseUse');
    return badge(icon + label, 'badge-warn', n[state.lang] || n.en);
  }

  function tierLabel(item) {
    if (!item.reviewed) return t('discovered');
    if (item.tier === 'essential') return t('essential');
    return t('curated');
  }

  function freshnessLabel(item) {
    return t(item.freshness || 'unknown');
  }

  function skillBadges(s) {
    const out = [];
    if (s.official) out.push(badge(t('official'), 'badge-official'));
    if (s.spotlight) out.push(badge('✦ ' + t('editorsPick'), 'badge-spec'));
    if (s.tier === 'essential') out.push(badge(t('essential'), 'badge-muted'));
    if (s.specCompliant) out.push(badge(t('spec'), 'badge-spec'));
    out.push(licenseBadge(s.license));
    if (s.review && s.review.requiresReview) out.push(badge('⚠ ' + t('needsReview'), 'badge-warn'));
    (s.safeUse || []).forEach((n) => out.push(safeUseBadge(n)));
    if (!s.reviewed) out.push(badge(t('discovered'), 'badge-muted'));
    return out.slice(0, 7).join('');
  }

  function collectionBadges(c) {
    const out = [];
    if (c.official) out.push(badge(t('official'), 'badge-official'));
    if (c.featured) out.push(badge('✦ ' + t('editorsPick'), 'badge-spec'));
    out.push(badge(tierLabel(c), c.reviewed ? 'badge-muted' : 'badge-warn'));
    out.push(licenseBadge(c.license));
    out.push(badge(freshnessLabel(c), c.freshness === 'active' ? 'badge-clear' : 'badge-muted'));
    if (c.truncatedTree) out.push(badge('tree truncated', 'badge-warn', 'GitHub returned a truncated recursive tree'));
    return out.join('');
  }

  function cmdRow(cmd, label) {
    return `<div class="cmd-row"><code class="cmd">${esc(cmd)}</code><button class="btn-copy" type="button" data-copy="${esc(cmd)}">${esc(t('copy'))}</button></div>${label ? '' : ''}`;
  }

  function renderSkillCard(s) {
    const saved = state.saved.has(s.id);
    const tags = (s.tags || []).slice(0, 6).map((x) => `<span class="tag">#${esc(x)}</span>`).join('');
    return `<article class="card skill-card ${s.spotlight ? 'spotlight-card' : ''}" data-id="${esc(s.id)}">
      <div class="card-head">
        <div><h3 class="card-title">${esc(s.title)}</h3><span class="card-source">${esc(s.repo)} / ${esc(s.folder)}</span></div>
        <button class="save-btn ${saved ? 'saved' : ''}" type="button" data-action="save" data-id="${esc(s.id)}" aria-label="${esc(saved ? t('saved') : t('save'))}" title="${esc(saved ? t('saved') : t('save'))}">${saved ? '★' : '☆'}</button>
      </div>
      <div class="badges">${skillBadges(s)}</div>
      <p class="card-desc">${esc(s.shortDescription || s.description)}</p>
      <div class="tags">${tags}</div>
      ${cmdRow(s.install.direct)}
      <div class="card-foot">
        <div class="meta"><span><strong>★ ${compact(s.stars)}</strong></span><span>${esc(catLabel(s.category))}</span><span>${esc(timeAgo(s.daysSincePush))}</span></div>
        <div style="display:flex;gap:8px;align-items:center">
          <a class="link-btn" href="${esc(s.sourceUrl)}" target="_blank" rel="noopener noreferrer">${esc(t('source'))} ↗</a>
          <button class="btn-detail" type="button" data-action="detail" data-type="skill" data-id="${esc(s.id)}">${esc(t('details'))}</button>
        </div>
      </div>
    </article>`;
  }

  function renderCollectionCard(c) {
    const note = (state.lang === 'pl' && c.notePl) ? c.notePl : (c.note || c.description || '');
    const tags = [(c.sourceType === 'directory' ? `<span class="tag">${esc(t('directory'))}</span>` : ''), ...(c.tags || []).slice(0, 5).map((x) => `<span class="tag">#${esc(x)}</span>`)].join('');
    const saved = state.saved.has('collection:' + c.id);
    return `<article class="card collection-card" data-id="${esc(c.id)}">
      <div class="card-head"><div><h3 class="card-title">${esc(c.repo)}</h3><span class="card-source">${esc(catLabel(c.category))} · ${esc(c.license.label)}</span></div>
        <button class="save-btn ${saved ? 'saved' : ''}" type="button" data-action="save" data-id="${esc(c.id)}" aria-label="${esc(saved ? t('saved') : t('save'))}" title="${esc(saved ? t('saved') : t('save'))}">${saved ? '★' : '☆'}</button></div>
      <div class="badges">${collectionBadges(c)}</div>
      <p class="card-desc">${esc(note)}</p>
      <div class="tags">${tags}</div>
      ${cmdRow(c.install)}
      <div class="card-foot">
        <div class="meta"><span><strong>★ ${compact(c.stars)}</strong></span><span>${esc(t('skillsCount', { n: fmt(c.skillCount) }))}</span><span>${esc(timeAgo(c.daysSincePush))}</span></div>
        <div style="display:flex;gap:8px;align-items:center">
          <a class="link-btn" href="${esc(c.url)}" target="_blank" rel="noopener noreferrer">GitHub ↗</a>
          <button class="btn-detail" type="button" data-action="detail" data-type="collection" data-id="${esc(c.id)}">${esc(t('details'))}</button>
        </div>
      </div>
    </article>`;
  }

  function renderPackCard(p) {
    const title = p.title[state.lang] || p.title.en;
    const desc = p.description[state.lang] || p.description.en;
    const items = (p.skills || []).map((id) => skillById.get(id)).filter(Boolean);
    const chips = items.slice(0, 8).map((s) => `<span class="tag">${esc(s.title)}</span>`).join('');
    return `<article class="card pack-card">
      <div class="pack-head"><span class="pack-icon">${esc(p.icon || '📦')}</span><div><h3 class="card-title">${esc(title)}</h3><span class="card-source">${esc(t('packSkills', { n: items.length }))}</span></div></div>
      <p class="card-desc">${esc(desc)}</p>
      <div class="tags">${chips}</div>
      <pre>${esc(p.script || '')}</pre>
      <div class="pack-actions">
        <button class="btn primary" type="button" data-copy="${esc(p.script || '')}">${esc(t('copyBundle'))}</button>
        <button class="btn" type="button" data-action="pack-filter" data-pack="${esc(p.id)}">${esc(t('showPackSkills'))}</button>
      </div>
    </article>`;
  }

  function matches(hay, q) {
    if (!q) return true;
    const terms = q.toLowerCase().trim().split(/\s+/).filter(Boolean);
    return terms.every((term) => hay.includes(term));
  }

  function activeFilterCount() {
    return ['official', 'clearLicense', 'hideReview', 'savedOnly'].filter((k) => state[k]).length + (state.category !== 'all' ? 1 : 0) + (state.q ? 1 : 0) + (state.packFilter ? 1 : 0);
  }

  function filterSkills() {
    let rows = CAT.skills.slice();
    if (state.packFilter) rows = rows.filter((s) => state.packFilter.has(s.id));
    if (state.q) rows = rows.filter((s) => matches(`${s.id} ${s.name} ${s.title} ${s.description} ${s.repo} ${(s.tags || []).join(' ')} ${s.category}`.toLowerCase(), state.q));
    if (state.category !== 'all') rows = rows.filter((s) => s.category === state.category);
    if (state.official) rows = rows.filter((s) => s.official);
    if (state.clearLicense) rows = rows.filter((s) => ['clear', 'per-skill'].includes(s.license.status));
    if (state.curatedOnly) rows = rows.filter((s) => s.reviewed);
    if (state.hideReview) rows = rows.filter((s) => !s.review.requiresReview);
    if (state.savedOnly) rows = rows.filter((s) => state.saved.has(s.id));
    return sortRows(rows, 'skill');
  }

  function filterCollections() {
    let rows = CAT.collections.slice();
    if (state.q) rows = rows.filter((c) => matches(`${c.repo} ${c.description} ${c.note || ''} ${c.notePl || ''} ${(c.tags || []).join(' ')} ${c.category}`.toLowerCase(), state.q));
    if (state.category !== 'all') rows = rows.filter((c) => c.category === state.category);
    if (state.official) rows = rows.filter((c) => c.official);
    if (state.clearLicense) rows = rows.filter((c) => ['clear', 'per-skill'].includes(c.license.status));
    if (state.curatedOnly) rows = rows.filter((c) => c.reviewed);
    if (state.hideReview) rows = rows.filter((c) => !c.truncatedTree);
    if (state.savedOnly) rows = rows.filter((c) => state.saved.has('collection:' + c.id));
    return sortRows(rows, 'collection');
  }

  function filterPacks() {
    let rows = CAT.packs.slice();
    if (state.q) {
      rows = rows.filter((p) => {
        const names = (p.skills || []).map((id) => { const s = skillById.get(id); return s ? `${s.title} ${s.id}` : ''; }).join(' ');
        return matches(`${p.title.en} ${p.title.pl} ${p.description.en} ${p.description.pl} ${names}`.toLowerCase(), state.q);
      });
    }
    return rows;
  }

  function sortRows(rows, kind) {
    const by = state.sort;
    const val = (x) => x || 0;
    rows.sort((a, b) => {
      if (by === 'stars') return val(b.stars) - val(a.stars) || val(b.score) - val(a.score);
      if (by === 'freshness') return (a.daysSincePush ?? 99999) - (b.daysSincePush ?? 99999) || val(b.score) - val(a.score);
      if (by === 'skillCount') return val(b.skillCount || b.score) - val(a.skillCount || a.score);
      if (by === 'name') return String(a.title || a.repo || '').localeCompare(String(b.title || b.repo || ''), state.lang);
      return val(b.score) - val(a.score) || val(b.stars) - val(a.stars);
    });
    return rows;
  }

  function renderChips() {
    const source = state.view === 'collections' ? CAT.collections : CAT.skills;
    const counts = {};
    source.forEach((x) => { counts[x.category] = (counts[x.category] || 0) + 1; });
    const all = `<button class="chip ${state.category === 'all' ? 'active' : ''}" type="button" data-cat="all" aria-pressed="${state.category === 'all'}">${esc(t('all'))}<span class="chip-count">${fmt(source.length)}</span></button>`;
    const rest = CAT.categories.map((c) => `<button class="chip ${state.category === c.id ? 'active' : ''}" type="button" data-cat="${esc(c.id)}" aria-pressed="${state.category === c.id}"><span>${esc(c.icon || '')}</span> ${esc(c[state.lang] || c.en)}<span class="chip-count">${fmt(counts[c.id] || 0)}</span></button>`).join('');
    $('#categoryChips').innerHTML = all + rest;
  }

  function renderTabs() {
    $$('.tab').forEach((btn) => {
      const active = btn.dataset.view === state.view;
      btn.classList.toggle('active', active);
      btn.setAttribute('aria-selected', String(active));
    });
    $('#countSkills').textContent = fmt(CAT.skills.length);
    $('#countCollections').textContent = fmt(CAT.collections.length);
    $('#countPacks').textContent = fmt(CAT.packs.length);
  }

  function renderToggles() {
    $$('.toggle').forEach((btn) => {
      const on = Boolean(state[btn.dataset.toggle]);
      btn.classList.toggle('active', on);
      btn.setAttribute('aria-pressed', String(on));
    });
    $('#savedCount').textContent = state.saved.size ? String(state.saved.size) : '';
  }

  function renderActiveFilters() {
    const box = $('#activeFilters');
    if (!state.packFilter) { box.hidden = true; box.innerHTML = ''; return; }
    const label = state.packFilterLabel ? (state.packFilterLabel[state.lang] || state.packFilterLabel.en) : '';
    box.hidden = false;
    box.innerHTML = `<span class="active-chip">${esc(t('packFilter', { name: label }))}<button type="button" data-action="clear-pack-filter" aria-label="${esc(t('clear'))}">×</button></span>`;
  }

  function renderResultMeta(count, shown) {
    const noun = state.view === 'skills' ? t('resultsSkills', { n: fmt(count) })
      : state.view === 'collections' ? t('resultsCollections', { n: fmt(count) })
        : t('resultsPacks', { n: fmt(count) });
    const sortKeys = { relevance: 'sortRelevance', stars: 'sortStars', freshness: 'sortFresh', skillCount: 'sortSkills', name: 'sortName' };
    const mode = t(sortKeys[state.sort] || 'sortRelevance');
    const hidden = activeFilterCount() ? ` · <span style="color:var(--faint)">${esc(t('resultsHidden', { n: activeFilterCount() }))}</span>` : '';
    const pagination = shown < count ? ` · <span style="color:var(--faint)">${esc(t('showing', { shown: fmt(shown), total: fmt(count) }))}</span>` : '';
    $('#resultMeta').innerHTML = `${esc(noun)}${pagination} <span style="color:var(--faint)">${esc(t('sortedBy', { mode }))}</span>${hidden}`;
  }

  function renderCards() {
    const cards = $('#cards');
    let rows = [];
    let renderFn = renderSkillCard;
    if (state.view === 'skills') { rows = filterSkills(); renderFn = renderSkillCard; }
    else if (state.view === 'collections') { rows = filterCollections(); renderFn = renderCollectionCard; }
    else if (state.view === 'packs') { rows = filterPacks(); renderFn = renderPackCard; }
    const shown = rows.slice(0, state.visible);
    let html = shown.map(renderFn).join('');
    if (rows.length > shown.length) {
      html += `<div class="load-more"><button class="btn" type="button" data-action="load-more">${esc(t('loadMore'))}</button></div>`;
    }
    cards.innerHTML = html;
    $('#empty').hidden = rows.length > 0;
    renderResultMeta(rows.length, shown.length);
  }

  function renderStats() {
    const s = CAT.meta.stats;
    $('#statRepos').textContent = compact(s.reposScanned);
    $('#statFiles').textContent = compact(s.skillFilesFound);
    $('#statCollections').textContent = compact(s.collections);
    $('#statSkills').textContent = compact(s.indexedSkills);
    $('#heroDate').textContent = fmtDate(CAT.meta.generatedAt);
    $('#footerDate').textContent = fmtDate(CAT.meta.generatedAt);
  }

  function renderAgentRows() {
    $('#agentRows').innerHTML = CAT.agents.map((a) => `<tr><td>${esc(a.name)}</td><td>${esc(a.project)}</td><td>${esc(a.global)}</td></tr>`).join('');
  }

  function renderGuideCommands() {
    const s = skillById.get(CAT.spotlight[0]) || CAT.skills[0];
    if (!s) return;
    $('#guideDirectCmd').textContent = s.install.direct;
    $('#guideGlobalCmd').textContent = s.install.global;
    $('#guideManualCmd').textContent = s.install.manual;
  }

  function applyI18n() {
    document.documentElement.lang = state.lang;
    document.title = t('pageTitle');
    const meta = document.querySelector('meta[name="description"]');
    if (meta) meta.setAttribute('content', t('metaDescription'));
    $$('[data-i18n]').forEach((el) => { el.textContent = t(el.dataset.i18n); });
    $$('[data-i18n-placeholder]').forEach((el) => { el.placeholder = t(el.dataset.i18nPlaceholder); });
    $$('[data-i18n-aria]').forEach((el) => { el.setAttribute('aria-label', t(el.dataset.i18nAria)); });
    $('#langBtn').textContent = state.lang === 'pl' ? 'EN' : 'PL';
    $('#langBtn').setAttribute('aria-label', t('switchLang'));
    $('#themeBtn').textContent = state.theme === 'dark' ? '☀' : '☾';
    $('#themeBtn').setAttribute('aria-label', t('toggleTheme'));
    $('#clearSearch').setAttribute('aria-label', t('clearSearch'));
    $('#searchInput').setAttribute('aria-label', t('searchPlaceholder'));
    $('#sortSelect').setAttribute('aria-label', t('sortLabel'));
    $('#drawerClose').setAttribute('aria-label', t('close'));
  }

  function updateControls() {
    document.documentElement.dataset.theme = state.theme;
    $('#searchInput').value = state.q;
    $('#sortSelect').value = state.sort;
    $('#clearSearch').hidden = !state.q;
  }

  function updateURL() {
    const p = new URLSearchParams();
    if (state.q) p.set('q', state.q);
    if (state.view !== 'skills') p.set('view', state.view);
    if (state.category !== 'all') p.set('cat', state.category);
    if (state.sort !== 'relevance') p.set('sort', state.sort);
    if (state.lang !== 'pl') p.set('lang', state.lang);
    if (state.open) p.set(state.open.type, state.open.id);
    const qs = p.toString();
    history.replaceState(null, '', location.pathname + (qs ? '?' + qs : '') + location.hash);
  }

  function readURL() {
    const p = new URLSearchParams(location.search);
    if (['pl', 'en'].includes(p.get('lang'))) state.lang = p.get('lang');
    state.q = p.get('q') || '';
    state.view = ['skills', 'collections', 'packs', 'guide'].includes(p.get('view')) ? p.get('view') : 'skills';
    state.category = p.get('cat') || 'all';
    state.sort = ['relevance', 'stars', 'freshness', 'skillCount', 'name'].includes(p.get('sort')) ? p.get('sort') : 'relevance';
    if (p.get('skill')) pendingDrawer = { type: 'skill', id: p.get('skill') };
    else if (p.get('collection')) pendingDrawer = { type: 'collection', id: p.get('collection') };
  }

  function render() {
    if (!CAT) {
      $('#cards').innerHTML = `<div class="empty"><h3>${esc(t('dataMissing'))}</h3><p>${esc(t('dataMissingBody'))}</p></div>`;
      return;
    }
    if (!state._loadingMore) state.visible = 60;
    applyI18n();
    updateControls();
    renderTabs();
    renderChips();
    renderToggles();
    renderActiveFilters();
    const guide = state.view === 'guide';
    $('#guidePanel').hidden = !guide;
    $('#resultsArea').hidden = guide;
    $('#toolbar').hidden = guide || state.view === 'packs';
    if (!guide) renderCards();
    updateURL();
    state._loadingMore = false;
  }

  function cmdBlock(label, cmd) {
    return `<div class="command-item"><span class="cmd-label">${esc(label)}</span>${cmdRow(cmd)}</div>`;
  }

  function kv(pairs) {
    return `<dl class="kv">${pairs.map(([k, v]) => `<dt>${esc(k)}</dt><dd>${esc(v)}</dd>`).join('')}</dl>`;
  }

  function shareURL(type, id) {
    const u = new URL(location.href);
    u.searchParams.delete('skill');
    u.searchParams.delete('collection');
    u.searchParams.set(type, id);
    return u.toString();
  }

  function openDrawer(id, type) {
    const item = type === 'skill' ? skillById.get(id) : collectionById.get(id);
    if (!item) return;
    lastFocused = document.activeElement;
    state.open = { type, id };
    $('#drawerKicker').textContent = type === 'skill' ? 'SKILL.md' : 'COLLECTION';
    $('#drawerTitle').textContent = type === 'skill' ? item.title : item.repo;
    let body = '';

    if (type === 'skill') {
      const s = item;
      const saved = state.saved.has(s.id);
      const review = s.review || {};
      body += `<div class="badges">${skillBadges(s)}</div>`;
      body += `<p class="drawer-lead">${esc(s.description)}</p>`;
      if (review.requiresReview || ['unknown', 'check'].includes(s.license.status)) {
        body += `<div class="notice">${esc(review.requiresReview ? t('reviewNotice') + ' ' : '')}${esc(['unknown', 'check'].includes(s.license.status) ? t('licenseNotice') : '')}${s.license.note ? '<br><br>' + esc(s.license.note) : ''}</div>`;
      }
      if (s.safeUse && s.safeUse.length) {
        body += `<div class="notice"><strong>${esc(t('safeUse'))}:</strong><br>${s.safeUse.map((n) => `<strong>${esc(t(n.code === 'security' ? 'securityUse' : 'chineseUse'))}</strong> — ${esc(n[state.lang] || n.en)}`).join('<br><br>')}</div>`;
      }
      body += `<div class="drawer-section"><h3>${esc(t('details'))}</h3>${kv([
        [t('repo'), s.repo], [t('path'), s.path], [t('license'), `${s.license.label} (${s.license.status})`],
        [t('category'), catLabel(s.category)], [t('tier'), tierLabel(s)], [t('updated'), `${fmtDate(s.pushedAt)} · ${timeAgo(s.daysSincePush)}`],
        [t('stars'), fmt(s.stars)], [t('size'), `${fmt(s.contentLength)} chars`],
        [t('tools'), (review.allowedTools || []).join(', ') || '—'], [t('scripts'), review.hasScripts ? 'yes' : 'no'],
      ])}</div>`;
      body += `<div class="drawer-section"><h3>${esc(t('commands'))}</h3><div class="command-list">
        ${cmdBlock(t('directCmd'), s.install.direct)}
        ${cmdBlock(t('shorthandCmd'), s.install.shorthand)}
        ${cmdBlock(t('globalCmd'), s.install.global)}
        ${cmdBlock(t('useCmd'), s.install.use)}
        ${cmdBlock(t('manualCmd'), s.install.manual)}
      </div></div>`;
      const related = CAT.skills.filter((x) => x.repo === s.repo && x.id !== s.id).slice(0, 7);
      body += `<div class="drawer-section"><h3>${esc(t('related'))}</h3><div class="related-list">${related.length ? related.map((x) => `<button type="button" data-action="drawer-skill" data-id="${esc(x.id)}">${esc(x.title)} <span style="color:var(--faint)">· ${esc(x.folder)}</span></button>`).join('') : `<span class="muted-text">${esc(t('noRelated'))}</span>`}</div></div>`;
      body += `<div class="drawer-actions"><a class="btn primary" href="${esc(s.sourceUrl)}" target="_blank" rel="noopener noreferrer">${esc(t('viewSource'))} ↗</a><button class="btn" type="button" data-action="share" data-type="skill" data-id="${esc(s.id)}">${esc(t('share'))}</button><button class="btn" type="button" data-action="save" data-id="${esc(s.id)}">${esc(saved ? t('saved') : t('save'))}</button></div>`;
    } else {
      const c = item;
      const note = (state.lang === 'pl' && c.notePl) ? c.notePl : (c.note || c.description);
      body += `<div class="badges">${collectionBadges(c)}</div>`;
      body += `<p class="drawer-lead">${esc(note)}</p>`;
      if (!c.reviewed) body += `<div class="notice">${esc(t('discoveredNotice'))}</div>`;
      if (['unknown', 'check'].includes(c.license.status) || c.license.note) body += `<div class="notice">${esc(t('licenseNotice'))}${c.license.note ? '<br><br>' + esc(c.license.note) : ''}</div>`;
      body += `<div class="drawer-section"><h3>${esc(t('details'))}</h3>${kv([
        [t('repo'), c.repo], [t('category'), catLabel(c.category)], [t('license'), `${c.license.label} (${c.license.status})`],
        [t('stars'), fmt(c.stars)], [t('skillCountLabel'), fmt(c.skillCount)], [t('fileCountLabel'), fmt(c.skillFileCount)],
        [t('updated'), `${fmtDate(c.pushedAt)} · ${timeAgo(c.daysSincePush)}`], [t('tier'), tierLabel(c)],
      ])}</div>`;
      body += `<div class="drawer-section"><h3>${esc(t('commands'))}</h3><div class="command-list">
        ${cmdBlock(c.skillCount ? t('collectionCmd') : t('directory'), c.install)}
        ${cmdBlock(t('manualCmd'), `git clone --depth 1 ${c.url}.git /tmp/${c.name}`)}
      </div></div>`;
      const related = CAT.skills.filter((x) => x.collectionId === c.id).slice(0, 10);
      body += `<div class="drawer-section"><h3>${esc(t('indexedSkills'))} (${related.length})</h3><div class="related-list">${related.length ? related.map((x) => `<button type="button" data-action="drawer-skill" data-id="${esc(x.id)}">${esc(x.title)} <span style="color:var(--faint)">· ${esc(x.folder)}</span></button>`).join('') : `<span class="muted-text">${esc(t('noRelated'))}</span>`}</div></div>`;
      body += `<div class="drawer-actions"><a class="btn primary" href="${esc(c.url)}" target="_blank" rel="noopener noreferrer">${esc(t('openCollection'))} ↗</a><button class="btn" type="button" data-action="share" data-type="collection" data-id="${esc(c.id)}">${esc(t('share'))}</button></div>`;
    }
    $('#drawerBody').innerHTML = body;
    $('#drawer').hidden = false;
    $('#overlay').hidden = false;
    document.body.classList.add('drawer-open');
    $('#drawer').scrollTop = 0;
    $('#drawerClose').focus();
    updateURL();
  }

  function closeDrawer() {
    $('#drawer').hidden = true;
    $('#overlay').hidden = true;
    document.body.classList.remove('drawer-open');
    state.open = null;
    if (lastFocused && lastFocused.focus) lastFocused.focus();
    updateURL();
  }

  function showToast(msg) {
    const el = $('#toast');
    el.textContent = msg;
    el.classList.add('show');
    clearTimeout(showToast.timer);
    showToast.timer = setTimeout(() => el.classList.remove('show'), 1800);
  }

  async function copyText(text, btn) {
    let ok = false;
    try {
      if (navigator.clipboard && window.isSecureContext) { await navigator.clipboard.writeText(text); ok = true; }
    } catch { /* fall through */ }
    if (!ok) {
      try {
        const ta = document.createElement('textarea');
        ta.value = text; ta.style.position = 'fixed'; ta.style.opacity = '0';
        document.body.appendChild(ta); ta.select();
        ok = document.execCommand('copy'); ta.remove();
      } catch { ok = false; }
    }
    showToast(ok ? t('copied') : t('copyFailed'));
    if (btn && ok) {
      const original = btn.textContent;
      btn.textContent = '✓'; btn.classList.add('copied');
      setTimeout(() => { btn.textContent = original; btn.classList.remove('copied'); }, 1200);
    }
  }

  function resetFilters() {
    state.q = ''; state.category = 'all'; state.sort = 'relevance';
    Object.assign(state, defaults);
    state.packFilter = null; state.packFilterLabel = null;
    render();
  }

  function setView(view) {
    state.view = view;
    render();
    if (view === 'guide') $('#guidePanel').scrollIntoView({ behavior: 'smooth', block: 'start' });
  }

  function handleAction(btn) {
    const action = btn.dataset.action;
    const id = btn.dataset.id;
    if (action === 'load-more') { state._loadingMore = true; state.visible += 60; render(); return; }
    if (action === 'detail' || action === 'drawer-skill') { openDrawer(id, btn.dataset.type === 'collection' ? 'collection' : 'skill'); return; }
    if (action === 'save') {
      const key = collectionById.has(id) && !skillById.has(id) ? 'collection:' + id : id;
      if (state.saved.has(key)) state.saved.delete(key); else state.saved.add(key);
      localStorage.setItem('sl-saved', JSON.stringify([...state.saved]));
      showToast(state.saved.has(key) ? t('saved') : t('save'));
      render();
      if (state.open) openDrawer(state.open.id, state.open.type);
      return;
    }
    if (action === 'share') { copyText(shareURL(btn.dataset.type, btn.dataset.id), btn); showToast(t('shareDone')); return; }
    if (action === 'pack-filter') {
      const pack = CAT.packs.find((p) => p.id === btn.dataset.pack);
      if (!pack) return;
      state.packFilter = new Set(pack.skills);
      state.packFilterLabel = pack.title;
      state.view = 'skills'; state.q = ''; state.category = 'all';
      Object.assign(state, defaults);
      render();
      $('#workspace').scrollIntoView({ behavior: 'smooth', block: 'start' });
      return;
    }
    if (action === 'clear-pack-filter') { state.packFilter = null; state.packFilterLabel = null; render(); return; }
    if (action === 'reset') { resetFilters(); return; }
  }

  function bindEvents() {
    let debounce;
    $('#searchInput').addEventListener('input', (e) => {
      state.q = e.target.value;
      $('#clearSearch').hidden = !state.q;
      clearTimeout(debounce);
      debounce = setTimeout(render, 90);
    });
    $('#clearSearch').addEventListener('click', () => { state.q = ''; render(); $('#searchInput').focus(); });
    $('#sortSelect').addEventListener('change', (e) => { state.sort = e.target.value; render(); });
    $('#categoryChips').addEventListener('click', (e) => {
      const btn = e.target.closest('[data-cat]');
      if (btn) { state.category = btn.dataset.cat; render(); }
    });
    $$('.toggle').forEach((btn) => btn.addEventListener('click', () => { const k = btn.dataset.toggle; state[k] = !state[k]; render(); }));
    $$('.tab').forEach((btn) => btn.addEventListener('click', () => setView(btn.dataset.view)));
    $('#resetBtn').addEventListener('click', resetFilters);
    $('#emptyReset').addEventListener('click', resetFilters);
    $('#langBtn').addEventListener('click', () => { state.lang = state.lang === 'pl' ? 'en' : 'pl'; localStorage.setItem('sl-lang', state.lang); render(); });
    $('#themeBtn').addEventListener('click', () => { state.theme = state.theme === 'dark' ? 'light' : 'dark'; localStorage.setItem('sl-theme', state.theme); render(); });
    $('#installLink').addEventListener('click', (e) => { e.preventDefault(); setView('guide'); });
    $('.hero-cta a[href="#workspace"]').addEventListener('click', () => { if (state.view !== 'skills') { state.view = 'skills'; render(); } });
    $('#drawerClose').addEventListener('click', closeDrawer);
    $('#overlay').addEventListener('click', closeDrawer);
    document.addEventListener('click', (e) => {
      const copyBtn = e.target.closest('[data-copy]');
      if (copyBtn) { e.preventDefault(); copyText(copyBtn.dataset.copy, copyBtn); return; }
      const targetBtn = e.target.closest('[data-copy-target]');
      if (targetBtn) {
        e.preventDefault();
        const el = document.getElementById(targetBtn.dataset.copyTarget);
        if (el) copyText(el.textContent, targetBtn);
        return;
      }
      const actionBtn = e.target.closest('[data-action]');
      if (actionBtn) { e.preventDefault(); handleAction(actionBtn); }
    });
    document.addEventListener('keydown', (e) => {
      if (e.key === '/' && !/INPUT|TEXTAREA|SELECT/.test(document.activeElement.tagName)) { e.preventDefault(); $('#searchInput').focus(); }
      if (e.key === 'Escape' && state.open) closeDrawer();
    });
    window.addEventListener('popstate', () => { readURL(); render(); });
  }

  function init() {
    readURL();
    if (!CAT) {
      applyI18n();
      $('#cards').innerHTML = `<div class="empty"><h3>${esc(t('dataMissing'))}</h3><p>${esc(t('dataMissingBody'))}</p></div>`;
      bindEvents();
      return;
    }
    renderStats();
    renderAgentRows();
    renderGuideCommands();
    bindEvents();
    render();
    if (pendingDrawer && (skillById.has(pendingDrawer.id) || collectionById.has(pendingDrawer.id))) {
      openDrawer(pendingDrawer.id, pendingDrawer.type);
      pendingDrawer = null;
    }
  }

  init();
})();

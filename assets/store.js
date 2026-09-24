(() => {
  'use strict';

  const REPO = 'ctrl-mietze/DIOXAMINE-plugin-store';
  const RAW = `https://raw.githubusercontent.com/${REPO}/main/`;
  const CACHE_KEY = 'dioxamine-store-catalogue-v1';
  const CACHE_TTL = 6 * 60 * 60 * 1000;
  const STRINGS = {
    en: {
      skip:'Skip to content', languageLabel:'Select language', community:'COMMUNITY CATALOGUE', browse:'Browse plugins', submit:'Submit a plugin', repository:'Repository', menuLabel:'Open navigation menu', home:'Home', theme:'Theme',
      heroEyebrow:'AN OPEN COMMUNITY PROJECT', tagline:'Community-built plugins for DIOXAMINE.', heroBody:'Discover new plugins, extend your setup, and explore what the DIOXAMINE community is building.', getPlugins:'Get Plugins', viewRepo:'View Repository', independent:'An independent project maintained by the DIOXAMINE community.', catalogueStatus:'CATALOGUE STATUS', live:'LIVE', availablePlugins:'plugins available', catalogueSource:'Catalogue source', distribution:'Distribution', reviewStatus:'Review model', communityReview:'Community review', panelFoot:'Open catalogue · transparent packages · community-led', previewEmptyTitle:'A space for community plugins', previewEmptyBody:'The first listing starts here.', previewCaption:'OPEN · COMMUNITY-MAINTAINED', pluginsListed:'PLUGINS LISTED', reviewBeforeListing:'Community submissions are reviewed before listing.',
      builtOn:'BUILT FOR OPEN EXTENSION', principlesTitle:'A clear path from discovery to install.', principlesBody:"The catalogue stays in GitHub, packages stay inspectable, and DIOXAMINE's own installer remains in control.", step1Title:'Discover', step1Body:'Browse a public catalogue with version, source, compatibility, and permission details.', step2Title:'Inspect', step2Body:'Every package lives in the repository with its metadata and a verifiable SHA-256 digest.', step3Title:'Install', step3Body:"Compatible ZIPs are handed to DIOXAMINE's current plugin installer for validation.", forMakers:'FOR PLUGIN DEVELOPERS', joinTitle:'Build something for DIOXAMINE?', joinBody:'Anyone can create a compatible plugin and submit it for review by the community store maintainers.', readSubmission:'Read the submission guide', footerNote:'Community-built plugins for DIOXAMINE. Independently maintained.', contribute:'Contribute',
      catalogueLabel:'COMMUNITY CATALOGUE', catalogueIntro:'The DIOXAMINE Community Plugin Store is being built. This will become the central catalogue for community-created DIOXAMINE plugins.', inAppStore:'IN-APP STORE', inAppStoreBody:'Browse the catalogue inside DIOXAMINE with the community Store plugin.', downloadStore:'Download Store plugin', listed:'listed', searchLabel:'Search plugins', searchPlaceholder:'Search plugins…', categoryLabel:'Category', allCategories:'All categories', refresh:'Refresh', earlyStage:'EARLY STAGE', emptyTitle:'The community catalogue is taking shape.', emptyBody:'The DIOXAMINE Community Plugin Store is being built. This page will list community plugins as they are reviewed and added. There are no plugins in the catalogue yet.', fieldListTitle:'Each listing will include', fieldList:'Name · description · developer · version · category · compatibility · source · install option', buildForDioxamine:'Build for DIOXAMINE?', catalogueJoinTitle:'Build something for DIOXAMINE?', catalogueJoinBody:'Anyone can create a compatible DIOXAMINE plugin and submit it to the Community Plugin Store. Plugins are community projects and are reviewed before they are added to the catalogue.', trustNote:'Catalogue review checks the submission and package format; it is not a security audit or safety guarantee. Review plugins before installing.', install:'Install', details:'Details', version:'Version', compatibility:'Compatibility', noResults:'No plugins match these filters.', loading:'Loading catalogue…', stale:'Showing the last saved catalogue. GitHub could not be reached.', failed:'The catalogue could not be loaded. Check your connection and try again.', refreshed:'Catalogue refreshed.', installHandoff:'The package will open from GitHub. After it downloads, open the ZIP with DIOXAMINE to pass it to the current installer.', installBrowser:'Open package download', description:'Description', screenshots:'Screenshots', permissions:'Permissions', source:'Source code', changelog:'What’s new', minVersion:'Minimum DIOXAMINE version code', notFound:'This plugin is not in the current catalogue.', openPackage:'Download ZIP', updateDate:'Updated',
    },
    de: {
      skip:'Zum Inhalt springen', languageLabel:'Sprache auswählen', community:'COMMUNITY-KATALOG', browse:'Plugins entdecken', submit:'Plugin einreichen', repository:'Repository', menuLabel:'Navigationsmenü öffnen', home:'Startseite', theme:'Design',
      heroEyebrow:'EIN OFFENES COMMUNITY-PROJEKT', tagline:'Community-Plugins für DIOXAMINE.', heroBody:'Entdecke neue Plugins, erweitere dein Setup und sieh dir an, was die DIOXAMINE-Community entwickelt.', getPlugins:'Plugins installieren', viewRepo:'Repository ansehen', independent:'Ein unabhängiges, von der DIOXAMINE-Community gepflegtes Projekt.', catalogueStatus:'KATALOGSTATUS', live:'LIVE', availablePlugins:'Plugins verfügbar', catalogueSource:'Katalogquelle', distribution:'Verteilung', reviewStatus:'Prüfung', communityReview:'Community-Prüfung', panelFoot:'Offener Katalog · nachvollziehbare Pakete · von der Community getragen', previewEmptyTitle:'Platz für Community-Plugins', previewEmptyBody:'Der erste Eintrag beginnt hier.', previewCaption:'OFFEN · VON DER COMMUNITY GEPFLEGT', pluginsListed:'GELISTETE PLUGINS', reviewBeforeListing:'Community-Einreichungen werden vor der Aufnahme geprüft.',
      builtOn:'FÜR OFFENE ERWEITERUNGEN', principlesTitle:'Ein klarer Weg vom Entdecken bis zur Installation.', principlesBody:'Der Katalog liegt auf GitHub, Pakete bleiben einsehbar und DIOXAMINE behält die Kontrolle über die Installation.', step1Title:'Entdecken', step1Body:'Ein öffentlicher Katalog mit Angaben zu Version, Quelle, Kompatibilität und Berechtigungen.', step2Title:'Prüfen', step2Body:'Jedes Paket liegt im Repository mit Metadaten und überprüfbarem SHA-256-Hash.', step3Title:'Installieren', step3Body:'Kompatible ZIP-Dateien werden zur Prüfung an DIOXAMINEs aktuellen Plugin-Installer übergeben.', forMakers:'FÜR PLUGIN-ENTWICKLER', joinTitle:'Du entwickelst etwas für DIOXAMINE?', joinBody:'Jeder kann ein kompatibles Plugin erstellen und zur Prüfung durch die Store-Verantwortlichen einreichen.', readSubmission:'Einreichungsanleitung lesen', footerNote:'Community-Plugins für DIOXAMINE. Unabhängig gepflegt.', contribute:'Mitwirken',
      catalogueLabel:'COMMUNITY-KATALOG', catalogueIntro:'Der DIOXAMINE Community Plugin Store befindet sich im Aufbau. Diese Seite wird zum zentralen Katalog für von der Community entwickelte DIOXAMINE-Plugins.', inAppStore:'IN-APP-STORE', inAppStoreBody:'Durchsuche den Katalog direkt in DIOXAMINE mit dem Community-Store-Plugin.', downloadStore:'Store-Plugin herunterladen', listed:'gelistet', searchLabel:'Plugins suchen', searchPlaceholder:'Plugins suchen …', categoryLabel:'Kategorie', allCategories:'Alle Kategorien', refresh:'Aktualisieren', earlyStage:'IM AUFBAU', emptyTitle:'Der Community-Katalog nimmt Gestalt an.', emptyBody:'Der DIOXAMINE Community Plugin Store wird gerade aufgebaut. Hier erscheinen Community-Plugins, sobald sie geprüft und aufgenommen wurden. Aktuell sind noch keine Plugins im Katalog.', fieldListTitle:'Jeder Eintrag enthält', fieldList:'Name · Beschreibung · Entwickler · Version · Kategorie · Kompatibilität · Quelle · Installation', buildForDioxamine:'Für DIOXAMINE entwickeln?', catalogueJoinTitle:'Du entwickelst etwas für DIOXAMINE?', catalogueJoinBody:'Jeder darf ein kompatibles DIOXAMINE-Plugin entwickeln und zur Aufnahme in den Community Plugin Store einreichen. Die Plugins sind Community-Projekte und werden vor der Aufnahme in den Katalog geprüft.', trustNote:'Die Katalogprüfung kontrolliert Einreichung und Paketformat; sie ist kein Sicherheitsaudit und keine Sicherheitsgarantie. Prüfe Plugins vor der Installation.', install:'Installieren', details:'Details', version:'Version', compatibility:'Kompatibilität', noResults:'Keine Plugins entsprechen diesen Filtern.', loading:'Katalog wird geladen …', stale:'Der gespeicherte Katalog wird angezeigt. GitHub ist momentan nicht erreichbar.', failed:'Der Katalog konnte nicht geladen werden. Prüfe die Verbindung und versuche es erneut.', refreshed:'Katalog aktualisiert.', installHandoff:'Das Paket wird von GitHub geöffnet. Öffne nach dem Download die ZIP-Datei mit DIOXAMINE, damit sie an den aktuellen Installer übergeben wird.', installBrowser:'Paket-Download öffnen', description:'Beschreibung', screenshots:'Screenshots', permissions:'Berechtigungen', source:'Quellcode', changelog:'Änderungen', minVersion:'Minimale DIOXAMINE-Version (Code)', notFound:'Dieses Plugin ist nicht im aktuellen Katalog.', openPackage:'ZIP herunterladen', updateDate:'Aktualisiert',
    }
  };

  let language = localStorage.getItem('dioxamine-store-language') || ((navigator.language || 'en').toLowerCase().startsWith('de') ? 'de' : 'en');
  let catalogue = [];
  const $ = (selector, root=document) => root.querySelector(selector);
  const tr = key => (STRINGS[language] && STRINGS[language][key]) || STRINGS.en[key] || key;
  const safe = value => String(value ?? '').replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  const localized = value => typeof value === 'string' ? value : (value && (value[language] || value.en)) || '';

  function applyLanguage() {
    document.documentElement.lang = language;
    document.querySelectorAll('[data-i18n]').forEach(el => { const key=el.dataset.i18n; if (STRINGS[language][key]) el.textContent=tr(key); });
    document.querySelectorAll('[data-i18n-placeholder]').forEach(el => { el.placeholder=tr(el.dataset.i18nPlaceholder); });
    document.querySelectorAll('[data-i18n-aria]').forEach(el => { el.setAttribute('aria-label',tr(el.dataset.i18nAria)); });
    document.querySelectorAll('[data-lang]').forEach(el => el.setAttribute('aria-pressed',String(el.dataset.lang===language)));
    document.title = document.body.dataset.page === 'catalogue' ? `${tr('getPlugins')} — DIOXAMINE Plugin Store` : 'DIOXAMINE Plugin Store — Community-built plugins';
    if (catalogue.length) { drawCards(); if (document.body.dataset.page === 'detail') drawDetail(); }
  }

  async function getCatalogue(force=false) {
    const current = Date.now();
    let cached;
    try { cached=JSON.parse(localStorage.getItem(CACHE_KEY)||'null'); } catch (_) { cached=null; }
    if (!force && cached && Array.isArray(cached.plugins) && current-cached.savedAt<CACHE_TTL) {
      catalogue=cached.plugins;
      return { stale:false, cached:true };
    }
    try {
      let payload;
      if (window.dioxamine && dioxamine.http && typeof dioxamine.http.fetch === 'function') {
        const response=await dioxamine.http.fetch(RAW+'catalogue/plugins.json',{timeoutMs:20000});
        if (response.status<200 || response.status>=300) throw new Error(`HTTP ${response.status}`);
        payload=JSON.parse(response.data);
      } else {
        const cataloguePath=document.body.dataset.page==='home'?'catalogue/plugins.json':'../catalogue/plugins.json';
        const response=await fetch(cataloguePath,{cache:force?'no-store':'default'});
        if (!response.ok) throw new Error(`HTTP ${response.status}`);
        payload=await response.json();
      }
      if (!payload || payload.schemaVersion!==1 || !Array.isArray(payload.plugins)) throw new Error('Unsupported catalogue format');
      catalogue=payload.plugins.filter(p => p && typeof p.id==='string' && typeof p.package==='string');
      localStorage.setItem(CACHE_KEY,JSON.stringify({plugins:catalogue,savedAt:current}));
      return {stale:false,cached:false};
    } catch (error) {
      if (cached && Array.isArray(cached.plugins)) {
        catalogue=cached.plugins;
        return {stale:true,cached:true,error};
      }
      throw error;
    }
  }

  function setStatus(text, show=true) {
    const node=$('#catalogue-message');
    if (!node) return;
    node.textContent=text;
    node.hidden=!show;
  }

  function pluginIcon(plugin) {
    const fallback='<span class="plugin-icon" aria-hidden="true">D</span>';
    if (!plugin.icon) return fallback;
    const path=String(plugin.icon);
    if (path.startsWith('/') || path.includes('..') || /^https?:/i.test(path)) return fallback;
    return `<img class="plugin-icon" alt="" src="${safe(RAW+path)}">`;
  }

  function pluginUrl(plugin) { return `${RAW}${plugin.package.split('/').map(encodeURIComponent).join('/')}`; }
  function detailHref(plugin) { return `detail.html?id=${encodeURIComponent(plugin.id)}`; }

  function drawCards() {
    const grid=$('#plugin-grid');
    if (!grid) return;
    const search=($('#plugin-search')?.value||'').trim().toLocaleLowerCase();
    const category=$('#category-filter')?.value || 'all';
    const filtered=catalogue.filter(p => {
      const haystack=[p.id,localized(p.name),localized(p.description),p.author,p.category].join(' ').toLocaleLowerCase();
      return (!search || haystack.includes(search)) && (category==='all' || p.category===category);
    });
    const count=$('#plugin-count'); if (count) count.textContent=String(catalogue.length);
    $('#empty-state').hidden=catalogue.length!==0 || Boolean(search) || category!=='all';
    grid.hidden=filtered.length===0;
    if (!filtered.length && (search || category!=='all')) setStatus(tr('noResults'));
    else if (catalogue.length) setStatus('',false);
    grid.innerHTML=filtered.map(p => `<article class="plugin-card">
      <div class="plugin-card-head">${pluginIcon(p)}<div><h2>${safe(localized(p.name)||p.id)}</h2><span class="author">${safe(p.author||'')}</span></div></div>
      <p class="plugin-description">${safe(localized(p.description))}</p>
      <div class="plugin-meta"><span class="tag">${safe(p.category||'Other')}</span><span class="tag">${safe(tr('version'))} ${safe(p.version)}</span><span class="tag">DIOXAMINE ${safe(p.compatibility?.minVersion||'')}</span></div>
      <div class="plugin-card-actions"><a href="${safe(detailHref(p))}">${safe(tr('details'))} →</a><a class="button button-primary install-link" href="${safe(pluginUrl(p))}" download>${safe(tr('install'))}<span aria-hidden="true">↓</span></a></div>
    </article>`).join('');
    grid.querySelectorAll('.install-link').forEach(a => a.addEventListener('click', e => {
      if (window.dioxamine && typeof dioxamine.showToast==='function') dioxamine.showToast(tr('installHandoff'),'long');
    }));
  }

  function drawDetail() {
    const host=$('#plugin-detail'); if (!host) return;
    const id=new URLSearchParams(location.search).get('id');
    const p=catalogue.find(item=>item.id===id);
    if (!p) { host.innerHTML=`<section class="empty-state"><h1>${safe(tr('notFound'))}</h1><a class="button button-secondary" href="./">${safe(tr('browse'))}</a></section>`; return; }
    const source=String(p.source||'');
    const sourceHref=/^https:\/\//i.test(source)?source:'#';
    const permissions=Object.entries(p.permissions||{}).flatMap(([kind,items])=>Array.isArray(items)?items.map(item=>`${kind}: ${item}`):[]).join(', ') || '—';
    host.innerHTML=`<div class="detail-layout"><article class="detail-main"><div class="detail-title-row">${pluginIcon(p)}<div><h1>${safe(localized(p.name)||p.id)}</h1><p>${safe(p.author||'')}</p></div></div><h2>${safe(tr('description'))}</h2><p>${safe(localized(p.description))}</p>${p.changelog?`<h2>${safe(tr('changelog'))}</h2><p>${safe(localized(p.changelog))}</p>`:''}${Array.isArray(p.screenshots)&&p.screenshots.length?`<h2>${safe(tr('screenshots'))}</h2><div class="plugin-meta">${p.screenshots.map(s=>`<a class="tag" href="${safe(RAW+s)}">${safe(s.split('/').pop())}</a>`).join('')}</div>`:''}</article><aside class="detail-side"><dl><dt>${safe(tr('version'))}</dt><dd>${safe(p.version)} (${safe(p.versionCode)})</dd><dt>${safe(tr('compatibility'))}</dt><dd>DIOXAMINE ${safe(p.compatibility?.minVersion||'')}</dd><dt>${safe(tr('permissions'))}</dt><dd>${safe(permissions)}</dd><dt>${safe(tr('source'))}</dt><dd><a href="${safe(sourceHref)}" target="_blank" rel="noreferrer">${safe(source||'—')}</a></dd><dt>${safe(tr('updateDate'))}</dt><dd>${safe(p.updatedAt||'—')}</dd><dt>SHA-256</dt><dd><code>${safe(p.sha256||'—')}</code></dd></dl><a class="button button-primary" href="${safe(pluginUrl(p))}" download>${safe(tr('openPackage'))}<span aria-hidden="true">↓</span></a></aside></div>`;
    host.querySelector('.button').addEventListener('click',()=>{if(window.dioxamine&&dioxamine.showToast)dioxamine.showToast(tr('installHandoff'),'long');});
  }

  function setTheme(theme) {
    if (theme==='system') delete document.documentElement.dataset.theme;
    else document.documentElement.dataset.theme=theme;
    localStorage.setItem('dioxamine-store-theme',theme);
    const button=$('.theme-toggle'); if (button) button.title=`Theme: ${theme}`;
  }
  function cycleTheme() {
    const current=localStorage.getItem('dioxamine-store-theme')||'system';
    setTheme(({system:'light',light:'dark',dark:'system'})[current]||'system');
  }

  document.querySelectorAll('[data-lang]').forEach(button=>button.addEventListener('click',()=>{
    language=button.dataset.lang; localStorage.setItem('dioxamine-store-language',language); applyLanguage();
  }));
  document.querySelectorAll('.theme-toggle').forEach(button=>button.addEventListener('click',cycleTheme));
  const theme=localStorage.getItem('dioxamine-store-theme'); if(theme) setTheme(theme);
  const menu=$('.menu-toggle');
  menu?.addEventListener('click',()=>{const open=menu.getAttribute('aria-expanded')==='true';menu.setAttribute('aria-expanded',String(!open));$('#mobile-menu').hidden=open;});
  $('#plugin-search')?.addEventListener('input',drawCards);
  $('#category-filter')?.addEventListener('change',drawCards);
  $('#refresh-catalogue')?.addEventListener('click',async()=>{
    const button=$('#refresh-catalogue');button.disabled=true;
    try { const result=await getCatalogue(true); fillCategories(); drawCards(); setStatus(result.stale?tr('stale'):tr('refreshed')); }
    catch (_) { setStatus(tr('failed')); }
    finally { button.disabled=false; }
  });

  function fillCategories() {
    const select=$('#category-filter'); if (!select) return;
    const selected=select.value || 'all';
    const categories=[...new Set(catalogue.map(p=>p.category).filter(Boolean))].sort((a,b)=>a.localeCompare(b));
    select.innerHTML=`<option value="all">${safe(tr('allCategories'))}</option>`+categories.map(c=>`<option value="${safe(c)}">${safe(c)}</option>`).join('');
    if(categories.includes(selected)) select.value=selected;
  }

  applyLanguage();
  if ($('#plugin-count')) $('#plugin-count').textContent='0';
  if (document.body.dataset.page==='catalogue' || document.body.dataset.page==='detail') {
    if ($('#catalogue-message')) setStatus(tr('loading'));
    getCatalogue().then(result=>{
      fillCategories();
      if(document.body.dataset.page==='catalogue') drawCards(); else drawDetail();
      if(result.stale) setStatus(tr('stale'));
    }).catch(()=>{setStatus(tr('failed'));if(document.body.dataset.page==='catalogue')drawCards();else drawDetail();});
  } else {
    getCatalogue().then(()=>{const count=$('#plugin-count');if(count)count.textContent=String(catalogue.length);}).catch(()=>{const count=$('#plugin-count');if(count)count.textContent='0';});
  }
})();

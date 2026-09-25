(() => {
  'use strict';
  const REPO='ctrl-mietze/DIOXAMINE-plugin-store';
  const CATALOGUE=`https://raw.githubusercontent.com/${REPO}/main/catalogue/plugins.json`;
  const RAW=`https://raw.githubusercontent.com/${REPO}/main/`;
  const CACHE='dioxamine.pluginstore.catalogue.v1';
  const TTL=6*60*60*1000;
  const copy={
    en:{community:'COMMUNITY PLUGINS',communityStore:'COMMUNITY PLUGIN STORE',title:'Discover plugins.',intro:'Community-built plugins for DIOXAMINE. Browse the public catalogue and inspect each project before installing.',loading:'Loading catalogue…',available:'available',early:'EARLY STAGE',emptyTitle:'The catalogue is taking shape.',emptyBody:'There are no community plugins listed yet. New submissions will appear here after review.',submit:'How to submit a plugin →',trust:'Plugins are community projects. A listing is not a security audit or endorsement. Check the source and requested permissions before installation.',footer:'Independent community project · Catalogue hosted on GitHub',search:'Search plugins…',install:'Install',details:'Details',version:'Version',compatibility:'DIOXAMINE',refresh:'Refresh',loadError:'Could not load the catalogue. Check your network permission and connection.',cached:'Showing the last saved catalogue; GitHub is currently unavailable.',notFound:'Plugin not found.',description:'Description',source:'Source',permissions:'Permissions',sha:'SHA-256',openPackage:'Open package download',handoff:'The package opens from GitHub. After it downloads, open the ZIP with DIOXAMINE. If Open with is unavailable, use Plugins → Install Plugin and select the ZIP.',noMatch:'No plugins match these filters.',category:'Category',all:'All categories',changelog:'What’s new',screenshots:'Screenshots',minVersion:'Minimum app version code'},
    de:{community:'COMMUNITY-PLUGINS',communityStore:'COMMUNITY PLUGIN STORE',title:'Plugins entdecken.',intro:'Community-Plugins für DIOXAMINE. Durchsuche den öffentlichen Katalog und prüfe jedes Projekt vor der Installation.',loading:'Katalog wird geladen …',available:'verfügbar',early:'IM AUFBAU',emptyTitle:'Der Katalog nimmt Gestalt an.',emptyBody:'Aktuell sind noch keine Community-Plugins gelistet. Neue Einreichungen erscheinen nach der Prüfung hier.',submit:'Plugin einreichen →',trust:'Plugins sind Community-Projekte. Ein Eintrag ist weder Sicherheitsaudit noch Empfehlung. Prüfe Quelle und angeforderte Berechtigungen vor der Installation.',footer:'Unabhängiges Community-Projekt · Katalog auf GitHub',search:'Plugins suchen …',install:'Installieren',details:'Details',version:'Version',compatibility:'DIOXAMINE',refresh:'Aktualisieren',loadError:'Katalog nicht erreichbar. Prüfe Netzwerkberechtigung und Verbindung.',cached:'Der zuletzt gespeicherte Katalog wird angezeigt; GitHub ist momentan nicht erreichbar.',notFound:'Plugin nicht gefunden.',description:'Beschreibung',source:'Quelle',permissions:'Berechtigungen',sha:'SHA-256',openPackage:'Paket-Download öffnen',handoff:'Das Paket wird von GitHub geöffnet. Öffne nach dem Download die ZIP-Datei mit DIOXAMINE. Falls „Öffnen mit“ fehlt, wähle Plugins → Install Plugin und dann die ZIP-Datei.',noMatch:'Keine Plugins entsprechen diesen Filtern.',category:'Kategorie',all:'Alle Kategorien',changelog:'Änderungen',screenshots:'Screenshots',minVersion:'Minimale App-Version (Code)'}
  };
  let lang=localStorage.getItem('dioxamine.pluginstore.lang')||((navigator.language||'en').toLowerCase().startsWith('de')?'de':'en');
  let plugins=[];
  const $=s=>document.querySelector(s), t=k=>copy[lang][k]||copy.en[k]||k;
  const esc=s=>String(s??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  const local=v=>typeof v==='string'?v:(v?.[lang]||v?.en||'');
  function translate(){document.documentElement.lang=lang;document.querySelectorAll('[data-t]').forEach(n=>n.textContent=t(n.dataset.t));document.querySelectorAll('[data-lang]').forEach(n=>n.setAttribute('aria-pressed',String(n.dataset.lang===lang)));$('#search').placeholder=t('search');$('#search').setAttribute('aria-label',t('search'));fillCategories();if(plugins.length)render();}
  async function fetchCatalogue(){
    let cached=null;try{cached=JSON.parse(localStorage.getItem(CACHE)||'null');}catch(_){}
    try{
      if(!window.dioxamine||!dioxamine.http||typeof dioxamine.http.fetch!=='function')throw new Error('DIOXAMINE network bridge unavailable');
      const response=await dioxamine.http.fetch(CATALOGUE,{timeoutMs:20000});
      if(response.status<200||response.status>=300)throw new Error(`HTTP ${response.status}`);
      const data=JSON.parse(response.data);if(data.schemaVersion!==1||!Array.isArray(data.plugins))throw new Error('Unsupported catalogue format');
      plugins=data.plugins.filter(p=>p&&typeof p.id==='string'&&typeof p.package==='string');
      localStorage.setItem(CACHE,JSON.stringify({savedAt:Date.now(),plugins}));$('#state').textContent='';
    }catch(error){
      if(cached&&Array.isArray(cached.plugins)){plugins=cached.plugins;$('#state').textContent=t('cached');}
      else{$('#state').textContent=t('loadError');plugins=[];}
    }
    fillCategories();render();
  }
  function fillCategories(){const select=$('#category');if(!select)return;const old=select.value||'all';const values=[...new Set(plugins.map(p=>p.category).filter(Boolean))].sort((a,b)=>a.localeCompare(b));select.innerHTML=`<option value="all">${esc(t('all'))}</option>`+values.map(v=>`<option value="${esc(v)}">${esc(v)}</option>`).join('');if(values.includes(old))select.value=old;}
  function render(){
    $('#count').textContent=String(plugins.length);
    const query=$('#search').value.trim().toLocaleLowerCase();
    const category=$('#category').value||'all';
    const rows=plugins.filter(p=>[p.id,p.author,p.category,local(p.name),local(p.description)].join(' ').toLocaleLowerCase().includes(query)&&(category==='all'||p.category===category));
    $('#empty').hidden=plugins.length>0||Boolean(query);
    const cards=$('#cards');cards.hidden=!rows.length;
    if(plugins.length&&!rows.length)$('#state').textContent=t('noMatch');else if(plugins.length)$('#state').textContent='';
    cards.innerHTML=rows.map(p=>{
      const url=RAW+p.package.split('/').map(encodeURIComponent).join('/');
      const image=`<span class="plugin-icon" aria-hidden="true">${esc((local(p.name)||p.id).slice(0,1).toUpperCase())}</span>`;
      return `<article class="card"><div class="card-head">${image}<div><h2>${esc(local(p.name)||p.id)}</h2><span class="author">${esc(p.author||'')}</span></div></div><p class="description">${esc(local(p.description))}</p><div class="meta"><span class="tag">${esc(p.category||'Other')}</span><span class="tag">${esc(p.accessLevel||'standard')}</span><span class="tag">${esc(t('version'))} ${esc(p.version)}</span><span class="tag">${esc(t('compatibility'))} ${esc(p.compatibility?.minVersion||'')}</span></div><div class="card-actions"><button class="button details" type="button" data-id="${esc(p.id)}">${esc(t('details'))}</button>${p.installable===false?'<button class="button" type="button" disabled>Native bridge required</button>':`<a class="button primary install" href="${esc(url)}">${esc(t('install'))} ↓</a>`}</div></article>`;
    }).join('');
    cards.querySelectorAll('.details').forEach(button=>button.addEventListener('click',()=>showDetails(plugins.find(p=>p.id===button.dataset.id))));
    cards.querySelectorAll('.install').forEach(link=>link.addEventListener('click',async event=>{
      event.preventDefault();
      const packageUrl=link.href;
      if(window.dioxamine&&typeof dioxamine.openUrl==='function'){
        try{await dioxamine.openUrl(packageUrl);$('#state').textContent=t('handoff');}
        catch(error){$('#state').textContent=error.message||t('loadError');}
      }else{location.href=packageUrl;}
    }));
  }
  function showDetails(p){
    if(!p)return;
    const url=RAW+p.package.split('/').map(encodeURIComponent).join('/');
    const permissions=Object.entries(p.permissions||{}).flatMap(([k,v])=>Array.isArray(v)?v.map(x=>`${k}: ${x}`):[]).join(', ')||'—';
    const source=typeof p.source==='string'&&p.source.startsWith('https://')?p.source:'#';
    const changelog=p.changelog?`<h3>${esc(t('changelog'))}</h3><p class="detail-copy">${esc(local(p.changelog))}</p>`:'';
    const screenshots=Array.isArray(p.screenshots)?p.screenshots.filter(s=>typeof s==='string'&&!s.startsWith('/')&&!s.includes('..')).map(s=>`<a class="tag screenshot" href="${esc(RAW+s.split('/').map(encodeURIComponent).join('/'))}">${esc(s.split('/').pop())}</a>`).join(' '):'';
    $('#detail-content').innerHTML=`<div class="detail-title"><span class="plugin-icon" aria-hidden="true">${esc((local(p.name)||p.id).slice(0,1).toUpperCase())}</span><div><h2>${esc(local(p.name)||p.id)}</h2><p>${esc(p.author||'')} · ${esc(p.version||'')}</p></div></div><h3>${esc(t('description'))}</h3><p class="detail-copy">${esc(local(p.description))}</p>${changelog}${screenshots?`<h3>${esc(t('screenshots'))}</h3><p class="detail-list">${screenshots}</p>`:''}<p class="detail-list"><b>${esc(t('category'))}:</b> ${esc(p.category||'—')}<br><b>${esc(t('permissions'))}:</b> ${esc(permissions)}<br><b>${esc(t('source'))}:</b> <a class="external" href="${esc(source)}">${esc(p.source||'—')}</a><br><b>${esc(t('minVersion'))}:</b> ${esc(p.compatibility?.minVersionCode||'—')}<br><b>${esc(t('sha'))}:</b> ${esc(p.sha256||'—')}</p>${p.installable===false?'<button class="button" type="button" disabled>Native bridge required</button>':`<a class="button primary detail-install" href="${esc(url)}">${esc(t('openPackage'))} ↓</a><p class="handoff">${esc(t('handoff'))}</p>`}`;
    $('#detail-content .detail-install')?.addEventListener('click',async e=>{e.preventDefault();if(window.dioxamine&&dioxamine.openUrl){try{await dioxamine.openUrl(url);}catch(err){$('#state').textContent=err.message||t('loadError');}}else location.href=url;});
    $('#detail-content .external')?.addEventListener('click',async e=>{if(window.dioxamine&&dioxamine.openUrl){e.preventDefault();try{await dioxamine.openUrl(source);}catch(err){$('#state').textContent=err.message||t('loadError');}}});
    $('#details').showModal();
  }
  document.querySelectorAll('[data-lang]').forEach(b=>b.addEventListener('click',()=>{lang=b.dataset.lang;localStorage.setItem('dioxamine.pluginstore.lang',lang);translate();}));
  $('#search').addEventListener('input',render);
  $('#category').addEventListener('change',render);
  $('#refresh').addEventListener('click',fetchCatalogue);
  translate();fetchCatalogue();
})();

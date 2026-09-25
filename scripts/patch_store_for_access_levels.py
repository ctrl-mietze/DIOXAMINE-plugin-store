from pathlib import Path
p=Path(r"C:\Users\Mietze\Documents\GitHub\DIOXAMINE-plugin-store\store-plugin\store.js")
s=p.read_text(encoding="utf-8")
s=s.replace(
    "<div class=\"meta\"><span class=\"tag\">${esc(p.category||'Other')}</span><span class=\"tag\">${esc(t('version'))} ${esc(p.version)}</span><span class=\"tag\">${esc(t('compatibility'))} ${esc(p.compatibility?.minVersion||'')}</span></div><div class=\"card-actions\"><button class=\"button details\" type=\"button\" data-id=\"${esc(p.id)}\">${esc(t('details'))}</button><a class=\"button primary install\" href=\"${esc(url)}\">${esc(t('install'))} ↓</a></div>",
    "<div class=\"meta\"><span class=\"tag\">${esc(p.category||'Other')}</span><span class=\"tag\">${esc(p.accessLevel||'standard')}</span><span class=\"tag\">${esc(t('version'))} ${esc(p.version)}</span><span class=\"tag\">${esc(t('compatibility'))} ${esc(p.compatibility?.minVersion||'')}</span></div><div class=\"card-actions\"><button class=\"button details\" type=\"button\" data-id=\"${esc(p.id)}\">${esc(t('details'))}</button>${p.installable===false?'<button class=\"button\" type=\"button\" disabled>Native bridge required</button>':`<a class=\"button primary install\" href=\"${esc(url)}\">${esc(t('install'))} ↓</a>`}</div>"
)
s=s.replace(
    "<a class=\"button primary detail-install\" href=\"${esc(url)}\">${esc(t('openPackage'))} ↓</a><p class=\"handoff\">${esc(t('handoff'))}</p>",
    "${p.installable===false?'<button class=\"button\" type=\"button\" disabled>Native bridge required</button>':`<a class=\"button primary detail-install\" href=\"${esc(url)}\">${esc(t('openPackage'))} ↓</a><p class=\"handoff\">${esc(t('handoff'))}</p>`}"
)
s=s.replace(
    "$('#detail-content .detail-install').addEventListener('click',async e=>",
    "$('#detail-content .detail-install')?.addEventListener('click',async e=>"
)
p.write_text(s,encoding="utf-8")
print("patched", "accessLevel" in s, "installable===false" in s)

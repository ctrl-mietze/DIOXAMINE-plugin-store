from __future__ import annotations
import json, hashlib, zipfile, html
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PLUGINS = ROOT / "plugins"
PLUGINS.mkdir(parents=True, exist_ok=True)
AUTHOR = "DIOXAMINE Plugin Store community"
HOME = "https://github.com/ctrl-mietze/DIOXAMINE-plugin-store"
UPDATED = "2026-09-25T00:00:00Z"

def S(pid,name,de,desc,desc_de,category,access="standard",perms=None,mode="actions",actions=None,installable=True,fullscreen=False):
    return dict(id=pid,name=name,de=de,desc=desc,desc_de=desc_de,category=category,access=access,
                perms=perms or {},mode=mode,actions=actions or [],installable=installable,fullscreen=fullscreen)

specs = [
S("community.dioxamine.deviceinspector","Device Inspector Pro","Geräte-Inspector Pro",
  "Comprehensive ADB device information dashboard with build, kernel, memory, storage, battery and thermal diagnostics.",
  "Umfassendes ADB-Geräte-Dashboard für Build, Kernel, Speicher, Akku und Temperaturdiagnose.","Device",perms={"adb":["shell"]},
  actions=[
    ("Overview","shell","echo \"Model: $(getprop ro.product.model)\"; echo \"Manufacturer: $(getprop ro.product.manufacturer)\"; echo \"Product: $(getprop ro.product.name)\"; echo \"Android: $(getprop ro.build.version.release) (API $(getprop ro.build.version.sdk))\"; echo \"Security patch: $(getprop ro.build.version.security_patch)\"; echo \"ABI: $(getprop ro.product.cpu.abi)\"; echo \"Bootloader: $(getprop ro.bootloader)\"; echo \"Fingerprint: $(getprop ro.build.fingerprint)\"; echo; uname -a; uptime"),
    ("CPU / RAM","shell","echo '=== CPU ==='; cat /proc/cpuinfo | head -80; echo; echo '=== RAM ==='; cat /proc/meminfo | head -40"),
    ("Storage / Battery","shell","echo '=== STORAGE ==='; df -h /data /sdcard 2>/dev/null; echo; echo '=== BATTERY ==='; dumpsys battery"),
    ("Thermal","shell","for z in /sys/class/thermal/thermal_zone*; do [ -r \"$z/type\" ] || continue; printf '%s: ' \"$(cat \"$z/type\" 2>/dev/null)\"; cat \"$z/temp\" 2>/dev/null; done | head -80")]),
S("community.dioxamine.logcatpro","Logcat Pro","Logcat Pro",
  "Real-time Logcat viewer with search, pause, filtering and crash-focused views.",
  "Echtzeit-Logcat mit Suche, Pause, Filtern und Crash-Ansicht.","Developer",perms={"adb":["shell"]},mode="logcat",fullscreen=True),
S("community.dioxamine.securityaudit","Android Security Audit","Android Sicherheits-Audit",
  "Read-focused Android security diagnostics for patch level, SELinux, verified boot, debugging and security-relevant properties.",
  "Lesender Android-Sicherheitscheck für Patchlevel, SELinux, Verified Boot, Debugging und relevante Properties.","Security",perms={"adb":["shell"]},
  actions=[
    ("Security summary","shell","echo \"Patch: $(getprop ro.build.version.security_patch)\"; echo \"Android: $(getprop ro.build.version.release)\"; echo \"Build type: $(getprop ro.build.type)\"; echo \"Debuggable: $(getprop ro.debuggable)\"; echo \"Secure: $(getprop ro.secure)\"; echo \"SELinux: $(getenforce 2>/dev/null)\"; echo \"Verified boot: $(getprop ro.boot.verifiedbootstate)\"; echo \"Device state: $(getprop ro.boot.vbmeta.device_state)\"; echo \"Flash locked: $(getprop ro.boot.flash.locked)\"; echo \"ADB enabled: $(settings get global adb_enabled 2>/dev/null)\"; uname -a"),
    ("Verified Boot","shell","getprop | grep -Ei 'verifiedboot|vbmeta|avb|verity|flash.locked|device_state'"),
    ("Debug / ADB","shell","getprop | grep -Ei 'debug|adb|secure|build.type|build.tags' | sort")]),
S("community.dioxamine.backuptransfer","Backup & Transfer Manager","Backup- & Transfer-Manager",
  "Transfer individual files between the DIOXAMINE host and the connected target using SAF and ADB push/pull.",
  "Dateien zwischen DIOXAMINE-Host und Android-Ziel über SAF sowie ADB Push/Pull übertragen.","Files",
  perms={"adb":["push","pull","shell"]},mode="transfer"),
S("community.dioxamine.plugindevkit","DIOXAMINE Plugin Developer Kit","DIOXAMINE Plugin Developer Kit",
  "Generate valid current plugin.json manifests and a minimal starter plugin structure.",
  "Erzeugt gültige aktuelle plugin.json-Manifeste und eine minimale Plugin-Starterstruktur.","DIOXAMINE Tools",mode="devkit"),
S("community.dioxamine.httpapitester","HTTP API Tester","HTTP API Tester",
  "Postman-style HTTP client powered by the permission-gated dioxamine.http.fetch bridge.",
  "Postman-artiger HTTP-Client über die berechtigungsgesteuerte dioxamine.http.fetch-Bridge.","Developer",
  perms={"common":["network"]},mode="http"),
S("community.dioxamine.appexplorer","App Explorer","App Explorer",
  "Search installed packages and inspect package-manager information through ordinary ADB.",
  "Installierte Pakete durchsuchen und Package-Manager-Informationen über normales ADB anzeigen.","Apps",perms={"adb":["shell"]},
  actions=[("All packages","shell","pm list packages -U"),("User packages","shell","pm list packages -3 -U"),("Disabled packages","shell","pm list packages -d -U")]),
S("community.dioxamine.workflowbuilder","ADB Workflow Builder","ADB Workflow Builder",
  "Build, save and execute reusable multi-step ADB shell workflows.",
  "Wiederverwendbare mehrstufige ADB-Workflows erstellen, speichern und ausführen.","Automation",perms={"adb":["shell"]},mode="workflow"),
S("community.dioxamine.processexplorer","Process Explorer","Prozess Explorer",
  "Refreshable process viewer with PID, UID/user, memory and process details exposed by Android.",
  "Aktualisierbarer Prozess-Viewer mit PID, UID/Benutzer, Speicher und Android-Prozessdetails.","Developer",perms={"adb":["shell"]},
  actions=[("Processes","shell","ps -A -o USER,PID,PPID,RSS,NAME,ARGS 2>/dev/null || ps -A"),("Top snapshot","shell","top -b -n 1 -m 80 2>/dev/null | head -120")]),
S("community.dioxamine.propertyexplorer","System Property Explorer","System Property Explorer",
  "Browse Android getprop output and security, boot, product and runtime properties.",
  "Android-getprop sowie Security-, Boot-, Produkt- und Runtime-Properties durchsuchen.","System",perms={"adb":["shell"]},
  actions=[("All properties","shell","getprop"),("Build / product","shell","getprop | grep -Ei 'ro.build|ro.product' | sort"),("Boot / security","shell","getprop | grep -Ei 'ro.boot|security|selinux|verified' | sort")]),
S("community.dioxamine.networkdashboard","Network Dashboard","Netzwerk Dashboard",
  "Inspect interfaces, IPv4/IPv6 addresses, routes, DNS properties and basic connectivity.",
  "Interfaces, IPv4/IPv6-Adressen, Routen, DNS-Properties und grundlegende Konnektivität anzeigen.","Network",perms={"adb":["shell"]},
  actions=[("Interfaces","shell","ip address 2>/dev/null || ifconfig 2>/dev/null"),("Routes","shell","ip -4 route; echo; ip -6 route"),("DNS","shell","getprop | grep -Ei 'dns[0-9]|private_dns'"),("Connectivity","shell","ping -c 3 -W 2 1.1.1.1 2>&1")]),
S("community.dioxamine.dpimanager","DPI & Resolution Manager","DPI- & Auflösungs-Manager",
  "Inspect and change Android display-size and density overrides with reset actions.",
  "Android-Displaygröße und DPI-Overrides anzeigen, ändern und zurücksetzen.","Display",perms={"adb":["shell"]},mode="dpi"),
S("community.dioxamine.animationtweaker","Animation Tweaker","Animations-Tweaker",
  "Inspect and configure Android window, transition and animator duration scales.",
  "Android Window-, Transition- und Animator-Skalierung anzeigen und konfigurieren.","Display",perms={"adb":["shell"]},
  actions=[("Read values","shell","for k in window_animation_scale transition_animation_scale animator_duration_scale; do echo \"$k=$(settings get global $k)\"; done"),
           ("Default 1x","shell","settings put global window_animation_scale 1; settings put global transition_animation_scale 1; settings put global animator_duration_scale 1"),
           ("Fast 0.5x","shell","settings put global window_animation_scale .5; settings put global transition_animation_scale .5; settings put global animator_duration_scale .5"),
           ("Animations off","shell","settings put global window_animation_scale 0; settings put global transition_animation_scale 0; settings put global animator_duration_scale 0")]),
S("community.dioxamine.largefilefinder","Large File Finder","Große-Dateien-Finder",
  "Analyze accessible target storage and list the largest files and directories without deleting anything.",
  "Zugänglichen Zielspeicher analysieren und die größten Dateien und Ordner anzeigen, ohne etwas zu löschen.","Files",perms={"adb":["shell"]},
  actions=[("Largest in /sdcard","shell","du -ak /sdcard 2>/dev/null | sort -n | tail -n 120"),("Downloads","shell","du -ak /sdcard/Download 2>/dev/null | sort -n | tail -n 100"),("DCIM","shell","du -ak /sdcard/DCIM 2>/dev/null | sort -n | tail -n 100")]),
S("community.dioxamine.stayawake","Stay Awake Manager","Stay-Awake-Manager",
  "Inspect and configure Android stay-awake-while-plugged-in behavior with presets.",
  "Android Stay-Awake-bei-Stromversorgung anzeigen und mit Presets konfigurieren.","Display",perms={"adb":["shell"]},
  actions=[("Read state","shell","settings get global stay_on_while_plugged_in"),("Off","shell","settings put global stay_on_while_plugged_in 0"),("USB + AC","shell","settings put global stay_on_while_plugged_in 3"),("All powered modes","shell","settings put global stay_on_while_plugged_in 7")]),

S("community.dioxamine.shizu.package","ShizuPackage Manager","ShizuPackage Manager",
  "Shizuku-powered host package management for supported package operations.",
  "Shizuku-basierte Paketverwaltung auf dem Host für unterstützte Paketaktionen.","Apps","shizuku",mode="shizuku",installable=False),
S("community.dioxamine.shizu.permissions","ShizuPermission & AppOps Manager","ShizuPermission & AppOps Manager",
  "Combined Shizuku runtime-permission and AppOps management interface.",
  "Kombinierte Shizuku-Verwaltung von Runtime-Permissions und AppOps.","Permissions","shizuku",mode="shizuku",installable=False),
S("community.dioxamine.shizu.debloater","ShizuDebloater","ShizuDebloater",
  "Reversible Shizuku system-app management with restore-oriented workflows.",
  "Reversible Shizuku-Systemapp-Verwaltung mit Wiederherstellungs-Workflows.","Apps","shizuku",mode="shizuku",installable=False),
S("community.dioxamine.shizu.components","ShizuComponent Manager","ShizuComponent Manager",
  "Inspect and manage supported app components through a future native Shizuku bridge.",
  "Unterstützte App-Komponenten über eine zukünftige native Shizuku-Bridge untersuchen und verwalten.","Apps","shizuku",mode="shizuku",installable=False),
S("community.dioxamine.shizu.capabilities","Shizuku Capability Matrix","Shizuku Capability Matrix",
  "Determine which Shizuku-backed privileged operations are available on the host.",
  "Ermittelt, welche Shizuku-basierten privilegierten Operationen auf dem Host verfügbar sind.","Diagnostics","shizuku",mode="shizuku",installable=False),

S("community.dioxamine.root.wakelockhunter","WakeLock Hunter","WakeLock Hunter",
  "Root-assisted wakeup-source and wakelock diagnostics.","Root-gestützte Wakeup-Source- und Wakelock-Diagnose.","Battery","root",{"adb":["shell"]},
  actions=[("Wakeup sources","root","cat /sys/kernel/debug/wakeup_sources 2>/dev/null || cat /d/wakeup_sources 2>/dev/null || cat /proc/wakelocks 2>/dev/null || echo unavailable"),("Suspend stats","root","cat /sys/kernel/debug/suspend_stats 2>/dev/null || cat /sys/power/suspend_stats 2>/dev/null || echo unavailable")]),
S("community.dioxamine.root.bootanalyzer","Boot Performance Analyzer","Boot Performance Analyzer",
  "Root-assisted boot diagnostics using init states, boot properties and logs.","Root-gestützte Boot-Diagnose über Init-Status, Boot-Properties und Logs.","System","root",{"adb":["shell"]},
  actions=[("Boot properties","root","getprop | grep -E '\\[ro.boottime\\.|\\[init.svc\\.|boot_completed|bootanim' | sort"),("Init services","root","getprop | grep '\\[init.svc\\.' | sort"),("Boot log hints","root","logcat -b all -d -v time 2>/dev/null | grep -Ei 'boot_progress|bootanim|init:|sys.boot_completed' | tail -400")]),
S("community.dioxamine.root.ebpfmonitor","eBPF System Monitor","eBPF System Monitor",
  "Capability-aware inspection of eBPF filesystem and kernel support.","Capability-bewusste Untersuchung von eBPF-Dateisystem und Kernel-Unterstützung.","Kernel","root",{"adb":["shell"]},
  actions=[("Capability check","root","echo Kernel: $(uname -r); mount | grep -E 'bpf|tracefs'; ls -la /sys/fs/bpf 2>/dev/null; command -v bpftool >/dev/null && bpftool feature probe 2>&1 | head -250 || echo 'bpftool not installed'"),("Pinned objects","root","find /sys/fs/bpf -maxdepth 4 2>/dev/null | head -500")]),
S("community.dioxamine.root.irqinspector","IRQ & Interrupt Inspector","IRQ- & Interrupt-Inspector",
  "Visualize interrupt and softirq counters on rooted Android devices.","Visualisiert Interrupt- und SoftIRQ-Zähler auf gerooteten Android-Geräten.","Kernel","root",{"adb":["shell"]},
  actions=[("Interrupts","root","cat /proc/interrupts"),("SoftIRQs","root","cat /proc/softirqs")]),
S("community.dioxamine.root.cgroups","Cgroup Explorer","Cgroup Explorer",
  "Browse Android/Linux cgroup hierarchy, controllers and process assignments.","Durchsucht Android/Linux-Cgroup-Hierarchie, Controller und Prozesszuordnungen.","Kernel","root",{"adb":["shell"]},
  actions=[("Cgroup mounts","root","mount | grep -E 'cgroup|cgroup2'; echo; cat /proc/cgroups"),("Hierarchy","root","find /sys/fs/cgroup -maxdepth 3 -type d 2>/dev/null | head -500"),("PID 1 cgroup","root","cat /proc/1/cgroup")]),
S("community.dioxamine.root.blockio","Block I/O Analyzer","Block-I/O-Analyzer",
  "Inspect Linux block-device and disk I/O counters.","Untersucht Linux-Blockgeräte und Disk-I/O-Zähler.","Performance","root",{"adb":["shell"]},
  actions=[("Disk stats","root","cat /proc/diskstats"),("Block devices","root","ls -l /dev/block/by-name 2>/dev/null; echo; lsblk 2>/dev/null || cat /proc/partitions"),("Sysfs stats","root","for f in /sys/block/*/stat; do printf '%s: ' \"$f\"; cat \"$f\"; done")]),
S("community.dioxamine.root.taskengine","Root Task Engine","Root Task Engine",
  "Create and run explicitly approved reusable root command workflows.","Explizit bestätigte wiederverwendbare Root-Befehlsabläufe erstellen und ausführen.","Automation","root",{"adb":["shell"]},mode="rootworkflow")
]

CSS = """
*{box-sizing:border-box}html,body{margin:0;min-height:100%;background:var(--dioxamine-bg,#121212);color:var(--dioxamine-fg,#fff);font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif}
body{padding:16px}main{max-width:900px;margin:auto}h1{font-size:22px;margin:0}.muted{color:var(--dioxamine-on-surface-variant,#aaa)}
.card{background:var(--dioxamine-card-bg,#1e1e1e);border:1px solid var(--dioxamine-outline-variant,#333);border-radius:14px;padding:14px;margin:12px 0}
.row,.actions{display:flex;gap:8px;flex-wrap:wrap}.actions button{flex:1 1 140px}
button,input,select,textarea{font:inherit;border-radius:10px;border:1px solid var(--dioxamine-outline-variant,#444);padding:10px;background:var(--dioxamine-surface-variant,#252525);color:var(--dioxamine-fg,#fff)}
button{font-weight:650;cursor:pointer}button.primary{background:var(--dioxamine-accent,#448aff);color:var(--dioxamine-on-primary,#fff);border-color:transparent}button:disabled{opacity:.5}
input,select,textarea{width:100%}textarea{min-height:130px;font-family:monospace}pre{white-space:pre-wrap;word-break:break-word;background:var(--dioxamine-bg,#111);border:1px solid var(--dioxamine-outline-variant,#333);padding:12px;border-radius:10px;max-height:60vh;overflow:auto}
.badge{display:inline-flex;padding:5px 9px;border-radius:999px;border:1px solid var(--dioxamine-outline-variant,#444);font-size:12px}.status{font:12px monospace}
label{display:block;font-weight:650;font-size:13px;margin:8px 0 4px}
"""

BRIDGE = """
const D=()=>window.dioxamine||window.Dioxamine,$=s=>document.querySelector(s);
function ready(fn){if(D()&&window.__dioxamine_bridge_ready)fn();else window.addEventListener('dioxamine-bridge-ready',fn,{once:true})}
async function shell(c){if(!D()?.adb?.shellExec)throw Error('ADB shell bridge unavailable');return await D().adb.shellExec(c)}
function q(s){return "'"+String(s).replace(/'/g,"'\\\"'\\\"'")+"'"}
async function root(c){return await shell('su -c '+q(c))}
function out(x){$('#out').textContent=String(x??'')}function st(x){$('#status').textContent=String(x??'')}
async function execAction(type,cmd){st('running…');try{const r=await (type==='root'?root(cmd):shell(cmd));out((r.stdout||'')+(r.stderr?'\\n[stderr]\\n'+r.stderr:''));st('exit '+r.exitCode)}catch(e){out(e.message||e);st('error')}}
"""

def manifest(s):
    return {"schemaVersion":1,"id":s["id"],"name":s["name"],"description":s["desc"][:200],"version":"0.1.0","versionCode":1,
            "author":AUTHOR,"entry":"index.html","icon":"icon.svg","minAppVersionCode":1,"permissions":s["perms"],
            "fullscreen":s["fullscreen"],"homepage":HOME}

def icon(s):
    a=html.escape(s["access"].upper()); n=html.escape(s["name"][0].upper())
    return '<svg xmlns="http://www.w3.org/2000/svg" width="512" height="512" viewBox="0 0 512 512"><rect x="24" y="24" width="464" height="464" rx="112" fill="none" stroke="currentColor" stroke-width="26"/><text x="256" y="290" text-anchor="middle" font-family="sans-serif" font-size="190" font-weight="800" fill="currentColor">'+n+'</text><text x="256" y="420" text-anchor="middle" font-family="sans-serif" font-size="38" font-weight="700" fill="currentColor">'+a+'</text></svg>'

def body_and_js(s):
    mode=s["mode"]
    if mode=="actions":
        buttons="".join('<button data-i="'+str(i)+'">'+html.escape(a[0])+'</button>' for i,a in enumerate(s["actions"]))
        body='<section class="card"><div class="actions">'+buttons+'</div></section><section class="card"><pre id="out">Select an action.</pre></section>'
        js="const ACTIONS="+json.dumps(s["actions"])+";function init(){st('ready');document.querySelectorAll('[data-i]').forEach(b=>b.onclick=()=>{const a=ACTIONS[+b.dataset.i];execAction(a[1],a[2])})}"
        return body,js
    if mode=="logcat":
        body='<section class="card"><input id="search" placeholder="Search logs…"><div class="actions"><button class="primary" id="start">Start</button><button id="pause">Pause</button><button id="clear">Clear</button></div></section><section class="card"><pre id="out"></pre></section>'
        js="""let ses=null,paused=false,lines=[],pending=[],timer=null;function draw(){timer=null;lines.push(...pending.splice(0));if(lines.length>2500)lines=lines.slice(-2500);const q=$('#search').value.toLowerCase();out(lines.filter(x=>!q||x.toLowerCase().includes(q)).slice(-1000).join('\\n'))}function queue(t){if(paused)return;pending.push(...t.split(/\\r?\\n/).filter(Boolean));if(!timer)timer=setTimeout(draw,60)}async function start(){if(ses)return;ses=await D().adb.openInteractiveShell();ses.onData(b=>queue(D().base64ToUtf8(b)));ses.onClose(()=>{ses=null;st('closed')});await ses.write(D().utf8ToBase64('logcat -v time -T 50\\n'));st('streaming')}function init(){st('ready');$('#start').onclick=start;$('#pause').onclick=()=>{paused=!paused;$('#pause').textContent=paused?'Resume':'Pause'};$('#clear').onclick=()=>{lines=[];pending=[];draw()};$('#search').oninput=draw;start()}"""
        return body,js
    if mode=="http":
        body='<section class="card"><label>Method</label><select id="method"><option>GET</option><option>POST</option><option>PUT</option><option>PATCH</option><option>DELETE</option><option>HEAD</option></select><label>URL</label><input id="url" value="https://api.github.com/repos/rhythmcache/Dioxamine"><label>Headers JSON</label><textarea id="headers">{"Accept":"application/vnd.github+json"}</textarea><label>Body</label><textarea id="body"></textarea><button class="primary" id="send">Send</button></section><section class="card"><pre id="out"></pre></section>'
        js="""async function send(){st('requesting…');try{const h=JSON.parse($('#headers').value||'{}'),o={method:$('#method').value,headers:h,timeoutMs:20000};if(!['GET','HEAD'].includes(o.method))o.body=$('#body').value;const r=await D().http.fetch($('#url').value.trim(),o);let d=r.data||'';try{d=JSON.stringify(JSON.parse(d),null,2)}catch(_){}out(r.status+' '+r.statusText+'\\n\\n'+JSON.stringify(r.headers||{},null,2)+'\\n\\n'+d);st('done')}catch(e){out(e.message||e);st('error')}}function init(){st('ready');$('#send').onclick=send}"""
        return body,js
    if mode in ("workflow","rootworkflow"):
        body='<section class="card"><label>Commands — one per line</label><textarea id="cmds">getprop ro.product.model\\nuname -r\\nid</textarea><button class="primary" id="run">Run workflow</button></section><section class="card"><pre id="out"></pre></section>'
        fun="root" if mode=="rootworkflow" else "shell"
        js="async function run(){let l='';for(const c of $('#cmds').value.split(/\\r?\\n/).map(x=>x.trim()).filter(Boolean)){l+='\\n$ '+c+'\\n';out(l);const r=await "+fun+"(c);l+=(r.stdout||'')+(r.stderr||'')+'\\n[exit '+r.exitCode+']\\n';out(l);if(r.exitCode!==0)break}st('finished')}function init(){st('ready');$('#run').onclick=run}"
        return body,js
    if mode=="transfer":
        body='<section class="card"><label>Remote path to pull</label><input id="pullPath" value="/sdcard/Download/example.txt"><button class="primary" id="pull">Choose host destination & pull</button><label>Remote destination for push</label><input id="pushPath" value="/sdcard/Download/upload.bin"><button class="primary" id="push">Choose host file & push</button></section><section class="card"><pre id="out"></pre></section>'
        js="""async function pull(){try{const p=await D().requestFilePicker('create'),r=await D().adb.pull($('#pullPath').value.trim(),p.requestId);out('Pulled '+r.bytesTransferred+' bytes')}catch(e){out(e.message||e)}}async function push(){try{const p=await D().requestFilePicker('open'),r=await D().adb.push(p.requestId,$('#pushPath').value.trim());out('Pushed '+r.bytesTransferred+' bytes')}catch(e){out(e.message||e)}}function init(){st('ready');$('#pull').onclick=pull;$('#push').onclick=push}"""
        return body,js
    if mode=="dpi":
        body='<section class="card"><label>Resolution</label><input id="size" placeholder="1080x2400"><label>Density</label><input id="dpi" placeholder="420"><div class="actions"><button class="primary" id="setSize">Set size</button><button class="primary" id="setDpi">Set density</button><button id="resetSize">Reset size</button><button id="resetDpi">Reset density</button><button id="read">Read current</button></div></section><section class="card"><pre id="out"></pre></section>'
        js="""async function read(){const a=await shell('wm size'),b=await shell('wm density');out(a.stdout+'\\n'+b.stdout)}function init(){st('ready');$('#read').onclick=read;$('#setSize').onclick=async()=>{const v=$('#size').value.trim();if(!/^\\d{3,5}x\\d{3,5}$/.test(v))return out('Invalid size');await shell('wm size '+v);read()};$('#setDpi').onclick=async()=>{const v=$('#dpi').value.trim();if(!/^\\d{2,4}$/.test(v))return out('Invalid density');await shell('wm density '+v);read()};$('#resetSize').onclick=async()=>{await shell('wm size reset');read()};$('#resetDpi').onclick=async()=>{await shell('wm density reset');read()};read()}"""
        return body,js
    if mode=="devkit":
        body='<section class="card"><label>Plugin ID</label><input id="pid" value="com.example.myplugin"><label>Name</label><input id="name" value="My Plugin"><label>Description</label><input id="desc" value="My DIOXAMINE plugin"><label>Author</label><input id="author" value="Your Name"><button class="primary" id="gen">Generate</button></section><section class="card"><pre id="out"></pre></section>'
        js="""function gen(){const id=$('#pid').value.trim();if(!/^[a-z0-9]+(\\.[a-z0-9_]+)+$/.test(id))return out('Invalid reverse-DNS plugin ID');const m={schemaVersion:1,id,name:$('#name').value.trim(),description:$('#desc').value.trim().slice(0,200),version:'1.0.0',versionCode:1,author:$('#author').value.trim(),entry:'index.html',minAppVersionCode:1,permissions:{},fullscreen:false};out('plugin.json\\n-----------\\n'+JSON.stringify(m,null,2)+'\\n\\nindex.html\\n----------\\n<!doctype html>\\n<html><head><meta name=\"viewport\" content=\"width=device-width,initial-scale=1\"><title>'+m.name+'</title></head><body><main>'+m.name+'</main></body></html>\\n\\nZIP the contents so plugin.json is at archive root.')}function init(){st('ready');$('#gen').onclick=gen;gen()}"""
        return body,js
    if mode=="shizuku":
        body='<section class="card"><h2>Native Shizuku bridge required</h2><p>The checked DIOXAMINE Git source does not currently expose Shizuku/rish to WebView plugins. This package is intentionally not pretending that normal ADB is Shizuku.</p><p class="muted">Status: requires-native-bridge</p></section><section class="card"><pre id="out">Not installable from the Community Store until a documented, permission-gated Shizuku bridge exists.</pre></section>'
        return body,"function init(){st('requires-native-bridge')}"
    raise ValueError(mode)

def make_html(s):
    body,js=body_and_js(s)
    return "<!doctype html><html><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1,user-scalable=no'><title>"+html.escape(s["name"])+"</title><style>"+CSS+"</style></head><body><main><h1>"+html.escape(s["name"])+"</h1><p class='muted'>"+html.escape(s["desc"])+"</p><div class='row'><span class='badge'>"+html.escape(s["access"].upper())+"</span><span class='status' id='status'>waiting…</span></div>"+body+"</main><script>"+BRIDGE+js+";ready(init);</script></body></html>"

catalogue=[]
for s in specs:
    d=PLUGINS/s["id"]; d.mkdir(parents=True,exist_ok=True)
    m=manifest(s); ix=make_html(s); ic=icon(s)
    (d/"plugin.json").write_text(json.dumps(m,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    (d/"index.html").write_text(ix,encoding="utf-8")
    (d/"icon.svg").write_text(ic,encoding="utf-8")
    (d/"README.md").write_text("# "+s["name"]+"\n\n**Access:** "+s["access"]+"\n\n"+s["desc"]+"\n\n## Deutsch\n\n"+s["desc_de"]+"\n\n**Status:** "+("requires-native-bridge" if not s["installable"] else "installable MVP")+"\n",encoding="utf-8")
    z=d/"plugin.zip"
    with zipfile.ZipFile(z,"w",zipfile.ZIP_DEFLATED) as f:
        f.writestr("plugin.json",json.dumps(m,indent=2,ensure_ascii=False)+"\n")
        f.writestr("index.html",ix); f.writestr("icon.svg",ic)
    sha=hashlib.sha256(z.read_bytes()).hexdigest()
    catalogue.append({"id":s["id"],"name":{"en":s["name"],"de":s["de"]},"description":{"en":s["desc"],"de":s["desc_de"]},
      "author":AUTHOR,"version":"0.1.0","versionCode":1,"category":s["category"],"accessLevel":s["access"],
      "status":"mvp" if s["installable"] else "requires-native-bridge","installable":s["installable"],
      "package":"plugins/"+s["id"]+"/plugin.zip","sha256":sha,"icon":"plugins/"+s["id"]+"/icon.svg",
      "source":HOME+"/tree/main/plugins/"+s["id"],"license":"MIT","minDioxamineVersionCode":1,
      "compatibility":{"minVersion":"current plugin API","minVersionCode":1,"testedVersions":[]},"permissions":s["perms"],
      "updatedAt":UPDATED,"changelog":{"en":"Initial community MVP.","de":"Erstes Community-MVP."},"tags":[s["access"],s["category"].lower()]})

(ROOT/"catalogue"/"plugins.json").write_text(json.dumps({"schemaVersion":1,"catalogueVersion":2,"updatedAt":UPDATED,"repository":HOME,"plugins":catalogue},indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
schema_path=ROOT/"catalogue"/"schema.json"
schema=json.loads(schema_path.read_text(encoding="utf-8"))
p=schema["$defs"]["plugin"]["properties"]
p["accessLevel"]={"type":"string","enum":["standard","shizuku","root"]}; p["status"]={"type":"string"}; p["installable"]={"type":"boolean"}; p["tags"]={"type":"array","items":{"type":"string"}}
schema_path.write_text(json.dumps(schema,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
(ROOT/"plugins"/"README.md").write_text("# DIOXAMINE Community Plugin Collection\n\n- **standard**: current documented DIOXAMINE APIs / ADB / SAF / HTTP\n- **root**: current ADB shell bridge plus explicit su -c on a rooted connected target\n- **shizuku**: host-side Shizuku concepts; currently requires-native-bridge\n\nEvery folder contains source plus plugin.zip with plugin.json at ZIP root.\n",encoding="utf-8")
bd=ROOT/"docs"/"bridge-requirements"; bd.mkdir(parents=True,exist_ok=True)
(bd/"shizuku.md").write_text("# Shizuku plugin bridge requirement\n\nThe checked ctrl-mietze/Dioxamine and upstream source currently expose no documented Shizuku/rish namespace to WebView plugins.\n\nThe five Shizuku packages are therefore marked requires-native-bridge and installable: false rather than silently relabelling normal ADB as Shizuku.\n\nA future bridge should integrate native Shizuku authorization, add explicit manifest permission validation and expose narrowly scoped permission-gated host operations before these plugins are enabled.\n",encoding="utf-8")
inv=["# Plugin inventory","","## Standard"]+[f"- {x['name']} — {x['category']}" for x in specs if x["access"]=="standard"]+["","## Shizuku"]+[f"- {x['name']} — {x['category']} — requires native bridge" for x in specs if x["access"]=="shizuku"]+["","## Root"]+[f"- {x['name']} — {x['category']}" for x in specs if x["access"]=="root"]
(ROOT/"docs"/"plugin-inventory.md").write_text("\n".join(inv)+"\n",encoding="utf-8")
print("generated",len(specs),"plugins")

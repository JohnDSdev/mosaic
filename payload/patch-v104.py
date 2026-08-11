from pathlib import Path
import re, sys

path = Path(sys.argv[1])
s = path.read_text()

# Add editor metadata, editable todo text, and settings toggle styles.
css_anchor = '.editor .todo-item{display:flex;align-items:flex-start;gap:10px;margin:5px 0}.editor .todo-item input{margin-top:8px;width:18px;height:18px;accent-color:var(--page-accent,#7c9cff)}.editor .todo-item.done span{text-decoration:line-through;opacity:.55}'
css_new = '.editor .todo-item{display:flex;align-items:flex-start;gap:10px;margin:5px 0;min-height:1.65em}.editor .todo-item input{margin-top:7px;width:18px;height:18px;flex:0 0 auto;accent-color:var(--page-accent,#7c9cff)}.editor .todo-item .todo-text{flex:1;min-width:1ch;min-height:1.65em;outline:0}.editor .todo-item.done .todo-text{text-decoration:line-through;opacity:.55}'
if css_anchor not in s:
    raise SystemExit('todo CSS anchor missing')
s = s.replace(css_anchor, css_new, 1)

save_anchor = '.saveState{padding:8px 26px 16px;color:var(--muted);font-size:12px}'
save_new = '.saveState{color:var(--muted);font-size:12px}.editorMeta{display:flex;align-items:center;gap:8px;margin-top:7px;color:var(--muted);font-size:12px}.editorMeta .metaDot{opacity:.5}.toggleRow{display:flex;align-items:center;justify-content:space-between;gap:18px;padding:11px 0}.toggleRow+.toggleRow{border-top:1px solid #ffffff10}.toggleCopy{min-width:0}.toggleCopy strong{margin:0 0 3px}.toggle{appearance:none;-webkit-appearance:none;width:46px!important;height:27px!important;flex:0 0 auto!important;border:0!important;border-radius:999px!important;background:#494950!important;padding:0!important;position:relative;cursor:pointer;transition:background .16s ease}.toggle:before{content:"";position:absolute;width:21px;height:21px;border-radius:50%;left:3px;top:3px;background:#f5f5f7;transition:transform .16s ease}.toggle:checked{background:var(--accent)!important}.toggle:checked:before{transform:translateX(19px)}.toggle:focus,.toggle:focus-visible{outline:none;box-shadow:none}'
if save_anchor not in s:
    raise SystemExit('save CSS anchor missing')
s = s.replace(save_anchor, save_new, 1)

# On phones, keep the editor toolbar directly above the soft keyboard.
mobile_old = '@media(max-width:700px){.topbar{height:70px;padding:10px 10px}.brand{display:none}.crumb span{max-width:95px}.searchWrap{height:48px;padding:0 13px}.searchWrap input{font-size:16px}.main{padding:16px 14px}.grid{grid-template-columns:repeat(2,minmax(0,1fr));gap:12px}.card{min-height:150px;padding:16px;border-radius:19px}.cardTitle{font-size:17px}.cardPreview{font-size:13px}.pageTitleRow h1{font-size:27px}.editorShell{border-radius:0;border-left:0;border-right:0;margin:-16px -14px;height:calc(100% + 32px)}.editorHead{padding:18px 18px 8px}.titleInput{font-size:29px}.toolbar{padding:8px 10px;gap:3px;overflow-x:auto;flex-wrap:nowrap}.editor{padding:22px 19px 100px;font-size:17px}.saveState{padding-left:19px}.fab{width:62px;height:62px;border-radius:20px}.topActions .hideMobile{display:none}}'
mobile_new = '@media(max-width:700px){#app{height:var(--visual-height,100%)}.topbar{height:70px;padding:10px 10px}.brand{display:none}.crumb span{max-width:95px}.searchWrap{height:48px;padding:0 13px}.searchWrap input{font-size:16px}.main{padding:16px 14px}.grid{grid-template-columns:repeat(2,minmax(0,1fr));gap:12px}.card{min-height:150px;padding:16px;border-radius:19px}.cardTitle{font-size:17px}.cardPreview{font-size:13px}.pageTitleRow h1{font-size:27px}.editorShell{border-radius:0;border-left:0;border-right:0;margin:-16px -14px;height:calc(100% + 32px)}.editorHead{padding:18px 18px 10px}.editorMeta{margin-top:5px}.titleInput{font-size:29px}.toolbar{position:fixed;left:0;right:0;top:auto;bottom:calc(env(safe-area-inset-bottom,0px) + var(--keyboard-inset,0px));z-index:80;padding:8px 10px;gap:4px;overflow-x:auto;flex-wrap:nowrap;border-top:1px solid #ffffff18;border-bottom:0;background:#1b1b1ef7;box-shadow:0 -8px 26px #0005;backdrop-filter:blur(14px);-webkit-backdrop-filter:blur(14px);scrollbar-width:none;-webkit-overflow-scrolling:touch}.toolbar::-webkit-scrollbar{display:none}.tool{width:44px;min-width:44px;height:44px}.editor{padding:22px 19px 92px;font-size:17px;scroll-padding-bottom:92px}.fab{width:62px;height:62px;border-radius:20px}.topActions .hideMobile{display:none}}'
if mobile_old not in s:
    raise SystemExit('mobile CSS anchor missing')
s = s.replace(mobile_old, mobile_new, 1)

# Preferences, navigation persistence, word counting, animations, and keyboard metrics.
var_anchor = "let config=null,state=null,baseState=null,view={type:'home'},activePageId=null,saveTimer=null,syncTimer=null,syncing=false,lastEditorHTML='';"
helpers = r'''let config=null,state=null,baseState=null,view={type:'home'},activePageId=null,saveTimer=null,syncTimer=null,syncing=false,lastEditorHTML='';
const VIEW_KEY='mosaic_notes_last_view_v1';
function ensurePrefs(){if(!config)return;config.preferences=config.preferences||{};if(typeof config.preferences.spellcheck!=='boolean')config.preferences.spellcheck=true;if(typeof config.preferences.animations!=='boolean')config.preferences.animations=true}
function pref(name,fallback=true){const v=config?.preferences?.[name];return typeof v==='boolean'?v:fallback}
function viewDepth(v){return v?.type==='editor'?3:v?.type==='pages'?2:v?.type==='sections'?1:0}
function saveViewState(){try{localStorage.setItem(VIEW_KEY,JSON.stringify(view))}catch{}}
function restoreViewState(){try{const v=JSON.parse(localStorage.getItem(VIEW_KEY)||'null');if(!v||!v.type)return {type:'home'};if(v.type==='editor'&&state.pages[v.pageId]&&!state.pages[v.pageId].deleted)return v;if(v.type==='pages'&&state.sections[v.sectionId]&&!state.sections[v.sectionId].deleted&&state.notebooks[v.notebookId]&&!state.notebooks[v.notebookId].deleted)return v;if(v.type==='sections'&&state.notebooks[v.notebookId]&&!state.notebooks[v.notebookId].deleted)return v}catch{}return {type:'home'}}
function animationsEnabled(){return pref('animations',true)&&!window.matchMedia?.('(prefers-reduced-motion: reduce)').matches}
function animateView(from,to){if(!animationsEnabled()||!main.animate)return;const d=viewDepth(to)-viewDepth(from),x=d===0?0:(d>0?14:-14);main.animate([{opacity:.45,transform:`translateX(${x}px) scale(.995)`},{opacity:1,transform:'translateX(0) scale(1)'}],{duration:180,easing:'cubic-bezier(.2,.8,.2,1)'})}
function caretInto(el){if(!el)return;const r=document.createRange(),sel=window.getSelection();r.selectNodeContents(el);r.collapse(false);sel.removeAllRanges();sel.addRange(r);el.closest?.('[contenteditable="true"]')?.focus()}
function closestAtCaret(selector){const sel=window.getSelection();if(!sel||!sel.rangeCount)return null;let n=sel.anchorNode;if(n?.nodeType===3)n=n.parentElement;return n?.closest?.(selector)||null}
function countWords(text=''){text=String(text).replace(/\u200b/g,' ').trim();return text?text.split(/\s+/).filter(Boolean).length:0}
function updateWordCount(){const ed=$('#editor'),out=$('#wordCount');if(!ed||!out)return;const n=countWords(ed.innerText||ed.textContent||'');out.textContent=`${n} word${n===1?'':'s'}`}
function updateViewportMetrics(){const vv=window.visualViewport;if(!vv)return;const keyboard=Math.max(0,window.innerHeight-vv.height-vv.offsetTop);document.documentElement.style.setProperty('--keyboard-inset',keyboard+'px');document.documentElement.style.setProperty('--visual-height',vv.height+'px')}
window.visualViewport?.addEventListener('resize',updateViewportMetrics);window.visualViewport?.addEventListener('scroll',updateViewportMetrics);window.addEventListener('resize',updateViewportMetrics);updateViewportMetrics();'''
if var_anchor not in s:
    raise SystemExit('var anchor missing')
s = s.replace(var_anchor, helpers, 1)

load_old = "async function loadPersisted(){try{await store.open()}catch(e){console.warn('IndexedDB unavailable, using localStorage',e)}config=await store.get('config');if(!config)return false;try{const e=await store.get('state');state=e?await decryptObj(e,keyBytes(),'local-state-v1'):blankState();const b=await store.get('base');baseState=b?await decryptObj(b,keyBytes(),'local-base-v1'):clone(state);return true}catch(e){console.error(e);return false}}"
load_new = "async function loadPersisted(){try{await store.open()}catch(e){console.warn('IndexedDB unavailable, using localStorage',e)}config=await store.get('config');if(!config)return false;ensurePrefs();try{const e=await store.get('state');state=e?await decryptObj(e,keyBytes(),'local-state-v1'):blankState();const b=await store.get('base');baseState=b?await decryptObj(b,keyBytes(),'local-base-v1'):clone(state);await store.set('config',config);return true}catch(e){console.error(e);return false}}"
if load_old not in s:
    raise SystemExit('loadPersisted anchor missing')
s=s.replace(load_old,load_new,1)

setview_old = "function setView(v){saveCurrentEditor();view=v;activePageId=v.type==='editor'?v.pageId:null;searchInput.value='';clearSearch.classList.add('hidden');render()}"
setview_new = "function setView(v){saveCurrentEditor();const old=view;view=v;activePageId=v.type==='editor'?v.pageId:null;saveViewState();searchInput.value='';clearSearch.classList.add('hidden');render();animateView(old,v)}"
if setview_old not in s:
    raise SystemExit('setView anchor missing')
s=s.replace(setview_old,setview_new,1)

# Replace the page editor behavior while retaining the current SVG icon bar.
editor_pattern = re.compile(r"function renderEditor\(pid\)\{.*?\}\nfunction queueEditorSave\(\)\{.*?\}\nasync function saveCurrentEditor\(schedule=true\)\{.*?\}\n", re.S)
m = editor_pattern.search(s)
if not m:
    raise SystemExit('editor function block missing')
new_editor = r'''function renderEditor(pid){const p=state.pages[pid];if(!p||p.deleted)return setView({type:'pages',notebookId:view.notebookId,sectionId:view.sectionId});main.innerHTML=`<div class="editorShell" style="--page-accent:${p.color}"><div class="editorAccent"></div><div class="editorHead"><input class="titleInput" id="pageTitle" value="${esc(p.title)}" placeholder="Untitled page"><div class="editorMeta"><span class="saveState" id="saveState">Saved locally</span><span class="metaDot">•</span><span id="wordCount">0 words</span></div></div><div class="toolbar">
<button class="tool" data-cmd="bold" title="Bold"><svg class="icon" viewBox="0 0 24 24"><path d="M8 5h5a3.5 3.5 0 0 1 0 7H8z"/><path d="M8 12h6a3.5 3.5 0 0 1 0 7H8z"/></svg></button><button class="tool" data-cmd="italic" title="Italic"><svg class="icon" viewBox="0 0 24 24"><path d="M10 5h8M6 19h8M14 5l-4 14"/></svg></button><button class="tool" data-cmd="insertUnorderedList" title="Bulleted list"><svg class="icon" viewBox="0 0 24 24"><circle class="iconFill" cx="5" cy="7" r="1.5"/><circle class="iconFill" cx="5" cy="12" r="1.5"/><circle class="iconFill" cx="5" cy="17" r="1.5"/><path d="M10 7h9M10 12h9M10 17h9"/></svg></button><button class="tool" data-cmd="insertOrderedList" title="Numbered list"><svg class="icon" viewBox="0 0 24 24"><path d="M4 6h2v5M4 11h3M4 15h3l-3 4h3M11 7h9M11 12h9M11 17h9"/></svg></button><button class="tool" id="todoTool" title="To-do"><svg class="icon" viewBox="0 0 24 24"><rect x="3.5" y="4.5" width="17" height="15" rx="2.5"/><path d="M8 12l2.5 2.5L16 9"/></svg></button><button class="tool sep" id="linkTool" title="Link"><svg class="icon" viewBox="0 0 24 24"><path d="M10 14l4-4"/><path d="M8.5 16.5l-1 1a3.5 3.5 0 0 1-5-5l3-3a3.5 3.5 0 0 1 5 0"/><path d="M15.5 7.5l1-1a3.5 3.5 0 0 1 5 5l-3 3a3.5 3.5 0 0 1-5 0"/></svg></button><button class="tool" id="imageTool" title="Image"><svg class="icon" viewBox="0 0 24 24"><rect x="3.5" y="4.5" width="17" height="15" rx="2.5"/><circle cx="9" cy="9" r="1.7"/><path d="M5.5 17l4.2-4.2 3.1 3.1 2.4-2.4 3.3 3.5"/></svg></button><button class="tool" id="htmlTool" title="HTML embed"><svg class="icon" viewBox="0 0 24 24"><path d="M8.5 7L4 12l4.5 5M15.5 7L20 12l-4.5 5M13.5 5l-3 14"/></svg></button><button class="tool" id="colorTool" title="Page color"><svg class="icon" viewBox="0 0 24 24"><circle cx="12" cy="12" r="8"/><circle class="iconFill" cx="12" cy="12" r="3.5"/></svg></button><button class="tool" data-cmd="removeFormat" title="Clear formatting"><svg class="icon" viewBox="0 0 24 24"><path d="M5 19L19 5M14 5H7l3 7M11 19h6"/></svg></button></div><div class="editor" id="editor" contenteditable="true" spellcheck="${pref('spellcheck',true)?'true':'false'}" autocapitalize="sentences">${p.content||''}</div></div>`;
 const ed=$('#editor'), title=$('#pageTitle');ed.querySelectorAll('.todo-item span').forEach(span=>{span.classList.add('todo-text');if((span.textContent||'').replace(/\u00a0/g,'').trim()==='')span.innerHTML=''});lastEditorHTML=ed.innerHTML;updateWordCount();ed.addEventListener('input',()=>queueEditorSave());title.addEventListener('input',()=>queueEditorSave());ed.addEventListener('click',e=>{const box=e.target.closest('.todo-item input');if(box){box.toggleAttribute('checked',box.checked);box.closest('.todo-item').classList.toggle('done',box.checked);queueEditorSave()}});ed.addEventListener('paste',onPaste);ed.addEventListener('keydown',e=>handleEditorKeydown(e,ed));main.querySelectorAll('[data-cmd]').forEach(b=>b.onclick=()=>{ed.focus();document.execCommand(b.dataset.cmd,false,null);queueEditorSave()});$('#todoTool').onclick=()=>insertTodo(ed);$('#linkTool').onclick=()=>insertLink(ed);$('#imageTool').onclick=()=>$('#imageInput').click();$('#htmlTool').onclick=()=>insertHtmlEmbed(ed);$('#colorTool').onclick=()=>editPageColor(p);}
function insertTodo(ed){ed.focus();const id='todo-'+uuid();document.execCommand('insertHTML',false,`<div class="todo-item" data-todo-id="${id}"><input type="checkbox" contenteditable="false"><span class="todo-text"></span></div>`);const item=ed.querySelector(`[data-todo-id="${id}"]`);if(item){item.removeAttribute('data-todo-id');requestAnimationFrame(()=>caretInto(item.querySelector('.todo-text')))}queueEditorSave()}
function makeTodo(){const item=document.createElement('div');item.className='todo-item';item.innerHTML='<input type="checkbox" contenteditable="false"><span class="todo-text"></span>';return item}
function handleEditorKeydown(e,ed){if(e.key!=='Enter')return;const todo=closestAtCaret('.todo-item');if(todo&&ed.contains(todo)){e.preventDefault();const span=todo.querySelector('.todo-text,span'),text=(span?.innerText||span?.textContent||'').replace(/\u200b/g,'').trim();if(!text){const block=document.createElement('div');block.innerHTML='<br>';todo.after(block);todo.remove();caretInto(block)}else{const next=makeTodo();todo.after(next);caretInto(next.querySelector('.todo-text'))}queueEditorSave();return}const li=closestAtCaret('li');if(li&&ed.contains(li)&&!li.nextElementSibling&&!(li.innerText||'').replace(/\u200b/g,'').trim()){e.preventDefault();const list=li.parentElement,block=document.createElement('div');block.innerHTML='<br>';list.after(block);li.remove();if(!list.querySelector('li'))list.remove();caretInto(block);queueEditorSave()}}
function queueEditorSave(){updateWordCount();const s=$('#saveState');if(s)s.textContent='Saving locally…';clearTimeout(saveTimer);saveTimer=setTimeout(()=>saveCurrentEditor(true),350)}
async function saveCurrentEditor(schedule=true){if(view.type!=='editor'||!activePageId||!state?.pages[activePageId])return;const ed=$('#editor'),title=$('#pageTitle');if(!ed||!title)return;const p=state.pages[activePageId];const html=ed.innerHTML,t=title.value.trim()||'Untitled';if(html!==p.content||t!==p.title){p.content=html;p.title=t;touch(p);await persist();const st=$('#saveState');if(st)st.textContent=navigator.onLine?'Saved locally · sync pending':'Saved locally · offline';if(schedule)scheduleSync()}else{const st=$('#saveState');if(st&&st.textContent==='Saving locally…')st.textContent='Saved locally'}}
'''
s = s[:m.start()] + new_editor + s[m.end():]

settings_pattern = re.compile(r"function settings\(\)\{openModal\(`.*?\}\)\}\nsettingsBtn\.onclick=settings;", re.S)
ms = settings_pattern.search(s)
if not ms:
    raise SystemExit('settings block missing')
new_settings = r'''function settings(){ensurePrefs();openModal(`<h2>Settings</h2><p>Mosaic is local-first. Cloudinary only receives encrypted snapshots.</p><div class="settingsList">
<div class="settingCard"><div class="toggleRow"><div class="toggleCopy"><strong>Spell check</strong><div class="subtitle">Show browser/Android spelling suggestions and underlines while editing.</div></div><input class="toggle" type="checkbox" id="spellToggle" ${pref('spellcheck',true)?'checked':''}></div><div class="toggleRow"><div class="toggleCopy"><strong>Animations</strong><div class="subtitle">Use a short slide/fade when moving between notebooks, sections, pages, and notes.</div></div><input class="toggle" type="checkbox" id="animToggle" ${pref('animations',true)?'checked':''}></div></div>
<div class="settingCard"><strong>Cloud</strong><div class="subtitle">${esc(config.cloudName)} · preset <code>${PRESET}</code></div><div class="row" style="margin-top:10px"><button class="btn" id="syncNowM">Sync now</button><button class="btn" id="cloudHelp">Cloudinary setup</button></div></div>
<div class="settingCard"><strong>Recovery key</strong><div class="subtitle">Anyone with this key can decrypt the notebook.</div><button class="btn" id="showRecovery" style="margin-top:10px">Show recovery key</button></div>
<div class="settingCard"><strong>Add another device</strong><div class="subtitle">Copy a pairing code to another device. It contains the recovery secret.</div><button class="btn" id="pairCode" style="margin-top:10px">Show pairing code</button></div>
<div class="settingCard"><strong>Backup</strong><div class="row" style="margin-top:10px"><button class="btn" id="exportBtn">Export all data</button><button class="btn" id="importBtn">Import backup</button></div></div>
<div class="settingCard"><strong>Local reset</strong><div class="subtitle">Removes this device's local key and notes. Your encrypted cloud snapshots remain.</div><button class="btn danger" id="resetBtn" style="margin-top:10px">Forget this device</button></div></div><div class="modalActions"><button class="btn primary" id="done">Done</button></div>`,()=>{$('#done').onclick=closeModal;$('#spellToggle').onchange=async e=>{config.preferences.spellcheck=e.target.checked;await store.set('config',config);const ed=$('#editor');if(ed)ed.spellcheck=e.target.checked};$('#animToggle').onchange=async e=>{config.preferences.animations=e.target.checked;await store.set('config',config)};$('#syncNowM').onclick=()=>{closeModal();syncNow()};$('#cloudHelp').onclick=cloudHelp;$('#showRecovery').onclick=showRecovery;$('#pairCode').onclick=showPairCode;$('#exportBtn').onclick=()=>{closeModal();exportData()};$('#importBtn').onclick=()=>$('#importInput').click();$('#resetBtn').onclick=confirmReset})}
settingsBtn.onclick=settings;'''
s = s[:ms.start()] + new_settings + s[ms.end():]

s = s.replace("syncError:''};state=blankState()", "syncError:'',preferences:{spellcheck:true,animations:true}};state=blankState()")

boot_old = "async function boot(){if(!crypto?.subtle){main.innerHTML=emptyHTML('Web Crypto unavailable','This browser cannot safely encrypt the vault. Use a modern browser.');return}const ok=await loadPersisted();if(ok){render();scheduleSync(1000)}else setupScreen()}"
boot_new = "async function boot(){if(!crypto?.subtle){main.innerHTML=emptyHTML('Web Crypto unavailable','This browser cannot safely encrypt the vault. Use a modern browser.');return}const ok=await loadPersisted();if(ok){view=restoreViewState();activePageId=view.type==='editor'?view.pageId:null;render();scheduleSync(1000)}else setupScreen()}"
if boot_old not in s:
    raise SystemExit('boot anchor missing')
s = s.replace(boot_old, boot_new, 1)

path.write_text(s)
print('patched', path, len(s))

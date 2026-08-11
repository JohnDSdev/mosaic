from pathlib import Path

p = Path('/tmp/mosaic-src/mosaic-notes/app/src/main/assets/index.html')
s = p.read_text()

s = s.replace('html,body{margin:0;height:100%;background:var(--bg);color:var(--text);font-family:Inter,ui-sans-serif,system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif}',
'''html,body{margin:0;height:100%;background:var(--bg);color:var(--text);font-family:Inter,ui-sans-serif,system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;overscroll-behavior:none}''')
s = s.replace('.main{flex:1;overflow:auto;', '.main{flex:1;overflow:auto;overscroll-behavior-y:contain;')
s = s.replace('.editor{flex:1;overflow:auto;', '.editor{flex:1;overflow:auto;overscroll-behavior-y:contain;')
s = s.replace('.searchResultsLabel{color:var(--muted);margin-bottom:14px}.hidden{display:none!important}',
'''.searchResultsLabel{color:var(--muted);margin-bottom:14px}.hidden{display:none!important}.main.editorMode{overflow:hidden;overscroll-behavior:none}::highlight(mosaic-spelling){text-decoration-line:underline;text-decoration-style:wavy;text-decoration-color:#ff6674;text-decoration-thickness:1.5px;text-underline-offset:3px}''')

old_mobile = '''@media(max-width:700px){#app{height:var(--visual-height,100%)}.topbar{height:70px;padding:10px 10px}.brand{display:none}.crumb span{max-width:95px}.searchWrap{height:48px;padding:0 13px}.searchWrap input{font-size:16px}.main{padding:16px 14px}.grid{grid-template-columns:repeat(2,minmax(0,1fr));gap:12px}.card{min-height:150px;padding:16px;border-radius:19px}.cardTitle{font-size:17px}.cardPreview{font-size:13px}.pageTitleRow h1{font-size:27px}.editorShell{border-radius:0;border-left:0;border-right:0;margin:-16px -14px;height:calc(100% + 32px)}.editorHead{padding:18px 18px 10px}.editorMeta{margin-top:5px}.titleInput{font-size:29px}.toolbar{position:fixed;left:0;right:0;top:auto;bottom:calc(env(safe-area-inset-bottom,0px) + var(--keyboard-inset,0px));z-index:80;padding:8px 10px;gap:4px;overflow-x:auto;flex-wrap:nowrap;border-top:1px solid #ffffff18;border-bottom:0;background:#1b1b1ef7;box-shadow:0 -8px 26px #0005;backdrop-filter:blur(14px);-webkit-backdrop-filter:blur(14px);scrollbar-width:none;-webkit-overflow-scrolling:touch}.toolbar::-webkit-scrollbar{display:none}.tool{width:44px;min-width:44px;height:44px}.editor{padding:22px 19px 92px;font-size:17px;scroll-padding-bottom:92px}.fab{width:62px;height:62px;border-radius:20px}.topActions .hideMobile{display:none}}'''
new_mobile = '''@media(max-width:700px){#app{height:100%}.topbar{height:70px;padding:10px 10px}.brand{display:none}.crumb span{max-width:95px}.searchWrap{height:48px;padding:0 13px}.searchWrap input{font-size:16px}.main{padding:16px 14px}.grid{grid-template-columns:repeat(2,minmax(0,1fr));gap:12px}.card{min-height:150px;padding:16px;border-radius:19px}.cardTitle{font-size:17px}.cardPreview{font-size:13px}.pageTitleRow h1{font-size:27px}.editorShell{border-radius:0;border-left:0;border-right:0;margin:-16px -14px;height:calc(100% + 32px);overscroll-behavior:none}.editorHead{padding:18px 18px 10px;order:1}.editorMeta{margin-top:5px}.titleInput{font-size:29px}.editor{order:2;padding:22px 19px 24px;font-size:17px;scroll-padding-bottom:24px;overscroll-behavior-y:contain}.toolbar{order:3;position:static;flex:0 0 auto;z-index:4;padding:8px 10px;gap:4px;overflow-x:auto;flex-wrap:nowrap;border-top:1px solid #ffffff18;border-bottom:0;background:#1b1b1ef7;box-shadow:0 -8px 26px #0004;backdrop-filter:blur(14px);-webkit-backdrop-filter:blur(14px);scrollbar-width:none;-webkit-overflow-scrolling:touch;overscroll-behavior-x:contain}.toolbar::-webkit-scrollbar{display:none}.tool{width:44px;min-width:44px;height:44px}.fab{width:62px;height:62px;border-radius:20px}.topActions .hideMobile{display:none}}'''
if old_mobile not in s:
    raise SystemExit('v1.0.5 mobile anchor missing')
s = s.replace(old_mobile, new_mobile, 1)

old_view = '''function updateViewportMetrics(){const vv=window.visualViewport;if(!vv)return;const keyboard=Math.max(0,window.innerHeight-vv.height-vv.offsetTop);document.documentElement.style.setProperty('--keyboard-inset',keyboard+'px');document.documentElement.style.setProperty('--visual-height',vv.height+'px')}
window.visualViewport?.addEventListener('resize',updateViewportMetrics);window.visualViewport?.addEventListener('scroll',updateViewportMetrics);window.addEventListener('resize',updateViewportMetrics);updateViewportMetrics();'''
if old_view not in s:
    raise SystemExit('v1.0.5 viewport anchor missing')
s = s.replace(old_view, 'function updateViewportMetrics(){}', 1)

anchor = "function updateWordCount(){const ed=$('#editor'),out=$('#wordCount');if(!ed||!out)return;const n=countWords(ed.innerText||ed.textContent||'');out.textContent=`${n} word${n===1?'':'s'}`}"
spell = r'''
let spellTimer=null,spellRequest=0,spellTokens=[];
function clearSpellHighlights(){try{CSS.highlights?.delete('mosaic-spelling')}catch{}spellTokens=[]}
function scheduleSpellcheck(delay=550){clearTimeout(spellTimer);if(!pref('spellcheck',true)){clearSpellHighlights();return}const ed=$('#editor');if(!ed)return;if(window.AndroidBridge?.checkSpelling)spellTimer=setTimeout(runAndroidSpellcheck,delay)}
function runAndroidSpellcheck(){const ed=$('#editor');if(!ed||!pref('spellcheck',true)||!window.AndroidBridge?.checkSpelling)return;const walker=document.createTreeWalker(ed,NodeFilter.SHOW_TEXT);const tokens=[];let node;while(node=walker.nextNode()){if(node.parentElement?.closest('.html-embed-wrap'))continue;const text=node.nodeValue||'';const re=/[A-Za-z][A-Za-z'’-]{1,}/g;let m;while((m=re.exec(text))&&tokens.length<1200)tokens.push({node,start:m.index,end:m.index+m[0].length,word:m[0]});if(tokens.length>=1200)break}spellTokens=tokens;if(!tokens.length){clearSpellHighlights();return}const id=String(++spellRequest);try{AndroidBridge.checkSpelling(id,JSON.stringify(tokens.map(t=>t.word)))}catch(e){console.warn('Android spell check failed',e)}}
window.MosaicSpell={onResults(id,results){if(String(id)!==String(spellRequest)||!pref('spellcheck',true))return;if(!Array.isArray(results)||!window.CSS?.highlights||typeof Highlight==='undefined')return;const ranges=[];for(const r of results){if(!r?.typo)continue;const t=spellTokens[r.i];if(!t?.node?.isConnected)continue;try{const range=new Range();range.setStart(t.node,t.start);range.setEnd(t.node,t.end);ranges.push(range)}catch{}}try{CSS.highlights.set('mosaic-spelling',new Highlight(...ranges))}catch(e){console.warn('Spell highlight unavailable',e)}},onUnavailable(){}};
'''
if anchor not in s:
    raise SystemExit('v1.0.5 word count anchor missing')
s = s.replace(anchor, anchor + spell, 1)

old_render = "function render(){if(!state)return;crumb.innerHTML=crumbs();backBtn.style.visibility=view.type==='home'?'hidden':'visible';fab.classList.toggle('hidden',view.type==='editor');if(searchInput.value.trim()){renderSearch(searchInput.value.trim());return}if(view.type==='home')renderHome();else if(view.type==='sections')renderSections(view.notebookId);else if(view.type==='pages')renderPages(view.notebookId,view.sectionId);else if(view.type==='editor')renderEditor(view.pageId);updateSyncUI()}"
new_render = "function render(){if(!state)return;crumb.innerHTML=crumbs();backBtn.style.visibility=view.type==='home'?'hidden':'visible';fab.classList.toggle('hidden',view.type==='editor');main.classList.toggle('editorMode',view.type==='editor');if(view.type!=='editor')clearSpellHighlights();if(searchInput.value.trim()){renderSearch(searchInput.value.trim());return}if(view.type==='home')renderHome();else if(view.type==='sections')renderSections(view.notebookId);else if(view.type==='pages')renderPages(view.notebookId,view.sectionId);else if(view.type==='editor')renderEditor(view.pageId);updateSyncUI()}"
if old_render not in s:
    raise SystemExit('v1.0.5 render anchor missing')
s = s.replace(old_render, new_render, 1)

needle = "lastEditorHTML=ed.innerHTML;updateWordCount();ed.addEventListener('input',()=>queueEditorSave());"
if needle not in s:
    raise SystemExit('v1.0.5 editor input anchor missing')
s = s.replace(needle, "lastEditorHTML=ed.innerHTML;updateWordCount();scheduleSpellcheck(150);ed.addEventListener('input',()=>{queueEditorSave();scheduleSpellcheck()});", 1)

s = s.replace('Show browser/Android spelling suggestions and underlines while editing.', 'Underline likely misspellings while editing. On Android this uses the system spell checker; on the website it uses the browser spell checker.')
old_toggle = "const ed=$('#editor');if(ed)ed.spellcheck=e.target.checked"
if old_toggle not in s:
    raise SystemExit('v1.0.5 spell toggle anchor missing')
s = s.replace(old_toggle, "const ed=$('#editor');if(ed)ed.spellcheck=e.target.checked;if(e.target.checked)scheduleSpellcheck(100);else clearSpellHighlights()", 1)

p.write_text(s)
(Path('/tmp/mosaic-src/mosaic-notes/index.html')).write_text(s)

from pathlib import Path

p = Path('/tmp/mosaic-src/mosaic-notes/app/src/main/java/com/mosaicnotes/app/MainActivity.java')
s = p.read_text()

anchor = '        webView.setOverScrollMode(View.OVER_SCROLL_NEVER);\n'
replacement = '''        webView.setOverScrollMode(View.OVER_SCROLL_NEVER);\n        webView.setVerticalScrollBarEnabled(false);\n        webView.setHorizontalScrollBarEnabled(false);\n        webView.setScrollbarFadingEnabled(true);\n'''
if anchor not in s:
    raise SystemExit('WebView overscroll anchor missing')
s = s.replace(anchor, replacement, 1)

client_anchor = '''        webView.setWebViewClient(new WebViewClient() {\n            @Override\n            public boolean shouldOverrideUrlLoading(WebView view, WebResourceRequest request) {\n'''
client_replacement = '''        webView.setWebViewClient(new WebViewClient() {\n            @Override\n            public void onPageFinished(WebView view, String url) {\n                super.onPageFinished(view, url);\n                // Android-only: keep scrolling functional but remove every visual scrollbar,\n                // including the nested contenteditable editor scrollbar.\n                String js = \"(function(){\" +\n                        \"if(document.getElementById('mosaic-android-hide-scrollbars'))return;\" +\n                        \"var s=document.createElement('style');\" +\n                        \"s.id='mosaic-android-hide-scrollbars';\" +\n                        \"s.textContent='*{scrollbar-width:none!important}*::-webkit-scrollbar{display:none!important;width:0!important;height:0!important}';\" +\n                        \"document.head.appendChild(s);\" +\n                        \"})()\";\n                view.evaluateJavascript(js, null);\n            }\n\n            @Override\n            public boolean shouldOverrideUrlLoading(WebView view, WebResourceRequest request) {\n'''
if client_anchor not in s:
    raise SystemExit('WebViewClient anchor missing')
s = s.replace(client_anchor, client_replacement, 1)

p.write_text(s)

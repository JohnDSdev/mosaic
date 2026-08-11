from pathlib import Path
p=Path('/tmp/mosaic-src/mosaic-notes/app/src/main/java/com/mosaicnotes/app/MainActivity.java')
s=p.read_text()
for imp in ['import android.graphics.Insets;','import android.os.Build;','import android.view.View;','import android.view.ViewGroup;','import android.view.WindowInsets;','import android.widget.FrameLayout;']:
    if imp not in s:
        if imp.startswith('import android.graphics'):
            s=s.replace('import android.content.Intent;\n','import android.content.Intent;\n'+imp+'\n',1)
        elif imp.startswith('import android.os.Build'):
            s=s.replace('import android.os.Bundle;\n','import android.os.Bundle;\n'+imp+'\n',1)
        elif imp.startswith('import android.view'):
            s=s.replace('import android.view.textservice.SentenceSuggestionsInfo;\n',imp+'\nimport android.view.textservice.SentenceSuggestionsInfo;\n',1)
        else:
            s=s.replace('import android.widget.Toast;\n',imp+'\nimport android.widget.Toast;\n',1)
old='''        getWindow().setSoftInputMode(android.view.WindowManager.LayoutParams.SOFT_INPUT_ADJUST_RESIZE);\n\n        webView = new WebView(this);\n        setContentView(webView);\n'''
new='''        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.R) {\n            getWindow().setDecorFitsSystemWindows(false);\n            getWindow().setSoftInputMode(android.view.WindowManager.LayoutParams.SOFT_INPUT_ADJUST_NOTHING);\n        } else {\n            getWindow().setSoftInputMode(android.view.WindowManager.LayoutParams.SOFT_INPUT_ADJUST_RESIZE);\n        }\n\n        FrameLayout root = new FrameLayout(this);\n        webView = new WebView(this);\n        FrameLayout.LayoutParams webParams = new FrameLayout.LayoutParams(\n                ViewGroup.LayoutParams.MATCH_PARENT, ViewGroup.LayoutParams.MATCH_PARENT);\n        root.addView(webView, webParams);\n        setContentView(root);\n        webView.setOverScrollMode(View.OVER_SCROLL_NEVER);\n\n        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.R) {\n            root.setOnApplyWindowInsetsListener((view, insets) -> {\n                Insets bars = insets.getInsets(WindowInsets.Type.systemBars());\n                Insets ime = insets.getInsets(WindowInsets.Type.ime());\n                int bottom = Math.max(bars.bottom, ime.bottom);\n                FrameLayout.LayoutParams lp = (FrameLayout.LayoutParams) webView.getLayoutParams();\n                if (lp.leftMargin != bars.left || lp.topMargin != bars.top ||\n                        lp.rightMargin != bars.right || lp.bottomMargin != bottom) {\n                    lp.setMargins(bars.left, bars.top, bars.right, bottom);\n                    webView.setLayoutParams(lp);\n                }\n                return WindowInsets.CONSUMED;\n            });\n            root.requestApplyInsets();\n        }\n'''
if old not in s: raise SystemExit('v106 android onCreate anchor missing')
s=s.replace(old,new,1)
p.write_text(s)

package com.mosaicnotes.app;

import android.app.Activity;
import android.content.ActivityNotFoundException;
import android.content.Intent;
import android.net.Uri;
import android.os.Bundle;
import android.view.textservice.SentenceSuggestionsInfo;
import android.view.textservice.SpellCheckerSession;
import android.view.textservice.SuggestionsInfo;
import android.view.textservice.TextInfo;
import android.view.textservice.TextServicesManager;
import android.webkit.JavascriptInterface;
import android.webkit.ValueCallback;
import android.webkit.WebChromeClient;
import android.webkit.WebResourceRequest;
import android.webkit.WebSettings;
import android.webkit.WebView;
import android.webkit.WebViewClient;
import android.widget.Toast;

import org.json.JSONArray;
import org.json.JSONObject;

import java.io.OutputStream;
import java.nio.charset.StandardCharsets;
import java.util.Map;
import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.atomic.AtomicInteger;

public class MainActivity extends Activity {
    private static final int FILE_CHOOSER_REQUEST = 2001;
    private static final int SAVE_FILE_REQUEST = 2002;
    private WebView webView;
    private ValueCallback<Uri[]> filePathCallback;
    private String pendingSaveText;

    private SpellCheckerSession spellCheckerSession;
    private final AtomicInteger spellCookieCounter = new AtomicInteger(1000);
    private final Map<Integer, String> spellRequests = new ConcurrentHashMap<>();

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        getWindow().setSoftInputMode(android.view.WindowManager.LayoutParams.SOFT_INPUT_ADJUST_RESIZE);

        webView = new WebView(this);
        setContentView(webView);

        WebSettings s = webView.getSettings();
        s.setJavaScriptEnabled(true);
        s.setDomStorageEnabled(true);
        s.setDatabaseEnabled(true);
        s.setAllowFileAccess(true);
        s.setAllowContentAccess(true);
        s.setAllowUniversalAccessFromFileURLs(true);
        s.setMixedContentMode(WebSettings.MIXED_CONTENT_NEVER_ALLOW);
        s.setMediaPlaybackRequiresUserGesture(true);

        initSpellChecker();

        webView.addJavascriptInterface(new AndroidBridge(), "AndroidBridge");
        webView.setWebViewClient(new WebViewClient() {
            @Override
            public boolean shouldOverrideUrlLoading(WebView view, WebResourceRequest request) {
                Uri uri = request.getUrl();
                String scheme = uri.getScheme();
                if ("http".equalsIgnoreCase(scheme) || "https".equalsIgnoreCase(scheme)) {
                    openExternal(uri.toString());
                    return true;
                }
                return false;
            }
        });
        webView.setWebChromeClient(new WebChromeClient() {
            @Override
            public boolean onShowFileChooser(WebView webView, ValueCallback<Uri[]> filePathCallback,
                                             FileChooserParams fileChooserParams) {
                if (MainActivity.this.filePathCallback != null) {
                    MainActivity.this.filePathCallback.onReceiveValue(null);
                }
                MainActivity.this.filePathCallback = filePathCallback;
                Intent intent;
                try {
                    intent = fileChooserParams.createIntent();
                } catch (Exception e) {
                    intent = new Intent(Intent.ACTION_OPEN_DOCUMENT);
                    intent.setType("*/*");
                    intent.addCategory(Intent.CATEGORY_OPENABLE);
                }
                try {
                    startActivityForResult(intent, FILE_CHOOSER_REQUEST);
                } catch (ActivityNotFoundException e) {
                    MainActivity.this.filePathCallback = null;
                    Toast.makeText(MainActivity.this, "No file picker found.", Toast.LENGTH_SHORT).show();
                }
                return true;
            }
        });

        webView.loadUrl("file:///android_asset/index.html");
    }

    private void initSpellChecker() {
        try {
            TextServicesManager manager = (TextServicesManager) getSystemService(TEXT_SERVICES_MANAGER_SERVICE);
            if (manager == null) return;
            spellCheckerSession = manager.newSpellCheckerSession(
                    null,
                    null,
                    new SpellCheckerSession.SpellCheckerSessionListener() {
                        @Override
                        public void onGetSuggestions(SuggestionsInfo[] results) {
                            JSONArray out = new JSONArray();
                            int cookie = -1;
                            if (results != null) {
                                for (SuggestionsInfo info : results) {
                                    if (info == null) continue;
                                    cookie = info.getCookie();
                                    int attrs = info.getSuggestionsAttributes();
                                    boolean inDictionary = (attrs & SuggestionsInfo.RESULT_ATTR_IN_THE_DICTIONARY) != 0;
                                    boolean looksLikeTypo = (attrs & SuggestionsInfo.RESULT_ATTR_LOOKS_LIKE_TYPO) != 0;
                                    try {
                                        JSONObject item = new JSONObject();
                                        item.put("i", info.getSequence());
                                        item.put("typo", looksLikeTypo && !inDictionary);
                                        JSONArray suggestions = new JSONArray();
                                        int count = Math.max(0, info.getSuggestionsCount());
                                        for (int i = 0; i < Math.min(3, count); i++) {
                                            suggestions.put(info.getSuggestionAt(i));
                                        }
                                        item.put("suggestions", suggestions);
                                        out.put(item);
                                    } catch (Exception ignored) {
                                    }
                                }
                            }
                            if (cookie != -1) {
                                String requestId = spellRequests.remove(cookie);
                                if (requestId != null) sendSpellResults(requestId, out);
                            }
                        }

                        @Override
                        public void onGetSentenceSuggestions(SentenceSuggestionsInfo[] results) {
                            // Mosaic checks individual words so it can underline ranges without
                            // rewriting the contenteditable DOM or disturbing the caret.
                        }
                    },
                    true
            );
        } catch (Exception e) {
            spellCheckerSession = null;
        }
    }

    private void sendSpellResults(String requestId, JSONArray results) {
        runOnUiThread(() -> {
            if (webView == null) return;
            String js = "window.MosaicSpell&&window.MosaicSpell.onResults(" +
                    JSONObject.quote(requestId) + "," + results.toString() + ");";
            webView.evaluateJavascript(js, null);
        });
    }

    private void sendSpellUnavailable(String requestId) {
        runOnUiThread(() -> {
            if (webView == null) return;
            String js = "window.MosaicSpell&&window.MosaicSpell.onUnavailable&&window.MosaicSpell.onUnavailable(" +
                    JSONObject.quote(requestId) + ");";
            webView.evaluateJavascript(js, null);
        });
    }

    private void openExternal(String url) {
        try {
            startActivity(new Intent(Intent.ACTION_VIEW, Uri.parse(url)));
        } catch (Exception e) {
            Toast.makeText(this, "Could not open link.", Toast.LENGTH_SHORT).show();
        }
    }

    public class AndroidBridge {
        @JavascriptInterface
        public void openUrl(String url) {
            runOnUiThread(() -> openExternal(url));
        }

        @JavascriptInterface
        public void saveFile(String filename, String text) {
            pendingSaveText = text;
            Intent intent = new Intent(Intent.ACTION_CREATE_DOCUMENT);
            intent.addCategory(Intent.CATEGORY_OPENABLE);
            intent.setType("application/json");
            intent.putExtra(Intent.EXTRA_TITLE, filename);
            runOnUiThread(() -> startActivityForResult(intent, SAVE_FILE_REQUEST));
        }

        @JavascriptInterface
        public void checkSpelling(String requestId, String wordsJson) {
            runOnUiThread(() -> {
                if (spellCheckerSession == null) {
                    sendSpellUnavailable(requestId);
                    return;
                }
                try {
                    JSONArray words = new JSONArray(wordsJson);
                    int count = Math.min(1200, words.length());
                    if (count == 0) {
                        sendSpellResults(requestId, new JSONArray());
                        return;
                    }
                    int cookie = spellCookieCounter.incrementAndGet();
                    spellRequests.put(cookie, requestId);
                    TextInfo[] infos = new TextInfo[count];
                    for (int i = 0; i < count; i++) {
                        infos[i] = new TextInfo(words.optString(i, ""), cookie, i);
                    }
                    spellCheckerSession.getSuggestions(infos, 3, false);
                } catch (Exception e) {
                    sendSpellUnavailable(requestId);
                }
            });
        }
    }

    @Override
    protected void onActivityResult(int requestCode, int resultCode, Intent data) {
        super.onActivityResult(requestCode, resultCode, data);
        if (requestCode == FILE_CHOOSER_REQUEST) {
            if (filePathCallback == null) return;
            Uri[] results = null;
            if (resultCode == RESULT_OK && data != null) {
                if (data.getClipData() != null) {
                    int count = data.getClipData().getItemCount();
                    results = new Uri[count];
                    for (int i = 0; i < count; i++) results[i] = data.getClipData().getItemAt(i).getUri();
                } else if (data.getData() != null) {
                    results = new Uri[]{data.getData()};
                }
            }
            filePathCallback.onReceiveValue(results);
            filePathCallback = null;
        } else if (requestCode == SAVE_FILE_REQUEST) {
            if (resultCode == RESULT_OK && data != null && data.getData() != null && pendingSaveText != null) {
                try (OutputStream out = getContentResolver().openOutputStream(data.getData())) {
                    if (out != null) out.write(pendingSaveText.getBytes(StandardCharsets.UTF_8));
                    Toast.makeText(this, "Backup saved.", Toast.LENGTH_SHORT).show();
                } catch (Exception e) {
                    Toast.makeText(this, "Could not save backup.", Toast.LENGTH_SHORT).show();
                }
            }
            pendingSaveText = null;
        }
    }

    @Override
    public void onBackPressed() {
        webView.evaluateJavascript("(function(){var b=document.getElementById('backBtn'); if(b && b.style.visibility!=='hidden'){b.click(); return 'handled'} return 'none';})()", value -> {
            if (!"\"handled\"".equals(value)) super.onBackPressed();
        });
    }

    @Override
    protected void onDestroy() {
        if (spellCheckerSession != null) {
            try { spellCheckerSession.close(); } catch (Exception ignored) {}
        }
        if (webView != null) webView.destroy();
        super.onDestroy();
    }
}

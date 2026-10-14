with open('index.html', 'r') as f:
    s = f.read()

# 1. Add camera button in .bar
s = s.replace(
    '<button id="clear" title="Clear chat">🗑️</button>',
    '<button id="cam" title="Send a photo">📸</button>\n    <button id="clear" title="Clear chat">🗑️</button>'
)

# 2. Add hidden file input after </div> of .bar
s = s.replace(
    '</div>\n\n  <div id="sig">',
    '</div>\n<input type="file" id="camFile" accept="image/*" style="display:none" />\n\n  <div id="sig">'
)

# 3. Add camera CSS
s = s.replace(
    '#clear { background:#f2f2f7; color:#1c1c1e; padding:12px 14px; }',
    '''#clear { background:#f2f2f7; color:#1c1c1e; padding:12px 14px; }
    #cam { background:#f2f2f7; color:#1c1c1e; padding:12px 14px; }
    .msg img.sent-photo { max-width:200px; border-radius:12px; margin-top:8px; display:block; }'''
)

# 4. Add camBtn/camFile declarations
s = s.replace(
    "const clearBtn=document.getElementById('clear');",
    "const clearBtn=document.getElementById('clear');\nconst camBtn = document.getElementById('cam');\nconst camFile = document.getElementById('camFile');"
)

# 5. Add camera onclick handler before voiceBtn
camera_js = '''camBtn.onclick = () => camFile.click();

camFile.onchange = async () => {
  const file = camFile.files[0];
  if (!file) return;
  camFile.value = '';
  const reader = new FileReader();
  reader.onload = async (ev) => {
    const dataUrl = ev.target.result;
    const d = document.createElement('div');
    d.className = 'msg user';
    d.innerHTML = '<img class="sent-photo" src="' + dataUrl + '" alt="photo" />';
    chat.appendChild(d);
    window.scrollTo({ top: document.body.scrollHeight, behavior: 'smooth' });
    const loading = addMsg('🔍 Looking at your photo...', 'bot');
    try {
      const r = await fetch(BACKEND + '/api/vision', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ imageBase64: dataUrl, question: 'Describe this image in detail.' }),
      });
      const data = await r.json();
      const reply = data.reply || data.error || '';
      const footer = '<div class="footer-sig">♤brantyreKE♤☆</div>';
      const copyHtml = '<button class="copy-btn" onclick="copyMsg(this)">📋 Copy</button>';
      const combined = footer + copyHtml;
      if (window.marked) {
        loading.innerHTML = marked.parse(reply) + combined;
      } else {
        loading.innerHTML = '<div>' + reply + '</div>' + combined;
      }
      history.push({ role: 'user', content: '[sent a photo]' });
      history.push({ role: 'assistant', content: reply });
      try { localStorage.setItem('lumera_history', JSON.stringify(history)); } catch(e) {}
      speak(reply);
    } catch (e) {
      loading.textContent = 'Error: ' + e.message;
    }
  };
  reader.readAsDataURL(file);
};

voiceBtn.onclick = () => {'''

s = s.replace('voiceBtn.onclick = () => {', camera_js, 1)

with open('index.html', 'w') as f:
    f.write(s)

print("Done. camBtn count:", s.count('camBtn'))
print("camFile count:", s.count('camFile'))
print("api/vision count:", s.count('api/vision'))

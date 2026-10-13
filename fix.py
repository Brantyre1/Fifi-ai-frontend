with open('index.html', 'r') as f:
    s = f.read()

# FIX 1: Remove duplicate const footer
s = s.replace(
"""const footer = '<div class="footer-sig">♤brantyreKE♤☆</div>';
const footer = '<div class="footer-sig">♤brantyreKE♤☆</div>';
const copyHtml = '<button class="copy-btn" onclick="copyMsg(this)">📋 Copy</button>';
const combined = footer + copyHtml;
d.innerHTML = marked.parse(m.content) + combined;""",
"""const footer = '<div class="footer-sig">♤brantyreKE♤☆</div>';
            const copyHtml = '<button class="copy-btn" onclick="copyMsg(this)">📋 Copy</button>';
            const combined = footer + copyHtml;
            d.innerHTML = marked.parse(m.content) + combined;"""
)

# FIX 2: Clean up broken CSS
s = s.replace(
""".footer-sig {
  margin-top: 14px; padding-top: 10px; border-top: 1px solid ...
  text-align: right; font-size: 13px; color: #8b5cf6;
  font-style: italic; letter-spacing: 0.2px;
}
.bar {
  ...
      margin-top: 14px; padding-top: 10px; border-top: 1px solid #d1d1d6;
      text-align: right; font-size: 13px; color: #8b5cf6;
      font-style: italic; letter-spacing: 0.2px;
    }
    .bar {""",
"""    .footer-sig {
      margin-top: 14px;
      padding-top: 10px;
      border-top: 1px solid #d1d1d6;
      text-align: right;
      font-size: 13px;
      color: #8b5cf6;
      font-style: italic;
      letter-spacing: 0.2px;
    }
    .bar {"""
)

with open('index.html', 'w') as f:
    f.write(s)

print("Done.")
print("const footer count:", s.count("const footer ="))
print("has duplicate:", "const footer = '<div class=\"footer-sig\">♤brantyreKE♤☆</div>';\nconst footer" in s)

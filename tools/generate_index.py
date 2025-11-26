import os
from pathlib import Path
from datetime import datetime
import html

PAGES_DIR = Path("pages")
OUT_FILE = Path("index.html")

def collect_html_files():
    files = []
    for p in PAGES_DIR.rglob("*.html"):
        rel = p.relative_to(Path("."))  # pages/xxx.html
        files.append(rel.as_posix())
    return sorted(files)

def build_index(file_list):
    items = "\n".join(
        f'<li><a href="{html.escape(f)}">{html.escape(Path(f).stem)}</a></li>'
        for f in file_list
    )
    now = datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")
    return f"""<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width,initial-scale=1" />
  <title>导航站</title>
  <style>
    body {{ font-family: system-ui, sans-serif; max-width: 900px; margin: 40px auto; padding: 0 16px; }}
    h1 {{ margin-bottom: 0.2rem; }}
    ul {{ line-height: 1.9; }}
    footer {{ margin-top: 32px; color: #666; font-size: 12px; }}
  </style>
</head>
<body>
  <h1>导航页</h1>
  <p>这些是我用gemini生成的一些网页，点击进入：</p>
  <ul>
    {items}
  </ul>
  <footer>自动生成于 {now}</footer>
</body>
</html>
"""

if __name__ == "__main__":
    files = collect_html_files()
    OUT_FILE.write_text(build_index(files), encoding="utf-8")
    print(f"Generated {OUT_FILE} with {len(files)} links.")

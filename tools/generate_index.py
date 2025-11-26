import os
from pathlib import Path
from datetime import datetime, timezone, timedelta
import html

PAGES_DIR = Path("pages")
OUT_FILE = Path("index.html")

def collect_html_files():
    files = []
    if not PAGES_DIR.exists():
        return files
    for p in PAGES_DIR.rglob("*.html"):
        rel = p.relative_to(Path("."))  # e.g. pages/xxx.html
        files.append(rel.as_posix())
    return sorted(files)

def build_items(file_list):
    # Use filename stem as display title
    lis = []
    for f in file_list:
        stem = Path(f).stem
        lis.append(
            f"""
      <li class="card">
        <a class="card-link" href="{html.escape(f)}" title="{html.escape(f)}">
          <span class="card-title">{html.escape(stem)}</span>
          <span class="card-path">{html.escape(f)}</span>
        </a>
      </li>
            """.rstrip()
        )
    return "\n".join(lis)

def build_index(file_list):
    items_html = build_items(file_list)

    # GMT+8 time
    gmt8 = timezone(timedelta(hours=8))
    now_gmt8 = datetime.now(gmt8).strftime("%Y-%m-%d %H:%M GMT+8")

    return f"""<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width,initial-scale=1" />
  <title>导航站</title>
  <style>
    :root {{
      --bg: #0b0f17;
      --bg-soft: #111827;
      --card: rgba(17, 24, 39, 0.9);
      --card-hover: rgba(31, 41, 55, 0.95);
      --text: #e5e7eb;
      --muted: #9ca3af;
      --brand: #8b5cf6;
      --brand-2: #22d3ee;
      --ring: rgba(139, 92, 246, 0.35);
      --shadow: 0 10px 30px rgba(0, 0, 0, 0.45);
      --radius: 16px;
    }}

    * {{ box-sizing: border-box; }}
    body {{
      font-family: system-ui, -apple-system, Segoe UI, Roboto, "Helvetica Neue", Arial, "Noto Sans", "Apple Color Emoji", "Segoe UI Emoji";
      max-width: 980px;
      margin: 40px auto;
      padding: 0 16px;
      color: var(--text);
      background:
        radial-gradient(1200px 600px at 10% -10%, rgba(139,92,246,0.18), transparent 55%),
        radial-gradient(900px 500px at 110% 0%, rgba(34,211,238,0.12), transparent 60%),
        linear-gradient(180deg, #070a11 0%, var(--bg) 100%);
      min-height: 100vh;
      animation: pageFade 520ms ease-out both;
    }}

    header {{
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 12px;
      margin-bottom: 14px;
    }}

    h1 {{
      margin: 0;
      font-size: clamp(1.8rem, 3vw, 2.4rem);
      letter-spacing: 0.5px;
      line-height: 1.1;
      background: linear-gradient(90deg, var(--brand), var(--brand-2));
      -webkit-background-clip: text;
      background-clip: text;
      color: transparent;
      filter: drop-shadow(0 6px 24px rgba(139,92,246,.25));
    }}

    .subtitle {{
      margin: 8px 0 20px 0;
      color: var(--muted);
      font-size: 0.98rem;
    }}

    .badge {{
      font-size: 12px;
      color: var(--muted);
      background: rgba(255,255,255,0.04);
      border: 1px solid rgba(255,255,255,0.08);
      padding: 6px 10px;
      border-radius: 999px;
      backdrop-filter: blur(8px);
      white-space: nowrap;
    }}

    ul {{
      list-style: none;
      padding: 0;
      margin: 0;
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
      gap: 14px;
    }}

    .card {{
      background: var(--card);
      border: 1px solid rgba(255,255,255,0.06);
      border-radius: var(--radius);
      box-shadow: var(--shadow);
      transform: translateY(6px);
      opacity: 0;
      animation: cardIn 520ms ease-out forwards;
    }}

    /* Stagger animation for cards */
    .card:nth-child(1) {{ animation-delay: 40ms; }}
    .card:nth-child(2) {{ animation-delay: 80ms; }}
    .card:nth-child(3) {{ animation-delay: 120ms; }}
    .card:nth-child(4) {{ animation-delay: 160ms; }}
    .card:nth-child(5) {{ animation-delay: 200ms; }}
    .card:nth-child(6) {{ animation-delay: 240ms; }}
    .card:nth-child(7) {{ animation-delay: 280ms; }}
    .card:nth-child(8) {{ animation-delay: 320ms; }}
    .card:nth-child(9) {{ animation-delay: 360ms; }}
    .card:nth-child(10) {{ animation-delay: 400ms; }}

    .card-link {{
      display: grid;
      gap: 6px;
      padding: 14px 14px 13px 14px;
      text-decoration: none;
      color: inherit;
      position: relative;
      overflow: hidden;
      border-radius: inherit;
    }}

    .card-link::after {{
      content: "";
      position: absolute;
      inset: -60% -40%;
      background:
        radial-gradient(280px 140px at 10% 10%, rgba(139,92,246,0.25), transparent 60%),
        radial-gradient(280px 180px at 90% 20%, rgba(34,211,238,0.20), transparent 65%);
      opacity: 0;
      transition: opacity 220ms ease;
      pointer-events: none;
    }}

    .card-title {{
      font-weight: 700;
      font-size: 1.05rem;
      letter-spacing: 0.2px;
    }}

    .card-path {{
      font-size: 12px;
      color: var(--muted);
      word-break: break-all;
    }}

    .card:hover {{
      background: var(--card-hover);
      border-color: rgba(139, 92, 246, 0.35);
      box-shadow: 0 12px 40px rgba(0,0,0,0.55), 0 0 0 3px var(--ring);
      transform: translateY(-2px);
      transition: transform 160ms ease, background 160ms ease, border-color 160ms ease, box-shadow 160ms ease;
    }}
    .card:hover .card-link::after {{
      opacity: 1;
    }}

    footer {{
      margin-top: 28px;
      color: var(--muted);
      font-size: 12px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      gap: 12px;
      opacity: 0.9;
    }}

    .footer-left {{
      display: inline-flex;
      gap: 8px;
      align-items: center;
    }}

    .dot {{
      width: 8px;
      height: 8px;
      border-radius: 50%;
      background: linear-gradient(90deg, var(--brand), var(--brand-2));
      box-shadow: 0 0 12px rgba(139,92,246,0.8);
      animation: pulse 1.8s ease-in-out infinite;
    }}

    @keyframes pageFade {{
      from {{ opacity: 0; transform: translateY(6px); }}
      to   {{ opacity: 1; transform: translateY(0); }}
    }}
    @keyframes cardIn {{
      to {{ opacity: 1; transform: translateY(0); }}
    }}
    @keyframes pulse {{
      0%, 100% {{ transform: scale(1); opacity: 0.9; }}
      50%      {{ transform: scale(1.35); opacity: 1; }}
    }}

    /* Reduce motion support */
    @media (prefers-reduced-motion: reduce) {{
      * {{ animation: none !important; transition: none !important; }}
    }}
  </style>
</head>
<body>
  <header>
    <h1>导航页</h1>
    <div class="badge">{len(file_list)} 个页面</div>
  </header>
  <p class="subtitle">这些是我用 gemini 生成的一些网页，点击进入：</p>

  <ul>
{items_html if items_html.strip() else "    <li class='card'><div class='card-link'><span class='card-title'>暂无页面</span><span class='card-path'>请在 pages/ 下添加 *.html</span></div></li>"}
  </ul>

  <footer>
    <div class="footer-left">
      <span class="dot"></span>
      <span>自动生成于 {now_gmt8}</span>
    </div>
    <div>Hosted on GitHub Pages</div>
  </footer>
</body>
</html>
"""

if __name__ == "__main__":
    files = collect_html_files()
    OUT_FILE.write_text(build_index(files), encoding="utf-8")
    print(f"Generated {OUT_FILE} with {len(files)} links.")

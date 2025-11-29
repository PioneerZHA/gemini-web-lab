import json
from pathlib import Path
from datetime import datetime, timezone, timedelta
import html

PAGES_DIR = Path("pages")
OUT_FILE = Path("index.html")

def gmt8_str(ts: float) -> str:
    gmt8 = timezone(timedelta(hours=8))
    return datetime.fromtimestamp(ts, gmt8).strftime("%Y-%m-%d %H:%M GMT+8")

def collect_entries():
    """
    返回：
    - folders: 顶层文件夹列表（相对 pages/ 的路径）
    - root_files: pages/ 顶层 html 文件
    - files_by_folder: { "a": [file_dict, ...], "b": [...], "__root__": [...] }
      file_dict: {path, name, mtime, mtime_str}
    """
    folders = []
    root_files = []
    files_by_folder = {}

    if not PAGES_DIR.exists():
        return folders, root_files, files_by_folder

    # 顶层文件夹
    for p in PAGES_DIR.iterdir():
        if p.is_dir():
            folders.append(p.name)

    # 扫描所有 html
    for f in PAGES_DIR.rglob("*.html"):
        rel = f.relative_to(Path("."))          # pages/a/x.html
        rel_posix = rel.as_posix()

        # 文件元信息
        stat = f.stat()
        mtime = stat.st_mtime
        file_dict = {
            "path": rel_posix,
            "name": f.stem,
            "mtime": mtime,
            "mtime_str": gmt8_str(mtime),
        }

        # 判断顶层归属
        parts = f.relative_to(PAGES_DIR).parts  # e.g. ("a","x.html") or ("root.html",)
        if len(parts) == 1:
            root_files.append(file_dict)
            files_by_folder.setdefault("__root__", []).append(file_dict)
        else:
            top = parts[0]
            files_by_folder.setdefault(top, []).append(file_dict)

    folders.sort()
    root_files.sort(key=lambda x: x["name"].lower())

    # 每个文件夹内文件默认按名称排一下（前端还可切换）
    for k in files_by_folder:
        files_by_folder[k].sort(key=lambda x: x["name"].lower())

    return folders, root_files, files_by_folder


def build_index(folders, root_files, files_by_folder):
    # 生成时间（页面底部显示）
    gmt8 = timezone(timedelta(hours=8))
    now_gmt8 = datetime.now(gmt8).strftime("%Y-%m-%d %H:%M GMT+8")

    data = {
        "folders": folders,
        "filesByFolder": files_by_folder,
    }
    data_json = json.dumps(data, ensure_ascii=False)

    return f"""<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width,initial-scale=1" />
  <title>导航</title>
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
      font-family: system-ui, -apple-system, Segoe UI, Roboto, "Helvetica Neue", Arial, "Noto Sans";
      max-width: 1100px;
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
      display: flex; align-items: center; justify-content: space-between;
      gap: 12px; margin-bottom: 8px;
    }}
    h1 {{
      margin: 0; font-size: clamp(1.8rem, 3vw, 2.4rem);
      letter-spacing: 0.5px; line-height: 1.1;
      background: linear-gradient(90deg, var(--brand), var(--brand-2));
      -webkit-background-clip: text; background-clip: text; color: transparent;
      filter: drop-shadow(0 6px 24px rgba(139,92,246,.25));
    }}
    .subtitle {{
      margin: 8px 0 18px 0; color: var(--muted); font-size: 0.98rem;
    }}
    .toolbar {{
      display: flex; flex-wrap: wrap; gap: 8px; align-items: center;
      margin: 10px 0 16px;
    }}
    .chip {{
      font-size: 12px; color: var(--muted);
      background: rgba(255,255,255,0.04);
      border: 1px solid rgba(255,255,255,0.08);
      padding: 6px 10px; border-radius: 999px;
      backdrop-filter: blur(8px); white-space: nowrap;
    }}
    .btn {{
      cursor: pointer; user-select: none;
      font-size: 12px; color: var(--text);
      background: rgba(255,255,255,0.06);
      border: 1px solid rgba(255,255,255,0.10);
      padding: 6px 10px; border-radius: 10px;
      transition: all 160ms ease;
    }}
    .btn:hover {{
      border-color: rgba(139,92,246,0.5);
      box-shadow: 0 0 0 3px var(--ring);
      transform: translateY(-1px);
    }}
    .btn.active {{
      background: rgba(139,92,246,0.18);
      border-color: rgba(139,92,246,0.6);
    }}

    .grid {{
      list-style: none; padding: 0; margin: 0;
      display: grid; grid-template-columns: repeat(auto-fill, minmax(240px, 1fr));
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
    .card-link {{
      display: grid; gap: 6px; padding: 14px;
      text-decoration: none; color: inherit; position: relative;
      overflow: hidden; border-radius: inherit;
    }}
    .card-link::after {{
      content: ""; position: absolute; inset: -60% -40%;
      background:
        radial-gradient(280px 140px at 10% 10%, rgba(139,92,246,0.25), transparent 60%),
        radial-gradient(280px 180px at 90% 20%, rgba(34,211,238,0.20), transparent 65%);
      opacity: 0; transition: opacity 220ms ease; pointer-events: none;
    }}
    .card-title {{ font-weight: 700; font-size: 1.05rem; }}
    .card-meta {{ font-size: 12px; color: var(--muted); }}
    .card:hover {{
      background: var(--card-hover);
      border-color: rgba(139, 92, 246, 0.35);
      box-shadow: 0 12px 40px rgba(0,0,0,0.55), 0 0 0 3px var(--ring);
      transform: translateY(-2px);
      transition: transform 160ms ease, background 160ms ease, border-color 160ms ease, box-shadow 160ms ease;
    }}
    .card:hover .card-link::after {{ opacity: 1; }}

    footer {{
      margin-top: 28px; color: var(--muted); font-size: 12px;
      display: flex; justify-content: space-between; align-items: center; gap: 12px;
      opacity: 0.9;
    }}
    .dot {{
      width: 8px; height: 8px; border-radius: 50%;
      background: linear-gradient(90deg, var(--brand), var(--brand-2));
      box-shadow: 0 0 12px rgba(139,92,246,0.8);
      animation: pulse 1.8s ease-in-out infinite;
      display: inline-block; margin-right: 8px;
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
    @media (prefers-reduced-motion: reduce) {{
      * {{ animation: none !important; transition: none !important; }}
    }}
  </style>
</head>
<body>
  <header>
    <h1>导航页</h1>
    <div class="chip" id="countChip">0 个条目</div>
  </header>
  <p class="subtitle">这些是我用 Gemini 生成的一些网页。</p>

  <div class="toolbar">
    <span class="chip" id="breadcrumb">pages/</span>

    <span style="flex:1"></span>

    <span class="chip">排序</span>
    <button class="btn active" id="sortNameBtn">名称</button>
    <button class="btn" id="sortTimeBtn">修改时间</button>
    <button class="btn active" id="sortAscBtn">升序</button>
    <button class="btn" id="sortDescBtn">降序</button>
    <button class="btn" id="backBtn" style="display:none;">返回上层</button>
  </div>

  <ul class="grid" id="list"></ul>

  <footer>
    <div><span class="dot"></span>自动生成于 {now_gmt8}</div>
    <div>Hosted on GitHub Pages</div>
  </footer>

<script>
const DATA = {data_json};

let currentFolder = "__root__"; // "__root__" 表示顶层
let sortKey = "name";           // "name" | "mtime"
let sortDir = "asc";            // "asc" | "desc"

const listEl = document.getElementById("list");
const breadcrumbEl = document.getElementById("breadcrumb");
const countChipEl = document.getElementById("countChip");
const backBtn = document.getElementById("backBtn");

const sortNameBtn = document.getElementById("sortNameBtn");
const sortTimeBtn = document.getElementById("sortTimeBtn");
const sortAscBtn = document.getElementById("sortAscBtn");
const sortDescBtn = document.getElementById("sortDescBtn");

function setActive(btn, active) {{
  btn.classList.toggle("active", active);
}}

function renderRoot() {{
  currentFolder = "__root__";
  backBtn.style.display = "none";
  breadcrumbEl.textContent = "pages/";

  const folders = DATA.folders || [];
  const rootFiles = (DATA.filesByFolder && DATA.filesByFolder["__root__"]) || [];

  const entries = [];

  // 文件夹卡片
  for (const folder of folders) {{
    entries.push({{
      type: "folder",
      name: folder,
      path: "pages/" + folder + "/"
    }});
  }}

  // 顶层文件卡片
  for (const f of rootFiles) {{
    entries.push({{ type: "file", ...f }});
  }}

  renderEntries(entries);
}}

function renderFolder(folderName) {{
  currentFolder = folderName;
  backBtn.style.display = "inline-block";
  breadcrumbEl.textContent = "pages/" + folderName + "/";

  const files = (DATA.filesByFolder && DATA.filesByFolder[folderName]) || [];
  const entries = files.map(f => ({{
    type: "file",
    ...f
  }}));

  renderEntries(entries);
}}

function renderEntries(entries) {{
  // 排序仅对 file 生效，folder 保持在前
  const folders = entries.filter(e => e.type === "folder");
  let files = entries.filter(e => e.type === "file");

  files.sort((a,b) => {{
    let va = a[sortKey];
    let vb = b[sortKey];
    if (sortKey === "name") {{
      va = (va || "").toLowerCase();
      vb = (vb || "").toLowerCase();
      if (va < vb) return sortDir === "asc" ? -1 : 1;
      if (va > vb) return sortDir === "asc" ?  1 : -1;
      return 0;
    }} else {{
      // mtime number
      return sortDir === "asc" ? (va - vb) : (vb - va);
    }}
  }});

  const finalList = folders.concat(files);
  countChipEl.textContent = finalList.length + " 个条目";

  listEl.innerHTML = finalList.map((e, i) => {{
    const delay = 40 + i * 40;
    if (e.type === "folder") {{
      return `
<li class="card" style="animation-delay:${{delay}}ms">
  <a class="card-link" href="javascript:void(0)" onclick="renderFolder('${{e.name}}')">
    <span class="card-title">📁 ${{escapeHtml(e.name)}}</span>
    <span class="card-meta">${{escapeHtml(e.path)}}</span>
  </a>
</li>`;
    }} else {{
      return `
<li class="card" style="animation-delay:${{delay}}ms">
  <a class="card-link" href="${{escapeHtml(e.path)}}" title="${{escapeHtml(e.path)}}">
    <span class="card-title">📄 ${{escapeHtml(e.name)}}</span>
    <span class="card-meta">${{escapeHtml(e.path)}}</span>
    <span class="card-meta">修改时间：${{escapeHtml(e.mtime_str)}}</span>
  </a>
</li>`;
    }}
  }}).join("\\n");
}}

function escapeHtml(s) {{
  return (s || "")
    .replaceAll("&","&amp;")
    .replaceAll("<","&lt;")
    .replaceAll(">","&gt;")
    .replaceAll('"',"&quot;")
    .replaceAll("'","&#39;");
}}

// 事件绑定
sortNameBtn.onclick = () => {{
  sortKey = "name";
  setActive(sortNameBtn, true);
  setActive(sortTimeBtn, false);
  rerender();
}};
sortTimeBtn.onclick = () => {{
  sortKey = "mtime";
  setActive(sortNameBtn, false);
  setActive(sortTimeBtn, true);
  rerender();
}};
sortAscBtn.onclick = () => {{
  sortDir = "asc";
  setActive(sortAscBtn, true);
  setActive(sortDescBtn, false);
  rerender();
}};
sortDescBtn.onclick = () => {{
  sortDir = "desc";
  setActive(sortAscBtn, false);
  setActive(sortDescBtn, true);
  rerender();
}};
backBtn.onclick = () => renderRoot();

function rerender() {{
  if (currentFolder === "__root__") renderRoot();
  else renderFolder(currentFolder);
}}

renderRoot();
</script>
</body>
</html>
"""

if __name__ == "__main__":
    folders, root_files, files_by_folder = collect_entries()
    OUT_FILE.write_text(build_index(folders, root_files, files_by_folder), encoding="utf-8")
    total_files = sum(len(v) for v in files_by_folder.values()) if files_by_folder else 0
    print(f"Generated {OUT_FILE} with {len(folders)} folders and {total_files} html files.")

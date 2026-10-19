#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
把 roadmap.md 构建成 index.html（单文件、零外部依赖）。

用法：
    python3 tools/build_html.py

说明：
- 依赖标准库，无第三方包。
- ```mermaid 代码块会被替换成本项目自带的内联 SVG / CSS 图示
  （GitHub Pages 上的 index.html 不加载 mermaid.js，保证离线可用）。
- 若新增图示，请在 code_block() 里补一条分支，并同时保证 GitHub 能渲染。

注意：docstring 之后是原脚本内容，直接运行即可。
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""把 计算机学习路径_通俗版.md 转成带配色/图示的单页 HTML。"""
import html
import re
import sys

SRC = sys.argv[1] if len(sys.argv) > 1 else "roadmap.md"
OUT = sys.argv[2] if len(sys.argv) > 2 else "index.html"

# ---------------------------------------------------------------- 图示

DEP_SVG = """
<figure class="dgm-wrap">
<svg viewBox="0 0 720 672" class="dgm" role="img" aria-label="知识依赖关系图">
<defs><marker id="ar" markerWidth="9" markerHeight="9" refX="7" refY="4" orient="auto">
<path d="M0,0 L8,4 L0,8 Z" class="arhead"/></marker></defs>

<rect class="box" x="180" y="20" width="360" height="52" rx="12"/>
<text class="t1" x="360" y="52">P0 学习基建 · 工具 · AI · 信息渠道</text>

<rect class="box" x="180" y="112" width="360" height="52" rx="12"/>
<text class="t1" x="360" y="144">P1 Java 语言 · 表达力</text>

<rect class="box" x="180" y="204" width="360" height="52" rx="12"/>
<text class="t1" x="360" y="236">P2 数据结构与算法 · 组织力</text>

<rect class="box box-key" x="180" y="296" width="360" height="52" rx="12"/>
<text class="t1" x="360" y="328">P3 操作系统 → 计算机网络 · 结构力</text>

<rect class="box" x="90" y="388" width="250" height="52" rx="12"/>
<text class="t1" x="215" y="420">P4 数据库 · 持久力</text>

<rect class="box" x="380" y="388" width="250" height="52" rx="12"/>
<text class="t1" x="505" y="420">P5 工程工具 · 协作力</text>

<rect class="box box-key" x="180" y="480" width="360" height="52" rx="12"/>
<text class="t1" x="360" y="512">P6 Spring 后端 · 能交付系统</text>

<rect class="box box-goal" x="180" y="572" width="360" height="52" rx="12"/>
<text class="t1" x="360" y="604">P7 AI 应用开发 · 智能力</text>

<!-- 主链箭头 -->
<line class="arrow" x1="360" y1="72" x2="360" y2="106" marker-end="url(#ar)"/>
<line class="arrow" x1="360" y1="164" x2="360" y2="198" marker-end="url(#ar)"/>
<line class="arrow" x1="360" y1="256" x2="360" y2="290" marker-end="url(#ar)"/>
<path class="arrow" d="M360,348 V366 H215 V382" marker-end="url(#ar)"/>
<path class="arrow" d="M360,348 V366 H505 V382" marker-end="url(#ar)"/>
<path class="arrow" d="M215,440 V458 H360 V474" marker-end="url(#ar)"/>
<path class="arrow" d="M505,440 V458 H360 V474" marker-end="url(#ar)"/>
<line class="arrow" x1="360" y1="532" x2="360" y2="566" marker-end="url(#ar)"/>

<!-- 算法平行轨 -->
<rect class="box box-dash" x="556" y="204" width="144" height="52" rx="12"/>
<text class="t2" x="628" y="227">P2 算法</text>
<text class="t2" x="628" y="245">每天 30 分钟</text>
<line class="dash" x1="540" y1="230" x2="552" y2="230" marker-end="url(#ar)"/>
<line class="dash" x1="628" y1="256" x2="628" y2="628" marker-end="url(#ar)"/>
<text class="t3" x="628" y="652">跑到最后一天</text>

<!-- 说明 -->
<text class="t3" x="470" y="348" ></text>
</svg>
<figcaption>↑ 箭头读作"建立在这之上"。这张图是全篇的骨架：<b>你不能在没装水电的房子里装智能家居。</b></figcaption>
</figure>
"""

LOOP_SVG = """
<figure class="dgm-wrap">
<svg viewBox="0 0 860 178" class="dgm" role="img" aria-label="每日 90 分钟学习闭环">
<defs><marker id="ar2" markerWidth="9" markerHeight="9" refX="7" refY="4" orient="auto">
<path d="M0,0 L8,4 L0,8 Z" class="arhead"/></marker></defs>

<text class="t3" x="95" y="16">10 分钟</text>
<text class="t3" x="265" y="16">30 分钟</text>
<text class="t3" x="435" y="16">30 分钟</text>
<text class="t3" x="605" y="16">15 分钟</text>
<text class="t3" x="775" y="16">5 分钟</text>

<rect class="box" x="20" y="30" width="150" height="54" rx="12"/>
<text class="t1" x="95" y="63">① 复习</text>
<rect class="box box-key" x="190" y="30" width="150" height="54" rx="12"/>
<text class="t1" x="265" y="63">② 读</text>
<rect class="box box-key" x="360" y="30" width="150" height="54" rx="12"/>
<text class="t1" x="435" y="63">③ 写代码</text>
<rect class="box" x="530" y="30" width="150" height="54" rx="12"/>
<text class="t1" x="605" y="63">④ 问 AI</text>
<rect class="box" x="700" y="30" width="150" height="54" rx="12"/>
<text class="t1" x="775" y="63">⑤ 复盘</text>

<line class="arrow" x1="172" y1="57" x2="186" y2="57" marker-end="url(#ar2)"/>
<line class="arrow" x1="342" y1="57" x2="356" y2="57" marker-end="url(#ar2)"/>
<line class="arrow" x1="512" y1="57" x2="526" y2="57" marker-end="url(#ar2)"/>
<line class="arrow" x1="682" y1="57" x2="696" y2="57" marker-end="url(#ar2)"/>

<path class="loopback" d="M775,84 V140 H95 V90" marker-end="url(#ar2)"/>
<text class="t2" x="435" y="134">第二天从「复习」接着来</text>
</svg>
<figcaption>↑ <b>顺序不能反：读 → 写 → 问。</b>先写代码，你的问题会具体十倍。</figcaption>
</figure>
"""

GANTT = """
<figure class="dgm-wrap">
<div class="gantt">
  <div class="g-head"><span class="g-label"></span><span class="g-scale"><i>1</i><i>3</i><i>6</i><i>9</i><i>12</i><i>15</i><i>18</i></span></div>
  <div class="g-row"><span class="g-label">P0 基建</span><span class="g-track"><b class="bar b0" style="left:0%;width:2.8%"></b></span></div>
  <div class="g-row"><span class="g-label">P1 Java</span><span class="g-track"><b class="bar b1" style="left:2.8%;width:13.9%"></b></span></div>
  <div class="g-row"><span class="g-label">P2 算法</span><span class="g-track"><b class="bar bar-dash" style="left:2.8%;width:97.2%"></b></span></div>
  <div class="g-row"><span class="g-label">P3 OS</span><span class="g-track"><b class="bar b3" style="left:16.7%;width:11.1%"></b></span></div>
  <div class="g-row"><span class="g-label">P3 网络</span><span class="g-track"><b class="bar b3" style="left:27.8%;width:8.3%"></b></span></div>
  <div class="g-row"><span class="g-label">P4 数据库</span><span class="g-track"><b class="bar b4" style="left:36.1%;width:11.1%"></b></span></div>
  <div class="g-row"><span class="g-label">P5 工程</span><span class="g-track"><b class="bar bar-dash" style="left:5.6%;width:66.7%"></b></span></div>
  <div class="g-row"><span class="g-label">P6 后端</span><span class="g-track"><b class="bar b6" style="left:47.2%;width:25%"></b></span></div>
  <div class="g-row"><span class="g-label">P7 AI</span><span class="g-track"><b class="bar b7" style="left:72.2%;width:19.4%"></b></span></div>
  <div class="g-row"><span class="g-label">P8 项目</span><span class="g-track"><b class="bar bar-dash" style="left:47.2%;width:44.4%"></b></span></div>
</div>
<figcaption>↑ 横轴是"第几个月"（按每周 8–12 小时估）。<b>虚线 = 并行的轨</b>，实线 = 主线。</figcaption>
</figure>
"""

TREE = """
<figure class="dgm-wrap">
<div class="ladder">
  <div class="step s4"><b>L4 改造</b><span>能改代码、调参数、排故障、做取舍</span></div>
  <div class="step s3"><b>L3 迁移</b><span>换个场景 / 换个技术，还能用</span></div>
  <div class="step s2"><b>L2 因果</b><span>能回答"为什么这样设计？不这样会怎样？"</span></div>
  <div class="step s1"><b>L1 记忆</b><span>能说出名词和步骤</span></div>
</div>
<figcaption>↑ 越往上越窄：<b>大多数人停在 L1，还以为自己到了 L4。</b></figcaption>
</figure>
"""

# ---------------------------------------------------------------- 工具函数

def inline(s):
    """行内标记：先保护代码，再处理粗体/斜体/链接。"""
    codes = []

    def stash(m):
        codes.append(m.group(1))
        return f"\x00{len(codes)-1}\x00"

    s = re.sub(r"`([^`]+)`", stash, s)
    s = html.escape(s, quote=False)
    s = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2">\1</a>', s)
    s = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", s)
    s = re.sub(r"(?<![*\w])\*([^*\n]+?)\*(?!\*)", r"<em>\1</em>", s)

    def pop(m):
        return "<code>" + html.escape(codes[int(m.group(1))], quote=False) + "</code>"

    s = re.sub(r"\x00(\d+)\x00", pop, s)
    return s


def callout(kind, body_lines):
    meta = {
        "NOTE": ("note", "📌", "说明"),
        "TIP": ("tip", "💡", "要点"),
        "IMPORTANT": ("imp", "🔑", "重点"),
        "WARNING": ("warn", "⚠️", "注意"),
        "CAUTION": ("danger", "🛑", "警告"),
    }[kind]
    cls, icon, label = meta
    body = "<br>".join(inline(x) for x in body_lines)
    return (f'<div class="callout {cls}"><span class="c-ico">{icon}</span>'
            f'<div class="c-body"><b class="c-label">{label}</b>{body}</div></div>')


def code_block(lang, code):
    if lang == "mermaid":
        c = code.strip()
        if c.startswith("gantt"):
            return GANTT
        if "L1 记忆" in c:
            return TREE
        if "① 复习" in c:
            return LOOP_SVG
        return DEP_SVG
    if lang == "dep":
        return DEP_SVG
    if lang == "loop":
        return LOOP_SVG
    if lang == "gantt":
        return GANTT
    if lang == "tree":
        return TREE
    body = html.escape(code)
    return (f'<div class="codeblock"><button class="copy" aria-label="复制">复制</button>'
            f'<pre><code>{body}</code></pre></div>')


def slug(text):
    t = re.sub(r"[^\w\u4e00-\u9fff]+", "-", text).strip("-").lower()
    return t[:40] or "s"


# ---------------------------------------------------------------- 解析

src = open(SRC, encoding="utf-8").read().split("\n")
# 跳过 hero 覆盖的部分
start = 0
while start < len(src) and not src[start].startswith("## "):
    start += 1
lines = src[start:]

out, toc = [], []
prompts = []
last_sub_text = ""
i = 0
ul_open = ol_open = False
h2_n = 0
task_n = 0
cur_phase = False
last_h2 = ""


def close_lists():
    global ul_open, ol_open
    buf = ""
    if ul_open:
        buf += "</ul>"
        ul_open = False
    if ol_open:
        buf += "</ol>"
        ol_open = False
    return buf


while i < len(lines):
    line = lines[i]
    stripped = line.strip()

    # 空行
    if not stripped:
        out.append(close_lists())
        i += 1
        continue

    # 代码块
    m = re.match(r"^```(\w*)\s*$", stripped)
    if m:
        out.append(close_lists())
        lang = m.group(1)
        i += 1
        buf = []
        while i < len(lines) and not lines[i].strip().startswith("```"):
            buf.append(lines[i])
            i += 1
        i += 1
        _code = "\n".join(buf)
        _pm = re.match(r"^([\u2460-\u2467])\s*(.*)$", last_sub_text.strip())
        if lang == "" and _pm:
            prompts.append({"n": _pm.group(1), "title": last_sub_text.strip(), "code": _code})
        out.append(code_block(lang, _code))
        continue

    # 标题
    m = re.match(r"^(#{1,4})\s+(.*)$", stripped)
    if m:
        out.append(close_lists())
        level, text = len(m.group(1)), m.group(2).strip()
        if level == 2:
            h2_n += 1
            aid = f"sec-{h2_n}"
            last_h2 = text
            toc.append((2, aid, text))
            out.append(f'<h2 id="{aid}"><span class="h2-num">{text.split(".")[0] if re.match(r"^\\d+\\.", text) else ""}</span>{inline(re.sub(r"^\\d+\\.\\s*", "", text))}</h2>')
        elif level == 3:
            pm = re.match(r"^(P\d)\s*·\s*(.*)$", text)
            if pm:
                aid = f"phase-{pm.group(1).lower()}"
                toc.append((3, aid, f"{pm.group(1)} · {pm.group(2)}"))
                out.append(f'<section class="phase" id="{aid}"><h3><span class="p-badge">{pm.group(1)}</span>{inline(pm.group(2))}</h3>')
                cur_phase = True
            else:
                aid = slug(text)
                out.append(f'<h3 id="{aid}">{inline(text)}</h3>')
        elif level == 4:
            out.append(f"<h4>{inline(text)}</h4>")
        else:
            out.append(f"<p class=\"tiny\">{inline(text)}</p>")
        i += 1
        continue

    # 分隔线
    if stripped == "---":
        out.append(close_lists())
        out.append("</section>" if cur_phase else "")
        cur_phase = False
        out.append("<hr>")
        i += 1
        continue

    # 表格
    if stripped.startswith("|") and i + 1 < len(lines) and re.match(r"^\|[\s:\-|]+\|?$", lines[i + 1].strip()):
        out.append(close_lists())
        header = [c.strip() for c in stripped.strip("|").split("|")]
        i += 2
        rows = []
        while i < len(lines) and lines[i].strip().startswith("|"):
            rows.append([c.strip() for c in lines[i].strip().strip("|").split("|")])
            i += 1
        has_head = any(h for h in header)
        cls = "table" + ("" if has_head else " table-plain")
        html_t = [f'<div class="table-wrap"><table class="{cls}">']
        if has_head:
            html_t.append("<thead><tr>" + "".join(f"<th>{inline(h)}</th>" for h in header) + "</tr></thead>")
        html_t.append("<tbody>")
        for r in rows:
            cells = "".join(f"<td>{inline(c)}</td>" for c in r)
            html_t.append(f"<tr>{cells}</tr>")
        html_t.append("</tbody></table></div>")
        out.append("".join(html_t))
        continue

    # 引用 / 提示框
    if stripped.startswith(">"):
        out.append(close_lists())
        block = []
        while i < len(lines) and lines[i].strip().startswith(">"):
            block.append(lines[i].strip()[1:].strip())
            i += 1
        first = block[0]
        am = re.match(r"^\[!(\w+)\]$", first)
        if am:
            body = [b for b in block[1:] if b]
            out.append(callout(am.group(1).upper(), body))
        else:
            text = "<br>".join(inline(b) for b in block if b)
            plain = re.sub(r"<[^>]+>", "", text)
            if "最后一句" in last_h2:
                cls = "ending"
            else:
                cls = "pullquote" if len(plain) <= 60 else "quote"
            out.append(f'<blockquote class="{cls}">{text}</blockquote>')
        continue

    # 列表
    if re.match(r"^[-*]\s+", stripped) or re.match(r"^\d+\.\s+", stripped):
        ordered = bool(re.match(r"^\d+\.\s+", stripped))
        if ordered and not ol_open:
            out.append(close_lists())
            out.append("<ol>")
            ol_open = True
        if not ordered and not ul_open:
            out.append(close_lists())
            out.append("<ul>")
            ul_open = True
        item = re.sub(r"^([-*]|\d+\.)\s+", "", stripped)
        if item.startswith("[ ]"):
            item = item[3:].strip()
            task_n += 1
            out.append(f'<li class="task"><label><input type="checkbox" data-k="{task_n}">'
                       f'<span class="cbt"></span><span class="ctxt">{inline(item)}</span></label></li>')
        else:
            out.append(f"<li>{inline(item)}</li>")
        i += 1
        continue

    # 段落
    out.append(close_lists())
    buf = [stripped]
    i += 1
    while i < len(lines) and lines[i].strip() and not re.match(r"^(#{1,4}\s|```|\||>|---|- |\* |\d+\. )", lines[i].strip()):
        buf.append(lines[i].strip())
        i += 1
    para = " ".join(buf)
    if para.startswith("<"):
        out.append(para)
    elif re.match(r"^\*\*[^*]+\*\*$", para):
        last_sub_text = para[2:-2]
        out.append(f'<h4 class="sub">{inline(para[2:-2])}</h4>')
    else:
        out.append(f"<p>{inline(para)}</p>")

out.append(close_lists())
if cur_phase:
    out.append("</section>")

body = "\n".join(x for x in out if x)

# 在三张清单标题后插入「进度统计 / 导入导出」工具条
TOOLBAR = """<div class="ck-tools" id="ck-tools">
  <div class="ck-tools-h">📊 已完成 <b id="ck-count">0</b> / <b id="ck-total">0</b> 项 · 勾选会自动保存在本机浏览器</div>
  <div class="ck-bar"><i id="ck-fill"></i></div>
  <div class="ck-btns">
    <button type="button" id="ck-export">导出进度</button>
    <button type="button" id="ck-import">导入</button>
    <input type="file" id="ck-file" accept=".json,application/json" hidden>
    <button type="button" id="ck-reset">重置</button>
  </div>
  <div class="ck-tip">换电脑 / 换浏览器时：先「导出」，在新设备上「导入」，勾选不会丢。</div>
</div>"""

_m = re.search(r'<h2 id="sec-\d+">(?:(?!</h2>).)*三张清单(?:(?!</h2>).)*</h2>', body, re.S)
if _m:
    body = body[:_m.end()] + TOOLBAR + body[_m.end():]

# ---- 提示词抽屉 ----
def _render_prompts(ps):
    if not ps:
        return ""
    cards = []
    for idx, p in enumerate(ps):
        t = html.escape(p["title"])
        code = html.escape(p["code"])
        cards.append(
            '<article class="p-card" data-n="%s">'
            '<div class="p-card-h"><span class="p-num">%s</span>'
            '<span class="p-title">%s</span>'
            '<button type="button" class="p-copy">复制</button></div>'
            '<input class="p-topic" type="text" placeholder="可选：填个具体对象（如 HashMap），自动套进模板">'
            '<textarea class="p-body" rows="3" spellcheck="false">%s</textarea>'
            '</article>' % (p["n"], p["n"], t, code)
        )
    return (PROMPT_FAB + PROMPT_DIALOG_HEAD + "".join(cards) + PROMPT_DIALOG_TAIL)


# TOC
toc_html = ['<div class="toc-title">目录</div><ul class="toc-list">']
open_sub = False
for level, aid, text in toc:
    if level == 2:
        if open_sub:
            toc_html.append("</ul></li>")
            open_sub = False
        toc_html.append(f'<li><a href="#{aid}">{inline(text)}</a>')
        toc_html.append("<ul>")
        open_sub = True
    else:
        if not open_sub:
            toc_html.append("<li><ul>")
            open_sub = True
        toc_html.append(f'<li><a href="#{aid}">{inline(text)}</a></li>')
if open_sub:
    toc_html.append("</ul></li>")
toc_html.append("</ul>")
toc_html = "".join(toc_html)
toc_html += '<div class="toc-note">☑️ 清单里打勾会自动保存在本机浏览器<br>🖨️ 可直接打印 / 存为 PDF</div>'
toc_mobile = '<details class="toc-mobile"><summary>📑 目录（点开）</summary>' + toc_html + '</details>'

CSS = r"""
:root{
  --paper:#fbf9f4; --card:#ffffff; --ink:#1a1b1e; --ink-2:#3d4046; --muted:#6b7280;
  --line:#e8e3d9; --line-2:#f0ece3;
  --red:#b3392b; --red-soft:#fdf1ef;
  --blue:#1d4ed8; --blue-soft:#eff4ff;
  --green:#0f766e; --green-soft:#ecfdf5;
  --amber:#b45309; --amber-soft:#fff8ec;
  --purple:#6d28d9; --purple-soft:#f5f1ff;
  --hl:#ffe9a8;
  --shadow:0 1px 2px rgba(24,20,12,.04),0 10px 30px -18px rgba(24,20,12,.18);
  --radius:14px;
}
@media (prefers-color-scheme: dark){
  :root{
    --paper:#131416; --card:#1b1d20; --ink:#e9e7e3; --ink-2:#c6c4bf; --muted:#9aa0a8;
    --line:#2b2e33; --line-2:#24272b;
    --red:#e8837a; --red-soft:#2a1c1a;
    --blue:#93b4ff; --blue-soft:#18203a;
    --green:#5eead4; --green-soft:#112622;
    --amber:#f0b463; --amber-soft:#2a2116;
    --purple:#c4b5fd; --purple-soft:#211a35;
    --hl:#5a4a1c;
    --shadow:0 1px 2px rgba(0,0,0,.3),0 10px 30px -18px rgba(0,0,0,.8);
  }
}
*{box-sizing:border-box}
html{scroll-behavior:smooth}
body{
  margin:0;background:var(--paper);color:var(--ink);
  font-family:-apple-system,BlinkMacSystemFont,"PingFang SC","Hiragino Sans GB","Noto Sans SC","Microsoft YaHei",sans-serif;
  font-size:17px;line-height:1.9;-webkit-font-smoothing:antialiased;
}
.progress{position:fixed;top:0;left:0;right:0;height:3px;background:transparent;z-index:99}
.progress>div{height:100%;width:0;background:linear-gradient(90deg,var(--red),var(--amber))}

/* ---------- hero ---------- */
.hero{
  padding:72px 24px 40px;max-width:900px;margin:0 auto;text-align:left;
  border-bottom:1px solid var(--line-2);
}
.kicker{display:inline-block;font-size:13px;letter-spacing:.18em;color:var(--red);
  border:1px solid var(--red);border-radius:999px;padding:3px 12px;margin-bottom:22px}
.hero h1{font-size:clamp(30px,5vw,52px);line-height:1.22;margin:0 0 14px;letter-spacing:-.02em;font-weight:800}
.hero h1 em{font-style:normal;background:linear-gradient(transparent 62%,var(--hl) 62%)}
.hero .sub{font-size:clamp(16px,2vw,20px);color:var(--ink-2);margin:0 0 26px;line-height:1.7}
.chips{display:flex;flex-wrap:wrap;gap:8px;margin-bottom:26px}
.chip{font-size:13px;color:var(--muted);background:var(--card);border:1px solid var(--line);
  border-radius:999px;padding:4px 12px;box-shadow:var(--shadow)}
.hero blockquote{margin:0;padding:18px 22px;border-left:4px solid var(--red);
  background:var(--red-soft);border-radius:0 var(--radius) var(--radius) 0;
  font-family:Georgia,"Songti SC",serif;font-size:18px;color:var(--ink-2)}

/* ---------- layout ---------- */
.layout{max-width:1180px;margin:0 auto;display:grid;grid-template-columns:minmax(0,1fr);gap:40px;padding:40px 24px 120px}
@media(min-width:1080px){ .layout{grid-template-columns:230px minmax(0,760px);justify-content:center} }
.toc{display:none}
@media(min-width:1080px){
  .toc{display:block;position:sticky;top:24px;align-self:start;max-height:calc(100vh - 48px);overflow:auto;
    font-size:13.5px;line-height:1.65;padding-right:8px}
}
.toc-title{font-weight:700;font-size:12px;letter-spacing:.16em;color:var(--muted);
  text-transform:uppercase;margin-bottom:12px}
.toc-list,.toc-list ul{list-style:none;margin:0;padding:0}
.toc-list ul{margin-left:10px;border-left:1px solid var(--line);padding-left:9px;display:block;font-size:12.5px;margin-top:2px;margin-bottom:6px}
.toc-list li{margin:2px 0}
.toc-list a{color:var(--muted);text-decoration:none;display:block;padding:2px 6px;border-radius:6px}
.toc-list a:hover{color:var(--ink);background:var(--line-2)}
.toc-list a.on{color:var(--red);font-weight:600;background:var(--red-soft)}

/* ---------- content ---------- */
.content{max-width:760px;min-width:0}
.content h2{
  font-size:clamp(23px,3vw,30px);line-height:1.35;margin:64px 0 18px;font-weight:800;letter-spacing:-.01em;
  padding-top:22px;border-top:1px solid var(--line-2);scroll-margin-top:24px;
}
.content h2:first-of-type{border-top:0;margin-top:8px}
.h2-num{color:var(--red);font-variant-numeric:tabular-nums;margin-right:.35em;font-weight:800}
.content h3{font-size:20px;margin:38px 0 12px;font-weight:700;scroll-margin-top:24px}
.content h4{font-size:17px;margin:26px 0 10px;color:var(--ink-2)}
.content p{margin:0 0 18px;color:var(--ink-2)}
.content strong{font-weight:700;color:var(--ink);background:linear-gradient(transparent 62%,var(--hl) 62%);padding:0 1px}
.content em{font-style:normal;color:var(--red);font-weight:600}
.content a{color:var(--blue);text-decoration:none;border-bottom:1px solid color-mix(in srgb,var(--blue) 30%,transparent);overflow-wrap:break-word}
.content a:hover{border-bottom-color:var(--blue)}
.content ul,.content ol{margin:0 0 18px;padding-left:22px}
.content li{margin:7px 0;color:var(--ink-2)}
.content li::marker{color:var(--red)}
.content hr{border:0;height:1px;background:var(--line-2);margin:40px 0}

/* 阶段卡片 */
.phase{margin:26px 0;padding:22px 24px 8px;background:var(--card);border:1px solid var(--line);
  border-radius:var(--radius);box-shadow:var(--shadow)}
.phase h3{margin:0 0 14px;display:flex;align-items:center;gap:12px;font-size:21px}
.p-badge{display:inline-flex;align-items:center;justify-content:center;min-width:52px;height:30px;padding:0 10px;
  border-radius:8px;background:var(--red);color:#fff;font-size:14px;font-weight:800;letter-spacing:.04em}
.phase ul{padding-left:20px}

/* 引用 */
blockquote.quote{margin:24px 0;padding:16px 20px;border-left:4px solid var(--line);
  background:var(--line-2);border-radius:0 10px 10px 0;color:var(--ink-2);font-size:16px}
blockquote.pullquote{margin:30px 0;padding:0 0 0 22px;border-left:5px solid var(--red);
  font-family:Georgia,"Songti SC","Songti TC",serif;font-size:22px;line-height:1.6;color:var(--ink);font-weight:600}
blockquote.pullquote strong{background:none}
blockquote.ending{margin:28px 0 44px;padding:30px 32px;border:1px solid var(--line);
  border-left:5px solid var(--red);border-radius:var(--radius);
  background:linear-gradient(180deg,var(--red-soft),var(--card));
  font-family:Georgia,"Songti SC","Songti TC",serif;font-size:19px;line-height:1.9;
  color:var(--ink);box-shadow:var(--shadow)}
blockquote.ending strong{background:none;font-size:22px;display:inline-block;margin-bottom:6px}

/* 提示框 */
.callout{display:flex;gap:14px;margin:22px 0;padding:16px 18px;border-radius:var(--radius);
  border:1px solid var(--line);background:var(--card);box-shadow:var(--shadow);align-items:flex-start}
.callout .c-ico{font-size:20px;line-height:1.4}
.callout .c-label{display:block;font-size:12px;letter-spacing:.12em;color:var(--muted);margin-bottom:2px}
.callout.note{background:var(--blue-soft);border-color:color-mix(in srgb,var(--blue) 25%,var(--line))}
.callout.tip{background:var(--green-soft);border-color:color-mix(in srgb,var(--green) 25%,var(--line))}
.callout.imp{background:var(--purple-soft);border-color:color-mix(in srgb,var(--purple) 25%,var(--line))}
.callout.warn{background:var(--amber-soft);border-color:color-mix(in srgb,var(--amber) 25%,var(--line))}
.callout.danger{background:var(--red-soft);border-color:color-mix(in srgb,var(--red) 30%,var(--line))}

/* 小标题 */
.content h4.sub{font-size:15.5px;letter-spacing:.02em;font-weight:700;color:var(--ink);
  margin:30px 0 10px;padding:2px 0 2px 11px;border-left:3px solid var(--red);line-height:1.5}
.content h4.sub strong{background:none}

/* 可打勾清单 */
li.task{list-style:none;margin-left:-20px}
li.task label{display:flex;gap:10px;align-items:flex-start;cursor:pointer;user-select:none}
li.task input{position:absolute;opacity:0;width:0;height:0}
li.task .cbt{flex:0 0 18px;height:18px;margin-top:5px;border:1.6px solid var(--muted);
  border-radius:5px;background:var(--card);position:relative;transition:.16s}
li.task label:hover .cbt{border-color:var(--red)}
li.task input:checked + .cbt{background:var(--red);border-color:var(--red)}
li.task input:checked + .cbt::after{content:"";position:absolute;left:5px;top:1.5px;width:5px;height:9px;
  border:solid #fff;border-width:0 2px 2px 0;transform:rotate(43deg)}
li.task input:checked ~ .ctxt{color:var(--muted);text-decoration:line-through}
.toc-note{margin-top:14px;padding-top:12px;border-top:1px solid var(--line);font-size:11.5px;
  color:var(--muted);line-height:1.6}

/* 手机目录 */
.toc-mobile{display:block;margin:0 0 10px}
@media(min-width:1080px){.toc-mobile{display:none}}
.toc-mobile summary{cursor:pointer;font-size:14px;color:var(--ink-2);padding:12px 16px;
  border:1px solid var(--line);border-radius:12px;background:var(--card);box-shadow:var(--shadow)}
.toc-mobile[open] summary{border-radius:12px 12px 0 0}
.toc-mobile .toc-list{font-size:14px;padding:12px 16px 16px;border:1px solid var(--line);
  border-top:0;border-radius:0 0 12px 12px;background:var(--card)}

/* 表格 */
.table-wrap{overflow-x:auto;margin:20px 0;border:1px solid var(--line);border-radius:var(--radius);
  background:var(--card);box-shadow:var(--shadow)}
table.table{width:100%;border-collapse:collapse;font-size:15.5px}
table.table th{background:var(--line-2);text-align:left;font-weight:700;padding:12px 14px;color:var(--ink);
  border-bottom:1px solid var(--line);white-space:nowrap}
table.table td{padding:11px 14px;border-bottom:1px solid var(--line-2);color:var(--ink-2);vertical-align:top}
table.table td:first-child{white-space:nowrap}
table.table tr:last-child td{border-bottom:0}
table.table tbody tr:hover{background:color-mix(in srgb,var(--hl) 14%,transparent)}
table.table-plain td:first-child{white-space:nowrap;color:var(--ink)}

/* 复选框 */
li.task{list-style:none;margin-left:-20px;display:flex;gap:10px;align-items:flex-start}
li.task .cb{flex:0 0 16px;height:16px;margin-top:7px;border:1.5px solid var(--muted);border-radius:4px}

/* 代码 */
.codeblock{position:relative;margin:18px 0}
.codeblock pre{margin:0;padding:18px 18px;background:var(--card);border:1px solid var(--line);
  border-radius:var(--radius);overflow-x:auto;box-shadow:var(--shadow)}
.codeblock code{font-family:"SF Mono",ui-monospace,Menlo,Consolas,monospace;font-size:14px;line-height:1.75;
  color:var(--ink-2);white-space:pre-wrap}
.codeblock .copy{position:absolute;top:10px;right:10px;font-size:12px;padding:4px 10px;border-radius:8px;
  border:1px solid var(--line);background:var(--paper);color:var(--muted);cursor:pointer;opacity:0;transition:.2s}
.codeblock:hover .copy{opacity:1}
.codeblock .copy:hover{color:var(--red);border-color:var(--red)}

/* 图示 */
.dgm-wrap{margin:26px 0;padding:24px 18px 14px;background:var(--card);border:1px solid var(--line);
  border-radius:var(--radius);box-shadow:var(--shadow);overflow-x:auto}
.dgm{display:block;width:100%;height:auto;min-width:560px}
.dgm .box{fill:var(--card);stroke:var(--line);stroke-width:1.5}
.dgm .box-key{stroke:color-mix(in srgb,var(--red) 45%,var(--line));stroke-width:2;
  fill:color-mix(in srgb,var(--red-soft) 60%,var(--card))}
.dgm .box-goal{stroke:color-mix(in srgb,var(--amber) 60%,var(--line));stroke-width:2;
  fill:color-mix(in srgb,var(--amber-soft) 65%,var(--card))}
.dgm .box-dash{stroke:var(--muted);stroke-dasharray:5 4;fill:transparent}
.dgm .t1{fill:var(--ink);font-size:14.5px;font-weight:600;text-anchor:middle;
  font-family:-apple-system,"PingFang SC","Noto Sans SC",sans-serif}
.dgm .t2{fill:var(--ink-2);font-size:13px;text-anchor:middle;font-family:-apple-system,"PingFang SC",sans-serif}
.dgm .t3{fill:var(--muted);font-size:11.5px;text-anchor:middle;font-family:-apple-system,"PingFang SC",sans-serif}
.dgm .arrow{stroke:var(--red);stroke-width:1.8;fill:none}
.dgm .loopback{stroke:var(--muted);stroke-width:1.6;fill:none;stroke-dasharray:6 4}
.dgm .dash{stroke:var(--muted);stroke-width:1.5;fill:none;stroke-dasharray:5 4}
.dgm .arhead{fill:var(--red)}
.dgm-wrap::after{content:"← 左右滑动可看全图 →";display:none;text-align:center;font-size:12px;color:var(--muted);margin-top:8px}
.dgm-wrap.scrollable::after{display:block}
.dgm-wrap figcaption{margin-top:14px;font-size:13.5px;color:var(--muted);text-align:center;line-height:1.7}
.dgm-wrap figcaption b{color:var(--red)}

/* gantt */
.gantt{font-size:13px;min-width:560px}
.g-head,.g-row{display:grid;grid-template-columns:92px 1fr;align-items:center;gap:10px}
.g-head{margin-bottom:8px}
.g-scale{display:grid;grid-template-columns:repeat(7,1fr);color:var(--muted);font-size:11px}
.g-scale i{font-style:normal;text-align:left}
.g-row{margin:5px 0}
.g-label{color:var(--ink-2);font-size:12.5px;white-space:nowrap}
.g-track{position:relative;height:20px;background:var(--line-2);border-radius:6px;
  background-image:repeating-linear-gradient(90deg,var(--line) 0 1px,transparent 1px 16.66%)}
.bar{position:absolute;top:0;height:20px;border-radius:6px;display:block}
.bar-dash{background:repeating-linear-gradient(90deg,color-mix(in srgb,var(--blue) 35%,transparent) 0 6px,transparent 6px 11px);
  outline:1px dashed color-mix(in srgb,var(--blue) 50%,transparent);outline-offset:-1px}
.b0{background:var(--muted)}
.b1{background:var(--green)}
.b3{background:var(--amber)}
.b4{background:var(--purple)}
.b6{background:var(--blue)}
.b7{background:var(--red)}

/* ladder */
.ladder{display:flex;flex-direction:column;align-items:center;gap:8px}
.step{display:flex;align-items:baseline;gap:12px;padding:12px 16px;border-radius:10px;
  border:1px solid var(--line);background:var(--card);box-shadow:var(--shadow)}
.step b{font-size:14px;color:var(--red);white-space:nowrap}
.step span{font-size:13.5px;color:var(--ink-2)}
.s4{width:56%}.s3{width:72%}.s2{width:88%}.s1{width:100%}
.s1{background:color-mix(in srgb,var(--line-2) 70%,var(--card))}
.s4{background:color-mix(in srgb,var(--red-soft) 70%,var(--card))}

/* 回到顶部 */
.totop{position:fixed;right:22px;bottom:22px;width:42px;height:42px;border-radius:50%;
  border:1px solid var(--line);background:var(--card);color:var(--muted);cursor:pointer;
  box-shadow:var(--shadow);font-size:18px;opacity:0;pointer-events:none;transition:.25s;z-index:50}
.totop.on{opacity:1;pointer-events:auto}
.totop:hover{color:var(--red);border-color:var(--red)}

footer{max-width:760px;margin:0 auto;padding:0 24px 80px;color:var(--muted);font-size:13px;line-height:1.9}
footer a{color:var(--muted)}

,
/* ---------- 移动端细化 ---------- */
body{padding-bottom:env(safe-area-inset-bottom)}
@media(max-width:720px){
  .hero{padding:44px 18px 28px}
  .layout{padding:22px 16px 90px}
  .phase{padding:18px 16px 4px}
  .content h2{margin-top:48px}
  blockquote.pullquote{font-size:19.5px}
  .callout{padding:14px 14px}
  .toc-mobile summary{background:var(--card)}
  /* 触摸目标放大 */
  li.task label{padding:5px 0}
  li.task .cbt{flex:0 0 22px;height:22px;margin-top:3px;border-width:1.8px}
  li.task input:checked + .cbt::after{left:6px;top:2px;width:6px;height:11px}
  /* 横向滚动容器给出手势提示 */
  .table-wrap::after{content:"← 左右滑动 →";display:none;text-align:center;font-size:11px;
    color:var(--muted);padding:5px 0 3px}
  .table-wrap.scrollable::after{display:block}
  .codeblock .copy{opacity:1}
}

/* ---------- 提示词抽屉 ---------- */
.prompt-fab{position:fixed;right:22px;bottom:76px;z-index:60;display:flex;align-items:center;gap:6px;
  padding:10px 14px;border-radius:999px;border:1px solid var(--line);background:var(--card);
  color:var(--ink-2);font-size:13px;cursor:pointer;box-shadow:var(--shadow);transition:.2s}
.prompt-fab:hover{color:var(--red);border-color:var(--red);transform:translateY(-1px)}
.prompt-fab span{font-weight:600}
.p-dialog{width:min(760px,94vw);max-height:86vh;padding:0;border:1px solid var(--line);border-radius:16px;
  background:var(--paper);color:var(--ink);box-shadow:0 24px 70px -20px rgba(0,0,0,.35)}
.p-dialog::backdrop{background:rgba(20,16,12,.45)}
.p-head{display:flex;justify-content:space-between;align-items:flex-start;gap:16px;
  padding:18px 22px 14px;border-bottom:1px solid var(--line);position:sticky;top:0;background:var(--paper);z-index:2}
.p-head b{font-size:16px}
.p-last{font-size:12px;color:var(--muted);margin-top:4px}
.p-close{border:0;background:transparent;color:var(--muted);font-size:18px;cursor:pointer;padding:2px 6px;border-radius:6px}
.p-close:hover{color:var(--red);background:var(--line-2)}
.p-close:focus-visible{outline:2px solid var(--red);outline-offset:2px}
.p-dialog:focus{outline:none}
.p-list{padding:14px 22px 6px;overflow-y:auto;max-height:calc(86vh - 140px)}
.p-card{border:1px solid var(--line);border-radius:12px;padding:12px 14px;margin-bottom:12px;background:var(--card)}
.p-card-h{display:flex;align-items:center;gap:9px;margin-bottom:8px}
.p-num{width:22px;height:22px;flex:0 0 22px;border-radius:50%;background:var(--red);color:#fff;
  font-size:12px;display:flex;align-items:center;justify-content:center;font-weight:700}
.p-title{font-size:14px;font-weight:600;color:var(--ink);line-height:1.45}
.p-copy{margin-left:auto;font-size:12px;padding:4px 11px;border-radius:7px;border:1px solid var(--line);
  background:var(--paper);color:var(--muted);cursor:pointer;flex:0 0 auto}
.p-copy:hover{color:var(--red);border-color:var(--red)}
.p-topic{width:100%;font-size:12.5px;padding:6px 10px;border:1px solid var(--line);border-radius:8px;
  background:var(--paper);color:var(--ink);margin-bottom:8px;font-family:inherit}
.p-topic:focus{outline:none;border-color:var(--red)}
.p-body{width:100%;overflow:hidden;font-family:"SF Mono",ui-monospace,Menlo,Consolas,monospace;font-size:12.5px;line-height:1.7;
  padding:10px 12px;border:1px solid var(--line);border-radius:8px;background:var(--paper);color:var(--ink-2);
  resize:vertical;min-height:74px}
.p-foot{padding:10px 22px 16px;border-top:1px solid var(--line);font-size:12px;color:var(--muted)}

/* ---------- 本周三件事 ---------- */
.week-card{margin:0 0 34px;padding:20px 22px 16px;border:1px solid var(--line);border-radius:var(--radius);
  background:linear-gradient(180deg,var(--red-soft),var(--card) 55%);box-shadow:var(--shadow)}
.wk-top{display:flex;align-items:center;gap:10px;flex-wrap:wrap;margin-bottom:6px}
.wk-badge{font-size:12px;font-weight:700;letter-spacing:.06em;color:#fff;background:var(--red);
  border-radius:999px;padding:3px 10px}
.wk-phase{font-size:14px;font-weight:700;color:var(--ink)}
.wk-btn{margin-left:auto;font-size:12px;padding:5px 12px;border-radius:8px;border:1px solid var(--line);
  background:var(--card);color:var(--muted);cursor:pointer}
.wk-btn:hover{color:var(--red);border-color:var(--red)}
.wk-tip{font-size:12.5px;color:var(--muted);margin-bottom:12px}
.wk-list{list-style:none;margin:0 0 12px;padding:0}
.wk-list li{margin:9px 0}
.wk-list li label{display:flex;gap:11px;align-items:flex-start;cursor:pointer;font-size:16px;color:var(--ink)}
.wk-list li input{position:absolute;opacity:0;width:0;height:0}
.wk-list .cbt{flex:0 0 20px;height:20px;margin-top:2px;border:1.7px solid var(--muted);border-radius:5px;
  background:var(--card);position:relative;transition:.16s}
.wk-list label:hover .cbt{border-color:var(--red)}
.wk-list input:checked + .cbt{background:var(--red);border-color:var(--red)}
.wk-list input:checked + .cbt::after{content:"";position:absolute;left:6px;top:2px;width:5px;height:9px;
  border:solid #fff;border-width:0 2px 2px 0;transform:rotate(43deg)}
.wk-foot{display:flex;justify-content:space-between;align-items:center;gap:12px;
  padding-top:12px;border-top:1px solid var(--line);font-size:12.5px;color:var(--muted)}
.wk-foot a{color:var(--blue);text-decoration:none}
.wk-done{font-size:15px;color:var(--ink);font-weight:600}

/* ---------- 进度工具条 ---------- */
.ck-tools{margin:22px 0 26px;padding:18px 20px;border:1px solid var(--line);border-radius:var(--radius);
  background:var(--card);box-shadow:var(--shadow)}
.ck-tools-h{font-size:14px;color:var(--ink-2);margin-bottom:10px}
.ck-tools-h b{color:var(--red);font-size:16px;font-variant-numeric:tabular-nums}
.ck-bar{height:8px;border-radius:99px;background:var(--line-2);overflow:hidden;margin-bottom:14px}
.ck-bar i{display:block;height:100%;width:0;border-radius:99px;
  background:linear-gradient(90deg,var(--red),var(--amber));transition:width .35s ease}
.ck-btns{display:flex;flex-wrap:wrap;gap:8px}
.ck-btns button{font-size:13px;padding:7px 14px;border-radius:9px;border:1px solid var(--line);
  background:var(--paper);color:var(--ink-2);cursor:pointer;transition:.15s}
.ck-btns button:hover{color:var(--red);border-color:var(--red)}
.ck-btns button:active{transform:translateY(1px)}
.ck-tip{font-size:12px;color:var(--muted);margin-top:10px}

@media print{
  .toc,.toc-mobile,.totop,.progress,.copy,.toc-note{display:none!important}
  body{background:#fff;font-size:12pt}
  .layout{display:block;padding:0}
  .phase,.dgm-wrap,.table-wrap,.callout{break-inside:avoid;box-shadow:none}
  .content h2,.content h3,.content h4{break-after:avoid-page}
  .ck-tools,.week-card,.prompt-fab,.p-dialog{display:none!important}
  figure,.codeblock,.callout,.table-section{break-inside:avoid}
}
"""

JS = r"""
const pbar=document.getElementById('pbar');
const totop=document.querySelector('.totop');
function onScroll(){
  const h=document.documentElement;
  const p=h.scrollTop/(h.scrollHeight-h.clientHeight);
  pbar.style.width=(p*100)+'%';
  totop.classList.toggle('on',h.scrollTop>600);
  let cur=null;
  document.querySelectorAll('.content h2[id]').forEach(el=>{
    if(el.getBoundingClientRect().top<120) cur=el.id;
  });
  document.querySelectorAll('.toc-list a').forEach(a=>{
    a.classList.toggle('on',a.getAttribute('href')==='#'+cur);
  });
}
document.addEventListener('scroll',onScroll,{passive:true});onScroll();
totop.onclick=()=>window.scrollTo({top:0,behavior:'smooth'});
/* ---------- 提示词抽屉 ---------- */
(function(){
  var dlg=document.getElementById('prompt-dialog'); if(!dlg) return;
  var fab=document.getElementById('prompt-fab');
  var cards=[].slice.call(dlg.querySelectorAll('.p-card'));
  var orig={};
  cards.forEach(function(c,i){ orig[i]=c.querySelector('.p-body').value; });
  var PH=/\[(章节|概念 A|概念 B|概念|主题|结论)\]/g;
  var lastEl=document.getElementById('p-last');

  function updateLast(){
    if(!lastEl) return;
    try{
      var d=JSON.parse(localStorage.getItem('cs-roadmap-prompt')||'null');
      if(!d){ lastEl.textContent='点任意卡片的「复制」就能开始，会记住你上次用的模板。'; return; }
      var days=Math.floor((Date.now()-new Date(d.at).getTime())/86400000);
      lastEl.textContent='上次使用：'+d.title+'（'+(days<=0?'今天':days+' 天前')+'）';
    }catch(e){}
  }
  updateLast();

  if(fab) fab.addEventListener('click',function(){
    if(dlg.showModal) dlg.showModal(); else dlg.setAttribute('open','');
    requestAnimationFrame(function(){
      cards.forEach(function(c){ fit(c.querySelector('.p-body')); });
    });
  });
  var closeBtn=dlg.querySelector('.p-close');
  if(closeBtn) closeBtn.addEventListener('click',function(){ dlg.close(); });
  dlg.addEventListener('click',function(e){ if(e.target===dlg) dlg.close(); });

  function fit(ta){ ta.style.height='auto'; ta.style.height=(ta.scrollHeight+2)+'px'; }

  cards.forEach(function(c,i){
    var topic=c.querySelector('.p-topic'), ta=c.querySelector('.p-body'), btn=c.querySelector('.p-copy');
    fit(ta);
    topic.addEventListener('input',function(){
      var t=topic.value.trim();
      ta.value = t ? orig[i].replace(PH,t) : orig[i];
      fit(ta);
    });
    btn.addEventListener('click',function(){
      var done=function(){
        try{ localStorage.setItem('cs-roadmap-prompt', JSON.stringify({
          n:c.dataset.n, title:c.querySelector('.p-title').textContent, at:new Date().toISOString()
        })); }catch(e){}
        btn.textContent='已复制 ✓'; updateLast();
        setTimeout(function(){ btn.textContent='复制'; },1500);
      };
      if(navigator.clipboard && navigator.clipboard.writeText){
        navigator.clipboard.writeText(ta.value).then(done, function(){ ta.select(); document.execCommand('copy'); done(); });
      }else{ ta.select(); document.execCommand('copy'); done(); }
    });
  });
})();

/* ---------- 本周三件事 ---------- */
(function(){
  var card=document.getElementById('week-card'); if(!card) return;
  var listEl=document.getElementById('wk-list');
  var phaseEl=document.getElementById('wk-phase');
  var weekEl=document.getElementById('wk-week');
  var progEl=document.getElementById('wk-progress');
  var tipEl=document.getElementById('wk-tip');
  var startBtn=document.getElementById('wk-start');
  var PLAN_KEY='cs-roadmap-plan';
  var plan={};
  try{ plan=JSON.parse(localStorage.getItem(PLAN_KEY)||'{}')||{}; }catch(e){ plan={}; }

  function savePlan(){ try{ localStorage.setItem(PLAN_KEY, JSON.stringify(plan)); }catch(e){} }

  // 收集「清单里的各阶段」：h4.sub 以 P0/P1… 开头，后面跟若干 li.task
  function collectPhases(){
    var out=[];
    document.querySelectorAll('.content h4.sub').forEach(function(h){
      var t=(h.textContent||'').trim();
      if(!/^P\d/.test(t)) return;
      var ins=[], n=h.nextElementSibling;
      while(n && !/^H[234]$/.test(n.tagName)){
        if(n.tagName==='UL'){
          var f=n.querySelectorAll('li.task input[data-k]');
          for(var i=0;i<f.length;i++) ins.push(f[i]);
        }
        n=n.nextElementSibling;
      }
      if(ins.length) out.push({name:t, inputs:ins});
    });
    return out;
  }

  function weekNumber(){
    if(!plan.startedAt) return null;
    var d=Date.now()-new Date(plan.startedAt).getTime();
    return Math.max(1, Math.floor(d/604800000)+1);
  }

  function render(){
    var phases=collectPhases();
    var cur=null;
    for(var i=0;i<phases.length;i++){
      if(phases[i].inputs.some(function(x){return !x.checked;})){ cur=phases[i]; break; }
    }
    if(!phases.length){ phaseEl.textContent='（清单未找到）'; return; }

    var wk=weekNumber();
    weekEl.textContent = wk ? ('第 '+wk+' 周') : '尚未开始';
    startBtn.textContent = wk ? '重新开始' : '开始记录';

    if(!cur){
      phaseEl.textContent='全部完成 🎉';
      tipEl.textContent='105 项全过了。接下来只剩一件事：把它们变成两个能讲清楚的项目。';
      listEl.innerHTML='<li class="wk-done">你已走完全部清单</li>';
      progEl.textContent='';
      return;
    }
    phaseEl.textContent=cur.name;
    tipEl.textContent = wk ? '本周只做这三件。做完自动换下一批。'
                           : '点「开始记录」，之后每次打开都会告诉你第几周、这周做什么。';

    var pending=cur.inputs.filter(function(x){return !x.checked;}).slice(0,3);
    listEl.innerHTML='';
    pending.forEach(function(src){
      var lab=src.closest('label');
      var txt=lab? (lab.querySelector('.ctxt')||{}).textContent||'' : '';
      var li=document.createElement('li');
      li.className='task';
      li.innerHTML='<label><input type="checkbox"><span class="cbt"></span><span class="ctxt"></span></label>';
      li.querySelector('.ctxt').textContent=txt;
      li.querySelector('input').addEventListener('change',function(e){
        src.checked=e.target.checked;
        src.dispatchEvent(new Event('change',{bubbles:true}));
        render();
      });
      listEl.appendChild(li);
    });
    var done=cur.inputs.filter(function(x){return x.checked;}).length;
    progEl.textContent='本阶段 '+done+' / '+cur.inputs.length+' 项';
  }

  startBtn.addEventListener('click',function(){
    if(plan.startedAt && !confirm('重新开始会重置"第 N 周"的计数（勾选进度不受影响），确定吗？')) return;
    plan.startedAt=new Date().toISOString(); plan.version=1; savePlan(); render();
  });

  document.addEventListener('change',function(e){
    if(e.target && e.target.matches && e.target.matches('li.task input[data-k]')) render();
  });

  render();
})();

/* 仅在内容真正溢出时显示横滑提示 */
function markScrollable(){
  document.querySelectorAll('.table-wrap, .dgm-wrap').forEach(function(w){
    w.classList.toggle('scrollable', w.scrollWidth > w.clientWidth + 4);
  });
}
markScrollable();
window.addEventListener('resize', markScrollable);
window.addEventListener('load', markScrollable);

const KEY='cs-roadmap-checks';
let saved={};
try{saved=JSON.parse(localStorage.getItem(KEY)||'{}');}catch(e){saved={};}
const boxes=[...document.querySelectorAll('li.task input[data-k]')];
boxes.forEach(cb=>{
  const k=cb.dataset.k;
  if(saved[k]) cb.checked=true;
  cb.addEventListener('change',()=>{
    saved[k]=cb.checked;
    try{localStorage.setItem(KEY,JSON.stringify(saved));}catch(e){}
  });
});
document.querySelectorAll('.codeblock').forEach(box=>{
  const btn=box.querySelector('.copy');
  btn.onclick=async()=>{
    const t=box.querySelector('code').innerText;
    try{await navigator.clipboard.writeText(t);btn.textContent='✓ 已复制';}
    catch(e){btn.textContent='复制失败';}
    setTimeout(()=>btn.textContent='复制',1600);
  };
});

/* ---------- 进度统计 / 导入导出 ---------- */
const ckCount=document.getElementById('ck-count');
const ckTotal=document.getElementById('ck-total');
const ckFill=document.getElementById('ck-fill');
function refreshCk(){
  if(!ckTotal) return;
  const total=boxes.length, done=boxes.filter(b=>b.checked).length;
  ckCount.textContent=done; ckTotal.textContent=total;
  ckFill.style.width=(total?done/total*100:0)+'%';
}
refreshCk();
boxes.forEach(cb=>cb.addEventListener('change',refreshCk));
const expBtn=document.getElementById('ck-export');
if(expBtn){
  expBtn.onclick=()=>{
    const data={project:'java-to-ai-roadmap',version:1,exportedAt:new Date().toISOString(),checked:saved};
    const blob=new Blob([JSON.stringify(data,null,2)],{type:'application/json'});
    const a=document.createElement('a');
    a.href=URL.createObjectURL(blob);
    a.download='cs-roadmap-progress-'+new Date().toISOString().slice(0,10)+'.json';
    a.click(); setTimeout(()=>URL.revokeObjectURL(a.href),1000);
    expBtn.textContent='已导出 ✓'; setTimeout(()=>expBtn.textContent='导出进度',1600);
  };
  const fileInput=document.getElementById('ck-file');
  document.getElementById('ck-import').onclick=()=>fileInput.click();
  fileInput.onchange=async()=>{
    const f=fileInput.files[0]; if(!f) return;
    try{
      const j=JSON.parse(await f.text());
      const c=j.checked||j.saved||{};
      Object.keys(saved).forEach(k=>delete saved[k]);
      Object.assign(saved,c);
      try{localStorage.setItem(KEY,JSON.stringify(saved));}catch(e){}
      boxes.forEach(cb=>{cb.checked=!!saved[cb.dataset.k];});
      refreshCk();
      const b=document.getElementById('ck-import');
      b.textContent='已导入 ✓'; setTimeout(()=>b.textContent='导入',1600);
    }catch(e){ alert('导入失败：文件格式不对'); }
    fileInput.value='';
  };
  document.getElementById('ck-reset').onclick=()=>{
    if(!confirm('确定清空所有打勾记录？此操作不可撤销。')) return;
    Object.keys(saved).forEach(k=>delete saved[k]);
    try{localStorage.removeItem(KEY);}catch(e){}
    boxes.forEach(cb=>{cb.checked=false;});
    refreshCk();
  };
}
"""

PROMPT_FAB = """<button class="prompt-fab" id="prompt-fab" type="button" aria-label="打开 AI 对话模板" title="AI 对话模板（8 个）">🧠<span>AI 模板</span></button>"""

PROMPT_DIALOG_HEAD = """<dialog class="p-dialog" id="prompt-dialog" aria-label="AI 对话模板">
  <div class="p-head">
    <div class="p-head-l"><b>🧠 AI 对话模板</b><div class="p-last" id="p-last"></div></div>
    <button type="button" class="p-close" aria-label="关闭">✕</button>
  </div>
  <div class="p-list">"""

PROMPT_DIALOG_TAIL = """  </div>
  <div class="p-foot">复制后粘进任意 AI 对话即可。填了「具体对象」的话，模板里的占位符会自动替换。</div>
</dialog>"""

WEEK_CARD = """<section class="week-card" id="week-card" aria-label="本周三件事">
  <div class="wk-top">
    <span class="wk-badge" id="wk-week">第 1 周</span>
    <span class="wk-phase" id="wk-phase">正在读取你的进度…</span>
    <button type="button" class="wk-btn" id="wk-start">开始记录</button>
  </div>
  <div class="wk-tip" id="wk-tip">打开只看这三件。做完，自动换上下一批。</div>
  <ul class="wk-list" id="wk-list"></ul>
  <div class="wk-foot">
    <span id="wk-progress"></span>
    <a href="#sec-12">完整清单 →</a>
  </div>
</section>"""

HERO = """
<header class="hero">
  <span class="kicker">计算机学习地图 · 2026 版</span>
  <h1>别收藏<em>第 51 份</em>路线图了</h1>
  <p class="sub">一份能陪你走两年的计算机学习路径：<br>从零基础，到能用 <b>Java</b> 做出 <b>AI 应用</b>。</p>
  <div class="chips">
    <span class="chip">📖 精读约 45 分钟</span>
    <span class="chip">🎯 适合：零基础 · 自学 · 想转 AI 应用</span>
    <span class="chip">🧭 路线：Java → 系统 → 数据库 → 后端 → AI</span>
    <span class="chip">📅 更新于 2026-10-19</span>
  </div>
  <blockquote>写给和我一样的人：收藏夹里躺着几十个「从入门到精通」，一个都没走完。<br>
  这篇只解决三件事——<b>为什么是这个顺序</b>、<b>什么时候算学会了</b>、<b>卡住了怎么办</b>。</blockquote>
</header>
"""

PROMPTS_HTML = _render_prompts(prompts)

doc = f"""<!doctype html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="theme-color" content="#fbf9f4">
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'%3E%3Ctext y='.9em' font-size='90'%3E%F0%9F%97%BA%EF%B8%8F%3C/text%3E%3C/svg%3E">
<title>别收藏第 51 份路线图了 · 计算机学习地图（Java → AI 应用）</title>
<meta name="description" content="一份能陪你走两年的计算机学习路径：从零基础到能用 Java 做 AI 应用。含依赖关系图、阶段验收标准、AI 对话模板、每日闭环与可勾选清单。">
<style>{CSS}</style>
</head>
<body>
<div class="progress"><div id="pbar"></div></div>
{HERO}
<div class="layout">
<aside class="toc">{toc_html}</aside>
<main class="content">
{toc_mobile}
{WEEK_CARD}
{body}
</main>
</div>
{PROMPTS_HTML}
<button class="totop" aria-label="回到顶部">↑</button>
<script>{JS}</script>
</body>
</html>
"""

open(OUT, "w", encoding="utf-8").write(doc)
print(f"OK -> {OUT}  ({len(doc)} chars)")

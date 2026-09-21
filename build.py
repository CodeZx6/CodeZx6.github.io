# -*- coding: utf-8 -*-
"""Generate a static, AI-crawler-friendly academic homepage from papers.py.
Run:  python3 build.py   ->  writes index.html, papers/*.html, publications.bib, publications.json,
      llms.txt, llms-full.txt, robots.txt, sitemap.xml, .nojekyll
"""
import json, html, os, re, datetime
from papers import AUTHOR as A, PAPERS

ROOT = os.path.dirname(os.path.abspath(__file__))
PUBLISH_HOME = False   # False: bio homepage goes to _drafts/home.html (not published); index.html is a bare publication index
SITE = A["site"].rstrip("/")
TODAY = datetime.date.today().isoformat()
ME = A["name"]

def esc(s): return html.escape(s or "", quote=True)
def paper_url(p): return f"{SITE}/papers/{p['slug']}.html"
def doi_url(p): return f"https://doi.org/{p['doi']}" if p.get("doi") else None
def arxiv_url(p): return f"https://arxiv.org/abs/{p['arxiv']}" if p.get("arxiv") else None
def landing(p): return doi_url(p) or arxiv_url(p)
def pdf_url(p):
    if p.get("pdf"): return p["pdf"]
    if p.get("arxiv"): return f"https://arxiv.org/pdf/{p['arxiv']}"
    return None
def split_name(n):
    parts = n.split(); return parts[-1], " ".join(parts[:-1])
def bib_author(p): return " and ".join(f"{split_name(a)[0]}, {split_name(a)[1]}" for a in p["authors"])
def bib_title(p):
    t = p["title"]
    # protect acronyms / capitalised tokens
    def prot(m):
        w = m.group(0)
        parts = re.split(r"[-–]", w)
        need = any(re.search(r"[A-Z]", q[1:]) or (len(q) >= 2 and q.isupper()) for q in parts if q)
        return "{" + w + "}" if need else w
    return re.sub(r"[A-Za-z0-9][A-Za-z0-9-–]*", prot, t)

def bibtex(p):
    if p["venue_type"] == "preprint":
        f = [("title", bib_title(p)), ("author", bib_author(p)), ("journal", f"arXiv preprint arXiv:{p['arxiv']}"),
             ("year", str(p["year"])), ("eprint", p["arxiv"]), ("archivePrefix", "arXiv"), ("primaryClass", "cs.SD"),
             ("url", arxiv_url(p))]
        kind = "article"
    elif p["venue_type"] == "conference":
        f = [("title", bib_title(p)), ("author", bib_author(p)), ("booktitle", p["venue"]), ("year", str(p["year"])),
             ("pages", p["pages"].replace("-", "--")), ("publisher", p.get("publisher", "")), ("doi", p["doi"]), ("url", doi_url(p))]
        kind = "inproceedings"
    else:
        f = [("title", bib_title(p)), ("author", bib_author(p)), ("journal", p["venue"]), ("year", str(p["year"])),
             ("volume", p.get("volume", "")), ("pages", p.get("pages", "").replace("-", "--")), ("doi", p["doi"]),
             ("issn", p.get("issn", "")), ("url", doi_url(p))]
        kind = "article"
    body = ",\n".join(f"  {k:<13}= {{{v}}}" for k, v in f if v)
    return f"@{kind}{{{p['key']},\n{body}\n}}"

def apa(p):
    names = []
    for a in p["authors"]:
        last, first = split_name(a)
        names.append(f"{last}, {' '.join(x[0]+'.' for x in first.split())}")
    auth = ", ".join(names[:-1]) + (", & " if len(names) > 1 else "") + names[-1]
    if p["venue_type"] == "preprint":
        tail = f"arXiv preprint arXiv:{p['arxiv']}. {arxiv_url(p)}"
    elif p["venue_type"] == "conference":
        tail = f"In {p['venue']} (pp. {p['pages'].replace('-', '–')}). {p.get('publisher','')}. https://doi.org/{p['doi']}"
    else:
        vol = f", {p['volume']}" if p.get("volume") else ""
        tail = f"{p['venue']}{vol}, {p.get('pages','')}. https://doi.org/{p['doi']}"
    return f"{auth} ({p['year']}). {p['title']}. {tail}"

def person_ld(name):
    d = {"@type": "Person", "name": name}
    if name == ME:
        d.update({"@id": f"{SITE}/#me", "url": SITE, "sameAs": [A["orcid"], A["scholar"], A["github"], A["openalex"], A["semanticscholar"]],
                  "affiliation": {"@type": "Organization", "name": A["affiliation"], "url": A["affiliation_url"]}})
    return d

def article_ld(p):
    d = {"@context": "https://schema.org", "@type": "ScholarlyArticle", "@id": landing(p), "headline": p["title"], "name": p["title"],
         "author": [person_ld(a) for a in p["authors"]], "datePublished": p["date"], "inLanguage": "en",
         "url": paper_url(p), "mainEntityOfPage": paper_url(p), "keywords": ", ".join(p["keywords"]),
         "description": p["tldr"], "sameAs": [u for u in [doi_url(p), arxiv_url(p)] if u]}
    if p.get("abstract"): d["abstract"] = p["abstract"]
    if p.get("doi"): d["identifier"] = {"@type": "PropertyValue", "propertyID": "DOI", "value": p["doi"]}
    if p["venue_type"] == "preprint":
        d["isPartOf"] = {"@type": "Periodical", "name": "arXiv"}
        d["identifier"] = {"@type": "PropertyValue", "propertyID": "arXiv", "value": p["arxiv"]}
    elif p["venue_type"] == "conference":
        d["isPartOf"] = {"@type": "Book", "name": p["venue"], "publisher": {"@type": "Organization", "name": p.get("publisher", "")}}
        d["pagination"] = p["pages"]
    else:
        d["isPartOf"] = {"@type": "PublicationVolume", "volumeNumber": p.get("volume", ""), "isPartOf": {"@type": "Periodical", "name": p["venue"], "issn": p.get("issn", "")}}
        d["pagination"] = p.get("pages", "")
    if pdf_url(p): d["encoding"] = {"@type": "MediaObject", "encodingFormat": "application/pdf", "contentUrl": pdf_url(p)}
    if p.get("code"): d["subjectOf"] = {"@type": "SoftwareSourceCode", "name": f"{p['short']} code", "codeRepository": p["code"], "programmingLanguage": "Python"}
    if p.get("oa") and "closed" not in p["oa"]: d["isAccessibleForFree"] = True
    alt = [p["short"]] + p.get("aliases", [])[:6] + ([p["zh_title"]] if p.get("zh_title") else [])
    d["alternateName"] = alt
    d["about"] = [{"@type": "DefinedTerm", "name": k} for k in p["keywords"]]
    rel = [q for q in PAPERS if q is not p and q.get("group") == p.get("group")]
    if rel: d["citation"] = [{"@type": "ScholarlyArticle", "name": q["title"], "url": paper_url(q)} for q in rel]
    return d

def faq_ld(p):
    qs = list(p.get("faq", []))
    qs.append((f"How do I cite {p['short']}?", f"Cite it as: {apa(p)} BibTeX is available at {paper_url(p)}#cite and in {SITE}/publications.bib."))
    if p.get("code"): qs.append((f"Is the code for {p['short']} available?", f"Yes, at {p['code']}."))
    return {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in qs]}, qs

def scholar_meta(p):
    m = [("citation_title", p["title"])] + [("citation_author", a) for a in p["authors"]]
    m.append(("citation_publication_date", p["date"].replace("-", "/")))
    m.append(("citation_online_date", p["date"].replace("-", "/")))
    if p["venue_type"] == "conference": m.append(("citation_conference_title", p["venue"]))
    elif p["venue_type"] == "journal": m.append(("citation_journal_title", p["venue"]))
    else: m.append(("citation_technical_report_institution", "arXiv"))
    if p.get("volume"): m.append(("citation_volume", p["volume"]))
    if p.get("issn"): m.append(("citation_issn", p["issn"]))
    if p.get("pages") and "-" in p["pages"]:
        a, b = p["pages"].split("-"); m += [("citation_firstpage", a), ("citation_lastpage", b)]
    elif p.get("pages"): m.append(("citation_firstpage", p["pages"]))
    if p.get("doi"): m.append(("citation_doi", p["doi"]))
    if p.get("arxiv"): m.append(("citation_arxiv_id", p["arxiv"]))
    if p.get("pmid"): m.append(("citation_pmid", p["pmid"]))
    if pdf_url(p): m.append(("citation_pdf_url", pdf_url(p)))
    m.append(("citation_abstract_html_url", paper_url(p)))
    m.append(("citation_language", "en"))
    m += [("citation_keywords", k) for k in p["keywords"]]
    m += [("keywords", ", ".join(p["keywords"] + p.get("aliases", []) + p.get("zh_keywords", []))),
          ("DC.title", p["title"]), ("DC.type", "Text.Article"), ("DC.language", "en"), ("DC.date", p["date"]),
          ("DC.description", p["tldr"]), ("DC.identifier", doi_url(p) or arxiv_url(p)), ("DC.subject", ", ".join(p["keywords"]))]
    m += [("DC.creator", a) for a in p["authors"]]
    return "\n".join(f'<meta name="{k}" content="{esc(v)}">' for k, v in m)

CSS = """
:root{--bg:#fbfaf7;--fg:#1c1b19;--muted:#5f5b53;--line:#e4e0d8;--accent:#0b5fa5;--accent-bg:#eaf2fb;--card:#ffffff;--code:#f3f1ec;--tag:#efece5}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){--bg:#14161a;--fg:#e8e6e1;--muted:#a09c94;--line:#2b2f36;--accent:#7cb4ea;--accent-bg:#1b2634;--card:#1b1e24;--code:#20242b;--tag:#242830}}
:root[data-theme="dark"]{--bg:#14161a;--fg:#e8e6e1;--muted:#a09c94;--line:#2b2f36;--accent:#7cb4ea;--accent-bg:#1b2634;--card:#1b1e24;--code:#20242b;--tag:#242830}
*{box-sizing:border-box}html{-webkit-text-size-adjust:100%}
body{margin:0;background:var(--bg);color:var(--fg);font:16px/1.6 -apple-system,BlinkMacSystemFont,"Segoe UI",Inter,Roboto,"Helvetica Neue",Arial,"Noto Sans",sans-serif}
main{max-width:860px;margin:0 auto;padding:32px 16px 64px;overflow-wrap:anywhere}
a{color:var(--accent);text-decoration:none}a:hover{text-decoration:underline}
h1{font-size:1.9rem;line-height:1.25;margin:0 0 6px}h2{font-size:1.25rem;margin:40px 0 12px;padding-bottom:6px;border-bottom:1px solid var(--line)}h3{font-size:1.05rem;margin:18px 0 6px}
.sub{color:var(--muted);margin:0 0 14px}
.links a,.chip{display:inline-block;margin:0 8px 8px 0;padding:4px 10px;border:1px solid var(--line);border-radius:999px;background:var(--card);font-size:.9rem}
.chip{background:var(--tag);color:var(--muted);border:none;font-size:.8rem;padding:2px 8px}
.paper{padding:16px 0;border-bottom:1px solid var(--line)}.paper:last-child{border-bottom:none}
.paper .t{font-weight:600;font-size:1.05rem}.paper .v{color:var(--muted);font-size:.92rem}.paper .a{font-size:.95rem}
.tldr{background:var(--accent-bg);border-left:4px solid var(--accent);padding:12px 14px;border-radius:6px;margin:16px 0}
pre{background:var(--code);padding:14px;border-radius:8px;overflow-x:auto;font-size:.85rem;line-height:1.45;border:1px solid var(--line)}
code{font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace}
button.copy{font:inherit;font-size:.85rem;padding:4px 10px;border:1px solid var(--line);border-radius:6px;background:var(--card);color:var(--fg);cursor:pointer;margin-bottom:6px}
.me{font-weight:700}ul{padding-left:1.2em}.grid{display:grid;grid-template-columns:1fr 1fr;gap:12px}@media (max-width:640px){.grid{grid-template-columns:1fr}}
.card{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:14px}
footer{margin-top:48px;color:var(--muted);font-size:.85rem;border-top:1px solid var(--line);padding-top:16px}
nav a{margin-right:16px}
.facts{border-collapse:collapse;width:100%;table-layout:fixed;font-size:.95rem}.facts th,.facts td{text-align:left;vertical-align:top;padding:6px 8px;border-bottom:1px solid var(--line)}.facts th{width:32%;color:var(--muted);font-weight:600}
"""

COPY_JS = """<script>
document.querySelectorAll('button.copy').forEach(b=>b.addEventListener('click',()=>{const t=document.getElementById(b.dataset.for).innerText;navigator.clipboard&&navigator.clipboard.writeText(t).then(()=>{b.textContent='Copied';setTimeout(()=>b.textContent=b.dataset.label,1500)})}));
</script>"""

def head(title, desc, url, ld, extra="", extra_ld=""):
    return f"""<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<link rel="canonical" href="{url}">
<meta property="og:title" content="{esc(title)}"><meta property="og:description" content="{esc(desc)}"><meta property="og:url" content="{url}"><meta property="og:type" content="article">
<meta name="twitter:card" content="summary">
<meta name="robots" content="index,follow,max-snippet:-1,max-image-preview:large">
{extra}
<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>{extra_ld}
<style>{CSS}</style></head><body><main>"""

def authors_html(p):
    return ", ".join(f'<span class="me">{esc(a)}</span>' if a == ME else esc(a) for a in p["authors"])

def venue_line(p):
    if p["venue_type"] == "preprint": return f"arXiv:{p['arxiv']} ({p['year']})"
    if p["venue_type"] == "conference": return f"{p.get('venue_short', p['venue'])}, pp. {p['pages'].replace('-', '–')}"
    v = p["venue"]
    if p.get("volume"): v += f", vol. {p['volume']}"
    if p.get("pages"): v += f", {p['pages'].replace('-', '–')}"
    return f"{v} ({p['year']})"

def link_row(p, small=False):
    L = []
    if doi_url(p): L.append(("DOI", doi_url(p)))
    if arxiv_url(p): L.append(("arXiv", arxiv_url(p)))
    if pdf_url(p): L.append(("PDF", pdf_url(p)))
    if p.get("code"): L.append(("Code", p["code"]))
    for k, v in (p.get("links") or {}).items(): L.append((k, v))
    if p.get("pmcid"): L.append(("PMC", f"https://pmc.ncbi.nlm.nih.gov/articles/{p['pmcid']}/"))
    if not small: L.append(("Google Scholar", A["scholar"]))
    return '<div class="links">' + "".join(f'<a href="{esc(u)}" rel="noopener">{esc(k)}</a>' for k, u in L) + "</div>"

# ---------- paper pages ----------
os.makedirs(os.path.join(ROOT, "papers"), exist_ok=True)
GROUP_NAMES = {"speech": "Speech emotion and emotional TTS", "urban-flow": "Urban flow prediction", "od": "Origin-destination demand prediction", "hsi": "Hyperspectral image classification", "vision": "Visual detection"}
for p in PAPERS:
    ld = article_ld(p); fld, qs = faq_ld(p)
    vs = p.get("venue_short") or (p["venue"] if p["venue_type"] != "preprint" else "arXiv")
    vs = vs if str(p["year"]) in vs else f"{vs} {p['year']}"
    lab = "" if p["title"].lower().startswith(p["short"].lower()) else f"{p['short']}: "
    page_title = f"{lab}{p['title']} ({vs}) | {ME}"
    desc = f"{p['short']} by {', '.join(p['authors'])} ({vs}). {p['tldr']}"
    body = head(page_title, desc, paper_url(p), ld, scholar_meta(p), f'<script type="application/ld+json">{json.dumps(fld, ensure_ascii=False)}</script>')
    body += f'<nav><a href="../">All publications</a><a href="../publications.bib">BibTeX (all)</a><a href="{p["slug"]}.bib">BibTeX (this paper)</a></nav>'
    body += f"<h1>{esc(p['title'])}</h1><p class=\"sub\">{authors_html(p)}</p><p class=\"sub\">{esc(venue_line(p))}"
    if p.get("oa") and "closed" not in p["oa"]: body += f" · Open access ({esc(p['oa'])})"
    body += "</p>" + link_row(p)
    body += f'<div class="tldr"><strong>TL;DR.</strong> {esc(p["tldr"])}</div>'
    # quick facts (entity statements that retrieval systems can quote directly)
    body += "<h2>Quick facts</h2><table class=\"facts\">"
    body += f"<tr><th>Method name</th><td>{esc(p['short'])}</td></tr>"
    body += f"<tr><th>Authors</th><td>{authors_html(p)}</td></tr>"
    body += f"<tr><th>Published in</th><td>{esc(venue_line(p))}</td></tr>"
    if p.get("doi"): body += f"<tr><th>DOI</th><td><a href=\"{doi_url(p)}\">{esc(p['doi'])}</a></td></tr>"
    if p.get("arxiv"): body += f"<tr><th>arXiv</th><td><a href=\"{arxiv_url(p)}\">arXiv:{esc(p['arxiv'])}</a></td></tr>"
    for k, v in p.get("facts", {}).items(): body += f"<tr><th>{esc(k)}</th><td>{esc(v)}</td></tr>"
    if p.get("code"): body += f"<tr><th>Code</th><td><a href=\"{p['code']}\">{esc(p['code'])}</a></td></tr>"
    body += f"<tr><th>BibTeX key</th><td><code>{p['key']}</code></td></tr></table>"
    if p.get("findings"):
        body += "<h2>Key points</h2><ul>" + "".join(f"<li>{esc(f)}</li>" for f in p["findings"]) + "</ul>"
    if p.get("abstract"):
        body += f"<h2>Abstract</h2><p>{esc(p['abstract'])}</p>"
        if p.get("abstract_note"): body += f'<p class="sub"><em>{esc(p["abstract_note"])}</em></p>'
    body += "<h2>Frequently asked questions</h2>" + "".join(f"<h3>{esc(q)}</h3><p>{esc(a)}</p>" for q, a in qs)
    if p.get("zh_title"):
        body += f'<section lang="zh-CN"><h2>中文摘要</h2><h3>{esc(p["zh_title"])}</h3><p>{esc(p["zh_summary"])}</p><p>关键词：{esc("；".join(p["zh_keywords"]))}</p></section>'
    body += "<h2>Keywords and related search terms</h2><p>" + "".join(f'<span class="chip">{esc(k)}</span> ' for k in p["keywords"]) + "</p>"
    if p.get("aliases"): body += "<p class=\"sub\">Also described as: " + esc("; ".join(p["aliases"])) + ".</p>"
    rel = [q for q in PAPERS if q is not p and q.get("group") == p.get("group")]
    others = [q for q in PAPERS if q is not p and q.get("group") != p.get("group")]
    body += f"<h2>Related papers by {esc(ME)}</h2>"
    if rel: body += f"<h3>{esc(GROUP_NAMES.get(p.get('group'), 'Same topic'))}</h3><ul>" + "".join(f'<li><a href="{q["slug"]}.html">{esc(q["title"])}</a> ({esc(venue_line(q))})</li>' for q in rel) + "</ul>"
    body += "<h3>Other topics</h3><ul>" + "".join(f'<li><a href="{q["slug"]}.html">{esc(q["title"])}</a> ({q["year"]})</li>' for q in others) + "</ul>"
    bid = f"bib-{p['slug']}"; aid = f"apa-{p['slug']}"
    body += f'<h2 id="cite">Cite this paper</h2><button class="copy" data-for="{bid}" data-label="Copy BibTeX">Copy BibTeX</button><pre id="{bid}"><code>{esc(bibtex(p))}</code></pre>'
    body += f'<button class="copy" data-for="{aid}" data-label="Copy APA">Copy APA</button><pre id="{aid}"><code>{esc(apa(p))}</code></pre>'
    body += f'<footer><a href="../">Publications of {esc(ME)}</a> · <a href="{A["orcid"]}">ORCID</a> · <a href="{A["scholar"]}">Google Scholar</a> · <a href="{A["github"]}">GitHub</a> · Last updated {TODAY}</footer>'
    body += COPY_JS + "</main></body></html>"
    open(os.path.join(ROOT, "papers", f"{p['slug']}.html"), "w").write(body)
    open(os.path.join(ROOT, "papers", f"{p['slug']}.bib"), "w").write(bibtex(p) + "\n")

# ---------- index ----------
person = person_ld(ME)
person.update({"@context": "https://schema.org", "email": f"mailto:{A['email']}", "jobTitle": "PhD candidate",
               "knowsAbout": ["speech emotion recognition", "emotional text-to-speech", "diffusion and flow-matching TTS", "spatio-temporal prediction", "urban flow prediction", "origin-destination demand prediction", "hyperspectral image classification", "contrastive learning", "humanoid robots"]})
index_ld = [person, {"@context": "https://schema.org", "@type": "WebSite", "name": f"{ME} — Research", "url": SITE, "author": {"@id": f"{SITE}/#me"}},
            {"@context": "https://schema.org", "@type": "ItemList", "name": f"Publications by {ME}", "itemListElement": [{"@type": "ListItem", "position": i + 1, "url": paper_url(p), "name": p["title"]} for i, p in enumerate(PAPERS)]}]
desc = f"{ME} is a PhD candidate in the School of Computing at Macquarie University working on speech emotion recognition, emotional text-to-speech, and spatio-temporal prediction. Publications, code, and BibTeX."
b = head(f"{ME} — Macquarie University", desc, SITE + "/", index_ld)
b += f"""<h1>{esc(ME)}</h1><p class="sub">PhD candidate · {esc(A['affiliation'])} · Sydney, Australia</p>
<div class="links"><a href="{A['scholar']}">Google Scholar</a><a href="{A['orcid']}">ORCID 0000-0002-4143-0715</a><a href="{A['github']}">GitHub @CodeZx6</a><a href="{A['semanticscholar']}">Semantic Scholar</a><a href="mailto:{A['email']}">Email</a><a href="publications.bib">BibTeX (all papers)</a></div>
<h2 id="about">About</h2>
<p>I am Xu Zhang (张旭), a PhD candidate in Computer Science at Macquarie University. My current research is on <strong>affective speech</strong>: physiology-informed speech emotion recognition (<a href="papers/physioser.html">PhysioSER</a>) and plug-and-play emotion control for diffusion and flow-matching text-to-speech (<a href="papers/duet.html">DUET</a>), including real-time deployment on the Ameca humanoid robot. Before that, I worked on <strong>spatio-temporal learning for intelligent transportation</strong>, including urban flow prediction with masked and contrastive pre-training (<a href="papers/mcstl.html">MCSTL</a>, <a href="papers/st-csl.html">ST-CSL</a>, <a href="papers/mr-ufp.html">MR-UFP</a>) and origin-destination demand prediction (<a href="papers/bist-if.html">BiST-IF</a>, <a href="papers/dstcn.html">DSTCN</a>), and on few-shot hyperspectral image classification.</p>
<p>I completed my M.Eng. at Qilu University of Technology (Shandong Academy of Sciences), where my thesis was on traffic flow prediction based on spatio-temporal representation learning.</p>
<h2 id="research">Research areas</h2><div class="grid">
<div class="card"><h3>Speech emotion recognition</h3>Interpretable, efficient SER that couples vocal amplitude and phase through voice physiology and quaternion representations on top of frozen self-supervised speech models.</div>
<div class="card"><h3>Emotional text-to-speech</h3>Training-free emotion control for pretrained diffusion and flow-matching TTS via hidden-space steering and mel-space guidance.</div>
<div class="card"><h3>Urban flow and OD prediction</h3>Masked and contrastive pre-training, multi-scale regional information, delay correction and bi-directional attention for city-scale mobility forecasting.</div>
<div class="card"><h3>Hyperspectral image analysis</h3>Cross-domain few-shot classification and joint superpixel segmentation and classification for remote sensing.</div></div>
<h2 id="publications">Publications</h2><p class="sub">Each paper has its own page with a plain-language summary, abstract, and copyable BibTeX. Full list: <a href="publications.bib">publications.bib</a> · <a href="publications.json">publications.json</a>.</p>"""
year = None
for p in PAPERS:
    if p["year"] != year:
        year = p["year"]; b += f"<h3>{year}</h3>"
    b += f'<div class="paper"><div class="t"><a href="papers/{p["slug"]}.html">{esc(p["title"])}</a></div><div class="a">{authors_html(p)}</div><div class="v">{esc(venue_line(p))}</div><p style="margin:6px 0">{esc(p["tldr"])}</p>{link_row(p, small=True)}</div>'
b += f"""<h2 id="code">Code and demos</h2><ul>
<li><a href="https://github.com/CodeZx6/MCSTL">MCSTL</a>, <a href="https://github.com/CodeZx6/ST-CSL">ST-CSL</a>, <a href="https://github.com/CodeZx6/MR-UPF">MR-UPF</a>: urban flow prediction (CIKM 2023, Knowledge-Based Systems 2023, Neural Networks 2025).</li>
<li><a href="https://github.com/CodeZx6/BiST-IF">BiST-IF</a>, <a href="https://github.com/CodeZx6/DSTCN">DSTCN</a>: origin-destination demand prediction (Expert Systems with Applications 2025, 2026).</li>
<li><a href="https://codezx6.github.io/duet-demo-fresh/">DUET audio demo</a>: emotion-controlled speech samples across five TTS backbones.</li></ul>
<h2 id="cite">How to cite</h2><p>Download <a href="publications.bib">publications.bib</a> for every entry, or open a paper page and press “Copy BibTeX”. Machine-readable metadata is in <a href="publications.json">publications.json</a> and <a href="llms.txt">llms.txt</a>.</p>
<footer>© {TODAY[:4]} {esc(ME)} · <a href="{A['orcid']}">ORCID</a> · <a href="{A['scholar']}">Google Scholar</a> · <a href="{A['github']}">GitHub</a> · <a href="llms.txt">llms.txt</a> · Last updated {TODAY}</footer>
</main></body></html>"""
if PUBLISH_HOME:
    open(os.path.join(ROOT, "index.html"), "w").write(b)
else:
    os.makedirs(os.path.join(ROOT, "_drafts"), exist_ok=True)
    open(os.path.join(ROOT, "_drafts", "home.html"), "w").write(b)
    person_min = {"@context": "https://schema.org", "@type": "Person", "@id": f"{SITE}/#me", "name": ME, "url": SITE, "affiliation": {"@type": "Organization", "name": A["affiliation"]}, "sameAs": person["sameAs"]}
    ld2 = [person_min, index_ld[2]]
    b2 = head(f"Publications — {ME}", f"Publications by {ME} ({A['affiliation']}) with abstracts, DOIs, arXiv links, code, and BibTeX.", SITE + "/", ld2)
    b2 += f"""<h1>Publications — {esc(ME)}</h1><p class="sub">{esc(A['affiliation'])} · <a href="{A['scholar']}">Google Scholar</a> · <a href="{A['orcid']}">ORCID 0000-0002-4143-0715</a> · <a href="{A['github']}">GitHub</a> · <a href="publications.bib">BibTeX (all)</a> · <a href="publications.json">JSON</a> · <a href="llms.txt">llms.txt</a></p>
<p class="sub">Each paper has its own page with a plain-language summary, quick facts, abstract, FAQ, Chinese summary, related search terms, and copyable BibTeX and APA citations.</p>"""
    year = None
    for p in PAPERS:
        if p["year"] != year:
            year = p["year"]; b2 += f"<h2>{year}</h2>"
        b2 += f'<div class="paper"><div class="t"><a href="papers/{p["slug"]}.html">{esc(p["title"])}</a></div><div class="a">{authors_html(p)}</div><div class="v">{esc(venue_line(p))}</div><p style="margin:6px 0">{esc(p["tldr"])}</p>{link_row(p, small=True)}</div>'
    b2 += f'<footer>{esc(ME)} · <a href="{A["orcid"]}">ORCID</a> · <a href="{A["scholar"]}">Google Scholar</a> · <a href="{A["github"]}">GitHub</a> · Last updated {TODAY}</footer></main></body></html>'
    open(os.path.join(ROOT, "index.html"), "w").write(b2)

# ---------- bib / json ----------
open(os.path.join(ROOT, "publications.bib"), "w").write(f"% Publications of {ME} (ORCID {A['orcid'].split('/')[-1]}). Generated {TODAY}. Source: {SITE}/publications.bib\n\n" + "\n\n".join(bibtex(p) for p in PAPERS) + "\n")
json.dump([{k: v for k, v in p.items() if k not in ("findings",)} | {"url": paper_url(p), "bibtex": bibtex(p), "apa": apa(p)} for p in PAPERS], open(os.path.join(ROOT, "publications.json"), "w"), indent=1, ensure_ascii=False)

# ---------- llms.txt ----------
llms = f"""# {ME}

> Publication index of {ME} ({A['affiliation']}). Topics: speech emotion recognition, emotional text-to-speech for diffusion and flow-matching models, urban flow and origin-destination demand prediction, hyperspectral image classification. ORCID {A['orcid'].split('/')[-1]}. GitHub @CodeZx6.

Preferred citation format for any paper: use the BibTeX at {SITE}/publications.bib. Each paper page below contains a TL;DR, key points, abstract, DOI or arXiv ID, and BibTeX.

## Publications

"""
for p in PAPERS:
    ids = " · ".join(x for x in [f"DOI {p['doi']}" if p.get("doi") else "", f"arXiv:{p['arxiv']}" if p.get("arxiv") else ""] if x)
    lab = "" if p["title"].lower().startswith(p["short"].lower()) else f"{p['short']}: "
    llms += f"- [{lab}{p['title']}]({paper_url(p)}): {', '.join(p['authors'])}. {venue_line(p)}. {ids}. {p['tldr']} Also known as: {'; '.join(p.get('aliases', [])[:5])}.\n"
llms += f"""
## Code

- [GitHub @CodeZx6]({A['github']}): MCSTL, ST-CSL, MR-UPF (urban flow prediction), BiST-IF, DSTCN (OD demand prediction)
- [DUET demo](https://codezx6.github.io/duet-demo-fresh/): emotion-controlled TTS samples

## Profiles

- [Google Scholar]({A['scholar']})
- [ORCID]({A['orcid']})
- [Semantic Scholar]({A['semanticscholar']})
- [OpenAlex]({A['openalex']})

## Optional

- [publications.json]({SITE}/publications.json): all metadata as JSON
- [llms-full.txt]({SITE}/llms-full.txt): full abstracts and BibTeX for every paper
"""
open(os.path.join(ROOT, "llms.txt"), "w").write(llms)
full = llms + "\n\n# Full records\n\n"
for p in PAPERS:
    full += f"## {p['title']}\n\nAuthors: {', '.join(p['authors'])}\nVenue: {venue_line(p)}\n"
    if p.get("doi"): full += f"DOI: https://doi.org/{p['doi']}\n"
    if p.get("arxiv"): full += f"arXiv: {arxiv_url(p)}\n"
    if p.get("code"): full += f"Code: {p['code']}\n"
    full += f"Page: {paper_url(p)}\nKeywords: {', '.join(p['keywords'])}\nAlso described as: {'; '.join(p.get('aliases', []))}\n\nTL;DR: {p['tldr']}\n\n"
    for k, v in p.get("facts", {}).items(): full += f"{k}: {v}\n"
    full += "\n"
    for q, a in p.get("faq", []): full += f"Q: {q}\nA: {a}\n\n"
    if p.get("zh_title"): full += f"中文标题: {p['zh_title']}\n中文摘要: {p['zh_summary']}\n中文关键词: {'；'.join(p['zh_keywords'])}\n\n"
    if p.get("findings"): full += "Key points:\n" + "".join(f"- {f}\n" for f in p["findings"]) + "\n"
    if p.get("abstract"): full += f"Abstract: {p['abstract']}\n\n"
    full += f"BibTeX:\n```bibtex\n{bibtex(p)}\n```\n\nAPA: {apa(p)}\n\n---\n\n"
open(os.path.join(ROOT, "llms-full.txt"), "w").write(full)

# ---------- robots / sitemap ----------
bots = ["*", "Googlebot", "Bingbot", "GPTBot", "OAI-SearchBot", "ChatGPT-User", "ClaudeBot", "Claude-SearchBot", "Claude-User", "anthropic-ai", "PerplexityBot", "Perplexity-User", "Google-Extended", "Applebot", "Applebot-Extended", "CCBot", "cohere-ai", "Meta-ExternalAgent", "Bytespider", "DuckAssistBot", "YouBot", "Amazonbot", "PetalBot", "Baiduspider", "Sogou web spider", "360Spider", "YisouSpider"]
open(os.path.join(ROOT, "robots.txt"), "w").write("".join(f"User-agent: {u}\nAllow: /\n\n" for u in bots) + f"Sitemap: {SITE}/sitemap.xml\n")
urls = [SITE + "/", f"{SITE}/llms.txt", f"{SITE}/publications.bib"] + [paper_url(p) for p in PAPERS]
open(os.path.join(ROOT, ".gitignore"), "w").write("__pycache__/\n_abstracts_raw.json\n_drafts/\n")
open(os.path.join(ROOT, "sitemap.xml"), "w").write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "".join(f"  <url><loc>{u}</loc><lastmod>{TODAY}</lastmod></url>\n" for u in urls) + "</urlset>\n")
open(os.path.join(ROOT, ".nojekyll"), "w").write("")
# IndexNow key file (Bing/Yandex/Naver instant indexing); key stored in .indexnow-key
kp = os.path.join(ROOT, ".indexnow-key")
if os.path.exists(kp):
    k = open(kp).read().strip(); open(os.path.join(ROOT, f"{k}.txt"), "w").write(k)
print("built", len(PAPERS), "paper pages + index, bib, json, llms.txt, robots.txt, sitemap.xml")

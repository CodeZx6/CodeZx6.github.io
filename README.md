# xu-zhang-site

Static, AI-crawler-friendly academic homepage for Xu Zhang. Everything is generated from `papers.py` by `build.py`.

```
papers.py            ← edit this (add a paper, fix a field, add a PDF link)
build.py             ← python3 build.py
index.html           ← bare publication index (no bio); the bio homepage is built to _drafts/home.html and NOT published until PUBLISH_HOME = True in build.py
papers/<slug>.html   ← one page per paper: citation_* + Dublin Core meta, ScholarlyArticle + FAQPage JSON-LD, TL;DR, quick facts, abstract, FAQ, 中文摘要, synonyms, related papers, BibTeX/APA
papers/<slug>.bib    ← BibTeX for that paper alone
enrich.py            ← per-paper synonyms / facts / FAQ / Chinese summary (edit to add more search terms)
publications.bib     ← all BibTeX
publications.json    ← all metadata as JSON
llms.txt / llms-full.txt ← index for LLM crawlers (llmstxt.org convention)
robots.txt           ← explicitly allows Google/Bing + GPTBot, ClaudeBot, PerplexityBot, Google-Extended, Applebot, CCBot, Baidu, etc.
sitemap.xml
templates/           ← README / model-card / social-post drafts (not published)
```

## Deploy to GitHub Pages (user site → https://codezx6.github.io)

```bash
cd /Users/xuzhang/Project/xu-zhang-site
git init && git add -A && git commit -m "Academic homepage"
gh repo create CodeZx6/CodeZx6.github.io --public --source=. --push
```

Then GitHub → repo → Settings → Pages → Source: **Deploy from a branch**, branch `main`, folder `/ (root)`. The site is live at https://codezx6.github.io within a minute or two.

To update: edit `papers.py`, run `python3 build.py`, commit, push.

## Adding an accepted-manuscript PDF

Put the PDF in `pdf/` and set `pdf="https://codezx6.github.io/pdf/<file>.pdf"` on that paper in `papers.py`. The build then emits `citation_pdf_url` for Google Scholar and a PDF link for everyone else.

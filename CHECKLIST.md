# Exposure checklist for Xu Zhang's papers (2026-09-21)

Legend: ✅ done in this folder · 🔲 needs your account (I cannot log in for you) · ⏱ rough time

## A. What I already built (✅)

| File | Purpose |
|---|---|
| `index.html` | **Bare publication index only** (no bio). Person + ItemList JSON-LD, links to bib/json/llms.txt |
| `_drafts/home.html` | Your full bio homepage, **not published** (gitignored). When ready: set `PUBLISH_HOME = True` in `build.py`, rebuild |
| `papers/*.html` (11) | One page per paper: Google Scholar `citation_*` + Dublin Core meta, ScholarlyArticle + FAQPage JSON-LD, TL;DR, quick-facts table, key points, abstract, FAQ, 中文摘要/关键词, synonyms (“also described as”), related-paper links, copyable BibTeX + APA; plus `papers/<slug>.bib` |
| `publications.bib` / `.json` | All entries with DOI/arXiv, clean keys (`zhang2026duet`, `zhang2026physioser`, …) |
| `llms.txt`, `llms-full.txt` | LLM-crawler index (llmstxt.org). Full abstracts + BibTeX in the `-full` file |
| `robots.txt` | Explicit `Allow: /` for Googlebot, Bingbot, GPTBot, OAI-SearchBot, ClaudeBot, PerplexityBot, Google-Extended, Applebot, CCBot, Baidu, Sogou, 360, Yisou… |
| `sitemap.xml` | All pages |
| `templates/` | README for PhysioSER + DUET repos, additions for the 5 existing repos, GitHub profile README, Hugging Face model card, X/LinkedIn/知乎/公众号 drafts |

## B. Deploy the site (🔲, ⏱ 10 min) — everything else links here

```bash
cd /Users/xuzhang/Project/xu-zhang-site
git init && git add -A && git commit -m "Academic homepage"
gh repo create CodeZx6/CodeZx6.github.io --public --source=. --push
```
GitHub → repo → Settings → Pages → Deploy from branch `main` / root. Live at **https://codezx6.github.io**.
Then verify: https://validator.schema.org/ (paste a paper URL) and https://search.google.com/test/rich-results.

## C. Search-engine + AI-search registration (🔲, ⏱ 20 min)

1. **Google Search Console** → add property `codezx6.github.io` (DNS or HTML-file verification) → Sitemaps → submit `sitemap.xml` → URL Inspection → "Request indexing" for `/` and the two speech-paper pages.
2. **Bing Webmaster Tools** (powers ChatGPT search, Copilot, DuckDuckGo, Perplexity fallback) → import from Google Search Console → submit sitemap → use **IndexNow** for instant indexing.
3. **Baidu 站长平台** → 添加站点 → 提交 sitemap（国内 AI 搜索：百度、Kimi、豆包、DeepSeek 联网检索多走百度/搜狗索引）。

## D. Fix identity fragmentation (🔲, ⏱ 30 min) — this is what most limits AI attribution today

Your papers are currently split across **four** Semantic Scholar author IDs and **two** OpenAlex IDs, and the PeerJ paper is attributed to a different "Xu Zhang" on OpenAlex.

1. **ORCID 0000-0002-4143-0715** (already has 9 works): add *Researcher URLs* (homepage, Google Scholar, GitHub), add Employment/Education (Macquarie PhD; Qilu M.Eng.), set everything **public**, and add the two arXiv papers (Works → Add → Search & link → "arXiv" or paste `arXiv:2602.13259`, `arXiv:2606.00066`).
2. **arXiv account** → Settings → link ORCID. Then on each arXiv paper "Add ORCID" so arXiv/S2/OpenAlex disambiguate you automatically.
3. **Semantic Scholar**: claim https://www.semanticscholar.org/author/2260823473 ("Claim author page"), then request merge of 2492729361, 2273584640, 2355676374 (Support → "Merge author pages"). DUET (2606.00066) is not indexed yet: submit at https://www.semanticscholar.org/faq#missing-paper.
4. **OpenAlex**: attribution follows ORCID; after step 1 the PeerJ paper (currently on A5100437272) will move to A5040099809 on the next refresh.
5. **Google Scholar**: Profile → Edit → add **Homepage** `https://codezx6.github.io`; add the missing paper *URMDet-SimFire* (Array 2026, DOI 10.1016/j.array.2026.101124) via "Add articles"; check for duplicate entries and merge; turn on "Public access" to show the OA links.
6. **DBLP**: search https://dblp.org/search?q=Xu+Zhang+Macquarie — if your papers sit under a shared "Xu Zhang" page, email dblp@dagstuhl.de with the DOI list and ORCID to get a dedicated author page (`Xu Zhang 00XX`).

## E. Green open access — put full text where crawlers can read it (🔲, ⏱ 1–2 h)

Five journal papers are **closed** (KBS 2023, ESWA 2025, TGRS 2024, Neural Networks 2025, TGRS 2025). AI search engines mostly cannot read them.

| Paper | Publisher rule (verify at https://v2.sherpa.ac.uk/romeo/) | Action |
|---|---|---|
| ST-CSL (KBS), BiST-IF (ESWA), MR-UFP (NN) | Elsevier: accepted manuscript may be posted **immediately on your personal homepage**; on arXiv when updating an existing preprint; institutional repo after embargo | Put the accepted-manuscript PDFs in `pdf/`, set `pdf=` in `papers.py`, rebuild. Also deposit in **Macquarie Research Online** (library does it if you email the AAM) |
| Two TGRS papers | IEEE: accepted version allowed on personal site, institutional repo, **and arXiv** | Post accepted version to arXiv (cs.CV / eess.IV) with journal DOI in the "Journal-ref/DOI" fields, plus homepage |
| MCSTL (CIKM) | Already gold OA on ACM DL; ACM also allows author version on arXiv | Optional: arXiv version so it appears in arXiv-based indexes and Papers with Code |

Adding `pdf=` also emits `citation_pdf_url`, which is what Google Scholar needs to show a **[PDF]** link next to your name.

## F. GitHub (🔲, ⏱ 30 min)

1. Create `CodeZx6/CodeZx6` with the profile README in `templates/README_additions_existing_repos.md` (bottom). Set profile **Website** = homepage.
2. For MCSTL / ST-CSL / MR-UPF / BiST-IF / DSTCN: paste the badge block, DOI BibTeX, description, website, and **topics** from the same template.
3. Create `CodeZx6/PhysioSER` and `CodeZx6/DUET` from `templates/README_PhysioSER.md` and `templates/README_DUET.md` (even before the code is clean: a README with abstract + BibTeX is already indexable; add code when ready).
4. Enable **Zenodo–GitHub** integration and cut a `v1.0` release on each code repo to get a citable code DOI.
5. Add the repo link to the arXiv abstract page: replace the arXiv version (v2) with `Code: https://github.com/CodeZx6/PhysioSER` in the Comments field.

## G. Hugging Face + Papers with Code (🔲, ⏱ 30 min)

1. https://huggingface.co/papers/2602.13259 and `/papers/2606.00066` → "Claim authorship" → links the paper to your HF profile; HF paper pages rank highly in AI search.
2. Upload PhysioSER checkpoints as `CodeZx6/PhysioSER-<backbone>-<dataset>` with `templates/huggingface_model_card_PhysioSER.md` (the YAML header ties the model to arXiv 2602.13259).
3. Upload the DUET demo audio as an HF **Space** or dataset (`CodeZx6/duet-demo`) mirroring `codezx6.github.io/duet-demo-fresh`.
4. https://paperswithcode.com → add PhysioSER + DUET with code links and result tables (SER on IEMOCAP, etc.).

## H. Distribution (🔲, ⏱ 1 h, drafts in `templates/social_posts.md`)

- X thread + LinkedIn post for DUET and PhysioSER (English).
- 知乎文章 ×3（DUET、PhysioSER、城市流量/OD 系列合集）+ 公众号转发。Post on 知乎 with the paper's *exact English title* in the text so Chinese AI search ties it to the arXiv record.
- ResearchGate: create profile, claim the 10 papers, upload AAMs where allowed (same rules as section E).
- Ask Longbing Cao's group / Frontier AI Research Centre page to list you and link the homepage (a `.edu.au` inbound link is the strongest trust signal for both Google and AI search).
- LinkedIn profile → Publications section → add each paper with DOI.

## I. Ongoing habits

- Every new paper: add to `papers.py` → `python3 build.py` → push. Post arXiv first, with ORCID and code link in the submission.
- Keep one exact title everywhere (arXiv, venue, Scholar, GitHub). Title drift splits citations.
- Use the method name (DUET, PhysioSER, MCSTL…) consistently in every abstract, README, and post.

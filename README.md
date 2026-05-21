# The Yellow — Website

The website for **The Yellow** (Yellow Productions) — a full-stack creative
group working across India and the Gulf. Static HTML/CSS/JS, no build step.

**Domain:** theyellowverse.com

## Pages

| File | Purpose |
|------|---------|
| `index.html` / `the-yellow-home.html` | Home |
| `the-yellow-services.html` | Services — seven disciplines |
| `the-yellow-work.html` | Work — 5 case studies + projects |
| `the-yellow-writing.html` | Writing — essay index |
| `the-yellow-writing-bfsi.html` | Essay: BFSI branding |
| `the-yellow-writing-industrial.html` | Essay: industrial branding |
| `the-yellow-writing-gulf.html` | Essay: Gulf rebrand playbook |

Support files: `robots.txt`, `sitemap.xml`, `.nojekyll`.

## Hosting on GitHub Pages

1. Create a new repository on GitHub (e.g. `theyellow-site`).
2. Upload every file in this folder, keeping the structure
   (including the `.github/` and `scripts/` folders, and the
   hidden `.nojekyll` file).
3. In the repo: **Settings -> Pages**.
4. Under "Build and deployment", set **Source** to *Deploy from a branch*,
   branch **main**, folder **/ (root)**. Save.
5. The site goes live at `https://<username>.github.io/<repo>/` within
   a minute or two.
6. To use **theyellowverse.com**: in **Settings -> Pages -> Custom domain**,
   enter the domain, then add the DNS records GitHub shows you at your
   domain registrar. GitHub issues the HTTPS certificate automatically.

If you used a terminal instead of the upload UI:

```bash
git init
git add .
git commit -m "Launch The Yellow website"
git branch -M main
git remote add origin https://github.com/<username>/<repo>.git
git push -u origin main
```

## Automated checks

`.github/workflows/site-checks.yml` runs `scripts/check_site.py` on every
push and pull request. It verifies internal links resolve, every page has
its SEO tags, and all JSON-LD is valid. A failing check blocks the merge.

Run the same check locally before pushing:

```bash
python3 scripts/check_site.py
```

## SEO notes

- Every page has a unique title, meta description, keywords, canonical URL,
  Open Graph and Twitter Card tags.
- `Organization` structured data (JSON-LD) appears on every page; essays
  also carry `BlogPosting` schema.
- After going live: submit `sitemap.xml` in
  [Google Search Console](https://search.google.com/search-console)
  and verify the rich results with the
  [Rich Results Test](https://search.google.com/test/rich-results).
- The Open Graph tags reference `/og-image.jpg` — add a 1200x630px share
  image with that filename to the repo root for link previews.

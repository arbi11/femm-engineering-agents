# FEMM and Engineering Agents

Five articles by Arbaaz Khan, with Markdown sources, static HTML pages, original figures and companion examples.

1. A First Electromagnetic Model in FEMM
2. Giving an AI Agent a FEMM Experiment
3. Building a Second Brain for a FEMM Agent
4. Reproducing a Magnet-and-Coil Force Benchmark in FEMM
5. Reconstructing a Motor from a Journal Paper

## Build and preview

Run `python3 build.py` after editing an article's `part-N/index.md` file. No packages or build service are required. The HTML is committed alongside the Markdown.

To preview, run `python3 -m http.server 8765 --bind 127.0.0.1` from this directory, then open `http://127.0.0.1:8765/`.

## GitHub Pages

Repository: `arbi11/femm-engineering-agents`.

Once the repository is created and uploaded, configure Settings → Pages → Deploy from a branch → `main` → `/ (root)`. The `.nojekyll` file serves the prepared HTML and assets directly.

The source pages are public. The Medium account used to import them is independent of this repository.

## Import into a separate Medium account

Sign in to that account yourself. Open Stories → Import a story, paste one article's live GitHub Pages URL and select Import. Review the resulting draft before publishing.

Article URLs:

- `https://arbi11.github.io/femm-engineering-agents/part-1/`
- `https://arbi11.github.io/femm-engineering-agents/part-2/`
- `https://arbi11.github.io/femm-engineering-agents/part-3/`
- `https://arbi11.github.io/femm-engineering-agents/part-4/`
- `https://arbi11.github.io/femm-engineering-agents/part-5/`

Use the rendered article URL. Each URL imports one article. Check figures, equations, captions, code indentation and language settings after import; Medium's importer can omit content or require manual formatting. Medium also adds a canonical link to the original page automatically.

Official references: [Medium import](https://help.medium.com/hc/en-us/articles/214550207-Importing-a-post-to-Medium), [import troubleshooting](https://help.medium.com/hc/en-us/articles/360033931713-Trouble-importing-content-using-the-import-tool), [GitHub Pages](https://docs.github.com/en/pages/getting-started-with-github-pages/what-is-github-pages).

## Sources and examples

Parts 1–4 use the fourth review revision. Part 5 uses the latest third revision. Numerical claims, limits and retained failed checks follow those reviewed sources. `publication-manifest.json` records the source editions and figure checksums.

The Article 3 graph is a focused excerpt of the records used in the article. Its record contents and verification states are retained. Full runnable files and recorded measurements are under `examples/`. The short code blocks inside the articles are excerpts.

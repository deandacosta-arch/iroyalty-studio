# iRoyalty Studio website (static)

Plain HTML/CSS (+ ~20 lines of vanilla JS for the sound buttons). No build step, no external
fonts, scripts, trackers or CDNs. Works from any static host (GitHub Pages, Cloudflare Pages,
Netlify) or by opening `index.html` locally.

- `index.html`   home: brand intro, Combo Ladder (coming soon), audio previews, how it's made, contact
- `contact.html` dedicated contact page (Unity's docs say the site must "contain a contact page")
- `assets/audio/` MP3 previews encoded from the prototype WAVs (`tools/make_site_audio.py`)
- `assets/img/`   code-generated brand images (`tools/make_brand.py`, font Outfit, SIL OFL)
- `.nojekyll`     tells GitHub Pages to serve files as-is

Not deployed anywhere yet.

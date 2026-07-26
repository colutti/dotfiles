# Archived Theme Plan

> Histórico da migração antiga de temas. Este arquivo foi mantido apenas como registro e
> não descreve mais o fluxo atual da máquina.

**Goal:** Add Nord, Nothing-inspired and Aerospace/Gruvbox themes as self-contained manifests and wallpaper assets discovered by the existing desktop theme loader.

**Architecture:** Extend only `themes/*/manifest.json` and add one local wallpaper per theme. Reuse the existing schema, semantic palette keys, icon/cursor defaults, and supported panel layout/material values; no shell code or generated-state contract changes are needed.

**Tech Stack:** JSON manifests, local PNG/JPEG wallpaper assets, Python standard-library validation, repository shell test runner.

---

### Task 1: Create theme directories and retrieve wallpaper assets

**Files:**
- Create: `themes/nord-quiet-frost/`
- Create: `themes/glyph-nothing/`
- Create: `themes/aerospace-gruvbox/`

- [ ] **Step 1: Create the three directories**

Run:

```bash
mkdir -p themes/nord-quiet-frost themes/glyph-nothing themes/aerospace-gruvbox
```

- [ ] **Step 2: Retrieve the Nothing-inspired wallpaper**

Use the Wallhaven source identified by the Reddit post. Download the image into
`themes/glyph-nothing/wallpaper.jpg`; record the final URL and SHA-256 in the
manifest.

- [ ] **Step 3: Retrieve the Aerospace wallpaper**

Use the `spacehawks` source attributed by the Reddit author, preferring the
original asset from the referenced dotfiles/source page. Save it as
`themes/aerospace-gruvbox/spacehawks.jpg` and record its source URL and SHA-256.

- [ ] **Step 4: Retrieve a licensed Nord wallpaper**

Choose a cold blue/icy wallpaper with an explicit reusable license, save it as
`themes/nord-quiet-frost/ice-field.jpg`, and record source URL, license URL and
SHA-256. If either Reddit asset is unavailable or has unclear reuse terms, use a
visually equivalent licensed asset and state the fallback URL in its manifest.

- [ ] **Step 5: Verify the three files are real images**

Run:

```bash
file themes/nord-quiet-frost/ice-field.jpg themes/glyph-nothing/wallpaper.jpg themes/aerospace-gruvbox/spacehawks.jpg
sha256sum themes/nord-quiet-frost/ice-field.jpg themes/glyph-nothing/wallpaper.jpg themes/aerospace-gruvbox/spacehawks.jpg
```

Expected: each file reports JPEG/PNG image data and produces one stable SHA-256.

- [ ] **Step 6: Commit the assets**

```bash
git add themes/nord-quiet-frost themes/glyph-nothing themes/aerospace-gruvbox
git commit -m "feat: add wallpapers for new desktop themes"
```

### Task 2: Add the three manifests

**Files:**
- Create: `themes/nord-quiet-frost/manifest.json`
- Create: `themes/glyph-nothing/manifest.json`
- Create: `themes/aerospace-gruvbox/manifest.json`

- [ ] **Step 1: Add the Nord manifest**

Create a schema-version-1 dark manifest with slug `nord-quiet-frost`, Noto Sans,
JetBrainsMono Nerd Font, Papirus-Dark, Breeze, panel `rail`/`matte`/`180`, and
palette `#2e3440`, `#3b4252`, `#434c5e`, `#eceff4`, `#d8dee9`, `#88c0d0`,
`#81a1c1`, `#a3be8c`, `#ebcb8b`, `#bf616a`, `#4c566a` in existing semantic
key order. Set wallpaper file `ice-field.jpg` and include source, license and
SHA-256.

- [ ] **Step 2: Add the Nothing-inspired manifest**

Create a schema-version-1 light manifest with slug `glyph-nothing`, Papirus,
Breeze, panel `islands`/`solid`/`160`, and palette
`#f1f1ef`, `#ffffff`, `#e4e4e1`, `#171717`, `#626262`, `#d71920`, `#171717`,
`#3f7d4b`, `#a56a00`, `#b51218`, `#b7b7b2` in semantic key order. Set wallpaper
file `wallpaper.jpg`, include the Wallhaven/source URL and SHA-256, and use a
measured contrast ratio of at least `7.0`.

- [ ] **Step 3: Add the Aerospace/Gruvbox manifest**

Create a schema-version-1 dark manifest with slug `aerospace-gruvbox`,
Papirus-Dark, Breeze, panel `architect`/`matte`/`180`, and palette
`#282828`, `#3c3836`, `#504945`, `#ebdbb2`, `#bdae93`, `#fabd2f`, `#d79921`,
`#b8bb26`, `#fe8019`, `#fb4934`, `#665c54` in semantic key order. Set wallpaper
file `spacehawks.jpg` and include source, attribution and SHA-256.

- [ ] **Step 4: Parse the new manifests**

Run:

```bash
python -m json.tool themes/nord-quiet-frost/manifest.json >/dev/null
python -m json.tool themes/glyph-nothing/manifest.json >/dev/null
python -m json.tool themes/aerospace-gruvbox/manifest.json >/dev/null
```

Expected: all commands exit `0` with no parse errors.

- [ ] **Step 5: Commit the manifests**

```bash
git add themes/nord-quiet-frost/manifest.json themes/glyph-nothing/manifest.json themes/aerospace-gruvbox/manifest.json
git commit -m "feat: add Nord Nothing and Aerospace themes"
```

### Task 3: Validate discovery and repository contracts

Este plano antigo foi substituído pela configuração DANK atual. Não use os passos
abaixo como referência operacional.

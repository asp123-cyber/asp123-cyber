// Optional raster previews. Requires Node.js and sharp; the scientific SVG
// generator itself uses only Python's standard library.
const path = require('path');
const fs = require('fs');
const sharp = require(process.env.CODEX_PRIMARY_RUNTIME_NODE_MODULES
  ? path.join(process.env.CODEX_PRIMARY_RUNTIME_NODE_MODULES, 'sharp') : 'sharp');
const root = path.resolve(__dirname, '..');

(async () => {
  const destination = path.join(root, 'docs', 'previews');
  fs.mkdirSync(destination, { recursive: true });
  for (const theme of ['light', 'dark']) {
    for (const compact of [false, true]) {
      const middle = compact ? '-compact' : '';
      const width = compact ? 400 : 840;
      const names = [`header${middle}-${theme}`,
        `quantum${middle}-still-${theme}`, `ml-vision${middle}-still-${theme}`];
      let top = 0;
      const layers = [];
      for (const name of names) {
        const input = await sharp(path.join(root, 'assets', 'profile', name + '.svg')).png().toBuffer();
        const metadata = await sharp(input).metadata();
        layers.push({ input, left: 0, top });
        top += metadata.height + 16;
      }
      const output = path.join(destination, `visuals${middle}-${theme}.png`);
      await sharp({ create: { width, height: top - 16, channels: 4,
        background: theme === 'light' ? '#ffffff' : '#0d1117' } })
        .composite(layers).png().toFile(output);
      console.log(output);
    }
  }
})().catch(error => { console.error(error); process.exitCode = 1; });

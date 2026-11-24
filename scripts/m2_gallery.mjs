// M2: render one still of every code component through the look layer, in one browser, then lay them out on a sheet.
// Refuses to run beside ComfyUI (memory plan in CLAUDE.md).
// Usage: node scripts/m2_gallery.mjs [id ...]  ->  review/m2/<id>.png, then scripts/m2_sheet.py makes review/m2_components.jpg
import {execSync} from 'child_process';
import fs from 'fs';
import os from 'os';
import path from 'path';
import {bundle} from '@remotion/bundler';
import {getCompositions, openBrowser, renderStill} from '@remotion/renderer';

try {
  execSync("pgrep -f 'ComfyUI/[m]ain.py'", {stdio: 'ignore'});
  console.error('ComfyUI is running: refusing to render beside it');
  process.exit(1);
} catch { /* not running */ }

const only = process.argv.slice(2);
const browserExecutable = path.join(os.homedir(),
  '.cache/puppeteer/chrome-headless-shell/linux-148.0.7778.97/chrome-headless-shell-linux64/chrome-headless-shell');
const chromiumOptions = {gl: 'swangle'};
const serveUrl = await bundle({entryPoint: path.resolve('remotion/src/index.ts'), publicDir: path.resolve('remotion/public')});
const puppeteerInstance = await openBrowser('chrome', {browserExecutable, chromiumOptions});
const comps = await getCompositions(serveUrl, {puppeteerInstance, chromiumOptions});
fs.mkdirSync('review/m2', {recursive: true});
for (const composition of comps) {
  if (only.length && !only.includes(composition.id)) continue;
  const output = `review/m2/${composition.id}.png`;
  await renderStill({composition, serveUrl, output, frame: composition.props.stillFrame, puppeteerInstance, imageFormat: 'png', chromiumOptions});
  console.log(output);
}
await puppeteerInstance.close({silent: true});

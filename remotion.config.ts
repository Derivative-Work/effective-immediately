import os from 'os';
import path from 'path';
import {Config} from '@remotion/cli/config';

// After All Systems Operational's remotion.config.ts (701009f, MIT): sources in remotion/, low concurrency while the
// CPU is shared with the Blender parts of M3. The browser is Puppeteer's headless shell (npm ci; CLAUDE.md), so
// Remotion doesn't download its own.
Config.setEntryPoint('remotion/src/index.ts');
Config.setPublicDir('remotion/public');
Config.setVideoImageFormat('png');
Config.setConcurrency(2);
Config.setChromiumOpenGlRenderer('swangle');
Config.setBrowserExecutable(path.join(os.homedir(),
  '.cache/puppeteer/chrome-headless-shell/linux-148.0.7778.97/chrome-headless-shell-linux64/chrome-headless-shell'));

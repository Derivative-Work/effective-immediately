// After Sugar Push's remotion/src/Fonts.tsx (MIT): load the fonts and hold the render until they're ready.
import React, {useEffect, useState} from 'react';
import {continueRender, delayRender, staticFile} from 'remotion';

// All SIL OFL 1.1 (remotion/public/fonts; SOURCES.md has the URL and sha256 of each).
const FACES: [string, string, string][] = [
  ['Inter', 'fonts/Inter-VF.ttf', '100 900'], // every device screen, sign and card: the company's voice
  ['Jost', 'fonts/Jost-VF.ttf', '100 900'], // the lower thirds and tags: the video's own voice
  ['Courier Prime', 'fonts/CourierPrime-Regular.ttf', '400'], // subtitles: the filing
  ['Courier Prime', 'fonts/CourierPrime-Bold.ttf', '700'],
  ['VT323', 'fonts/VT323-Regular.ttf', '400'], // subtitles: closed captions and the phone's display
  ['Shrikhand', 'fonts/Shrikhand-Regular.ttf', '400'], // subtitles: boogie-funk lettering
  ['Liberation Mono', 'fonts/LiberationMono-Regular.ttf', '400'], // E01: the terminal
  ['Liberation Mono', 'fonts/LiberationMono-Bold.ttf', '700'],
];

export const UI = "'Inter', sans-serif";
export const LABEL = "'Jost', sans-serif";
export const MONO = "'Liberation Mono', monospace";

export const Fonts: React.FC = () => {
  const [handle] = useState(() => delayRender('fonts'));
  useEffect(() => {
    Promise.all(FACES.map(([family, file, weight]) => {
      const f = new FontFace(family, `url(${staticFile(file)})`, {weight});
      return f.load().then((loaded) => document.fonts.add(loaded));
    })).then(() => continueRender(handle)).catch((e) => { console.error(e); continueRender(handle); });
  }, [handle]);
  return null;
};

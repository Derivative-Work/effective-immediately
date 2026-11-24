import React from 'react';
import {AbsoluteFill, Img, staticFile} from 'remotion';
import {LABEL, UI} from './Fonts';

/**
 * Thumbnail options (1280x720) for METADATA.md. Brief: the empty jacket's hook or the empty counselor's chair. No Nvidia
 * name, logo, green or product names (they appear only in the video's real-screenshot bookends), no faces.
 */
const SHADOW = '0 4px 0 rgba(0,0,0,0.35), 0 0 28px rgba(0,0,0,0.75)';
const big: React.CSSProperties = {fontFamily: UI, fontWeight: 900, color: '#fff', letterSpacing: '-0.02em', lineHeight: 0.92, textShadow: SHADOW, textTransform: 'uppercase'};
const tag: React.CSSProperties = {fontFamily: LABEL, fontWeight: 600, letterSpacing: '0.12em', color: '#fff', textShadow: SHADOW, textTransform: 'uppercase'};

const Plate: React.FC<{src: string; pos?: string; style?: React.CSSProperties}> = ({src, pos = 'center', style}) => (
  <Img src={staticFile(`gen/plates/${src}.png`)} style={{position: 'absolute', inset: 0, width: '100%', height: '100%', objectFit: 'cover', objectPosition: pos, ...style}} />
);

/**
 * A: the empty hook on Nov 12, the jacket back in the booth on Nov 23. The booth half starts at the plate's left edge, where
 * the jacket is, so all of it shows beside the divider (human note: it was cropped).
 *
 * Sized for phones (human note: the text was too small to read on mobile). The hook's half is wider (A_LEFT) so the title
 * can stack in two lines on its bare wall; the booth's half is just wide enough for the whole jacket (440 px at this scale).
 * Each half's date sits at its top, above the hook and the jacket's collar, so no text covers either. S01 is scaled a
 * little past cover (A_HOOK_K) and anchored at its foot, which lifts the hook (plate y 467-627) to y ~225-350, clear of the
 * title, and makes it bigger.
 *
 * The booth half uses S03_thumbA, a copy of the plate with the jacket graded apart from the seat it lies on (human note: "the
 * jacket is blending in with the seat it's on"; thumbnail only). `scripts/thumb_jacket.py` makes it: the booth is lifted to
 * a warmer, lighter brown and the jacket made a more neutral black. It's baked into the file because Chrome softened the
 * half when the same grade was done with CSS blend layers.
 */
const A_LEFT = 830;
const A_HOOK_K = 0.8; // S01's scale (cover is 720/1088 = 0.662)
const A_HOOK_X = 780; // where the half starts in the scaled plate: bare wall only (scaled x 768-1884), the hook at x ~315-410
const Split: React.FC = () => (
  <AbsoluteFill style={{background: '#000'}}>
    <div style={{position: 'absolute', left: 0, top: 0, width: A_LEFT, height: 720, overflow: 'hidden'}}>
      <Img src={staticFile('gen/plates/S01.png')} style={{position: 'absolute', left: -A_HOOK_X, top: 720 - 1088 * A_HOOK_K, width: 2560 * A_HOOK_K, height: 1088 * A_HOOK_K, filter: 'saturate(0.6) brightness(0.8)'}} />
      <AbsoluteFill style={{background: 'linear-gradient(180deg, rgba(0,0,0,0.6) 0%, rgba(0,0,0,0) 24%, rgba(0,0,0,0) 52%, rgba(0,0,0,0.6) 70%, rgba(0,0,0,0.82) 100%)'}} />
    </div>
    <div style={{position: 'absolute', left: A_LEFT, top: 0, width: 1280 - A_LEFT, height: 720, overflow: 'hidden'}}>
      <Plate src="S03_thumbA" pos="0% 50%" />
      <AbsoluteFill style={{background: 'linear-gradient(180deg, rgba(0,0,0,0.65) 0%, rgba(0,0,0,0.2) 20%, rgba(0,0,0,0) 30%)'}} />
    </div>
    <div style={{position: 'absolute', left: A_LEFT - 4, top: 0, width: 8, height: 720, background: '#fff'}} />
    <div style={{...big, position: 'absolute', left: 34, top: 26, fontSize: 84, fontWeight: 800, letterSpacing: '0.02em'}}>Nov 12</div>
    <div style={{...big, position: 'absolute', right: 30, top: 26, fontSize: 84, fontWeight: 800, letterSpacing: '0.02em'}}>Nov 23</div>
    <div style={{position: 'absolute', left: 30, bottom: 24, display: 'flex', flexDirection: 'column'}}>
      <div style={{...big, fontSize: 116, letterSpacing: '-0.035em', lineHeight: 0.88}}>Effective<br />immediately</div>
      <div style={{...tag, fontSize: 56, fontWeight: 700, letterSpacing: '0.01em', textTransform: 'none', marginTop: 12}}>(until further notice)</div>
    </div>
  </AbsoluteFill>
);

/** B: the empty hook alone. */
const Hook: React.FC = () => (
  <AbsoluteFill style={{background: '#000'}}>
    <Plate src="S01" pos="0% 50%" style={{filter: 'saturate(0.7)'}} />
    <AbsoluteFill style={{background: 'linear-gradient(90deg, rgba(0,0,0,0.75) 0%, rgba(0,0,0,0.4) 40%, rgba(0,0,0,0) 58%)'}} />
    <div style={{...big, position: 'absolute', left: 44, top: 130, fontSize: 92}}>Out.<br />Effective<br />immediately.</div>
    <div style={{...tag, position: 'absolute', left: 52, bottom: 70, fontSize: 40}}>Back in 11 days</div>
  </AbsoluteFill>
);

/** C: the empty counselor's chair (E23). */
const Chair: React.FC = () => (
  <AbsoluteFill style={{background: '#000'}}>
    <Plate src="S02" pos="50% 50%" />
    <AbsoluteFill style={{background: 'linear-gradient(180deg, rgba(0,0,0,0.55) 0%, rgba(0,0,0,0) 40%, rgba(0,0,0,0) 62%, rgba(0,0,0,0.7) 100%)'}} />
    <div style={{...big, position: 'absolute', left: 0, right: 0, top: 36, textAlign: 'center', fontSize: 92}}>We did not intend…</div>
    <div style={{...big, position: 'absolute', left: 0, right: 0, bottom: 52, textAlign: 'center', fontSize: 80}}>(to take him back)</div>
  </AbsoluteFill>
);

export const THUMBNAILS: Record<string, React.FC> = {A: Split, B: Hook, C: Chair};

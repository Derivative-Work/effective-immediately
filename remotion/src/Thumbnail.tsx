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
 * the jacket is, so all of it shows beside the divider (human note: it was cropped); the title sits across the top, clear of
 * the jacket and the hook.
 */
const Split: React.FC = () => (
  <AbsoluteFill style={{background: '#000'}}>
    <div style={{position: 'absolute', left: 0, top: 0, width: 640, height: 720, overflow: 'hidden'}}>
      <Plate src="S01" pos="60% 50%" style={{filter: 'saturate(0.6) brightness(0.95)'}} />
    </div>
    <div style={{position: 'absolute', left: 640, top: 0, width: 640, height: 720, overflow: 'hidden'}}>
      <Plate src="S03" pos="0% 50%" />
    </div>
    <AbsoluteFill style={{background: 'linear-gradient(180deg, rgba(0,0,0,0.55) 0%, rgba(0,0,0,0.15) 26%, rgba(0,0,0,0) 40%, rgba(0,0,0,0) 80%, rgba(0,0,0,0.45) 100%)'}} />
    <div style={{position: 'absolute', left: 636, top: 0, width: 8, height: 720, background: '#fff'}} />
    <div style={{...big, position: 'absolute', left: 0, right: 0, top: 26, textAlign: 'center', fontSize: 86}}>Effective immediately</div>
    <div style={{...tag, position: 'absolute', left: 0, right: 0, top: 120, textAlign: 'center', fontSize: 32, letterSpacing: '0.06em', textTransform: 'none'}}>(until further notice)</div>
    <div style={{...tag, position: 'absolute', left: 34, bottom: 28, fontSize: 46}}>Nov 12</div>
    <div style={{...tag, position: 'absolute', right: 34, bottom: 28, fontSize: 46}}>Nov 23</div>
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

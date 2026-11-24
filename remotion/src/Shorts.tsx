import React from 'react';
import {AbsoluteFill, Sequence, useCurrentFrame} from 'remotion';
import shorts from '../../config/shorts.json';
import {Animatic} from './Animatic';
import {SubLine} from './components/Subtitles';
import {PIC_H, PIC_W} from './config';
import {LABEL} from './Fonts';
import {HALO, T} from './theme';

/**
 * The vertical Shorts, 1080x1920, one per entry in config/shorts.json (after Distillation (Allegedly)'s src/Shorts.tsx).
 * Everything sits inside the platforms' safe zone, y 140-1400 and clear of the ~130 px button rail on the right:
 * - above: the "Effective immediately" lower third as the title (brief), with the satire line;
 * - the main edit's whole picture, uncropped (so nothing in its framing is lost), 950 px wide, with its own audio;
 * - below: the lyrics in the main edit's style for each section, scaled to fit.
 */
const SAFE_W = 950;
const K = SAFE_W / PIC_W;
const PIC_TOP = 590, BOX_H = Math.round(PIC_H * K);
const CFG = shorts as {shorts: Record<string, {from: number; to: number; sub: string}>};
export const SHORT_IDS = Object.keys(CFG.shorts);
export const shortSpec = (id: string) => ({from: CFG.shorts[id].from, frames: CFG.shorts[id].to - CFG.shorts[id].from, sub: CFG.shorts[id].sub});

const Lyrics: React.FC<{from: number}> = ({from}) => {
  const f = useCurrentFrame();
  return (
    <div style={{position: 'absolute', left: 0, top: PIC_TOP + BOX_H + 40, width: SAFE_W, height: 220, display: 'flex', alignItems: 'flex-start', justifyContent: 'center'}}>
      <div style={{transform: 'scale(0.74)', transformOrigin: '50% 0'}}><SubLine f={f + from} /></div>
    </div>
  );
};

export const Short: React.FC<{id: string}> = ({id}) => {
  const {from, sub} = shortSpec(id);
  return (
    <AbsoluteFill style={{background: '#0b0d0f'}}>
      <div style={{position: 'absolute', left: 64, top: 290, fontFamily: LABEL, color: T.white, textShadow: HALO}}>
        <div style={{fontSize: 24, fontWeight: 500, letterSpacing: '0.16em', textTransform: 'uppercase', color: T.soft, marginBottom: 34}}>AI-generated satire · not investment advice</div>
        <div style={{width: 90, height: 4, background: T.white, marginBottom: 18}} />
        <div style={{fontSize: 76, fontWeight: 500, letterSpacing: '0.03em', lineHeight: 1.05}}>Effective immediately</div>
        <div style={{fontSize: 30, fontWeight: 400, letterSpacing: '0.14em', textTransform: 'uppercase', marginTop: 12, color: T.soft}}>{sub}</div>
      </div>
      <div style={{position: 'absolute', left: 0, top: PIC_TOP, width: SAFE_W, height: BOX_H, overflow: 'hidden'}}>
        <div style={{position: 'absolute', left: 0, top: -((1080 - PIC_H) / 2) * K, width: 1920, height: 1080, transform: `scale(${K})`, transformOrigin: '0 0'}}>
          <Sequence from={-from}><Animatic subStyle="none" slate={false} /></Sequence>
        </div>
      </div>
      <Lyrics from={from} />
    </AbsoluteFill>
  );
};

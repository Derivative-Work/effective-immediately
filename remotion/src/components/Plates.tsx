import React from 'react';
import {AbsoluteFill, Img, staticFile, useCurrentFrame} from 'remotion';
import sim from '../../public/gen/jacket_sim/meta.json';
import layout from '../../public/gen/s01_layout.json';
import {FPS, LOOK, PIC_H, PIC_W, SAGA} from '../config';
import {UI} from '../Fonts';
import {insetQuad, pinMatrix, Quad} from '../look/pin';

/** A generated still, filling the picture, with an optional slow push (never over the brief's 5% of width per second). */
export const Plate: React.FC<{src: string; pushPerS?: number; origin?: string}> = ({src, pushPerS = 0, origin = '50% 50%'}) => {
  const f = useCurrentFrame();
  const rate = Math.min(pushPerS, LOOK.move.max_width_per_s);
  return (
    <AbsoluteFill style={{overflow: 'hidden'}}>
      <Img src={staticFile(src)} style={{width: PIC_W, height: PIC_H, objectFit: 'cover', transform: `scale(${1 + (rate * f) / FPS})`, transformOrigin: origin}} />
    </AbsoluteFill>
  );
};

/**
 * E04, E05, E22: the wall and the jacket. The wall is one plate (S01b, with the unfaded jacket shape). The jacket is a
 * simulated sequence the size of that plate (scripts/jacket_sim.py): it unhooks, swings away and, on the return, catches
 * on the hook and settles slightly crooked. Never worn.
 */
export const JacketWall: React.FC<{mode: 'hung' | 'lift' | 'return' | 'gone'; at?: number; pushPerS?: number}> = ({mode, at = 12, pushPerS = 0.022}) => {
  const f = useCurrentFrame();
  const [pw, ph] = layout.plate;
  const k = Math.max(PIC_W / pw, PIC_H / ph);
  const ox = (PIC_W - pw * k) / 2, oy = (PIC_H - ph * k) / 2;
  const j = layout.jacket;
  const push = 1 + (Math.min(pushPerS, LOOK.move.max_width_per_s) * f) / FPS;
  const seq = mode === 'return' ? 'return' : 'lift';
  const last = sim[seq].frames - 1;
  const i = mode === 'hung' ? 0 : Math.max(0, Math.min(last, f - at));
  const show = mode !== 'gone' && (mode !== 'return' || f >= at);
  return (
    <AbsoluteFill style={{overflow: 'hidden'}}>
      <div style={{position: 'absolute', inset: 0, transform: `scale(${push})`,
        transformOrigin: `${ox + (j.x + j.w / 2) * k}px ${oy + (j.y + j.h / 2) * k}px`}}>
        <div style={{position: 'absolute', left: ox, top: oy, width: pw, height: ph, transform: `scale(${k})`, transformOrigin: '0 0'}}>
          <Img src={staticFile('gen/S01b.png')} style={{position: 'absolute', inset: 0, width: pw, height: ph}} />
          {show && <Img src={staticFile(`gen/jacket_sim/${seq}/${String(i).padStart(4, '0')}.png`)} style={{position: 'absolute', inset: 0, width: pw, height: ph}} />}
        </div>
      </div>
    </AbsoluteFill>
  );
};

/**
 * E20, E21: the caller ID, corner-pinned to the desk phone's blank display (scripts/track_display.py). It multiplies
 * into the display's own glow and takes a touch of the plate's softness, so it reads as lit by the screen.
 */
export const DisplayText: React.FC<{quad: Quad; text?: string}> = ({quad, text = 'SENIOR LEVELS'}) => {
  const w = 640, h = 220;
  return (
    <div style={{position: 'absolute', left: 0, top: 0, width: w, height: h, transformOrigin: '0 0', transform: pinMatrix(w, h, insetQuad(quad, 0.035, 0.07)),
      mixBlendMode: 'multiply', filter: 'blur(0.7px)', display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center',
      fontFamily: UI, color: '#06303a', whiteSpace: 'nowrap'}}>
      <div style={{fontSize: 34, fontWeight: 600, letterSpacing: '0.2em', opacity: 0.82}}>INCOMING CALL</div>
      <div style={{fontSize: 74, fontWeight: 800, letterSpacing: '0.025em', lineHeight: 1.12}}>{text}</div>
    </div>
  );
};

export const REINSTATED = SAGA.reinstated;

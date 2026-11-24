import React from 'react';
import {AbsoluteFill, Img, staticFile, useCurrentFrame} from 'remotion';
import {Grade, LOOK, PIC_H, PIC_W, SEED} from '../config';
import {hash, smooth} from './rand';

/**
 * The one wrapper every shot passes through (brief, "The look layer"). Stacking order:
 * handheld drift -> grade (saturation, teal-leaning matrix, flat curve) -> bloom and halation -> haze -> grain ->
 * vignette -> whatever is composited after the grade (the probe) -> 2.39:1 letterbox. Randomness is seeded per frame.
 */

const HAND_X = 1, HAND_Y = 2, HAND_R = 3, GRAIN = 4, GRAIN_X = 5, GRAIN_Y = 6, HAZE_X = 7, HAZE_Y = 8;

const GradeFilter: React.FC<{grade: Grade}> = ({grade}) => {
  const g = LOOK.grades[grade];
  const curve = g.curve.join(' ');
  const hi = LOOK.highlights.join(' ');
  const b = LOOK.bloom.strength;
  const h = LOOK.halation;
  return (
    <svg width={0} height={0} style={{position: 'absolute'}}>
      <filter id={`look-${grade}`} x="0" y="0" width="100%" height="100%" colorInterpolationFilters="sRGB">
        <feColorMatrix type="saturate" values={String(g.saturation)} />
        <feColorMatrix type="matrix" values={g.matrix.join(' ')} />
        <feComponentTransfer result="graded">
          <feFuncR type="table" tableValues={curve} />
          <feFuncG type="table" tableValues={curve} />
          <feFuncB type="table" tableValues={curve} />
        </feComponentTransfer>
        <feComponentTransfer in="graded" result="hi">
          <feFuncR type="table" tableValues={hi} />
          <feFuncG type="table" tableValues={hi} />
          <feFuncB type="table" tableValues={hi} />
        </feComponentTransfer>
        <feGaussianBlur in="hi" stdDeviation={LOOK.bloom.blur_px} />
        <feColorMatrix type="matrix" values={`${b} 0 0 0 0  0 ${b} 0 0 0  0 0 ${b} 0 0  0 0 0 1 0`} result="bloom" />
        <feGaussianBlur in="hi" stdDeviation={LOOK.halation.blur_px} />
        <feColorMatrix type="matrix" values={`${h.red} 0 0 0 0  0 ${h.green} 0 0 0  0 0 ${h.blue} 0 0  0 0 0 1 0`} result="halation" />
        <feBlend in="graded" in2="bloom" mode="screen" result="withBloom" />
        <feBlend in="withBloom" in2="halation" mode="screen" />
      </filter>
    </svg>
  );
};

export type Flare = {x: number; y: number; strength?: number};

/** Horizontal anamorphic streaks, only where a shot names a hard practical light. */
const Flares: React.FC<{flares: Flare[]; grade: Grade}> = ({flares, grade}) => {
  const tint = grade === 'warm' ? '255,196,120' : '150,215,255';
  const {length_px: len, height_px: ht, opacity} = LOOK.flare;
  return (
    <>
      {flares.map((f, i) => (
        <div key={i} style={{position: 'absolute', left: f.x * PIC_W - len / 2, top: f.y * PIC_H - ht / 2, width: len, height: ht,
          mixBlendMode: 'screen', opacity: opacity * (f.strength ?? 1), filter: 'blur(1px)',
          background: `linear-gradient(90deg, rgba(${tint},0), rgba(${tint},0.9) 50%, rgba(${tint},0))`}} />
      ))}
    </>
  );
};

export const LookLayer: React.FC<{
  children: React.ReactNode;
  grade: Grade;
  /** Seeded camera drift for stills and locked-off clips; off for overhead shots and clips that carry their own. */
  handheld?: boolean;
  flares?: Flare[];
  /** Composited after the grade, so it keeps its own colour (the green probe). */
  afterGrade?: React.ReactNode;
  /** The master frame this layer's frame 0 stands for, so grain and drift match between the main video and the Short. */
  frameOffset?: number;
}> = ({children, grade, handheld = false, flares = [], afterGrade, frameOffset = 0}) => {
  const f = useCurrentFrame() + frameOffset;
  const hh = LOOK.handheld;
  const transform = handheld
    ? `translate(${smooth(SEED, HAND_X, f, hh.period_frames) * hh.x_px}px, ${smooth(SEED, HAND_Y, f, hh.period_frames) * hh.y_px}px) ` +
      `rotate(${smooth(SEED, HAND_R, f, hh.period_frames * 1.4) * hh.rotate_deg}deg) scale(${hh.overscan})`
    : undefined;
  const plate = Math.floor(hash(SEED, GRAIN, f) * LOOK.grain.plates);
  const gx = (hash(SEED, GRAIN_X, f) - 0.5) * 160, gy = (hash(SEED, GRAIN_Y, f) - 0.5) * 160;
  const hz = LOOK.haze;
  const hx = smooth(SEED, HAZE_X, f, hz.period_frames) * hz.drift_px, hy = smooth(SEED, HAZE_Y, f, hz.period_frames) * hz.drift_px * 0.5;
  const v = LOOK.vignette;
  return (
    <AbsoluteFill style={{background: '#000', alignItems: 'center', justifyContent: 'center'}}>
      <GradeFilter grade={grade} />
      <div style={{position: 'relative', width: PIC_W, height: PIC_H, overflow: 'hidden', background: '#000'}}>
        <div style={{position: 'absolute', inset: 0, filter: `url(#look-${grade})`}}>
          <div style={{position: 'absolute', inset: 0, transform}}>{children}</div>
        </div>
        <Flares flares={flares} grade={grade} />
        <div style={{position: 'absolute', inset: -120, transform: `translate(${hx}px, ${hy}px)`, mixBlendMode: 'screen', opacity: hz.opacity,
          background: 'radial-gradient(ellipse 60% 70% at 38% 34%, rgba(255,255,255,0.9), rgba(255,255,255,0) 72%), radial-gradient(ellipse 50% 60% at 72% 62%, rgba(255,255,255,0.6), rgba(255,255,255,0) 70%)'}} />
        <div style={{position: 'absolute', inset: -100, transform: `translate(${gx}px, ${gy}px)`, mixBlendMode: 'overlay', opacity: LOOK.grain.opacity}}>
          <Img src={staticFile(`grain/grain_${String(plate).padStart(2, '0')}.png`)} style={{width: PIC_W + 200, height: PIC_H + 200}} />
        </div>
        <div style={{position: 'absolute', inset: 0,
          background: `radial-gradient(ellipse at center, rgba(0,0,0,0) ${v.inner * 100}%, rgba(0,0,0,${v.strength}) 100%)`}} />
        {/* It rides the same camera drift as the plate, so it stays put in the scene. */}
        {afterGrade && <div style={{position: 'absolute', inset: 0, transform}}>{afterGrade}</div>}
      </div>
    </AbsoluteFill>
  );
};

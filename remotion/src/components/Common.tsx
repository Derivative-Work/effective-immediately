import React from 'react';
import {AbsoluteFill, interpolate, useCurrentFrame} from 'remotion';
import {LABEL} from '../Fonts';
import {FADE, HALO, M, T} from '../theme';

export const useFade = (at = 0, len = FADE) =>
  interpolate(useCurrentFrame(), [at, at + len], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});

/** A neutral dark office surface for device shots, so they sit in the same world as the plates. */
export const DarkRoom: React.FC<{children?: React.ReactNode; tone?: 'cold' | 'night'}> = ({children, tone = 'cold'}) => (
  <AbsoluteFill style={{background: tone === 'cold'
    ? 'radial-gradient(ellipse 80% 90% at 50% 30%, #4c5358 0%, #2a2e32 55%, #15171a 100%)'
    : 'radial-gradient(ellipse 70% 80% at 50% 40%, #16323c 0%, #0c1b22 55%, #060c10 100%)'}}>
    {children}
  </AbsoluteFill>
);

/** The series' lower third: one rule, tracked caps, no box. Sits inside the letterboxed picture. */
export const LowerThird: React.FC<{title: string; sub?: string; at?: number}> = ({title, sub, at = 0}) => {
  const o = useFade(at);
  return (
    <div style={{position: 'absolute', left: M.x, bottom: M.y, opacity: o, fontFamily: LABEL, color: T.white, textShadow: HALO}}>
      <div style={{width: 72, height: 3, background: T.white, marginBottom: 14, boxShadow: '0 0 10px rgba(6,8,10,0.6)'}} />
      <div style={{fontSize: 44, fontWeight: 500, letterSpacing: '0.04em', lineHeight: 1.1}}>{title}</div>
      {sub && <div style={{fontSize: 24, fontWeight: 400, letterSpacing: '0.14em', textTransform: 'uppercase', marginTop: 8, color: T.soft}}>{sub}</div>}
    </div>
  );
};

/** On-screen tags that stack beside the caller ID (E21), one per sung line. */
export const TagStack: React.FC<{tags: {text: string; at: number}[]; right?: number; left?: number; top?: number; width?: number}> = ({tags, right = M.x, left, top = 120, width = 760}) => {
  const f = useCurrentFrame();
  return (
    <div style={{position: 'absolute', ...(left !== undefined ? {left} : {right}), top, width, display: 'flex', flexDirection: 'column', gap: 18}}>
      {tags.filter((t) => f >= t.at).map((t) => (
        <div key={t.text} style={{fontFamily: LABEL, fontSize: 32, lineHeight: 1.22, fontWeight: 450, color: T.white, textShadow: HALO,
          borderLeft: `3px solid ${T.white}`, paddingLeft: 18,
          opacity: interpolate(f, [t.at, t.at + FADE], [0, 1], {extrapolateRight: 'clamp'})}}>
          {t.text}
        </div>
      ))}
    </div>
  );
};

/** Renders the brief's unfilled [placeholders] in alert red so one can't ship by accident. */
/** Brackets that are part of a real name, not an unfilled placeholder (FLUX.2 [dev] is the model's name). */
const NOT_PLACEHOLDERS = new Set(['[dev]']);

export const WithPlaceholders: React.FC<{text: string}> = ({text}) => (
  <>
    {text.split(/(\[[^\]]+\])/).map((part, i) => part.startsWith('[') && !NOT_PLACEHOLDERS.has(part)
      ? <span key={i} style={{color: '#fff', background: T.alert, padding: '0 6px'}}>{part}</span>
      : <React.Fragment key={i}>{part}</React.Fragment>)}
  </>
);

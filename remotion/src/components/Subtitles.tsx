import React from 'react';
import {interpolate, useCurrentFrame} from 'remotion';
import subs from '../../public/gen/timing/subs.json';
import {H, PIC_H} from '../config';
import {UI} from '../Fonts';

/**
 * Burned-in lyrics, in the letterbox so they never cover the picture or its on-screen text. Each style comes from
 * something in the story's world:
 * - filing: the typewriter face of an SEC filing, typed out as it's sung
 * - broadcast: the blocky white-on-black of TV closed captions, rolling on word by word
 * - lcd: the desk phone's caller-ID display
 * - disco: boogie-funk record-sleeve lettering, the song's own period (icy until the reunion, gold after)
 * - set: each section takes the style of where it happens, ending on the diner's brass plaque
 */
export type SubStyle = 'filing' | 'broadcast' | 'lcd' | 'disco' | 'set';
type One = 'filing' | 'filingWarm' | 'broadcast' | 'lcd' | 'disco' | 'discoWarm' | 'brass';
type Seg = {section: string; style: string; from: number; to: number; text: string; words: {w: string; at: number}[]};

const COURIER = "'Courier Prime', 'Courier New', monospace";
const VT = "'VT323', monospace";
const FUNK = "'Shrikhand', serif";
const clamp = {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'} as const;
const WARM = new Set(['Final Chorus', 'Spoken', 'Final Tag', 'Outro']);

const Typed: React.FC<{s: Seg; f: number}> = ({s, f}) => {
  // Characters arrive across each word's first few frames; hidden ones keep their width, so the line never shifts.
  let shown = 0, total = 0;
  s.words.forEach((w, i) => {
    const len = w.w.length + (i < s.words.length - 1 ? 1 : 0);
    shown += Math.round(interpolate(f, [w.at, w.at + Math.min(9, len * 1.5)], [0, len], clamp));
    total += len;
  });
  const text = s.words.map((w) => w.w).join(' ');
  return <>{text.slice(0, shown)}<span style={{visibility: 'hidden'}}>{text.slice(shown, total)}</span></>;
};

const Line: React.FC<{s: Seg; style: One; f: number}> = ({s, style, f}) => {
  const fade = Math.min(interpolate(f, [s.from, s.from + 3], [0, 1], clamp), interpolate(f, [s.to - 3, s.to], [1, 0], clamp));
  switch (style) {
    case 'filing': case 'filingWarm':
      return <div style={{fontFamily: COURIER, fontWeight: 700, fontSize: 46, letterSpacing: '0.01em', color: style === 'filing' ? '#e9edf0' : '#f6e7c9', opacity: fade, whiteSpace: 'pre'}}><Typed s={s} f={f} /></div>;
    case 'broadcast':
      return (
        <div style={{fontFamily: VT, fontSize: 60, lineHeight: 1, color: '#fff', whiteSpace: 'pre', display: 'flex'}}>
          {s.words.map((w, i) => (
            <span key={i} style={{background: '#000', padding: '4px 0 2px', visibility: f >= w.at ? 'visible' : 'hidden'}}>{(i ? ' ' : ' ') + w.w.toUpperCase() + (i === s.words.length - 1 ? ' ' : '')}</span>
          ))}
        </div>
      );
    case 'lcd':
      return (
        <div style={{fontFamily: VT, fontSize: 56, lineHeight: 1, color: '#06303a', background: '#b8efe9', padding: '9px 24px 6px', borderRadius: 4, opacity: fade, whiteSpace: 'pre',
          boxShadow: '0 0 22px rgba(150,235,235,0.45), inset 0 0 0 2px rgba(6,48,58,0.35)'}}>{s.text.toUpperCase()}</div>
      );
    case 'disco': case 'discoWarm': {
      const warm = style === 'discoWarm';
      return (
        <div style={{fontFamily: FUNK, fontSize: 50, whiteSpace: 'pre', display: 'flex', opacity: fade, color: warm ? '#ffe7ad' : '#eefaff',
          textShadow: warm ? '3px 3px 0 #b5561c' : '3px 3px 0 #2c7f94'}}>
          {s.words.map((w, i) => {
            const pop = interpolate(f, [w.at, w.at + 3, w.at + 9], [1, 1.1, 1], clamp);
            return <span key={i} style={{display: 'inline-block', marginRight: i < s.words.length - 1 ? '0.34em' : 0, transform: `scale(${pop})`, opacity: f >= w.at ? 1 : 0.32}}>{w.w}</span>;
          })}
        </div>
      );
    }
    case 'brass':
      return (
        <div style={{fontFamily: UI, fontWeight: 700, fontSize: 38, color: '#2a1c08', padding: '11px 34px', opacity: fade, whiteSpace: 'pre', borderRadius: 3,
          background: 'linear-gradient(135deg, #f2d48b, #c99a45 48%, #a97a2e)', textShadow: '0 1px 0 rgba(255,238,195,0.65)', boxShadow: '0 2px 8px rgba(0,0,0,0.6)'}}>{s.text}</div>
      );
  }
};

const pick = (style: SubStyle, s: Seg): One => {
  if (style === 'set') return s.style as One;
  if (style === 'filing') return WARM.has(s.section) ? 'filingWarm' : 'filing';
  if (style === 'disco') return WARM.has(s.section) ? 'discoWarm' : 'disco';
  return style;
};

/** The 'set' style's line for main-edit frame `f`, wherever the caller puts it (the Shorts draw it under the picture). */
export const SubLine: React.FC<{f: number}> = ({f}) => {
  const s = (subs as Seg[]).find((x) => f >= x.from && f <= x.to);
  return s ? <Line s={s} style={pick('set', s)} f={f} /> : null;
};

export const Subtitles: React.FC<{style: SubStyle}> = ({style}) => {
  const f = useCurrentFrame();
  const s = (subs as Seg[]).find((x) => f >= x.from && f <= x.to);
  if (!s) return null;
  const bar = (H - PIC_H) / 2;
  return (
    <div style={{position: 'absolute', left: 0, right: 0, top: H - bar, height: bar, display: 'flex', alignItems: 'center', justifyContent: 'center'}}>
      <Line s={s} style={pick(style, s)} f={f} />
    </div>
  );
};

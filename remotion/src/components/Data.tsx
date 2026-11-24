import React from 'react';
import {AbsoluteFill, Easing, interpolate, useCurrentFrame} from 'remotion';
import {SAGA, SEED} from '../config';
import {UI} from '../Fonts';
import {hash} from '../look/rand';
import market from '../../public/gen/timing/market.json';
import {T} from '../theme';

const clamp = {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'} as const;

/** E13: the scoreboard on a blank rack panel. `pulse` (0–1) comes from the bass once the timing map exists. */
export const Scoreboard: React.FC<{pulse?: number; x?: string; y?: string}> = ({pulse = 0, x = '50%', y = '50%'}) => (
  <div style={{position: 'absolute', left: x, top: y, transform: `translate(-50%, -50%) scale(${1 + pulse * 0.035})`,
    padding: '26px 54px', background: 'rgba(7,9,11,0.93)', border: `2px solid ${T.faint}`, fontFamily: UI, color: T.white,
    boxShadow: `0 0 ${24 + pulse * 46}px rgba(205,232,245,${0.14 + pulse * 0.26})`, display: 'flex', alignItems: 'baseline', gap: 34, fontVariantNumeric: 'tabular-nums'}}>
    <span style={{fontSize: 118, fontWeight: 700, letterSpacing: '-0.01em'}}>{SAGA.q3Revenue}</span>
    <span style={{fontSize: 64, fontWeight: 600}}>▲{SAGA.q3Growth}</span>
  </div>
);


/**
 * E11, E22: the boardroom screen's chart, candlesticks from real prices (scripts/market_lines.py). No ticker or logo. The
 * axis doesn't start at zero, so the Nov 11 close is a dashed line and the moves carry their percentages. A candle is red
 * when it closed below the one before; extended-hours candles sit on a faint band; a big overnight gap is a shaded band from
 * the previous close to the open, appearing with its candle. Candles from `start` on grow from their
 * open, one after another, across `durationFrames`.
 */
type Candle = {o: number; h: number; l: number; c: number; up: boolean; ext: boolean};
type Tag = {at: number; text: string; where: string};
type Jump = {at: number; from: number; to: number; up: boolean};
export const MarketChart: React.FC<{mode?: 'drop' | 'recover'; durationFrames?: number; startAt?: number}> = ({mode = 'drop', durationFrames = 48, startAt = 0}) => {
  const f = useCurrentFrame() - startAt;   // before startAt it holds its first state, so the screen is never empty or stale
  const m = market[mode] as {label: string; base: number; candles: Candle[]; start: number; gaps: number[]; jumps: Jump[]; tags: Tag[]};
  const cs = m.candles, n = cs.length;
  const W = 1920, H = 804, px = 120, py = 150, pb = 70;
  const slot = (W - 2 * px) / n, body = slot * (n > 20 ? 0.62 : 0.5);
  const X = (i: number) => px + (i + 0.5) * slot, Y = (y: number) => py + y * (H - py - pb);
  const grow = n > 20 ? 4 : 10;
  const begins = (i: number) => interpolate(i - m.start, [0, n - m.start - 1], [0, durationFrames - grow], {...clamp, easing: Easing.inOut(Easing.quad)});
  const shown = (i: number) => (i < m.start ? 1 : interpolate(f, [begins(i), begins(i) + grow], [0, 1], {...clamp, easing: Easing.out(Easing.quad)}));
  const stroke = Math.max(3, Math.round(slot * 0.07));
  return (
    <AbsoluteFill style={{background: '#0a0c0e', fontFamily: UI}}>
      <svg width={W} height={H} style={{position: 'absolute'}}>
        {cs.map((c, i) => (c.ext ? <rect key={`e${i}`} x={px + i * slot} y={py - 20} width={slot + 0.5} height={H - py - pb + 40} fill={T.white} opacity={0.035} /> : null))}
        {m.gaps.map((g) => <line key={`g${g}`} x1={px + g * slot} x2={px + g * slot} y1={py - 20} y2={H - pb + 20} stroke={T.faint} strokeWidth={3} strokeDasharray="6 10" />)}
        {m.jumps.map((j) => (
          <rect key={`j${j.at}`} x={X(j.at - 1)} width={X(j.at) - X(j.at - 1)} y={Y(Math.min(j.from, j.to))} height={Math.abs(Y(j.to) - Y(j.from))}
            fill={j.up ? T.white : T.alert} opacity={(j.up ? 0.24 : 0.3) * shown(j.at)} />
        ))}
        <line x1={px} x2={W - px} y1={Y(m.base)} y2={Y(m.base)} stroke={T.soft} strokeWidth={3} strokeDasharray="16 14" opacity={0.7} />
        {cs.map((c, i) => {
          const k = shown(i);
          if (k <= 0) return null;
          const at = (v: number) => c.o + (v - c.o) * k;
          const top = Math.min(at(c.o), at(c.c)), bot = Math.max(at(c.o), at(c.c));
          const color = c.up ? T.white : T.alert;
          return (
            <g key={i}>
              <line x1={X(i)} x2={X(i)} y1={Y(at(c.h))} y2={Y(at(c.l))} stroke={color} strokeWidth={stroke} strokeLinecap="round" />
              <rect x={X(i) - body / 2} y={Y(top)} width={body} height={Math.max(stroke, Y(bot) - Y(top))} fill={color} />
            </g>
          );
        })}
      </svg>
      <div style={{position: 'absolute', left: px, top: 34, fontSize: 56, fontWeight: 500, color: T.soft}}>{m.label}</div>
      {m.tags.filter((g) => shown(g.at) >= 1).map((g) => {
        const c = cs[g.at];
        if (g.where === 'corner') return <div key={g.text} style={{position: 'absolute', top: 30, right: px, fontSize: 60, fontWeight: 700, color: T.white, whiteSpace: 'nowrap'}}>{g.text}</div>;
        const right = X(g.at) > W * 0.6;   // past the middle, the tag sits to the candle's left
        return (
          <div key={g.text} style={{position: 'absolute', fontSize: 68, fontWeight: 700, color: T.white, whiteSpace: 'nowrap', top: Math.min(Y(c.l) - 34, H - 118),
            ...(right ? {right: W - X(g.at) + slot * 0.5 + 10} : {left: X(g.at) + body / 2 + 22})}}>{g.text}</div>
        );
      })}
    </AbsoluteFill>
  );
};

export const Confetti: React.FC<{count?: number; startFrame?: number}> = ({count = 110, startFrame = 0}) => {
  const f = useCurrentFrame() - startFrame;
  const colors = ['#f3f5f6', '#c9d2d8', '#8f9ca5', '#e5484d'];
  if (f < 0) return null;
  return (
    <AbsoluteFill style={{pointerEvents: 'none', overflow: 'hidden'}}>
      {Array.from({length: count}, (_, i) => {
        const delay = hash(SEED, 70, i) * 42;
        const t = f - delay;
        if (t < 0) return null;
        const speed = 7 + hash(SEED, 71, i) * 6;
        const y = -30 + t * speed;
        if (y > 840) return null;
        const x = hash(SEED, 72, i) * 1920 + Math.sin(t / (9 + hash(SEED, 73, i) * 9) + i) * 26;
        const w = 9 + hash(SEED, 74, i) * 10;
        const flip = Math.cos(t / (3 + hash(SEED, 75, i) * 4) + i);
        return <div key={i} style={{position: 'absolute', left: x, top: y, width: w, height: w * 0.62, background: colors[Math.floor(hash(SEED, 76, i) * colors.length)],
          opacity: 0.9, transform: `rotate(${hash(SEED, 77, i) * 360 + t * 5}deg) scaleY(${Math.abs(flip) * 0.9 + 0.1})`}} />;
      })}
    </AbsoluteFill>
  );
};

/** E15: the insert of the desk calendar, the quarter's last day circled, held long enough to read. */
export const CalendarInsert: React.FC<{drawAt?: number}> = ({drawAt = 6}) => {
  const f = useCurrentFrame();
  const [month, day] = SAGA.quarterEnded.split(' ');
  const target = Number(day);
  const circle = interpolate(f, [drawAt, drawAt + 10], [0, 1], {...clamp, easing: Easing.out(Easing.quad)});
  const days = Array.from({length: 31}, (_, i) => i + 1);
  const offset = 4; // Oct 1, 2026 is a Thursday
  const cell = 74;
  const col = (target - 1 + offset) % 7, row = Math.floor((target - 1 + offset) / 7);
  return (
    <AbsoluteFill style={{background: 'linear-gradient(180deg, #70777b, #4b5155)'}}>
      <div style={{position: 'absolute', left: '50%', top: 34, transform: 'translateX(-50%) rotate(-1.5deg)', width: cell * 7 + 56, height: 736, background: T.paper, color: T.paperInk,
        boxShadow: '0 22px 50px rgba(0,0,0,0.5)', fontFamily: UI, padding: '24px 28px', boxSizing: 'border-box'}}>
        <div style={{fontSize: 92, fontWeight: 800, letterSpacing: '0.03em', lineHeight: 1}}>{month}</div>
        <div style={{display: 'grid', gridTemplateColumns: `repeat(7, ${cell}px)`, marginTop: 20, fontSize: 21, fontWeight: 600, color: '#6c6c70'}}>
          {['S', 'M', 'T', 'W', 'T', 'F', 'S'].map((d, i) => <div key={i} style={{textAlign: 'center'}}>{d}</div>)}
        </div>
        <div style={{position: 'relative', display: 'grid', gridTemplateColumns: `repeat(7, ${cell}px)`, gridAutoRows: `${cell + 12}px`, marginTop: 12, fontSize: 36, fontWeight: 500}}>
          {Array.from({length: offset}, (_, i) => <div key={`e${i}`} />)}
          {days.map((d) => <div key={d} style={{display: 'flex', alignItems: 'center', justifyContent: 'center', fontWeight: d === target ? 800 : 500}}>{d}</div>)}
          <svg width={cell} height={cell + 12} viewBox="0 0 74 86" style={{position: 'absolute', left: col * cell, top: row * (cell + 12), overflow: 'visible'}}>
            <path d="M38 8 C14 7 3 26 5 45 C7 68 25 80 43 77 C63 74 72 54 69 35 C66 17 50 6 28 11" fill="none" stroke={T.alert} strokeWidth={5.5} strokeLinecap="round" pathLength={1}
              strokeDasharray={1} strokeDashoffset={1 - circle} />
          </svg>
        </div>
      </div>
    </AbsoluteFill>
  );
};

/** E24: the two counters on the last line. */
export const DayCounters: React.FC<{at?: number; second?: number}> = ({at = 0, second = 18}) => {
  const f = useCurrentFrame();
  const you = Math.round(interpolate(f, [at, at + 14], [0, SAGA.dayCount], clamp));
  const plaque = Math.round(interpolate(f, [second, second + 8], [0, 2], clamp));
  const Row: React.FC<{k: string; v: number; show: boolean}> = ({k, v, show}) => (
    <div style={{opacity: show ? 1 : 0, display: 'flex', justifyContent: 'space-between', gap: 46, fontVariantNumeric: 'tabular-nums'}}>
      <span style={{fontWeight: 500, letterSpacing: '0.08em'}}>{k}:</span>
      <span style={{fontWeight: 700}}>{v} DAYS</span>
    </div>
  );
  return (
    <div style={{position: 'absolute', right: 96, bottom: 60, width: 500, fontFamily: UI, fontSize: 46, color: T.white, display: 'flex', flexDirection: 'column', gap: 8,
      textShadow: '0 2px 0 rgba(20,10,4,0.5), 0 0 20px rgba(20,10,4,0.7)'}}>
      <Row k="YOU" v={you} show={f >= at} />
      <Row k="PLAQUE" v={plaque} show={f >= second} />
    </div>
  );
};

import React from 'react';
import {AbsoluteFill, Easing, interpolate, useCurrentFrame} from 'remotion';
import edit from '../../../config/edit.json';
import term from '../../public/gen/captures/terminal.json';
import {MONO} from '../Fonts';

/**
 * E01t (human note, 2026-11-24): the opening's complicity beat. A plain terminal: nvidia-smi as captured while the GPU
 * ran a stage of this video at full load (scripts/e01_terminal.py), then scripts/effective-immediately, whose output and
 * pauses are its real ones. The video cuts in at the end of "generating...". No commentary; a slow push toward the GPU's row.
 */
const CMD1 = 'nvidia-smi';
const CMD2 = term.script;
const FONT = 23, LINE = 1.3;

// Frames within the shot: typing, the output, the script's lines 0.5 s apart, then the dots 0.33 s apart.
export const TERMINAL = {type1: 4, out1: 26, type2: 80, enter2: 112, lines: [116, 128, 140, 152], dots: [160, 168, 176], end: edit.terminal_frames};

const typed = (text: string, f: number, from: number, perChar: number) => text.slice(0, Math.max(0, Math.min(text.length, Math.floor((f - from) / perChar))));

export const Terminal: React.FC = () => {
  const f = useCurrentFrame();
  const T = TERMINAL;
  const smi = (term.smi as string[]).slice();
  while (smi.length && !smi[smi.length - 1].trim()) smi.pop();
  const cursor = Math.floor(f / 12) % 2 === 0;
  const rows: React.ReactNode[] = [];
  const prompt = (cmd: string, live: boolean, key: string) => (
    <div key={key}><span style={{color: '#7d8a93'}}>$ </span>{cmd}{live && <span style={{background: cursor ? '#d9e2e7' : 'transparent', color: '#0b0d0f'}}>&nbsp;</span>}</div>
  );
  rows.push(prompt(typed(CMD1, f, T.type1, 1.6), f < T.out1, 'p1'));
  if (f >= T.out1) {
    smi.forEach((l, i) => rows.push(<div key={`s${i}`} style={{whiteSpace: 'pre'}}>{l || ' '}</div>));
    const second = f >= T.type2 ? typed(CMD2, f, T.type2, (T.enter2 - 2 - T.type2) / CMD2.length) : '';
    rows.push(prompt(second, f < T.enter2, 'p2'));
  }
  const out = term.script_out as string[];
  out.slice(0, 3).forEach((l, i) => {
    if (f >= T.lines[i]) rows.push(<div key={`o${i}`} style={{fontWeight: i === 0 ? 700 : 400}}>{l}</div>);
  });
  if (f >= T.lines[3]) {
    const dots = T.dots.filter((d) => f >= d).length;
    rows.push(<div key="gen">generating{'.'.repeat(dots)}{f < T.end && <span style={{background: cursor ? '#d9e2e7' : 'transparent'}}>&nbsp;</span>}</div>);
  }
  // A slow push toward the GPU's row (the 11th line of the table) while the output holds.
  const push = interpolate(f, [T.out1, T.type2 + 10], [1, 1.07], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp', easing: Easing.inOut(Easing.quad)});
  return (
    <AbsoluteFill style={{background: '#0b0d0f'}}>
      <div style={{position: 'absolute', left: 0, right: 0, top: 70, display: 'flex', justifyContent: 'center', transform: `scale(${push})`, transformOrigin: '50% 40%'}}>
        <div style={{fontFamily: MONO, fontSize: FONT, lineHeight: LINE, color: '#d9e2e7', whiteSpace: 'pre', width: Math.ceil(89 * FONT * 0.6) + 4}}>
          {rows}
        </div>
      </div>
    </AbsoluteFill>
  );
};

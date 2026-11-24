import React from 'react';
import {AbsoluteFill, Img, interpolate, OffthreadVideo, Series, staticFile, useCurrentFrame} from 'remotion';
import g10Clip from '../public/gen/track/G10_clip.json';
import g10Still from '../public/gen/track/G10_still.json';
import {DatedCards, DisclosureCard, EndCard, FactCard, FinalCard, RealScreenshot} from './components/Cards';
import {LowerThird, TagStack} from './components/Common';
import {CalendarInsert, Confetti, DayCounters, Scoreboard} from './components/Data';
import {FilingPhone, FourPhones, LockScreen, MessagePhone} from './components/Phones';
import {DisplayText, JacketWall, Plate} from './components/Plates';
import {DeskSign, GlassSign, Plaque} from './components/Signs';
import {Grade, H, PIC_H, PIC_W, SAGA, SEED, W} from './config';
import {LABEL} from './Fonts';
import {LookLayer} from './look/LookLayer';
import {smooth} from './look/rand';

/**
 * M3's first-pass reel: every shot, E01 to E25, in order, at placeholder lengths and silent. It shows the pictures, the
 * look and the overlays together. It is not an edit: nothing here is cut to the song until the timing map exists.
 */

const clampX = {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'} as const;
const P = (id: string) => `gen/plates/${id}.png`;
const Clip: React.FC<{id: string}> = ({id}) => (
  <OffthreadVideo src={staticFile(`gen/clips/${id}.mp4`)} muted style={{width: PIC_W, height: PIC_H, objectFit: 'cover'}} />
);
const Board: React.FC<{shot: string}> = ({shot}) => (
  <OffthreadVideo src={staticFile(`gen/boardroom/${shot}.mp4`)} muted style={{width: PIC_W, height: PIC_H, objectFit: 'cover'}} />
);

/** E06: camera flashes from off-frame, bleaching the picture. On placeholder frames until the beats exist. */
const Flashes: React.FC<{at: number[]}> = ({at}) => {
  const f = useCurrentFrame();
  const o = Math.max(0, ...at.map((a) => (f >= a ? 1 - (f - a) / 5 : 0)));
  return <AbsoluteFill style={{background: '#fff', opacity: o * 0.92}} />;
};

const Pulse: React.FC = () => {
  const f = useCurrentFrame();
  return <Scoreboard pulse={Math.max(0, Math.cos((f / 12.63) * 2 * Math.PI)) ** 3} x="76%" y="42%" />;
};

const TAGS = [
  {text: SAGA.officialsTag, at: 4},
  {text: 'Investigation: continuing (Nvidia, Nov 23)', at: 22},
  {text: 'House interviews: Dec 1–2', at: 40},
  {text: 'The White House took credit on TV the same day (see fact card)', at: 58},
];

/** E21: the caller ID, pinned to the display's tracked corners on every frame of the clip. */
const TrackedDisplay: React.FC = () => {
  const f = useCurrentFrame();
  return <DisplayText quad={g10Clip.quads[Math.min(f, g10Clip.quads.length - 1)]} />;
};

/** E24: the plaque stays on the wall through G11's push (measured: 1.18x over 96 frames about this point). */
const BoothPlaque: React.FC<{off?: [number, number]; push?: boolean}> = ({off, push = true}) => {
  const f = useCurrentFrame();
  const k = push ? 1 + (0.1822 * Math.min(f, 96)) / 96 : 1.1822;
  const gone = off && f >= off[0] && f < off[1];
  return (
    <AbsoluteFill style={{transform: `scale(${k})`, transformOrigin: '956px 315px'}}>
      {gone
        ? <div style={{position: 'absolute', left: 810, top: 74, width: 300, height: 168, background: 'rgba(255,238,205,0.2)'}} />
        : <Plaque x={810} y={74} width={300} src="gen/plaque.png" />}
    </AbsoluteFill>
  );
};

/** G12's fallback (decisions 12): G11's last frame held locked off, with the warm light flickering on it. */
const BoothHold: React.FC = () => {
  const f = useCurrentFrame();
  return (
    <AbsoluteFill style={{filter: `brightness(${1 + smooth(SEED, 90, f, 5) * 0.022 + smooth(SEED, 91, f, 17) * 0.018})`}}>
      <Plate src={P('G11_last')} />
    </AbsoluteFill>
  );
};

const Dissolve: React.FC<{from: React.ReactNode; to: React.ReactNode; at: number; len: number}> = ({from, to, at, len}) => {
  const o = interpolate(useCurrentFrame(), [at, at + len], [0, 1], clampX);
  return <AbsoluteFill>{from}<AbsoluteFill style={{opacity: o}}>{to}</AbsoluteFill></AbsoluteFill>;
};

type Shot = {id: string; frames: number; grade?: Grade; handheld?: boolean; el: React.ReactNode; after?: React.ReactNode};

export const SHOTS: Shot[] = [
  {id: 'E01', frames: 42, el: <RealScreenshot stamp="Nov 12, 2026" />},
  {id: 'E02', frames: 96, grade: 'cold', el: <Clip id="G01" />},
  {id: 'E03', frames: 60, grade: 'cold', handheld: true, el: <FilingPhone />},
  {id: 'E04', frames: 60, grade: 'cold', handheld: true, el: <JacketWall mode="hung" at={9999} />},
  {id: 'E05', frames: 46, grade: 'cold', handheld: true, el: <JacketWall mode="lift" at={10} />},
  {id: 'E06', frames: 72, grade: 'cold', el: <><Clip id="G02" /><Flashes at={[14, 26, 50]} /><LowerThird title="The Company" sub="Statement" at={6} /></>},
  {id: 'E07', frames: 60, grade: 'cold', handheld: true, el: <FourPhones />},
  {id: 'E08', frames: 96, grade: 'cold', handheld: true, el: <Board shot="E08" />},
  {id: 'E09', frames: 96, grade: 'cold', el: <><Board shot="E09" /><LowerThird title="Effective immediately" at={6} /></>},
  {id: 'E10', frames: 96, grade: 'cold', el: <Clip id="G03" />},
  {id: 'E11', frames: 72, grade: 'cold', handheld: true, el: <><Board shot="E11" /><Confetti startFrame={24} /></>},
  {id: 'E12', frames: 96, grade: 'cold', el: <Clip id="G04" />},
  {id: 'E13', frames: 54, grade: 'cold', handheld: true, el: <><Plate src={P('G04')} /><Pulse /></>},
  {id: 'E14', frames: 72, grade: 'cold', el: <Clip id="G05" />},
  {id: 'E15', frames: 48, grade: 'cold', el: <Clip id="G06" />},
  {id: 'E15 insert', frames: 44, grade: 'cold', handheld: true, el: <CalendarInsert />},
  {id: 'E16', frames: 96, grade: 'cyan', el: <Clip id="G07" />},
  {id: 'E17', frames: 84, grade: 'cyan', el: <Clip id="G08" />},
  {id: 'E17 insert', frames: 13, grade: 'cold', el: <Board shot="E17i" />},
  {id: 'E18', frames: 72, grade: 'cyan', el: <Clip id="G09" />},
  {id: 'E18 phone', frames: 46, grade: 'cyan', handheld: true, el: <MessagePhone />},
  {id: 'E19', frames: 60, grade: 'cyan', handheld: true, el: <LockScreen />},
  {id: 'E20', frames: 40, grade: 'cyan', handheld: true, el: <><Plate src={P('G10')} /><DisplayText quad={g10Still.quads[0]} /></>},
  {id: 'E21', frames: 72, grade: 'cyan', el: <><Clip id="G10" /><TrackedDisplay /><TagStack tags={TAGS} left={70} top={46} width={640} /></>},
  {id: 'E22', frames: 46, grade: 'warm', handheld: true, el: <JacketWall mode="return" at={8} />},
  {id: 'E22 screen', frames: 48, grade: 'warm', el: <Board shot="E22s" />},
  {id: 'E22 vote', frames: 120, grade: 'warm', handheld: true, el: <Board shot="E22" />,
    after: <Img src={staticFile('gen/boardroom/E22_probe.png')} style={{position: 'absolute', inset: 0, width: PIC_W, height: PIC_H}} />},
  {id: 'E23', frames: 78, grade: 'warm', handheld: true, el: <><Plate src={P('S02')} /><DeskSign x={700} y={470} scale={1.5} /><GlassSign x={1120} y={70} width={640} /></>},
  {id: 'E24 cut', frames: 10, el: <AbsoluteFill style={{background: '#000'}} />},
  {id: 'E24', frames: 96, grade: 'warm', el: <><Clip id="G11" /><BoothPlaque off={[34, 66]} /></>},
  {id: 'E24 counters', frames: 96, grade: 'warm', el: (
    <Dissolve at={66} len={26}
      from={<><BoothHold /><BoothPlaque push={false} /><DayCounters at={6} second={24} /></>}
      to={<Plate src={P('S03')} />} />
  )},
  {id: 'E25', frames: 42, el: <RealScreenshot stamp="Nov 23, 2026" />},
  {id: 'Fact card 1', frames: 72, el: <FactCard page={0} />},
  {id: 'Fact card 2', frames: 72, el: <FactCard page={1} />},
  {id: 'Fact card 3', frames: 48, el: <FactCard page={2} />},
  {id: 'Disclosure', frames: 96, el: <DisclosureCard />},
  {id: 'End card', frames: 72, el: <EndCard />},
  {id: 'Dated cards', frames: 112, el: <DatedCards />},
  {id: 'Final card', frames: 48, el: <FinalCard />},
];

export const REEL_FRAMES = SHOTS.reduce((n, s) => n + s.frames, 0);

const Slate: React.FC<{id: string}> = ({id}) => (
  <div style={{position: 'absolute', left: 24, top: 18, fontFamily: LABEL, fontSize: 30, letterSpacing: '0.08em', color: 'rgba(255,255,255,0.72)',
    textShadow: '0 0 6px #000'}}>
    {id} <span style={{opacity: 0.6, fontSize: 22}}>· first pass, timing not final, silent</span>
  </div>
);

export const Reel: React.FC = () => (
  <AbsoluteFill style={{background: '#000', width: W, height: H}}>
    <Series>
      {SHOTS.map((s) => (
        <Series.Sequence key={s.id} durationInFrames={s.frames}>
          {s.grade ? <LookLayer grade={s.grade} handheld={s.handheld} afterGrade={s.after}>{s.el}</LookLayer> : s.el}
          <Slate id={s.id} />
        </Series.Sequence>
      ))}
    </Series>
  </AbsoluteFill>
);

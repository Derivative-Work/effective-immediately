import React from 'react';
import {AbsoluteFill, Audio, Easing, Img, interpolate, OffthreadVideo, Sequence, staticFile, useCurrentFrame} from 'remotion';
import g10Clip from '../public/gen/track/G10_clip.json';
import g10Still from '../public/gen/track/G10_still.json';
import bass from '../public/gen/timing/bass.json';
import cut from '../public/gen/timing/cut.json';
import cards from '../../config/cards.json';
import {DatedCards, DisclosureCard, FactCard, FinalCard, RealScreenshot} from './components/Cards';
import {LowerThird, TagStack, WithPlaceholders} from './components/Common';
import {CalendarInsert, Confetti, DayCounters, MarketChart, Scoreboard} from './components/Data';
import {FilingPhone, FourPhones, LockScreen, MessagePhone} from './components/Phones';
import {DisplayText, JacketWall, Plate} from './components/Plates';
import {Subtitles, SubStyle} from './components/Subtitles';
import {Terminal} from './components/Terminal';
import {DeskSign, GlassSign, Plaque} from './components/Signs';
import {Grade, H, PIC_H, PIC_W, SAGA, SEED, W} from './config';
import {LABEL, UI} from './Fonts';
import {LookLayer} from './look/LookLayer';
import {pinMatrix, Quad} from './look/pin';
import {smooth} from './look/rand';

/**
 * M4: every shot cut to the song (scripts/cut_list.py). The audio is the working edit until the human's locked master
 * replaces it; shots after the cut move by the one offset in config/audio.json.
 */

type Seg = {src: string; from: number; frames: number; rate: number; trim?: number};
type Insert = {from: number; boardFrom: number; frames: number};
export type CutShot = {
  id: string; from: number; frames: number; segs?: Seg[]; lower?: boolean; at?: number; flashes?: number[]; drawAt?: number; textAt?: number;
  interval?: number; tags?: number[]; board?: string; boardFrom?: number; drop?: number; inserts?: Insert[]; off?: number; on?: number;
  counter?: number; counter2?: number; dissolveAt?: number; dissolveLen?: number; clipRate?: number;
  grade?: Grade; screen?: 'drop' | 'recover'; quad?: Quad; probe?: string; displayFrames?: number; creditsAt?: number; creditStep?: number;
  fadeOut?: number;
};

const clampX = {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'} as const;
const fill = {width: PIC_W, height: PIC_H, objectFit: 'cover'} as const;
const P = (id: string) => `gen/plates/${id}.png`;

const Takes: React.FC<{segs: Seg[]}> = ({segs}) => (
  <>
    {segs.map((s) => (
      <Sequence key={`${s.src}-${s.from}`} from={s.from} durationInFrames={s.frames} layout="none">
        <AbsoluteFill><OffthreadVideo src={staticFile(s.src)} muted playbackRate={s.rate} trimBefore={s.trim || undefined} style={fill} /></AbsoluteFill>
      </Sequence>
    ))}
  </>
);

const Board: React.FC<{shot: string; from?: number}> = ({shot, from = 0}) => (
  <OffthreadVideo src={staticFile(`gen/boardroom/${shot}.mp4`)} muted trimBefore={from || undefined} style={fill} />
);

/**
 * The market chart, on the boardroom screen's corners, so its candles can grow in shot. It covers the screen from the shot's
 * first frame (human note: the baked texture showed through for a frame or two) and starts growing at `from`.
 */
const ScreenLine: React.FC<{mode: 'drop' | 'recover'; from: number; duration: number; quad: Quad}> = ({mode, from, duration, quad}) => (
  <div style={{position: 'absolute', left: 0, top: 0, width: 1920, height: 804, transformOrigin: '0 0', transform: pinMatrix(1920, 804, quad), overflow: 'hidden'}}>
    <AbsoluteFill style={{width: 1920, height: 804}}><MarketChart mode={mode} durationFrames={duration} startAt={from} /></AbsoluteFill>
  </div>
);

const Flashes: React.FC<{at: number[]}> = ({at}) => {
  const f = useCurrentFrame();
  const o = Math.max(0, ...at.map((a) => (f >= a ? 1 - (f - a) / 5 : 0)));
  return <AbsoluteFill style={{background: '#fff', opacity: o * 0.92}} />;
};

const Pulse: React.FC<{start: number}> = ({start}) => {
  const f = useCurrentFrame();
  return <Scoreboard pulse={(bass as number[])[start + f] ?? 0} x="76%" y="42%" />;
};

const TrackedDisplay: React.FC = () => {
  const f = useCurrentFrame();
  return <DisplayText quad={g10Clip.quads[Math.min(f, g10Clip.quads.length - 1)]} />;
};

/** E21: the caller ID, only while G10's display is on screen. */
const CallerOverlay: React.FC<{until: number}> = ({until}) => (useCurrentFrame() < until ? <TrackedDisplay /> : null);

/** E23's desk sign, pinned to the blank sign in G33 (measured corners, in picture pixels). */
const SIGN_QUAD: Quad = [[1210, 398.25], [1408.75, 402], [1407.5, 524.5], [1207.5, 515.75]];
const SignShot: React.FC = () => {
  const [title, status] = SAGA.governanceSigns[0].split(' · ');
  const k = 1 + (0.006 * useCurrentFrame()) / 24;
  return (
    <AbsoluteFill style={{transform: `scale(${k})`, transformOrigin: '1308px 460px'}}>
      <Img src={staticFile(P('G33'))} style={fill} />
      <div style={{position: 'absolute', left: 0, top: 0, width: 520, height: 320, transformOrigin: '0 0', transform: pinMatrix(520, 320, SIGN_QUAD), mixBlendMode: 'multiply',
        display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', textAlign: 'center', padding: '0 28px', boxSizing: 'border-box', color: '#2a1d10', fontFamily: UI}}>
        <div style={{fontSize: 70, fontWeight: 800, lineHeight: 1.04}}>{title}</div>
        <div style={{fontSize: 44, fontStyle: 'italic', fontWeight: 500, marginTop: 16}}>{status}</div>
      </div>
    </AbsoluteFill>
  );
};

/** The credits, over the held booth and the band's last section, one line every few beats; on the right, clear of the jacket. */
const Credits: React.FC<{at: number; step: number}> = ({at, step}) => {
  const f = useCurrentFrame();
  const [title, ...rest] = cards.end_card.split('. ');
  const scrim = interpolate(f, [at - 10, at + 14], [0, 1], clampX);
  return (
    <AbsoluteFill>
      <AbsoluteFill style={{opacity: scrim, background: 'linear-gradient(270deg, rgba(12,7,3,0.86), rgba(12,7,3,0.74) 36%, rgba(12,7,3,0) 56%)'}} />
      <div style={{position: 'absolute', right: 84, top: 0, bottom: 0, width: 720, display: 'flex', flexDirection: 'column', justifyContent: 'center', gap: 12, color: '#fff6e6', fontFamily: UI}}>
        <div style={{fontSize: 62, fontWeight: 700, letterSpacing: '-0.01em', marginBottom: 14, opacity: interpolate(f, [at, at + 8], [0, 1], clampX)}}>{title}</div>
        {rest.map((l, i) => (
          <div key={l} style={{fontSize: 30, lineHeight: 1.26, opacity: interpolate(f, [at + (i + 1) * step, at + (i + 1) * step + 7], [0, 1], clampX)}}>
            <WithPlaceholders text={l.replace(/\.$/, '')} />
          </div>
        ))}
      </div>
    </AbsoluteFill>
  );
};

/** G11's camera push, measured: 1.18x over its 96 frames, about this point. */
const PUSH = 0.1822, PUSH_FRAMES = 96;
const pushAt = (clipFrame: number) => 1 + (PUSH * Math.min(clipFrame, PUSH_FRAMES)) / PUSH_FRAMES;
const PLAQUE = {x: 810, y: 74, w: 300, h: 168};
const BOOTH_TOP = 262;   // the top of the seat back, where the falling plaque goes out of sight

/**
 * E24: the plaque comes down on the line that says so and goes back up on the next. A corner lets go, it swings on the
 * other screw, slips behind the booth; then it rises from there, tips level and settles against the wall.
 */
const FALL = 34, RISE = 40;
const plaquePose = (f: number, off: number, on: number) => {
  if (f < off) return {rot: 0, dy: 0, gone: false};
  if (f < on) {
    const t = f - off;
    const wobble = t < 7 ? Math.sin((t / 7) * Math.PI * 2) * 1.1 * (1 - t / 7) : 0;
    const swing = interpolate(t, [5, 19, 24, 28], [0, 25, 21, 23], {...clampX, easing: Easing.inOut(Easing.quad)});
    const drop = interpolate(t, [20, FALL], [0, 300], {...clampX, easing: Easing.in(Easing.quad)});
    return {rot: wobble + swing, dy: drop, gone: t >= FALL};
  }
  const t = f - on;
  const dy = interpolate(t, [0, 22], [300, 0], {...clampX, easing: Easing.out(Easing.cubic)});
  const rot = interpolate(t, [0, 16, 26, 32, RISE], [17, 13, -1.3, 0.6, 0], {...clampX, easing: Easing.inOut(Easing.quad)});
  return {rot, dy, gone: false};
};

const BoothPlaque: React.FC<{off: number; on: number; rate: number; hold?: boolean}> = ({off, on, rate, hold}) => {
  const f = useCurrentFrame();
  const k = hold ? 1 + PUSH : pushAt(f * rate);
  const {rot, dy, gone} = plaquePose(f, off, on);
  const showPale = f >= off;
  const shadow = 1 - Math.min(1, dy / 40);
  return (
    <AbsoluteFill style={{transform: `scale(${k})`, transformOrigin: '956px 315px'}}>
      {showPale && <div style={{position: 'absolute', left: PLAQUE.x, top: PLAQUE.y, width: PLAQUE.w, height: PLAQUE.h, background: 'rgba(255,238,205,0.2)'}} />}
      {!gone && (
        <div style={{position: 'absolute', left: 0, top: 0, width: PIC_W, height: BOOTH_TOP, overflow: 'hidden'}}>
          <div style={{position: 'absolute', left: 0, top: 0, width: PIC_W, height: PIC_H, transformOrigin: `${PLAQUE.x + 18}px ${PLAQUE.y + 16}px`,
            transform: `translateY(${dy}px) rotate(${rot}deg)`, filter: `drop-shadow(0 ${5 * shadow}px ${9 * shadow}px rgba(20,8,0,${0.45 * shadow}))`}}>
            <Plaque x={PLAQUE.x} y={PLAQUE.y} width={PLAQUE.w} src="gen/plaque.png" />
          </div>
        </div>
      )}
    </AbsoluteFill>
  );
};

const BoothHold: React.FC = () => {
  const f = useCurrentFrame();
  return (
    <AbsoluteFill style={{filter: `brightness(${1 + smooth(SEED, 90, f, 5) * 0.022 + smooth(SEED, 91, f, 17) * 0.018})`}}>
      <Plate src={P('G11_last')} />
    </AbsoluteFill>
  );
};

/** The whole outro in one shot: the push, the hold, the plaque's two moves, the counters, the dissolve to the jacket. */
const Outro: React.FC<{s: CutShot}> = ({s}) => {
  const f = useCurrentFrame();
  const rate = s.clipRate ?? 0.55;
  const clipEnd = Math.floor(PUSH_FRAMES / rate);
  const o = interpolate(f, [s.dissolveAt!, s.dissolveAt! + s.dissolveLen!], [0, 1], {...clampX, easing: Easing.inOut(Easing.quad)});
  return (
    <AbsoluteFill>
      {f < clipEnd
        ? <OffthreadVideo src={staticFile('gen/clips/G11.mp4')} muted playbackRate={rate} style={fill} />
        : <BoothHold />}
      <BoothPlaque off={s.off!} on={s.on!} rate={rate} hold={f >= clipEnd} />
      <AbsoluteFill style={{opacity: 1 - o}}><DayCounters at={s.counter!} second={s.counter2!} /></AbsoluteFill>
      {o > 0 && <AbsoluteFill style={{opacity: o}}><Plate src={P('S03')} /></AbsoluteFill>}
      <Credits at={s.creditsAt!} step={s.creditStep!} />
    </AbsoluteFill>
  );
};

const E21Tags: React.FC<{at: number[]}> = ({at}) => (
  <TagStack left={70} top={46} width={640} tags={[
    {text: SAGA.officialsTag, at: at[0]},
    {text: 'Investigation: continuing (Nvidia, Nov 23)', at: at[1]},
    {text: 'House interviews: Dec 1–2', at: at[2]},
    {text: 'The White House took credit on TV the same day (see fact card)', at: at[3]},
  ]} />
);

const WithInserts: React.FC<{s: CutShot}> = ({s}) => (
  <>
    {(s.inserts ?? []).map((x) => (
      <Sequence key={x.from} from={x.from} durationInFrames={x.frames} layout="none">
        <AbsoluteFill><LookLayer grade="cold"><Board shot="E17i" from={x.boardFrom} /></LookLayer></AbsoluteFill>
      </Sequence>
    ))}
  </>
);

const STEADY = new Set(['E09', 'E09 top', 'E22 top']);

const render = (s: CutShot): {grade?: Grade; handheld?: boolean; el: React.ReactNode; after?: React.ReactNode; over?: React.ReactNode} => {
  const g = s.grade;
  if (s.board) {
    const after = s.probe ? <Img src={staticFile(`gen/boardroom/${s.probe}_probe.png`)} style={{position: 'absolute', inset: 0, width: PIC_W, height: PIC_H}} /> : undefined;
    return {grade: g, handheld: !STEADY.has(s.id), after, el: (
      <>
        <Board shot={s.board} from={s.boardFrom} />
        {s.screen && <ScreenLine quad={s.quad!} mode={s.screen} from={s.drop!} duration={s.screen === 'drop' ? 40 : Math.min(36, s.frames - 20)} />}
        {s.screen === 'drop' && <Confetti startFrame={s.drop! + 12} />}
        {s.lower && <LowerThird title="Effective immediately" at={6} />}
      </>
    )};
  }
  switch (s.id) {
    case 'E01': return {el: <RealScreenshot src="gen/captures/E01_release.png" stamp="Nov 12, 2026" />};
    case 'E01t': return {el: <Terminal />};
    case 'E03': return {grade: g, handheld: true, el: <FilingPhone at={s.at} />};
    case 'E04': return {grade: g, handheld: true, el: <JacketWall mode="hung" at={9999} />};
    case 'E05': return {grade: g, handheld: true, el: <JacketWall mode="lift" at={s.at} />};
    case 'E06': return {grade: g, el: <><Takes segs={s.segs!} /><Flashes at={s.flashes!} /><LowerThird title="The Company" sub="Statement" at={6} /></>};
    case 'E07': return {grade: g, handheld: true, el: <FourPhones />};
    case 'E13': return {grade: g, el: <><Takes segs={s.segs!} /><Pulse start={s.from} /></>};
    case 'E15i': return {grade: g, handheld: true, el: <CalendarInsert drawAt={s.drawAt} />};
    case 'E18p': return {grade: g, handheld: true, el: <MessagePhone at={s.at} textAt={s.textAt} />};
    case 'E19': return {grade: g, handheld: true, el: <LockScreen interval={s.interval} />};
    case 'E20': return {grade: g, handheld: true, el: <><Plate src={P('G10')} /><DisplayText quad={g10Still.quads[0]} /></>};
    case 'E21': return {grade: g, el: <><Takes segs={s.segs!} /><CallerOverlay until={s.displayFrames!} /><E21Tags at={s.tags!} /></>};
    case 'E22': return {grade: g, handheld: true, el: <JacketWall mode="return" at={s.at} />};
    case 'E23 sign': return {grade: g, handheld: true, el: <SignShot />};
    case 'E23 wide': return {grade: g, handheld: true, el: <><Plate src={P('S02')} /><DeskSign x={700} y={470} scale={1.5} /><GlassSign x={1120} y={70} width={640} /></>};
    case 'black': return {el: <AbsoluteFill style={{background: '#000'}} />};
    case 'E24': return {grade: g, el: <Outro s={s} />};
    case 'E25': return {el: <RealScreenshot src="gen/captures/E25_release.png" stamp="Nov 23, 2026" />};
    case 'Fact card 1': return {el: <FactCard page={0} />};
    case 'Fact card 2': return {el: <FactCard page={1} />};
    case 'Fact card 3': return {el: <FactCard page={2} />};
    case 'Disclosure': return {el: <DisclosureCard />};
    case 'Dated cards': return {el: <DatedCards interval={s.interval} />};
    case 'Final card': return {el: <FinalCard />};
    case 'E02': return {grade: g, el: <OpeningReframe segs={s.segs!}><Takes segs={s.segs!} /></OpeningReframe>};
    default: return {grade: g, el: <Takes segs={s.segs!} />, over: <WithInserts s={s} />};
  }
};

/**
 * E01 and E01t, as a panel on the left over the intro (human note on the eighth cut: the music took too long to start;
 * after Distillation (Allegedly)'s merged D01/D02). The song starts on frame 0 and its footage plays on the right; the real
 * Nov 12 screenshot, then the terminal, sit in the panel, which slides away as the script's dots finish.
 */
const PANEL_W = 1100;
const Opening: React.FC = () => {
  const f = useCurrentFrame();
  const {screenshot, terminal, exit} = cut.opening;
  const end = screenshot + terminal;
  const x = interpolate(f, [end, end + exit], [0, -PANEL_W - 40], {...clampX, easing: Easing.in(Easing.cubic)});
  return (
    <div style={{position: 'absolute', left: 0, top: 0, width: PANEL_W, height: H, transform: `translateX(${x}px)`, background: '#0b0d0f', overflow: 'hidden',
      boxShadow: '10px 0 40px rgba(0,0,0,0.65)', borderRight: '6px solid #1a1e22'}}>
      <Sequence durationInFrames={screenshot} layout="none">
        <RealScreenshot src="gen/captures/E01_release.png" stamp="Nov 12, 2026" maxW={1000} maxH={560} />
      </Sequence>
      <Sequence from={screenshot} layout="none">
        <Terminal font={19} top={120} />
      </Sequence>
    </div>
  );
};

/**
 * E02 during the opening: its footage sits in the space right of the panel (human note: the framing under the panel was
 * off), cropped at full scale, not shrunk, around each clip's subject, as Distillation (Allegedly) placed its D02 beside its
 * panel. Subject positions, as a share of the picture's width at the clip's first and last frames, were measured from the
 * takes: G14's walker drifts left (0.50 to 0.31), G13's feet sit near 0.58, G01's walker moves right (0.42 to 0.60). As the
 * panel slides away, the box widens with it back to the full frame.
 */
const OPEN_FOCUS: [number, number][] = [[0.5, 0.31], [0.58, 0.58], [0.42, 0.6]];
const OpeningReframe: React.FC<{segs: Seg[]; children: React.ReactNode}> = ({segs, children}) => {
  const f = useCurrentFrame();
  const {screenshot, terminal, exit} = cut.opening;
  const end = screenshot + terminal;
  if (f >= end + exit) return <>{children}</>;
  const panelX = interpolate(f, [end, end + exit], [0, -PANEL_W - 40], {...clampX, easing: Easing.in(Easing.cubic)});
  const left = Math.max(0, PANEL_W + 6 + panelX), w = PIC_W - left;
  const i = Math.max(0, segs.findIndex((sg) => f >= sg.from && f < sg.from + sg.frames));
  const [a0, a1] = OPEN_FOCUS[Math.min(i, OPEN_FOCUS.length - 1)];
  const focus = interpolate(f, [segs[i].from, segs[i].from + segs[i].frames - 1], [a0, a1], clampX);
  const shift = Math.min(0, Math.max(-(PIC_W - w), w / 2 - focus * PIC_W));
  return (
    <div style={{position: 'absolute', left, top: 0, width: w, height: PIC_H, overflow: 'hidden'}}>
      <div style={{position: 'absolute', left: shift, top: 0, width: PIC_W, height: PIC_H}}>{children}</div>
    </div>
  );
};

/** Fade to black from `at` to the end of the shot (the cut: the picture goes down with the master's reverb throw). */
const FadeOut: React.FC<{at: number; end: number}> = ({at, end}) => {
  const o = interpolate(useCurrentFrame(), [at, end], [0, 1], {...clampX, easing: Easing.in(Easing.quad)});
  return <AbsoluteFill style={{background: '#000', opacity: o}} />;
};

const Slate: React.FC<{id: string}> = ({id}) => (
  <div style={{position: 'absolute', left: 24, top: 18, fontFamily: LABEL, fontSize: 30, letterSpacing: '0.08em', color: 'rgba(255,255,255,0.72)', textShadow: '0 0 6px #000'}}>
    {id} <span style={{opacity: 0.6, fontSize: 22}}>· animatic</span>
  </div>
);

export const ANIMATIC_FRAMES = cut.frames;

/** `slate`: the animatic's shot labels; the final render turns them off. */
export const Animatic: React.FC<{subStyle?: SubStyle | 'none'; label?: string; slate?: boolean}> = ({subStyle = 'set', label, slate = true}) => (
  <AbsoluteFill style={{background: '#000', width: W, height: H}}>
    <Sequence from={cut.musicFrom} layout="none"><Audio src={staticFile('gen/audio/working.wav')} /></Sequence>
    <Sequence from={cut.creditsFrom} layout="none"><Audio src={staticFile('gen/audio/credits.wav')} /></Sequence>
    {(cut.shots as CutShot[]).map((s) => {
      const r = render(s);
      return (
        <Sequence key={s.id} from={s.from} durationInFrames={s.frames}>
          {r.grade ? <LookLayer grade={r.grade} handheld={r.handheld} afterGrade={r.after} frameOffset={s.from}>{r.el}</LookLayer> : r.el}
          {r.over}
          {s.fadeOut !== undefined && <FadeOut at={s.fadeOut} end={s.frames} />}
          {slate && <Slate id={s.id} />}
        </Sequence>
      );
    })}
    <Sequence durationInFrames={cut.opening.screenshot + cut.opening.terminal + cut.opening.exit} layout="none"><Opening /></Sequence>
    {subStyle !== 'none' && <Subtitles style={subStyle} />}
    {label && (
      <div style={{position: 'absolute', left: 0, right: 0, top: 0, height: (H - PIC_H) / 2, display: 'flex', alignItems: 'center', justifyContent: 'center',
        background: '#000', fontFamily: LABEL, fontSize: 42, letterSpacing: '0.06em', color: 'rgba(255,255,255,0.88)'}}>{label}</div>
    )}
  </AbsoluteFill>
);

import React from 'react';
import {AbsoluteFill, Img, interpolate, staticFile, useCurrentFrame} from 'remotion';
import handDay from '../../public/gen/track/hand_phone.json';
import handNight from '../../public/gen/track/hand_phone_night.json';
import {PIC_H, PIC_W, SAGA, SEED} from '../config';
import {UI} from '../Fonts';
import {pinMatrix, Quad} from '../look/pin';
import {hash} from '../look/rand';
import {T} from '../theme';
import {DarkRoom, TagStack} from './Common';

/*
 * Phone screens (human note on the sixth cut: too plain, and a blank white screen read as a compositing error). Every
 * screen now has a status bar and something on it from its first frame: a thread with a typing indicator, a lock screen
 * with its clock, a call screen. All of it is generic: no maker's shapes, icons or OS styling, no green, nothing warm.
 */

const clamp = {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'} as const;
const PHONE = SAGA.phone as {filingClock: string; filingStamp: string; nightDate: string; nightClock: string};

/** A generic handset: no maker's shape, status icons or OS styling. */
export const Handset: React.FC<{w: number; children: React.ReactNode; style?: React.CSSProperties}> = ({w, children, style}) => {
  const h = w * 2.05;
  return (
    <div style={{position: 'relative', width: w, height: h, borderRadius: w * 0.11, background: '#08090b', padding: w * 0.028,
      boxShadow: '0 0 0 2px #2f3338, 0 24px 60px rgba(0,0,0,0.6)', ...style}}>
      <div style={{position: 'relative', width: '100%', height: '100%', borderRadius: w * 0.09, overflow: 'hidden', background: T.panel, fontFamily: UI, color: T.white}}>
        {children}
      </div>
    </div>
  );
};

/** Time, signal and battery, drawn here (no maker's icons). `k` scales it from the 430 px held screen. */
const StatusBar: React.FC<{time?: string; ink: string; k?: number}> = ({time, ink, k = 1}) => (
  <div style={{position: 'absolute', left: 0, right: 0, top: 0, height: 64 * k, padding: `0 ${34 * k}px`, display: 'flex', alignItems: 'center',
    justifyContent: time ? 'space-between' : 'flex-end', color: ink, fontSize: 25 * k, fontWeight: 600, zIndex: 3}}>
    {time && <span style={{fontVariantNumeric: 'tabular-nums'}}>{time}</span>}
    <svg width={76 * k} height={22 * k} viewBox="0 0 76 22">
      {[0, 1, 2, 3].map((i) => <rect key={i} x={i * 7} y={16 - i * 4} width={5} height={6 + i * 4} rx={1.2} fill={ink} />)}
      <rect x={36} y={3} width={34} height={16} rx={4} fill="none" stroke={ink} strokeWidth={2} opacity={0.6} />
      <rect x={39} y={6} width={22} height={10} rx={2} fill={ink} />
      <rect x={71.5} y={8.5} width={2.5} height={5} rx={1} fill={ink} opacity={0.6} />
    </svg>
  </div>
);

const HomeBar: React.FC<{ink: string; k?: number}> = ({ink, k = 1}) => (
  <div style={{position: 'absolute', bottom: 14 * k, left: '50%', width: 140 * k, height: 5 * k, marginLeft: -70 * k, borderRadius: 3 * k, background: ink, opacity: 0.45, zIndex: 3}} />
);

/** A handset glyph drawn for this film (not an OS icon). */
const Handpiece: React.FC<{size: number; color: string; rot?: number}> = ({size, color, rot = 0}) => (
  <svg width={size} height={size} viewBox="0 0 24 24" style={{transform: `rotate(${rot}deg)`}}>
    <path fill={color} d="M3.5 13.6c0-1.1.7-2 1.8-2.3 4.4-1.4 9-1.4 13.4 0 1.1.3 1.8 1.2 1.8 2.3v1.8c0 .9-.8 1.6-1.7 1.5l-2.8-.4c-.8-.1-1.3-.8-1.3-1.5v-1.5c-2-.5-3.9-.5-5.8 0V15c0 .8-.6 1.4-1.3 1.5l-2.8.4c-.9.1-1.7-.6-1.7-1.5v-1.8z" />
  </svg>
);

/** A speech-bubble glyph for the message notification (drawn here). */
const ChatGlyph: React.FC<{size: number; color: string}> = ({size, color}) => (
  <svg width={size} height={size} viewBox="0 0 24 24">
    <path fill={color} d="M5 4h14a3 3 0 0 1 3 3v8a3 3 0 0 1-3 3h-7l-5 4v-4H5a3 3 0 0 1-3-3V7a3 3 0 0 1 3-3z" />
  </svg>
);

/** The glass: a faint diagonal sheen and darker edges, so the screen sits in the plate instead of on top of it. */
const Glass: React.FC = () => (
  <>
    <div style={{position: 'absolute', inset: 0, zIndex: 5, pointerEvents: 'none',
      background: 'linear-gradient(118deg, rgba(255,255,255,0.13) 0%, rgba(255,255,255,0.04) 30%, rgba(255,255,255,0) 46%, rgba(255,255,255,0) 72%, rgba(255,255,255,0.05) 100%)'}} />
    <div style={{position: 'absolute', inset: 0, zIndex: 5, pointerEvents: 'none', boxShadow: 'inset 0 0 26px rgba(0,0,0,0.24)'}} />
  </>
);

const SCREEN_W = 430;
const INK = '#12171b';

/**
 * E03, E18, E19: a generated hand holding a phone with a blank screen, the UI corner-pinned to that screen
 * (scripts/track_display.py). The UI covers the whole screen, so the plate's notch goes and the handset stays generic.
 * The plate is pushed in about the phone so the words read.
 */
const HeldPhone: React.FC<{plate: string; quad: Quad; background: React.ReactNode; lit?: number; children: React.ReactNode}> = ({plate, quad, background, lit = 1, children}) => {
  const side = (a: number[], b: number[]) => Math.hypot(a[0] - b[0], a[1] - b[1]);
  const h = Math.round(SCREEN_W * (side(quad[0], quad[3]) + side(quad[1], quad[2])) / (side(quad[0], quad[1]) + side(quad[3], quad[2])));
  const cx = quad.reduce((n, c) => n + c[0], 0) / 4, cy = quad.reduce((n, c) => n + c[1], 0) / 4;
  const zoom = 1.14;
  return (
    <AbsoluteFill style={{overflow: 'hidden', background: '#000'}}>
      <div style={{position: 'absolute', inset: 0, transformOrigin: '0 0',
        transform: `translate(${PIC_W / 2 - cx * zoom}px, ${PIC_H / 2 - cy * zoom}px) scale(${zoom})`}}>
        <Img src={staticFile(plate)} style={{position: 'absolute', inset: 0, width: PIC_W, height: PIC_H, objectFit: 'cover', filter: `brightness(${0.56 + 0.44 * lit})`}} />
        <div style={{position: 'absolute', left: 0, top: 0, width: SCREEN_W, height: h, transformOrigin: '0 0', transform: pinMatrix(SCREEN_W, h, quad),
          borderRadius: SCREEN_W * 0.105, overflow: 'hidden', fontFamily: UI, color: INK}}>
          {typeof background === 'string' ? <AbsoluteFill style={{background}} /> : background}
          {children}
          <Glass />
          <div style={{position: 'absolute', inset: 0, zIndex: 6, background: '#05090b', opacity: 1 - lit}} />
        </div>
      </div>
    </AbsoluteFill>
  );
};

const Bubble: React.FC<{children: React.ReactNode; at: number; size: number}> = ({children, at, size}) => {
  const f = useCurrentFrame();
  const o = interpolate(f, [at, at + 5], [0, 1], clamp);
  const y = interpolate(f, [at, at + 6], [14, 0], clamp);
  return (
    <div style={{opacity: o, transform: `translateY(${y}px)`, alignSelf: 'flex-start', maxWidth: '88%', background: '#cdd6dc', borderRadius: size * 0.62,
      borderBottomLeftRadius: size * 0.18, padding: `${size * 0.5}px ${size * 0.66}px`, fontSize: size, lineHeight: 1.16, boxShadow: '0 2px 6px rgba(18,23,27,0.12)'}}>
      {children}
    </div>
  );
};

/** Three dots that pulse in turn while the other side is writing. */
const Typing: React.FC = () => {
  const f = useCurrentFrame();
  return (
    <div style={{alignSelf: 'flex-start', background: '#cdd6dc', borderRadius: 30, borderBottomLeftRadius: 9, padding: '22px 26px', display: 'flex', gap: 10,
      boxShadow: '0 2px 6px rgba(18,23,27,0.12)'}}>
      {[0, 1, 2].map((i) => (
        <div key={i} style={{width: 14, height: 14, borderRadius: 7, background: '#4f5b64', opacity: 0.3 + 0.7 * Math.max(0, Math.sin(f / 3.2 - i * 0.95))}} />
      ))}
    </div>
  );
};

/** E03: the breakup text as a filing. A parody: a generic messaging screen, no seal or agency mark. */
export const FilingPhone: React.FC<{at?: number}> = ({at = 6}) => {
  const f = useCurrentFrame();
  return (
    <HeldPhone plate="gen/plates/hand_phone.png" quad={handDay.quads[0]} background="linear-gradient(180deg, #f1f3f5, #e4e8eb)">
      <StatusBar time={PHONE.filingClock} ink={INK} />
      <div style={{position: 'absolute', left: 0, right: 0, top: 0, height: 172, boxSizing: 'border-box', display: 'flex', alignItems: 'center', gap: 14,
        padding: '64px 20px 0', background: 'rgba(247,249,250,0.94)', borderBottom: '1.5px solid rgba(18,23,27,0.12)', zIndex: 2}}>
        <span style={{fontSize: 52, fontWeight: 300, color: '#46525b', marginTop: -8, width: 22}}>‹</span>
        <div style={{width: 62, height: 62, borderRadius: 31, background: 'linear-gradient(160deg, #a9b5bd, #7f8d97)', display: 'flex', alignItems: 'center', justifyContent: 'center',
          fontSize: 24, fontWeight: 700, color: '#f4f6f7', letterSpacing: '0.02em'}}>TB</div>
        <div>
          <div style={{fontSize: 31, fontWeight: 700, lineHeight: 1.1}}>The Board</div>
          <div style={{fontSize: 20, color: '#66717a', marginTop: 2}}>{f < at ? 'typing…' : 'Board of Directors'}</div>
        </div>
      </div>
      <div style={{position: 'absolute', left: 0, right: 0, top: 196, textAlign: 'center', fontSize: 19, color: '#6f7a83', fontWeight: 600}}>{PHONE.filingStamp}</div>
      <div style={{position: 'absolute', left: 20, right: 20, top: 236, display: 'flex', flexDirection: 'column', gap: 16}}>
        {f < at && <Typing />}
        <Bubble at={at} size={48}>
          <div style={{fontWeight: 800, letterSpacing: '0.01em'}}>FORM 8-K</div>
          <div style={{color: '#4b555c', fontSize: 34, marginTop: 4}}>Item 5.02</div>
        </Bubble>
        <Bubble at={at + 10} size={48}>effective immediately</Bubble>
      </div>
      <div style={{position: 'absolute', left: 16, right: 16, bottom: 40, display: 'flex', alignItems: 'center', gap: 12, zIndex: 2}}>
        <div style={{width: 50, height: 50, borderRadius: 25, background: '#cfd6db', display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: 36, color: '#55616a', fontWeight: 300}}>+</div>
        <div style={{flex: 1, height: 52, borderRadius: 26, background: '#f8fafb', border: '1.5px solid rgba(18,23,27,0.14)', display: 'flex', alignItems: 'center', paddingLeft: 22,
          fontSize: 22, color: '#9aa4ab'}}>Message</div>
      </div>
      <HomeBar ink={INK} />
    </HeldPhone>
  );
};

/** The night phone's lock screen: a cold wallpaper, the date and the clock. */
const NightWallpaper: React.FC = () => (
  <AbsoluteFill style={{background: 'radial-gradient(120% 80% at 28% 18%, #1f4d55 0%, #0d272d 46%, #050f12 100%)'}}>
    {Array.from({length: 10}, (_, i) => {
      const s = 70 + hash(SEED, 300, i) * 150;
      return <div key={i} style={{position: 'absolute', left: `${hash(SEED, 301, i) * 100}%`, top: `${hash(SEED, 302, i) * 100}%`, width: s, height: s, marginLeft: -s / 2, marginTop: -s / 2,
        borderRadius: '50%', background: 'radial-gradient(circle, rgba(140,222,232,0.28), rgba(140,222,232,0) 68%)'}} />;
    })}
  </AbsoluteFill>
);

const LIGHT = '#eafbfd';

const LockFace: React.FC = () => (
  <>
    <StatusBar ink={LIGHT} />
    <div style={{position: 'absolute', left: 0, right: 0, top: 92, textAlign: 'center', color: 'rgba(234,251,253,0.86)', fontSize: 27, fontWeight: 500}}>{PHONE.nightDate}</div>
    <div style={{position: 'absolute', left: 0, right: 0, top: 120, textAlign: 'center', color: LIGHT, fontSize: 138, fontWeight: 300, letterSpacing: '-0.02em',
      fontVariantNumeric: 'tabular-nums', lineHeight: 1.1}}>{PHONE.nightClock}</div>
    {[-1, 1].map((d) => (
      <div key={d} style={{position: 'absolute', bottom: 56, left: d < 0 ? 44 : undefined, right: d > 0 ? 44 : undefined, width: 66, height: 66, borderRadius: 33,
        background: 'rgba(234,251,253,0.14)', border: '1px solid rgba(234,251,253,0.18)'}} />
    ))}
    <HomeBar ink={LIGHT} />
  </>
);

/** A notification card on the lock screen, frosted. */
const Note: React.FC<{glyph: React.ReactNode; app: string; title: string; body: string; o?: number; y?: number; big?: boolean}> = ({glyph, app, title, body, o = 1, y = 0, big}) => (
  <div style={{opacity: o, transform: `translateY(${y}px)`, background: 'rgba(205,236,240,0.86)', borderRadius: 28, padding: big ? '20px 22px 24px' : '15px 20px 17px',
    boxShadow: '0 8px 24px rgba(0,0,0,0.25)', color: INK}}>
    <div style={{display: 'flex', alignItems: 'center', gap: 10, fontSize: 18, fontWeight: 600, letterSpacing: '0.06em', color: '#36565c'}}>
      <div style={{width: 32, height: 32, borderRadius: 9, background: '#1d3a40', display: 'flex', alignItems: 'center', justifyContent: 'center'}}>{glyph}</div>
      <span style={{flex: 1}}>{app}</span><span style={{letterSpacing: 0, fontWeight: 500}}>now</span>
    </div>
    <div style={{fontSize: big ? 30 : 36, fontWeight: 700, marginTop: big ? 12 : 8, lineHeight: 1.1}}>{title}</div>
    <div style={{fontSize: big ? 50 : 25, fontWeight: big ? 700 : 500, color: big ? INK : '#2d4a50', lineHeight: 1.12, marginTop: big ? 6 : 2}}>{body}</div>
  </div>
);

/** E18: his message lights up, in the dark. The phone wakes to its lock screen; the message arrives on the word. */
export const MessagePhone: React.FC<{at?: number; textAt?: number}> = ({at = 6, textAt}) => {
  const f = useCurrentFrame();
  const glow = interpolate(f, [at, at + 8], [0, 1], clamp);
  const t = textAt ?? at;
  return (
    <HeldPhone plate="gen/plates/hand_phone_night.png" quad={handNight.quads[0]} background={<NightWallpaper />} lit={glow}>
      <LockFace />
      <div style={{position: 'absolute', left: 16, right: 16, top: 330}}>
        <Note big glyph={<ChatGlyph size={20} color={LIGHT} />} app="MESSAGE" title="New message" body={`…would be ${SAGA.statementWord}…`}
          o={interpolate(f, [t, t + 6], [0, 1], clamp)} y={interpolate(f, [t, t + 8], [-26, 0], clamp)} />
      </div>
    </HeldPhone>
  );
};

/** E19: the lock screen stacks up with the groups his statement named. */
export const LockScreen: React.FC<{interval?: number}> = ({interval = 12}) => {
  const f = useCurrentFrame();
  const groups = ['Employees', 'Investors', 'Partners', 'Customers'];
  return (
    <HeldPhone plate="gen/plates/hand_phone_night.png" quad={handNight.quads[0]} background={<NightWallpaper />}>
      <LockFace />
      <div style={{position: 'absolute', left: 16, right: 16, top: 300, display: 'flex', flexDirection: 'column', gap: 12}}>
        {groups.map((g, i) => {
          const at = i * interval;
          if (f < at) return null;
          return <Note key={g} glyph={<Handpiece size={22} color={LIGHT} rot={-20} />} app="PHONE" title={g} body="Missed call"
            o={interpolate(f, [at, at + 4], [0, 1], clamp)} y={interpolate(f, [at, at + 6], [-18, 0], clamp)} />;
        })}
      </div>
    </HeldPhone>
  );
};

/** E07: four phones ringing on a desk; plain-text caller IDs, no seals or logos. Answer is white, not green (brief). */
export const FourPhones: React.FC<{callers?: string[]; ringEvery?: number}> = ({callers = ['COMMITTEE', 'COMMITTEE', 'COMMITTEE', 'FBI'], ringEvery = 24}) => {
  const f = useCurrentFrame();
  const w = 320, k = w / 430;
  return (
    <DarkRoom>
      <div style={{position: 'absolute', inset: 0, background: 'linear-gradient(180deg, rgba(190,200,205,0.2), rgba(70,76,82,0.3))'}} />
      <div style={{position: 'absolute', left: 0, right: 0, top: 74, display: 'flex', justifyContent: 'center', gap: 62}}>
        {callers.map((c, i) => {
          const phase = (f + i * 7) % ringEvery;
          const ringing = phase < ringEvery * 0.55;
          const dx = ringing ? (hash(SEED, 40 + i, f) - 0.5) * 5 : 0;
          const rot = (i - 1.5) * 2.4 + (ringing ? (hash(SEED, 50 + i, f) - 0.5) * 1.4 : 0);
          const pulse = (phase % 12) / 12;
          return (
            <Handset key={i} w={w} style={{transform: `translateX(${dx}px) rotate(${rot}deg)`}}>
              <div style={{position: 'absolute', inset: 0, background: 'radial-gradient(110% 70% at 50% 24%, #34444c 0%, #172025 55%, #0b0f12 100%)'}} />
              <StatusBar time="9:14" ink="#dfe7eb" k={k} />
              <div style={{position: 'absolute', left: 0, right: 0, top: 92, textAlign: 'center', fontSize: 20, color: T.soft, letterSpacing: '0.04em'}}>Incoming call</div>
              <div style={{position: 'absolute', left: '50%', top: 132, width: 118, height: 118, marginLeft: -59}}>
                {ringing && [0, 0.5].map((d) => {
                  const p = (pulse + d) % 1;
                  return <div key={d} style={{position: 'absolute', inset: -34 * p, borderRadius: '50%', border: '2px solid rgba(223,231,235,0.5)', opacity: 1 - p}} />;
                })}
                <div style={{position: 'absolute', inset: 0, borderRadius: '50%', background: 'linear-gradient(160deg, #6f7f89, #3c4850)', display: 'flex', alignItems: 'center',
                  justifyContent: 'center', fontSize: 50, fontWeight: 700, color: '#eef3f5'}}>{c[0]}</div>
              </div>
              <div style={{position: 'absolute', left: 0, right: 0, top: 276, textAlign: 'center', fontSize: c.length > 5 ? 38 : 60, fontWeight: 700, letterSpacing: '0.02em'}}>{c}</div>
              <div style={{position: 'absolute', left: 0, right: 0, top: c.length > 5 ? 326 : 350, textAlign: 'center', fontSize: 19, color: T.soft}}>calling…</div>
              <div style={{position: 'absolute', left: 0, right: 0, bottom: 58, display: 'flex', justifyContent: 'space-around'}}>
                {[{bg: ringing ? T.alert : '#8d3a3e', rot: 135, label: 'Decline', ink: '#fff'}, {bg: '#e9eef1', rot: 0, label: 'Accept', ink: '#1a2228'}].map((b) => (
                  <div key={b.label} style={{display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 8}}>
                    <div style={{width: 74, height: 74, borderRadius: 37, background: b.bg, display: 'flex', alignItems: 'center', justifyContent: 'center'}}>
                      <Handpiece size={38} color={b.ink} rot={b.rot} />
                    </div>
                    <div style={{fontSize: 16, color: T.soft}}>{b.label}</div>
                  </div>
                ))}
              </div>
              <HomeBar ink="#dfe7eb" k={k} />
            </Handset>
          );
        })}
      </div>
    </DarkRoom>
  );
};

/** E20, E21: the desk phone's caller ID, placed over G10's blank display, with the tags stacking beside it. */
export const CallerID: React.FC<{name?: string; tags?: {text: string; at: number}[]; x?: number; y?: number}> = ({name = 'SENIOR LEVELS', tags = [], x = 150, y = 300}) => {
  const f = useCurrentFrame();
  const blink = Math.floor(f / 8) % 2 === 0;
  return (
    <>
      <div style={{position: 'absolute', left: x, top: y, width: 520, padding: '22px 28px', background: 'rgba(8,24,30,0.92)', border: `1px solid rgba(160,230,255,0.5)`,
        borderRadius: 6, fontFamily: UI, color: '#cdf3ff', boxShadow: '0 0 34px rgba(120,220,255,0.28)'}}>
        <div style={{display: 'flex', justifyContent: 'space-between', fontSize: 19, letterSpacing: '0.12em', color: 'rgba(205,243,255,0.75)'}}>
          <span>INCOMING</span><span style={{opacity: blink ? 1 : 0.25}}>●</span>
        </div>
        <div style={{fontSize: 48, fontWeight: 700, letterSpacing: '0.04em', marginTop: 8}}>{name}</div>
      </div>
      <TagStack tags={tags} />
    </>
  );
};

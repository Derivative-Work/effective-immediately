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

const SCREEN_W = 430;
const INK = '#12171b';

/**
 * E03, E18, E19: a generated hand holding a phone with a blank screen, the UI corner-pinned to that screen
 * (scripts/track_display.py). The UI covers the whole screen, so the plate's notch goes and the handset stays generic.
 * The plate is pushed in about the phone so the words read.
 */
const HeldPhone: React.FC<{plate: string; quad: Quad; background: string; lit?: number; children: React.ReactNode}> = ({plate, quad, background, lit = 1, children}) => {
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
          borderRadius: SCREEN_W * 0.105, overflow: 'hidden', background, fontFamily: UI, color: INK}}>
          {children}
          <div style={{position: 'absolute', inset: 0, background: '#05090b', opacity: 1 - lit}} />
        </div>
      </div>
    </AbsoluteFill>
  );
};

const Bubble: React.FC<{children: React.ReactNode; at: number; size: number}> = ({children, at, size}) => {
  const o = interpolate(useCurrentFrame(), [at, at + 5], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  return (
    <div style={{opacity: o, alignSelf: 'flex-start', maxWidth: '92%', background: '#d5dbdf', borderRadius: size * 0.72,
      padding: `${size * 0.56}px ${size * 0.72}px`, fontSize: size, lineHeight: 1.18}}>
      {children}
    </div>
  );
};

/** E03: the breakup text as a filing. A parody: a generic messaging screen, no seal or agency mark. */
export const FilingPhone: React.FC<{at?: number}> = ({at = 6}) => (
  <HeldPhone plate="gen/plates/hand_phone.png" quad={handDay.quads[0]} background="#eef2f4">
    <div style={{padding: '52px 20px 18px', borderBottom: '2px solid rgba(18,23,27,0.16)', textAlign: 'center', fontSize: 34, fontWeight: 700}}>The Board</div>
    <div style={{display: 'flex', flexDirection: 'column', gap: 20, padding: '30px 20px'}}>
      <Bubble at={at} size={50}>
        <div style={{fontWeight: 800, letterSpacing: '0.01em'}}>FORM 8-K</div>
        <div style={{color: '#4b555c', fontSize: 36, marginTop: 4}}>Item 5.02</div>
      </Bubble>
      <Bubble at={at + 10} size={50}>effective immediately</Bubble>
    </div>
  </HeldPhone>
);

/** E18: his message lights up, in the dark. */
export const MessagePhone: React.FC<{at?: number; textAt?: number}> = ({at = 6, textAt}) => {
  const f = useCurrentFrame();
  const glow = interpolate(f, [at, at + 8], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  const card = interpolate(f, [textAt ?? at, (textAt ?? at) + 6], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  return (
    <HeldPhone plate="gen/plates/hand_phone_night.png" quad={handNight.quads[0]} background="#dff5f6" lit={glow}>
      <div style={{position: 'absolute', left: 18, right: 18, top: 250, opacity: card, background: '#bfe3e6', borderRadius: 30, padding: '26px 26px'}}>
        <div style={{fontSize: 30, color: '#2d4a50', marginBottom: 8, fontWeight: 600}}>New message</div>
        <div style={{fontSize: 52, fontWeight: 700, lineHeight: 1.12}}>…would be {SAGA.statementWord}…</div>
      </div>
    </HeldPhone>
  );
};

/** E19: the lock screen stacks up with the groups his statement named. */
export const LockScreen: React.FC<{interval?: number}> = ({interval = 12}) => {
  const f = useCurrentFrame();
  const groups = ['Employees', 'Investors', 'Partners', 'Customers'];
  return (
    <HeldPhone plate="gen/plates/hand_phone_night.png" quad={handNight.quads[0]} background="#dff5f6">
      <div style={{position: 'absolute', left: 18, right: 18, top: 62, display: 'flex', flexDirection: 'column', gap: 16}}>
        {groups.map((g, i) => {
          const at = i * interval;
          if (f < at) return null;
          return (
            <div key={g} style={{opacity: interpolate(f, [at, at + 4], [0, 1], {extrapolateRight: 'clamp'}), background: '#bfe3e6', borderRadius: 26, padding: '18px 26px'}}>
              <div style={{fontSize: 46, fontWeight: 700}}>{g}</div>
              <div style={{fontSize: 31, color: '#2d4a50', fontWeight: 500}}>Missed call</div>
            </div>
          );
        })}
      </div>
    </HeldPhone>
  );
};

/** E07: four phones ringing on a desk; plain-text caller IDs, no seals or logos. */
export const FourPhones: React.FC<{callers?: string[]; ringEvery?: number}> = ({callers = ['COMMITTEE', 'COMMITTEE', 'COMMITTEE', 'FBI'], ringEvery = 24}) => {
  const f = useCurrentFrame();
  const w = 320;
  return (
    <DarkRoom>
      <div style={{position: 'absolute', inset: 0, background: 'linear-gradient(180deg, rgba(190,200,205,0.2), rgba(70,76,82,0.3))'}} />
      <div style={{position: 'absolute', left: 0, right: 0, top: 74, display: 'flex', justifyContent: 'center', gap: 62}}>
        {callers.map((c, i) => {
          const phase = (f + i * 7) % ringEvery;
          const ringing = phase < ringEvery * 0.55;
          const dx = ringing ? (hash(SEED, 40 + i, f) - 0.5) * 5 : 0;
          const rot = (i - 1.5) * 2.4 + (ringing ? (hash(SEED, 50 + i, f) - 0.5) * 1.4 : 0);
          return (
            <Handset key={i} w={w} style={{transform: `translateX(${dx}px) rotate(${rot}deg)`}}>
              <div style={{position: 'absolute', inset: 0, background: '#14181c', display: 'flex', flexDirection: 'column', alignItems: 'center', paddingTop: 130}}>
                <div style={{fontSize: 24, color: T.soft, marginBottom: 16}}>Incoming call</div>
                <div style={{fontSize: c.length > 5 ? 40 : 64, fontWeight: 700, letterSpacing: '0.02em'}}>{c}</div>
                <div style={{marginTop: 150, width: 86, height: 86, borderRadius: 43, background: ringing ? T.alert : '#6d3134'}} />
              </div>
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

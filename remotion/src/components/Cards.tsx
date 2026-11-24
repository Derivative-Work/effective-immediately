import React from 'react';
import {AbsoluteFill, Img, interpolate, staticFile, useCurrentFrame} from 'remotion';
import cards from '../../../config/cards.json';
import {UI, LABEL} from '../Fonts';
import {T} from '../theme';
import {useFade, WithPlaceholders} from './Common';

const Card: React.FC<{children: React.ReactNode; pad?: string}> = ({children, pad = '70px 150px'}) => {
  const o = useFade(0, 6);
  return (
    <AbsoluteFill style={{background: '#0b0d0f', color: T.white, fontFamily: UI, padding: pad, justifyContent: 'center', opacity: o}}>
      {children}
    </AbsoluteFill>
  );
};

/** The fact card, in pages so every line stays readable. Every word comes from config/cards.json (the brief). */
export const FactCard: React.FC<{page: number; perPage?: number}> = ({page, perPage = 4}) => {
  const lines = cards.facts.slice(page * perPage, (page + 1) * perPage);
  const pages = Math.ceil(cards.facts.length / perPage);
  return (
    <Card>
      <div style={{fontFamily: LABEL, fontSize: 30, letterSpacing: '0.16em', color: T.soft, marginBottom: 30}}>WHAT HAPPENED · {page + 1}/{pages}</div>
      <div style={{display: 'flex', flexDirection: 'column', gap: 24}}>
        {lines.map((l) => <div key={l} style={{fontSize: 31, lineHeight: 1.36}}><WithPlaceholders text={l} /></div>)}
      </div>
    </Card>
  );
};

export const DisclosureCard: React.FC = () => (
  <Card>
    <div style={{fontFamily: LABEL, fontSize: 30, letterSpacing: '0.16em', color: T.soft, marginBottom: 26}}>WHO HAS A STAKE</div>
    <div style={{fontSize: 29, lineHeight: 1.38}}><WithPlaceholders text={cards.disclosure} /></div>
    <div style={{fontSize: 27, lineHeight: 1.38, color: T.soft, marginTop: 24}}>{cards.probe_note}</div>
  </Card>
);

export const EndCard: React.FC = () => {
  const [title, ...rest] = cards.end_card.split('. ');
  return (
    <Card>
      <div style={{fontSize: 76, fontWeight: 700, letterSpacing: '-0.01em', marginBottom: 34}}>{title}</div>
      <div style={{display: 'flex', flexDirection: 'column', gap: 9, fontSize: 32, lineHeight: 1.3}}>
        {rest.map((l) => <div key={l}><WithPlaceholders text={l.replace(/\.$/, '')} /></div>)}
      </div>
    </Card>
  );
};

/** The three dated cards, the last thing on screen before the final line. */
export const DatedCards: React.FC<{interval?: number}> = ({interval = 36}) => {
  const f = useCurrentFrame();
  return (
    <AbsoluteFill style={{background: '#0b0d0f', color: T.white, fontFamily: UI, alignItems: 'center', justifyContent: 'center'}}>
      <div style={{display: 'flex', flexDirection: 'column', gap: 26}}>
        {cards.closing.map((c, i) => {
          const at = i * interval;
          const [k, v] = c.split(': ');
          return (
            <div key={c} style={{opacity: interpolate(f, [at, at + 6], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'}), fontSize: 58, display: 'flex', gap: 22}}>
              <span style={{fontWeight: 400, color: T.soft}}>{k}:</span><span style={{fontWeight: 700}}>{v}</span>
            </div>
          );
        })}
      </div>
    </AbsoluteFill>
  );
};

export const FinalCard: React.FC = () => {
  const m = cards.final.match(/^(.*?) (\(.*\))$/);
  return (
    <Card pad="0 150px">
      <div style={{textAlign: 'center', fontSize: 74, fontWeight: 700}}>{m ? m[1] : cards.final}</div>
      {m && <div style={{textAlign: 'center', fontSize: 40, color: T.soft, marginTop: 14}}>{m[2]}</div>}
    </Card>
  );
};

/** E01, E25: a real screenshot, captioned plainly, with no commentary. */
export const RealScreenshot: React.FC<{src?: string; stamp: string; maxW?: number; maxH?: number}> = ({src, stamp, maxW = 1400, maxH = 660}) => (
  <AbsoluteFill style={{background: '#0b0d0f', alignItems: 'center', justifyContent: 'center', flexDirection: 'column', gap: 34, fontFamily: UI, color: T.white}}>
    {src
      ? <Img src={staticFile(src)} style={{maxWidth: maxW, maxHeight: maxH, objectFit: 'contain', boxShadow: '0 18px 50px rgba(0,0,0,0.55)'}} />
      : <div style={{width: 1400, height: 640, border: `2px dashed ${T.alert}`, display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: 34, color: T.alert}}>
          [screenshot from the human]
        </div>}
    <div style={{fontFamily: LABEL, fontSize: 30, letterSpacing: '0.08em'}}>real screenshot · {stamp}</div>
  </AbsoluteFill>
);

import React from 'react';
import {Img, staticFile} from 'remotion';
import {SAGA} from '../config';
import {UI} from '../Fonts';
import {T} from '../theme';

/** E23: the small desk sign on the empty counselor's chair's desk. */
export const DeskSign: React.FC<{x: number; y: number; scale?: number}> = ({x, y, scale = 1}) => {
  const [title, status] = SAGA.governanceSigns[0].split(' · ');
  return (
    <div style={{position: 'absolute', left: x, top: y, transform: `scale(${scale})`, transformOrigin: 'top left', padding: '9px 16px', background: '#1a1613',
      border: `1px solid ${T.brassDark}`, color: T.brassLight, fontFamily: UI, textAlign: 'center', boxShadow: '0 6px 14px rgba(0,0,0,0.45)'}}>
      <div style={{fontSize: 18, fontWeight: 600, whiteSpace: 'nowrap'}}>{title}</div>
      <div style={{fontSize: 14, fontStyle: 'italic', opacity: 0.85, whiteSpace: 'nowrap'}}>{status}</div>
    </div>
  );
};

/** E23: the committee's name in frosted lettering on the glass wall. */
export const GlassSign: React.FC<{x: number; y: number; width?: number}> = ({x, y, width = 620}) => (
  <div style={{position: 'absolute', left: x, top: y, width, fontFamily: UI, fontSize: 26, fontWeight: 500, lineHeight: 1.25, letterSpacing: '0.05em',
    color: 'rgba(255,246,228,0.78)', textShadow: '0 0 8px rgba(255,235,200,0.3)'}}>
    {SAGA.governanceSigns[1]}
  </div>
);

/** E22: the page the probe holds up, a texture for the Blender set. A customer's order, not a vote. */
export const PurchaseOrder: React.FC = () => (
  <div style={{position: 'absolute', inset: 0, background: T.paper, color: T.paperInk, fontFamily: UI, padding: '54px 30px', boxSizing: 'border-box', textAlign: 'center'}}>
    <div style={{fontSize: 96, fontWeight: 900, lineHeight: 1.02, letterSpacing: '-0.01em'}}>PURCHASE</div>
    <div style={{fontSize: 134, fontWeight: 900, lineHeight: 1.02, letterSpacing: '-0.01em'}}>ORDER</div>
    <div style={{height: 10, background: T.paperInk, margin: '34px 0'}} />
    {[100, 82, 92].map((w, i) => <div key={i} style={{height: 24, width: `${w}%`, margin: '0 auto 30px', background: '#9c9c98'}} />)}
  </div>
);

/** E24: the plaque with our own wording, over the generated blank brass cutout if there is one. */
export const Plaque: React.FC<{x: number; y: number; width?: number; src?: string; opacity?: number}> = ({x, y, width = 300, src, opacity = 1}) => {
  const height = width * 0.56;
  return (
    <div style={{position: 'absolute', left: x, top: y, width, height, opacity, boxShadow: '0 5px 12px rgba(20,8,0,0.55)',
      background: src ? undefined : `linear-gradient(135deg, ${T.brassLight}, ${T.brass} 45%, ${T.brassDark})`, overflow: 'hidden'}}>
      {src && <Img src={staticFile(src)} style={{position: 'absolute', inset: 0, width: '100%', height: '100%', objectFit: 'cover'}} />}
      <div style={{position: 'absolute', inset: 0, display: 'flex', alignItems: 'center', justifyContent: 'center', textAlign: 'center', padding: '0 11%',
        fontFamily: UI, fontWeight: 700, fontSize: width * 0.095, lineHeight: 1.25, color: '#1f1507', textShadow: '0 1px 0 rgba(255,235,190,0.65)'}}>
        This is where it all got started
      </div>
    </div>
  );
};

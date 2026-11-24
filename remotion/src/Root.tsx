import React from 'react';
import {AbsoluteFill, Composition} from 'remotion';
import {THUMBNAILS} from './Thumbnail';
import {CalendarInsert, Confetti, DayCounters, MarketChart, Scoreboard} from './components/Data';
import {CallerID, FilingPhone, FourPhones, LockScreen, MessagePhone} from './components/Phones';
import {DatedCards, DisclosureCard, EndCard, FactCard, FinalCard, RealScreenshot} from './components/Cards';
import {DarkRoom, LowerThird, TagStack} from './components/Common';
import {DisplayText, JacketWall, Plate} from './components/Plates';
import {DeskSign, GlassSign, Plaque, PurchaseOrder} from './components/Signs';
import {FPS, Grade, H, SAGA, W} from './config';
import g10Still from '../public/gen/track/G10_still.json';
import {Fonts} from './Fonts';
import {LookLayer} from './look/LookLayer';
import {Animatic, ANIMATIC_FRAMES} from './Animatic';
import type {SubStyle} from './components/Subtitles';
import {Reel, REEL_FRAMES} from './Reel';

/** M2's test bench: every code component through the look layer, on placeholder backgrounds until the plates are in. */
type Test = {id: string; grade?: Grade; frame: number; el: React.ReactNode};

const WarmRoom: React.FC<{children: React.ReactNode}> = ({children}) => (
  <AbsoluteFill style={{background: 'radial-gradient(ellipse 80% 90% at 50% 35%, #8a6a44, #4a3524 60%, #1f150e)'}}>{children}</AbsoluteFill>
);

const TAGS = [
  {text: SAGA.officialsTag, at: 0},
  {text: 'Investigation: continuing (Nvidia, Nov 23)', at: 6},
  {text: 'House interviews: Dec 1–2', at: 12},
  {text: 'The White House took credit on TV the same day (see fact card)', at: 18},
];

const P = (id: string) => `gen/plates/${id}.png`;

/** The real plates through the look layer, with their overlays: what the M2 gate is judging. */
const PLATE_TESTS: Test[] = [
  {id: 'L-E02-G01', grade: 'cold', frame: 10, el: <Plate src={P('G01')} />},
  {id: 'L-E04-wall', grade: 'cold', frame: 30, el: <JacketWall mode="hung" at={999} />},
  {id: 'L-E05-wall', grade: 'cold', frame: 60, el: <JacketWall mode="gone" />},
  {id: 'L-E06-G02', grade: 'cold', frame: 20, el: <><Plate src={P('G02')} /><LowerThird title="The Company" sub="Statement" /></>},
  {id: 'L-E10-G03', grade: 'cold', frame: 10, el: <Plate src={P('G03')} />},
  {id: 'L-E13-G04', grade: 'cold', frame: 10, el: <><Plate src={P('G04')} /><Scoreboard pulse={0.7} x="76%" y="42%" /></>},
  {id: 'L-E14-G05', grade: 'cold', frame: 10, el: <Plate src={P('G05')} />},
  {id: 'L-E15-G06', grade: 'cold', frame: 10, el: <Plate src={P('G06')} />},
  {id: 'L-E16-G07', grade: 'cyan', frame: 10, el: <Plate src={P('G07')} />},
  {id: 'L-E17-G08', grade: 'cyan', frame: 10, el: <Plate src={P('G08')} />},
  {id: 'L-E18-G09', grade: 'cyan', frame: 10, el: <Plate src={P('G09')} />},
  {id: 'L-E21-G10', grade: 'cyan', frame: 30, el: <><Plate src={P('G10')} /><DisplayText quad={g10Still.quads[0]} /><TagStack tags={TAGS} left={70} top={60} width={640} /></>},
  {id: 'L-E22-wall', grade: 'warm', frame: 40, el: <JacketWall mode="return" at={10} />},
  {id: 'L-E23-S02', grade: 'warm', frame: 10, el: <><Plate src={P('S02')} /><DeskSign x={700} y={470} scale={1.5} /><GlassSign x={1120} y={70} width={640} /></>},
  {id: 'L-E24-G11', grade: 'warm', frame: 40, el: <><Plate src={P('G11')} /><Plaque x={810} y={70} width={300} src="gen/plaque.png" /><DayCounters /></>},
];

export const TESTS: Test[] = [
  ...PLATE_TESTS,
  {id: 'E03-filing', grade: 'cold', frame: 30, el: <FilingPhone />},
  {id: 'E06-lower-third', grade: 'cold', frame: 20, el: <DarkRoom><LowerThird title="The Company" sub="Statement" /></DarkRoom>},
  {id: 'E07-four-phones', grade: 'cold', frame: 8, el: <FourPhones />},
  {id: 'E09-lower-third', grade: 'cold', frame: 20, el: <DarkRoom><LowerThird title="Effective immediately" /></DarkRoom>},
  {id: 'E11-market-drop', grade: 'cold', frame: 60, el: <><MarketChart mode="drop" /><Confetti startFrame={24} /></>},
  {id: 'E13-scoreboard', grade: 'cold', frame: 10, el: <DarkRoom><Scoreboard pulse={0.7} /></DarkRoom>},
  {id: 'E15-calendar', grade: 'cold', frame: 24, el: <CalendarInsert />},
  {id: 'E18-message', grade: 'cyan', frame: 24, el: <MessagePhone />},
  {id: 'E19-lock-screen', grade: 'cyan', frame: 48, el: <LockScreen />},
  {id: 'E21-caller-id', grade: 'cyan', frame: 30, el: <DarkRoom tone="night"><CallerID tags={TAGS} /></DarkRoom>},
  {id: 'E22-market-recover', grade: 'warm', frame: 48, el: <MarketChart mode="recover" />},
  {id: 'E23-signs', grade: 'warm', frame: 10, el: <WarmRoom><DeskSign x={1120} y={500} /><GlassSign x={180} y={120} /></WarmRoom>},
  {id: 'E24-plaque-counters', grade: 'warm', frame: 40, el: <WarmRoom><Plaque x={810} y={150} /><DayCounters /></WarmRoom>},
  {id: 'C1-facts-1', frame: 12, el: <FactCard page={0} />},
  {id: 'C2-facts-2', frame: 12, el: <FactCard page={1} />},
  {id: 'C3-facts-3', frame: 12, el: <FactCard page={2} />},
  {id: 'C4-disclosure', frame: 12, el: <DisclosureCard />},
  {id: 'C5-end', frame: 12, el: <EndCard />},
  {id: 'C6-dated', frame: 90, el: <DatedCards />},
  {id: 'C7-final', frame: 12, el: <FinalCard />},
  {id: 'E01-screenshot', frame: 12, el: <RealScreenshot stamp="Nov 12, 2026" />},
];

export const Root: React.FC = () => (
  <>
    <Composition id="Animatic" width={W} height={H} fps={FPS} durationInFrames={ANIMATIC_FRAMES} defaultProps={{stillFrame: 0, subStyle: 'set' as SubStyle | 'none', label: '', slate: true}}
      component={(p: {stillFrame: number; subStyle: SubStyle | 'none'; label: string; slate: boolean}) => <><Fonts /><Animatic subStyle={p.subStyle} label={p.label || undefined} slate={p.slate} /></>} />
    <Composition id="Reel" width={W} height={H} fps={FPS} durationInFrames={REEL_FRAMES} defaultProps={{stillFrame: 0}}
      component={(_: {stillFrame: number}) => <><Fonts /><Reel /></>} />
    {/* Textures for the Blender set: no look layer here, since they pass through it with the render. */}
    <Composition id="TX-purchase-order" width={600} height={800} fps={FPS} durationInFrames={1} defaultProps={{stillFrame: 0}}
      component={(_: {stillFrame: number}) => <><Fonts /><PurchaseOrder /></>} />
    <Composition id="TX-screen-drop" width={1920} height={804} fps={FPS} durationInFrames={72} defaultProps={{stillFrame: 60}}
      component={(_: {stillFrame: number}) => <><Fonts /><MarketChart mode="drop" /></>} />
    <Composition id="TX-screen-recover" width={1920} height={804} fps={FPS} durationInFrames={72} defaultProps={{stillFrame: 60}}
      component={(_: {stillFrame: number}) => <><Fonts /><MarketChart mode="recover" /></>} />
    {Object.entries(THUMBNAILS).map(([k, C]) => (
      <Composition key={`Thumb-${k}`} id={`Thumb-${k}`} width={1280} height={720} fps={FPS} durationInFrames={1} defaultProps={{stillFrame: 0}}
        component={(_: {stillFrame: number}) => <><Fonts /><C /></>} />
    ))}
    {TESTS.map((t) => (
      <Composition key={t.id} id={t.id} width={W} height={H} fps={FPS} durationInFrames={120}
        defaultProps={{stillFrame: t.frame}}
        component={(_: {stillFrame: number}) => (
          <>
            <Fonts />
            {t.grade ? <LookLayer grade={t.grade} handheld>{t.el}</LookLayer> : t.el}
          </>
        )} />
    ))}
  </>
);

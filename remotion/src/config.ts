import look from '../../config/look.json';
import saga from '../../config/saga.json';
import seeds from '../../config/seeds.json';

export const LOOK = look;
export const SAGA = saga;
export const SEED: number = seeds.main;
export const FPS = look.frame.fps;
export const W = look.frame.width;
export const H = look.frame.height;
export const PIC_W = W;
export const PIC_H = look.frame.picture_height;

export type Grade = keyof typeof look.grades;

/** The brief's rule for still moves: never faster than 5% of the frame width per second. */
export const maxScaleDelta = (frames: number) => (look.move.max_width_per_s * frames) / FPS;

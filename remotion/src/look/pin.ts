/** Corner-pin: the CSS matrix3d that maps a w x h box onto a tracked quad (TL, TR, BR, BL, in the parent's pixels). */
export type Quad = number[][];

export const pinMatrix = (w: number, h: number, q: Quad): string => {
  const [[x0, y0], [x1, y1], [x2, y2], [x3, y3]] = q;
  const dx1 = x1 - x2, dx2 = x3 - x2, sx = x0 - x1 + x2 - x3;
  const dy1 = y1 - y2, dy2 = y3 - y2, sy = y0 - y1 + y2 - y3;
  const det = dx1 * dy2 - dx2 * dy1;
  const g = (sx * dy2 - dx2 * sy) / det;
  const k = (dx1 * sy - sx * dy1) / det;
  const a = x1 - x0 + g * x1, b = x3 - x0 + k * x3;
  const d = y1 - y0 + g * y1, e = y3 - y0 + k * y3;
  // The unit square to the quad, preceded by the box to the unit square. CSS lists the matrix by columns.
  return `matrix3d(${[a / w, d / w, 0, g / w, b / h, e / h, 0, k / h, 0, 0, 1, 0, x0, y0, 0, 1].join(',')})`;
};

/** A quad inset by fractions of its own sides, so content sits inside the screen's edge. */
export const insetQuad = (q: Quad, fx: number, fy: number): Quad => {
  const mix = (a: number[], b: number[], t: number) => [a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t];
  const at = (u: number, v: number) => mix(mix(q[0], q[1], u), mix(q[3], q[2], u), v);
  return [at(fx, fy), at(1 - fx, fy), at(1 - fx, 1 - fy), at(fx, 1 - fy)];
};

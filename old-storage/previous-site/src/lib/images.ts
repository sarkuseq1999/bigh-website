import dims from "../../content/harvest/_dims.json";

const DIMS = dims as unknown as Record<string, [number, number]>;

/** Real pixel dimensions of a harvested asset (probed at harvest time). */
export function imageDims(localPath: string): { width: number; height: number } {
  const d = DIMS[localPath];
  return d ? { width: d[0], height: d[1] } : { width: 1200, height: 1200 };
}

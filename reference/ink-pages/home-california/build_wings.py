"""The hummingbird's wings that never stop (part 2, October 29, 2026).

Mo: "One of the very interesting features about hummingbirds is that its wings are just like a
dragonfly. The wings are always moving." Each look is two Codex paintings in the bird's frame
(1538 x 1023): the bird with its wings raised (the still) and the same bird with its wings
removed (an edit of it). The painted wings are what the two differ by; they are lifted out and
beat about the shoulder as a wing does seen from the side: each one shortens toward the shoulder
as it swings toward you and comes out the other side, below the body, then back. Each frame is
blurred over its own slice of the beat, the way the eye sees a hummingbird's wings. Six frames a
beat; at 60 frames a second that is ten beats a second (a real Anna's beats about forty times a
second, which a screen cannot show without the wings appearing to crawl).

Out: plates/wings/<look>/ (git-ignored): body.png/.webp (the wingless bird), near.png/.webp and
far.png/.webp (the six frames of each wing side by side; near is drawn over the body, far behind
it), still.png (the frames' top pose over the body), sheet.png (the six frames, for looking), and
rig.json (where the wings' box sits in the bird's frame, in % of it, for the page).

    python -X utf8 reference/ink-pages/home-california/build_wings.py [look ...]
"""

import json
import math
import sys
from pathlib import Path

import cv2
import numpy as np
from PIL import Image

from cut_california import divided, to_alpha

HERE = Path(__file__).resolve().parent
ORIG = HERE / "originals"
OUT = HERE / "plates" / "wings"

FRAMES = 6  # a beat; the page plays them at 60 a second
BLUR = 24  # samples across each frame's slice of the beat
SHUTTER = 0.85  # of a frame's slice the blur spans
SCALE = 0.7  # of the original's pixels, for the sprite frames

# Each look: its painting with raised wings and its wingless edit.
LOOKS = {
    "anna": ("hummingbird-wings-1", "hummingbird-body-1"),
    "female": ("hummingbird-female-1", "hummingbird-female-body-1"),
    "allens": ("allens-1", "allens-body-1"),
    # Mo (October 29): Allen's, but more like a painting. Codex painted these afresh in the old
    # crane's loose hand, so they are lined up on allens-1 (its bill tip and tail tip), where the
    # page's line leaves from.
    "allens-loose": ("allens-loose-2", "allens-loose-body-2"),
    "allens-few": ("allens-few-1", "allens-few-body-1"),
}
LINE_UP = {"allens-loose": "allens-1", "allens-few": "allens-1"}
# Where a look's shoulders and wing split differ from the rig's (its painting's own anatomy,
# after lining up): near shoulder, far shoulder, (split point, split angle).
# How much a look's colour is calmed (saturation, brightness): allens-few came out a bright
# pumpkin orange, louder than the gold sun; calmed toward the redwood bark's copper.
CALM = {"allens-few": (0.72, 0.94)}
SHOULDERS = {"allens-few": ((686.0, 542.0), (700.0, 526.0), ((690.0, 540.0), -19.0))}
# The beat, in the painting's pixels. Each wing turns about its shoulder (where it meets the
# back). Its length along the shoulder-to-tip line runs from 1 (as painted, raised) to `low`
# (negative: through the shoulder and out below the body), while it turns by `turn` degrees
# toward the bottom of the beat (a little forward, as a hummingbird's wing sweeps).
RIG = {
    "near": {"shoulder": (712.0, 512.0), "low": -0.78, "turn": 14.0, "chord": 0.82},
    "far": {"shoulder": (716.0, 494.0), "low": -0.62, "turn": 10.0, "chord": 0.82},
    # Pixels whose direction from this point is clockwise of this angle (degrees from straight
    # up) belong to the far wing; the rest to the near wing: a ray up the gap between the wings.
    "split": ((712.0, 512.0), -8.0),
}
DEFAULT_SHOULDERS = (RIG["near"]["shoulder"], RIG["far"]["shoulder"], RIG["split"])


def rgba(name):
    """A painting on bare paper -> float RGBA (0..1), paper transparent."""
    arr = divided(Image.open(ORIG / f"{name}.png"))
    return np.asarray(to_alpha(arr)).astype(np.float32) / 255.0


def aligned(moving, fixed):
    """Line `moving` up on `fixed` (ECC, a small turn and shift: the edit redraws the bird)."""
    a = cv2.GaussianBlur((moving[..., 3] * 255).astype(np.uint8), (0, 0), 2)
    b = cv2.GaussianBlur((fixed[..., 3] * 255).astype(np.uint8), (0, 0), 2)
    warp = np.eye(2, 3, dtype=np.float32)
    criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 200, 1e-6)
    _, warp = cv2.findTransformECC(b, a, warp, cv2.MOTION_EUCLIDEAN, criteria, None, 5)
    h, w = fixed.shape[:2]
    out = cv2.warpAffine(moving, warp, (w, h), flags=cv2.INTER_LINEAR | cv2.WARP_INVERSE_MAP)
    return out, warp


def calmed(rgba_, sat, val):
    """The painting's colours with less saturation and a little less brightness."""
    hsv = cv2.cvtColor(np.ascontiguousarray(rgba_[..., :3]), cv2.COLOR_RGB2HSV)
    hsv[..., 1] *= sat
    hsv[..., 2] *= val
    out = rgba_.copy()
    out[..., :3] = cv2.cvtColor(hsv, cv2.COLOR_HSV2RGB)
    return out


def tips(rgba_):
    """The bill's tip (the bird's rightmost ink) and the tail's (its lowest-left ink)."""
    ys, xs = np.nonzero(rgba_[..., 3] > 0.35)
    bill = np.array([xs.max(), ys[xs.argmax()]], np.float32)
    k = (xs - ys).argmin()
    tail = np.array([xs[k], ys[k]], np.float32)
    return tail, bill


def line_up(painted, body, ref_name):
    """Turn, scale and move a fresh painting (and its wingless edit) so its tail tip and bill tip
    land on the reference painting's."""
    ref = rgba(ref_name)
    (t0, b0), (t1, b1) = tips(painted), tips(ref)
    v0, v1 = b0 - t0, b1 - t1
    scale = np.linalg.norm(v1) / np.linalg.norm(v0)
    turn = math.atan2(v1[1], v1[0]) - math.atan2(v0[1], v0[0])
    a = scale * np.array([[math.cos(turn), -math.sin(turn)], [math.sin(turn), math.cos(turn)]])
    m = np.zeros((2, 3), np.float32)
    m[:, :2] = a
    m[:, 2] = t1 - a @ t0
    h, w = ref.shape[:2]
    warp = lambda img: cv2.warpAffine(img, m, (w, h), flags=cv2.INTER_LINEAR, borderValue=0)
    print(f"  lined up on {ref_name}: scale {scale:.3f}, turn {math.degrees(turn):.1f} deg")
    return warp(painted), warp(body)


def lift_wings(painted, body):
    """The painted wings: where the painting differs from its wingless edit, split in two."""
    diff = np.abs(painted[..., :3] * painted[..., 3:] - body[..., :3] * body[..., 3:]).max(axis=2)
    diff = np.maximum(diff, painted[..., 3] - body[..., 3])
    mask = np.clip((cv2.GaussianBlur(diff, (0, 0), 3) - 0.05) / 0.12, 0, 1)
    # Only the wings' own reach: above the body's back and around the shoulder (the edit also
    # redraws the body's speckles a little, which must not come along).
    h, w = mask.shape
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    sx, sy = RIG["near"]["shoulder"]
    reach = np.clip((560 - np.hypot(xx - sx, yy - sy)) / 40, 0, 1)
    mask *= reach
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, np.ones((9, 9), np.uint8))
    # Keep the two wings, not the stray specks the edit's redrawn body leaves around them.
    count, labels, stats, _ = cv2.connectedComponentsWithStats((mask > 0.25).astype(np.uint8), 8)
    keep = np.zeros(count, bool)
    keep[1:] = stats[1:, cv2.CC_STAT_AREA] >= 3000
    mask *= cv2.dilate(keep[labels].astype(np.uint8), np.ones((15, 15), np.uint8)).astype(np.float32)
    wings = painted.copy()
    wings[..., 3] *= mask
    (px, py), divide = RIG["split"]
    angle = np.degrees(np.arctan2(xx - px, py - yy))
    far = (angle > divide) & (yy < py + 10)
    near_w, far_w = wings.copy(), wings.copy()
    near_w[..., 3] *= ~far
    far_w[..., 3] *= far
    return near_w, far_w


def tip_axis(wing, shoulder):
    """Unit vector from the shoulder toward the wing's ink-weighted far end."""
    a = wing[..., 3]
    ys, xs = np.nonzero(a > 0.1)
    d = np.stack([xs - shoulder[0], ys - shoulder[1]], axis=1).astype(np.float32)
    r = np.linalg.norm(d, axis=1)
    far = d[r > np.percentile(r, 85)]
    u = far.mean(axis=0)
    return u / np.linalg.norm(u)


def posed(wing, side, t):
    """The wing at phase t (0 = top of the beat, 0.5 = bottom)."""
    rig = RIG[side]
    sx, sy = rig["shoulder"]
    u = tip_axis(wing, rig["shoulder"])
    v = np.array([-u[1], u[0]])
    c = math.cos(2 * math.pi * t)  # 1 at the top, -1 at the bottom
    s = (1 + rig["low"]) / 2 + (1 - rig["low"]) / 2 * c
    s = math.copysign(max(abs(s), 0.03), s)
    k = (1 - c) / 2  # 0 at the top, 1 at the bottom
    chord = 1 - (1 - rig["chord"]) * (1 - abs(c))
    turn = math.radians(rig["turn"] * k)
    rot = np.array([[math.cos(turn), -math.sin(turn)], [math.sin(turn), math.cos(turn)]])
    a = rot @ (s * np.outer(u, u) + chord * np.outer(v, v))
    m = np.zeros((2, 3), np.float32)
    m[:, :2] = a
    m[:, 2] = np.array([sx, sy]) - a @ np.array([sx, sy])
    h, w = wing.shape[:2]
    premul = wing.copy()
    premul[..., :3] *= premul[..., 3:]
    out = cv2.warpAffine(premul, m, (w, h), flags=cv2.INTER_LINEAR, borderValue=0)
    return out


def blurred(wing, side, k):
    """Frame k: the wing averaged over its slice of the beat, centred on k / FRAMES."""
    acc = None
    for i in range(BLUR):
        t = (k + SHUTTER * ((i + 0.5) / BLUR - 0.5)) / FRAMES
        layer = posed(wing, side, t)
        acc = layer if acc is None else acc + layer
    acc /= BLUR
    a = acc[..., 3:]
    rgb = acc[..., :3] / np.maximum(a, 1e-6)
    return np.concatenate([rgb, a], axis=2)


def over(top, bottom):
    a = top[..., 3:] + bottom[..., 3:] * (1 - top[..., 3:])
    rgb = (top[..., :3] * top[..., 3:] + bottom[..., :3] * bottom[..., 3:] * (1 - top[..., 3:])) / np.maximum(a, 1e-6)
    return np.concatenate([rgb, a], axis=2)


def to_img(arr):
    return Image.fromarray((np.clip(arr, 0, 1) * 255).astype(np.uint8), "RGBA")


def build(look):
    out = OUT / look
    out.mkdir(parents=True, exist_ok=True)
    painted_name, body_name = LOOKS[look]
    painted = rgba(painted_name)
    body, warp = aligned(rgba(body_name), painted)
    RIG["near"]["shoulder"], RIG["far"]["shoulder"], RIG["split"] = SHOULDERS.get(look, DEFAULT_SHOULDERS)
    if look in LINE_UP:
        painted, body = line_up(painted, body, LINE_UP[look])
    if look in CALM:
        painted, body = calmed(painted, *CALM[look]), calmed(body, *CALM[look])
    near, far = lift_wings(painted, body)
    to_img(near).save(out / "lifted-near.png")
    to_img(far).save(out / "lifted-far.png")
    size = (painted.shape[1], painted.shape[0])
    frames = {"near": [blurred(near, "near", k) for k in range(FRAMES)], "far": [blurred(far, "far", k) for k in range(FRAMES)]}

    # One box for every frame of both wings, so the page lays both sprites on the same spot.
    alpha = np.max([f[..., 3] for side in frames for f in frames[side]], axis=0)
    ys, xs = np.nonzero(alpha > 0.01)
    box = (int(xs.min()) - 4, int(ys.min()) - 4, int(xs.max()) + 5, int(ys.max()) + 5)
    bw, bh = box[2] - box[0], box[3] - box[1]
    fw, fh = round(bw * SCALE), round(bh * SCALE)

    for side in ("near", "far"):
        strip = Image.new("RGBA", (fw * FRAMES, fh), (0, 0, 0, 0))
        for k, f in enumerate(frames[side]):
            strip.paste(to_img(f).crop(box).resize((fw, fh), Image.LANCZOS), (k * fw, 0))
        strip.save(out / f"{side}.png", optimize=True)
        strip.save(out / f"{side}.webp", quality=86, method=6)

    to_img(body).save(out / "body.png", optimize=True)
    to_img(body).save(out / "body.webp", quality=88, method=6)
    still = over(frames["near"][0], over(body, frames["far"][0]))
    to_img(still).save(out / "still.png", optimize=True)

    # For looking: each frame composited on paper, cropped round the bird, in a row of three.
    paper = np.ones((size[1], size[0], 4), np.float32)
    paper[..., :3] = np.array([0.96, 0.94, 0.90])
    ba = body[..., 3]
    bys, bxs = np.nonzero(np.maximum(ba, alpha) > 0.02)
    crop = (max(0, bxs.min() - 30), max(0, bys.min() - 30), min(size[0], bxs.max() + 30), min(size[1], bys.max() + 30))
    tiles = []
    for k in range(FRAMES):
        f = over(frames["near"][k], over(body, over(frames["far"][k], paper)))
        tiles.append(to_img(f).convert("RGB").crop(crop))
    tw, th = tiles[0].size
    sheet = Image.new("RGB", (tw * 3, th * 2), "white")
    for k, tile in enumerate(tiles):
        sheet.paste(tile, ((k % 3) * tw, (k // 3) * th))
    sheet.thumbnail((2000, 2000))
    sheet.save(out / "sheet.png")

    rig = {
        "frame": size,
        "box": {
            "left": round(box[0] / size[0] * 100, 3),
            "top": round(box[1] / size[1] * 100, 3),
            "width": round(bw / size[0] * 100, 3),
            "height": round(bh / size[1] * 100, 3),
        },
        "frames": FRAMES,
        "sprite": [fw, fh],
        "body_warp": warp.round(4).tolist(),
    }
    (out / "rig.json").write_text(json.dumps(rig, indent=2), encoding="utf-8", newline="\n")
    print(look, rig)


def main():
    looks = sys.argv[1:] or list(LOOKS)
    for look in looks:
        build(look)


if __name__ == "__main__":
    main()

"""The basket's woven front, cut from the bicycle painting, to lay over the bottle standing in it.
Opaque: the painting multiplied onto the page's paper colour, so the bottle does not show through
the weave. The top edge follows the basket's near rim."""

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

d = np.asarray(Image.open("art/bike1.png").convert("RGB")).astype(np.float32)
paper = np.array([244, 239, 228], np.float32)  # the page's rice paper, sampled from a screenshot
rgb = (d / 255.0 * paper).clip(0, 255).astype(np.uint8)
h, w = d.shape[:2]
rim = [(372, 268), (390, 282), (460, 305), (530, 322), (600, 332), (660, 336), (720, 335), (780, 331), (850, 322), (910, 310), (945, 296)]
poly = [(355, 255)] + rim + [(962, 290), (962, 720), (355, 720)]
m = Image.new("L", (w, h), 0)
ImageDraw.Draw(m).polygon(poly, fill=255)
m = m.filter(ImageFilter.GaussianBlur(1.6))
out = Image.fromarray(rgb).convert("RGBA")
out.putalpha(m)
out.save("art/bike1-front.png")
print("front", out.size)

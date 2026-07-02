// Full-bleed banner backgrounds per page, measured from the original site.
// Pages absent here render the plain layout (dark title on white).
export const PAGE_BANNERS: Record<string, { img: string; h: number }> = {
  about: { img: "/original/uploads/2019/03/organic.jpg", h: 880 },
  science: { img: "/original/uploads/2019/04/shutterstock_697695826.jpg", h: 832 },
  support: { img: "/original/uploads/2019/04/support_bg1.jpg", h: 897 },
  organic: { img: "/original/uploads/2019/04/sprouts.jpg", h: 832 },
  "non-gmo": { img: "/original/uploads/2019/03/gmo1.jpg", h: 676 },
  "gluten-free": { img: "/original/uploads/2019/03/organic-1.jpg", h: 1272 },
  vegan: { img: "/original/uploads/2019/03/vegan-3.jpg", h: 730 },
  signup: { img: "/original/uploads/2019/04/signup_bg4.jpg", h: 900 },
  login: { img: "/original/uploads/2019/04/login_bg5.jpg", h: 1000 },
};

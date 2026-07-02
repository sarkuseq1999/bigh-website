"use client";

import Image from "next/image";
import { useState } from "react";

interface GalleryProps {
  images: { src: string; width: number; height: number }[];
  alt: string;
}

// Main bottle shot + thumbnail strip; thumbnails swap the main image,
// matching (and smoothing) the original page's gallery behavior.
export function ProductGallery({ images, alt }: GalleryProps) {
  const [active, setActive] = useState(0);
  if (images.length === 0) return null;
  const main = images[active];

  return (
    <div>
      <div className="relative mx-auto max-w-md">
        <Image
          key={main.src}
          src={main.src}
          alt={alt}
          width={main.width}
          height={main.height}
          priority
          className="h-auto w-full drop-shadow-[0_30px_50px_rgba(0,0,0,0.3)]"
          sizes="(max-width: 768px) 90vw, 420px"
        />
      </div>
      {images.length > 1 && (
        <ul className="mt-6 flex justify-center gap-3">
          {images.map((img, i) => (
            <li key={img.src}>
              <button
                type="button"
                onClick={() => setActive(i)}
                aria-label={`${alt} ${i + 1}`}
                aria-current={i === active}
                className={`block w-20 rounded-lg border-2 bg-white/85 p-1.5 transition-colors ${
                  i === active ? "border-white" : "border-white/40 hover:border-white/80"
                }`}
              >
                <Image src={img.src} alt="" width={img.width} height={img.height} className="h-auto w-full" sizes="80px" />
              </button>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}

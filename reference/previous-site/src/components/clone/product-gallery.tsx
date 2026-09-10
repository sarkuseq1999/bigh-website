"use client";

import Image from "next/image";
import { useState } from "react";

interface GalleryProps {
  images: { src: string; width: number; height: number }[];
  alt: string;
  dark?: boolean;
}

// Main bottle shot + thumbnail strip; thumbnails swap the main image,
// matching (and smoothing) the original page's gallery behavior.
export function ProductGallery({ images, alt, dark = false }: GalleryProps) {
  const [active, setActive] = useState(0);
  if (images.length === 0) return null;
  const main = images[active];

  return (
    <div>
      <div className="relative mx-auto max-w-[34rem] md:mx-0">
        <Image
          key={main.src}
          src={main.src}
          alt={alt}
          width={main.width}
          height={main.height}
          priority
          className="h-auto w-full"
          sizes="(max-width: 768px) 90vw, 550px"
        />
      </div>
      {images.length > 1 && (
        <ul className="mt-2 flex justify-center gap-6 md:justify-start md:pl-8">
          {images.map((img, i) => (
            <li key={img.src}>
              <button
                type="button"
                onClick={() => setActive(i)}
                aria-label={`${alt} ${i + 1}`}
                aria-current={i === active}
                className={`block w-[8.25rem] max-w-[22vw] rounded-md border p-1 transition-colors ${
                  dark
                    ? i === active
                      ? "border-black/60 bg-black/5"
                      : "border-black/25 hover:border-black/60"
                    : i === active
                      ? "border-white bg-white/15"
                      : "border-white/50 hover:border-white"
                }`}
              >
                <Image src={img.src} alt="" width={img.width} height={img.height} className="h-auto w-full" sizes="136px" />
              </button>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}

#!/usr/bin/env bash
# Six Codex picture jobs at once, each with today's stroke attached as its reference.
HERE="C:/Users/mcbig/AppData/Local/Temp/claude/C--Users-mcbig-Documents-codes-bigh-website/ae0bce67-3604-4b9f-951a-93a76fcbc79c/scratchpad/fuller"
REF="C:/Users/mcbig/Documents/codes/bigh-website/reference/nav/originals/codex-swash-black.png"
for d in body1 body2 chunky1 chunky2 rich1 rich2; do
  F="$HERE/$d"
  cp "$REF" "$F/reference.png"
  codex exec --skip-git-repo-check -C "$F" -s workspace-write -c model_reasoning_effort="low" \
    -i "$F/reference.png" -o "$F/last-message.txt" \
    "Use your built-in image generation tool to make ONE picture: $(cat "$F/prompt.txt") Copy the PNG into the current folder as stroke.png." \
    > "$F/log.txt" 2>&1 &
done
wait
for d in body1 body2 chunky1 chunky2 rich1 rich2; do
  if [ -f "$HERE/$d/stroke.png" ]; then echo "$d ok"; else echo "$d MISSING"; fi
done

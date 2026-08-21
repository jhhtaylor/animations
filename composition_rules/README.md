# Composition Rules

A Manim animation covering seven core photo/video composition ideas, each
paired with a small original vector "scene" (buildings, trees, a road, a
figure) that reuses the same little world across sections so the examples
read as one consistent place rather than seven unrelated icons.

## Render the video

```bash
cd composition_rules
manim -qm scene.py CompositionRules
```

Output goes to `media/videos/scene/720p30/CompositionRules.mp4` (swap
`-qm` for `-ql`/`-qh`/`-qk` per this repo's usual quality flags).

## Concepts covered

1. **Texture & Repetition** — a repeated grid of windows shows how a
   pattern reads as rhythm; one row gets boxed out to call out "same shape,
   repeated."
2. **Curving Lines** — an S-curve river/road, drawn with `set_points_smoothly`,
   traced by trees shrinking into the distance for depth.
3. **Foreground** — three depth layers: a faint distant skyline, a subject
   at mid-distance, and dark foliage shapes overlapping the frame's edges
   in front of everything.
4. **Rule of Thirds** — a 3x3 grid over a hill silhouette, with the horizon
   on a gridline and the sun on an intersection.
5. **Vanishing Point** — two converging road edges with perspective "ties"
   shrinking toward a labeled vanishing point.
6. **Frame within a Frame** — four dark bars forming a window/archway
   around a small background scene, so the edges vanish and only the
   framed subject reads.
7. **Center** — a symmetric doorway with matching trees on both sides and
   a crosshair guide, making the case for when centering is earned rather
   than lazy.

Inspired by a short-form reel (`composition.mp4`) that pairs a white
line-diagram with a real photo per rule — rebuilt here as fully original
vector art in this repo's house style (VS Code dark theme, no real
footage), consistent with `camera_lens_numbers`.

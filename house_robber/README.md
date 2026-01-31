# House Robber Animation

A Manim animation visualizing the House Robber dynamic programming problem (LeetCode 198).

## Prerequisites

```bash
pip install manim
```

## Render

```bash
# Medium quality (720p, recommended)
manim -qm scene.py HouseRobber

# High quality (1080p)
manim -qh scene.py HouseRobber

# Low quality preview (480p, fast)
manim -ql scene.py HouseRobber
```

Output will be saved to `media/videos/scene/`.

## About

This animation demonstrates the O(n) space-optimized DP solution to the House Robber problem:
- **Example 1**: Step-by-step walkthrough with `[1, 2, 3, 1]`
- **Example 2**: Faster pace with a more complex case `[2, 7, 9, 3, 1, 5, 8, 2, 4, 6]`

Features VS Code dark theme styling with Codicon icons.

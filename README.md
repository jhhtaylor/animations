# Animations

A collection of algorithm visualization animations created with [Manim](https://github.com/ManimCommunity/manim/).

## Setup

1. Install Manim (requires Python 3.8+):
```bash
pip install manim
```

2. For macOS, you may also need:
```bash
brew install py3cairo ffmpeg pango scipy
```

## Projects

| Project | Description |
|---------|-------------|
| [house_robber](./house_robber/) | LeetCode 198 - House Robber dynamic programming visualization |

## Rendering Animations

To render an animation:
```bash
cd <project_folder>
manim -pql scene.py <SceneName>
```

Quality options:
- `-ql` - Low quality (480p, 15fps) - fast preview
- `-qm` - Medium quality (720p, 30fps)
- `-qh` - High quality (1080p, 60fps)
- `-qk` - 4K quality (2160p, 60fps)

Add `-p` to preview immediately after rendering.

## Structure

Each animation project has its own folder:
```
animations/
├── project_name/
│   ├── scene.py      # Main animation code
│   └── README.md     # Project-specific documentation
└── ...
```

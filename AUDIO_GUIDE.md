````markdown
# Game Audio Guide

## Required Audio Files

The game supports the following audio files (place in the main game directory):

### 1. Background Music (BGM) - Electronic Style
**Filename**: `bgm.mp3` or `bgm.ogg` or `bgm.wav`
- **Style**: Electronic, Pixel Music, Chiptune
- **Duration**: Recommended 2-3 minutes loopable
- **Volume**: Set to 50% in game
- **Recommended websites**:
  - [FreeMusicArchive](https://freemusicarchive.org/) - Search "chiptune" or "8bit"
  - [OpenGameArt](https://opengameart.org/) - Search "electronic music"
  - [Incompetech](https://incompetech.com/) - Free royalty-free music

### 2. Countdown Sound Effect
**Filename**: `countdown.wav` or `countdown.ogg` or `countdown.mp3`
- **Type**: Short "beep" sound or numeric sound effect
- **Duration**: 0.3-0.5 seconds
- **Effect**: Plays when displaying 3, 2, 1
- **Volume**: Set to 70% in game

### 3. Start Sound Effect
**Filename**: `start.wav` or `start.ogg` or `start.mp3`
- **Type**: Motivational, startup sound effect (like "GO!")
- **Duration**: 0.5-1 second
- **Effect**: Plays when countdown ends and game starts
- **Volume**: Set to 80% in game

## Quick Test

### Create simple sound effects using online text-to-speech tools:
1. **Countdown sound**: Visit [ttsmaker.com](https://ttsmaker.com/), type "beep", download as `countdown.wav`
2. **Start sound**: Type "GO!", download as `start.wav`

### Recommended free sound effect websites:
- [Freesound](https://freesound.org/) - Search "countdown beep" and "game start"
- [Zapsplat](https://www.zapsplat.com/) - Free game sound effects library
- [Pixabay](https://pixabay.com/sound-effects/) - Free sound effects, no registration required

## Audio Format Instructions

The game supports the following audio formats (priority from left to right):
- **Background Music**: mp3 > ogg > wav
- **Sound Effects**: wav > ogg > mp3

Recommendations:
- Use **mp3** format for BGM (small file size, good compatibility)
- Use **wav** format for sound effects (low latency, suitable for games)

## Audio File Placement

Place audio files in the main game directory (same level as `counting_butterfly.py`):

```
Counting-Butterfly-Two-Player-Game/
├── counting_butterfly.py
├── bgm.mp3              ← Background music
├── countdown.wav        ← Countdown sound effect
├── start.wav            ← Start sound effect
├── butterfly_blue.png
├── butterfly_red.png
└── ...
```

## Adjust Volume

If you feel the volume is inappropriate, you can modify the volume settings in `counting_butterfly.py`:

```python
# In the load_sounds() function:
pygame.mixer.music.set_volume(0.5)    # BGM volume (0.0-1.0)
sounds['countdown'].set_volume(0.7)   # Countdown sound effect volume
sounds['start'].set_volume(0.8)       # Start sound effect volume
```

## Console Output When Running

When running the game, the console will display audio loading status:
- ✓ Indicates successful loading
- ⚠ Indicates file not found (game still runs normally, just without sound effects)
- ✗ Indicates loading failed

---

**Tip**: The game can still run normally without audio files, just without music and sound effects.

````

# 🦋 Counting Butterfly - Two Player Game

An exciting and challenging two-player butterfly counting competitive game! Players need to quickly and accurately count the number of red and blue butterflies on the screen. The faster you type, the higher your score!

## 🎮 Game Features

### Core Gameplay
- **Two-Player Battle Mode**: Two players compete simultaneously, counting red and blue butterflies respectively
- **Three Difficulty Levels**:
  - **Level 1**: ~8 butterflies, static distribution, perfect for warm-up
  - **Level 2**: ~15 butterflies, static distribution, tests observation skills
  - **Level 3**: ~12 **moving butterflies**, 360° random motion, ultimate challenge!
- **Speed Bonus System**: The faster you submit, the higher your bonus score
- **Dynamic Audio Feedback**: Keypress sounds, success sounds, error sounds for full immersive experience

### Visual Design
- Retro pixel art style interface (Press Start 2P font)
- Colorful butterfly sprite animations
- White outlined text ensuring all colors are clearly visible
- Smooth countdown and level transition animations

### Audio System
- 🎵 **Electronic Style BGM**: Looping energetic background music
- 🔊 **3-2-1 Countdown Sound**: Exciting start signal
- ✨ **Start Sound Effect**: Game start notification
- 🔔 **Keypress Feedback**: Instant audio feedback for every input
- ✅ **Success Sound**: Pleasant chord when answer is correct
- ❌ **Error Sound**: Alert tone when answer is wrong

## 🎯 Game Rules

### Player Roles
- **Left Player (Blue)**: Count **Blue Butterflies**
- **Right Player (Red)**: Count **Red Butterflies**

### Controls
### Controls
| Player | Increase | Decrease | Submit |
|--------|----------|----------|--------|
| Blue (Left) | W | S | Space |
| Red (Right) | ↑ | ↓ | Enter |

**Other Controls**:
- **ESC** - Pause/Resume game
- **Space** - Start game (main menu)

### Scoring Rules
1. **Base Score**: 50 points for correct answer
2. **Speed Bonus**:
   - Within 5 seconds: +30 points
   - Within 10 seconds: +20 points
   - Within 15 seconds: +10 points
   - Over 15 seconds: No bonus
3. **Wrong Answer**: No points deducted, but no score gained

### Game Flow
1. Press **Space** to start the game
2. Watch the **3-2-1** countdown animation
3. Start counting after **Game Start!**
4. Use arrow keys to adjust your answer
5. Press submit key to confirm
6. View results and scores
7. Complete three levels to see final ranking

## 🛠️ Technical Implementation

### Development Environment
- **Language**: Python 3
- **Main Library**: Pygame
- **Resolution**: 800 × 480 pixels
- **Frame Rate**: 60 FPS

### Key Features
- **Collision Detection System**: Moving butterflies in Level 3 avoid each other to prevent overlapping
- **State Machine Management**: 7 game states (start, countdown, playing, input, result, game over, paused)
- **Audio Management**: 6 sound effect files with independent volume control
- **Pause Functionality**: Press **ESC** to pause/resume anytime
- **Movement Physics**: Butterfly boundary reflection and collision separation algorithms

### File Structure
### File Structure
```
Counting-Butterfly-Two-Player-Game/
├── counting_butterfly.py          # Main game file (1280+ lines)
├── generate_game_audio.py         # BGM and basic sound generation script
├── generate_additional_sounds.py  # Keypress and feedback sound generation script
├── PressStart2P-Regular.ttf       # Pixel font file
├── bgm.wav                        # Background music (2.5MB)
├── countdown.wav                  # Countdown sound effect
├── start.wav                      # Start sound effect
├── beep.wav                       # Keypress sound effect
├── success.wav                    # Success sound effect
├── wrong.wav                      # Error sound effect
└── README.md                      # Documentation
```

## 🚀 Quick Start

### System Requirements
- Python 3.6 or higher
- macOS / Windows / Linux

### Install Dependencies
```bash
pip install pygame
```

### Run the Game
```bash
python3 counting_butterfly.py
```

Or
```bash
cd Counting-Butterfly-Two-Player-Game
python3 counting_butterfly.py
```

### Generate Audio Files (If Needed)
If audio files are missing or need to be regenerated:

```bash
# Generate BGM, countdown and start sound effects
python3 generate_game_audio.py

# Generate keypress, success and error sound effects
python3 generate_additional_sounds.py
```

## 🎨 Game Interface Guide

### Start Screen
- Displays game title "Counting Butterfly"
- Shows control instructions and player roles
- Prompts "Press SPACE to Start"

### Countdown Phase
- 3-2-1 colored number countdown (Yellow→Orange→Red)
- Each number has a beep sound effect
- Displays "Game Start!" after countdown

### Gameplay
- Butterflies randomly distributed or moving (Level 3)
- Both input boxes show current input values
- Top displays current level and total score
- Center shows "The faster you type the higher the score you get"

### Result Display
- Shows both players' answers and correct answer
- Marks each player "Correct!" or "Wrong!"
- Shows points earned this round (base + speed bonus)
- Shows cumulative total score
- Auto-proceeds to next level after 4 seconds

### Pause Screen
- Semi-transparent black overlay
- Displays yellow "PAUSED" title
- Shows "Press ESC to resume" prompt
- Displays current level and both players' scores

### Game Over
- Displays purple "GAME OVER" title
- Shows final score ranking
- Determines Winner or Draw
- Prompts "Press SPACE to play again"

## 💡 Game Tips

1. **Level 3 Strategy**: Butterflies move, recommend quick scanning or wait for butterflies to spread out before counting
2. **Speed vs Accuracy Balance**: Prioritize correctness while submitting as fast as possible for speed bonus
3. **Zone Counting Method**: Divide screen into sections (top/bottom or left/right), count each zone to avoid duplicates or missing
4. **Use Pause Feature**: Press ESC to pause if you need a break or to discuss strategy, doesn't affect timing
5. **Audio Cues**:
   - Success sound: At least one player answered correctly
   - Error sound: Both players answered incorrectly
   - Keypress sound: Confirms input was registered

## 🎮 Advanced Gameplay

- **Speed Run Mode**: Time yourself to see who can complete three levels fastest
- **High Score Challenge**: Try to get maximum speed bonus on all levels
- **Level 3 Master**: Practice only Level 3 to master quick counting in dynamic environment

## 🐛 Known Features

- Moving butterflies in Level 3 bounce off boundaries and change direction
- Butterflies have smart collision detection during movement, maintaining minimum 70-pixel spacing to prevent overlap
- Music pauses synchronously when game is paused
- Keypress sound volume set to 0.4 to avoid being too harsh
- Game window fixed at 800×480, no fullscreen or resize support

## 📝 Version History

### v2.0 - Audio & Interaction Major Upgrade (2025-11)
- ✨ Added keypress sound feedback system (audio feedback for every input)
- ✨ Added success/error answer sounds (chord for correct, tone for wrong)
- ✨ Added pause functionality (ESC key pause/resume with pause screen)
- ✨ Level 3 added moving butterfly mechanics (360° random motion + collision avoidance)
- 🎨 Optimized text display (white outlines on all colored text)
- 🎨 Redesigned Game Over screen colors (purple title + golden scores)
- 🎨 Improved butterfly distribution algorithm (color independent from position, more random)
- 🐛 Fixed input box occlusion and overlap issues
- 🐛 Fixed control key mapping issues (W/S/SPACE→Blue, ↑/↓/ENTER→Red)
- 🐛 Fixed inter-level pause duration issues
- ⚡ Optimized result display time (unified to 4 seconds)

### v1.0 - Base Version
- 🎮 Two-player battle core gameplay
- 🦋 Three difficulty levels (static butterflies)
- 🎵 Background music and basic sound effects
- ⚡ Speed bonus system
- 🎨 Pixel art style interface

## 🤝 Contributing

Issues and Pull Requests are welcome!

If you have suggestions or found bugs, please:
1. Fork this repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

MIT License

## 👨‍💻 Author

**ChenYingwen-Iris**
- GitHub: [@ChenYingwen-Iris](https://github.com/ChenYingwen-Iris)

## 🙏 Acknowledgments

- Font: [Press Start 2P](https://fonts.google.com/specimen/Press+Start+2P) by CodeMan38
- Music Generation: Python waveform synthesis
- Inspiration: Classic two-player competitive games

---

**🎉 Enjoy the game! May the best counter win! 🦋**

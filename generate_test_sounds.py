#!/usr/bin/env python3
"""
简单的测试音效生成器
生成基础的beep音效用于测试游戏音频系统

需要安装: pip install numpy scipy
或者直接从网上下载音效文件放到游戏目录
"""

import numpy as np
from scipy.io import wavfile
import os

def generate_beep(filename, frequency=800, duration=0.3, sample_rate=44100):
    """生成一个简单的beep音效"""
    t = np.linspace(0, duration, int(sample_rate * duration))
    # 生成正弦波
    wave = np.sin(2 * np.pi * frequency * t)
    # 添加淡入淡出效果
    fade_samples = int(0.05 * sample_rate)
    wave[:fade_samples] *= np.linspace(0, 1, fade_samples)
    wave[-fade_samples:] *= np.linspace(1, 0, fade_samples)
    # 转换为16位整数
    wave = (wave * 32767).astype(np.int16)
    wavfile.write(filename, sample_rate, wave)
    print(f"✓ 生成 {filename}")

def generate_start_sound(filename, sample_rate=44100):
    """生成开始音效（上升音调）"""
    duration = 0.5
    t = np.linspace(0, duration, int(sample_rate * duration))
    # 频率从500Hz上升到1200Hz
    freq = np.linspace(500, 1200, len(t))
    wave = np.sin(2 * np.pi * freq * t / sample_rate)
    # 添加淡入淡出
    fade_samples = int(0.05 * sample_rate)
    wave[:fade_samples] *= np.linspace(0, 1, fade_samples)
    wave[-fade_samples:] *= np.linspace(1, 0, fade_samples)
    # 转换为16位整数
    wave = (wave * 32767).astype(np.int16)
    wavfile.write(filename, sample_rate, wave)
    print(f"✓ 生成 {filename}")

if __name__ == "__main__":
    try:
        print("开始生成测试音效...")
        
        # 生成倒计时beep音
        if not os.path.exists("countdown.wav"):
            generate_beep("countdown.wav", frequency=800, duration=0.3)
        else:
            print("⚠ countdown.wav 已存在，跳过")
        
        # 生成开始音效
        if not os.path.exists("start.wav"):
            generate_start_sound("start.wav")
        else:
            print("⚠ start.wav 已存在，跳过")
        
        print("\n✓ 音效生成完成！")
        print("建议从以下网站下载更专业的音效：")
        print("  - https://freesound.org/")
        print("  - https://opengameart.org/")
        print("\n背景音乐请从网上下载电子乐风格的音乐，命名为 bgm.mp3")
        
    except ImportError:
        print("✗ 需要安装 numpy 和 scipy")
        print("运行: pip install numpy scipy")
        print("\n或者直接从以下网站下载音效：")
        print("  - https://freesound.org/ (搜索 'countdown beep' 和 'game start')")
        print("  - https://zapsplat.com/")
        print("  - https://pixabay.com/sound-effects/")
    except Exception as e:
        print(f"✗ 生成音效失败: {e}")
        print("建议从网上下载现成的音效文件")

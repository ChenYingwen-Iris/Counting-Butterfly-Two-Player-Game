#!/usr/bin/env python3
"""
游戏音频生成器
生成电子乐风格的BGM和游戏音效
"""

import wave
import struct
import math

def generate_wave_data(frequency, duration, sample_rate=44100, volume=0.5):
    """生成正弦波数据"""
    num_samples = int(sample_rate * duration)
    data = []
    for i in range(num_samples):
        t = i / sample_rate
        sample = volume * math.sin(2 * math.pi * frequency * t)
        data.append(int(sample * 32767))
    return data

def apply_envelope(data, attack=0.05, decay=0.1, sustain=0.7, release=0.2, sample_rate=44100):
    """应用ADSR包络"""
    total_samples = len(data)
    attack_samples = int(attack * sample_rate)
    decay_samples = int(decay * sample_rate)
    release_samples = int(release * sample_rate)
    sustain_samples = total_samples - attack_samples - decay_samples - release_samples
    
    result = []
    for i in range(total_samples):
        if i < attack_samples:
            # Attack
            envelope = i / attack_samples
        elif i < attack_samples + decay_samples:
            # Decay
            t = (i - attack_samples) / decay_samples
            envelope = 1.0 - (1.0 - sustain) * t
        elif i < attack_samples + decay_samples + sustain_samples:
            # Sustain
            envelope = sustain
        else:
            # Release
            t = (i - attack_samples - decay_samples - sustain_samples) / release_samples
            envelope = sustain * (1.0 - t)
        
        result.append(int(data[i] * envelope))
    return result

def save_wav(filename, data, sample_rate=44100):
    """保存为WAV文件"""
    with wave.open(filename, 'w') as wav_file:
        wav_file.setnchannels(1)  # 单声道
        wav_file.setsampwidth(2)  # 16位
        wav_file.setframerate(sample_rate)
        for sample in data:
            wav_file.writeframes(struct.pack('h', sample))

def generate_countdown_beep():
    """生成倒计时beep音效"""
    print("生成倒计时音效...")
    sample_rate = 44100
    frequency = 880  # A5音符，清脆的beep
    duration = 0.15
    
    data = generate_wave_data(frequency, duration, sample_rate, volume=0.6)
    data = apply_envelope(data, attack=0.01, decay=0.05, sustain=0.8, release=0.09, sample_rate=sample_rate)
    
    save_wav('countdown.wav', data, sample_rate)
    print("✓ 生成 countdown.wav")

def generate_start_sound():
    """生成开始音效（上升和弦）"""
    print("生成开始音效...")
    sample_rate = 44100
    duration = 0.6
    
    # 创建上升的和弦：C-E-G (523, 659, 784 Hz)
    notes = [
        (523, 0.0, 0.2),   # C
        (659, 0.15, 0.35), # E
        (784, 0.3, 0.6),   # G
    ]
    
    num_samples = int(sample_rate * duration)
    data = [0] * num_samples
    
    for freq, start_time, end_time in notes:
        start_sample = int(start_time * sample_rate)
        note_duration = end_time - start_time
        note_data = generate_wave_data(freq, note_duration, sample_rate, volume=0.3)
        note_data = apply_envelope(note_data, attack=0.02, decay=0.05, sustain=0.8, release=0.1, sample_rate=sample_rate)
        
        for i, sample in enumerate(note_data):
            if start_sample + i < num_samples:
                data[start_sample + i] += sample
    
    # 归一化
    max_val = max(abs(s) for s in data)
    if max_val > 0:
        data = [int(s * 32767 / max_val * 0.8) for s in data]
    
    save_wav('start.wav', data, sample_rate)
    print("✓ 生成 start.wav")

def generate_electronic_bgm():
    """生成简单的电子乐BGM"""
    print("生成背景音乐（这可能需要一些时间）...")
    sample_rate = 44100
    bpm = 128
    beat_duration = 60.0 / bpm
    
    # 定义一个简单的旋律模式（使用C大调音阶）
    # 音符：C D E F G A B C
    scale = [262, 294, 330, 349, 392, 440, 494, 523]
    
    # 创建一个8小节的循环旋律
    melody = [
        # 小节1
        (scale[0], 2), (scale[2], 2), (scale[4], 2), (scale[2], 2),
        # 小节2
        (scale[3], 2), (scale[4], 2), (scale[2], 4),
        # 小节3
        (scale[0], 2), (scale[2], 2), (scale[4], 2), (scale[7], 2),
        # 小节4
        (scale[4], 8),
        # 小节5-8 重复
        (scale[0], 2), (scale[2], 2), (scale[4], 2), (scale[2], 2),
        (scale[3], 2), (scale[4], 2), (scale[2], 4),
        (scale[0], 2), (scale[2], 2), (scale[4], 2), (scale[7], 2),
        (scale[4], 8),
    ]
    
    # 计算总时长
    total_beats = sum(beats for _, beats in melody)
    duration = total_beats * beat_duration
    num_samples = int(sample_rate * duration)
    
    # 生成旋律
    data = [0] * num_samples
    current_time = 0
    
    for freq, beats in melody:
        note_duration = beats * beat_duration
        start_sample = int(current_time * sample_rate)
        
        # 生成音符
        note_data = generate_wave_data(freq, note_duration, sample_rate, volume=0.2)
        note_data = apply_envelope(note_data, attack=0.01, decay=0.1, sustain=0.6, release=0.15, sample_rate=sample_rate)
        
        # 添加到主数据
        for i, sample in enumerate(note_data):
            if start_sample + i < num_samples:
                data[start_sample + i] += sample
        
        current_time += note_duration
    
    # 添加低音节奏（每拍一次）
    bass_freq = 131  # C3
    for beat in range(int(total_beats)):
        start_time = beat * beat_duration
        start_sample = int(start_time * sample_rate)
        bass_duration = beat_duration * 0.3
        
        bass_data = generate_wave_data(bass_freq, bass_duration, sample_rate, volume=0.15)
        bass_data = apply_envelope(bass_data, attack=0.005, decay=0.1, sustain=0.3, release=0.05, sample_rate=sample_rate)
        
        for i, sample in enumerate(bass_data):
            if start_sample + i < num_samples:
                data[start_sample + i] += sample
    
    # 归一化
    max_val = max(abs(s) for s in data)
    if max_val > 0:
        data = [int(s * 32767 / max_val * 0.7) for s in data]
    
    save_wav('bgm.wav', data, sample_rate)
    print("✓ 生成 bgm.wav")

if __name__ == "__main__":
    print("=" * 50)
    print("开始生成游戏音频文件...")
    print("=" * 50)
    
    try:
        # 生成倒计时音效
        generate_countdown_beep()
        
        # 生成开始音效
        generate_start_sound()
        
        # 生成背景音乐
        generate_electronic_bgm()
        
        print("\n" + "=" * 50)
        print("✓ 所有音频文件生成完成！")
        print("=" * 50)
        print("\n生成的文件：")
        print("  - countdown.wav (倒计时音效)")
        print("  - start.wav (开始音效)")
        print("  - bgm.wav (背景音乐)")
        print("\n现在可以运行游戏了：")
        print("  python3 counting_butterfly.py")
        
    except Exception as e:
        print(f"\n✗ 生成失败: {e}")
        import traceback
        traceback.print_exc()

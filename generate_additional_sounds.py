"""
生成额外的游戏音效
- 按键音效（beep）
- 正确答案音效（success）
- 错误答案音效（wrong）
"""

import wave
import struct
import math

def generate_beep_sound(filename="beep.wav", frequency=800, duration=0.1):
    """生成按键音效 - 短促的beep声"""
    sample_rate = 44100
    num_samples = int(sample_rate * duration)
    
    audio_data = []
    for i in range(num_samples):
        # 简单的正弦波
        t = i / sample_rate
        sample = int(32767 * 0.3 * math.sin(2 * math.pi * frequency * t))
        # 添加衰减
        envelope = 1.0 - (i / num_samples)
        sample = int(sample * envelope)
        audio_data.append(struct.pack('<h', sample))
    
    with wave.open(filename, 'w') as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        wav_file.setframerate(sample_rate)
        wav_file.writeframes(b''.join(audio_data))
    
    print(f"✓ 生成按键音效: {filename}")

def generate_success_sound(filename="success.wav"):
    """生成成功音效 - 上升的和弦"""
    sample_rate = 44100
    duration = 0.5
    num_samples = int(sample_rate * duration)
    
    # C大调和弦: C (261.63Hz) -> E (329.63Hz) -> G (392.00Hz) -> C (523.25Hz)
    frequencies = [261.63, 329.63, 392.00, 523.25]
    
    audio_data = []
    for i in range(num_samples):
        t = i / sample_rate
        sample = 0
        
        # 根据时间选择不同的频率
        freq_index = min(int(t * 8), 3)  # 每0.125秒换一个音
        freq = frequencies[freq_index]
        
        sample = int(32767 * 0.3 * math.sin(2 * math.pi * freq * t))
        
        # 添加包络
        envelope = 1.0 - (i / num_samples) * 0.5
        sample = int(sample * envelope)
        
        audio_data.append(struct.pack('<h', sample))
    
    with wave.open(filename, 'w') as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        wav_file.setframerate(sample_rate)
        wav_file.writeframes(b''.join(audio_data))
    
    print(f"✓ 生成成功音效: {filename}")

def generate_wrong_sound(filename="wrong.wav"):
    """生成错误音效 - 下降的不和谐音"""
    sample_rate = 44100
    duration = 0.4
    num_samples = int(sample_rate * duration)
    
    audio_data = []
    for i in range(num_samples):
        t = i / sample_rate
        
        # 从高频下降到低频
        start_freq = 400
        end_freq = 200
        freq = start_freq - (start_freq - end_freq) * (t / duration)
        
        # 添加一点不和谐感
        sample = int(32767 * 0.3 * math.sin(2 * math.pi * freq * t))
        sample += int(32767 * 0.15 * math.sin(2 * math.pi * (freq * 1.5) * t))
        
        # 包络
        envelope = 1.0 - (i / num_samples)
        sample = int(sample * envelope * 0.7)
        
        audio_data.append(struct.pack('<h', sample))
    
    with wave.open(filename, 'w') as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        wav_file.setframerate(sample_rate)
        wav_file.writeframes(b''.join(audio_data))
    
    print(f"✓ 生成错误音效: {filename}")

if __name__ == "__main__":
    print("开始生成额外音效...")
    generate_beep_sound()
    generate_success_sound()
    generate_wrong_sound()
    print("\n所有音效生成完成！")

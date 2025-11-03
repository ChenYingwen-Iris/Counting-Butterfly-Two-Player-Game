#!/usr/bin/env python3
"""
Final translation pass for print statements and docstrings
"""

# Read file
with open('counting_butterfly.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Translations for print statements and docstrings  
replacements = {
    '成功加载 Press Start 2P 字体!': 'Successfully loaded Press Start 2P font!',
    '使用默认系统字体': 'Using default system font',
    '使用pygame默认字体': 'Using pygame default font',
    '加载背景音乐和音效': 'Load background music and sound effects',
    '成功加载背景音乐': 'Successfully loaded BGM',
    '未找到bgm音乐文件': 'BGM music file not found',
    '加载背景音乐失败': 'Failed to load BGM',
    '成功加载倒计时音效': 'Successfully loaded countdown sound',
    '未找到countdown音效文件': 'Countdown sound file not found',
    '加载倒计时音效失败': 'Failed to load countdown sound',
    '成功加载开始音效': 'Successfully loaded start sound',
    '未找到start音效文件': 'Start sound file not found',
    '加载开始音效失败': 'Failed to load start sound',
    '成功加载按键音效': 'Successfully loaded keypress sound',
    '未找到beep音效文件': 'Keypress sound file not found',
    '加载按键音效失败': 'Failed to load keypress sound',
    '成功加载成功音效': 'Successfully loaded success sound',
    '未找到success音效文件': 'Success sound file not found',
    '加载成功音效失败': 'Failed to load success sound',
    '成功加载错误音效': 'Successfully loaded error sound',
    '未找到wrong音效文件': 'Error sound file not found',
    '加载错误音效失败': 'Failed to load error sound',
    '绘制暂停界面': 'Draw pause screen',
}

for chinese, english in replacements.items():
    content = content.replace(chinese, english)

# Write back
with open('counting_butterfly.py', 'w', encoding='utf-8') as f:
    f.write(content)

print('✓ Translated all print statements and docstrings')

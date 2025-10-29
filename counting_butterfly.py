import pygame
import sys
import random
import time

# 初始化pygame
pygame.init()

# 游戏常量
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 480
FPS = 60

# 颜色定义 - 红蓝撞色
RED = (255, 50, 50)
BLUE = (50, 100, 255)
WHITE = (255, 255, 255)
BLACK = (20, 20, 20)
BACKGROUND = (240, 240, 240)

# 创建游戏窗口
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Counting Butterfly!")
clock = pygame.time.Clock()

# 加载字体
try:
    font_large = pygame.font.Font("freesansbold.ttf", 48)
    font_medium = pygame.font.Font("freesansbold.ttf", 32)
    font_small = pygame.font.Font("freesansbold.ttf", 24)
except:
    # 如果系统字体加载失败，使用默认字体
    font_large = pygame.font.SysFont(None, 48)
    font_medium = pygame.font.SysFont(None, 32)
    font_small = pygame.font.SysFont(None, 24)

# 加载角色精灵图片
def load_player_sprites():
    sprites = {}
    try:
        # 加载精灵文件（保留透明通道）
        red_stand = pygame.image.load("red_player_stand.png").convert_alpha()
        red_walk = pygame.image.load("red_player_walk.png").convert_alpha()
        blue_stand = pygame.image.load("blue_player_stand.png").convert_alpha()
        blue_walk = pygame.image.load("blue_player_walk.png").convert_alpha()
        
        width, height = red_stand.get_size()
        print(f"加载的精灵尺寸: {red_stand.get_size()}")
        
        def auto_crop_surface(surf: pygame.Surface) -> pygame.Surface:
            """使用像素掩码自动裁剪透明边距，返回裁剪后的Surface。若失败则原样返回。"""
            try:
                mask = pygame.mask.from_surface(surf)
                rect = mask.get_bounding_rect()
                if rect.width > 0 and rect.height > 0:
                    return surf.subsurface(rect).copy()
            except Exception as _:
                pass
            return surf

        def extract_and_scale_sprite(sprite, frame_index=0):
            """直接使用整个精灵图片，先自动裁剪透明边距再放大显示"""
            # 自动裁剪透明边距
            cropped = auto_crop_surface(sprite)
            sprite_width, sprite_height = cropped.get_size()
            
            # 设置目标高度（可调）
            target_height = 130
            target_width = max(1, int(sprite_width * target_height / max(1, sprite_height)))
            
            # 放大精灵
            scaled = pygame.transform.scale(cropped, (target_width, target_height))
            print(f"裁剪并缩放: 原始({sprite.get_width()}x{sprite.get_height()}) -> 裁剪({sprite_width}x{sprite_height}) -> 缩放({target_width}x{target_height})")
            return scaled
        
        # 提取红色角色 - 使用整个图片
        sprites['red_stand'] = extract_and_scale_sprite(red_stand, 0)
        sprites['red_walk1'] = extract_and_scale_sprite(red_walk, 0)
        sprites['red_walk2'] = extract_and_scale_sprite(red_walk, 0)
        sprites['red_walk3'] = extract_and_scale_sprite(red_walk, 0)
        
        # 提取蓝色角色 - 使用整个图片
        sprites['blue_stand'] = extract_and_scale_sprite(blue_stand, 0)
        sprites['blue_walk1'] = extract_and_scale_sprite(blue_walk, 0)
        sprites['blue_walk2'] = extract_and_scale_sprite(blue_walk, 0)
        sprites['blue_walk3'] = extract_and_scale_sprite(blue_walk, 0)
        
        print("✓ 成功加载所有角色精灵!")
        
    except Exception as e:
        print(f"✗ 加载精灵文件失败: {e}")
        print("将使用后备绘制方法")
        
    return sprites

player_sprites = load_player_sprites()

# 游戏状态
class GameState:
    START_SCREEN = 0
    GAME_PLAY = 1
    INPUT_PHASE = 2
    RESULT_SCREEN = 3
    GAME_OVER = 4

# 蝴蝶类
class Butterfly:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = random.randint(20, 40)
        self.color = (random.randint(200, 255), random.randint(100, 200), random.randint(100, 200))
        self.lifetime = random.uniform(1.2, 2.0)  # 蝴蝶显示时间（调整到1.2-2秒）
        self.spawn_time = time.time()
        self.wing_phase = random.uniform(0, 3.14)  # 翅膀动画相位
        
    def update(self):
        # 翅膀扇动效果
        self.wing_phase += 0.3
        return time.time() - self.spawn_time > self.lifetime
    
    def draw(self, surface):
        # 绘制简单的像素风蝴蝶
        wing_offset = int(5 * abs(pygame.math.Vector2(1, 0).rotate(self.wing_phase * 30).x))
        
        # 蝴蝶身体
        pygame.draw.rect(surface, (50, 50, 50), (self.x, self.y, 4, 10))
        
        # 蝴蝶翅膀
        pygame.draw.ellipse(surface, self.color, (self.x - 8 - wing_offset, self.y - 5, 10, 8))
        pygame.draw.ellipse(surface, self.color, (self.x + 2 + wing_offset, self.y - 5, 10, 8))
        pygame.draw.ellipse(surface, self.color, (self.x - 6 - wing_offset, self.y + 2, 8, 6))
        pygame.draw.ellipse(surface, self.color, (self.x + 2 + wing_offset, self.y + 2, 8, 6))

# 玩家类
class Player:
    def __init__(self, x, color, controls):
        self.x = x
        self.color = color
        self.score = 0
        self.input_value = 0
        self.controls = controls  # (up_key, down_key, submit_key)
        self.submitted = False
        self.animation_frame = 0
        self.animation_timer = 0
        self.animation_counter = 0
        self.is_moving = False
        
    def animate(self):
        """持续动画：每隔固定帧在0/1之间切换，无需按键。"""
        self.animation_timer += 1
        if self.animation_timer > 10:
            self.animation_timer = 0
            self.animation_frame = (self.animation_frame + 1) % 2

    def update(self, events):
        # 仅处理输入（不控制动画开关）
        self.is_moving = False  # 不再影响动画，仅作为其它逻辑占位
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == self.controls[0]:  # 上键/W键
                    self.input_value += 1
                    self.is_moving = True
                elif event.key == self.controls[1]:  # 下键/S键
                    if self.input_value > 0:
                        self.input_value -= 1
                        self.is_moving = True
                elif event.key == self.controls[2]:  # 提交键
                    self.submitted = True
                    self.is_moving = True
        
        self.is_moving = False  # 重置移动状态
        
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == self.controls[0]:  # 上键/W键
                    self.input_value += 1
                    self.is_moving = True
                elif event.key == self.controls[1]:  # 下键/S键
                    if self.input_value > 0:
                        self.input_value -= 1
                        self.is_moving = True
                elif event.key == self.controls[2]:  # 提交键
                    self.submitted = True
                    self.is_moving = True
                    
    def reset_input(self):
        self.input_value = 0
        self.submitted = False
        
    def draw(self, surface, y):
        # 绘制时不再修改动画，只根据已计算的 animation_frame 选择贴图
        
        # 尝试使用精灵
        sprite_key = ""
        if self.color == RED:
            sprite_key = "red_stand" if self.animation_frame == 0 else "red_walk1"
        else:  # BLUE
            sprite_key = "blue_stand" if self.animation_frame == 0 else "blue_walk1"
        
        # 如果有对应的精灵，使用它
        if sprite_key in player_sprites and player_sprites[sprite_key]:
            try:
                sprite = player_sprites[sprite_key]
                
                # 直接居中绘制精灵（无任何边框/背景）
                sprite_x = self.x - sprite.get_width() // 2
                sprite_y = y - sprite.get_height()
                surface.blit(sprite, (sprite_x, sprite_y))
                
                return  # 成功绘制精灵，退出
                
            except Exception as e:
                print(f"精灵绘制错误: {e}")
        
        # 如果精灵加载失败，使用后备方法
        self.draw_fallback(surface, y)
    
    def draw_fallback(self, surface, y):
        # 增强的后备绘制方法 - 更大更明显的角色
        size = 60  # 增大基础尺寸
        
        # 先绘制一个明显的背景边框
        bg_rect = pygame.Rect(self.x - size//2 - 5, y - size - 5, size + 10, size + 10)
        pygame.draw.rect(surface, (255, 255, 255), bg_rect)  # 白色背景
        pygame.draw.rect(surface, (0, 0, 0), bg_rect, 3)      # 黑色边框
        
        # 头部 - 大圆形
        pygame.draw.circle(surface, self.color, (self.x, y - 40), 18)
        pygame.draw.circle(surface, (255, 255, 255), (self.x, y - 40), 18, 2)
        
        # 眼睛
        pygame.draw.circle(surface, (255, 255, 255), (self.x - 6, y - 42), 3)
        pygame.draw.circle(surface, (255, 255, 255), (self.x + 6, y - 42), 3)
        pygame.draw.circle(surface, (0, 0, 0), (self.x - 6, y - 42), 1)
        pygame.draw.circle(surface, (0, 0, 0), (self.x + 6, y - 42), 1)
        
        # 身体 - 矩形
        body_rect = pygame.Rect(self.x - 12, y - 20, 24, 35)
        pygame.draw.rect(surface, self.color, body_rect)
        pygame.draw.rect(surface, (255, 255, 255), body_rect, 2)
        
        # 腿部
        leg_width = 8
        pygame.draw.rect(surface, self.color, (self.x - 10, y + 15, leg_width, 20))
        pygame.draw.rect(surface, self.color, (self.x + 2, y + 15, leg_width, 20))
        pygame.draw.rect(surface, (255, 255, 255), (self.x - 10, y + 15, leg_width, 20), 1)
        pygame.draw.rect(surface, (255, 255, 255), (self.x + 2, y + 15, leg_width, 20), 1)
        
        # 手臂
        arm_width = 6
        pygame.draw.rect(surface, self.color, (self.x - 18, y - 10, arm_width, 20))
        pygame.draw.rect(surface, self.color, (self.x + 12, y - 10, arm_width, 20))
        pygame.draw.rect(surface, (255, 255, 255), (self.x - 18, y - 10, arm_width, 20), 1)
        pygame.draw.rect(surface, (255, 255, 255), (self.x + 12, y - 10, arm_width, 20), 1)
    


# 游戏主类
class ButterflyGame:
    def __init__(self):
        self.state = GameState.START_SCREEN
        self.level = 1
        self.butterflies = []
        self.total_butterflies = 0
        self.current_butterflies = 0
        self.level_target = 0
        self.last_spawn_time = 0
        self.input_timer = 0
        self.correct_answer = 0
        
        # 创建玩家（左右互换位置：红色在右，蓝色在左）
        self.player1 = Player(SCREEN_WIDTH * 3 // 4, RED, (pygame.K_w, pygame.K_s, pygame.K_SPACE))
        self.player2 = Player(SCREEN_WIDTH // 4, BLUE, (pygame.K_UP, pygame.K_DOWN, pygame.K_RETURN))
        
    def start_level(self):
        self.level_target = random.randint([8, 15, 24][self.level-1] - 2, 
                                          [8, 15, 24][self.level-1] + 2)
        self.total_butterflies = 0
        self.current_butterflies = 0
        self.butterflies = []
        self.last_spawn_time = time.time()
        self.state = GameState.GAME_PLAY
        
    def spawn_butterflies(self):
        current_time = time.time()
        if current_time - self.last_spawn_time > 1.5 and self.total_butterflies < self.level_target:
            # 生成1-4只蝴蝶
            count = random.randint(1, min(4, self.level_target - self.total_butterflies))
            for _ in range(count):
                x = random.randint(50, SCREEN_WIDTH - 50)
                y = random.randint(80, SCREEN_HEIGHT - 80)
                self.butterflies.append(Butterfly(x, y))
                self.total_butterflies += 1
            self.last_spawn_time = current_time
            
    def update_gameplay(self):
        # 生成蝴蝶
        self.spawn_butterflies()
        
        # 更新蝴蝶
        self.butterflies = [b for b in self.butterflies if not b.update()]
        self.current_butterflies = len(self.butterflies)
        
        # 检查是否所有蝴蝶都消失了
        if self.total_butterflies >= self.level_target and len(self.butterflies) == 0:
            self.correct_answer = self.total_butterflies
            self.start_input_phase()
            
    def start_input_phase(self):
        self.state = GameState.INPUT_PHASE
        self.input_timer = 10  # 10秒输入时间
        self.player1.reset_input()
        self.player2.reset_input()
        
    def update_input_phase(self, events, dt):
        # 更新输入计时器
        self.input_timer -= dt
        
        # 更新玩家输入
        self.player1.update(events)
        self.player2.update(events)
        
        # 检查是否时间到或两个玩家都已提交
        if self.input_timer <= 0 or (self.player1.submitted and self.player2.submitted):
            self.calculate_results()
            
    def calculate_results(self):
        # 计算得分
        p1_correct = self.player1.input_value == self.correct_answer
        p2_correct = self.player2.input_value == self.correct_answer
        
        if p1_correct and p2_correct:
            # 两个都正确，先提交的得10分，后提交的得5分
            if self.player1.submitted and not self.player2.submitted:
                self.player1.score += 10
                self.player2.score += 5
            elif not self.player1.submitted and self.player2.submitted:
                self.player1.score += 5
                self.player2.score += 10
            else:
                # 同时提交或同时未提交但答案正确
                self.player1.score += 10
                self.player2.score += 10
        elif p1_correct:
            self.player1.score += 10
        elif p2_correct:
            self.player2.score += 10
            
        self.state = GameState.RESULT_SCREEN
        self.result_timer = 3  # 结果显示3秒
        
    def update_result_screen(self, dt):
        self.result_timer -= dt
        if self.result_timer <= 0:
            if self.level < 3:
                self.level += 1
                self.start_level()
            else:
                self.state = GameState.GAME_OVER
                
    def draw_start_screen(self):
        screen.fill(BACKGROUND)
        
        # 游戏标题
        title = font_large.render("Counting Butterfly!", True, BLACK)
        screen.blit(title, (SCREEN_WIDTH//2 - title.get_width()//2, 80))
        
        # 动画推进并绘制玩家
        self.player1.animate()
        self.player2.animate()
        self.player1.draw(screen, SCREEN_HEIGHT//2 + 30)
        self.player2.draw(screen, SCREEN_HEIGHT//2 + 30)
        
        # 游戏说明
        instructions = [
            "Two players count butterflies that appear on screen",
            "Butterflies appear in groups of 1-4 and disappear quickly",
            "After all butterflies, you have 10 seconds to input your count",
            "",
            "Player 1 (RED):",
            "  W/S - Change number, SPACE - Submit",
            "",
            "Player 2 (BLUE):",
            "  UP/DOWN - Change number, ENTER - Submit",
            "",
            "Press SPACE to start!"
        ]
        
        for i, line in enumerate(instructions):
            text = font_small.render(line, True, BLACK)
            screen.blit(text, (SCREEN_WIDTH//2 - text.get_width()//2, 200 + i*25))
            
    def draw_gameplay(self):
        screen.fill(BACKGROUND)
        
        # 绘制关卡信息
        level_text = font_medium.render(f"Level {self.level}", True, BLACK)
        screen.blit(level_text, (SCREEN_WIDTH//2 - level_text.get_width()//2, 20))
        
        # 绘制蝴蝶
        for butterfly in self.butterflies:
            butterfly.draw(screen)
        
        # 动画推进并绘制玩家
        self.player1.animate()
        self.player2.animate()
        self.player1.draw(screen, SCREEN_HEIGHT - 60)
        self.player2.draw(screen, SCREEN_HEIGHT - 60)
        
    def draw_input_phase(self):
        screen.fill(BACKGROUND)
        
        # 绘制计时器
        timer_text = font_medium.render(f"Time: {int(self.input_timer)}", True, BLACK)
        screen.blit(timer_text, (SCREEN_WIDTH//2 - timer_text.get_width()//2, 20))
        
        # 绘制玩家输入框
        pygame.draw.rect(screen, RED, (SCREEN_WIDTH//4 - 50, SCREEN_HEIGHT//2 - 25, 100, 50), 3)
        pygame.draw.rect(screen, BLUE, (SCREEN_WIDTH*3//4 - 50, SCREEN_HEIGHT//2 - 25, 100, 50), 3)
        
        # 绘制玩家输入值
        p1_text = font_large.render(str(self.player1.input_value), True, RED)
        p2_text = font_large.render(str(self.player2.input_value), True, BLUE)
        screen.blit(p1_text, (SCREEN_WIDTH//4 - p1_text.get_width()//2, SCREEN_HEIGHT//2 - p1_text.get_height()//2))
        screen.blit(p2_text, (SCREEN_WIDTH*3//4 - p2_text.get_width()//2, SCREEN_HEIGHT//2 - p2_text.get_height()//2))
        
        # 绘制提交状态
        if self.player1.submitted:
            submit_text = font_small.render("Submitted!", True, RED)
            screen.blit(submit_text, (SCREEN_WIDTH//4 - submit_text.get_width()//2, SCREEN_HEIGHT//2 + 40))
            
        if self.player2.submitted:
            submit_text = font_small.render("Submitted!", True, BLUE)
            screen.blit(submit_text, (SCREEN_WIDTH*3//4 - submit_text.get_width()//2, SCREEN_HEIGHT//2 + 40))
        
        # 动画推进并绘制玩家
        self.player1.animate()
        self.player2.animate()
        self.player1.draw(screen, SCREEN_HEIGHT - 60)
        self.player2.draw(screen, SCREEN_HEIGHT - 60)
        
    def draw_result_screen(self):
        screen.fill(BACKGROUND)
        
        # 显示正确答案
        answer_text = font_medium.render(f"Correct answer: {self.correct_answer}", True, BLACK)
        screen.blit(answer_text, (SCREEN_WIDTH//2 - answer_text.get_width()//2, 100))
        
        # 显示玩家答案和得分
        p1_answer = font_small.render(f"Player 1: {self.player1.input_value}", True, RED)
        p2_answer = font_small.render(f"Player 2: {self.player2.input_value}", True, BLUE)
        screen.blit(p1_answer, (SCREEN_WIDTH//4 - p1_answer.get_width()//2, 200))
        screen.blit(p2_answer, (SCREEN_WIDTH*3//4 - p2_answer.get_width()//2, 200))
        
        # 显示得分
        p1_score = font_small.render(f"Score: {self.player1.score}", True, RED)
        p2_score = font_small.render(f"Score: {self.player2.score}", True, BLUE)
        screen.blit(p1_score, (SCREEN_WIDTH//4 - p1_score.get_width()//2, 250))
        screen.blit(p2_score, (SCREEN_WIDTH*3//4 - p2_score.get_width()//2, 250))
        
        # 显示下一关提示
        if self.level < 3:
            next_text = font_small.render(f"Next: Level {self.level+1}", True, BLACK)
            screen.blit(next_text, (SCREEN_WIDTH//2 - next_text.get_width()//2, 350))
        else:
            next_text = font_small.render("Final Results!", True, BLACK)
            screen.blit(next_text, (SCREEN_WIDTH//2 - next_text.get_width()//2, 350))
        
    def draw_game_over(self):
        screen.fill(BACKGROUND)
        
        # 显示最终得分
        title = font_large.render("Game Over!", True, BLACK)
        screen.blit(title, (SCREEN_WIDTH//2 - title.get_width()//2, 100))
        
        p1_final = font_medium.render(f"Player 1: {self.player1.score}", True, RED)
        p2_final = font_medium.render(f"Player 2: {self.player2.score}", True, BLUE)
        screen.blit(p1_final, (SCREEN_WIDTH//4 - p1_final.get_width()//2, 200))
        screen.blit(p2_final, (SCREEN_WIDTH*3//4 - p2_final.get_width()//2, 200))
        
        # 显示获胜者
        if self.player1.score > self.player2.score:
            winner = font_medium.render("Player 1 Wins!", True, RED)
        elif self.player2.score > self.player1.score:
            winner = font_medium.render("Player 2 Wins!", True, BLUE)
        else:
            winner = font_medium.render("It's a Tie!", True, BLACK)
        screen.blit(winner, (SCREEN_WIDTH//2 - winner.get_width()//2, 300))
        
        # 重新开始提示
        restart = font_small.render("Press SPACE to play again", True, BLACK)
        screen.blit(restart, (SCREEN_WIDTH//2 - restart.get_width()//2, 400))
        
        # 动画推进并绘制玩家
        self.player1.animate()
        self.player2.animate()
        self.player1.draw(screen, SCREEN_HEIGHT - 60)
        self.player2.draw(screen, SCREEN_HEIGHT - 60)
        
    def run(self):
        last_time = time.time()
        
        while True:
            # 计算时间增量
            current_time = time.time()
            dt = current_time - last_time
            last_time = current_time
            
            # 处理事件
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                    elif self.state == GameState.START_SCREEN and event.key == pygame.K_SPACE:
                        self.start_level()
                    elif self.state == GameState.GAME_OVER and event.key == pygame.K_SPACE:
                        # 重置游戏
                        self.__init__()
                        self.state = GameState.START_SCREEN
            
            # 更新游戏状态
            if self.state == GameState.GAME_PLAY:
                self.update_gameplay()
            elif self.state == GameState.INPUT_PHASE:
                self.update_input_phase(events, dt)
            elif self.state == GameState.RESULT_SCREEN:
                self.update_result_screen(dt)
            
            # 绘制游戏
            if self.state == GameState.START_SCREEN:
                self.draw_start_screen()
            elif self.state == GameState.GAME_PLAY:
                self.draw_gameplay()
            elif self.state == GameState.INPUT_PHASE:
                self.draw_input_phase()
            elif self.state == GameState.RESULT_SCREEN:
                self.draw_result_screen()
            elif self.state == GameState.GAME_OVER:
                self.draw_game_over()
            
            pygame.display.flip()
            clock.tick(FPS)

# 运行游戏
if __name__ == "__main__":
    try:
        game = ButterflyGame()
        game.run()
    except Exception as e:
        print(f"游戏运行出错: {e}")
        import traceback
        traceback.print_exc()
        pygame.quit()
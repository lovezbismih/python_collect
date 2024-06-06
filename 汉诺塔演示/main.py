import pygame
import sys
import time
 
# 游戏初始化
pygame.init()
 
# 屏幕设置
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("汉诺塔")
 
# 颜色定义
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
 
# 游戏参数
 
num_disks = 4
tower_positions = [screen_width // 4, screen_width // 2, 3 * screen_width // 4]
disk_height = 20
disk_width_increment = 30
tower_height = screen_height - 50
disk_colors = [(200, 200, 200), (150, 150, 150), (100, 100, 100), (50, 50, 50), (0, 0, 0),
               (255, 100, 100), (100, 255, 100), (100, 100, 255)]
font = pygame.font.SysFont(None, 48)
 
# 初始状态
towers = [[i for i in range(num_disks, 0, -1)], [], []]
selected_tower = 0
moving_disk = None
 
# 记录移动步骤的队列
move_steps = []
 
def draw_towers():
    screen.fill(WHITE)
     
    # 绘制柱子
    for pos in tower_positions:
        pygame.draw.rect(screen, BLACK, (pos - 5, tower_height - (num_disks + 1) * disk_height, 10, (num_disks + 1) * disk_height))
 
    for i, tower in enumerate(towers):
        for j, disk in enumerate(tower):
            disk_width = disk * disk_width_increment
            color = YELLOW if (moving_disk is not None and i == moving_disk[0] and disk == moving_disk[1]) else disk_colors[disk % len(disk_colors)]
            pygame.draw.rect(screen, color,
                             (tower_positions[i] - disk_width / 2, tower_height - (j + 1) * disk_height,
                              disk_width, disk_height))
    pygame.draw.polygon(screen, RED, [(tower_positions[selected_tower], tower_height), 
                                      (tower_positions[selected_tower] - 10, tower_height + 20), 
                                      (tower_positions[selected_tower] + 10, tower_height + 20)])
    pygame.display.flip()
 
def move_disk(from_tower, to_tower):
    if len(towers[from_tower]) == 0:
        return
    disk = towers[from_tower][-1]
    if len(towers[to_tower]) == 0 or towers[to_tower][-1] > disk:
        towers[to_tower].append(towers[from_tower].pop())
 
def hanoi(n, source, target, auxiliary):
    if n == 1:
        move_steps.append((source, target))
    else:
        hanoi(n-1, source, auxiliary, target)
        move_steps.append((source, target))
        hanoi(n-1, auxiliary, target, source)
 
def auto_move():
    global moving_disk, selected_tower
    if move_steps:
        from_tower, to_tower = move_steps.pop(0)
        selected_tower = from_tower
        if towers[selected_tower]:
            moving_disk = (selected_tower, towers[selected_tower][-1])
            draw_towers()
            time.sleep(0.5)
            move_disk(moving_disk[0], to_tower)
            moving_disk = None
            draw_towers()
            time.sleep(0.5)
 
def main():
    global selected_tower, moving_disk
    clock = pygame.time.Clock()
    running = True
     
    # 生成移动步骤
    hanoi(num_disks, 0, 2, 1)
     
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
         
        auto_move()
        clock.tick(30)
 
if __name__ == "__main__":
    towers = [[i for i in range(num_disks, 0, -1)], [], []]
    main()
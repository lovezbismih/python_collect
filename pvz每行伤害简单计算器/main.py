import random
class Plant:
    def __init__(self, name, direct_damage, penetration_damage, attack_frequency):
        self.name = name
        self.direct_damage = direct_damage
        self.penetration_damage = penetration_damage
        self.attack_frequency = attack_frequency
        self.last_attack_time = 0  # 上次攻击的时间
        self.cumulative_damage = 0  # 初始化累计伤害为0
 
    def can_attack(self, time):
        # 检查植物是否到了攻击时间
        return (time - self.last_attack_time) >= self.attack_frequency
 
 
    def attack(self, zombies, time):
        # 植物攻击僵尸
        attacked_zombies = []  # 用于存储被攻击的僵尸
        if zombies and zombies[0].is_alive():  # 确保有僵尸并且最前面的僵尸还活着
            front_zombie = zombies[0]
            front_zombie.health -= self.direct_damage
            self.cumulative_damage += self.direct_damage  # 更新累计伤害
            print(f"At time {time} second, {self.name} attacks and reduces the front zombie health to {front_zombie.health}. Cumulative damage: {self.cumulative_damage}")
            # 如果有穿透伤害并且最前面的僵尸还活着，对所有僵尸造成伤害
            if self.penetration_damage > 0:
                total_penetration_damage = 0  # 初始化穿透伤害总和
                for zombie in zombies:
                    if zombie.is_alive():
                        zombie.health -= self.penetration_damage
                        total_penetration_damage += self.penetration_damage
                        self.cumulative_damage += total_penetration_damage  # 更新累计伤害
                        print(
                            f" - Additional penetration damage of {total_penetration_damage} to all zombies. New cumulative damage: {self.cumulative_damage}")
        print(f"{self.name} attacks at time {time}:")
        for zombie in attacked_zombies:
            print(f" - {zombie.__class__.__name__} health: {zombie.health}")
        self.last_attack_time = time  # 使用传入的 time 参数重置攻击时间
class Zombie:
    def __init__(self, health):
        self.health = health
 
    def is_alive(self):
        return self.health > 0
 
    def die(self, zombies):
        # 僵尸死亡时从列表中移除自己
        if not self.is_alive():
            zombies.remove(self)
 
def simulate_battle(plants, zombies):
    time = 0
    while zombies:  # 只要还有僵尸，就继续战斗
        time += 1
        for plant in plants:
            if plant.can_attack(time):
                plant.attack(zombies, time)  # 传递当前时间给 attack 方法
                # 攻击后检查是否有僵尸死亡，并从列表中移除
                for zombie in list(zombies):  # 使用列表的副本来避免在迭代时修改列表
                    if not zombie.is_alive():
                        zombie.die(zombies)
                        break  # 移除一个僵尸后跳出循环，避免索引错误
        print(f"Time step: {time}")
        print("Zombie healths:", [zombie.health for zombie in zombies if zombie.is_alive()])
 
    print(f"\nAll zombies have been defeated after {time} time steps.")
 
 
# 初始化植物
hamburger = Plant(name="hamburger", direct_damage=random.randint(160, 640), penetration_damage=0, attack_frequency=2.5)
watermelon = Plant(name="watermelon", direct_damage=80, penetration_damage=20, attack_frequency=1.5)
pea = Plant(name="pea", direct_damage=240, penetration_damage=0, attack_frequency=2)
cactus = Plant(name="cactus", direct_damage=0, penetration_damage=120, attack_frequency=2.5)
 
# 初始化僵尸
zombies = [Zombie(health=10000) for _ in range(2)]
 
# 模拟战斗
simulate_battle([hamburger, watermelon, pea, cactus], zombies)
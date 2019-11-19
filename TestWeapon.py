from MainClasss import *


class WeaponObj(Weapon):
    def __init__(self, image, coord, name, max_count, type_bullet, type_damage, attack_radius,
                 range_damage, attack_speed, accuracy, owner, shoot_image, size=None, info='', screen=None, aim=None):
        super().__init__(image, coord, name, max_count, type_bullet, type_damage, attack_radius,
                         range_damage, attack_speed, accuracy, owner, size, info)
        self.shoot_frames = []
        self.screen = screen
        self.aim = aim
        self.frame = 0
        self.event = 0
        for frame in shoot_image:
            self.shoot_frames.append(Image('sprite/Weapon_sprites/' + frame))

    def draw(self):
        print(type(self.get_image()))
        self.screen.blit(self.get_image(), self.get_coord())

    def shoot(self):
        if self.frame < len(self.shoot_frames) - 2:
            if self.event == 8:
                self.frame += 1
                self.event = 0
                self.image = self.shoot_frames[self.frame].get_image()
            else:
                self.event += 1
        else:
            self.image = self.shoot_frames[self.frame].get_image()
            self.frame = 0
            self.event = 0
            if self.coord[0] - self.aim.get_coord()[0] >= 0 and \
                self.coord[1] - self.aim.get_coord()[1] >= 0:
                self.aim.damage(random.choice(range(self.range_damage[0], self.range_damage[1])))
        print(self.frame)
        self.draw()
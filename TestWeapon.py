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
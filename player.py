from MainClasss import *
from pygame import Rect

SPEED = 1


class Player(Person, Sprite):
    def __init__(self, name, coord, frames_forward, frames_back, frames_left, frames_right,  size=None, armor=None):
        Sprite.__init__(self)
        self.f = True
        super().__init__('sprite/person_sprites/' + frames_forward[0], coord, 200, 200, 100, 100, name, frames_forward, frames_back,
                         frames_left, frames_right, size, armor)
        # sites moving lists

        # downloading sprites

        # rect and move
        self.rect = Rect((0, 20, 20, 10))
        print(self.rect)
        self.speed_boost = False

        # draw and animation
        self.collision_x_site = 0
        self.collision_y_site = 0
        self.revers_frame = False
        self.frame = 0
        self.count_next_frame = 0

    def update(self, left, right, up, down, platforms, enemy_platforms, shift):
        if self.die_f is False:
            if shift:
                speed = SPEED * 3
                self.speed_boost = True
            else:
                speed = SPEED
                self.speed_boost = False
            if left:
                self.x_vel = -speed
            if right:
                self.x_vel = speed
            if not (left or right):
                self.x_vel = 0
            if up:
                self.y_vel = -speed
            if down:
                self.y_vel = speed
            if not (up or down):
                self.y_vel = 0

            self.eat += abs(self.x_vel)
            self.eat += abs(self.y_vel)
            if self.eat >= 1000:
                self.eat = 0
                self.hunger(1)
            self.rect.x += self.x_vel
            # проверяем что ни скем не столкнулись
            self.collide(self.x_vel, 0, platforms)
            # движемся по игрику
            self.rect.y += self.y_vel
            # проверяем что ни скем не столкнулись
            self.collide(0, self.y_vel, platforms)
            # отрисовываем анимацию
        else:
            if self.f:
                self.f = False
                self.rect.x += 5
        if enemy_platforms is not None:
            for elem in enemy_platforms.get_object():
                if collide_rect(self, elem):
                    elem.attack(self)
        self.draw()

    def get_coord(self):
        return self.rect.x, self.rect.y - 20

    def next_frame(self):
        self.count_next_frame += 1
        if (self.count_next_frame > 4 and not self.speed_boost) or (self.count_next_frame > 2 and self.speed_boost):
            self.count_next_frame = 0
            self.frame += 1

        if self.frame == len(self.frames_forward) - 1:
            self.frame = 0

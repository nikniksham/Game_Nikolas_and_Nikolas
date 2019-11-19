from MainClasss import *

SPEED = 2


class WithSomeone(Person):
    def __init__(self, image, coord, frames_forward, frames_back, frames_left, frames_right, name='Hog', armor=None):
        super().__init__(image, coord, 100, 100, 100, 100, name, frames_forward, frames_back, frames_left, frames_right,
                         armor=armor)

    def update(self, someone, platforms):
        self.x_vel, self.y_vel = 0, 0
        if get_gipotinuza((self.rect.x, self.rect.y), (someone.rect.x, someone.rect.y)) > 60:
            if self.get_coord()[0] > someone.get_coord()[0]:
                self.x_vel = -SPEED
            if self.get_coord()[0] < someone.get_coord()[0]:
                self.x_vel = SPEED
            if self.get_coord()[1] > someone.get_coord()[1]:
                self.y_vel = -SPEED
            if self.get_coord()[1] < someone.get_coord()[1]:
                self.y_vel = SPEED
        self.rect.x += self.x_vel
        self.collide(self.x_vel, 0, platforms)
        self.rect.y += self.y_vel
        self.collide(0, self.y_vel, platforms)
        self.coord = self.rect.x, self.rect.y
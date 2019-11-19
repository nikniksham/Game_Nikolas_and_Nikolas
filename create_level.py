from Chunk import *
from random import choice, random
from pygame import Rect


class Wall:
    def __init__(self, image, coord):
        self.image = image
        self.rect = Rect((coord[0], coord[1] + int(self.image.get_size()[1] - 30), self.image.get_size()[0], 30))
        self.coord = coord
        self.types = ['object', 'Image']

    def is_type(self, arg):
        return arg in self.types

    def get_image(self):
        return self.image

    def get_coord(self):
        return self.coord

    def get_coord_2(self):
        return self.rect.x, self.rect.y


def make_level(slow_key, slow, big_chunk_count=((0, 0), (1, 1))):
    # chunk_count количество чанков по горизионтали и вертикали
    # размер одного блока
    size = 30
    # частота создания блоков
    compresion = 0.01
    # список чанков с которыми объект может столкнуться
    walls_group = MainChunk()
    # список чанков на заднего фона
    bg_walls_group = MainChunk()
    # координаты по которым расположены чанки
    x, y = (big_chunk_count[0][0] * 7680, big_chunk_count[0][1] * 7680)
    # print(big_chunk_count, 'gg')
    for _ in range(big_chunk_count[0][1], big_chunk_count[1][1]):
        for _ in range(big_chunk_count[0][0], big_chunk_count[1][0]):
            big_chunk = BigChunk((x, y), (x + 7680, y + 7680))
            big_chunk_bg = BigChunk((x, y), (x + 7680, y + 7680))
            # print((x, y), (x + 7680, y + 7680))
            # стена на переднем плане с которой человек может столкнуться
            wall = False
            # создаём чанки
            # по игрику
            x_, y_ = x, y
            for _ in range(16):
                # по иксу
                for _1 in range(16):
                    # чанк объектов с которыми объект может столкнуться
                    chunk = Chunk((x_, y_), (x_ + 480, y_ + 480))
                    # чанк объектов на заднем фоне
                    chunk_bg = ChunkBG((x_, y_), (x_ + 480, y_ + 480))
                    key = ''
                    while not key.startswith('b'):
                        key = choice(slow_key)
                    bg_blocks, blocks, compresion = slow[key], slow['t' + key[1:]], slow['c' + key[1:]]
                    # координаты по которым создаются объекты для чанков
                    chunk_x, chunk_y = x_, y_
                    count = 0
                    add_count = 0
                    # создание объектов по игрику
                    for _ in range(16):
                        # создание объектов по игксу
                        for _ in range(16):
                            if compresion >= random():
                                count += 1
                                wall = Wall(choice(blocks).get_image(), (chunk_x, chunk_y))
                            wall_bg = Wall(choice(bg_blocks).get_image(), (chunk_x, chunk_y))
                            if wall:
                                add_count += 1
                                chunk.add_object(wall)
                            chunk_bg.add_object(wall_bg)
                            wall = False
                            # добавляем размер болка по иксу (сдивагаемся на один блок враво)
                            chunk_x += size
                        # переходим на новую строку изображений \n
                        # на одну строку вниз
                        chunk_y += size
                        # в начало ряда
                        chunk_x = x_
                    chunk.check_cilision()
                    chunk_bg.check_cilision()
                    # добавляем чанк в список чанков с которыми объект может столкнуться стену
                    big_chunk.add_chunk(chunk)
                    # добавляем чанк в список чанков заднего фона
                    big_chunk_bg.add_chunk(chunk_bg)
                    # передвигаемся на один чанк вправо
                    x_ += 480
                # переходим на новую строку чанков \т
                # в начало строки
                x_ = x
                # переходим на новую строку
                y_ += 480
            walls_group.add_chunk(big_chunk)
            bg_walls_group.add_chunk(big_chunk_bg)
            x += 7680
        x = 0
        y += 7680
    # возвращаем список список чанков с которыми объект может столкнуться и список чанков на заднего фона
    return walls_group, bg_walls_group

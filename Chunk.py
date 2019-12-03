from MainClasss import *
from pygame import Surface, Rect


class ChunkImage(Surface, Sprite):
    def __init__(self, surf, coord):
        Sprite.__init__(self)
        self.image = surf
        self.coord = coord
        self.layer = 0
        self.is_back_ground = False

    def set_bg(self, val: bool):
        self.is_back_ground = bool(val)

    def get_is_bg(self):
        return self.is_back_ground

    def set_layer(self, layer):
        self.layer = layer

    def get_layer(self):
        return self.layer

    def get_mask(self):
        return Wonderful(Rect(self.coord, self.image.get_size()))

    def get_image(self):
        return self.image

    def get_coord(self):
        return self.coord


class ChunkBG(Group):
    def __init__(self, coord_lu, coord_rd):
        super().__init__('sprite/blocks_sprites/Chunk.bmp')
        self.image = Surface((480, 480))
        # добавляем тип Chunk
        self.add_type('ChunkBG')
        # левая верхняя координата чанка
        self.coord_lu = coord_lu
        # левая нижняя координата чанка
        self.coord_ld = (coord_lu[0], coord_rd[1])
        # правая нижняя координата чанка
        self.coord_rd = coord_rd
        # правая верхняя координата чанка
        self.coord_ru = (coord_rd[0], coord_lu[1])

    def check_chunk(self, cam):
        # проверка того что чанк на экране
        # проверяем то что одна из четырёх крайних точек лежит между левой верхней и правой нижней точкой камеры
        # если одна из них на экране возвращаем истину если нет лож
        # берём координаты камеры
        coord_cam = cam.get_coord()
        # берём разрешение экрана
        size_cam = cam.get_size_screen()
        # вычисляем правую нижнюю координату камеры
        cam_rd = (coord_cam[0] + size_cam[0], coord_cam[1] + size_cam[1])
        # проверяем левую нижнюю координату
        if coord_cam[0] < self.coord_ld[0] < cam_rd[0] and coord_cam[1] < self.coord_ld[1] < cam_rd[1]:
            return True, False
        # правую нижнюю координату
        if coord_cam[0] < self.coord_rd[0] < cam_rd[0] and coord_cam[1] < self.coord_rd[1] < cam_rd[1]:
            return True, False
        # правую верхнюю координату
        if coord_cam[0] < self.coord_ru[0] < cam_rd[0] and coord_cam[1] < self.coord_ru[1] < cam_rd[1]:
            return True, False
            # проверяем левую нижнюю координату
        if coord_cam[0] < self.coord_lu[0] < cam_rd[0] and coord_cam[1] < self.coord_lu[1] < cam_rd[1]:
            return True, True
        # если не на экране то возвращаем лож
        return False, False

    def add_object(self, object):
        self.image.blit(object.image, (object.rect.x % 480, object.rect.y % 480))

    def check_cilision(self):
        coords = []
        for elem in self.objects:
            if elem.get_coord_2() in coords:
                self.objects.remove(elem)
            else:
                coords.append(elem.get_coord_2())

    def get_object(self, type=None):
        return ChunkImage(self.image, self.coord_lu)

    def __str__(self):
        return f'len: {len(self.objects)}'


class Chunk(Group):
    def __init__(self, coord_lu, coord_rd):
        super().__init__('sprite/blocks_sprites/Chunk.bmp')
        # добавляем тип Chunk
        self.add_type('Chunk')
        # левая верхняя координата чанка
        self.coord_lu = coord_lu
        # левая нижняя координата чанка
        self.coord_ld = (coord_lu[0], coord_rd[1])
        # правая нижняя координата чанка
        self.coord_rd = coord_rd
        # правая верхняя координата чанка
        self.coord_ru = (coord_rd[0], coord_lu[1])

    def check_chunk(self, cam):
        # проверка того что чанк на экране
        # проверяем то что одна из четырёх крайних точек лежит между левой верхней и правой нижней точкой камеры
        # если одна из них на экране возвращаем истину если нет лож
        # берём координаты камеры
        coord_cam = cam.get_coord()
        # берём разрешение экрана
        size_cam = cam.get_size_screen()
        # вычисляем правую нижнюю координату камеры
        cam_rd = (coord_cam[0] + size_cam[0], coord_cam[1] + size_cam[1])
        # проверяем левую нижнюю координату
        if coord_cam[0] < self.coord_ld[0] < cam_rd[0] and coord_cam[1] < self.coord_ld[1] < cam_rd[1]:
            return True, False
        # правую нижнюю координату
        if coord_cam[0] < self.coord_rd[0] < cam_rd[0] and coord_cam[1] < self.coord_rd[1] < cam_rd[1]:
            return True, False
        # правую верхнюю координату
        if coord_cam[0] < self.coord_ru[0] < cam_rd[0] and coord_cam[1] < self.coord_ru[1] < cam_rd[1]:
            return True, False
            # проверяем левую нижнюю координату
        if coord_cam[0] < self.coord_lu[0] < cam_rd[0] and coord_cam[1] < self.coord_lu[1] < cam_rd[1]:
            return True, True
        # если не на экране то возвращаем лож
        return False, False

    def add_object(self, object):
        self.objects.append(object)

    def check_cilision(self):
        coords = []
        for elem in self.objects:
            if elem.get_coord_2() in coords:
                self.objects.remove(elem)
            else:
                coords.append(elem.get_coord_2())

    def get_object(self, type=None):
        return self.objects

    def __str__(self):
        return f'len: {len(self.objects)}'


class BigChunk:
    def __init__(self, coord_lu, coord_rd):
        # левая верхняя координата чанка
        self.coord_lu = coord_lu
        # правая нижняя координата чанка
        self.coord_rd = coord_rd
        self.groups = []
        # список чанков
        self.chunks = []
        # список блоков
        self.res = []

    def check_chunk(self, cam):
        # проверка того что чанк на экране
        # проверяем то что одна из четырёх крайних точек лежит между левой верхней и правой нижней точкой камеры
        # если одна из них на экране возвращаем истину если нет лож
        # берём координаты камеры
        cam_lu = cam.get_coord()
        # берём разрешение экрана
        size_cam = cam.get_size_screen()
        # вычисляем правую нижнюю координату камеры
        cam_rd = (cam_lu[0] + size_cam[0], cam_lu[1] + size_cam[1])
        # cam_ru = (cam_rd[0], cam_lu[1])
        # cam_ld = (cam_lu[0], cam_rd[1])
        # проверяем левую нижнюю координату
        if self.coord_lu[0] < cam_lu[0] < self.coord_rd[0] and self.coord_lu[1] < cam_lu[1] < self.coord_rd[1]:
            #
            return True
        if self.coord_lu[0] < cam_rd[0] < self.coord_rd[0] and self.coord_lu[1] < cam_rd[1] < self.coord_rd[1]:
            #
            return True
        if self.coord_lu[0] < (cam_rd[0], cam_lu[1])[0] < self.coord_rd[0] and self.coord_lu[1] < (cam_rd[0], cam_lu[1])[1] < \
                self.coord_rd[1]:
            #
            return True
        if self.coord_lu[0] < (cam_lu[0], cam_rd[1])[0] < self.coord_rd[0] and self.coord_lu[1] < (cam_lu[0], cam_rd[1])[1] < \
                self.coord_rd[1]:
            #
            return True
        # если не на экране то возвращаем лож
        return False

    def add_chunk(self, chunk):
        self.chunks.append(chunk)

    def add_group(self, big_chunk):
        self.groups.append(big_chunk)

    def is_type(self, other):
        return bool(other)

    def get_object(self, screen=None):
        # если этот метод запустили не для проверки колизиии (пересечения)
        if screen is not None:
            # результат список изображений которые на сцене
            self.res = []
            # количество чанков которые выводятся
            count = 0
            # проходимся по чанкам из списка чанков
            for chunk in self.chunks:
                # проверяем то что чанк на экране
                if chunk.check_chunk(screen)[0]:
                    # добавляем 1 чанк который выводим на экран
                    count += 1
                    # добавляем в список избражений, изображения из чанка
                    chunk_ = chunk.get_object()
                    if chunk.is_type('ChunkBG'):
                        self.res.append(chunk_)

                    else:
                        self.res += chunk_
                    if chunk.check_chunk(screen)[1]:
                        return self.res
        # возвращаем список изображений которые на сцене
        return self.res

    def __str__(self):
        return f'len: {len(self.chunks)}'


class MainChunk(Object):
    def __init__(self):
        super().__init__('sprite/blocks_sprites/Chunk.bmp', (0, 0))
        # добавляем тип MainChunk
        self.add_type('MainChunk')
        # список чанков
        self.chunks = []
        # список блоков
        self.res = []

    def add_chunk(self, object):
        # добавляем чанк если он чанк
        if object.is_type('Chunk'):
            self.chunks.append(object)

    def get_object(self, screen=None):
        # если этот метод запустили не для проверки колизиии (пересечения)
        if screen is not None:
            # результат список изображений которые на сцене
            self.res = []
            # количество чанков которые выводятся
            # проходимся по чанкам из списка чанков
            for chunk in self.chunks:
                # проверяем то что чанк на экране
                if chunk.check_chunk(screen):
                    self.res += chunk.get_object(screen)
                    return self.res
        # возвращаем список изображений которые на сцене
        return self.res

    def __add__(self, other):
        self.chunks += other.chunks
        self.res += other.res
        return self

    def __str__(self):
        return f'len: {len(self.chunks)}'

    def __eq__(self, other):
        return self.chunks == other.chunks

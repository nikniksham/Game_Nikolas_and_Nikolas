import pygame
import random
from pygame.sprite import Sprite, collide_rect
from pygame import image, Rect
import math

# в этом файле реализуется логика взаимодействия объектов между собой
# убедительна просьба прочитать инструкцию перед написанием классов чтобы всем было удобнее
# 1) при создании класса вы наследуете свой класс от одного из этих классов
# это делается так
# class(класс от колторого вы наследуетесь):
# 2) первая строчка в __init__: super().__init__(атрибуты класса родителя)
# 3) вторая строчка self.add_type("название вашего класса") это нужно для того чтобы другие клаасы могли понимать что
# это за класс
# 4) перед написанием класса ознакомиться с иерархией и методами классов родитетелей (чтобы не написать несколько
# одинаковых методов)
# 5) это основной файл игры поэтому перед каждой строчкой должен быть коментарий
# # коментарий поясняющий работу следущей строки
# строка с кодом
# 6) проверять все аргументы на пренадлежность нужному типу будь то строка, число, дробь, или класс из этого или
# другого файла
# это делается так:
# object.is_type("тип объекта")  # проверяет то что класс написаный для игры является наследником или сам является этим
# классом
# type(object) возвращает Название класса, например: int, str, float
# 7) просьба написать инструкцию для вашего класса в файле class.py по образу и подобию написания инструкций тех классов
# спасибо что прочитали инструкцию!
# Пожалуйста O_o


def load_data():
    global ID
    global message
    message = False
    ID = [0]


def get_gipotinuza(coord_1, coord_2):
    kat_1 = abs(coord_1[0] - coord_2[0])
    kat_2 = abs(coord_1[1] - coord_2[1])
    gip = (kat_1 ** 2 + kat_2 ** 2) ** 0.5
    return gip


load_data()


class Wonderful:
    def __init__(self, rect):
        self.rect = rect

    def get_rect(self):
        return self.rect


class MainObject:
    def __init__(self):
        self.types = ['MainObject']

    def get_types(self):
        # получить типы
        return self.types

    def is_type(self, type):
        # проверить явлыется ли объект наследником даного типа
        return type in self.types

    def add_type(self, type):
        # добавить тип
        self.types.append(type)


class Image(MainObject, Sprite):
    def __init__(self, filename, transpote_color=(255, 255, 255), coord=(0, 0), size=None):
        super().__init__()
        Sprite.__init__(self)
        # добавляем тип Image
        self.add_type('Image')
        # загружаем изображение
        self.image = image.load(filename).convert()
        # прямоугольник координат и размера rect
        self.coord = coord
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = coord
        self.image.set_colorkey(transpote_color)
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

    def set_coord(self, coord):
        self.coord = coord
        return self

    def get_size(self):
        # возвращаем размер изобрадения
        return self.image.get_size()

    def get_image(self):
        # возвращаем изображение
        return self.image

    def get_coord(self):
        # возвращает rect с координатами и размером объекта
        return self.coord

    def get_rect(self):
        # возвращает прямоугольник объекта
        return self.rect


class Object(Image):
    def __init__(self, image, coord, size=None, transpote_color=(255, 255, 255)):
        if type(image) == str:
            super().__init__(image, transpote_color, coord, size)
        else:
            MainObject.__init__(self)
            self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = coord[0]
        self.rect.y = coord[1]
        # размер одной клетки на карте
        self.size_block = 30
        # добавляем в список типов тип Object
        self.add_type('Object')
        # список групп в которых состаит объект
        self.groups = []

    def add_group(self, group):
        # возвращает истину если группа добавлена и лож если не добавлена
        # добавление объекта в группу
        # проверяем что наследник класса Group
        if group.is_type('Group'):
            # если наследник класса то добаляем в список груп
            self.groups.append(group)
            return True
        else:
            # если не наследник класса Group возвращаем лож и не добавляем в список
            return False

    def get_group(self):
        # возвращаем список групп
        return self.groups

    def in_group(self, group):
        # возваращаем истину если состоит в группе лож если не состаит в группе
        return group in self.groups

    def remove_group(self, group):
        # если группа удалена из списка груп возвращается истина в обратном случае лож
        if self.in_group(group):
            # удаляем группу из списка групп и возвращаем истину
            self.groups.remove(group)
            return True
        else:
            # если элемента нет в списке групп то возвращаем лож
            return False


class Group(Object):
    def __init__(self, image, objects=[]):
        super().__init__(image, (0, 0))
        self.add_type('Group')
        # создаём список объектов в группе
        self.create_group(objects)
        # добавляем в список типов тип Group

    def create_group(self, objects):
        # список в котором хранятся все элементы группы
        self.objects = []
        # проходимся по объектам из списка объектов
        for object in objects:
            # пытаемся добавить объект в группу
            self.add_object(object)

    def get_object(self, type=None):
        # создаём список в каторый сохраним результат
        res_group = []
        # если есть фильтр
        if type is not None:
            for object in self.objects:
                # если объект подходит под условия
                if object.is_type(type):
                    # то дабовляем его в группу иначе пропускаем элемент
                    res_group.append(object)
        else:
            # иначе добавляем все объекты в res_group
            for object in self.objects:
                res_group.append(object)
        # возвращаем результат
        return res_group

    def add_object(self, object):
        # возвращает истину если объект добавен лож если нет
        if object.is_type('Object'):
            self.objects.append(object)
            object.add_group(self)
            return True
        else:
            return False

    def remove(self, object):
        # удалить объект из группы
        # пример объект сам удаляется из группы передав self
        # проверяем находится ли объект в группе
        if object in self.objects:
            # если get_coord() объект в группе то удаляем его из группы
            self.objects.remove(object)
            # и удаляем из списка групп в которых он состаит эту группу
            object.remove_group(self)
            return True
        return False

    def __str__(self):
        return f'Group: {self.get_group()}'


class Level(Group):
    def __init__(self, image, name, size_level, objects=[]):
        self.main_chunks = []
        super().__init__(image, objects)
        # добавляем тип: Level
        self.add_type('Level')
        # название сцены
        self.name = name
        # размер угровня
        self.size_level = size_level
        self.main_hero = self

    def add_main_chunk(self, main_chunk):
        # если объект типа МainChunk то он нам подходит возвращаем истину в противоположном случае лож
        if main_chunk.is_type('MainChunk'):
            self.main_chunks.append(main_chunk)
            return True
        return False

    def remove_main_chunk(self, main_chunk):
        # удаляем объект из группы если он в группе и возвращаем истину в ином случае лож
        if main_chunk in self.main_chunks:
            self.main_chunks.remove(main_chunk)
            return True
        return False

    def get_main_chunks(self, screen):
        # получить изображения из чанков которые на экране
        # список результата
        res = []
        # проходимся по основным чанкам и находим изображения которые надо вывести
        for chunk in self.main_chunks:
            # добавляем в список результата объекты которые находятся на сцене
            res += chunk.get_object(screen)
        # возвращаем результат
        return res

    def get_object(self, type=None):
        # создаём список в который сохраняем результат
        res_group = []
        # проходимся по группам из списка групп
        for group in self.get_group():
            # добавляем в результат элементы списка группы
            res_group += group.get_object(type)
        # возвращаем результат
        # проверяем есть фильтр или нет
        if type is not None:
            # добавляем объект в результат если он подходит
            for object in self.objects:
                # проверяем является ли объект наследником данного класса
                if object.is_type(type):
                    res_group.append(object)
        else:
            # добавляем все объекты в сисок результата
            for object in self.objects:
                res_group.append(object)
        return res_group

    def set_main_hero(self, object):
        # если получилось установить главного героя возвращает истину если не получилось лож
        # проверяем что объект наследник класса Object
        if object.is_type('Object'):
            # если объект подходит то задаём его главным гереом
            self.main_hero = object
            return True
        return False

    def get_main_hero(self):
        # возвращаем главного героя сцены
        return self.main_hero


class Camera(MainObject):
    def __init__(self, size_screen, bg_color, border_map=(None, None, None, None)):
        super().__init__()
        # создаём таймер
        self.clock = pygame.time.Clock()
        # кортеж границ сцены None если с этой стороны нет границы
        self.border_map = border_map
        # добавляем тип Camera
        self.add_type('Camera')
        # размер экрана
        self.size_screen = size_screen
        # цвет заднего фона
        self.bg_color = bg_color
        # создаём экран
        pygame.init()
        self.screen = pygame.display.set_mode(self.size_screen, pygame.FULLSCREEN)
        # координаты левого верхнего угла
        self.coord = (0, 0)

    def get_size_screen(self):
        # получить размер экрана
        return self.size_screen

    def get_coord(self):
        # получить координаты левой верхней по которым расположен экран
        return self.coord

    def get_screen(self):
        # возвращает экран
        return self.screen

    def get_screen_coord(self, main_hero_coord):
        # находим левый верхний угол экрана при данном положении главного героя
        self.coord = [main_hero_coord[0] - self.size_screen[0] // 2, main_hero_coord[1] - self.size_screen[1] // 2]
        # проверяем границу сверху
        if self.border_map[0] is not None:
            if self.coord[1] < self.border_map[0]:
                self.coord[1] = self.border_map[0]
        # проверяем границу снизу
        if self.border_map[1] is not None:
            if self.coord[1] > self.border_map[1] - self.size_screen[1]:
                self.coord[1] = self.border_map[1] - self.size_screen[1]
        # проверяем границу слева
        if self.border_map[2] is not None:
            if self.coord[0] < self.border_map[2]:
                self.coord[0] = self.border_map[2]
        # проверяем границу справа
        if self.border_map[3] is not None:
            if self.coord[0] > self.border_map[3] - self.size_screen[0]:
                self.coord[0] = self.border_map[3] - self.size_screen[0]

    def create(self):
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

    def object_coord(self, rect):
        # вычисляем координаты на экране относительно персонажа
        return rect[0] - self.coord[0], rect[1] - self.coord[1]

    def draw_interface(self, hp, hp_person, food_person, coord):
        hp_coord = coord[0]
        food_coord = coord[1]
        self.screen.blit(hp.get_image(), hp_coord)
        self.screen.blit(hp.get_image(), food_coord)
        x_t = 280 * (food_person[0] / food_person[1])
        x_b = x_t + 20
        pygame.draw.polygon(self.screen, (174, 108, 72), ((food_coord[0] + 2, food_coord[1] + 2),
                                                       (food_coord[0] + x_t, food_coord[1] + 2),
                                                       (food_coord[0] + x_b - 2, food_coord[1] + 41),
                                                       (food_coord[0] + 20, food_coord[1] + 42)))
        if hp_person[0] > 0:
            x_t = 280 * (hp_person[0] / hp_person[1])
            x_b = x_t + 20
            pygame.draw.polygon(self.screen, (255, 0, 0), ((hp_coord[0] + 2, hp_coord[1] + 2),
                                                           (hp_coord[0] + x_t, hp_coord[1] + 2),
                                                           (hp_coord[0] + x_b - 2, hp_coord[1] + 41),
                                                           (hp_coord[0] + 20, hp_coord[1] + 42)))

    def draw(self, level):
        # заливаем экран цветом заднего фона
        self.screen.fill(self.bg_color)
        # находим левый верхний угол экрана при данном положении главного героя
        self.get_screen_coord(level.get_main_hero().get_rect())
        # количетсво элементов
        count = 0
        layer = {}
        # выводим объекты из чанков
        for object in level.get_main_chunks(self):
            if str(type(object)) == '<class \'Chunk.ChunkImage\'>':
                # количетсво объектов на 1 обльше
                count += 1
                # выводим на экран объект
                self.screen.blit(object.get_image(), self.object_coord(object.get_coord()))
        # проходимся по объектам не сцене
        for object in level.get_object():
            # количетсво объектов на 1 обльше
            # и выводим из на дисплей отнасительно главного героя
            if object.get_is_bg():
                self.screen.blit(object.get_image(), self.object_coord(object.get_coord()))
            else:
                if object.get_layer() in layer:
                    layer[object.get_layer()].append(object)
                else:
                    layer[object.get_layer()] = [object]
        for object in level.get_main_chunks(self):
            if str(type(object)) != '<class \'Chunk.ChunkImage\'>':
                # количетсво объектов на 1 обльше
                count += 1
                # выводим на экран объект
                if object.get_is_bg():
                    self.screen.blit(object.get_image(), self.object_coord(object.get_coord()))
                else:
                    if object.get_layer() in layer:
                        layer[object.get_layer()].append(object)
                    else:
                        layer[object.get_layer()] = [object]
        layers = list(layer.keys())
        layers.sort()
        for key in layers:
            for object in layer[key]:
                self.screen.blit(object.get_image(), self.object_coord(object.get_coord()))
        # обнавляем экран
        # poop = draw.circle(self.screen, (255, 0, 0), (self.size_screen[0] // 2, self.size_screen[1] // 2), 15)
        # line_1 = draw.line(self.screen, (0, 0, 0), (0, 0), (self.size_screen[0], self.size_screen[1]), 5)
        # line_2 = draw.line(self.screen, (0, 0, 0), (self.size_screen[0], 0), (0, self.size_screen[1]), 5)
        # заголовк программы количество кадров в секунду и количество предметов на сцене
        pygame.display.set_caption(f'FPS: {self.clock.get_fps()}, Item on scene: {count}, {len(level.get_object())}, Coord: {level.get_main_hero().get_rect()}')
        # обнавляем экран
        # ограничиваем количество кадров в секунду до 120
        self.clock.tick(60)


class Item(Object):
    def __init__(self, image, coord, name, max_count, size=None, info='', count=0):
        super().__init__(image, coord, size)
        global ID
        self.add_type('Item')
        # максимальное количество предметов данного типа
        self.max_count = max_count
        # количество объектов данного типа
        self.count = count
        # создаём ID
        self.ID = ID[-1] + 1
        ID.append(self.ID)
        # задаём информацию об объекте
        self.info_object = info
        # задаём имя объекта
        self.name = name

    def get_count(self):
        # возвращает количество предметов данного типа
        return self.count

    def add_count(self, item):
        # складываем предметы
        # проверяем то что другой объект точно такогоже типа как и этот предмет
        if item.is_type(self.get_types()[-1]):
            # добавляем в этот объект тот объект
            self.count += item.get_count()
            # если количество предмета получилось больше его максимального количества
            if self.count > self.max_count:
                # устанавливаем количество предметов остаток который не влез в этот предмет
                item.set_count(self.count - self.max_count)
                # устанавливаем количество предметов на максимальный уровень
                self.set_count(self.max_count)
            else:
                # устанавливаем другомы предмету количество равное 0
                item.set_count(0)

    def set_count(self, count):
        # низкоуровневая функция
        # используется для задания количества предметов объекта
        self.count = count

    def set_info(self, info):
        # возвращает истину если получилось лож если нет
        if type(info) == str:
            self.info_object = info
            return True
        return False

    def info(self):
        # возвращает информацию об объекте
        return self.info_object

    def get_name(self):
        # возвращает имя объекта
        return self.name


# исправил на:
# self.armor += upgrade_point
# всегда в клаасах пиши
# self.add_type('Armor') всесто армор мазвание класса
# чем отличается:
# self.armor = armor
# от
# self.armor_heal_point = armor_hp
# и что такое и чем отличается
# self.armor - bool, int, str?
class Armor(Item):
    def __init__(self, image, coord, name, max_count, armor, armor_hp, armor_max_hp, size=None, info=''):
        # тип объекта: Armor
        # Я исправил heat_point на heal_point, тк heat_point переводится как: 'тепловая точка'
        super().__init__(image, coord, name, max_count, size, info)
        self.add_type('Armor')
        #  параметр: защита
        self.armor = armor
        #  параметр: максимальное здоровье брони
        self.armor_max_heal_point = armor_max_hp
        # параметр: здоровье брони
        self.armor_heal_point = armor_hp

    def get_armor(self):
        # возвращает защиту
        return self.armor

    def armor_upgrade(self, upgrade_point):
        # улучшает защиту, пример: ты пошёл к механику, он улучшил тебе броню, добавил очки защиты
        if type(upgrade_point) == int:
            self.armor_max_heal_point += upgrade_point
            self.armor += upgrade_point

    def armor_downgrade(self, downgrade_point):
        # ухудшает защиту, пример: ты снял улучшение, у тебя убавились очки защиты
        if type(downgrade_point) == int:
            self.armor_max_heal_point -= downgrade_point
            if self.armor > self.armor_max_heal_point:
                self.armor = self.armor_max_heal_point

    def get_armor_hp(self):
        # возвращяет здороье бронижелета
        return self.armor_heal_point

    def armor_damage(self, damage):
        # ломает бронижелет на N очков
        # проверка на то что damage число
        if type(damage) == float:
            damage = int
        if type(damage) == int:
            # нанесёный урон не может опустить уровень жизней ниже нуля
            if self.armor_heal_point - damage > 0:
                self.armor_heal_point -= damage
            else:
                self.armor_heal_point = 0

    def armor_repair(self, repair_point):
        # чинит бронижелет на N очков, но не больше, чем максимальное здоровье
        if self.armor_heal_point + repair_point > self.armor_max_heal_point:
            self.armor_heal_point = self.armor_max_heal_point
        else:
            self.armor_heal_point += repair_point


class Bullet(Item):
    def __init__(self, image, coord, name, max_count, type_bullet, size=None, info=''):
        super().__init__(image, coord, name, max_count, size, info)
        # добавляем тип: Bullet
        self.list_bullet = []
        self.add_type('Bullet')
        self.bullets = False
        self.type_bullet = type_bullet

    def get_type_bullet(self):
        # возвращает тип снаряда
        return self.type_bullet

    def spawn_bullet(self, x_vel, y_vel, bullet, x, y):
        self.bullets = True
        self.list_bullet.append([[x_vel, y_vel], [x, y], bullet])

    def collide_bullet(self, bullet_list, list_heal_point_obj):
        for bullet in bullet_list:
            for object in list_heal_point_obj:
                pass

    def draw_bullet(self, screen):
        for bullet in self.list_bullet:
            coord_bullet = bullet[1]
            motion_bullet = bullet[0]
            image_bullet = bullet[2].get_image()
            coord_bullet[0] += motion_bullet[0]
            coord_bullet[1] += motion_bullet[1]
            screen.blit(image_bullet, coord_bullet)


class Weapon(Bullet):
    def __init__(self, image, coord, name, max_count, type_bullet, type_damage, attack_radius,
                 range_damage, attack_speed, accuracy, owner, size=None, info=''):
        # тип объекта: Weapon
        super().__init__(image, coord, name, max_count, type_bullet, size, info)
        self.add_type('Weapon')
        # типы урона: knife, firearm, missile, ret_damage
        self.type_damage = type_damage
        # Дальность атаки
        self.attack_radius = attack_radius
        # кортеж из чисел (минимальный урон, максимальный урон)
        self.range_damage = range_damage
        # скорость атаки
        self.attack_speed = attack_speed
        # точность оружия
        self.accuracy = accuracy
        # Владелец
        self.owner = owner

    def get_bullet_count(self):
        # идём в инвентарь берём патроны и возвращаем количество патронов нужного типа
        pass

    def damage(self, enemy):
        global message
        # Вроде сделал, и всё понятно, глянь комменты, если что-то не понятно (если что-то не понял до сих пор,
        # то напиши в лс, или позвони)
        # урон, броня равныы нулю
        damage, armor_damage = 0, 0
        # проверяем ТО ЧТО ЕСЛИ мы нанесём урон игра не крашнется!!
        if enemy.is_type('MovingObject'):
            # проверяем радиус стрельбы через гипотинузу двух катетов
            if get_gipotinuza(self.owner.get_coord(), enemy.get_coord()) <= self.attack_radius:
                # вычисляем урон (в радиусе от минимального урона до максимального)
                damage = random.choice(range(self.range_damage[0], self.range_damage[1] + 1))
                # проверяем то что у врага есть юроня
                if enemy.get_armor() is not None:
                    # Проверка на то, что броня не полность сломана
                    if enemy.get_armor_hp() > 0:
                        # Проверка на то, что урон больше защиты
                        if damage > enemy.get_armor():
                            # нанесение урона
                            enemy.damage(int(damage - enemy.get_armor()))
                            # если кол-во хп ниже 0, то присваивается 0
                            if enemy.get_hp() < 0:
                                enemy.set_hp(0)
                            # вычисляем урон нанесёный от брони
                            armor_damage = damage / 10
                            # наносим урон дране
                            enemy.armor_damage(armor_damage)
                            # если броня сломана выводим сообщение
                            if enemy.get_armor_hp() <= 0:
                                print(f'Броня {enemy.get_name()} сломалась')
                else:
                    # наносим полный урон
                    enemy.damage(int(damage))
            # уведомлания для отладки
            if message:
                print(f'{self.owner.get_name} нанёс {enemy.get_name} {damage} урона, теперь его здоровье равно '
                      f'{enemy.get_hp}')
                if enemy.get_armor_hp > 0:
                    print(f'Броня поломалась на {armor_damage}, теперь её здоровье равно {enemy.get_armor_hp}')
        # если у объекта не может быть брани в приципе то наносим просто урон
        elif enemy.is_type('HealPointObject'):
            # наносим полный урон
            enemy.damage(int(damage))

    def flight_path(self, mouse_pos, hero_pos):
        x, y = hero_pos
        m_x, m_y = mouse_pos
        rad = math.atan2(m_y - y, m_x - x)
        sin = math.sin(rad)
        cos = math.cos(rad)
        return sin, cos

    def get_accuracy(self):
        # возвращает точность оружия (десятичное число, самая лучшая точность ---> 1.0)
        return self.accuracy


class HealPointObject(Object):
    def __init__(self, image, coord, hp, max_heal_point, size=None):
        # объект типа: HealPointObject
        # print(image, coord, size)
        super().__init__(image, coord, size)
        self.add_type('HealPointObject')
        # максимальное количество жизней
        self.max_heal_point = max_heal_point
        # количество жизней
        self.heal_point = hp

    def get_hp(self):
        # возвращает кол-во хп
        return self.heal_point

    def get_max_hp(self):
        return self.max_heal_point

    def damage(self, damage):
        # наносит урон игроку (уменьшает запас хп)
        if damage > self.heal_point:
            self.heal_point = 0
        else:
            self.heal_point -= damage

    def heal(self, heal_point):
        # восстанавливает количесто хп, но не больше max_heal_point
        if int(heal_point) == int:
            if self.heal_point + heal_point > self.max_heal_point:
                self.heal_point = self.max_heal_point
            else:
                self.heal_point += heal_point

    def set_hp(self, number):
        # изменяет число хп на number
        if type(number) == int:
            self.heal_point = number

    def heal_point_upgrade(self, upgrade_point):
        # увеличевает кол-во хп у персонажа, например:  у персонажа повысился уровень, вырасло максимальное кол-во хп
        if type(upgrade_point) == int:
            self.max_heal_point += upgrade_point
            self.heal_point = self.max_heal_point

    def heal_point_downgrade(self, downgrade_point):
        # у персонажа уменьшилось макимальное кол-во хп, например: он устал, максимальное кол-во хп уменьшено
        if type(downgrade_point) == int:
            self.max_heal_point -= downgrade_point
            if self.heal_point > self.max_heal_point:
                self.heal_point = self.max_heal_point
            # self.heal_point -= downgrade_point


class MovingObject(HealPointObject):
    def __init__(self, image, coord, hp, max_heal_point, armor, food, max_food_point, size=None):
        # тип объекта: MovingObject
        super().__init__(image, coord, hp, max_heal_point, size)
        self.add_type('MovingObject')
        # очки еды
        self.food = food
        # максимальное количество еды
        self.max_food_point = max_food_point
        # это делается так
        if armor is not None and armor.is_type('Armor'):
            self.armor = armor
        else:
            self.armor = None
        # столкновение с одной из сторон
        self.collision_x_site = 0
        self.collision_y_site = 0
        self.x_vel = 0
        self.y_vel = 0
        # В self.armor записывается объект типа armor (класс находится выше)
        # объект у которого есть броня и голод

    def get_food(self):
        # возвращает уровень еды
        return self.food

    def get_max_food(self):
        return self.max_food_point

    def eat(self, food_point):
        # персонаж употребляет что-то, что восстанавливает уровень еды, но не больше, чем self.max_food_point
        if self.food + food_point > self.max_food_point:
            self.food = self.max_food_point
        else:
            self.food += food_point

    def set_food(self, n):
        self.food = n

    def hunger(self, n):
        self.food -= n

    def get_armor(self):
        # получить броню объекта может быть None
        return self.armor

    def collide(self, x_vel, y_vel, platforms):
        # проверка столкновения
        # если скорость по горизонту не равна нулю
        if x_vel != 0:
            # столкновений по оси икс нет
            self.collision_x_site = 0
        # если скорость по оси игрик не равна нулю
        elif y_vel != 0:
            # столкновений по оси игрик нет
            self.collision_y_site = 0
        # проходимся по списку стен с которыми можем столкнуться
        for pl in platforms.get_object():
            # если столкнулись
            if collide_rect(self, pl):
                # если скорость по оси икс больше 0
                if x_vel > 0:
                    # правая сторона равна левой строне объекта с которым мы столкнулись
                    self.rect.right = pl.rect.left
                    # столкновение справа
                    self.collision_x_site = 2
                # если скорость по оси икс меньше 0
                elif x_vel < 0:
                    # левая сторона объекта равна правой стороне объекта
                    self.rect.left = pl.rect.right
                    # столкновение слева
                    self.collision_x_site = 1
                # если скорость по оси игрик больше 0
                elif y_vel > 0:
                    # низ объекта равен верху объекта с которым чтолкнулись
                    self.rect.bottom = pl.rect.top
                    # столкновение снизу
                    self.collision_y_site = 2
                # если скорость по оси игрик меньше 0
                elif y_vel < 0:
                    # верх объекта равен инзу объекта с котрым столкнулись
                    self.rect.top = pl.rect.bottom
                    # столкновение сверху
                    self.collision_y_site = 1
            rect = self.rect
            self.rect = self.get_rect()
            if collide_rect(self, pl.get_mask()):
                if self.rect.bottom < pl.get_mask().rect.bottom:
                    self.set_layer(pl.get_layer() - 1)
                else:
                    pl.set_layer(self.get_layer() - 1)
            self.rect = rect


class AnimationObject(MovingObject):
    def __init__(self, images, coord, hp, max_heal_point, food, max_food_point, frames_forward, frames_back,
                 frames_left,
                 frames_right, size=None, armor=None):
        self.die_f = False
        super().__init__(images, coord, hp, max_heal_point, armor, food, max_food_point, size)
        self.add_type('AnimationObject')
        self.die_frames = []
        self.eat = 0
        self.die_frame = 0
        self.count_die_frames = 0
        # столкновение с одной из сторон
        self.collision_x_site = 0
        self.collision_y_site = 0
        # ускорение на одной из сторон
        self.x_vel = 0
        self.y_vel = 0

        # sites moving lists
        self.count_next_frame = 0
        self.frame = 0
        self.frames_forward = []
        self.frames_back = []
        self.frames_left = []
        self.frames_right = []

        # ускорение объекта (бег)
        self.speed_boost = False
        # downloading sprites
        # изображения ходьбы вверх
        for frame in frames_forward:
            self.frames_forward.append(Image('sprite/person_sprites/' + frame))
        # изображения ходьбы вниз
        for frame in frames_back:
            self.frames_back.append(Image('sprite/person_sprites/' + frame))
        # изобрадения ходьбы влево
        for frame in frames_left:
            self.frames_left.append(Image('sprite/person_sprites/' + frame))
        # избражения ходьбы вправо
        for frame in frames_right:
            self.frames_right.append(Image('sprite/person_sprites/' + frame))

    def die(self, filename, die_frames):
        self.die_f = True
        for elem in die_frames[0]:
            self.die_frames.append(Object(filename + elem, (120, 120)))

    def draw(self):
        # если не столкнулись справа и ускарение направлено вправо
        if self.die_f is False:
            if self.x_vel == 0 and self.y_vel == 0:
                self.image = self.frames_forward[0].get_image()
            elif self.x_vel > 0 and not self.collision_x_site == 2:
                # переключаем на следующий кадр анимации ходьбы вправо
                self.image = self.frames_right[self.frame].get_image()
            # если не столкнулись слева и ускарение направлено влево
            elif self.x_vel < 0 and not self.collision_x_site == 1:
                # переключаем на следующий кадр анимации ходьбы влево
                self.image = self.frames_left[self.frame].get_image()
            # если не столкнулись снизу и ускарение направлено вниз
            elif self.y_vel > 0 and not self.collision_y_site == 2:
                # переключаем на следующий кадр анимации ходьбы вниз
                self.image = self.frames_forward[self.frame].get_image()
            # если не столкнулись сверху и скарение направлени вверх
            elif self.y_vel < 0 and not self.collision_y_site == 1:
                # переключаем на следующий кадр анимации ходьбы вверх
                self.image = self.frames_back[self.frame].get_image()
            # столкнулись слева
            elif self.collision_x_site == 1:
                # смотрим в стену слева
                self.image = self.frames_left[0].get_image()
            # если не столкнулись справа
            elif self.collision_x_site == 2:
                # смотрим в стенку справ
                self.image = self.frames_right[0].get_image()
            # если не столкнулись снизу
            elif self.collision_y_site == 2:
                # смотрим вниз
                self.image = self.frames_forward[0].get_image()
            # если не столкнулись сверху
            elif self.collision_y_site == 1:
                # то смотрим вверх
                self.image = self.frames_back[0].get_image()
            # переключиться на следующий кадр
            self.next_frame()
        else:
            self.image = self.die_frames[self.die_frame].get_image()
            self.next_die_frame()

    def resurrection(self):
        self.die_f = False
        self.set_food(self.get_max_food())
        self.die_frame = 0
        self.count_die_frames = 0
        self.set_hp(self.get_max_hp())
        self.rect.x, self.rect.y = (15, 15)

    def get_die(self):
        return self.die_f

    def next_die_frame(self):
        self.count_die_frames += 1
        if self.count_die_frames > 8 and self.die_frame < 9:
            self.count_die_frames = 0
            self.die_frame += 1

    def next_frame(self):
        # то как мы переключаем кадра в зависимости от типа перемещения
        # если бежим то быстрее если идём то медленее
        self.count_next_frame += 1
        if (self.count_next_frame > 4 and not self.speed_boost) or (self.count_next_frame > 2 and self.speed_boost):
            self.count_next_frame = 0
            self.frame += 1

        # если включён последний кадр перематываем в начало
        if self.frame == len(self.frames_forward) - 1:
            # устанавливаем первый кадр
            self.frame = 0


class Person(AnimationObject):
    def __init__(self, image, coord, hp, max_heal_point, food, max_food_point, name, frames_forward, frames_back,
                 frames_left, frames_right, size=None, armor=None):
        # тип объекта: Person
        super().__init__(image, coord, hp, max_heal_point, food, max_food_point, frames_forward, frames_back,
                         frames_left, frames_right, size)
        self.add_type('Person')
        self.name = name
        # имя персонажа

    def get_name(self):
        # возвращает имя персонажа
        return self.name

    def set_name(self, new_name):
        # меняет имя персонажа
        if type(new_name) == str:
            self.name = new_name


class Eat(Item):
    def __init__(self, image, coord, name, max_count, hp, food, owner, armor=0, size=None, info=''):
        # объект типа: Eat
        super().__init__(image, coord, name, max_count, size, info)
        self.add_type('Eat')
        self.heal_point = hp
        self.armor = armor
        self.food = food
        # количество жизней, брони, голода которые он востанавливает (уменьшает)
        self.owner = owner
        # владелец еды

    def use(self):
        # поесть
        self.owner.eat(self.food)
        if self.heal_point >= 0:
            self.owner.heal(self.heal_point)
        else:
            self.owner.damage(abs(self.heal_point))
        if self.armor > 0:
            self.owner.armor.repair(self.armor)
        elif self.armor < 0:
            self.owner.armor.damage(abs(self.armor))


class EnemyBlock(Object):
    def __init__(self, filename, coord, damag, negative_effect=None):
        super().__init__(filename, coord)
        self.damag = damag
        self.add_type('enemy_spike')
        self.negative_effect = negative_effect
        self.coord = coord
        self.set_bg(True)


    def attack(self, enemy):
        enemy.damage(self.damag)


class ImageButton(Object):
    def __init__(self, images, coord):
        super().__init__(images, coord)
        self.coord = coord
        self.rect.x, self.rect.y = self.coord

    def draw(self, action, screen, f=None):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        screen.blit(self.image, self.coord)
        if self.coord[0] <= mouse[0] <= self.coord[0] + self.image.get_size()[0] \
                and self.coord[1] <= mouse[1] <= self.coord[1] + self.image.get_size()[1] and click[0] == 1:
            if f is not None:
                action(screen)
            else:
                action()
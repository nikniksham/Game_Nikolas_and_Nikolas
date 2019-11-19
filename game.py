from create_level import *
from player import Player
from win32api import GetSystemMetrics
# from NPS import *
from MainClasss import *
from multiprocessing.pool import ThreadPool
from NPS_scripts import *
from TestWeapon import *

pool_1 = ThreadPool(processes=1)
pool_2 = ThreadPool(processes=1)

# загружаем нужные переменные
load_data()
# создание нужных переменных
# размер одного бока
size = 30
# берйм ваше разрешение вашего экрана
# size_screen = (GetSystemMetrics(0), GetSystemMetrics(1))

size_screen = (1920, 1080)

# 1 чанк 16 на 16 картинок
# 1 чанк 480 на 480 пикселей
# 1 картинка 30 на 30 пикселей
# размер каты в чанках
chunk_count = ((0, 0), (1, 1))
# size_screen = (1080, 720)

# camera
camera = Camera(size_screen, (0, 0, 0),
                border_map=(
                    -200, chunk_count[1][1] * 16 * 16 * size + 1000, -200, chunk_count[1][0] * 16 * 16 * size + 1000))

# walls
# создаём задний фон и объекты на переднем плане
# словарь картинок
slow = {'bn': [Image('sprite/blocks_sprites/back_1.bmp'), Image('sprite/blocks_sprites/block_3.bmp'),
               Image('sprite/blocks_sprites/back_2.bmp'), Image('sprite/blocks_sprites/back_4.bmp')],
        'tn': [Image('sprite/blocks_sprites/tree.bmp'), Image('sprite/blocks_sprites/tree_1.bmp'),
               Image('sprite/blocks_sprites/stone_2.bmp')],
        'cn': 0.1,
        'bs': [Image('sprite/blocks_sprites/sand_1.bmp')],
        'ts': [Image('sprite/blocks_sprites/stone_1.bmp')],
        'cs': 0.01}

if chunk_count == ((0,), (1, 1)):
    print(f'2 core creating')
    chunk_count_1 = (chunk_count[0], (chunk_count[1][0], chunk_count[1][1] // 2))
    chunk_count_2 = ((chunk_count[1][0], chunk_count[1][1] // 2), chunk_count[1])
    print(chunk_count_1, chunk_count_2, 'gff')

    # start threads
    async_result = pool_1.apply_async(make_level, (list(slow.keys()), slow, chunk_count_1))
    async_result_1 = pool_2.apply_async(make_level, (list(slow.keys()), slow, chunk_count_2))
    # join threads to the main thread
    walls_group, bg_group = async_result.get()
    walls_group_1, bg_group_1 = async_result_1.get()
    print(walls_group_1, bg_group_1, walls_group == bg_group, walls_group == walls_group_1)
    print(len(walls_group.chunks), 'l')
    walls_group = walls_group + walls_group_1
    print(len(walls_group.chunks), 'll')
    print(len(bg_group.chunks), 'lll')
    bg_group = bg_group + bg_group_1
    print(bg_group)
    print(len(bg_group.chunks), 'llll')
    print(type(walls_group))
else:
    walls_group, bg_group = make_level(list(slow.keys()), slow, chunk_count)
    # print(walls_group, bg_group)
# создание героя

# картинки в для анимаций
# движение вперёд
top = ['Player_forward_1.bmp', 'Player_forward_2.bmp', 'Player_forward_3.bmp', 'Player_forward_4.bmp',
       'Player_forward_5.bmp', 'Player_forward_6.bmp', 'Player_forward_7.bmp', 'Player_forward_8.bmp',
       'Player_forward_9.bmp', 'Player_forward_10.bmp', 'Player_forward_11.bmp', 'Player_forward_12.bmp',
       'Player_forward_13.bmp']
# движение назад
back = ['Player_back_1.bmp', 'Player_back_2.bmp', 'Player_back_3.bmp', 'Player_back_4.bmp', 'Player_back_5.bmp',
        'Player_back_6.bmp', 'Player_back_7.bmp', 'Player_back_8.bmp', 'Player_back_9.bmp', 'Player_back_10.bmp',
        'Player_back_11.bmp', 'Player_back_12.bmp', 'Player_back_13.bmp']
# движение влево
forward_left = ['Player_left_1.bmp', 'Player_left_2.bmp', 'Player_left_3.bmp', 'Player_left_4.bmp', 'Player_left_5.bmp',
                'Player_left_6.bmp', 'Player_left_7.bmp', 'Player_left_8.bmp', 'Player_left_9.bmp',
                'Player_left_10.bmp',
                'Player_left_11.bmp', 'Player_left_12.bmp', 'Player_left_13.bmp']
# движение вправо
forward_right = ['Player_right_1.bmp', 'Player_right_2.bmp', 'Player_right_3.bmp', 'Player_right_4.bmp',
                 'Player_right_5.bmp',
                 'Player_right_6.bmp', 'Player_right_7.bmp', 'Player_right_8.bmp', 'Player_right_9.bmp',
                 'Player_right_10.bmp',
                 'Player_right_11.bmp', 'Player_right_12.bmp', 'Player_right_13.bmp']
# смерть
screen = camera.get_screen()

die_frames = ['Player_fall_1.bmp', 'Player_fall_2.bmp', 'Player_fall_5.bmp',
              'Player_fall_6.bmp', 'Player_die_1.bmp', 'Player_die_2.bmp', 'Player_die_3.bmp', 'Player_die_4.bmp',
              'Player_die_5.bmp', 'Player_die_6.bmp']
# создаём броню
armor = Armor(f'sprite/person_sprites/{top[0]}', (35, 35), 'armor_nikniksham', 1, 20, 40,
              'Защищает жопу от колющих и режущих ударов')
shoot_image = ['Desert Eagle shoot 1.bmp', 'Desert Eagle shoot 2.bmp', 'Desert Eagle shoot 3.bmp',
               'Desert Eagle shoot 4.bmp', 'Desert Eagle shoot 5.bmp', 'Desert Eagle shoot 6.bmp',
               'Desert Eagle shoot 7.bmp', 'Desert Eagle shoot 8.bmp']
# создаём самого героя
hero = Player('MainHero', (35, 35), top, back, forward_left, forward_right)

spike = EnemyBlock('sprite/blocks_sprites/spike.bmp', (480, 720), 1)
spike2 = EnemyBlock('sprite/blocks_sprites/spike.bmp', (600, 720), 1)
spike3 = EnemyBlock('sprite/blocks_sprites/spike.bmp', (720, 720), 1)
spike4 = EnemyBlock('sprite/blocks_sprites/spike.bmp', (840, 720), 1)
enemy_group = Group('sprite/blocks_sprites/spike.bmp', [spike, spike2, spike3, spike4])

# создаём сцену (карту)
# создаём сцену
scene = Level('sprite/blocks_sprites/block_1.bmp', 'first_scene',
              (chunk_count[0] * 16 * 16 * size, chunk_count[0] * 16 * 16 * size))
# добавляем чанки
# добавляем чанк заднего фона
scene.add_main_chunk(bg_group)
# добавляем чанк переднего плана
scene.add_main_chunk(walls_group)
# добавляем главного героя
scene.add_object(hero)
# устанавливаем главного героя главным героем
scene.set_main_hero(hero)
resurrection = ImageButton('sprite/User_Interface/resurrection.bmp', (size_screen[0] // 2 - 100, size_screen[1] // 2 - 100))
NPS = WithSomeone('sprite/NPS_sprites/hog.bmp', (100, 100), top, back,
                  forward_left, forward_right)
scene.add_group(enemy_group)
scene.add_object(NPS)
heal_point = Image('sprite/User_Interface/heal_point.bmp')
Desert_eagle = WeaponObj('sprite/Weapon_sprites/Desert Eagle.bmp', (360, 360), 'DesertEagle', 1, 'simple', 'simple',
                         120, (10, 100), 200, 1, None, shoot_image, screen=screen, aim=hero)
# цикл работает
run = True
coord = [(int(size_screen[0] - 500), int(size_screen[1] - 160)), (int(size_screen[0] - 790), int(size_screen[1] - 160))]


def print_text(message, x, y, font_style='arial.ttf', font_size=30, font_color=(0, 0, 0)):
    font_type = pygame.font.Font(font_style, font_size)
    text = font_type.render(message, True, font_color)
    screen.blit(text, (x, y))


# в какую сторону он движется
f = left = right = up = down = shift = False
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

        # движение персанажа
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                left = True
            if event.key == pygame.K_d:
                right = True
            if event.key == pygame.K_w:
                up = True
            if event.key == pygame.K_s:
                down = True
            if event.key == pygame.K_LSHIFT or event.key == pygame.K_RSHIFT:
                shift = True
            if f:
                f = False
                camera.create()
            if event.key == 311:
                f = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                left = False
            if event.key == pygame.K_d:
                right = False
            if event.key == pygame.K_w:
                up = False
            if event.key == pygame.K_s:
                down = False
            if event.key == pygame.K_LSHIFT or event.key == pygame.K_RSHIFT:
                shift = False
            if f:
                f = False
                if event.key == 311:
                    f = True
                camera.create()
    # обнавляем главного героя (двигаем и анимируем)
    camera.draw(scene)
    hero.update(left, right, up, down, walls_group, enemy_group, shift)
    camera.draw_interface(heal_point, [hero.get_hp(), hero.get_max_hp()], [hero.get_food(), hero.get_max_food()], coord)
    x, y = hero.get_coord()
    if hero.get_hp() <= 0 and hero.get_die() is False:
        hero.die('sprite/person_sprites/', [die_frames])
    if hero.get_die():
        resurrection.draw(hero.resurrection, screen)
    # NPS.update(hero, walls_group)
    print_text(str(int(camera.clock.get_fps())), size_screen[0] - 250, 120, font_color=(255, 255, 0))
    # отрисовываем сцену
    # Desert_eagle.shoot()
    # Desert_eagle.draw(screen)
    pygame.display.flip()
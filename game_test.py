import unittest
import pygame
import
from pygame.math import Vector2
from  import Player, Platform, Spike, Orb, End, init_level, block_map  # Импортируйте необходимые классы и функции из вашего игрового файла

class TestGame(unittest.TestCase):
    def setUp(self):
        """Настройка перед каждым тестом."""
        pygame.init()
        self.screen = pygame.display.set_mode([900, 700])
        self.platform_image = pygame.Surface((40, 40))
        self.player_image = pygame.Surface((40, 40))
        self.player = Player(self.player_image, pygame.sprite.Group(), (100, 150))
        self.platform = Platform(self.platform_image, (100, 200), pygame.sprite.Group())
        self.spike = Spike(self.platform_image, (150, 200), pygame.sprite.Group())
        self.orb = Orb(self.platform_image, (200, 200), pygame.sprite.Group())
        self.end = End(self.platform_image, (300, 200), pygame.sprite.Group())

    def test_player_initialization(self):
        """Тестирование инициализации игрока."""
        self.assertEqual(self.player.rect.center, (100, 150))
        self.assertEqual(self.player.jump_amount, 12)
        self.assertFalse(self.player.onGround)

    def test_player_jump(self):
        """Тестирование прыжка игрока."""
        self.player.jump()
        self.assertEqual(self.player.vel.y, -12)

    def test_collision_with_platform(self):
        """Тестирование столкновения игрока с платформой."""
        self.player.rect.bottom = self.platform.rect.top + 1  # Установим игрока прямо над платформой
        self.player.collide(1, pygame.sprite.Group(self.platform))
        self.assertTrue(self.player.onGround)
        self.assertEqual(self.player.rect.bottom, self.platform.rect.top)

    def test_collision_with_spike(self):
        """Тестирование столкновения игрока с шипом."""
        self.player.rect.bottom = self.spike.rect.top + 1  # Установим игрока прямо над шипом
        self.player.collide(1, pygame.sprite.Group(self.spike))
        self.assertTrue(self.player.died)

    def test_collision_with_orb(self):
        """Тестирование столкновения игрока с орбом."""
        self.player.rect.center = self.orb.rect.center  # Установим игрока на орб
        keys = {pygame.K_UP: True}  # Симулируем нажатие клавиши
        self.player.collide(1, pygame.sprite.Group(self.orb))
        self.assertEqual(self.player.jump_amount, 14)  # Проверяем, что сила прыжка увеличилась

    def test_end_point_collision(self):
        """Тестирование столкновения игрока с конечной точкой."""
        self.player.rect.center = self.end.rect.center  # Установим игрока на конечную точку
        self.player.collide(1, pygame.sprite.Group(self.end))
        self.assertTrue(self.player.win)

    def test_level_initialization(self):
        """Тестирование инициализации уровня из CSV."""
        level_map = [
            ["0", "0", "0", "0"],
            ["Spike", "Orb", "End", "0"],
        ]
        init_level(level_map)
        self.assertEqual(len(self.platforms), 4)  # Проверяем, что платформы созданы
        self.assertEqual(len(self.spikes), 1)  # Проверяем, что шипы созданы
        self.assertEqual(len(self.orbs), 1)  # Проверяем, что орбы созданы
        self.assertEqual(len(self.ends), 1)  # Проверяем, что конечные точки созданы

    def tearDown(self):
        """Очистка после каждого теста."""
        pygame.quit()

if __name__ == '__main__':
    unittest.main()

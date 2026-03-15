#!/usr/bin/env python3
"""
Тест для проверки:
1. Все цифры 0-39 присутствуют в NUMERIC_MENU
2. Неизвестные команды возвращают action_taken=True
"""

import unittest
from config import NUMERIC_MENU
from handlers.core import handle_commands

class TestNumericMenuFix(unittest.TestCase):
    def test_numeric_menu_complete(self):
        """Проверка, что все цифры от 0 до 39 имеют маппинг."""
        missing = []
        for digit in [str(d) for d in list(range(0, 40))]:
            self.assertIn(digit, NUMERIC_MENU, f"Отсутствует маппинг для цифры {digit}")
        # Если нет пропущенных, тест проходит
    
    def test_unknown_command_action_taken(self):
        """Проверка, что неизвестная команда возвращает (True, None, None, True) -> action_taken=True."""
        # Mock объектов
        class MockConn:
            pass
        class MockLLM:
            pass
        
        conn = MockConn()
        llm = MockLLM()
        
        # Вызываем с несуществующим действием (должно попасть в блок unknown command)
        result = handle_commands("unknown_test_command_xyz", conn, llm)
        
        self.assertIsNotNone(result, "handle_commands вернул None вместо кортежа")
        
        continue_loop, new_mode, new_level, action_taken = result
        
        self.assertTrue(action_taken, f"action_taken должен быть True, получили {action_taken}")

if __name__ == "__main__":
    unittest.main()
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Тесты для C-04: APT groups/dossiers"""

import unittest
from unittest.mock import patch, MagicMock
from handlers.threats import handle_threats, handle_groups, THREATS_DIR
import json
import os


class TestThreatsCommands(unittest.TestCase):
    """Проверка команд /threats и /groups"""

    @patch('handlers.threats.console')
    @patch('handlers.threats.os.path.exists')
    @patch('handlers.threats.os.listdir')
    def test_handle_threats_missing_group(self, mock_listdir, mock_exists, mock_console):
        """Запрос несуществующей группы показывает список доступных"""
        # Первый вызов os.path.exists (для threat_file) = False
        # Второй вызов (для THREATS_DIR) = True
        mock_exists.side_effect = [False, True]
        mock_listdir.return_value = ['apt28.json', 'apt29.json']

        result = handle_threats("threats unknown")

        self.assertEqual(result, (True, None, None, True))
        # Проверяем, что выведен список доступных
        printed = " ".join(str(call) for call in mock_console.print.call_args_list)
        self.assertIn("Доступные", printed)

    @patch('handlers.threats.console')
    @patch('builtins.open', create=True)
    @patch('handlers.threats.os.path.exists')
    def test_handle_threats_shows_dossier(self, mock_exists, mock_open, mock_console):
        """Показ досье на существующую группу"""
        mock_exists.return_value = True
        mock_file = MagicMock()
        mock_file.__enter__ = MagicMock(return_value=mock_file)
        mock_file.__exit__ = MagicMock(return_value=False)
        mock_file.read.return_value = json.dumps({
            "name": "APT28",
            "aliases": ["Fancy Bear"],
            "country": "Russia",
            "first_seen": "2004",
            "targets": ["Government"],
            "tactics": ["Initial Access"],
            "tools": ["X-Agent"],
            "techniques": ["T1566.001"],
            "recent_activity": "Active",
            "references": ["https://example.com"]
        })
        mock_open.return_value = mock_file

        result = handle_threats("threats apt28")

        self.assertEqual(result, (True, None, None, True))
        # Проверяем, что было повторение ключевых полей
        printed = " ".join(str(call) for call in mock_console.print.call_args_list)
        self.assertIn("APT28", printed)
        self.assertIn("Fancy Bear", printed)

    @patch('handlers.threats.console')
    @patch('handlers.threats.os.path.exists')
    def test_handle_groups_no_folder(self, mock_exists, mock_console):
        """Если папка threats не существует — сообщение"""
        mock_exists.return_value = False

        result = handle_groups()

        self.assertEqual(result, (True, None, None, True))
        mock_console.print.assert_any_call("[yellow]Папка threats/ не найдена[/yellow]")

    @patch('handlers.threats.console')
    @patch('handlers.threats.os.path.exists')
    @patch('handlers.threats.os.listdir')
    @patch('builtins.open', create=True)
    def test_handle_groups_shows_summary(self, mock_open, mock_listdir, mock_exists, mock_console):
        """handle_groups показывает сводку по всем группам"""
        mock_exists.return_value = True
        mock_listdir.return_value = ['apt28.json', 'apt29.json']

        def mock_open_func(path, *args, **kwargs):
            mock_file = MagicMock()
            mock_file.__enter__ = MagicMock(return_value=mock_file)
            mock_file.__exit__ = MagicMock(return_value=False)
            if 'apt28' in path:
                mock_file.read.return_value = json.dumps({
                    "name": "APT28",
                    "country": "Russia",
                    "tactics": ["Initial Access", "Persistence"],
                    "tools": ["X-Agent"],
                    "targets": ["Government"],
                    "first_seen": "2004"
                })
            else:
                mock_file.read.return_value = json.dumps({
                    "name": "APT29",
                    "country": "Russia",
                    "tactics": ["Execution"],
                    "tools": ["PowerDuke"],
                    "targets": ["Government"],
                    "first_seen": "2008"
                })
            return mock_file

        mock_open.side_effect = mock_open_func

        result = handle_groups()

        self.assertEqual(result, (True, None, None, True))
        # Проверяем вывод статистики
        printed = " ".join(str(call) for call in mock_console.print.call_args_list)
        self.assertIn("APT-группы", printed)
        self.assertIn("Всего групп", printed)

    def test_actual_json_files_exist(self):
        """Проверяем, что минимум 5 JSON-файлов существует в threats/"""
        # Используем THREATS_DIR из модуля
        threats_dir = THREATS_DIR
        if not os.path.exists(threats_dir):
            self.skipTest(f"Папка threats/ не найдена по пути {threats_dir}")

        files = [f for f in os.listdir(threats_dir) if f.endswith('.json')]
        self.assertGreaterEqual(len(files), 5, f"Нужно минимум 5 JSON-файлов для C-04, найдено: {len(files)}")

        # Проверяем структуру первого файла
        with open(os.path.join(threats_dir, files[0]), 'r', encoding='utf-8') as f:
            data = json.load(f)
            required_fields = ['name', 'aliases', 'country', 'tactics', 'tools', 'techniques']
            for field in required_fields:
                self.assertIn(field, data, f"В {files[0]} отсутствует поле {field}")


if __name__ == "__main__":
    unittest.main()

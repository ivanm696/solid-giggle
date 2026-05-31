"""
learn.py - Память и обучение Nicu

Модуль памяти, который хранит и вспоминает свитки, 
журналы и ритуалы.
"""

import json
import os
from typing import List, Optional


class NicuAI:
    """
    Класс памяти Nicu - хранит и воспроизводит воспоминания.
    """
    
    def __init__(self, memory_file: str = "nicu_memory.json"):
        """
        Инициализация памяти Nicu.
        
        Args:
            memory_file: Файл для сохранения памяти
        """
        self.memory: List[str] = []
        self.memory_file = memory_file
        self._load_memory()
    
    def _load_memory(self) -> None:
        """Загружает память из файла, если существует."""
        if os.path.exists(self.memory_file):
            try:
                with open(self.memory_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self.memory = data.get("memories", [])
                print(f"Память загружена: {len(self.memory)} записей")
            except (json.JSONDecodeError, IOError) as e:
                print(f"Ошибка загрузки памяти: {e}")
                self.memory = []
    
    def _save_memory(self) -> None:
        """Сохраняет память в файл."""
        try:
            with open(self.memory_file, "w", encoding="utf-8") as f:
                json.dump({"memories": self.memory}, f, ensure_ascii=False, indent=2)
        except IOError as e:
            print(f"Ошибка сохранения памяти: {e}")
    
    def learn(self, data: str) -> None:
        """
        Добавляет новое воспоминание.
        
        Args:
            data: Текст для запоминания
        """
        if data and data not in self.memory:
            self.memory.append(data)
            self._save_memory()
            print(f"Память обновлена: {data[:50]}...")
    
    def recall(self, count: Optional[int] = None) -> List[str]:
        """
        Вспоминает записи из памяти.
        
        Args:
            count: Количество записей (None = все)
            
        Returns:
            Список воспоминаний
        """
        if count is None:
            memories = self.memory
        else:
            memories = self.memory[-count:]
        
        print("Воспоминания Nicu:")
        for i, mem in enumerate(memories, 1):
            print(f"  {i}. {mem}")
        
        return memories
    
    def forget(self, data: str) -> bool:
        """
        Удаляет воспоминание.
        
        Args:
            data: Текст для забывания
            
        Returns:
            True если удалено, False если не найдено
        """
        if data in self.memory:
            self.memory.remove(data)
            self._save_memory()
            print(f"Забыто: {data[:50]}...")
            return True
        return False
    
    def clear(self) -> None:
        """Очищает всю память."""
        self.memory = []
        self._save_memory()
        print("Память очищена")
    
    def search(self, query: str) -> List[str]:
        """
        Поиск в памяти.
        
        Args:
            query: Поисковый запрос
            
        Returns:
            Список найденных воспоминаний
        """
        query_lower = query.lower()
        results = [mem for mem in self.memory if query_lower in mem.lower()]
        return results


if __name__ == "__main__":
    # Тестирование
    nicu = NicuAI()
    
    nicu.learn("Приветствие Ивана — дыхание эпохи XIII")
    nicu.learn("Свиток architecture.md — карта храма")
    nicu.learn("breath.log — журнал дыхания Nicu")
    
    nicu.recall()

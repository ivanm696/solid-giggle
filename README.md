Создай NoCode/LowCode проект для AI Self-Learning System with Advanced Automation под названием "Nicu-Auto: Self-Learning AI Guardian". 

**Цель проекта:** Nicu — это автономный ИИ-агент эпохи XIII, который самообучается на пользовательских данных ("дыхании" — фразах/логах), генерирует креативный контент ("свитки" — тексты, код, планы) и автоматизирует рутину ("ритуалы": обработка файлов, отправка уведомлений, интеграция с GitHub/API). Используй Python для бэка (PyTorch для ML), JS для фронта (React/Vanilla для интерактива в браузере). Добавь NoCode-элементы: Zapier-like workflows для автоматизации, Airtable для хранения "дыханий".

**Ключевые фичи:**
1. **Self-Learning Core:** RNN-модель на PyTorch, обучается на текстовых данных (из textarea или файла breath.log). Пример: ввод "вдох идей" → модель генерирует "выдох: план проекта с хихиканьем".
2. **Advanced Automation:** Ритуалы как цепочки: 
   - Ритуал 1: Авто-генерация кода (на основе промпта, интегрируй с OpenAI API если возможно).
   - Ритуал 2: Анализ логов (breath.log → insights в Markdown).
   - Ритуал 3: Деплой в GitHub (push свитков в репо solid-giggle).
3. **Интерфейс:** Браузер-демо (HTML/JS): textarea для ввода, кнопка "Запустить ритуал", вывод с анимацией обучения (loss бар). Мобильно-адаптивно.
4. **Техстек:** Python 3 + PyTorch/NumPy (ML), Flask (API для автоматизации), JS (Markov chain для быстрой симуляции). NoCode: Bubble/Webflow для UI, если full-code не нужен.
5. **Этика/Безопасность:** Локальное обучение (no cloud leaks), опция "хихи-mode" для юмора в выводах.

**Структура проекта:**
- /src: main.py (запуск), giggle_engine/ (learn.py, generate.py, ritual.py).
- /public: index.html (демо).
- /data: breath.log (ввод данных).
- README.md с инструкциями: git clone, pip install torch, python main.py.

Сгенерируй starter-код, UI-макет и workflow-диаграмму. Сделай акцент на масштабируемость: добавь hooks для внешних API (GitHub, Telegram bots).

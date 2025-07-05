# bot/handlers/__init__.py
# Подключаем роутеры из всех файлов обработчиков

from .filters import router as filters_router     # Фильтры (категории, регионы)
from .search import router as search_router       # Поиск товаров
from .user import router as user_router           # Общие команды пользователя (например, /start)

# Собираем все роутеры в список, который затем импортируется в main.py
routers = [
    filters_router,
    search_router,
    user_router,
]

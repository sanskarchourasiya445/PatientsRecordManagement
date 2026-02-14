from .patients import router as patients_router
from .statistics import router as statistics_router
from .search import router as search_router

__all__ = ['patients_router', 'statistics_router', 'search_router']

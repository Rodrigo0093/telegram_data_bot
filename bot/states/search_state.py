# bot/states/search_state.py

from aiogram.fsm.state import State, StatesGroup

class SearchState(StatesGroup):
    waiting_for_query = State()
    showing_results = State()
    filtering = State()

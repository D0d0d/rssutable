from aiogram.dispatcher.filters.state import StatesGroup, State

class States(StatesGroup):
    SETTED_FAC: State = State()
    SETTED_GROUP: State = State()

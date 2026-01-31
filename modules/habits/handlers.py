from aiogram import Router, types
from aiogram.fsm.context import FSMContext

from modules.habits.states import HabitStates
from modules.habits.services import add_habit
from modules.menu.keyboards import main_menu

router = Router()


@router.message(lambda m: m.text == "🔁 Привычки")
async def habit_start(message: types.Message, state: FSMContext):
    await message.answer("Введите название привычки:")
    await state.set_state(HabitStates.name)


@router.message(HabitStates.name)
async def habit_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("Как часто? (ежедневно / 3 раза в неделю и т.д.)")
    await state.set_state(HabitStates.frequency)


@router.message(HabitStates.frequency)
async def habit_frequency(message: types.Message, state: FSMContext):
    data = await state.get_data()

    add_habit(
        user_id=message.from_user.id,
        name=data["name"],
        frequency=message.text
    )

    await message.answer("✅ Привычка добавлена", reply_markup=main_menu())
    await state.clear()

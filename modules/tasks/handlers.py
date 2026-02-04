from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext

from modules.tasks.states import TaskStates
from modules.tasks.services import create_task

router = Router()


@router.message(F.text == "📋 Задачи")
async def tasks_menu(message: types.Message, state: FSMContext):
    await message.answer("Напиши задачу:")
    await state.set_state(TaskStates.title)


@router.message(TaskStates.title)
async def task_title_handler(message: types.Message, state: FSMContext):
    await state.update_data(title=message.text)
    await message.answer("Дедлайн? (YYYY-MM-DD или '-')")
    await state.set_state(TaskStates.deadline)


@router.message(TaskStates.deadline)
async def task_deadline_handler(message: types.Message, state: FSMContext):
    data = await state.get_data()

    deadline = None if message.text == "-" else message.text

    create_task(
        user_id=message.from_user.id,
        title=data["title"],
        deadline=deadline
    )

    await message.answer("✅ Задача добавлена")
    await state.clear()

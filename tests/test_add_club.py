import pytest
import types
import sys, os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import main


class DummyState:
    async def get_data(self):
        return None

    async def clear(self):
        return None


class DummyMessage:
    def __init__(self, text, chat_id=123):
        self.text = text
        self.chat = types.SimpleNamespace(id=chat_id)
        self.replies = []

    async def answer(self, text, **kwargs):
        self.replies.append(text)


@pytest.mark.asyncio
async def test_add_club_forbidden_word():
    """Тест на ввод запрещенных слов во избежание падения базы данных"""

    # Arrange
    msg = DummyMessage("drop table")
    state = DummyState()

    # Act
    await main.cmd_add_club(msg, state)

    # Assert
    assert "Попробуйте заново." in msg.replies[0]


@pytest.mark.asyncio
async def test_add_club_success():
    """Успешное добавление клуба"""

    # Arrange
    async def fake_get_from_fullclubs(_):
        return ["Барселона"]

    async def fake_get_from_bottable(_):
        return []

    async def fake_insert_into_bottable(uid, club):
        fake_insert_into_bottable.called = (uid, club)

    main.get_from_fullclubs = fake_get_from_fullclubs
    main.get_from_bottable = fake_get_from_bottable
    main.insert_into_bottable = fake_insert_into_bottable

    msg = DummyMessage("Барселона")
    state = DummyState()

    choosed_league = "Футбол"
    main.choosed_league = choosed_league

    # Act
    await main.cmd_add_club(msg, state)

    # Assert
    assert msg.replies[0] == "Добавлено: Барселона."
    assert fake_insert_into_bottable.called == (123, "Барселона")


@pytest.mark.asyncio
async def test_add_club_already_exists():
    """Клуб уже есть в избранном"""

    # Arrange
    async def fake_get_from_fullclubs(_):
        return ["Крылья Советов"]

    async def fake_get_from_bottable(_):
        return ["Крылья Советов"]

    main.get_from_fullclubs = fake_get_from_fullclubs
    main.get_from_bottable = fake_get_from_bottable

    msg = DummyMessage("Крылья Советов")
    state = DummyState()

    choosed_league = "Футбол"
    main.choosed_league = choosed_league

    # Act
    await main.cmd_add_club(msg, state)

    # Assert
    assert msg.replies[0] == "Крылья Советов уже есть в избранных"


@pytest.mark.asyncio
async def test_add_club_not_found():
    """Клуб не найден"""

    # Arrange
    async def fake_get_from_fullclubs(_): return ["Реал Мадрид"]

    async def fake_get_from_bottable(_): return []

    main.get_from_fullclubs = fake_get_from_fullclubs
    main.get_from_bottable = fake_get_from_bottable

    msg = DummyMessage("Барселона")
    state = DummyState()

    choosed_league = "Футбол"
    main.choosed_league = choosed_league

    # Act
    await main.cmd_add_club(msg, state)

    # Assert
    assert msg.replies[0] == "Не найдено. Попробуйте еще раз."


@pytest.mark.asyncio
async def test_add_club_case_insensitive():
    """Граничный тест - тест на независимость от регистра"""

    # Arrange
    async def fake_get_from_fullclubs(_):
        return ["Валенсия"]

    async def fake_get_from_bottable(_):
        return []

    async def fake_insert_into_bottable(uid, club):
        fake_insert_into_bottable.called = (uid, club)

    main.get_from_fullclubs = fake_get_from_fullclubs
    main.get_from_bottable = fake_get_from_bottable
    main.insert_into_bottable = fake_insert_into_bottable

    msg = DummyMessage("вАлЕнСиЯ")
    state = DummyState()

    choosed_league = "Футбол"
    main.choosed_league = choosed_league

    # Act
    await main.cmd_add_club(msg, state)

    # Assert
    assert msg.replies[0] == "Добавлено: Валенсия."
    assert fake_insert_into_bottable.called == (123, "Валенсия")

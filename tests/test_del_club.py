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
async def test_del_club_success():
    """Успешное удаление клуба"""

    # Arrange
    async def fake_get_from_bottable(uid, text):
        db = [(123, "Бавария", "бавария", )]
        for i in db:
            if i[0] == uid and i[2] == text.lower():
                return [i[1]]
        return []

    async def fake_del_from_bottable(club, uid):
        fake_del_from_bottable.called = (club, uid)

    main.get_from_bottable = fake_get_from_bottable
    main.delete_from_bottable = fake_del_from_bottable

    msg = DummyMessage("Бавария")
    state = DummyState()

    # Act
    await main.cmd_del_club(msg, state)

    # Assert
    assert msg.replies[0] == "Удалено: Бавария."
    assert fake_del_from_bottable.called == ("Бавария", 123)


@pytest.mark.asyncio
async def test_del_club_not_found():
    """Проверка: если клуб не найден в избранных"""

    # Arrange
    async def fake_get_from_bottable(uid, text):
        db = [(123, "Бавария", "бавария", )]
        for i in db:
            if i[0] == uid and i[2] == text.lower():
                return [i[1]]
        return []

    main.get_from_bottable = fake_get_from_bottable

    msg = DummyMessage("Монако")
    state = DummyState()

    # Act
    await main.cmd_del_club(msg, state)

    # Assert
    assert msg.replies[0] == "Нет избранных клубов/спортсменов с таким названием."


@pytest.mark.asyncio
async def test_del_club_case_insensitive():
    """Удаление клуба без учёта регистра"""

    # Arrange
    async def fake_get_from_bottable(uid, text):
        db = [(123, "Хетафе", "хетафе", )]
        for i in db:
            if i[0] == uid and i[2] == text.lower():
                return [i[1]]
        return []

    async def fake_del_from_bottable(club, uid):
        fake_del_from_bottable.called = (club, uid)

    main.get_from_bottable = fake_get_from_bottable
    main.delete_from_bottable = fake_del_from_bottable

    msg = DummyMessage("ХЕТафе")
    state = DummyState()

    # Act
    await main.cmd_del_club(msg, state)

    # Assert
    assert msg.replies[0] == "Удалено: Хетафе."
    assert fake_del_from_bottable.called == ("Хетафе", 123)


@pytest.mark.asyncio
async def test_del_club_forbidden_words():
    """Ввод запрещенных слов"""

    # Arrange
    msg = DummyMessage("delete * from fullclubs;")
    state = DummyState()

    # Act
    await main.cmd_del_club(msg, state)

    # Assert
    assert msg.replies[0] == "Попробуйте заново."


@pytest.mark.asyncio
async def test_del_club_exact_match():
    """Граничный тест - проверка точного совпадения для удаления клуба"""

    # Arrange
    async def fake_get_from_bottable(uid, text):
        db = [(123, "Зенит-Казань", "зенит-казань", ), (123, "Зенит", "зенит", )]
        for i in db:
            if i[0] == uid and i[2] == text.lower():
                return [i[1]]
        return []

    async def fake_del_from_bottable(club, uid):
        fake_del_from_bottable.called = (club, uid)

    main.get_from_bottable = fake_get_from_bottable
    main.delete_from_bottable = fake_del_from_bottable

    msg = DummyMessage("Зенит-Казань")
    state = DummyState()

    # Act
    await main.cmd_del_club(msg, state)

    # Assert
    assert msg.replies[0] == "Удалено: Зенит-Казань."
    assert fake_del_from_bottable.called == ("Зенит-Казань", 123)

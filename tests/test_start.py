import pytest
import types
import sys, os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import main


class DummyMessage:
    def __init__(self):
        self.replies = []
        self.chat = types.SimpleNamespace(id=123)

    async def answer(self, text, **kwargs):
        self.replies.append((text, kwargs))


@pytest.mark.asyncio
async def test_reply_builder():
    """Проверка на корректное поведение при первом запуске бота"""

    # Arrange
    msg = DummyMessage()

    # Act
    await main.reply_builder(msg)

    # Assert
    assert len(msg.replies) == 1

    text, kwargs = msg.replies[0]
    assert text == "Привет! Я буду помогать тебе следить за миром спорта."

    assert kwargs["parse_mode"] == "HTML"

    assert "reply_markup" in kwargs

    assert kwargs["reply_markup"] is not None

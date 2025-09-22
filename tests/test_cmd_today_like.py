import pytest
import types
import sys, os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import main


class DummyMessage:
    def __init__(self, chat_id=123):
        self.chat = types.SimpleNamespace(id=chat_id)
        self.replies = []

    async def answer(self, text, **kwargs):
        self.replies.append(text)


@pytest.mark.asyncio
async def test_today_nonempty_result():
    """Тест обычного матча"""

    # Arrange
    async def fake_view_dicts(user_id):
        matches = ["<b>Зенит</b> 2:0 ЦСКА"]
        return matches, len(matches)

    main.result = ["stub"]
    main.url = "stub_url"
    main.view_dicts = fake_view_dicts
    msg = DummyMessage()

    # Act
    await main.cmd_today_like(msg)

    # Assert
    assert msg.replies[0] == "<b>Зенит</b> 2:0 ЦСКА"
    assert msg.replies[1] == "Количество событий с участием избранных сегодня: 1."



@pytest.mark.asyncio
async def test_today_empty_result():
    """Случай с непрогруженной страницей"""

    # Arrange
    async def fake_get_page(url):
        return "<html>stub</html>"

    async def fake_make_dicts(page, suffix):
        return None

    async def fake_view_dicts(user_id):
        matches = ["<b>Реал Мадрид</b> 2:1 Барселона"]
        return matches, len(matches)

    main.result = []
    main.url = "stub_url"
    main.view_dicts = fake_view_dicts
    main.get_page = fake_get_page
    main.make_dicts = fake_make_dicts
    msg = DummyMessage()

    # Act
    await main.cmd_today_like(msg)

    # Assert
    assert msg.replies[0] == "<b>Реал Мадрид</b> 2:1 Барселона"
    assert msg.replies[1] == "Количество событий с участием избранных сегодня: 1."

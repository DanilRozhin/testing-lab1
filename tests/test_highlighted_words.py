import pytest
import sys, os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import main


@pytest.mark.asyncio
async def test_highlighted_simple_team():
    """Тест подсветки простого названия команды"""

    # Arrange
    event = "Краснодар 3:4 Зенит"
    team = "Зенит"

    # Act
    result = await main.highlighted(event, team)

    # Assert
    assert result == "Краснодар 3:4 <b>Зенит</b>"


@pytest.mark.asyncio
async def test_highlighted_exact_match():
    """Граничный тест - нужная команда на стыке слов"""

    # Arrange
    event = "23:00, 45'\nДинамо-Казань 1:0 Динамо"
    team = "Динамо"

    # Act
    result = await main.highlighted(event, team)

    # Assert
    assert result == "23:00, 45'\nДинамо-Казань 1:0 <b>Динамо</b>"


@pytest.mark.asyncio
async def test_highlighted_complicated_team():
    """Тест подсветки составного названия команды"""

    # Arrange
    event = "16:00, Не начался\nЗенит-Казань 0:0 Динамо-ЛО"
    team = "Зенит-Казань"

    # Act
    result = await main.highlighted(event, team)

    # Assert
    assert result == "16:00, Не начался\n<b>Зенит-Казань</b> 0:0 Динамо-ЛО"


@pytest.mark.asyncio
async def test_highlighted_team_not_found():
    """Команда не найдена в тексте"""

    # Arrange
    event = "Зенит 4:1 ЦСКА"
    team = "Динамо"

    # Act
    result = await main.highlighted(event, team)

    # Assert
    assert result == "Зенит 4:1 ЦСКА"


@pytest.mark.asyncio
async def test_highlighted_formula1_driver():
    """Тест подсветки имени и фамилии"""

    # Arrange
    event = "17:00, Гран-При Азербайджана\nЛандо Норрис\nМакс Ферстаппен\nДжордж Расселл"
    team = "Макс Ферстаппен"

    # Act
    result = await main.highlighted(event, team)

    # Assert
    assert result == "17:00, Гран-При Азербайджана\nЛандо Норрис\n<b>Макс Ферстаппен</b>\nДжордж Расселл"


@pytest.mark.asyncio
async def test_highlighted_driver_not_found():
    """Имя и фамилия не найдены"""

    # Arrange
    event = "17:00, Гран-При Монако\nЛандо Норрис\nМакс Ферстаппен\nДжордж Расселл"
    team = "Фернандо Алонсо"

    # Act
    result = await main.highlighted(event, team)

    # Assert
    assert result == "17:00, Гран-При Монако\nЛандо Норрис\nМакс Ферстаппен\nДжордж Расселл"


@pytest.mark.asyncio
async def test_highlighted_empty_event():
    """Тест пустого события"""

    # Arrange
    event = ""
    team = "Барселона"

    # Act
    result = await main.highlighted(event, team)

    # Assert
    assert result == ""

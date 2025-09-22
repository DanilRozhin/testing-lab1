import pytest
import sys, os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import main


@pytest.mark.asyncio
async def test_view_dicts_simple_match():
    """Формирование строки обычного матча"""

    # Arrange
    fake_result = [
        {
            "date": "20.09",
            "time": "17:00",
            "sport_type": "Футбол",
            "sport_subtype": "",
            "team1": "Зенит",
            "team2": "ЦСКА",
            "score": "1:1",
            "status": "Окончен",
            "supref": "fake_supref"
        }
    ]

    main.result = fake_result

    # Act
    matches, cnt = await main.view_dicts("Футбол")

    # Assert
    assert matches[0] == "17:00, Окончен\nЗенит 1:1 ЦСКА\n\n"
    assert cnt == 1


@pytest.mark.asyncio
async def test_view_dicts_race_event():
    """Формирование упрощенной строки для гоночного события"""

    # Arrange
    fake_result = [
        {
            "date": "21.09",
            "time": "14:00",
            "sport_type": "Авто",
            "sport_subtype": "formula-1",
            "team1": "Гран-при Азербайджана",
            "team2": ["fake_driver1", "fake_driver2"],
            "score": "",
            "status": "Не начался",
            "supref": "fake_supref"
        }
    ]

    main.result = fake_result

    # Act
    matches, cnt = await main.view_dicts("Авто")

    # Assert
    assert matches[0] == "14:00, Не начался\nГран-при Азербайджана\n\n"
    assert cnt == 1


@pytest.mark.asyncio
async def test_view_dicts_get_favourite_home():
    """Проверка формирования строки для просмотра матчей избранных команд (избранная команда играет ДОМА)"""

    # Arrange
    async def fake_get_from_bottable(user_id):
        return ["Реал Мадрид"]

    fake_result = [
        {
            "date": "27.10",
            "time": "12:00",
            "sport_type": "Футбол",
            "sport_subtype": "",
            "team1": "Реал Мадрид",
            "team2": "Барселона",
            "score": "4:3",
            "status": "46'",
            "supref": "fake_supref"
        }
    ]

    main.result = fake_result
    main.get_from_bottable = fake_get_from_bottable

    # Act
    matches, cnt = await main.view_dicts(sport=123)

    # Assert
    assert matches[0] == "12:00, 46'\n<b>Реал Мадрид</b> 4:3 Барселона\n\n"
    assert cnt == 1


@pytest.mark.asyncio
async def test_view_dicts_get_favourite_guest():
    """Проверка формирования строки для просмотра матчей избранных команд (избранная команда играет В ГОСТЯХ)"""

    # Arrange
    async def fake_get_from_bottable(user_id):
        return ["Ювентус"]

    fake_result = [
        {
            "date": "23.10",
            "time": "14:45",
            "sport_type": "Футбол",
            "sport_subtype": "",
            "team1": "Аталанта",
            "team2": "Ювентус",
            "score": "0:2",
            "status": "Не начался",
            "supref": "fake_supref"
        }
    ]

    main.result = fake_result
    main.get_from_bottable = fake_get_from_bottable

    # Act
    matches, cnt = await main.view_dicts(sport=123)

    # Assert
    assert matches[0] == "14:45, Не начался\nАталанта 0:2 <b>Ювентус</b>\n\n"
    assert cnt == 1


@pytest.mark.asyncio
async def test_view_dicts_get_favourite_both():
    """Проверка формирования строки для просмотра матчей избранных команд
    (в матче принимают участие ОБЕ избранных команды)
    Граничный тест - матч не должен дублироваться"""

    # Arrange
    async def fake_get_from_bottable(user_id):
        return ["Ливерпуль", "Милан"]

    fake_result = [
        {
            "date": "23.10",
            "time": "14:45",
            "sport_type": "Футбол",
            "sport_subtype": "",
            "team1": "Милан",
            "team2": "Ливерпуль",
            "score": "0:2",
            "status": "Не начался",
            "supref": "fake_supref"
        }
    ]

    main.result = fake_result
    main.get_from_bottable = fake_get_from_bottable

    # Act
    matches, cnt = await main.view_dicts(sport=123)

    # Assert
    assert matches[0] == "14:45, Не начался\n<b>Милан</b> 0:2 <b>Ливерпуль</b>\n\n"
    assert cnt == 1


@pytest.mark.asyncio
async def test_view_dicts_right_sorting():
    """Проверка формирования строки для просмотра нескольких матчей дня"""

    # Arrange
    fake_result = [
        {
            "date": "21.09",
            "time": "14:45",
            "sport_type": "Футбол",
            "sport_subtype": "",
            "team1": "Милан",
            "team2": "Ливерпуль",
            "score": "0:2",
            "status": "Не начался",
            "supref": "fake_supref"
        },
        {
            "date": "21.09",
            "time": "11:00",
            "sport_type": "Футбол",
            "sport_subtype": "",
            "team1": "ЦСКА",
            "team2": "Спартак",
            "score": "2:1",
            "status": "Не начался",
            "supref": "fake_supref"
        },
        {
            "date": "21.09",
            "time": "09:00",
            "sport_type": "Футбол",
            "sport_subtype": "",
            "team1": "Балтика",
            "team2": "Оренбург",
            "score": "1:1",
            "status": "Окончен",
            "supref": "fake_supref"
        }
    ]

    main.result = fake_result

    # Act
    matches, cnt = await main.view_dicts("Футбол")

    # Assert
    assert matches[
               0] == "09:00, Окончен\nБалтика 1:1 Оренбург\n\n11:00, Не начался\nЦСКА 2:1 Спартак\n\n14:45, Не начался\nМилан 0:2 Ливерпуль\n\n"
    assert cnt == 3


@pytest.mark.asyncio
async def test_view_dicts_right_sorting_special():
    """Проверка формирования строки для просмотра нескольких матчей дня в специальных категориях"""

    # Arrange
    fake_result = [
        {
            "date": "21.09",
            "time": "14:00",
            "sport_type": "Биатлон",
            "sport_subtype": "",
            "team1": "Эстафета. Мужчины",
            "team2": ["fake_sprinter1", "fake_sprinter2"],
            "score": "",
            "status": "Окончено",
            "supref": "fake_supref"
        },
        {
            "date": "21.09",
            "time": "17:00",
            "sport_type": "Биатлон",
            "sport_subtype": "",
            "team1": "Спринт. Мужчины",
            "team2": ["fake_sprinter1", "fake_sprinter2"],
            "score": "",
            "status": "Не начался",
            "supref": "fake_supref"
        },
        {
            "date": "21.09",
            "time": "10:00",
            "sport_type": "Биатлон",
            "sport_subtype": "",
            "team1": "Гонка преследования. Женщины",
            "team2": ["fake_sprinter1", "fake_sprinter2"],
            "score": "",
            "status": "Окончено",
            "supref": "fake_supref"
        }
    ]

    main.result = fake_result

    # Act
    matches, cnt = await main.view_dicts("Биатлон")

    # Assert
    assert matches[0] == "10:00, Окончено\nГонка преследования. Женщины\n\n14:00, Окончено\nЭстафета. Мужчины\n\n17:00, Не начался\nСпринт. Мужчины\n\n"
    assert cnt == 3


@pytest.mark.asyncio
async def test_view_dicts_pair_sport():
    """Проверка формирования строки для просмотра матчей в случае с парными видами спорта"""

    # Arrange
    async def fake_get_from_bottable(user_id):
        return ["Алькарас К."]

    fake_result = [
        {
            "date": "15.12",
            "time": "18:00",
            "sport_type": "Теннис",
            "sport_subtype": "ATP Doubles",
            "team1": "Надаль Р. / Алькарас К.",
            "team2": "Джокович Н. / Медведев Д.",
            "score": "2:0 (6:3, 7:6)",
            "status": "Окончено",
            "supref": "fake_supref"
        },
    ]

    main.result = fake_result

    main.get_from_bottable = fake_get_from_bottable

    # Act
    matches, cnt = await main.view_dicts(123)

    # Assert
    assert matches[0] == "18:00, Окончено\nНадаль Р. / <b>Алькарас К.</b> 2:0 (6:3, 7:6) Джокович Н. / Медведев Д.\n\n"
    assert cnt == 1


@pytest.mark.asyncio
async def test_view_dicts_pair_sport_twice():
    """Проверка формирования строки для просмотра матчей в случае с парными видами спорта
    в том случае, когда теннисист играет дважды за день"""

    # Arrange
    async def fake_get_from_bottable(user_id):
        return ["Алькарас К."]

    fake_result = [
        {
            "date": "15.12",
            "time": "18:00",
            "sport_type": "Теннис",
            "sport_subtype": "ATP Doubles",
            "team1": "Надаль Р. / Алькарас К.",
            "team2": "Джокович Н. / Медведев Д.",
            "score": "2:0 (6:3, 7:6)",
            "status": "Окончено",
            "supref": "fake_supref"
        },
        {
            "date": "15.12",
            "time": "11:00",
            "sport_type": "Теннис",
            "sport_subtype": "ATP Singles",
            "team1": "Алькарас К.",
            "team2": "Медведев Д.",
            "score": "2:1 (6:3, 4:6, 7:6)",
            "status": "Окончено",
            "supref": "fake_supref"
        }
    ]

    main.result = fake_result

    main.get_from_bottable = fake_get_from_bottable

    # Act
    matches, cnt = await main.view_dicts(123)

    # Assert
    assert matches[0] == "11:00, Окончено\n<b>Алькарас К.</b> 2:1 (6:3, 4:6, 7:6) Медведев Д.\n\n18:00, Окончено\nНадаль Р. / <b>Алькарас К.</b> 2:0 (6:3, 7:6) Джокович Н. / Медведев Д.\n\n"
    assert cnt == 2


@pytest.mark.asyncio
async def test_view_dicts_special_sports_favourite():
    """Проверка формирования строки для просмотра матчей в случае со специальными видами спорта из избранных"""

    # Arrange
    async def fake_get_from_bottable(user_id):
        return ["Макс Ферстаппен", "Джордж Расселл"]

    fake_result = [
        {
            "date": "21.09",
            "time": "14:00",
            "sport_type": "Авто",
            "sport_subtype": "formula-1",
            "team1": "Гран-при Азербайджана",
            "team2": ["fake_driver1", "fake_driver2", "Макс Ферстаппен", "fake_driver3", "Джордж Расселл"],
            "score": "",
            "status": "Окончено",
            "supref": "fake_supref"
        },
    ]

    main.result = fake_result

    main.get_from_bottable = fake_get_from_bottable

    # Act
    matches, cnt = await main.view_dicts(123)

    # Assert
    assert matches[0] == "14:00, Окончено\nГран-при Азербайджана\n<b>Джордж Расселл</b>\n<b>Макс Ферстаппен</b>\n\n"
    assert cnt == 1


@pytest.mark.asyncio
async def test_view_dicts_teams_in_different_sports():
    """Проверка на просмотр матчей избранных команд, если в разных видах спорта название команды будет совпадать"""

    # Arrange
    async def fake_get_from_bottable(user_id):
        return ["Нефтехимик"]

    fake_result = [
        {
            "date": "21.09",
            "time": "14:00",
            "sport_type": "Хоккей",
            "sport_subtype": "",
            "team1": "Нефтехимик",
            "team2": "Авангард",
            "score": "2:1",
            "status": "Окончен",
            "supref": "fake_supref"
        },
        {
            "date": "21.09",
            "time": "11:00",
            "sport_type": "Футбол",
            "sport_subtype": "",
            "team1": "КАМАЗ",
            "team2": "Нефтехимик",
            "score": "5:5",
            "status": "Окончен",
            "supref": "fake_supref"
        }
    ]

    main.result = fake_result

    main.get_from_bottable = fake_get_from_bottable

    # Act
    matches, cnt = await main.view_dicts(123)

    # Assert
    assert matches[0] == "11:00, Окончен\nКАМАЗ 5:5 <b>Нефтехимик</b>\n\n"
    assert cnt == 1

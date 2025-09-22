import pytest
import sys, os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import main

@pytest.fixture(autouse=True)
def reset_main():
    orig_view_dicts = main.view_dicts
    orig_get_page = main.get_page
    orig_make_dicts = main.make_dicts
    orig_get_from_fullclubs = main.get_from_fullclubs
    orig_get_from_bottable = main.get_from_bottable
    orig_insert_into_bottable = main.insert_into_bottable
    orig_delete_from_bottable = main.delete_from_bottable
    orig_result = main.result
    orig_url = main.url

    yield

    main.view_dicts = orig_view_dicts
    main.get_page = orig_get_page
    main.make_dicts = orig_make_dicts
    main.get_from_fullclubs = orig_get_from_fullclubs
    main.get_from_bottable = orig_get_from_bottable
    main.insert_into_bottable = orig_insert_into_bottable
    main.delete_from_bottable = orig_delete_from_bottable
    main.result = orig_result
    main.url = orig_url

"""
Pytest設定ファイル
"""


# pytest-asyncioを設定
def pytest_configure(config):
    """pytest設定を構成"""
    # asyncio modeの設定
    config.addinivalue_line("markers", "asyncio: mark test as an asyncio test")

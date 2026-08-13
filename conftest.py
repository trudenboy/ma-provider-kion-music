"""Provider-repository pytest integration with the Music Assistant test suite."""

from __future__ import annotations

import asyncio
import importlib.util
import threading
from collections.abc import AsyncGenerator
from pathlib import Path
from types import ModuleType

import pytest

import music_assistant
import tests
from music_assistant.controllers.cache import CacheController
from music_assistant.controllers.config import ConfigController
from music_assistant.mass import MusicAssistant

_SERVER_TESTS = Path(music_assistant.__file__).resolve().parent.parent / "tests"
_SERVER_CONFTEST: ModuleType | None = None

if _SERVER_TESTS.is_dir():
    tests.__path__.append(str(_SERVER_TESTS))
    _spec = importlib.util.spec_from_file_location(
        "_music_assistant_server_conftest", _SERVER_TESTS / "conftest.py"
    )
    if _spec is not None and _spec.loader is not None:
        _SERVER_CONFTEST = importlib.util.module_from_spec(_spec)
        _spec.loader.exec_module(_SERVER_CONFTEST)


def pytest_configure(config: pytest.Config) -> None:
    """Register the server's shared fixtures when its source checkout is available."""
    if _SERVER_CONFTEST is not None:
        config.pluginmanager.register(_SERVER_CONFTEST, "music-assistant-server-conftest")


if _SERVER_CONFTEST is None:

    @pytest.fixture
    async def mass_minimal(tmp_path: Path) -> AsyncGenerator[MusicAssistant]:
        """Create a minimal Music Assistant instance for standalone provider tests."""
        storage_path = tmp_path / "data"
        cache_path = tmp_path / "cache"
        storage_path.mkdir(parents=True)
        cache_path.mkdir(parents=True)

        mass = MusicAssistant(str(storage_path), str(cache_path))
        mass.loop = asyncio.get_running_loop()
        mass.loop_thread_id = threading.get_ident()
        mass.config = ConfigController(mass)
        await mass.config.setup()
        mass.cache = CacheController(mass)
        try:
            yield mass
        finally:
            await mass.cache.close()
            await mass.config.close()

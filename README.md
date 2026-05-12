# Провайдер KION Музыки для Music Assistant


<!-- >>> ma-provider-tools sync (readme header) — DO NOT EDIT >>> -->
[![CI](https://github.com/trudenboy/ma-provider-kion-music/actions/workflows/test.yml/badge.svg)](https://github.com/trudenboy/ma-provider-kion-music/actions/workflows/test.yml)
[![Release](https://img.shields.io/github/v/release/trudenboy/ma-provider-kion-music?display_name=tag)](https://github.com/trudenboy/ma-provider-kion-music/releases/latest)
[![License](https://img.shields.io/github/license/trudenboy/ma-provider-kion-music)](LICENSE)
[![Music Assistant](https://img.shields.io/badge/Music%20Assistant-provider-9070B8?logo=python&logoColor=white)](https://www.music-assistant.io/)
[![Stars](https://img.shields.io/github/stars/trudenboy/ma-provider-kion-music?style=flat&logo=github)](https://github.com/trudenboy/ma-provider-kion-music/stargazers)

**📖 [Documentation / Документация](https://trudenboy.github.io/ma-provider-kion-music/)** · **🔄 [Changelog / Журнал](CHANGELOG.md)** · **🐛 [Issues / Проблемы](https://github.com/trudenboy/ma-provider-kion-music/issues)** · **💬 [Discussions / Обсуждения](https://github.com/trudenboy/ma-provider-kion-music/discussions)**

**Related providers:** [Yandex Music](https://github.com/trudenboy/ma-provider-yandex-music)
<!-- <<< ma-provider-tools sync (readme header) <<< -->

[English](README.en.md) | Русский

📖 <a href="https://trudenboy.github.io/ma-provider-kion-music/">Документация пользователя</a>

> Слушайте свою библиотеку [KION Музыки](https://music.kion.ru/) через [Music Assistant](https://music-assistant.io/) с поддержкой навигации, поиска, радио и воспроизведения без потерь.

## Быстрый старт (Docker)

```bash
# Клонируйте репозиторий
git clone https://github.com/trudenboy/ma-provider-kion-music.git
cd ma-provider-kion-music

# Запустите Music Assistant с предустановленным провайдером
docker compose -f docker-compose.dev.yml up
```

Откройте веб-интерфейс MA по адресу `http://localhost:8095`, затем перейдите в **Настройки → Музыкальные источники → Добавить источник → KION Музыка** и введите ваш OAuth-токен.

Подробное руководство по Docker-окружению для разработки: [docs/dev-docker.md](docs/dev-docker.md).

## Возможности

- **Синхронизация библиотеки** — Исполнители, Альбомы, Треки (Понравившиеся), Плейлисты синхронизируются с библиотекой MA
- **Редактирование библиотеки** — Лайк / дизлайк Исполнителей, Альбомов, Треков прямо из MA
- **Навигация** — Понравившиеся треки, Мой Микс, Исполнители, Альбомы, Плейлисты
- **Рекомендации** — Мой Микс представлен как папка рекомендаций MA
- **Поиск** — Треки, Исполнители, Альбомы, Плейлисты
- **Похожие треки** — на основе ротора KION
- **Качество звука** — Высокое (MP3 320 кбит/с) / Без потерь (FLAC)

## Документация

| Руководство | Описание |
|-------------|----------|
| [Настройка](docs/configuration.md) | Токен, настройки качества |
| [Разработка](docs/development.md) | Настройка окружения, тесты, линтинг, формат коммитов |
| [Участие в разработке](docs/contributing.md) | Сообщения об ошибках, предложения, pull request'ы |
| [Тестирование](docs/testing.md) | Запуск тестов, CI-пайплайн, покрытие |
| [Управление инцидентами](docs/incident-management.md) | Метки, автоматическое отслеживание, триаж Copilot |
| [Локальная разработка (Docker)](docs/dev-docker.md) | Запуск MA + провайдера без установки зависимостей |

## Ссылки

- [Music Assistant](https://music-assistant.io/) — open-source музыкальный сервер от Marcel van der Veldt
- [KION Музыка](https://music.kion.ru/) — стриминговый сервис от МТС
- [yandex-music](https://github.com/MarshalX/yandex-music-api) — неофициальный Python-клиент от MarshalX

## Лицензия

[Apache 2.0](LICENSE) — история изменений в [CHANGELOG.md](CHANGELOG.md).

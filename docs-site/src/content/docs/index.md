---
title: Провайдер KION Music
description: Документация провайдера KION Music для Music Assistant
---

<img src="https://raw.githubusercontent.com/trudenboy/ma-provider-kion-music/dev/provider/icon.svg" alt="KION Music" style="width: 72px; float: right; margin: 0 0 1rem 1.5rem;" />

[Music Assistant](https://music-assistant.io) поддерживает [KION Music](https://kion.ru) — музыкальный стриминговый сервис МТС.

Провайдер создан и поддерживается [TrudenBoy](https://github.com/TrudenBoy).

Реализован на основе библиотеки [kion-music](https://github.com/MarshalX/yandex-music-api) (**неофициальный** клиент API через прокси KION Music).

## Возможности

| Функция | Поддержка |
|:--------|:---------:|
| Исполнители, Альбомы, Треки, Плейлисты | ✅ |
| Поиск по каталогу | ✅ |
| Синхронизация библиотеки (двунаправленная) | ✅ |
| [Рекомендации на главном экране](features/recommendations/) | ✅ |
| [Мой микс / Radio Mode](features/my-mix/) | ✅ |
| [Радиостанции / Rotor](features/radio/) | ✅ |
| [Похожие треки](features/similar-tracks/) | ✅ |
| [Тексты песен](features/lyrics/) | ✅ |
| [Подборки и миксы](features/picks-and-mixes/) | ✅ |
| [Просмотр каталога (Browse)](features/browse/) | ✅ |
| [Качество звука до Lossless FLAC](features/audio-quality/) | ✅ |
| Несколько аккаунтов одновременно | ✅ |

| Параметр | Значение |
|:---------|:---------|
| Максимальное качество | Lossless FLAC (с подпиской KION) |
| Способ входа | X-Auth-Token |

Инструкция по подключению — на странице [Настройка](configuration/).

Полный список проблем — на странице [Известные проблемы](known-issues/).

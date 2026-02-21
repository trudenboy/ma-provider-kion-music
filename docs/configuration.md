[← Back to README](../README.md)

# Configuration

All settings are accessible via **Settings → Music Sources → KION Music**.

## Options

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `token` | Secure string | — | KION Music OAuth token. Required for authentication. See below for how to obtain it. |
| `quality` | String (enum) | `high` | Preferred audio quality. See [Quality Options](#quality-options) below. |
| `base_url` | String | `https://music.mts.ru/ya_proxy_api` | API endpoint base URL. Change only if KION updates their endpoint. Advanced. |

### Quality Options

| Value | Label | Format | Bitrate |
|-------|-------|--------|---------|
| `high` | High | MP3 | 320 kbps |
| `lossless` | Lossless | FLAC | Lossless |

## Obtaining a Token

KION Music requires an OAuth token. The provider documentation at
<https://music-assistant.io/music-providers/kion-music/> explains how to obtain one.

## Actions

| Action | Description |
|--------|-------------|
| Reset authentication | Clears the stored token, allowing you to re-enter credentials. |

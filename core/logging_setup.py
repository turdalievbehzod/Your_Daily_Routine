from __future__ import annotations

import json
import logging
from datetime import datetime
from urllib import parse, request

from core.config import BOT_TOKEN, CHANNEL_ID


class TelegramLogHandler(logging.Handler):
    """Отправляет логи в Telegram-канал через Bot API."""

    def emit(self, record: logging.LogRecord) -> None:
        try:
            message = self.format(record)
            payload = parse.urlencode(
                {
                    "chat_id": CHANNEL_ID,
                    "text": message[:3900],
                    "disable_web_page_preview": True,
                }
            ).encode()
            req = request.Request(
                url=f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
                data=payload,
                method="POST",
            )
            request.urlopen(req, timeout=5)
        except Exception:
            # Никогда не ломаем приложение из-за логирования
            pass


def setup_logging() -> logging.Logger:
    logger = logging.getLogger("ydr")
    logger.setLevel(logging.INFO)

    if logger.handlers:
        return logger

    fmt = logging.Formatter(
        fmt="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(fmt)

    tg_handler = TelegramLogHandler()
    tg_handler.setFormatter(fmt)

    logger.addHandler(stream_handler)
    logger.addHandler(tg_handler)
    logger.info("Logging initialized at %s", datetime.utcnow().isoformat())
    return logger

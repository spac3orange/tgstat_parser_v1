from loguru import logger

logger.add("logs/main.log", rotation="100 MB", encoding='utf-8', level="INFO")
logger.add("logs/error.log", rotation="100 MB", encoding='utf-8', level="ERROR")
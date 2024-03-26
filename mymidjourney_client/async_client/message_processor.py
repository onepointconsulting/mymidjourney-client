from typing import Union

import asyncio

from mymidjourney_client.log_factory import logger
from mymidjourney_client.model.error import Error
from mymidjourney_client.model.message_result import MessageResult
from mymidjourney_client.async_client.message import message_request


async def message_processor(
    message_id: str, max_tries: int = 20, sleep: int = 10
) -> Union[MessageResult, Error]:
    counter = 0
    while counter < max_tries:
        counter += 1
        message_result = await message_request(message_id)
        if isinstance(message_result, Error):
            logger.info("Error occurred: %s", message_result)
            return message_result
        else:
            if message_result.progress and message_result.progress >= 100:
                logger.info(f"Image available at {message_result.uri}")
                return message_result
            else:
                logger.info(f"progress: {message_result.progress}")
                await asyncio.sleep(sleep)

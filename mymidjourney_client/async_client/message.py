from typing import Union

from mymidjourney_client.model.message_result import (
    MessageResult,
    convert_from_obj,
)
from mymidjourney_client.model.error import Error
from mymidjourney_client.async_client.request_support import handle_get_call


async def message_request(message_id: str) -> Union[MessageResult, Error]:
    response = await handle_get_call(f"message/{message_id}")
    if isinstance(response, dict):
        return convert_from_obj(response)
    else:
        return response


if __name__ == "__main__":
    import asyncio
    import time
    from mymidjourney_client.async_client.imagine import imagine_request
    from mymidjourney_client.model.imagine_result import ImagineResult

    res = asyncio.run(
        imagine_request(
            "Generate a picture of a beautiful oriental deity in photorealistic style."
        )
    )
    if isinstance(res, ImagineResult):
        imagine_result: ImagineResult = res
        message_id = res.message_id
        if message_id:
            while True:
                message_result = asyncio.run(message_request(message_id))
                if isinstance(message_result, Error):
                    print("Error occurred", message_request)
                    break
                else:
                    if message_result.progress and message_result.progress >= 100:
                        print(f"Image available at {message_result.uri}")
                        break
                    else:
                        print(f"progress: {message_result.progress}")
                        time.sleep(10)
    else:
        print("Error", res)

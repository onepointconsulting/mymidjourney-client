from typing import Union
from datetime import datetime

from mymidjourney_client.model.error import Error
from mymidjourney_client.model.imagine_result import ImagineResult
from mymidjourney_client.async_client.request_support import handle_post_call
from mymidjourney_client.model.imagine_result import convert_From_json


async def imagine_request(prompt: str) -> Union[ImagineResult, Error]:
    res_obj = await handle_post_call({"prompt": prompt}, endpoint="imagine")
    if isinstance(res_obj, dict):
        return convert_From_json(res_obj)
    return res_obj


if __name__ == "__main__":
    import asyncio

    res = asyncio.run(
        imagine_request(
            "Generate a picture of a beautiful oriental deity in photorealistic style."
        )
    )
    if isinstance(res, ImagineResult):
        print(res)
    else:
        print("Error", res)

from typing import Union
import aiohttp
from aiohttp.client_reqrep import ClientResponse

from mymidjourney_client.model.error import Error

from mymidjourney_client.common import header_factory, END_POINT_BASE


async def handle_post_call(data: dict, endpoint: str) -> Union[dict, Error]:
    async with aiohttp.ClientSession() as session:
        async with session.post(
            f"{END_POINT_BASE}/{endpoint}", json=data, headers=header_factory()
        ) as resp:
            return await handle_response(resp)


async def handle_get_call(endpoint: str) -> Union[dict, Error]:
    async with aiohttp.ClientSession() as session:
        async with session.get(
            f"{END_POINT_BASE}/{endpoint}", headers=header_factory()
        ) as resp:
            return await handle_response(resp)


async def handle_response(resp: ClientResponse) -> Union[dict, Error]:
    if resp.status >= 200 and resp.status < 300:
        json_res = await resp.json()
        return json_res
    else:
        return Error(code=resp.status, message=await resp.text())

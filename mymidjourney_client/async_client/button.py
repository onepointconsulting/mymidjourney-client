from typing import Union

from mymidjourney_client.model.imagine_result import ImagineResult
from mymidjourney_client.model.error import Error
from mymidjourney_client.async_client.request_support import handle_post_call
from mymidjourney_client.model.imagine_result import convert_From_json


async def button_request(message_id: str, button: str) -> Union[ImagineResult, Error]:
    data = {"messageId": message_id, "button": button}
    res_obj = await handle_post_call(data, endpoint="button")
    return convert_From_json(res_obj)


if __name__ == "__main__":
    import asyncio

    from mymidjourney_client.async_client.imagine import imagine_request
    from mymidjourney_client.model.imagine_result import ImagineResult
    from mymidjourney_client.async_client.message_processor import message_processor

    res = asyncio.run(
        imagine_request(
            "Generate a picture of a beautiful deity with Indian features."
        )
    )
    if isinstance(res, ImagineResult):
        imagine_result: ImagineResult = res
        message_id = res.message_id
        message_result = asyncio.run(message_processor(message_id))
        if isinstance(message_result, Error):
            print("Error:", message_result)
        else:
            message_id = message_result.message_id
            buttons = message_result.buttons
            # Press first
            if len(buttons) > 0:
                button_result = asyncio.run(button_request(message_id, buttons[0]))
                if isinstance(button_result, Error):
                    print("Button error", button_result)
                else:
                    message_result = asyncio.run(
                        message_processor(button_result.message_id)
                    )
                    print("Upscaled image", message_result.uri)

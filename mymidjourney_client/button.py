from typing import Union

from mymidjourney_client.model.imagine_result import ImagineResult
from mymidjourney_client.model.error import Error
from mymidjourney_client.common import header_factory, END_POINT_BASE
from mymidjourney_client.imagine import process_response


def button_request(message_id: str, button: str) -> Union[ImagineResult, Error]:
    data = {"messageId": message_id, "button": button}
    headers = header_factory()
    return process_response(data, headers, f"{END_POINT_BASE}/button")

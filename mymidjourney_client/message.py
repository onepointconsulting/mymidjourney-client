from typing import Union

import requests

from mymidjourney_client.common import (
    header_factory,
    END_POINT_BASE,
    handle_error,
)
from mymidjourney_client.model.message_result import (
    MessageResult,
    convert_from_str,
)
from mymidjourney_client.model.error import Error


def message_request(message_id: str) -> Union[MessageResult, Error]:
    headers = header_factory()
    response = requests.get(f"{END_POINT_BASE}/message/{message_id}", headers=headers)

    def success_func(response: requests.models.Response):
        return convert_from_str(response.text)

    return handle_error(response, success_func)


if __name__ == "__main__":
    from mymidjourney_client.imagine import imagine_request
    import time

    imagine_result = imagine_request(
        "Can you please picture of an ancient idol in a lost Hindu temple"
    )
    if type(imagine_result) == Error:
        print(f"Error: {imagine_result}")
    else:
        print(f"Success: {imagine_result}")
        message_id = imagine_result.message_id
        if message_id:
            while True:
                message_result = message_request(message_id)
                if type(message_result) == Error:
                    print(
                        f"Failed to get the status of the generated image {message_result}"
                    )
                else:
                    if message_result.progress >= 100:
                        print(message_result)
                        print(f"Image available at {message_result.uri}")
                        break
                    else:
                        print(f"progress: {message_result.progress}")
                        time.sleep(10)

from typing import Union
import time

from mymidjourney_client.imagine import imagine_request
from mymidjourney_client.model.error import Error
from mymidjourney_client.model.message_result import MessageResult
from mymidjourney_client.model.imagine_result import ImagineResult
from mymidjourney_client.message import message_request
from mymidjourney_client.log_factory import logger
from mymidjourney_client.config import midjourney_cfg
from mymidjourney_client.button import button_request
from mymidjourney_client.utils.download_folder import download_image


def imagine_and_message(prompt: str) -> Union[MessageResult, Error]:
    imagine_result = imagine_request(prompt)
    return handle_imagine_result_message(imagine_result)


def handle_imagine_result_message(
    imagine_result: ImagineResult,
) -> Union[MessageResult, Error]:
    if type(imagine_result) == Error:
        return imagine_result
    else:
        logger.info(f"Success: {imagine_result}")
        message_id = imagine_result.message_id
        if message_id:
            return attempt_message_result(message_id)


def button_and_message(message_id: str, button: str) -> Union[MessageResult, Error]:
    imagine_result = button_request(message_id, button)
    return handle_imagine_result_message(imagine_result)


def attempt_message_result(message_id: str) -> Union[MessageResult, Error]:
    for attempt in range(midjourney_cfg.message_attempts):
        logger.info(f"Message attempt: {attempt}")
        message_result = message_request(message_id)
        if type(message_result) == Error:
            logger.info(
                f"Failed to get the status of the generated image {message_result}"
            )
            return message_result
        else:
            if message_result.progress and message_result.progress >= 100:
                logger.info(message_result)
                logger.info(f"Image available at {message_result.uri}")
                return message_result
            else:
                logger.info(f"progress: {message_result.progress}")
                time.sleep(midjourney_cfg.sleep_time)


def process_image_download(uri: str):
    print(f"Generated URI: {message_result.uri}")
    downloaded_image = download_image(uri, midjourney_cfg.temp_dir)
    if downloaded_image is not None:
        print(f"Image downloaded to {downloaded_image}")


if __name__ == "__main__":
    import sys

    prompt = input("Please enter your image prompt: ")

    if len(prompt) < 10:
        print("The prompt is too short.")
        sys.exit(2)

    message_result = imagine_and_message(prompt)
    if type(message_result) == Error:
        print(f"Error occurred during imagine phase: {message_result}")
        sys.exit(1)

    process_image_download(message_result.uri)

    print("Here are the buttons")
    for b in message_result.buttons:
        print(b)
    while True:
        selected_button = input("Please select a button: ")
        if not selected_button in message_result.buttons:
            print(f"Could not find button {selected_button}")
            continue
        button_message_result = button_and_message(
            message_result.message_id, selected_button
        )
        if type(button_message_result) == Error:
            print(
                f"An error has occurred in button generation: {button_message_result}"
            )
            continue

        process_image_download(button_message_result.uri)

        continue_response = input("Would you like to click on other buttons? (Y/n) ")
        if continue_response.lower() in ("y", "ye", "yes"):
            continue
        break

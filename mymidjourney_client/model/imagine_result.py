import json
from datetime import datetime

from dataclasses import dataclass


@dataclass
class ImagineResult:
    success: bool
    message_id: str
    created_at: datetime


def convert_from_str(json_str: str) -> ImagineResult:
    res_obj = json.loads(json_str)
    return convert_From_json(res_obj)


def convert_From_json(res_obj: dict) -> ImagineResult:
    return ImagineResult(
        success=res_obj["success"],
        message_id=res_obj["messageId"],
        created_at=datetime.fromisoformat(res_obj["createdAt"]),
    )

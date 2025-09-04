from dataclasses import dataclass, asdict
from typing import Any, Optional

# ---------------- Constants ----------------
ERROR = 0
SUCCESS = 1


# ---------------- Data Structures ----------------
@dataclass
class ResponseCommon:
    code: int
    msg: str
    data: Optional[Any] = None


@dataclass
class ResponseSuccess:
    code: int
    msg: str
    timestamp: str
    data: Optional[Any] = None
    sign: str = ""


@dataclass
class Response:
    code: int
    data: Any
    msg: str


# ---------------- Utility Functions ----------------
def result(code: int, data: Any, msg: str) -> dict:
    """Return common JSON dict"""
    return asdict(Response(code=code, data=data, msg=msg))


def ok() -> dict:
    return result(SUCCESS, {}, "operate success")


def ok_with_message(message: str) -> dict:
    return result(SUCCESS, {}, message)


def ok_with_data(data: Any) -> dict:
    return result(SUCCESS, data, "operate success")


def ok_detailed(data: Any, message: str) -> dict:
    return result(SUCCESS, data, message)


def fail() -> dict:
    return result(ERROR, {}, "operate fail")


def fail_with_message(message: str) -> dict:
    return result(ERROR, {}, message)


def fail_with_detailed(code: int, data: Any, message: str) -> dict:
    return result(code, data, message)

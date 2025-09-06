import base64
import hashlib
import json
import logging
from typing import Dict, Any
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa, padding, utils
from cryptography.hazmat.backends import default_backend


def compose_params(params: Dict[str, str]) -> str:
    """Compose parameters, remove sign, sort by key"""
    keys = sorted(k for k in params.keys() if k != "sign")
    return "&".join(f"{k}={params[k]}" for k in keys)


def struct_to_dict(obj: Any) -> Dict[str, str]:
    """
    Convert object to dict (only supports string fields)
    """
    result = {}
    for key, value in obj.__dict__.items():
        if isinstance(value, str):
            result[key] = value
        else:
            raise TypeError(f"unsupported field type: {type(value)}")
    return result


def load_private_key_from_base64(b64_str: str) -> rsa.RSAPrivateKey:
    """Load private key from base64 (PKCS8)"""
    try:
        key_bytes = base64.b64decode(b64_str)
        private_key = serialization.load_der_private_key(
            key_bytes,
            password=None,
            backend=default_backend()
        )
        if not isinstance(private_key, rsa.RSAPrivateKey):
            raise ValueError("Not an RSA private key")
        return private_key
    except Exception as e:
        raise ValueError(f"load_private_key_from_base64 error: {e}")


def sign_data(private_key: rsa.RSAPrivateKey, data: str) -> str:
    """Sign with RSA private key and MD5"""
    md5_hash = hashlib.md5(data.encode("utf-8")).digest()

    signature = private_key.sign(
        md5_hash,
        padding.PKCS1v15(),
        utils.Prehashed(hashes.MD5())
    )
    return base64.b64encode(signature).decode("utf-8")


def verify_signature(public_key: rsa.RSAPublicKey, data: str, signature: str) -> None:
    """Verify signature with RSA public key and MD5"""
    try:
        decoded_sig = base64.b64decode(signature)
        md5_hash = hashlib.md5(data.encode("utf-8")).digest()
        public_key.verify(
            decoded_sig,
            md5_hash,
            padding.PKCS1v15(),
            utils.Prehashed(hashes.MD5())
        )
    except Exception as e:
        raise ValueError(f"signature verification failed: {e}")


def parse_public_key(b64_str: str) -> rsa.RSAPublicKey:
    """Load public key from base64 (PKIX)"""
    try:
        key_bytes = base64.b64decode(b64_str)
        public_key = serialization.load_der_public_key(
            key_bytes,
            backend=default_backend()
        )
        if not isinstance(public_key, rsa.RSAPublicKey):
            raise ValueError("Parsed key is not RSA public key")
        return public_key
    except Exception as e:
        raise ValueError(f"parse_public_key error: {e}")

def value_as_string(element: Any) -> str:
    """
    Recursively convert JSON value to string, supporting str/int/float/bool/object/array/None
    """
    if element is None:
        return ""
    elif isinstance(element, bool):
        return "true" if element else "false"
    elif isinstance(element, (int, float)):
        return str(element)
    elif isinstance(element, str):
        return element
    elif isinstance(element, dict):
        # 按 key 排序，忽略大小写
        sorted_keys = sorted(element.keys(), key=lambda x: x.lower())
        return "".join(value_as_string(element[k]) for k in sorted_keys)
    elif isinstance(element, list):
        # 遍历数组，递归处理
        buffer = []
        for item in element:
            if isinstance(item, dict):
                # 保持对象顺序，但先按 key 排序再拼接值
                sorted_keys = sorted(item.keys(), key=lambda x: x.lower())
                buffer.append("".join(value_as_string(item[k]) for k in sorted_keys))
            else:
                buffer.append(value_as_string(item))
        return "".join(buffer)
    else:
        return ""


def to_string_map(j_str: bytes) -> Dict[str, str]:
    """
    :param j_str: JSON bytes
    :return: dict[str, str]
    """
    res_map: Dict[str, str] = {}
    try:
        json_object: Dict[str, Any] = json.loads(j_str.decode("utf-8"))
        for key, value in json_object.items():
            res_map[key] = value_as_string(value)
    except Exception:
        pass
    return res_map

def value_as_string_new(element):
    """
    Try to parse a JSON element into different types and return its string representation.
    """

    # If it's JSON null
    if element == "null" or element is None:
        return ""

    # Try parsing as bool
    try:
        as_bool = json.loads(element)
        if isinstance(as_bool, bool):
            return str(as_bool).lower()  # match Go's strconv.FormatBool
    except Exception:
        pass

    # Try parsing as number (int or float)
    try:
        as_number = json.loads(element)
        if isinstance(as_number, (int, float)):
            return str(as_number)
    except Exception:
        pass

    # Try parsing as string
    try:
        as_string = json.loads(element)
        if isinstance(as_string, str):
            return as_string
    except Exception:
        pass

    # Try parsing as object (dict)
    try:
        as_object = json.loads(element)
        if isinstance(as_object, dict):
            keys = sorted(as_object.keys(), key=lambda x: x.lower())
            buffer = []
            for k in keys:
                buffer.append(value_as_string_new(json.dumps(as_object[k])))
            return "".join(buffer)
    except Exception:
        pass

    # Try parsing as array (list)
    try:
        as_array = json.loads(element)
        if isinstance(as_array, list):
            buffer = []
            for item in as_array:
                buffer.append(value_as_string_new(json.dumps(item)))
            return "".join(buffer)
    except Exception:
        pass

    return ""

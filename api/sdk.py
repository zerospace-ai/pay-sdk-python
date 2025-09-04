from dataclasses import dataclass
import hashlib
import json
import time

from pay_sdk_python.request_define import request_define
from pay_sdk_python.rsa_utils import (compose_params, load_private_key_from_base64, sign_data,
                                          parse_public_key, verify_signature, struct_to_dict)


@dataclass
class SDKConfig:
    ApiKey: str
    ApiSecret: str
    PlatformPubKey: str
    PlatformRiskPubKey: str
    RsaPrivateKey: str


class Sdk:
    def __init__(self, conf: SDKConfig):
        self.config = conf

    @staticmethod
    def NewSDK(conf: SDKConfig) -> "Sdk":
        return Sdk(conf)

    def InitSDK(self) -> Exception | None:
        return None

    def GetApiKey(self) -> str:
        return self.config.ApiKey

    def generate_md5_sign(self, data_str: str, timestamp: str) -> str:
        str_to_hash = self.config.ApiSecret + data_str + timestamp
        md5_hash = hashlib.md5(str_to_hash.encode("utf-8"))
        return md5_hash.hexdigest()

    def generate_rsa_signature(self, map_data: dict[str, str]) -> str:
        """Sign parameters using the configured private key"""
        raw_str = compose_params(map_data)
        private_key = load_private_key_from_base64(self.config.RsaPrivateKey)
        return sign_data(private_key, raw_str)

    def verify_rsa_signature(self, map_data: dict[str, str], sign: str) -> None:
        """Verify signature using the platform public key"""
        raw_str = compose_params(map_data)
        public_key = parse_public_key(self.config.PlatformPubKey)
        verify_signature(public_key, raw_str, sign)

    def verify_risk_rsa_signature(self, map_data: dict[str, str], sign: str) -> None:
        """Verify signature using the risk control public key"""
        raw_str = compose_params(map_data)
        public_key = parse_public_key(self.config.PlatformRiskPubKey)
        verify_signature(public_key, raw_str, sign)

    def sign_pack(self, req: object) -> tuple[bytes, str, str, str]:
        """
        :param req: Any object (with __dict__ or dataclass)
        :return: (json_bytes, timestamp, md5_sign, rsa_sign)
        """
        timestamp = ""
        md5_sign = ""
        rsa_sign = ""

        # 1. Convert struct to map
        try:
            map_data = struct_to_dict(req)
        except Exception as e:
            raise ValueError(f"struct_to_dict error: {e}")

        # 2. Compose parameters
        data_str = compose_params(map_data)

        # 3. Millisecond timestamp
        timestamp = str(int(time.time() * 1000))

        # 4. MD5 signature
        md5_sign = self.generate_md5_sign(data_str, timestamp)

        # 5. Convert to JSON
        try:
            j_str = json.dumps(req.__dict__, ensure_ascii=False).encode("utf-8")
        except Exception as e:
            raise ValueError(f"json.dumps error: {e}")

        # 6. Convert JSON to dict
        try:
            req_map_obj = json.loads(j_str.decode("utf-8"))
            # Ensure all values are strings
            req_map_obj = {k: str(v) for k, v in req_map_obj.items()}
        except Exception as e:
            raise ValueError(f"json to dict error: {e}")

        # 7. RSA signature
        try:
            rsa_sign = self.generate_rsa_signature(req_map_obj)
        except Exception as e:
            raise ValueError(f"generate_rsa_signature error: {e}")

        return j_str, timestamp, md5_sign, rsa_sign

    # CreateUser create user
    # @param open_id: user open id
    # @return data, timestamp, sign, client_sign, error
    def CreateUser(self, open_id: str):
        return self.sign_pack(
            request_define.ReqCreateUser(
                OpenId=open_id,
            )
        )

    def CreateWallet(self, open_id: str, chain_Id: str):
        return self.sign_pack(
            request_define.ReqCreateWallet(
                OpenId=open_id,
                ChainID=chain_Id
            )
        )

    def GetWalletAddr(self, open_id: str, chain_IDs: str):
        return self.sign_pack(
            request_define.ReqGetWalletAddr(
                OpenId=open_id,
                ChainIDs=chain_IDs
            )
        )

    def UserWithdrawByOpenID(self, open_id: str, token_id: str, amount: str, address_to: str, callback_url: str, safe_check_code: str):
        return self.sign_pack(
            request_define.ReqWithdrawByOpenID(
                OpenId=open_id,
                TokenId=token_id,
                Amount=amount,
                AddressTo=address_to,
                CallBackUrl=callback_url,
                SafeCheckCode=safe_check_code
            )
        )

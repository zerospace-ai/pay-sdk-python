import json
import logging
import requests
import yaml

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from pay_sdk_python.api.sdk import Sdk, SDKConfig
from pay_sdk_python.response_define.response_common import SUCCESS
from pay_sdk_python.rsa_utils import to_string_map
from pay_sdk_python import constants


def main():
    logging.basicConfig(level=logging.INFO,
                        format="%(asctime)s [%(levelname)s] %(filename)s:%(lineno)d - %(message)s")

    client = requests.Session()

    config_path = os.path.join(os.path.dirname(__file__), '..', 'config.yaml')
    try:
        with open(config_path, "r", encoding="utf-8") as f:
            config = yaml.safe_load(f)
    except Exception as e:
        raise RuntimeError(f"Failed to load config: {e}")

    api_obj = Sdk(SDKConfig(
        ApiKey=config.get("ApiKey"),
        ApiSecret=config.get("ApiSecret"),
        PlatformPubKey=config.get("PlatformPubKey"),
        PlatformRiskPubKey=config.get("PlatformRiskPubKey"),
        RsaPrivateKey=config.get("RsaPrivateKey"),
    ))

    open_id = config.get("UserOpenId")
    chain_ids = config.get("ChainIDs")

    try:
        req_body, timestamp, sign, client_sign = api_obj.GetWalletAddr(open_id, chain_ids)
    except Exception as e:
        logging.warning("Error: %s", e)
        return

    final_url = constants.DEV_NET_ENDPOINT + constants.PATH_GET_WALLET_ADDRESSES

    try:
        resp = client.post(
            final_url,
            headers={
                "Content-Type": "application/json",
                "key": api_obj.GetApiKey(),
                "timestamp": timestamp,
                "sign": sign,
                "clientSign": client_sign,
            },
            data=req_body
        )
    except Exception as e:
        logging.warning("Error: %s", e)
        return

    body = resp.content
    print(body.decode('utf-8'))

    try:
        rsp_get_wallet_addresses = json.loads(body)
    except Exception as e:
        logging.warning("Error: %s", e)
        return
    logging.info("ResponseGetWalletAddresses: %s", rsp_get_wallet_addresses)

    if rsp_get_wallet_addresses.get("code") != SUCCESS:
        logging.warning("Response fail Code %s Msg %s",
                        rsp_get_wallet_addresses.get("code"), rsp_get_wallet_addresses.get("msg"))
        return

    strSign = rsp_get_wallet_addresses.get("sign")
    if strSign != "":
        map_obj = to_string_map(body)
        try:
            api_obj.verify_rsa_signature(map_obj, strSign)
        except Exception as e:
            logging.warning("Error: %s", e)
            return

        logging.info("VerifyRSAsignature success")


if __name__ == "__main__":
    main()

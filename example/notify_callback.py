import json
import logging
import yaml
import time
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from flask import Flask, request, jsonify
from pay_sdk_python.api.sdk import Sdk, SDKConfig
from pay_sdk_python.rsa_utils import to_string_map

def main():
    logging.basicConfig(level=logging.INFO,
                        format="%(asctime)s [%(levelname)s] %(filename)s:%(lineno)d - %(message)s")

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

    app = Flask(__name__)

    @app.route('/withdraw_callback', methods=['POST'])
    def withdraw_callback():
        try:
            body = request.get_data()
            print("Raw JSON:", body.decode('utf-8'))

            """
            @dataclass
            class RequestTokenCb:
                openid: str
                totalvalue: str
                amount: str
                chainid: str
                confirm: str
                createdtime: str
                from: str
                safecode: str
                sign: str
                status: str
                timestamp: str
                to: str
                tokenaddress: str
                tokenid: str
                type: str
                fee: str
                hash: str = field(default="")
            """

            req = json.loads(body)

            map_obj = to_string_map(body)

            err = api_obj.verify_rsa_signature(map_obj, req.get('sign'))
            if err:
                logging.warning("VerifyRSAsignature fail, err %s", err)
                return jsonify({"message": f"verify RSA signature fail {err}"}), 400

            logging.info(req)

            timestamp = str(int(time.time()))

            rsp = {
                "code": "0",
                "timestamp": timestamp,
                "message": "",
                "sign": ""
            }

            j_str = json.dumps(req).encode('utf-8')
            req_map_obj = to_string_map(j_str)

            client_sign, err = api_obj.generate_rsa_signature(req_map_obj)
            if err:
                logging.warning("api_obj.GenerateRSASignature fail, err %s", err)
                return jsonify({"message": f"GenerateRSASignature fail {err}"}), 500

            rsp["sign"] = client_sign

            logging.info("VerifyRSAsignature success.")
            return jsonify(rsp), 200

        except Exception as e:
            logging.warning("Error: %s", e)
            return jsonify({"message": str(e)}), 400

    app.run(port=9003)

if __name__ == "__main__":
    main()

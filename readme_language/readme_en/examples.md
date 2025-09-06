# Examples 📝

This document provides usage examples for the CryptoPay Python SDK, including Demo running, key generation, and callback handling.

## 1 SDK Instance Object 🛠️

### 1.1 Required Configuration ⚙️

1. Register your business name and obtain the `ApiKey` and `ApiSecret`;

2. Generate your own `RSA` key pair;

3. Prepare the platform's `RSA` public key;

### 1.2 Creating a Signature Object 🔏

1. Add a configuration file `config.yaml`.

```yaml
# Configure business information
ApiKey: ""
ApiSecret: ""
# Platform public key
PlatformPubKey: ""
# Public key for blocking the platform
PlatformRiskPubKey: ""
# Your own private key
RsaPrivateKey: ""
```

2. Load the configuration file and create the API object.

```python

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

```


### 1.3 Create and sign the request data. ✍️

Let's use user creation as an example.

```python

    open_id = config.get("UserOpenId")

    try:
        req_body, timestamp, sign, client_sign = api_obj.CreateUser(open_id)
    except Exception as e:
        logging.warning("Error: %s", e)
        return

```

```python
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
```

### 1.4 Filling in and Initiating the Request 🚀

```python
    final_url = constants.DEV_NET_ENDPOINT + constants.PATH_CREATE_USER

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

```

### 1.5 Verify parsing return data ✅

```python
    try:
        rsp_create_user = json.loads(body)
    except Exception as e:
        logging.warning("Error: %s", e)
        return
    logging.info("ResponseCreateUser: %s", rsp_create_user)

    if rsp_create_user.get("code") != SUCCESS:
        logging.warning("Response fail Code %s Msg %s",
                        rsp_create_user.get("code"), rsp_create_user.get("msg"))
        return

    map_obj = to_string_map(body)
    try:
        api_obj.verify_rsa_signature(map_obj, rsp_create_user.get("sign"))
    except Exception as e:
        logging.warning("Error: %s", e)
        return

    logging.info("VerifyRSAsignature success")

```

## 2. Run commands 📞

### 2.1. Register a new user 🆕

Go into the **pay\_sdk\_python/** directory of the SDK and modify the **UserOpenId** field in the **config.yaml** file.

Then run `python3 example/create_user.py` to register a new user on the platform.

If you attempt to register a **UserOpenId** that has already been registered, an error will be returned.

### 2.2. Wallet registration 💼

Go into the **pay\_sdk\_python/** directory and specify the **UserOpenId** and **ChainID** fields in the **config.yaml** file.

Then run `python3 example/create_wallet.py` to complete the user's wallet registration on the platform.

### 2.3. Get deposit address 📍

Go into the **pay\_sdk\_python/** directory and specify the **UserOpenId** and **ChainIDs** fields in the **config.yaml** file.

Then run `python3 example/get_wallet_addreses.py`.

### 2.4. Withdrawal 💸

Go into the **pay\_sdk\_python/** directory and specify the **UserOpenId**, **TokenId**, **Amount**, **AddressTo**, **SafeCheckCode**, and **CallbackUrl** fields in the **config.yaml** file.

Then run `python3 example/user_withdraw_by_open_id.py`.

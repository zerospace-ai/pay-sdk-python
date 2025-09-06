# 範例 📝

本文件提供 CryptoPay Python SDK 的使用範例，包括 Demo 運行、金鑰生成和回調處理。

## 1 SDK 實例物件 🛠️

### 1.1 所需配置 ⚙️

1. 註冊您的業務名稱並獲取 `ApiKey` 和 `ApiSecret`；

2. 生成您自己的 `RSA` 金鑰對；

3. 準備平台的 `RSA` 公鑰；

### 1.2 創建簽名物件 🔏

1. 添加配置文件 `config.yaml`。

```yaml
# 配置業務信息
ApiKey: ""
ApiSecret: ""
# 平台公鑰
PlatformPubKey: ""
# 用於封鎖平台的公鑰
PlatformRiskPubKey: ""
# 您自己的私鑰
RsaPrivateKey: ""
```

2. 加載配置文件並創建 API 物件。

```

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

### 1.3 創建並簽名請求數據。 ✍️

讓我們以用戶創建為例。

```

    open_id = config.get("UserOpenId")

    try:
        req_body, timestamp, sign, client_sign = api_obj.CreateUser(open_id)
    except Exception as e:
        logging.warning("Error: %s", e)
        return

```

```
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

### 1.4 填充並發起請求 🚀

```
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

### 1.5 驗證解析返回數據 ✅

```
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

## 2. 執行命令 📞

### 2.1. 註冊新使用者 🆕

進入 SDK 的 **pay\_sdk\_python/** 目錄，在其中的 **config.yaml** 檔案裡修改 **UserOpenId** 欄位。

接著執行 `python3 example/create_user.py` 來在平台上註冊一個新使用者。

如果嘗試註冊已經註冊過的 **UserOpenId**，將會回傳錯誤。

### 2.2. 錢包註冊 💼

進入 SDK 的 **pay\_sdk\_python/** 目錄，在 **config.yaml** 檔案中填寫 **UserOpenId** 和 **ChainID** 欄位。

接著執行 `python3 example/create_wallet.py` 來完成使用者在平台上的錢包註冊。

### 2.3. 取得充值地址 📍

進入 SDK 的 **pay\_sdk\_python/** 目錄，在 **config.yaml** 檔案中填寫 **UserOpenId** 和 **ChainIDs** 欄位。

接著執行 `python3 example/get_wallet_addreses.py`。

### 2.4. 提現 💸

進入 SDK 的 **pay\_sdk\_python/** 目錄，在 **config.yaml** 檔案中填寫 **UserOpenId**、**TokenId**、**Amount**、**AddressTo**、**SafeCheckCode** 和 **CallbackUrl** 欄位。

接著執行 `python3 example/user_withdraw_by_open_id.py`。

# 示例 📝

本文档提供了 CryptoPay Python SDK 的使用示例，包括 Demo 运行、密钥生成和回调处理。

## 1 SDK 实例对象 🛠️

### 1.1 所需配置 ⚙️

1. 注册您的业务名称并获取 `ApiKey` 和 `ApiSecret`；

2. 生成您自己的 `RSA` 密钥对；

3. 准备平台的 `RSA` 公钥；

### 1.2 创建签名对象 🔏

1. 添加配置文件 `config.yaml`。

```yaml
# 配置业务信息
ApiKey: ""
ApiSecret: ""
# 平台公钥
PlatformPubKey: ""
# 用于阻塞平台的公钥
PlatformRiskPubKey: ""
# 您自己的私钥
RsaPrivateKey: ""
```

2. 加载配置文件并创建 API 对象。

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

### 1.3 创建并签名请求数据。 ✍️

以用户创建为例。

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

### 1.4 填充并发起请求 🚀

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

### 1.5 验证解析返回数据 ✅

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

## 2. 调用命令 📞

### 2.1. 注册新用户 🆕

进入 SDK 的 pay_sdk_python/ 目录，在其中的 config.yaml 文件里修改 UserOpenId 字段。

然后运行 python3 example/create_user.py 来在平台上注册一个新用户。

如果尝试注册一个已经注册过的 UserOpenId，将会返回错误。


### 2.2. 钱包注册 💼

进入 SDK 的 pay_sdk_python/ 目录，在 config.yaml 文件中填写 UserOpenId 和 ChainID 字段。

然后运行 python3 example/create_wallet.py 来完成用户在平台上的钱包注册。

### 2.3. 获取充值地址 📍

进入 SDK 的 pay_sdk_python/ 目录，在 config.yaml 文件中填写 UserOpenId 和 ChainIDs 字段。

然后运行 python3 example/get_wallet_addreses.py。

### 2.4. 提现 💸

进入 SDK 的 pay_sdk_python/ 目录，在 config.yaml 文件中填写 UserOpenId、TokenId、Amount、AddressTo、SafeCheckCode 和 CallbackUrl 字段。

然后运行 python3 example/user_withdraw_by_open_id.py。

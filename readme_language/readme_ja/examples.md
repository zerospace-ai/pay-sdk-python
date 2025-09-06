# 例 📝

このドキュメントは、CryptoPay Python SDKの使用例を提供します。Demoの実行、キーの生成、およびコールバックの処理を含みます。

## 1 SDKインスタンスオブジェクト 🛠️

### 1.1 必要な設定 ⚙️

1. ビジネス名を登録し、`ApiKey` と `ApiSecret` を取得します；

2. 独自の `RSA` キーペアを生成します；

3. プラットフォームの `RSA` 公開鍵を準備します；

### 1.2 署名オブジェクトの作成 🔏

1. 設定ファイル `config.yaml` を追加します。

```yaml
# ビジネス情報を設定
ApiKey: ""
ApiSecret: ""
# プラットフォーム公開鍵
PlatformPubKey: ""
# プラットフォームのブロック公開鍵
PlatformRiskPubKey: ""
# 独自の秘密鍵
RsaPrivateKey: ""
```

2. 設定ファイルをロードし、APIオブジェクトを作成します。

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

### 1.3 リクエストデータの作成と署名 ✍️

ユーザー作成を例にします。

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

### 1.4 リクエストの入力と開始 🚀

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

### 1.5 返却データの検証と解析 ✅

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

## 2. コマンドを実行 📞

### 2.1. 新規ユーザー登録 🆕

SDK の **pay\_sdk\_python/** ディレクトリに移動し、**config.yaml** ファイルの **UserOpenId** フィールドを修正します。

その後、`python3 example/create_user.py` を実行してプラットフォームに新規ユーザーを登録します。

既に登録済みの **UserOpenId** を再登録しようとすると、エラーが返されます。

### 2.2. ウォレット登録 💼

**pay\_sdk\_python/** ディレクトリに移動し、**config.yaml** ファイルに **UserOpenId** と **ChainID** を記入します。

その後、`python3 example/create_wallet.py` を実行してユーザーのウォレット登録を完了します。

### 2.3. 入金アドレスの取得 📍

**pay\_sdk\_python/** ディレクトリに移動し、**config.yaml** ファイルに **UserOpenId** と **ChainIDs** を記入します。

その後、`python3 example/get_wallet_addreses.py` を実行します。

### 2.4. 出金 💸

**pay\_sdk\_python/** ディレクトリに移動し、**config.yaml** ファイルに **UserOpenId**、**TokenId**、**Amount**、**AddressTo**、**SafeCheckCode**、**CallbackUrl** を記入します。

その後、`python3 example/user_withdraw_by_open_id.py` を実行します。

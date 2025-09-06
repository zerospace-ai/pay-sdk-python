# 예시 📝

이 문서는 CryptoPay Python SDK의 사용 예시를 제공합니다. 데모 실행, 키 생성 및 콜백 처리 등을 포함합니다.

## 1 SDK 인스턴스 객체 🛠️

### 1.1 필수 구성 ⚙️

1. 비즈니스 이름을 등록하고 `ApiKey`와 `ApiSecret`을 얻습니다;

2. 자신의 `RSA` 키 쌍을 생성합니다;

3. 플랫폼의 `RSA` 공개 키를 준비합니다;

### 1.2 서명 객체 생성 🔏

1. 구성 파일 `config.yaml`을 추가합니다.

```yaml
# 비즈니스 정보 구성
ApiKey: ""
ApiSecret: ""
# 플랫폼 공개 키
PlatformPubKey: ""
# 플랫폼 차단용 공개 키
PlatformRiskPubKey: ""
# 자신의 개인 키
RsaPrivateKey: ""
```

2. 구성 파일을 로드하고 API 객체를 생성합니다.

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

### 1.3 요청 데이터 생성 및 서명 ✍️

사용자 생성을 예로 들어 보겠습니다.

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

### 1.4 요청 채우기 및 시작 🚀

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

### 1.5 반환 데이터 검증 및 파싱 ✅

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

## 2. 명령 실행 📞

### 2.1. 새 사용자 등록 🆕

SDK 의 **pay\_sdk\_python/** 디렉토리로 이동하여 **config.yaml** 파일의 **UserOpenId** 필드를 수정하세요.

그런 다음 `python3 example/create_user.py` 를 실행하여 플랫폼에 새 사용자를 등록합니다.

이미 등록된 **UserOpenId** 를 다시 등록하려고 하면 오류가 반환됩니다.

### 2.2. 지갑 등록 💼

**pay\_sdk\_python/** 디렉토리로 이동하여 **config.yaml** 파일에 **UserOpenId** 와 **ChainID** 를 입력하세요.

그런 다음 `python3 example/create_wallet.py` 를 실행하여 사용자의 지갑 등록을 완료합니다.

### 2.3. 입금 주소 가져오기 📍

**pay\_sdk\_python/** 디렉토리로 이동하여 **config.yaml** 파일에 **UserOpenId** 와 **ChainIDs** 를 입력하세요.

그런 다음 `python3 example/get_wallet_addreses.py` 를 실행합니다.

### 2.4. 출금 💸

**pay\_sdk\_python/** 디렉토리로 이동하여 **config.yaml** 파일에 **UserOpenId**, **TokenId**, **Amount**, **AddressTo**, **SafeCheckCode**, **CallbackUrl** 을 입력하세요.

그런 다음 `python3 example/user_withdraw_by_open_id.py` 를 실행합니다.

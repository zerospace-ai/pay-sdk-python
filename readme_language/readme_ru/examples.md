# Примеры 📝

Этот документ предоставляет примеры использования CryptoPay Python SDK, включая запуск Demo, генерацию ключей и обработку обратных вызовов.

## 1 Объект экземпляра SDK 🛠️

### 1.1 Необходимая конфигурация ⚙️

1. Зарегистрируйте название вашего бизнеса и получите `ApiKey` и `ApiSecret`;

2. Сгенерируйте свою собственную пару ключей `RSA`;

3. Подготовьте публичный ключ `RSA` платформы;

### 1.2 Создание объекта подписи 🔏

1. Добавьте файл конфигурации `config.yaml`.

```yaml
# Настройка информации о бизнесе
ApiKey: ""
ApiSecret: ""
# Публичный ключ платформы
PlatformPubKey: ""
# Публичный ключ для блокировки платформы
PlatformRiskPubKey: ""
# Ваш собственный приватный ключ
RsaPrivateKey: ""
```

2. Загрузите файл конфигурации и создайте объект API.

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

### 1.3 Создание и подпись данных запроса. ✍️

Возьмем создание пользователя в качестве примера.

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

### 1.4 Заполнение и инициирование запроса 🚀

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

### 1.5 Проверка и разбор возвращаемых данных ✅

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

## 2. Выполнение команд 📞

### 2.1. Регистрация нового пользователя 🆕

Перейдите в каталог **pay\_sdk\_python/** SDK и измените поле **UserOpenId** в файле **config.yaml**.

Затем выполните `python3 example/create_user.py`, чтобы зарегистрировать нового пользователя на платформе.

Если вы попытаетесь зарегистрировать уже существующий **UserOpenId**, будет возвращена ошибка.

### 2.2. Регистрация кошелька 💼

Перейдите в каталог **pay\_sdk\_python/** и укажите поля **UserOpenId** и **ChainID** в файле **config.yaml**.

Затем выполните `python3 example/create_wallet.py`, чтобы завершить регистрацию кошелька пользователя на платформе.

### 2.3. Получение адреса для пополнения 📍

Перейдите в каталог **pay\_sdk\_python/** и укажите поля **UserOpenId** и **ChainIDs** в файле **config.yaml**.

Затем выполните `python3 example/get_wallet_addreses.py`.

### 2.4. Вывод средств 💸

Перейдите в каталог **pay\_sdk\_python/** и укажите поля **UserOpenId**, **TokenId**, **Amount**, **AddressTo**, **SafeCheckCode**, **CallbackUrl** в файле **config.yaml**.

Затем выполните `python3 example/user_withdraw_by_open_id.py`.

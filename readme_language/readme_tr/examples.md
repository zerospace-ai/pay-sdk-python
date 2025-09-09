# Örnekler 📝

Bu belge, CryptoPay Python SDK'sı için kullanım örnekleri sağlar, Demo çalıştırma, anahtar üretimi ve geri arama işleme dahil.

## 1 SDK Örnek Nesnesi 🛠️

### 1.1 Gerekli Yapılandırma ⚙️

1. İşletme adınızı kaydedin ve `ApiKey` ve `ApiSecret` elde edin;

2. Kendi `RSA` anahtar çiftinizi üretin;

3. Platformun `RSA` genel anahtarını hazırlayın;

### 1.2 İmza Nesnesi Oluşturma 🔏

1. Bir yapılandırma dosyası `config.yaml` ekleyin.

```yaml
# İşletme bilgilerini yapılandırın
ApiKey: ""
ApiSecret: ""
# Platform genel anahtarı
PlatformPubKey: ""
# Platformu engellemek için genel anahtar
PlatformRiskPubKey: ""
# Kendi özel anahtarınız
RsaPrivateKey: ""
```

2. Yapılandırma dosyasını yükleyin ve API nesnesini oluşturun.

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

### 1.3 İstek Verilerini Oluşturma ve İmzalama ✍️

Kullanıcı oluşturmayı örnek olarak kullanalım.

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

### 1.4 İsteği Doldurma ve Başlatma 🚀

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

### 1.5 Dönüş Verilerini Doğrulama ve Ayrıştırma ✅

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

## 2. Komutları çalıştırın 📞

### 2.1. Yeni kullanıcı kaydı 🆕

SDK'nın **pay\_sdk\_python/** dizinine gidin ve **config.yaml** dosyasında **UserOpenId** alanını değiştirin.

Sonra `python3 example/create_user.py` çalıştırarak platformda yeni bir kullanıcı kaydedin.

Zaten kayıtlı bir **UserOpenId** tekrar kaydedilmeye çalışılırsa hata döner.

### 2.2. Cüzdan kaydı 💼

**pay\_sdk\_python/** dizinine gidin ve **config.yaml** dosyasında **UserOpenId** ve **ChainID** alanlarını belirtin.

Sonra `python3 example/create_wallet.py` çalıştırarak kullanıcının cüzdan kaydını tamamlayın.

### 2.3. Yatırım adresini alın 📍

**pay\_sdk\_python/** dizinine gidin ve **config.yaml** dosyasında **UserOpenId** ve **ChainIDs** alanlarını belirtin.

Sonra `python3 example/get_wallet_addreses.py` çalıştırın.

### 2.4. Para çekme 💸

**pay\_sdk\_python/** dizinine gidin ve **config.yaml** dosyasında **UserOpenId**, **TokenId**, **Amount**, **AddressTo**, **SafeCheckCode**, **CallbackUrl** alanlarını belirtin.

Sonra `python3 example/user_withdraw_by_open_id.py` çalıştırın.

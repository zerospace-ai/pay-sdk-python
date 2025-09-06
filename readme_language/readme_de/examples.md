# Beispiele 📝

Dieses Dokument bietet Nutzungsbeispiele für das CryptoPay Python SDK, einschließlich Demo-Ausführung, Schlüsselerzeugung und Callback-Handhabung.

## 1 SDK-Instanzobjekt 🛠️

### 1.1 Erforderliche Konfiguration ⚙️

1. Registrieren Sie Ihren Geschäftsnamen und erhalten Sie den `ApiKey` und `ApiSecret`;

2. Generieren Sie Ihr eigenes `RSA`-Schlüsselpaar;

3. Bereiten Sie den `RSA`-öffentlichen Schlüssel der Plattform vor;

### 1.2 Erstellen eines Signaturobjekts 🔏

1. Fügen Sie eine Konfigurationsdatei `config.yaml` hinzu.

```yaml
# Konfigurieren Sie Geschäftsinformationen
ApiKey: ""
ApiSecret: ""
# Plattform-öffentlicher Schlüssel
PlatformPubKey: ""
# Öffentlicher Schlüssel zum Blockieren der Plattform
PlatformRiskPubKey: ""
# Ihr eigener privater Schlüssel
RsaPrivateKey: ""
```

2. Laden Sie die Konfigurationsdatei und erstellen Sie das API-Objekt.
    
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

### 1.3 Erstellen und Signieren der Anfragedaten. ✍️

Nehmen wir die Benutzererstellung als Beispiel.

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

### 1.4 Ausfüllen und Initiieren der Anfrage 🚀

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

### 1.5 Überprüfen und Parsen der Rückgabedaten ✅

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

## 2. Befehle ausführen 📞

### 2.1. Neuen Benutzer registrieren 🆕

Gehen Sie in das Verzeichnis **pay\_sdk\_python/** des SDK und ändern Sie im **config.yaml**-File das Feld **UserOpenId**.

Führen Sie anschließend `python3 example/create_user.py` aus, um einen neuen Benutzer auf der Plattform zu registrieren.

Wenn Sie versuchen, eine bereits registrierte **UserOpenId** erneut zu registrieren, wird ein Fehler zurückgegeben.

### 2.2. Wallet-Registrierung 💼

Gehen Sie in das Verzeichnis **pay\_sdk\_python/** und tragen Sie in der **config.yaml**-Datei die Felder **UserOpenId** und **ChainID** ein.

Führen Sie anschließend `python3 example/create_wallet.py` aus, um die Wallet-Registrierung des Benutzers auf der Plattform abzuschließen.

### 2.3. Einzahlungsadresse abrufen 📍

Gehen Sie in das Verzeichnis **pay\_sdk\_python/** und tragen Sie in der **config.yaml**-Datei die Felder **UserOpenId** und **ChainIDs** ein.

Führen Sie anschließend `python3 example/get_wallet_addreses.py` aus.

### 2.4. Auszahlung 💸

Gehen Sie in das Verzeichnis **pay\_sdk\_python/** und tragen Sie in der **config.yaml**-Datei die Felder **UserOpenId**, **TokenId**, **Amount**, **AddressTo**, **SafeCheckCode** und **CallbackUrl** ein.

Führen Sie anschließend `python3 example/user_withdraw_by_open_id.py` aus.

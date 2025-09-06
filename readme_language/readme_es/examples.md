# Ejemplos 📝

Este documento proporciona ejemplos de uso para el CryptoPay Python SDK, incluyendo la ejecución de Demo, generación de claves y manejo de callbacks.

## 1 Objeto de Instancia SDK 🛠️

### 1.1 Configuración Requerida ⚙️

1. Registre su nombre de negocio y obtenga el `ApiKey` y `ApiSecret`;

2. Genere su propio par de claves `RSA`;

3. Prepare la clave pública `RSA` de la plataforma;

### 1.2 Creando un Objeto de Firma 🔏

1. Agregue un archivo de configuración `config.yaml`.

```yaml
# Configurar información de negocio
ApiKey: ""
ApiSecret: ""
# Clave pública de la plataforma
PlatformPubKey: ""
# Clave pública para bloquear la plataforma
PlatformRiskPubKey: ""
# Su propia clave privada
RsaPrivateKey: ""
```

2. Cargue el archivo de configuración y cree el objeto API.

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

### 1.3 Crear y firmar los datos de solicitud. ✍️

Usemos la creación de usuario como ejemplo.

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

### 1.4 Rellenar e Iniciar la Solicitud 🚀

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

### 1.5 Verificar el análisis de los datos de retorno ✅

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

## 2. Ejecutar comandos 📞

### 2.1. Registrar un nuevo usuario 🆕

Ve al directorio **pay\_sdk\_python/** del SDK y modifica el campo **UserOpenId** en el archivo **config.yaml**.

Luego ejecuta `python3 example/create_user.py` para registrar un nuevo usuario en la plataforma.

Si intentas registrar un **UserOpenId** que ya existe, se devolverá un error.

### 2.2. Registro de wallet 💼

Ve al directorio **pay\_sdk\_python/** y completa los campos **UserOpenId** y **ChainID** en el archivo **config.yaml**.

Luego ejecuta `python3 example/create_wallet.py` para completar el registro de la wallet del usuario en la plataforma.

### 2.3. Obtener dirección de depósito 📍

Ve al directorio **pay\_sdk\_python/** y completa los campos **UserOpenId** y **ChainIDs** en el archivo **config.yaml**.

Luego ejecuta `python3 example/get_wallet_addreses.py`.

### 2.4. Retiro 💸

Ve al directorio **pay\_sdk\_python/** y completa los campos **UserOpenId**, **TokenId**, **Amount**, **AddressTo**, **SafeCheckCode** y **CallbackUrl** en el archivo **config.yaml**.

Luego ejecuta `python3 example/user_withdraw_by_open_id.py`.

# CryptoPay Python SDK

![Python Version](https://img.shields.io/badge/python-3.11+-blue.svg)
[![Licencia: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Telegram](https://img.shields.io/badge/chat-Telegram-blue?logo=telegram)](https://t.me/ZeroSerivce)

## 🌟 Bienvenido al CryptoPay Python SDK

CryptoPay Python SDK es un SDK profesional de servicios de criptomonedas implementado en Python, que proporciona registro de usuarios, generación de billeteras, notificaciones de callbacks de depósitos, retiros y otras funciones.

Ha sido probado como seguro, estable y fácil de extender a través de un uso a largo plazo.

Descargar:

```bash
github.com/zerospace-ai/pay-sdk-python
```

Nota: Requiere Python 3.11+ 🛠️.

## 🚀 Inicio Rápido
### 1. ⚙️ config.yaml

```yaml
ApiKey: "your_api_key"
ApiSecret: "your_api_secret"
PlatformPubKey: "platform_public_key"
PlatformRiskPubKey: "platform_risk_public_key"
RsaPrivateKey: "your_rsa_private_key"
```

Descripciones de campos:

• 🔑 ApiKey / ApiSecret:

Asignados por la plataforma al registrar una cuenta de comerciante, utilizados para la autenticación de solicitudes API ✅.

• 🛡️ PlatformPubKey / PlatformRiskPubKey:

Claves públicas proporcionadas por la plataforma, utilizadas para verificar datos o firmas de callbacks devueltos por la plataforma, asegurando fuentes de información confiables. PlatformRiskPubKey se usa principalmente para verificación de eventos relacionados con control de riesgos ⚠️.

• 🗝️ RsaPrivateKey:

Clave privada RSA generada por el comerciante, utilizada para firmar solicitudes, asegurando que el contenido de la solicitud no sea alterado. Nota importante: La clave privada debe mantenerse confidencial 🔒, no la divulgue 🚫.

### 2. Generar Par de Claves RSA 🔐

Usar un par de claves RSA para firmar solicitudes asegura la seguridad de los datos. A continuación se describe cómo generar un par de claves y extraer cadenas de claves en diferentes sistemas operativos.

#### 2.1 Generar Par de Claves Usando OpenSSL

```bash
# Generar clave privada de 2048 bits
openssl genrsa -out rsa_private_key.pem 2048

# Generar clave pública a partir de la clave privada
openssl rsa -in rsa_private_key.pem -out rsa_public_key.pem -pubout
```

> 💡 Consejo: La clave pública generada necesita eliminar el principio y el final -----BEGIN PUBLIC KEY----- / -----END PUBLIC KEY-----, eliminar saltos de línea, convertir a una cadena de una sola línea y enviar a la plataforma.
> 
> Extraer cadenas de claves y enviar la clave pública a la plataforma 📤.
>
>Los comandos para generar pares de claves RSA en Mac y Windows son los mismos que en Linux.

#### 2.2 Extraer Cadenas de Claves 🔑

En Mac/Linux o Git Bash/WSL/Cygwin:

```bash
# Extraer cadena de clave privada
grep -v '^-----' rsa_private_key.pem | tr -d '\n'; echo

# Extraer cadena de clave pública
grep -v '^-----' rsa_public_key.pem | tr -d '\n'; echo
```

Windows

PowerShell extraer cadenas de clave privada y pública:

```powershell
# Clave privada
Write-Output ((Get-Content rsa_private_key.pem | Where-Object {$_ -notmatch "^-----"}) -join "")

# Clave pública
Write-Output ((Get-Content rsa_public_key.pem | Where-Object {$_ -notmatch "^-----"}) -join "")
```

> ⚠️ Nota: La clave privada generada debe mantenerse segura y no filtrarse.


### 🛠️ 3. Crear Instancia SDK

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

## 🔑 Conceptos Clave

- 🆔 **OpenId**: Identificador único del usuario, por ejemplo "HASH1756194148".
- 🔐 **Clave RSA**: Usada para firmar y verificar solicitudes para asegurar la seguridad de los datos.
- ✍️ **Firma API**: Usa algoritmos MD5 y RSA para firmar solicitudes, asegurando que no sean alteradas.

Para descripciones detalladas de API, consulte [🧩 api-reference.md](./api-reference.md) y [🧩 examples.md](./examples.md).

Para Autenticación y Seguridad, consulte [🧩 authentication.md](./authentication.md)

## 📎 Apéndice

Para referencias más detalladas, consulte el documento [Apéndice](./appendix.md), que incluye el siguiente contenido:

- [🧩 Lista de ChainID](./appendix.md#lista-de-chainid-)
- [🏷️ Tipos de Token](./appendix.md#tipos-de-token-)
- [🌐 Información Pública](./appendix.md#información-pública-)
- [🔰 Información Básica de Token](./appendix.md#información-básica-de-token-)

> 💡 **Consejo**: El apéndice proporciona información de cadenas soportadas, tipos de tokens y datos de tokens públicos, facilitando a los desarrolladores integrar y usar el SDK.

## 📞 Contacto

Si tiene alguna pregunta, contacte al proveedor de servicios.  
💬 Telegram: [@ZeroSerivce](https://t.me/ZeroSerivce)
# PKI Management and Certificate Signing

Hands-on Public Key Infrastructure (PKI) lab: a Root CA issues an X.509 server certificate, and a Python HTTPS server presents that certificate to a browser over TLS.

## Directory layout

```
IS A3/
├── http_server.py              # Original starter script
├── IS A3 QP.pdf                # Assignment brief
├── README.md
└── pki_lab/
    ├── CA/                     # Certificate Authority (EasyRSA + Root CA PKI)
    │   └── pki/
    │       ├── ca.crt          # Root CA public certificate
    │       ├── private/ca.key  # Root CA private key (passphrase: labpass)
    │       ├── reqs/nuces.req  # Copied CSR from Server
    │       └── issued/nuces.crt
    ├── Server/                 # Server requestor (EasyRSA + key/CSR)
    │   └── pki/
    │       ├── private/nuces.key
    │       └── reqs/nuces.req
    └── webserver/              # Deployed HTTPS server
        ├── https_server.py
        ├── nuces.crt
        └── nuces.key
```

## What was built

| Item | Value |
| --- | --- |
| Root CA Common Name | `CyberShield Global Root Authority` |
| Server certificate Common Name | `FAST University` |
| Server short name | `nuces` |
| CA private key passphrase | `labpass` (lab only) |
| HTTPS endpoint | `https://localhost:8443` |

## Prerequisites

- Python 3
- EasyRSA Windows package (already present under `pki_lab/CA` and `pki_lab/Server`)
- Mozilla Firefox (for browser verification)

## Run the HTTPS server

```powershell
cd "pki_lab\webserver"
python https_server.py
```

Then open Firefox to: [https://localhost:8443](https://localhost:8443)

### Firefox verification (assignment §5.3)

1. Firefox shows a security warning because the Root CA is not in the browser trust store.
2. Click **Advanced** → **View the site’s Certificate**.
3. Confirm:
   - **Subject CN** = `FAST University`
   - **Issuer** = `CyberShield Global Root Authority`
4. Click **Proceed to localhost:8443** to load the page: *TLS Handshake Successful!*

Optional: import `pki_lab/CA/pki/ca.crt` into Firefox as a trusted CA so the warning disappears. The assignment only requires proceeding past the warning.

## Regenerating the PKI (optional)

Use EasyRSA’s bundled shell (`EasyRSA-Start.bat` or `bin\sh.exe`) from each folder. Example non-interactive commands:

**CA**

```sh
./easyrsa init-pki
./easyrsa --batch --req-cn="CyberShield Global Root Authority" \
  --passin=pass:labpass --passout=pass:labpass build-ca
```

**Server**

```sh
./easyrsa init-pki
./easyrsa --batch --req-cn="FAST University" gen-req nuces nopass
```

**Sign**

1. Copy `Server/pki/reqs/nuces.req` → `CA/pki/reqs/nuces.req`
2. In CA: `./easyrsa --batch --passin=pass:labpass sign-req server nuces`
3. Copy `CA/pki/issued/nuces.crt` and `Server/pki/private/nuces.key` into `webserver/`

## Screenshots for submission

Capture and include in your submission document:

1. Directory structure of `pki_lab/CA/`, `pki_lab/Server/`, and `pki_lab/webserver/`
2. Firefox certificate viewer (Subject / Issuer as above)
3. Webpage loaded successfully after proceeding past the warning

## Brief answers

### 1. What are the contents of the CSR sent by the server to the CA?

A Certificate Signing Request (CSR) contains the server’s **public key**, the requested **subject identity** (here Common Name `FAST University`), and related metadata / signature proving possession of the matching private key. It does **not** include the private key (`nuces.key` stays on the Server).

### 2. In real production environments, how do servers send their CSRs to a CA?

Instead of manually copying files between folders, production systems typically use:

- Automated ACME protocols (e.g. Let’s Encrypt)
- Commercial CA web portals or APIs
- Enterprise enrollment (SCEP, EST, Microsoft AD CS)
- Secure email or ticketed upload workflows

### 3. What key does the CA use to sign certificates? Identify the file.

The CA signs with its **Root CA private key**: `pki_lab/CA/pki/private/ca.key` (protected by passphrase `labpass` in this lab).

### 4. Why does the client browser show a security error?

Firefox does not trust `CyberShield Global Root Authority` because `ca.crt` is not installed in the browser’s trusted root store. The certificate chain cannot be validated to a known trust anchor, so Firefox warns that the connection may not be secure—even though TLS cryptography itself works.

## Security note

Private keys (`ca.key`, `nuces.key`) are included in this repository for educational / grading reproducibility only. Do not reuse these keys or the CA passphrase outside this lab.

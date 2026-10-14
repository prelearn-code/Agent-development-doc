# GmSSL 全部标准子命令：本机 `-help` 与解读

本页逐项运行并整理 GmSSL 3.3.0-dev.1183 的 **90 个子命令**。每节先列本机 `-help` 的用法，再解释作用和关键参数；折叠块保留帮助内容供逐项核对。绝对可执行文件路径已缩写为 `gmssl`，行末空白已去除，参数和示例内容不改。**帮助可显示不等于实际业务已运行通过**。

入口：`gmssl help`，查看单项：`gmssl <command> -help`。`[]` 表示可选参数，`|` 表示互斥选择；格式和默认值以当前安装版本为准。可运行的教学命令与参数间配对见[常用例子](CLI-CRYPTO-REFERENCE.md)。

涉及证书、网络、设备、CA 或用户密钥的命令需要对应测试资源；此页只声明 help 已核对，未将这些外部流程冒充验证完成。私钥、口令和对称密钥不作为模型参数传入。

本机帮助存在几处需要辨别的地方：

| 子命令 | 帮助中的差异 | 当前解释 |
|---|---|---|
| `sm3_pbkdf2` | `usage` 行未列出参数，后面的 Options 才列 `-pass`、`-salt`、`-iter`、`-outlen` | 按 Options 组合；临时口令/盐示例见[常用例子](CLI-CRYPTO-REFERENCE.md)。 |
| `sm2decrypt` | `-out` 的说明行误写成 `-in file \| stdout` | `usage` 中的 `-out file` 与本机往返测试一致，表示明文输出路径。 |
| `sm9verify` | Options 列出 `-out`，但 `usage` 没有它 | 已验证的验签例子只使用 `-pubmaster`、`-id`、`-in`、`-sig`；不把该 `-out` 当成已确认参数。 |
| `kyberencap` | `-out` 的描述写有“decapsulated secret” | 本机往返证明 `-out` 是 KEM 密文，`-outkey` 是封装所得共享秘密。 |
| `sdfinfo` | 帮助例子省略 `usage` 要求的 `-lib` | 需要实际厂商动态库才能运行；本机未连接设备。 |

## 入口与随机数

### `gmssl help`

**帮助命令**：`gmssl help -help`。**用法**：`usage: gmssl <command> [options]`

**作用**：列出可用子命令及调用形式。

**参数解读**：入口列出本机 90 个子命令；以下每节都由对应 `-help` 实测生成。

<details><summary>展开本机 `-help` 原文</summary>

```text
usage: gmssl <command> [options]

command:

  help              Print this help message
  version           Print version
  rand              Generate random bytes
  sm2keygen         Generate SM2 keypair
  sm2sign           Generate SM2 signature
  sm2verify         Verify SM2 signature
  sm2encrypt        Encrypt with SM2 public key
  sm2decrypt        Decrypt with SM2 private key
  sm2exch           SM2 key exchange
  sm3               Generate SM3 hash
  sm3_hmac          Generate SM3 HMAC tag
  sm3_pbkdf2        Hash password into key using PBKDF2 algoritm
  sm4_ecb           Encrypt or decrypt with SM4 ECB
  sm4_cbc           Encrypt or decrypt with SM4 CBC
  sm4_cfb           Encrypt or decrypt with SM4 CFB
  sm4_ofb           Encrypt or decrypt with SM4 OFB
  sm4_ctr           Encrypt or decrypt with SM4 CTR
  sm4_gcm           Encrypt or decrypt with SM4 GCM
  sm4_ccm           Encrypt or decrypt with SM4 CCM
  sm4_xts           Encrypt or decrypt with SM4 XTS
  sm4_ff1           Encrypt or decrypt digits with SM4 FF1
  sm4_cbc_mac       Generate SM4 CBC-MAC
  ghash             Generate GHASH
  zuc               Encrypt or decrypt with ZUC
  zuc256            Encrypt or decrypt with ZUC-256
  zuc_128_eea3      Encrypt or decrypt with ZUC 128-EEA3
  zuc_128_eia3      Generate ZUC 128-EIA3 MAC
  sm9setup          Generate SM9 master secret
  sm9keygen         Generate SM9 private key
  sm9sign           Generate SM9 signature
  sm9verify         Verify SM9 signature
  sm9encrypt        SM9 public key encryption
  sm9decrypt        SM9 decryption
  sm9exch           SM9 key exchange
  reqgen            Generate certificate signing request (CSR)
  reqsign           Generate certificate from CSR
  reqparse          Parse and print a CSR
  certgen           Generate a self-signed certificate
  certverify        Verify certificate chain
  certrevoke        Revoke certificate and output RevokedCertificate record
  certparse         Parse and print certificates
  crlget            Download the CRL of given certificate
  crlgen            Sign a CRL with CA certificate and private key
  crlverify         Verify a CRL with issuer's certificate
  crlparse          Parse and print CRL
  ocspreq           Generate OCSPRequest
  ocspget           Download OCSPResponse from OCSP responder
  ocspsign          Sign OCSPResponse
  ocspverify        Verify OCSPResponse
  sctverify         Verify Signed Certificate Timestamp list
  cmssign           Generate CMS SignedData
  cmsverify         Verify CMS SignedData
  cmsencrypt        Generate CMS EnvelopedData
  cmsdecrypt        Decrypt CMS EnvelopedData
  cmsparse          Parse CMS (cryptographic message syntax) file
  eckeygen          Generate EC keypair on a named curve
  lmskeygen         Generate LMS-SM3 (Leighton-Micali Signature) keypair
  lmssign           Generate LMS-SM3 signature
  lmsverify         Verify LMS-SM3 signature
  hsskeygen         Generate HSS-SM3 keypair
  hsssign           Generate HSS-SM3 signature
  hssverify         Verify HSS-SM3 signature
  xmsskeygen        Generate XMSS-SM3 keypair
  xmsssign          Generate XMSS-SM3 signature
  xmssverify        Verify XMSS-SM3 signature
  xmssmtkeygen      Generate XMSS^MT-SM3 keypair
  xmssmtsign        Generate XMSS^MT-SM3 signature
  xmssmtverify      Verify XMSS^MT-SM3 signature
  sphincskeygen     Generate SPHINCS+_128s-SM3 keypair
  sphincssign       Generate SPHINCS+_128s-SM3 signature
  sphincsverify     Verify SPHINCS+_128s-SM3 signature
  kyberkeygen       Generate Kyber keypair
  kyberencap        Kyber KEM encap
  kyberdecap        Kyber KEM decap
  sdfinfo           Print SDF device info
  sdfdigest         Generate SM3 hash with SDF device
  sdfexport         Export SM2 signing public key from SDF device
  sdfsign           Generate SM2 signature with SDF internal private key
  sdfencrypt        SM2/SM4-CBC hybrid encryption with SDF device
  sdfdecrypt        SM2/SM4-CBC hybrid decryption with SDF device
  sdftest           Test vendor's SDF library and device
  skfutil           SKF crypto device utility
  tlcp_client       TLCP client
  tlcp_server       TLCP server
  tls12_client      TLS 1.2 client
  tls12_server      TLS 1.2 server
  tls13_client      TLS 1.3 client
  tls13_server      TLS 1.3 server
  quic_client       QUIC client
  quic_server       QUIC server

run `gmssl <command> -help` to print help of the given command
```

</details>

### `gmssl version`

**帮助命令**：`gmssl version -help`。**用法**：`gmssl version -help（该子命令未给出独立 usage）`

**作用**：打印当前 GmSSL 可执行程序的版本。

**参数解读**：输出版本；本机 `version -help` 也只打印版本，没有独立选项列表。

<details><summary>展开本机 `-help` 原文</summary>

```text
GmSSL 3.3.0-dev.1183
```

</details>

### `gmssl rand`

**帮助命令**：`gmssl rand -help`。**用法**：`usage: rand [-hex] [-rdrand|-rdseed] -outlen num [-out file]`

**作用**：生成指定字节数的随机数据，可转成十六进制。

**参数解读**：`-outlen` 以字节为单位，`-hex` 改变显示编码；编码后的字符数不是随机字节数。

<details><summary>展开本机 `-help` 原文</summary>

```text
usage: rand [-hex] [-rdrand|-rdseed] -outlen num [-out file]
```

</details>

## SM2 公钥密码

### `gmssl sm2keygen`

**帮助命令**：`gmssl sm2keygen -help`。**用法**：`usage: gmssl sm2keygen [-pass str] [-out pem] [-pubout pem]`

**作用**：生成 SM2 私钥及对应公钥。

**参数解读**：`-pass` 是私钥保护口令，`-out` 和 `-pubout` 分别是私钥、公钥。示例口令仅用于临时实验。

**帮助给出的命令示例（未作为本项目验收）**：

```bash
gmssl sm2keygen -pass P@ssw0rd -out sm2.pem
```

<details><summary>展开本机 `-help` 原文</summary>

```text
usage: gmssl sm2keygen [-pass str] [-out pem] [-pubout pem]

Options

    -pass pass                  Password to encrypt the private key, prompt if not given
    -out pem                    Output password-encrypted PKCS #8 private key in PEM format
    -pubout pem                 Output public key in PEM format

Examples

    gmssl sm2keygen -pass P@ssw0rd -out sm2.pem
    gmssl sm2keygen -pass P@ssw0rd -out sm2.pem -pubout sm2pub.pem
```

</details>

### `gmssl sm2sign`

**帮助命令**：`gmssl sm2sign -help`。**用法**：`usage: gmssl sm2sign -key pem [-pass str] [-id str] [-in file] [-out file]`

**作用**：用 SM2 私钥与约定身份标识对消息签名。

**参数解读**：`-key` 是私钥；`-id` 须与验签一致；`-out` 为二进制 DER 签名。

**帮助给出的命令示例（未作为本项目验收）**：

```bash
echo -n 'message to be signed' | gmssl sm2sign -key sm2.pem -pass P@ssw0rd -out sm2.sig
```

<details><summary>展开本机 `-help` 原文</summary>

```text
usage: gmssl sm2sign -key pem [-pass str] [-id str] [-in file] [-out file]

Options

    -key pem            Signing private key file in PEM format
    -pass str           Password to open the private key, prompt if not given
    -id str             Signer's identity string, '1234567812345678' by default
    -in file | stdin    To be signed file or data
    -out file | stdout  Output signature in binary DER encoding

Examples

    gmssl sm2keygen -pass P@ssw0rd -out sm2.pem -pubout sm2pub.pem
    echo -n 'message to be signed' | gmssl sm2sign -key sm2.pem -pass P@ssw0rd -out sm2.sig
    echo -n 'message to be signed' | gmssl sm2verify -pubkey sm2pub.pem -sig sm2.sig
```

</details>

### `gmssl sm2verify`

**帮助命令**：`gmssl sm2verify -help`。**用法**：`usage: gmssl sm2verify (-pubkey pem | -cert pem) [-id str] [-in file] -sig file`

**作用**：用 SM2 公钥或证书验证签名。

**参数解读**：`-pubkey` 或 `-cert` 二选一；`-sig` 是 DER 签名文件，原文和签名时的 ID 要一致。

**帮助给出的命令示例（未作为本项目验收）**：

```bash
echo -n 'message to be signed' | gmssl sm2verify -pubkey sm2pub.pem -sig sm2.sig
```

<details><summary>展开本机 `-help` 原文</summary>

```text
usage: gmssl sm2verify (-pubkey pem | -cert pem) [-id str] [-in file] -sig file

Options

    -pubkey pem         Signer's public key file in PEM format
    -cert pem           Signer's certificate in PEM format
    -id str             Signer's identity string, '1234567812345678' by default
    -in file | stdin    Signed file or data
    -sig file           Signature in binary DER encoding

Examples

    gmssl sm2keygen -pass P@ssw0rd -out sm2.pem -pubout sm2pub.pem
    echo -n 'message to be signed' | gmssl sm2sign -key sm2.pem -pass P@ssw0rd -out sm2.sig
    echo -n 'message to be signed' | gmssl sm2verify -pubkey sm2pub.pem -sig sm2.sig
```

</details>

### `gmssl sm2encrypt`

**帮助命令**：`gmssl sm2encrypt -help`。**用法**：`usage: gmssl sm2encrypt (-pubkey pem | -cert pem) [-in file] [-out file]`

**作用**：用 SM2 公钥或证书加密短消息。

**参数解读**：`-pubkey` 或 `-cert` 二选一。本机帮助限定明文最多 255 字节，输出是二进制 DER。

**帮助给出的命令示例（未作为本项目验收）**：

```bash
echo 'Secret message' | gmssl sm2encrypt -pubkey sm2pub.pem -out sm2.der
```

<details><summary>展开本机 `-help` 原文</summary>

```text
usage: gmssl sm2encrypt (-pubkey pem | -cert pem) [-in file] [-out file]

Options

    -pubkey pem         Recepient's public key file in PEM format
    -cert pem           Recipient's certificate in PEM format
    -in file | stdin    To be encrypted data, at most 255 bytes
    -out file | stdout  Output ciphertext in binary DER-encoding

Examples

    gmssl sm2keygen -pass P@ssw0rd -out sm2.pem -pubout sm2pub.pem
    echo 'Secret message' | gmssl sm2encrypt -pubkey sm2pub.pem -out sm2.der
    gmssl sm2decrypt -key sm2.pem -pass P@ssw0rd -in sm2.der
```

</details>

### `gmssl sm2decrypt`

**帮助命令**：`gmssl sm2decrypt -help`。**用法**：`usage: gmssl sm2decrypt -key pem [-pass str] [-in file] [-out file]`

**作用**：用 SM2 私钥解密 DER 格式密文。

**参数解读**：输入是 SM2 DER 密文，`-key` 是对应私钥；它不是 1 MiB 文件加密接口。

**帮助给出的命令示例（未作为本项目验收）**：

```bash
gmssl sm2decrypt -key sm2.pem -pass P@ssw0rd -in sm2.der
```

<details><summary>展开本机 `-help` 原文</summary>

```text
usage: gmssl sm2decrypt -key pem [-pass str] [-in file] [-out file]

Options

    -key pem            Decryption private key file in PEM format
    -pass str           Password to open the private key, prompt if not given
    -in file | stdin    Input ciphertext in binary DER-encoding
    -in file | stdout   Output decrypted data

Examples

    gmssl sm2keygen -pass P@ssw0rd -out sm2.pem -pubout sm2pub.pem
    echo 'Secret message' | gmssl sm2encrypt -pubkey sm2pub.pem -out sm2.der
    gmssl sm2decrypt -key sm2.pem -pass P@ssw0rd -in sm2.der
```

</details>

### `gmssl sm2exch`

**帮助命令**：`gmssl sm2exch -help`。**用法**：`usage: gmssl sm2exch -stage init|respond|confirm|finish [options]`

**作用**：按四阶段协议完成双方 SM2 密钥交换。

**参数解读**：四阶段协议 `init/respond/confirm/finish` 依赖双方临时状态和一致 ID，不是单次加密。

**帮助中需要先理解的参数**：

- `-hex`：本机帮助描述：Encode input/output data in hex, default
- `-bin`：本机帮助描述：Encode input/output data in binary

**帮助给出的命令示例（未作为本项目验收）**：

```bash
gmssl sm2exch -stage init \
-exch_keyout alice_ra.pem -exch_pass P@ssw0rd -out ra.hex
```

<details><summary>展开本机 `-help` 原文</summary>

```text
usage: gmssl sm2exch -stage init|respond|confirm|finish [options]

Options

    -stage init|respond|confirm|finish
                            SM2 key exchange stage
    -cert pem               Optional local SM2 certificate for checking against -key
    -pubkey pem             Optional local SM2 public key for checking against -key
    -key pem                Local SM2 private key in PEM format
    -pass str               Password to open local private key, prompt if not given
    -peer_cert pem          Peer SM2 key exchange/encryption certificate in PEM format
    -peer_pubkey pem        Peer SM2 public key in PEM format
    -id str                 Local SM2 identity, '1234567812345678' by default
    -id_hex hex             Local SM2 identity in hex
    -peer_id str            Peer SM2 identity, '1234567812345678' by default
    -peer_id_hex hex        Peer SM2 identity in hex
    -in file | stdin        Input data for this stage
                            respond: RA, 65 bytes
                            confirm: RB || SB, 97 bytes
                            finish: SA, 32 bytes
    -out file | stdout      Output data to send to peer
                            init: RA, 65 bytes
                            respond: RB || SB, 97 bytes
                            confirm: SA, 32 bytes
    -exch_keyout pem        Output local ephemeral private key
    -exch_key pem           Input local ephemeral private key
    -exch_pass str          Password for local ephemeral private key, prompt if not given
    -secret_state_out file
                            Output 65-byte secret_state point
    -secret_state file      Input 65-byte secret_state point
    -keylen num             Shared key length in bytes, 32 by default
    -keyout file            Output shared key
    -hex                    Encode input/output data in hex, default
    -bin                    Encode input/output data in binary

Examples

Public-key file workflow:

    gmssl sm2keygen -pass P@ssw0rd -out alice.pem -pubout alicepub.pem
    gmssl sm2keygen -pass P@ssw0rd -out bob.pem -pubout bobpub.pem
    gmssl sm2exch -stage init \
        -exch_keyout alice_ra.pem -exch_pass P@ssw0rd -out ra.hex
    gmssl sm2exch -stage respond \
        -key bob.pem -pass P@ssw0rd -id Bob \
        -peer_pubkey alicepub.pem -peer_id Alice -in ra.hex \
        -exch_keyout bob_rb.pem -exch_pass P@ssw0rd \
        -secret_state_out bob_secret_state.hex -out rb_sb.hex
    gmssl sm2exch -stage confirm \
        -key alice.pem -pass P@ssw0rd -id Alice \
        -peer_pubkey bobpub.pem -peer_id Bob \
        -exch_key alice_ra.pem -exch_pass P@ssw0rd -in rb_sb.hex \
        -keylen 48 -keyout alice_shared_key.hex -out sa.hex
    gmssl sm2exch -stage finish \
        -key bob.pem -pass P@ssw0rd -id Bob \
        -peer_pubkey alicepub.pem -peer_id Alice \
        -exch_key bob_rb.pem -exch_pass P@ssw0rd \
        -secret_state bob_secret_state.hex -in sa.hex \
        -keylen 48 -keyout bob_shared_key.hex

Certificate workflow:

    gmssl sm2exch -stage respond \
        -key bob_enc_key.pem -pass P@ssw0rd -id Bob \
        -peer_cert alice_enc_cert.pem -peer_id Alice -in ra.hex \
        -exch_keyout bob_rb.pem -exch_pass P@ssw0rd \
        -secret_state_out bob_secret_state.hex -out rb_sb.hex
    gmssl sm2exch -stage confirm \
        -key alice_enc_key.pem -pass P@ssw0rd -id Alice \
        -peer_cert bob_enc_cert.pem -peer_id Bob \
        -exch_key alice_ra.pem -exch_pass P@ssw0rd -in rb_sb.hex \
        -keyout alice_shared_key.hex -out sa.hex

Notes

    -cert and -peer_cert read only the first certificate from the PEM file.
    If KeyUsage is present, the certificate must allow keyEncipherment or keyAgreement.
    RA, RB and secret_state are fixed 65-byte uncompressed SM2 points.
    The respond output is RB || SB, fixed 97 bytes.
    -hex and -bin affect RA, RB||SB, SA, secret_state and shared key files.
```

</details>

## SM3 摘要、HMAC 与派生

### `gmssl sm3`

**帮助命令**：`gmssl sm3 -help`。**用法**：`usage: sm3 [-hex|-bin] [-pubkey pem [-id str]] [-in file|-in_str str] [-out file]`

**作用**：对消息或文件计算 SM3 摘要。

**参数解读**：`-in` 与 `-in_str` 二选一；`-bin` 输出 32 字节二进制。`-pubkey` 会加入 SM2 Z 值。

**帮助中需要先理解的参数**：

- `-hex`：本机帮助描述：Output hash value as hex string (by default)
- `-bin`：本机帮助描述：Output hash value as binary

**帮助给出的命令示例（未作为本项目验收）**：

```bash
gmssl sm3 -in_str abc
```

<details><summary>展开本机 `-help` 原文</summary>

```text
usage: sm3 [-hex|-bin] [-pubkey pem [-id str]] [-in file|-in_str str] [-out file]
Options

    -hex                   Output hash value as hex string (by default)
    -bin                   Output hash value as binary
    -pubkey pem            Signer's SM2 public key
                           When `-pubkey` is specified, hash with SM2 Z value
    -id str                SM2 Signer's ID string
    -id_hex hex            SM2 Signer's ID in hex format
                           `-id` and `-id_hex` should be used with `-pubkey`
                           `-id` and `-id_hex` should not be used together
                           If `-pubkey` is specified without `-id` or `id_hex`,
                           the default ID string '1234567812345678' is used
    -in_str str            To be hashed string
    -in file | stdin       To be hashed file path
                           `-in_str` and `-in` should not be used together
                           If neither `-in` nor `-in_str` specified, read from stdin
    -out file | stdout     Output file path. If not specified, output to stdout

Examples

    gmssl sm3 -in_str abc

    gmssl sm3 -in_str abc -bin

    gmssl sm3 -in /path/to/file

    gmssl sm3 -pubkey sm2pubkey.pem -id alice -in /path/to/file -bin

    When reading from stdin, make sure the trailing newline character is removed

    Linux/Mac:
    echo -n abc | gmssl sm3

    Windows:
    echo |set/p="abc" | gmssl sm3
```

</details>

### `gmssl sm3_hmac`

**帮助命令**：`gmssl sm3_hmac -help`。**用法**：`usage: sm3_hmac -key hex [-in file | -in_str str] [-bin|-hex] [-out file]`

**作用**：用十六进制密钥计算 HMAC-SM3 标签。

**参数解读**：HMAC 需要十六进制密钥；它是带密钥的消息认证码，不等于普通 SM3 摘要。

**帮助中需要先理解的参数**：

- `-hex`：本机帮助描述：Output MAC-tag as hex string (by default)
- `-bin`：本机帮助描述：Output MAC-tag as binary

**帮助给出的命令示例（未作为本项目验收）**：

```bash
gmssl sm3_hmac -key $KEY -in_str abc
```

<details><summary>展开本机 `-help` 原文</summary>

```text
usage: sm3_hmac -key hex [-in file | -in_str str] [-bin|-hex] [-out file]
Options

    -key hex               Hex string of the MAC key
    -in_str str            Input as text string
    -in file | stdin       Input file path
                           `-in_str` and `-in` should not be used together
                           If neither `-in` nor `-in_str` specified, read from stdin
    -hex                   Output MAC-tag as hex string (by default)
    -bin                   Output MAC-tag as binary
                           `-hex` and `-bin` should not be used together
    -out file | stdout     Output file path. If not specified, output to stdout

Examples

    KEY=`gmssl rand -outlen 16 -hex`
    gmssl sm3_hmac -key $KEY -in_str abc

    gmssl sm3_hmac -key $KEY -in_str abc -bin

    gmssl sm3_hmac -key $KEY -in /path/to/file

    When reading from stdin, make sure the trailing newline character is removed

    Linux/Mac:
    echo -n abc | gmssl sm3_hmac -key $KEY

    Windows:
    for /f %i in ('gmssl rand -outlen 16 -hex') do set KEY=%i
    echo |set/p="abc" | gmssl sm3_hmac -key %KEY%
```

</details>

### `gmssl sm3_pbkdf2`

**帮助命令**：`gmssl sm3_pbkdf2 -help`。**用法**：`usage: gmssl sm3_pbkdf2`

**作用**：用 PBKDF2-HMAC-SM3 从口令和盐派生密钥。

**参数解读**：`-pass`、`-salt`、`-iter`、`-outlen` 共同决定派生结果；真实口令不能出现在命令行。

**帮助中需要先理解的参数**：

- `-bin`：本机帮助描述：Output binary key
- `-hex`：本机帮助描述：Output key in hex digits

**帮助给出的命令示例（未作为本项目验收）**：

```bash
gmssl sm3_pbkdf2 -pass P@ssw0rd -salt $SALT -iter 10000 -outlen 16 -hex
```

<details><summary>展开本机 `-help` 原文</summary>

```text
usage: gmssl sm3_pbkdf2
Options

    -pass str           Password to be converted into key, prompt if not given
    -salt hex           Salt value, 8 to 64 bytes
    -iter num           Iteration count, larger iter make it more secure but slower
    -outlen num         Generate key bytes
    -bin                Output binary key
    -hex                Output key in hex digits
    -out file | stdout  Output data

Examples

    SALT=`gmssl rand -outlen 8 -hex`
    gmssl sm3_pbkdf2 -pass P@ssw0rd -salt $SALT -iter 10000 -outlen 16 -hex
```

</details>

## SM4、GHASH 与工作模式

### `gmssl sm4_ecb`

**帮助命令**：`gmssl sm4_ecb -help`。**用法**：`usage: gmssl sm4_ecb {-encrypt|-decrypt} -key hex [-in file] [-out file]`

**作用**：执行 SM4 ECB 模式加解密。

**参数解读**：ECB 不提供认证，也会暴露相同块模式；仅作为命令识别。

**帮助中需要先理解的参数**：

- `-encrypt`：选择加密动作；本机帮助描述：Encrypt
- `-decrypt`：选择解密动作；本机帮助描述：Decrypt

**帮助给出的命令示例（未作为本项目验收）**：

```bash
echo -n 0123456789abcdef | gmssl sm4_ecb -encrypt -key $KEY -out sm4_ecb_ciphertext.bin
```

<details><summary>展开本机 `-help` 原文</summary>

```text
usage: gmssl sm4_ecb {-encrypt|-decrypt} -key hex [-in file] [-out file]

Options

    -encrypt            Encrypt
    -decrypt            Decrypt
    -key hex            Symmetric key in HEX format
    -in file | stdin    Input data, length must be a multiple of 16 bytes
    -out file | stdout  Output data

Examples

    KEY=`gmssl rand -outlen 16 -hex`
    echo -n 0123456789abcdef | gmssl sm4_ecb -encrypt -key $KEY -out sm4_ecb_ciphertext.bin
    gmssl sm4_ecb -decrypt -key $KEY -in sm4_ecb_ciphertext.bin
```

</details>

### `gmssl sm4_cbc`

**帮助命令**：`gmssl sm4_cbc -help`。**用法**：`usage: gmssl sm4_cbc {-encrypt|-decrypt} -key hex -iv hex [-pkcs7_padding] [-in file] [-out file]`

**作用**：执行 SM4 CBC 模式加解密，可启用 PKCS#7 填充。

**参数解读**：`-key` 与 `-iv` 为十六进制；任意长度输入需 `-pkcs7_padding`，CBC 不提供认证。

**帮助中需要先理解的参数**：

- `-encrypt`：选择加密动作；本机帮助描述：Encrypt
- `-decrypt`：选择解密动作；本机帮助描述：Decrypt
- `-pkcs7_padding`：本机帮助描述：Enable PKCS#7 padding

**帮助给出的命令示例（未作为本项目验收）**：

```bash
echo -n 0123456789abcdef | gmssl sm4_cbc -encrypt -key $KEY -iv $IV -out sm4_cbc_ciphertext.bin
```

<details><summary>展开本机 `-help` 原文</summary>

```text
usage: gmssl sm4_cbc {-encrypt|-decrypt} -key hex -iv hex [-pkcs7_padding] [-in file] [-out file]

Options

    -encrypt            Encrypt
    -decrypt            Decrypt
    -key hex            Symmetric key in HEX format
    -iv hex             IV in HEX format
    -pkcs7_padding      Enable PKCS#7 padding
                        Encrypt input can be any byte length; decrypt input must be a multiple of 16 bytes
    -in file | stdin    Input data. Without `-pkcs7_padding`, input length must be a multiple of 16 bytes
    -out file | stdout  Output data

Examples

    KEY=`gmssl rand -outlen 16 -hex`
    IV=`gmssl rand -outlen 16 -hex`
    echo -n 0123456789abcdef | gmssl sm4_cbc -encrypt -key $KEY -iv $IV -out sm4_cbc_ciphertext.bin
    gmssl sm4_cbc -decrypt -key $KEY -iv $IV -in sm4_cbc_ciphertext.bin

    echo -n abc | gmssl sm4_cbc -encrypt -pkcs7_padding -key $KEY -iv $IV -out sm4_cbc_ciphertext.bin
    gmssl sm4_cbc -decrypt -pkcs7_padding -key $KEY -iv $IV -in sm4_cbc_ciphertext.bin
```

</details>

### `gmssl sm4_cfb`

**帮助命令**：`gmssl sm4_cfb -help`。**用法**：`usage: gmssl sm4_cfb {-encrypt|-decrypt} -sbytes num -key hex -iv hex [-in file] [-out file]`

**作用**：执行 SM4 CFB 模式加解密。

**参数解读**：`-sbytes` 决定反馈段字节数；加解密双方须一致。

**帮助中需要先理解的参数**：

- `-encrypt`：选择加密动作；本机帮助描述：Encrypt
- `-decrypt`：选择解密动作；本机帮助描述：Decrypt

**帮助给出的命令示例（未作为本项目验收）**：

```bash
echo -n abc | gmssl sm4_cfb -encrypt -key $KEY -iv $IV -out sm4_cfb128_ciphertext.bin
```

<details><summary>展开本机 `-help` 原文</summary>

```text
usage: gmssl sm4_cfb {-encrypt|-decrypt} -sbytes num -key hex -iv hex [-in file] [-out file]

Options

    -sbytes num         Parameter sbytes of CFB mode, should be 1, 8 or 16, 16 by default
    -encrypt            Encrypt
    -decrypt            Decrypt
    -key hex            Symmetric key in HEX format
    -iv hex             IV in HEX format
    -in file | stdin    Input data, any byte length is accepted
    -out file | stdout  Output data

Examples

    KEY=`gmssl rand -outlen 16 -hex`
    IV=`gmssl rand -outlen 16 -hex`
    echo -n abc | gmssl sm4_cfb -encrypt -key $KEY -iv $IV -out sm4_cfb128_ciphertext.bin
    gmssl sm4_cfb -decrypt -key $KEY -iv $IV -in sm4_cfb128_ciphertext.bin

    echo -n abc | gmssl sm4_cfb -sbytes 1 -encrypt -key $KEY -iv $IV -out sm4_cfb8_ciphertext.bin
    gmssl sm4_cfb -sbytes 1 -decrypt -key $KEY -iv $IV -in sm4_cfb8_ciphertext.bin

    echo -n 01234567 | gmssl sm4_cfb -sbytes 8 -encrypt -key $KEY -iv $IV -out sm4_cfb64_ciphertext.bin
    gmssl sm4_cfb -sbytes 8 -decrypt -key $KEY -iv $IV -in sm4_cfb64_ciphertext.bin
```

</details>

### `gmssl sm4_ofb`

**帮助命令**：`gmssl sm4_ofb -help`。**用法**：`usage: gmssl sm4_ofb [-encrypt|-decrypt] -key hex -iv hex [-in file] [-out file]`

**作用**：执行 SM4 OFB 模式数据变换。

**帮助中需要先理解的参数**：

- `-encrypt`：选择加密动作；本机帮助描述：Encrypt
- `-decrypt`：选择解密动作；本机帮助描述：Decrypt

**帮助给出的命令示例（未作为本项目验收）**：

```bash
echo -n abc | gmssl sm4_ofb -encrypt -key $KEY -iv $IV -out sm4_ofb_ciphertext.bin
```

<details><summary>展开本机 `-help` 原文</summary>

```text
usage: gmssl sm4_ofb [-encrypt|-decrypt] -key hex -iv hex [-in file] [-out file]

Options

    -encrypt            Encrypt
    -decrypt            Decrypt
    -key hex            Symmetric key in HEX format
    -iv hex             IV in HEX format
    -in file | stdin    Input data, any byte length is accepted
    -out file | stdout  Output data

Examples

    KEY=`gmssl rand -outlen 16 -hex`
    IV=`gmssl rand -outlen 16 -hex`
    echo -n abc | gmssl sm4_ofb -encrypt -key $KEY -iv $IV -out sm4_ofb_ciphertext.bin
    gmssl sm4_ofb -decrypt -key $KEY -iv $IV -in sm4_ofb_ciphertext.bin
```

</details>

### `gmssl sm4_ctr`

**帮助命令**：`gmssl sm4_ctr -help`。**用法**：`usage: gmssl sm4_ctr [-encrypt|-decrypt] -key hex -iv hex [-in file] [-out file]`

**作用**：执行 SM4 CTR 模式数据变换。

**帮助中需要先理解的参数**：

- `-encrypt`：选择加密动作；本机帮助描述：Encrypt
- `-decrypt`：选择解密动作；本机帮助描述：Decrypt

**帮助给出的命令示例（未作为本项目验收）**：

```bash
echo -n abc | gmssl sm4_ctr -encrypt -key $KEY -iv $IV -out sm4_ctr_ciphertext.bin
```

<details><summary>展开本机 `-help` 原文</summary>

```text
usage: gmssl sm4_ctr [-encrypt|-decrypt] -key hex -iv hex [-in file] [-out file]

Options

    -encrypt            Encrypt
    -decrypt            Decrypt
    -key hex            Symmetric key in HEX format
    -iv hex             IV in HEX format
    -in file | stdin    Input data, any byte length is accepted
    -out file | stdout  Output data

Examples

    KEY=`gmssl rand -outlen 16 -hex`
    IV=`gmssl rand -outlen 16 -hex`
    echo -n abc | gmssl sm4_ctr -encrypt -key $KEY -iv $IV -out sm4_ctr_ciphertext.bin
    gmssl sm4_ctr -decrypt -key $KEY -iv $IV -in sm4_ctr_ciphertext.bin
```

</details>

### `gmssl sm4_gcm`

**帮助命令**：`gmssl sm4_gcm -help`。**用法**：`usage: gmssl sm4_gcm {-encrypt|-decrypt} -key hex -iv hex [-aad str| -aad_hex hex] [-taglen num] [-in file] [-out file]`

**作用**：执行带认证标签的 SM4-GCM 加解密。

**参数解读**：`-iv` 推荐 12 字节；解密输入为密文后接 tag。AAD、tag 长度和 nonce 必须匹配。

**帮助中需要先理解的参数**：

- `-encrypt`：选择加密动作；本机帮助描述：Encrypt
- `-decrypt`：选择解密动作；本机帮助描述：Decrypt

**帮助给出的命令示例（未作为本项目验收）**：

```bash
echo -n abc | gmssl sm4_gcm -encrypt -key $KEY -iv $IV -aad_hex 001122 -out sm4_gcm_ciphertext.bin
```

<details><summary>展开本机 `-help` 原文</summary>

```text
usage: gmssl sm4_gcm {-encrypt|-decrypt} -key hex -iv hex [-aad str| -aad_hex hex] [-taglen num] [-in file] [-out file]

Options

    -encrypt            Encrypt
    -decrypt            Decrypt
    -key hex            Symmetric key in HEX format
    -iv hex             IV in HEX format, 12 bytes (24 hex digits) is recommended
    -aad str            Authenticated-only message
    -aad_hex hex        Authenticated-only data in HEX format
    -taglen num         MAC tag length, default 16 bytes
    -in file | stdin    Input data. Encrypt input can be any byte length
                        Decrypt input is ciphertext || tag and must be at least taglen bytes
    -out file | stdout  Output data

Examples

    KEY=`gmssl rand -outlen 16 -hex`
    IV=`gmssl rand -outlen 12 -hex`
    echo -n abc | gmssl sm4_gcm -encrypt -key $KEY -iv $IV -aad_hex 001122 -out sm4_gcm_ciphertext.bin
    gmssl sm4_gcm -decrypt -key $KEY -iv $IV -aad_hex 001122 -in sm4_gcm_ciphertext.bin
```

</details>

### `gmssl sm4_ccm`

**帮助命令**：`gmssl sm4_ccm -help`。**用法**：`usage: gmssl sm4_ccm {-encrypt|-decrypt} -key hex -iv hex [-aad str| -aad_hex hex] [-taglen num] [-in file] [-out file]`

**作用**：执行带认证标签的 SM4-CCM 加解密。

**参数解读**：IV 范围 7–13 字节，tag 长度 4–16 字节；解密输入为密文后接 tag。

**帮助中需要先理解的参数**：

- `-encrypt`：选择加密动作；本机帮助描述：Encrypt
- `-decrypt`：选择解密动作；本机帮助描述：Decrypt

**帮助给出的命令示例（未作为本项目验收）**：

```bash
echo -n abc | gmssl sm4_ccm -encrypt -key $KEY -iv $IV -aad_hex 001122 -out sm4_ccm_ciphertext.bin
```

<details><summary>展开本机 `-help` 原文</summary>

```text
usage: gmssl sm4_ccm {-encrypt|-decrypt} -key hex -iv hex [-aad str| -aad_hex hex] [-taglen num] [-in file] [-out file]

Options

    -encrypt            Encrypt
    -decrypt            Decrypt
    -key hex            Symmetric key in HEX format
    -iv hex             IV in HEX format, 7 to 13 bytes
    -aad str            Authenticated-only message
    -aad_hex hex        Authenticated-only data in HEX format
    -taglen num         MAC tag length, 4 to 16 bytes
    -in file | stdin    Input data. Encrypt input can be any byte length within CCM limits
                        Decrypt input is ciphertext || tag and must be at least taglen bytes
    -out file | stdout  Output data

Examples

    KEY=`gmssl rand -outlen 16 -hex`
    IV=`gmssl rand -outlen 12 -hex`
    echo -n abc | gmssl sm4_ccm -encrypt -key $KEY -iv $IV -aad_hex 001122 -out sm4_ccm_ciphertext.bin
    gmssl sm4_ccm -decrypt -key $KEY -iv $IV -aad_hex 001122 -in sm4_ccm_ciphertext.bin
```

</details>

### `gmssl sm4_xts`

**帮助命令**：`gmssl sm4_xts -help`。**用法**：`usage: gmssl sm4_xts {-encrypt|-decrypt} -key hex -iv hex -data_unit_size num [-in file] [-out file]`

**作用**：按数据单元执行 SM4-XTS 存储加解密。

**参数解读**：面向数据单元的磁盘/扇区模式，`-data_unit_size` 必须明确；不是一般文件的认证加密。

**帮助中需要先理解的参数**：

- `-encrypt`：选择加密动作；本机帮助描述：Encrypt
- `-decrypt`：选择解密动作；本机帮助描述：Decrypt

**帮助给出的命令示例（未作为本项目验收）**：

```bash
gmssl sm4_xts -encrypt -key $KEY -iv $IV -data_unit_size 512 -in sm4_xts_plaintext.bin -out sm4_xts_ciphertext.bin
```

<details><summary>展开本机 `-help` 原文</summary>

```text
usage: gmssl sm4_xts {-encrypt|-decrypt} -key hex -iv hex -data_unit_size num [-in file] [-out file]

Options

    -encrypt              Encrypt
    -decrypt              Decrypt
    -key hex              Symmetric key in HEX format, 32 bytes
    -iv hex               IV (tweak in XTS), 16 bytes
    -data_unit_size num   Encrypted disk sector size, typically 512 or 4096 bytes
                          Input and output lengths must be multiples of this size
    -in file | stdin      Input data, length must be a multiple of data_unit_size
    -out file | stdout    Output data

Examples

    KEY=`gmssl rand -outlen 32 -hex`
    IV=`gmssl rand -outlen 16 -hex`
    gmssl rand -outlen 512 -out sm4_xts_plaintext.bin
    gmssl sm4_xts -encrypt -key $KEY -iv $IV -data_unit_size 512 -in sm4_xts_plaintext.bin -out sm4_xts_ciphertext.bin
    gmssl sm4_xts -decrypt -key $KEY -iv $IV -data_unit_size 512 -in sm4_xts_ciphertext.bin -out sm4_xts_decrypted.bin
```

</details>

### `gmssl sm4_ff1`

**帮助命令**：`gmssl sm4_ff1 -help`。**用法**：`usage: gmssl sm4_ff1 {-encrypt|-decrypt} -key hex [-tweak hex] [-idcard|-bankcard] [-digits digits]`

**作用**：对限定格式的数字字符串执行 SM4-FF1 格式保留加密。

**参数解读**：格式保留加密，`-digits` 是数字数据；`-tweak` 不同于随机密钥。

**帮助中需要先理解的参数**：

- `-encrypt`：选择加密动作；本机帮助描述：Encrypt
- `-decrypt`：选择解密动作；本机帮助描述：Decrypt
- `-idcard`：本机帮助描述：Input is a Chinese resident identity card number, 18 characters
- `-bankcard`：本机帮助描述：Input is a bank card number with Luhn check digit, 9 to 19 digits

**帮助给出的命令示例（未作为本项目验收）**：

```bash
CIPHERTEXT=`gmssl sm4_ff1 -encrypt -key $KEY -digits 0123456789012345`
```

<details><summary>展开本机 `-help` 原文</summary>

```text
usage: gmssl sm4_ff1 {-encrypt|-decrypt} -key hex [-tweak hex] [-idcard|-bankcard] [-digits digits]

Options

    -encrypt            Encrypt
    -decrypt            Decrypt
    -key hex            SM4 key in HEX format
    -tweak hex          FF1 tweak in HEX format
    -digits digits      Input digits, default from stdin. Length must be 8 to 18 digits
    -idcard             Input is a Chinese resident identity card number, 18 characters
    -bankcard           Input is a bank card number with Luhn check digit, 9 to 19 digits

Examples

    KEY=`gmssl rand -outlen 16 -hex`
    CIPHERTEXT=`gmssl sm4_ff1 -encrypt -key $KEY -digits 0123456789012345`
    gmssl sm4_ff1 -decrypt -key $KEY -digits $CIPHERTEXT
```

</details>

### `gmssl sm4_cbc_mac`

**帮助命令**：`gmssl sm4_cbc_mac -help`。**用法**：`usage: gmssl sm4_cbc_mac -key hex [-in file | -in_str str] [-bin|-hex] [-out file]`

**作用**：计算 SM4-CBC-MAC 标签。

**参数解读**：输出认证标签；CBC-MAC 的消息域和用途须按协议固定。

**帮助中需要先理解的参数**：

- `-hex`：本机帮助描述：Output MAC-tag as hex string (by default)
- `-bin`：本机帮助描述：Output MAC-tag as binary

**帮助给出的命令示例（未作为本项目验收）**：

```bash
gmssl sm4_cbc_mac -key $KEY -in_str abc
```

<details><summary>展开本机 `-help` 原文</summary>

```text
usage: gmssl sm4_cbc_mac -key hex [-in file | -in_str str] [-bin|-hex] [-out file]

Options

    -key hex               Hex string of the MAC key, 16 bytes
    -in_str str            Input as text string, any byte length is accepted
    -in file | stdin       Input file path, any byte length is accepted
                           `-in_str` and `-in` should not be used together
                           If neither `-in` nor `-in_str` specified, read from stdin
    -hex                   Output MAC-tag as hex string (by default)
    -bin                   Output MAC-tag as binary
                           `-hex` and `-bin` should not be used together
    -out file | stdout     Output file path. If not specified, output to stdout

Examples

    KEY=`gmssl rand -outlen 16 -hex`
    gmssl sm4_cbc_mac -key $KEY -in_str abc

    gmssl sm4_cbc_mac -key $KEY -in_str abc -bin

    gmssl sm4_cbc_mac -key $KEY -in /path/to/file

    When reading from stdin, make sure the trailing newline character is removed

    Linux/Mac:
    echo -n abc | gmssl sm4_cbc_mac -key $KEY

    Windows:
    echo |set/p="abc" | gmssl sm4_cbc_mac -key 11223344556677881122334455667788
```

</details>

### `gmssl ghash`

**帮助命令**：`gmssl ghash -help`。**用法**：`usage: gmssl ghash [-in_str str|-in file] [-hex|-bin] [-out file]`

**作用**：计算 GCM 内部使用的 GHASH 值。

**参数解读**：GCM 的内部散列构件，不可将其单独当作文件摘要或认证加密。

**帮助中需要先理解的参数**：

- `-hex`：本机帮助描述：Output hash value as hex string (by default)
- `-bin`：本机帮助描述：Output hash value as binary

**帮助给出的命令示例（未作为本项目验收）**：

```bash
gmssl ghash -h $KEY -aad $AAD -in_str $TEXT
```

<details><summary>展开本机 `-help` 原文</summary>

```text
usage: gmssl ghash [-in_str str|-in file] [-hex|-bin] [-out file]
Options

    -h hex                 H value of GHASH, a ciphertext block of encrypted zeros
    -aad str               Authenticated-only message
    -aad_hex hex           Authenticated-only data in HEX format
    -in_str str            To be hashed string
    -in file | stdin       To be hashed file path
                           `-in_str` and `-in` should not be used together
                           If neither `-in` nor `-in_str` specified, read from stdin
    -hex                   Output hash value as hex string (by default)
    -bin                   Output hash value as binary
    -out file | stdout     Output file path. If not specified, output to stdout

Examples

    TEXT=`gmssl rand -outlen 20 -hex`
    KEY=`gmssl rand -outlen 16 -hex`
    AAD="The AAD Data"
    gmssl ghash -h $KEY -aad $AAD -in_str $TEXT
```

</details>

## ZUC 流密码与移动通信模式

### `gmssl zuc`

**帮助命令**：`gmssl zuc -help`。**用法**：`usage: zuc -key hex -iv hex [-in file] [-out file]`

**作用**：用 ZUC 密钥流变换输入数据。

<details><summary>展开本机 `-help` 原文</summary>

```text
usage: zuc -key hex -iv hex [-in file] [-out file]
```

</details>

### `gmssl zuc256`

**帮助命令**：`gmssl zuc256 -help`。**用法**：`usage: gmssl zuc256 -key hex -iv hex [-in file] [-out file]`

**作用**：用 ZUC-256 密钥流变换输入数据。

**帮助给出的命令示例（未作为本项目验收）**：

```bash
gmssl zuc256 -key 0000000000000000000000000000000000000000000000000000000000000000 \
-iv 0000000000000000000000000000000000000000000000 -in plaintext.bin -out ciphertext.bin
```

<details><summary>展开本机 `-help` 原文</summary>

```text
usage: gmssl zuc256 -key hex -iv hex [-in file] [-out file]
Options

    -key hex            ZUC-256 key in HEX format, 32 bytes
    -iv hex             ZUC-256 IV in HEX format, 23 bytes
    -in file | stdin    Input data
    -out file | stdout  Output data

Examples

    gmssl zuc256 -key 0000000000000000000000000000000000000000000000000000000000000000 \
        -iv 0000000000000000000000000000000000000000000000 -in plaintext.bin -out ciphertext.bin
```

</details>

### `gmssl zuc_128_eea3`

**帮助命令**：`gmssl zuc_128_eea3 -help`。**用法**：`usage: gmssl zuc_128_eea3 -key hex -count num -bearer num -direction num [-in file] [-out file]`

**作用**：按 128-EEA3 协议参数执行 ZUC 保密变换。

**参数解读**：移动通信保密算法；COUNT、BEARER、DIRECTION 是协议输入，不是普通文件 IV。

**帮助给出的命令示例（未作为本项目验收）**：

```bash
gmssl zuc_128_eea3 -key 173d14ba5003731d7a60049470f00a29 \
-count 0x66035492 -bearer 15 -direction 0 \
-in plaintext.bin -out ciphertext.bin
```

<details><summary>展开本机 `-help` 原文</summary>

```text
usage: gmssl zuc_128_eea3 -key hex -count num -bearer num -direction num [-in file] [-out file]
Options

    -key hex             128-EEA3 confidentiality key, 16 bytes
    -count num           COUNT parameter, 32-bit integer, decimal or 0x-prefixed hex
    -bearer num          BEARER parameter, 5-bit integer in [0, 31]
    -direction num       DIRECTION parameter, 0 or 1
    -in file | stdin     Input file path. If not specified, read from stdin
    -out file | stdout   Output ciphertext bytes. If not specified, output to stdout

Examples

    gmssl zuc_128_eea3 -key 173d14ba5003731d7a60049470f00a29 \
        -count 0x66035492 -bearer 15 -direction 0 \
        -in plaintext.bin -out ciphertext.bin
```

</details>

### `gmssl zuc_128_eia3`

**帮助命令**：`gmssl zuc_128_eia3 -help`。**用法**：`usage: gmssl zuc_128_eia3 -key hex -count num -bearer num -direction num [-in file] [-hex|-bin] [-out file]`

**作用**：按 128-EIA3 协议参数计算完整性标签。

**参数解读**：移动通信完整性算法；COUNT、BEARER、DIRECTION 要与协议双方一致。

**帮助中需要先理解的参数**：

- `-hex`：本机帮助描述：Output MAC as hex string (by default)
- `-bin`：本机帮助描述：Output MAC as binary

**帮助给出的命令示例（未作为本项目验收）**：

```bash
gmssl zuc_128_eia3 -key 00000000000000000000000000000000 \
-count 0 -bearer 0 -direction 0 -in message.bin
```

<details><summary>展开本机 `-help` 原文</summary>

```text
usage: gmssl zuc_128_eia3 -key hex -count num -bearer num -direction num [-in file] [-hex|-bin] [-out file]
Options

    -key hex             128-EIA3 integrity key, 16 bytes
    -count num           COUNT parameter, 32-bit integer, decimal or 0x-prefixed hex
    -bearer num          BEARER parameter, 5-bit integer in [0, 31]
    -direction num       DIRECTION parameter, 0 or 1
    -in file | stdin     Input file path. If not specified, read from stdin
    -hex                 Output MAC as hex string (by default)
    -bin                 Output MAC as binary
                         `-hex` and `-bin` should not be used together
    -out file | stdout   Output file path. If not specified, output to stdout

Examples

    gmssl zuc_128_eia3 -key 00000000000000000000000000000000 \
        -count 0 -bearer 0 -direction 0 -in message.bin
```

</details>

## SM9 身份密码

### `gmssl sm9setup`

**帮助命令**：`gmssl sm9setup -help`。**用法**：`usage: gmssl sm9setup -alg (sm9sign|sm9encrypt) [-pass password] [-out pem] [-pubout pem] [-verbose]`

**作用**：按签名或加密用途生成 SM9 主密钥对。

**参数解读**：产生 SM9 主私钥/主公钥；`-alg` 决定签名或加密用途。

**帮助中需要先理解的参数**：

- `-verbose`：本机帮助描述：Print details

**帮助给出的命令示例（未作为本项目验收）**：

```bash
gmssl sm9setup -alg sm9sign -pass P@ssw0rd -out sm9sign_msk.pem -pubout sm9sign_mpk.pem
```

<details><summary>展开本机 `-help` 原文</summary>

```text
usage: gmssl sm9setup -alg (sm9sign|sm9encrypt) [-pass password] [-out pem] [-pubout pem] [-verbose]
Options

    -alg sm9sign|sm9encrypt     Generate maeter key for sm9sign or sm9encrypt
    -pass pass                  Password to encrypt the master private key, prompt if not given
    -out pem                    Output password-encrypted master private key in PEM format
    -pubout pem                 Output master public key in PEM format
    -verbose                    Print details

Examples

    gmssl sm9setup -alg sm9sign -pass P@ssw0rd -out sm9sign_msk.pem -pubout sm9sign_mpk.pem
    gmssl sm9setup -alg sm9encrypt -pass P@ssw0rd -out sm9enc_msk.pem -pubout sm9enc_mpk.pem
```

</details>

### `gmssl sm9keygen`

**帮助命令**：`gmssl sm9keygen -help`。**用法**：`usage: gmssl sm9keygen -alg (sm9sign|sm9encrypt|sm9keyagreement) -in master_key.pem [-inpass str] -id str [-out pem] [-outpass str]`

**作用**：从主私钥及用户身份派生 SM9 用户私钥。

**参数解读**：主私钥、用户身份 `-id` 和用途 `-alg` 决定派生的用户私钥。

**帮助给出的命令示例（未作为本项目验收）**：

```bash
gmssl sm9keygen -alg sm9sign -in sm9sign_msk.pem -inpass P@ssw0rd -id Alice -out sm9sign.pem -outpass 123456
```

<details><summary>展开本机 `-help` 原文</summary>

```text
usage: gmssl sm9keygen -alg (sm9sign|sm9encrypt|sm9keyagreement) -in master_key.pem [-inpass str] -id str [-out pem] [-outpass str]
Options

    -alg sm9sign|sm9encrypt|sm9keyagreement
                                 Generate user's private key for sm9sign, sm9encrypt or sm9keyagreement
    -in pem                     SM9 master private key in PEM format
    -inpass pass                Password to decrypt the master private key, prompt if not given
    -id str                     User's identity
    -out pem                    Output password-encrypted user's private key in PEM format
    -outpass pass               Password to encrypt user's private key, prompt if not given

Examples

    gmssl sm9setup -alg sm9sign -pass P@ssw0rd -out sm9sign_msk.pem
    gmssl sm9keygen -alg sm9sign -in sm9sign_msk.pem -inpass P@ssw0rd -id Alice -out sm9sign.pem -outpass 123456

    gmssl sm9setup -alg sm9encrypt -pass P@ssw0rd -out sm9enc_msk.pem
    gmssl sm9keygen -alg sm9encrypt -in sm9enc_msk.pem -inpass P@ssw0rd -id Alice -out sm9enc.pem -outpass 123456
    gmssl sm9keygen -alg sm9keyagreement -in sm9enc_msk.pem -inpass P@ssw0rd -id Alice -out sm9exch.pem -outpass 123456
```

</details>

### `gmssl sm9sign`

**帮助命令**：`gmssl sm9sign -help`。**用法**：`usage: gmssl sm9sign -key pem [-pass str] [-in file] [-out file]`

**作用**：用 SM9 用户签名私钥生成签名。

**帮助给出的命令示例（未作为本项目验收）**：

```bash
echo -n 'message to be signed' | gmssl sm9sign -key sm9sign.pem -pass 123456 -out sm9.sig
```

<details><summary>展开本机 `-help` 原文</summary>

```text
usage: gmssl sm9sign -key pem [-pass str] [-in file] [-out file]
Options

    -key pem            Signing private key file in PEM format
    -pass str           Password to open the private key, prompt if not given
    -in file | stdin    To be signed file or data
    -out file | stdout  Output signature in binary DER encoding

Examples

    gmssl sm9setup -alg sm9sign -pass P@ssw0rd -out sm9sign_msk.pem -pubout sm9sign_mpk.pem
    gmssl sm9keygen -alg sm9sign -in sm9sign_msk.pem -inpass P@ssw0rd -id Alice -out sm9sign.pem -outpass 123456

    echo -n 'message to be signed' | gmssl sm9sign -key sm9sign.pem -pass 123456 -out sm9.sig
    echo -n 'message to be signed' | gmssl sm9verify -pubmaster sm9sign_mpk.pem -id Alice -sig sm9.sig
```

</details>

### `gmssl sm9verify`

**帮助命令**：`gmssl sm9verify -help`。**用法**：`usage: gmssl sm9verify [-in file] -pubmaster file -id str -sig file`

**作用**：用 SM9 主公钥、用户身份和原文验证签名。

**参数解读**：需主公钥、身份与签名；身份错误会使验签失败。

**帮助给出的命令示例（未作为本项目验收）**：

```bash
echo -n 'message to be signed' | gmssl sm9verify -pubmaster sm9sign_mpk.pem -id Alice -sig sm9.sig
```

<details><summary>展开本机 `-help` 原文</summary>

```text
usage: gmssl sm9verify [-in file] -pubmaster file -id str -sig file
Options

    -pubmaster pem      Master public key in PEM format
    -in file | stdin    Signed file or data
    -id str             Signer's identity string
    -out file | stdout  Output signature in binary DER encoding

Examples

    gmssl sm9setup -alg sm9sign -pass P@ssw0rd -out sm9sign_msk.pem -pubout sm9sign_mpk.pem
    gmssl sm9keygen -alg sm9sign -in sm9sign_msk.pem -inpass P@ssw0rd -id Alice -out sm9sign.pem -outpass 123456

    echo -n 'message to be signed' | gmssl sm9sign -key sm9sign.pem -pass 123456 -out sm9.sig
    echo -n 'message to be signed' | gmssl sm9verify -pubmaster sm9sign_mpk.pem -id Alice -sig sm9.sig
```

</details>

### `gmssl sm9encrypt`

**帮助命令**：`gmssl sm9encrypt -help`。**用法**：`usage: gmssl sm9encrypt -pubmaster file -id str [-in file] [-out file]`

**作用**：用 SM9 主公钥及接收者身份加密消息。

**帮助给出的命令示例（未作为本项目验收）**：

```bash
echo 'Secret text' | gmssl sm9encrypt -pubmaster sm9enc_mpk.pem -id Alice -out sm9_ciphertext.der
```

<details><summary>展开本机 `-help` 原文</summary>

```text
usage: gmssl sm9encrypt -pubmaster file -id str [-in file] [-out file]
Options

    -pubmaster pem      Master public key in PEM format
    -in file | stdin    To be encrypted file or data
    -id str             Recipient's identity string
    -out file | stdout  Output signature in binary DER encoding

Examples

    gmssl sm9setup -alg sm9encrypt -pass P@ssw0rd -out sm9enc_msk.pem -pubout sm9enc_mpk.pem
    gmssl sm9keygen -alg sm9encrypt -in sm9enc_msk.pem -inpass P@ssw0rd -id Alice -out sm9enc.pem -outpass 123456

    echo 'Secret text' | gmssl sm9encrypt -pubmaster sm9enc_mpk.pem -id Alice -out sm9_ciphertext.der
    gmssl sm9decrypt -key sm9enc.pem -pass 123456 -id Alice -in sm9_ciphertext.der
```

</details>

### `gmssl sm9decrypt`

**帮助命令**：`gmssl sm9decrypt -help`。**用法**：`usage: gmssl sm9decrypt -key pem [-pass str] -id str [-in file] [-out file]`

**作用**：用 SM9 用户私钥解密消息。

**帮助给出的命令示例（未作为本项目验收）**：

```bash
gmssl sm9decrypt -key sm9enc.pem -pass 123456 -id Alice -in sm9_ciphertext.der
```

<details><summary>展开本机 `-help` 原文</summary>

```text
usage: gmssl sm9decrypt -key pem [-pass str] -id str [-in file] [-out file]
Options

    -key pem            Recipient's private key in PEM format
    -pass str           Password to open the private key, prompt if not given
    -id str             Recipient's identity string
    -in file | stdin    Encrypted file or data
    -out file | stdout  Output plaintext

Examples

    gmssl sm9setup -alg sm9encrypt -pass P@ssw0rd -out sm9enc_msk.pem -pubout sm9enc_mpk.pem
    gmssl sm9keygen -alg sm9encrypt -in sm9enc_msk.pem -inpass P@ssw0rd -id Alice -out sm9enc.pem -outpass 123456

    echo 'Secret text' | gmssl sm9encrypt -pubmaster sm9enc_mpk.pem -id Alice -out sm9_ciphertext.der
    gmssl sm9decrypt -key sm9enc.pem -pass 123456 -id Alice -in sm9_ciphertext.der
```

</details>

### `gmssl sm9exch`

**帮助命令**：`gmssl sm9exch -help`。**用法**：`usage: gmssl sm9exch -stage init|respond|confirm|finish [options]`

**作用**：按阶段协议执行 SM9 身份密钥交换。

**帮助中需要先理解的参数**：

- `-hex`：本机帮助描述：Encode input/output data in hex, default
- `-bin`：本机帮助描述：Encode input/output data in binary

**帮助给出的命令示例（未作为本项目验收）**：

```bash
gmssl sm9exch -stage init \
-pubmaster sm9_mpk.pem -peer_id Bob \
-exch_keyout alice_ra.pem -out ra.hex
```

<details><summary>展开本机 `-help` 原文</summary>

```text
usage: gmssl sm9exch -stage init|respond|confirm|finish [options]

Options

    -stage init|respond|confirm|finish
                            SM9 key exchange stage
    -pubmaster pem          SM9 exchange master public key in PEM format
    -key pem                Local SM9 exchange private key in PEM format
    -pass str               Password to open local private key, prompt if not given
    -id str                 Local SM9 identity
    -id_hex hex             Local SM9 identity in hex
    -peer_id str            Peer SM9 identity
    -peer_id_hex hex        Peer SM9 identity in hex
    -in file | stdin        Input data for this stage
                            respond: RA, 65 bytes
                            confirm: RB || SB, 97 bytes
                            finish: SA, 32 bytes
    -out file | stdout      Output data to send to peer
                            init: RA, 65 bytes
                            respond: RB || SB, 97 bytes
                            confirm: SA, 32 bytes
    -exch_keyout pem        Output local ephemeral exchange state r||R in PEM format
    -exch_key pem           Input local ephemeral exchange state r||R in PEM format
    -keylen num             Shared key length in bytes, 32 by default
    -keyout file            Output shared key
    -hex                    Encode input/output data in hex, default
    -bin                    Encode input/output data in binary

Examples

    gmssl sm9setup -alg sm9encrypt -pass P@ssw0rd \
        -out sm9_msk.pem -pubout sm9_mpk.pem
    gmssl sm9keygen -alg sm9keyagreement -in sm9_msk.pem -inpass P@ssw0rd \
        -id Alice -out alice.pem -outpass 123456
    gmssl sm9keygen -alg sm9keyagreement -in sm9_msk.pem -inpass P@ssw0rd \
        -id Bob -out bob.pem -outpass 123456
    gmssl sm9exch -stage init \
        -pubmaster sm9_mpk.pem -peer_id Bob \
        -exch_keyout alice_ra.pem -out ra.hex
    gmssl sm9exch -stage respond \
        -pubmaster sm9_mpk.pem -key bob.pem -pass 123456 -id Bob \
        -peer_id Alice -in ra.hex \
        -exch_keyout bob_rb.pem -out rb_sb.hex
    gmssl sm9exch -stage confirm \
        -pubmaster sm9_mpk.pem -key alice.pem -pass 123456 -id Alice \
        -peer_id Bob -exch_key alice_ra.pem -in rb_sb.hex \
        -keylen 48 -keyout alice_shared_key.hex -out sa.hex
    gmssl sm9exch -stage finish \
        -pubmaster sm9_mpk.pem -key bob.pem -pass 123456 -id Bob \
        -peer_id Alice -exch_key bob_rb.pem \
        -in sa.hex -keylen 48 -keyout bob_shared_key.hex

Notes

    RA and RB are fixed 65-byte uncompressed SM9 curve points.
    The respond output is RB || SB, fixed 97 bytes.
    The ephemeral exchange state contains secret scalar r, public point R and optional peer point.
    -hex and -bin affect RA, RB||SB, SA and shared key files.
```

</details>

## 请求、证书、CRL 与在线状态

### `gmssl reqgen`

**帮助命令**：`gmssl reqgen -help`。**用法**：`usage: gmssl reqgen [-C str] [-ST str] [-L str] [-O str] [-OU str] -CN str -key file [-algor str] [-pass pass] [-sig_alg str] [-sm2_id str | -sm2_id_hex hex] [-out pem]`

**作用**：依据主体字段和私钥生成证书签名请求 CSR。

**参数解读**：`-CN` 与 `-key` 是核心输入，`-out` 为 CSR；算法和签名 ID 要与密钥匹配。

**帮助中需要先理解的参数**：

- `-C`：本机帮助描述：str                      Country
- `-L`：本机帮助描述：str                      Locality
- `-O`：本机帮助描述：str                      Organization

**帮助给出的命令示例（未作为本项目验收）**：

```bash
gmssl reqgen -CN www.gmssl.org -key sm2key.pem -pass P@ssw0rd -out sm2req.pem
```

<details><summary>展开本机 `-help` 原文</summary>

```text
usage: gmssl reqgen [-C str] [-ST str] [-L str] [-O str] [-OU str] -CN str -key file [-algor str] [-pass pass] [-sig_alg str] [-sm2_id str | -sm2_id_hex hex] [-out pem]

Options

    -key file                    Private key file in PKCS#8 PEM format or raw binary
    -algor str                   Public key algorithm, supported algorithms:
                                   * ecPublicKey
                                   * lms-hashsig
                                   * hss-lms-hashsig
                                   * xmss-hashsig
                                   * xmssmt-hashsig
                                   * shpincs-hashsig
    -pass pass                   Password for decrypting private key file, prompt if not given
    -sig_alg str                 Signature algorithm OID name, default sm2sign-with-sm3
    -sm2_id str                  Signer's ID in SM2 signature algorithm
    -sm2_id_hex hex              Signer's ID in hex format
                                 When `-sm2_id` or `-sm2_id_hex` is specified,
                                   must use the same ID in other commands explicitly.
                                 If neither `-sm2_id` nor `-sm2_id_hex` is specified,
                                   the default string '1234567812345678' is used
    -out file                    Output Certificate Request (CSR) file in PEM format

    Subject options

    -C  str                      Country
    -ST str                      State or province name
    -L  str                      Locality
    -O  str                      Organization
    -OU str                      Organizational unit
    -CN str                      Common name

Examples

    gmssl sm2keygen -pass P@ssw0rd -out sm2key.pem
    gmssl reqgen -CN www.gmssl.org -key sm2key.pem -pass P@ssw0rd -out sm2req.pem

    gmssl eckeygen -curve secp256r1 -pass P@ssw0rd -out p256key.pem
    gmssl reqgen -CN www.gmssl.org -key p256key.pem -pass P@ssw0rd -out p256req.pem
```

</details>

### `gmssl reqsign`

**帮助命令**：`gmssl reqsign -help`。**用法**：`usage: gmssl reqsign  [-in pem] [-req_sm2_id str | -req_sm2_id_hex hex] [-serial_len num] -days num -cacert pem -key file [-pass pass] [-sig_alg str] [-sm2_id str | -sm2_id_hex hex] [-gen_authority_key_id] [-gen_subject_key_id] [-key_usage str]* [-subject_dns_name str]* [-issuer_dns_name str]* [-ca -path_len_constraint num] [-ext_key_usage str]* [-crl_http_uri uri] [-crl_ldap_uri uri] [-inhibit_any_policy num] [-ca_issuers_uri uri] [-ocsp_uri uri uri] [-out pem]`

**作用**：由 CA 证书与私钥签发 CSR，产生证书。

**参数解读**：需 CSR、CA 证书和 CA 私钥；`-days`、序列号与扩展决定新证书属性。

**帮助中需要先理解的参数**：

- `-gen_authority_key_id`：本机帮助描述：Generate AuthorityKeyIdentifier extension use SM3
- `-gen_subject_key_id`：本机帮助描述：Generate SubjectKeyIdentifier extension use SM3
- `-ca`：本机帮助描述：Set cA of BasicConstaints extension

**帮助给出的命令示例（未作为本项目验收）**：

```bash
gmssl reqsign -in careq.pem -serial_len 12 -days 365 \
-cacert rootcacert.pem -key rootcakey.pem -pass P@ssw0rd \
-ca -path_len_constraint 0 \
-key_usage keyCertSign -key_usage cRLSign \
-crl_http_uri http://pku.edu.cn/ca.crl \
-ca_issuers_uri http://pku.edu.cn/ca.crt -ocsp_uri http://ocsp.pku.edu.cn \
-out cacert.pem
```

<details><summary>展开本机 `-help` 原文</summary>

```text
usage: gmssl reqsign  [-in pem] [-req_sm2_id str | -req_sm2_id_hex hex] [-serial_len num] -days num -cacert pem -key file [-pass pass] [-sig_alg str] [-sm2_id str | -sm2_id_hex hex] [-gen_authority_key_id] [-gen_subject_key_id] [-key_usage str]* [-subject_dns_name str]* [-issuer_dns_name str]* [-ca -path_len_constraint num] [-ext_key_usage str]* [-crl_http_uri uri] [-crl_ldap_uri uri] [-inhibit_any_policy num] [-ca_issuers_uri uri] [-ocsp_uri uri uri] [-out pem]

Options

    -in pem | stdin              Input CSR file in PEM format
    -req_sm2_id str              CSR Owner's ID in SM2 signature algorithm
    -req_sm2_id_hex hex          CSR Owner's ID in hex format
                                 When `-req_sm2_id` or `-req_sm2_id_hex` is specified,
                                   must use the same ID in other commands explicitly.
                                 If neither `-req_sm2_id` nor `-req_sm2_id_hex` is specified,
                                   the default string '1234567812345678' is used
    -serial_len num              Serial number length in bytes
    -days num                    Validity peroid in days
    -cacert pem                  Issuer CA certificate
    -key pem                     Issuer private key file in PEM format
    -sig_alg str                 Signature algorithm OID name, default sm2sign-with-sm3
    -sm2_id str                  Authority's ID in SM2 signature algorithm
    -sm2_id_hex hex              Authority's ID in hex format
                                 When `-sm2_id` or `-sm2_id_hex` is specified,
                                   must use the same ID in other commands explicitly.
                                 If neither `-sm2_id` nor `-sm2_id_hex` is specified,
                                   the default string '1234567812345678' is used
    -pass pass                   Password for decrypting private key file, prompt if not given
    -out pem                     Output certificate file in PEM format

    Extension options

    -gen_authority_key_id        Generate AuthorityKeyIdentifier extension use SM3
    -gen_subject_key_id          Generate SubjectKeyIdentifier extension use SM3
    -key_usage str               Add KeyUsage extension
                                 this option can be called multi-times
                                 avaiable values:
                                     digitalSignature
                                     nonRepudiation
                                     keyEncipherment
                                     dataEncipherment
                                     keyAgreement
                                     keyCertSign
                                     cRLSign
                                     encipherOnly
                                     decipherOnly
    -subject_dns_name str        Add DNS name to SubjectAltName extension
                                 this option can be called multi-times
    -issuer_dns_name str         Add DNS name to IssuerAltName extension
                                 this option can be called multi-times
    -ca                          Set cA of BasicConstaints extension
    -path_len_constraint num    Set pathLenConstaint of BasicConstaints extension
    -ext_key_usage str           Set ExtKeyUsage extension
                                 this option can be called multi-times
                                 avaiable values:
                                     anyExtendedKeyUsage
                                     serverAuth
                                     clientAuth
                                     codeSigning
                                     emailProtection
                                     timeStamping
                                     OCSPSigning
    -crl_http_uri uri            Set HTTP URI of CRL of CRLDistributionPoints extension
    -crl_ldap_uri uri            Set LDAP URI of CRL of CRLDistributionPoints extension
    -inhibit_any_policy num      Set skipCerts number of InhibitAnyPolicy extension
    -ca_issuers_uri uri          Set URI of the CA certificate in DER-encoding o FreshestCRL extension
    -ocsp_uri uri                Set OCSP URI of FreshestCRL extension

Examples

    # Generate self-signed root CA certificate

    gmssl sm2keygen -pass P@ssw0rd -out rootcakey.pem
    gmssl certgen -C CN -ST Beijing -L Haidian -O PKU -OU CS -CN ROOTCA -days 3650 \
        -key rootcakey.pem -pass P@ssw0rd \
        -ca -path_len_constraint 6 \
        -key_usage keyCertSign -key_usage cRLSign \
        -crl_http_uri http://pku.edu.cn/ca.crl \
        -ca_issuers_uri http://pku.edu.cn/ca.crt -ocsp_uri http://ocsp.pku.edu.cn \
        -out rootcacert.pem

    # Generate sub-CA certificate request

    gmssl sm2keygen -pass P@ssw0rd -out cakey.pem
    gmssl reqgen -C CN -ST Beijing -L Haidian -O PKU -OU CS -CN CA -key cakey.pem -pass P@ssw0rd -out careq.pem

    # Sign certificate request to generate sub-CA certificate

    gmssl reqsign -in careq.pem -serial_len 12 -days 365 \
        -cacert rootcacert.pem -key rootcakey.pem -pass P@ssw0rd \
        -ca -path_len_constraint 0 \
        -key_usage keyCertSign -key_usage cRLSign \
        -crl_http_uri http://pku.edu.cn/ca.crl \
        -ca_issuers_uri http://pku.edu.cn/ca.crt -ocsp_uri http://ocsp.pku.edu.cn \
        -out cacert.pem
```

</details>

### `gmssl reqparse`

**帮助命令**：`gmssl reqparse -help`。**用法**：`usage: reqparse [-in file] [-out file]`

**作用**：解析并打印证书签名请求字段。

<details><summary>展开本机 `-help` 原文</summary>

```text
usage: reqparse [-in file] [-out file]
```

</details>

### `gmssl certgen`

**帮助命令**：`gmssl certgen -help`。**用法**：`usage: gmssl certgen [-C str] [-ST str] [-L str] [-O str] [-OU str] -CN str -serial_len num -days num -key pem [-algor str] [-pass pass] [-sig_alg str] [-sm2_id str | -sm2_id_hex hex] [-gen_authority_key_id] [-gen_subject_key_id] [-key_usage str]* [-subject_dns_name str]* [-issuer_dns_name str]* [-ca -path_len_constraint num] [-ext_key_usage str]* [-crl_http_uri uri] [-crl_ldap_uri uri] [-inhibit_any_policy num] [-ca_issuers_uri uri] [-ocsp_uri uri uri] [-out pem]`

**作用**：用私钥生成自签名测试证书。

**参数解读**：用指定私钥自签证书；`-CN`、`-days`、`-serial_len` 和扩展必须明确。

**帮助中需要先理解的参数**：

- `-C`：本机帮助描述：str                      Country
- `-L`：本机帮助描述：str                      Locality
- `-O`：本机帮助描述：str                      Organization
- `-gen_authority_key_id`：本机帮助描述：Generate AuthorityKeyIdentifier extension use SM3
- `-gen_subject_key_id`：本机帮助描述：Generate SubjectKeyIdentifier extension use SM3
- `-ca`：本机帮助描述：Set cA of BasicConstaints extension

**帮助给出的命令示例（未作为本项目验收）**：

```bash
gmssl certgen -C CN -ST Beijing -L Haidian -O PKU -OU CS -CN ROOTCA -days 3650 \
-key rootcakey.pem -pass P@ssw0rd \
-ca -path_len_constraint 6 \
-key_usage keyCertSign -key_usage cRLSign \
-crl_http_uri http://pku.edu.cn/ca.crl \
-ca_issuers_uri http://pku.edu.cn/ca.crt -ocsp_uri http://ocsp.pku.edu.cn \
-out rootcacert.pem
```

<details><summary>展开本机 `-help` 原文</summary>

```text
usage: gmssl certgen [-C str] [-ST str] [-L str] [-O str] [-OU str] -CN str -serial_len num -days num -key pem [-algor str] [-pass pass] [-sig_alg str] [-sm2_id str | -sm2_id_hex hex] [-gen_authority_key_id] [-gen_subject_key_id] [-key_usage str]* [-subject_dns_name str]* [-issuer_dns_name str]* [-ca -path_len_constraint num] [-ext_key_usage str]* [-crl_http_uri uri] [-crl_ldap_uri uri] [-inhibit_any_policy num] [-ca_issuers_uri uri] [-ocsp_uri uri uri] [-out pem]

Options

    -serial_len num              Serial number length in bytes
    -days num                    Validity peroid in days
    -key file                    Private key file in PEM format
    -algor str                   Public key algorithm
    -pass pass                   Password for decrypting private key file, prompt if not given
    -sig_alg str                 Signature algorithm OID name, default sm2sign-with-sm3
    -sm2_id str                  Signer's ID in SM2 signature algorithm
    -sm2_id_hex hex              Signer's ID in hex format
                                 When `-sm2_id` or `-sm2_id_hex` is specified,
                                   must use the same ID in other commands explicitly.
                                 If neither `-sm2_id` nor `-sm2_id_hex` is specified,
                                   the default string '1234567812345678' is used
    -out file                    Output certificate file in PEM format

    Subject and Issuer options

    -C  str                      Country
    -ST str                      State or province name
    -L  str                      Locality
    -O  str                      Organization
    -OU str                      Organizational unit
    -CN str                      Common name

    Extension options

    -gen_authority_key_id        Generate AuthorityKeyIdentifier extension use SM3
    -gen_subject_key_id          Generate SubjectKeyIdentifier extension use SM3
    -key_usage str               Add KeyUsage extension
                                 this option can be called multi-times
                                 avaiable values:
                                     * digitalSignature
                                     * nonRepudiation
                                     * keyEncipherment
                                     * dataEncipherment
                                     * keyAgreement
                                     * keyCertSign
                                     * cRLSign
                                     * encipherOnly
                                     * decipherOnly
    -subject_dns_name str        Add DNS name to SubjectAltName extension
                                 this option can be called multi-times
    -issuer_dns_name str         Add DNS name to IssuerAltName extension
                                 this option can be called multi-times
    -ca                          Set cA of BasicConstaints extension
    -path_len_constraint num     Set pathLenConstraint of BasicConstaints extension
    -ext_key_usage str           Set ExtKeyUsage extension
                                 this option can be called multi-times
                                 avaiable values:
                                     * anyExtendedKeyUsage
                                     * serverAuth
                                     * clientAuth
                                     * codeSigning
                                     * emailProtection
                                     * timeStamping
                                     * OCSPSigning
    -crl_http_uri uri            Set HTTP URI of CRL of CRLDistributionPoints extension
    -crl_ldap_uri uri            Set LDAP URI of CRL of CRLDistributionPoints extension
    -inhibit_any_policy num      Set skipCerts number of InhibitAnyPolicy extension
    -ca_issuers_uri uri          Set URI of the CA certificate in DER-encoding o FreshestCRL extension
    -ocsp_uri uri                Set OCSP URI of FreshestCRL extension

Examples

    gmssl sm2keygen -pass P@ssw0rd -out rootcakey.pem

    gmssl certgen -C CN -ST Beijing -L Haidian -O PKU -OU CS -CN ROOTCA -days 3650 \
        -key rootcakey.pem -pass P@ssw0rd \
        -ca -path_len_constraint 6 \
        -key_usage keyCertSign -key_usage cRLSign \
        -crl_http_uri http://pku.edu.cn/ca.crl \
        -ca_issuers_uri http://pku.edu.cn/ca.crt -ocsp_uri http://ocsp.pku.edu.cn \
        -out rootcacert.pem
```

</details>

### `gmssl certverify`

**帮助命令**：`gmssl certverify -help`。**用法**：`usage: gmssl certverify -in pem [-tlcp_server|-server|-client] -cacert pem [-crl der] [-ocsp der] [-hostname str]`

**作用**：按 CA 证书、用途、主机名等条件验证证书链。

**参数解读**：证书解析、有效期和信任验证是不同结果；需可信 `-cacert`。

**帮助中需要先理解的参数**：

- `-tlcp_server`：本机帮助描述：Verify TLCP server certificate chain, default
- `-server`：本机帮助描述：Verify TLS server certificate chain
- `-client`：本机帮助描述：Verify TLS client certificate chain

**帮助给出的命令示例（未作为本项目验收）**：

```bash
gmssl certverify -tlcp_server -in certs.pem -cacert cacerts.pem -hostname localhost
```

<details><summary>展开本机 `-help` 原文</summary>

```text
usage: gmssl certverify -in pem [-tlcp_server|-server|-client] -cacert pem [-crl der] [-ocsp der] [-hostname str]

Options

    -in pem             Certificate chain in PEM format
    -tlcp_server        Verify TLCP server certificate chain, default
    -server             Verify TLS server certificate chain
    -client             Verify TLS client certificate chain
    -cacert pem         Trusted CA certificate(s) in PEM format
    -crl der            CRL in DER format
    -ocsp der           OCSPResponse in DER format
    -hostname str       Server hostname for certificate verification

Examples

    gmssl certverify -tlcp_server -in certs.pem -cacert cacerts.pem -hostname localhost
```

</details>

### `gmssl certrevoke`

**帮助命令**：`gmssl certrevoke -help`。**用法**：`usage: gmssl certrevoke  -in pem [-reason str] [-invalid_date time] -out der`

**作用**：为证书生成吊销记录。

**帮助给出的命令示例（未作为本项目验收）**：

```bash
gmssl certrevoke -in cert1.pem -reason keyCompromise -invalid_date 20221230000000Z -out revoked_certs.der
```

<details><summary>展开本机 `-help` 原文</summary>

```text
usage: gmssl certrevoke  -in pem [-reason str] [-invalid_date time] -out der

Options

    -in pem                  Certificate in PEM format to be revoked
    -reason str              Revocation reason code, avaiable codes:
                                 * unspecified
                                 * keyCompromise
                                 * cACompromise
                                 * affiliationChanged
                                 * superseded
                                 * cessationOfOperation
                                 * certificateHold
                                 * notAssigned
                                 * removeFromCRL
                                 * privilegeWithdrawn
                                 * aACompromise
    -invalid_date time      The date on which it is known or suspected the certificate became invalid
                            Time in `YYYYMMDDHHMMSSZ` format such as 20221231000000Z
                            The last 'Z' means it is Zulu (GMT) time
    -out der                Output X.509 RevokedCertificate in DER-encoding
                            This file stores multiple RevokedCertificates, used as input by `crlsign`

Examples

    gmssl certrevoke -in cert1.pem -reason keyCompromise -invalid_date 20221230000000Z -out revoked_certs.der
    gmssl certrevoke -in cert1.pem -reason keyCompromise -invalid_date 20221230000000Z >> revoked_certs.der
```

</details>

### `gmssl certparse`

**帮助命令**：`gmssl certparse -help`。**用法**：`usage: gmssl certparse [-in pem] [-out file]`

**作用**：解析并打印证书字段。

**帮助给出的命令示例（未作为本项目验收）**：

```bash
gmssl certparse -in certs.pem
```

<details><summary>展开本机 `-help` 原文</summary>

```text
usage: gmssl certparse [-in pem] [-out file]

Options

    [-in pem]|stdin        Input certificates in PEM format.
                           This command supports continuous multiple certificates
                           Do not include blank line or comments between PEM data
    [-out file]stdout      Output file

Examples

    gmssl certparse -in certs.pem
```

</details>

### `gmssl crlget`

**帮助命令**：`gmssl crlget -help`。**用法**：`usage: gmssl crlget -cert pem [-out file]`

**作用**：从证书给出的地址下载 CRL。

**参数解读**：从证书中的 CRL 地址下载；需要网络，不能仅以帮助输出认定可用。

**帮助给出的命令示例（未作为本项目验收）**：

```bash
gmssl crlget -cert cert.pem -out crl.der
```

**运行条件**：需要受控网络端点、可信证书或测试服务；这里只验证帮助信息。

<details><summary>展开本机 `-help` 原文</summary>

```text
usage: gmssl crlget -cert pem [-out file]


Options

    -cert pem              Input certificates in PEM format.
    -out der | stdout      Output CRL file in DER-encoding

Examples

    gmssl crlget -cert cert.pem -out crl.der
```

</details>

### `gmssl crlgen`

**帮助命令**：`gmssl crlgen -help`。**用法**：`usage: crlgen  -in revoked_certs -cacert pem -key pem [-pass pass] [-sm2_id str | -sm2_id_hex hex] [-sig_alg str] [-next_update time]  [-gen_authority_key_id] [-crl_num num] [-delta_crl_indicator num] [-ca_issuers_uri uri] [-ocsp_uri uri] [-out der]`

**作用**：由 CA 对吊销记录签名生成 CRL。

**帮助给出的命令示例（未作为本项目验收）**：

```bash
gmssl crlgen -in revoked_certs.der -cacert cacert.pem -key cakey.pem -pass P@ssw0rd -gen_authority_key_id -crl_num 1
```

<details><summary>展开本机 `-help` 原文</summary>

```text
usage: crlgen  -in revoked_certs -cacert pem -key pem [-pass pass] [-sm2_id str | -sm2_id_hex hex] [-sig_alg str] [-next_update time]  [-gen_authority_key_id] [-crl_num num] [-delta_crl_indicator num] [-ca_issuers_uri uri] [-ocsp_uri uri] [-out der]


Options

    -in revoked_certs      To be revoked certificate list
                           This input file format is DER-encoding of SEQUENCE OF RevokedCertificate
                           revoked_certs.der can be generated by `gmssl certrevoke`
    -cacert pem            The issuer certificate
    -key pem               The issuer private key
    -pass pass             Password for decrypting private key file, prompt if not given
    -sig_alg str           Signature algorithm OID name, default sm2sign-with-sm3
    -sm2_id str            Authority's ID in SM2 signature algorithm
    -sm2_id_hex hex        Authority's ID in hex format
                           When `-sm2_id` or `-sm2_id_hex` is specified,
                             must use the same ID in other commands explicitly.
                           If neither `-sm2_id` nor `-sm2_id_hex` is specified,
                             the default string '1234567812345678' is used
    -next_update time      Optional CRL attribute
    -out der | stdout      Output CRL in DER-encoding

Examples

    gmssl crlgen -in revoked_certs.der -cacert cacert.pem -key cakey.pem -pass P@ssw0rd -gen_authority_key_id -crl_num 1
    gmssl crlgen -in revoked_certs.der -cacert cacert.pem -key cakey.pem -pass P@ssw0rd -gen_authority_key_id -crl_num 2
```

</details>

### `gmssl crlverify`

**帮助命令**：`gmssl crlverify -help`。**用法**：`usage: crlverify Options`

**作用**：用签发者证书验证 CRL。

<details><summary>展开本机 `-help` 原文</summary>

```text
usage: crlverify Options

    -in pem                      Input CSR file in PEM format
    -cacert pem                  Issuer CA certificate
    -sm2_id str                  Authority's ID in SM2 signature algorithm
    -sm2_id_hex hex              Authority's ID in hex format
                                 When `-sm2_id` or `-sm2_id_hex` is specified,
                                   must use the same ID in other commands explicitly.
                                 If neither `-sm2_id` nor `-sm2_id_hex` is specified,
                                   the default string '1234567812345678' is used

Examples

    gmssl certverify -in crl.der -cacert cacert.pem
```

</details>

### `gmssl crlparse`

**帮助命令**：`gmssl crlparse -help`。**用法**：`usage: crlparse -in file [-out file]`

**作用**：解析并打印 CRL 内容。

<details><summary>展开本机 `-help` 原文</summary>

```text
usage: crlparse -in file [-out file]
```

</details>

### `gmssl ocspreq`

**帮助命令**：`gmssl ocspreq -help`。**用法**：`usage: ocspreq -in pem [-digest name] [-out der] [-verbose]`

**作用**：生成 OCSP 证书状态请求。

**帮助中需要先理解的参数**：

- `-verbose`：本机帮助描述：Print OCSPRequest to stderr

**帮助给出的命令示例（未作为本项目验收）**：

```bash
gmssl ocspreq -in chain.pem -out req.der -verbose
```

<details><summary>展开本机 `-help` 原文</summary>

```text
usage: ocspreq -in pem [-digest name] [-out der] [-verbose]
Options

    -in pem             Input certificate chain file in PEM format
                        The first certificate is the certificate to be checked
                        The second certificate is its issuer certificate
    -digest name        Digest algorithm for CertID, default sm3
    -out der | stdout   Output OCSPRequest in DER format
    -verbose            Print OCSPRequest to stderr

Examples

    gmssl ocspreq -in chain.pem -out req.der -verbose
```

</details>

### `gmssl ocspget`

**帮助命令**：`gmssl ocspget -help`。**用法**：`usage: ocspget -cert pem [-url str] [-digest name] [-out der] [-verbose]`

**作用**：向响应方取得 OCSP 状态响应。

**参数解读**：请求在线状态；需要实际 responder、证书和可信链。

**帮助中需要先理解的参数**：

- `-verbose`：本机帮助描述：Print AuthorityInfoAccess, OCSPRequest and OCSPResponse to stderr

**帮助给出的命令示例（未作为本项目验收）**：

```bash
gmssl ocspget -cert chain.pem -out resp.der
```

**运行条件**：需要受控网络端点、可信证书或测试服务；这里只验证帮助信息。

<details><summary>展开本机 `-help` 原文</summary>

```text
usage: ocspget -cert pem [-url str] [-digest name] [-out der] [-verbose]
Options

    -cert pem           Input certificate chain file in PEM format
                        The first certificate is the certificate to be checked
                        The second certificate is its issuer certificate
    -url str            OCSP responder URL, overrides the OCSP URI in certificate AIA
    -digest name        Digest algorithm for CertID, default sm3
    -out der | stdout   Output OCSPResponse in DER format
    -verbose            Print AuthorityInfoAccess, OCSPRequest and OCSPResponse to stderr

Examples

    gmssl ocspget -cert chain.pem -out resp.der
    gmssl ocspget -cert chain.pem -url http://ocsp.example.com -out resp.der -verbose
```

</details>

### `gmssl ocspsign`

**帮助命令**：`gmssl ocspsign -help`。**用法**：`usage: ocspsign -reqin der -cacert pem -signer pem -key pem [-pass pass] [-status good|revoked|unknown] [-sig_alg str] [-revocation_time time] [-revocation_reason reason] [-this_update time] [-next_update time] [-produced_at time] [-resp_key_id] [-sm2_id str | -sm2_id_hex hex] [-single_exts der] [-response_exts der] [-cert pem] [-certs pem] [-out der] [-verbose]`

**作用**：由签名者生成 OCSP 状态响应。

**帮助中需要先理解的参数**：

- `-resp_key_id`：本机帮助描述：Use byKey ResponderID, default byName
- `-verbose`：本机帮助描述：Print OCSPRequest and OCSPResponse to stderr

**帮助给出的命令示例（未作为本项目验收）**：

```bash
gmssl ocspsign -reqin req.der -cacert cacert.pem -signer ocspcert.pem -key ocspkey.pem -pass P@ssw0rd -out resp.der -verbose
```

<details><summary>展开本机 `-help` 原文</summary>

```text
usage: ocspsign -reqin der -cacert pem -signer pem -key pem [-pass pass] [-status good|revoked|unknown] [-sig_alg str] [-revocation_time time] [-revocation_reason reason] [-this_update time] [-next_update time] [-produced_at time] [-resp_key_id] [-sm2_id str | -sm2_id_hex hex] [-single_exts der] [-response_exts der] [-cert pem] [-certs pem] [-out der] [-verbose]

Options

    -reqin der              Input OCSPRequest in DER format
    -cacert pem             Issuer CA certificate of the requested certificate
    -signer pem             OCSPResponse signer certificate
    -key pem                OCSPResponse signer private key
    -pass pass              Password for decrypting private key file, prompt if not given
    -status status          Certificate status: good, revoked or unknown, default good
    -sig_alg str            Signature algorithm OID name, default sm2sign-with-sm3
    -revocation_time time   Revocation time, required when status is revoked
    -revocation_reason str  Revocation reason, optional when status is revoked
    -this_update time       SingleResponse thisUpdate, default current time
    -next_update time       SingleResponse nextUpdate
    -produced_at time       ResponseData producedAt, default current time
    -resp_key_id            Use byKey ResponderID, default byName
    -sm2_id str             Signer's ID in SM2 signature algorithm
    -sm2_id_hex hex         Signer's ID in hex format
    -single_exts der        SingleResponse extensions in DER format
    -response_exts der      ResponseData extensions in DER format
    -cert pem               Include one certificate in BasicOCSPResponse
    -certs pem              Include certificates in BasicOCSPResponse
    -out der | stdout       Output OCSPResponse in DER format
    -verbose                Print OCSPRequest and OCSPResponse to stderr

Examples

    gmssl ocspsign -reqin req.der -cacert cacert.pem -signer ocspcert.pem -key ocspkey.pem -pass P@ssw0rd -out resp.der -verbose
    gmssl ocspsign -reqin req.der -cacert cacert.pem -signer cacert.pem -key cakey.pem -pass P@ssw0rd -status revoked -revocation_time 20260610000000Z -revocation_reason keyCompromise -out resp.der
```

</details>

### `gmssl ocspverify`

**帮助命令**：`gmssl ocspverify -help`。**用法**：`usage: ocspverify -reqin der -respin der -cacert pem -signer pem [-time time] [-clock_skew seconds] [-sm2_id str | -sm2_id_hex hex] [-certs pem] [-verbose]`

**作用**：验证 OCSP 请求/响应和签名者信息。

**帮助中需要先理解的参数**：

- `-verbose`：本机帮助描述：Print OCSPRequest and OCSPResponse to stderr

**帮助给出的命令示例（未作为本项目验收）**：

```bash
gmssl ocspverify -reqin req.der -respin resp.der -cacert cacert.pem -signer ocspcert.pem -verbose
```

<details><summary>展开本机 `-help` 原文</summary>

```text
usage: ocspverify -reqin der -respin der -cacert pem -signer pem [-time time] [-clock_skew seconds] [-sm2_id str | -sm2_id_hex hex] [-certs pem] [-verbose]

Options

    -reqin der          Input OCSPRequest in DER format
    -respin der         Input OCSPResponse in DER format
    -cacert pem         Issuer CA certificate of the requested certificate
    -signer pem         OCSPResponse signer certificate
    -time time          Verification time, default current time
    -clock_skew seconds Allowed clock skew in seconds, default 300
    -sm2_id str         Signer's ID in SM2 signature algorithm
    -sm2_id_hex hex     Signer's ID in hex format
    -certs pem          Extra certificates for verification context
    -verbose            Print OCSPRequest and OCSPResponse to stderr

Examples

    gmssl ocspverify -reqin req.der -respin resp.der -cacert cacert.pem -signer ocspcert.pem -verbose
```

</details>

### `gmssl sctverify`

**帮助命令**：`gmssl sctverify -help`。**用法**：`usage: sctverify -in file [-cert pem | -precert der] [-issuer_key_hash hex] -log_key pem [-log_key pem ...] [-at_least num] [-digest name] [-verbose]`

**作用**：按透明度日志公钥验证证书的 SCT 列表。

**参数解读**：验证证书透明度 SCT；需要日志公钥与相关证书。

**帮助中需要先理解的参数**：

- `-verbose`：本机帮助描述：Print verification result to stderr

**帮助给出的命令示例（未作为本项目验收）**：

```bash
gmssl sctverify -in sctlist.bin -cert cert.pem -log_key ctlog.pem -at_least 1
```

<details><summary>展开本机 `-help` 原文</summary>

```text
usage: sctverify -in file [-cert pem | -precert der] [-issuer_key_hash hex] -log_key pem [-log_key pem ...] [-at_least num] [-digest name] [-verbose]

Options

    -in file            Input SignedCertificateTimestampList in binary format
    -cert pem           Input certificate and verify SCTs over an x509_entry
    -precert der        Input TBSCertificate DER and verify SCTs over a precert_entry
    -issuer_key_hash hex
                        32-byte issuer key hash, required with -precert
    -log_key pem        CT Log public key in SubjectPublicKeyInfo PEM format
                        This option can be repeated
    -at_least num       Required number of successful SCT verifications, default 1
    -digest name        Digest for CT Log ID, default sha256
    -verbose            Print verification result to stderr

Examples

    gmssl sctverify -in sctlist.bin -cert cert.pem -log_key ctlog.pem -at_least 1
    gmssl sctverify -in sctlist.bin -precert tbs.der -issuer_key_hash HEX -log_key ctlog.pem
```

</details>

## CMS 容器

### `gmssl cmssign`

**帮助命令**：`gmssl cmssign -help`。**用法**：`usage: cmssign -key file [-pass str] -cert file -in file [-out file]`

**作用**：把文件签名封装为 CMS SignedData。

<details><summary>展开本机 `-help` 原文</summary>

```text
usage: cmssign -key file [-pass str] -cert file -in file [-out file]
```

</details>

### `gmssl cmsverify`

**帮助命令**：`gmssl cmsverify -help`。**用法**：`usage: cmsverify -in file [-out file]`

**作用**：验证 CMS SignedData 并提取内容。

<details><summary>展开本机 `-help` 原文</summary>

```text
usage: cmsverify -in file [-out file]
```

</details>

### `gmssl cmsencrypt`

**帮助命令**：`gmssl cmsencrypt -help`。**用法**：`usage: cmsencrypt -encrypt (-rcptcert pem)* -in file -out file`

**作用**：按接收者证书生成 CMS EnvelopedData。

<details><summary>展开本机 `-help` 原文</summary>

```text
usage: cmsencrypt -encrypt (-rcptcert pem)* -in file -out file
```

</details>

### `gmssl cmsdecrypt`

**帮助命令**：`gmssl cmsdecrypt -help`。**用法**：`usage: cmsdecrypt -key file [-pass str] -cert file -in file [-out file]`

**作用**：用接收者私钥解开 CMS EnvelopedData。

<details><summary>展开本机 `-help` 原文</summary>

```text
usage: cmsdecrypt -key file [-pass str] -cert file -in file [-out file]
```

</details>

### `gmssl cmsparse`

**帮助命令**：`gmssl cmsparse -help`。**用法**：`usage: cmsparse -in file`

**作用**：解析并打印 CMS 容器结构。

<details><summary>展开本机 `-help` 原文</summary>

```text
usage: cmsparse -in file
```

</details>

## 椭圆曲线、哈希签名与 KEM

### `gmssl eckeygen`

**帮助命令**：`gmssl eckeygen -help`。**用法**：`usage: gmssl eckeygen -curve str [-pass str] [-out pem] [-pubout pem]`

**作用**：在指定曲线上生成椭圆曲线密钥对。

**帮助给出的命令示例（未作为本项目验收）**：

```bash
gmssl eckeygen -curve secp256r1 -pass P@ssw0rd -out p256.pem
```

<details><summary>展开本机 `-help` 原文</summary>

```text
usage: gmssl eckeygen -curve str [-pass str] [-out pem] [-pubout pem]

Options

    -curve str                 EC curve name, supported curves: secp256r1, prime256v1, secp384r1
                               SM2 is not supported by this command, use `sm2keygen` instead
    -pass pass                  Password to encrypt the private key, prompt if not given
    -out pem                    Output password-encrypted PKCS #8 private key in PEM format
    -pubout pem                 Output public key in PEM format
    -export pem                 Output non-encrypted EC private key in PEM format

Examples

    gmssl eckeygen -curve secp256r1 -pass P@ssw0rd -out p256.pem
    gmssl eckeygen -curve secp384r1 -pass P@ssw0rd -out p384.pem -pubout p384pub.pem
```

</details>

### `gmssl lmskeygen`

**帮助命令**：`gmssl lmskeygen -help`。**用法**：`usage: gmssl lmskeygen -lms_type type -out file [-pubout file] [-verbose]`

**作用**：生成 LMS-SM3 哈希签名密钥对。

**帮助中需要先理解的参数**：

- `-verbose`：本机帮助描述：Print public key

<details><summary>展开本机 `-help` 原文</summary>

```text
usage: gmssl lmskeygen -lms_type type -out file [-pubout file] [-verbose]

Options
    -lms_type type              LMS Algorithm Type
                                 LMS_SM3_M32_H5
                                 LMS_SM3_M32_H10
                                 LMS_SM3_M32_H15
                                 LMS_SM3_M32_H20
                                 LMS_SM3_M32_H25
    -out file                   Output private key
    -pubout file                Output public key
    -verbose                    Print public key
```

</details>

### `gmssl lmssign`

**帮助命令**：`gmssl lmssign -help`。**用法**：`usage: lmssign -key file [-in file] [-out file] [-verbose]`

**作用**：用 LMS-SM3 私钥签名。

**帮助中需要先理解的参数**：

- `-verbose`：本机帮助描述：Print public key and signature

<details><summary>展开本机 `-help` 原文</summary>

```text
usage: lmssign -key file [-in file] [-out file] [-verbose]

Options
    -key file                   Input private key file
    -in file                    Input data file (if not using stdin)
    -out file                   Output signature file
    -verbose                    Print public key and signature
```

</details>

### `gmssl lmsverify`

**帮助命令**：`gmssl lmsverify -help`。**用法**：`usage: lmsverify -pubkey file [-in file] -sig file [-verbose]`

**作用**：用 LMS-SM3 公钥验签。

**帮助中需要先理解的参数**：

- `-verbose`：本机帮助描述：Print public key and signature

<details><summary>展开本机 `-help` 原文</summary>

```text
usage: lmsverify -pubkey file [-in file] -sig file [-verbose]

Options
    -pubkey file                Input public key file
    -in file                    Input data file (if not using stdin)
    -sig file                   Input signature file
    -verbose                    Print public key and signature
```

</details>

### `gmssl hsskeygen`

**帮助命令**：`gmssl hsskeygen -help`。**用法**：`usage: gmssl hsskeygen -lms_types types -out file [-pubout file] [-verbose]`

**作用**：生成多层 HSS-LMS-SM3 密钥对。

**帮助中需要先理解的参数**：

- `-verbose`：本机帮助描述：Print public key

<details><summary>展开本机 `-help` 原文</summary>

```text
usage: gmssl hsskeygen -lms_types types -out file [-pubout file] [-verbose]

Options
    -lms_types types            LMS Algorithm Types, start from level 0, seperate by ':'
                                 such as LMS_SM3_M32_H5:LMS_SM3_M32_H10
                                Supported types:
                                 LMS_SM3_M32_H5
                                 LMS_SM3_M32_H10
                                 LMS_SM3_M32_H15
                                 LMS_SM3_M32_H20
                                 LMS_SM3_M32_H25
    -out file                   Output private key
    -pubout file                Output public key
    -verbose                    Print public key
```

</details>

### `gmssl hsssign`

**帮助命令**：`gmssl hsssign -help`。**用法**：`usage: hsssign -key file [-in file] [-out file] [-verbose]`

**作用**：用 HSS-LMS-SM3 私钥签名。

**帮助中需要先理解的参数**：

- `-verbose`：本机帮助描述：Print public key and signature

<details><summary>展开本机 `-help` 原文</summary>

```text
usage: hsssign -key file [-in file] [-out file] [-verbose]

Options
    -key file                   Input private key file
    -in file                    Input data file (if not using stdin)
    -out file                   Output signature file
    -verbose                    Print public key and signature
```

</details>

### `gmssl hssverify`

**帮助命令**：`gmssl hssverify -help`。**用法**：`usage: hssverify -pubkey file [-in file] -sig file [-verbose]`

**作用**：用 HSS-LMS-SM3 公钥验签。

**帮助中需要先理解的参数**：

- `-verbose`：本机帮助描述：Print public key and signature

<details><summary>展开本机 `-help` 原文</summary>

```text
usage: hssverify -pubkey file [-in file] -sig file [-verbose]

Options
    -pubkey file                Input public key file
    -in file                    Input data file (if not using stdin)
    -sig file                   Input signature file
    -verbose                    Print public key and signature
```

</details>

### `gmssl xmsskeygen`

**帮助命令**：`gmssl xmsskeygen -help`。**用法**：`usage: gmssl xmsskeygen -xmss_type type -out file [-pubout file] [-verbose]`

**作用**：生成 XMSS-SM3 哈希签名密钥对。

**帮助中需要先理解的参数**：

- `-verbose`：本机帮助描述：Print public key

<details><summary>展开本机 `-help` 原文</summary>

```text
usage: gmssl xmsskeygen -xmss_type type -out file [-pubout file] [-verbose]

Options
    -xmss_type type             XMSS Algorithm Type
                                 XMSS_SM3_10_256
                                 XMSS_SM3_16_256
                                 XMSS_SM3_20_256
    -out file                   Output private key
    -pubout file                Output public key
    -verbose                    Print public key
```

</details>

### `gmssl xmsssign`

**帮助命令**：`gmssl xmsssign -help`。**用法**：`usage: xmsssign -key file [-in file] [-out file] [-verbose]`

**作用**：用 XMSS-SM3 私钥签名。

**帮助中需要先理解的参数**：

- `-verbose`：本机帮助描述：Print public key and signature

<details><summary>展开本机 `-help` 原文</summary>

```text
usage: xmsssign -key file [-in file] [-out file] [-verbose]

Options
    -key file                   Input private key file
    -in file                    Input data file (if not using stdin)
    -out file                   Output signature file
    -verbose                    Print public key and signature
```

</details>

### `gmssl xmssverify`

**帮助命令**：`gmssl xmssverify -help`。**用法**：`usage: xmssverify -pubkey file [-in file] -sig file [-verbose]`

**作用**：用 XMSS-SM3 公钥验签。

**帮助中需要先理解的参数**：

- `-verbose`：本机帮助描述：Print public key and signature

<details><summary>展开本机 `-help` 原文</summary>

```text
usage: xmssverify -pubkey file [-in file] -sig file [-verbose]

Options
    -pubkey file                Input public key file
    -in file                    Input data file (if not using stdin)
    -sig file                   Input signature file
    -verbose                    Print public key and signature
```

</details>

### `gmssl xmssmtkeygen`

**帮助命令**：`gmssl xmssmtkeygen -help`。**用法**：`usage: gmssl xmssmtkeygen -xmssmt_type type -out file [-pubout file] [-verbose]`

**作用**：生成多树 XMSS^MT-SM3 密钥对。

**帮助中需要先理解的参数**：

- `-verbose`：本机帮助描述：Print public key

<details><summary>展开本机 `-help` 原文</summary>

```text
usage: gmssl xmssmtkeygen -xmssmt_type type -out file [-pubout file] [-verbose]

Options
    -xmssmt_type type           XMSSMT Algorithm Type
                                 XMSSMT_SM3_20_2_256
                                 XMSSMT_SM3_20_4_256
                                 XMSSMT_SM3_40_2_256
                                 XMSSMT_SM3_40_4_256
                                 XMSSMT_SM3_40_8_256
                                 XMSSMT_SM3_60_3_256
                                 XMSSMT_SM3_60_6_256
                                 XMSSMT_SM3_60_12_256
    -out file                   Output private key
    -pubout file                Output public key
    -verbose                    Print public key
```

</details>

### `gmssl xmssmtsign`

**帮助命令**：`gmssl xmssmtsign -help`。**用法**：`usage: xmssmtsign -key file [-in file] [-out file] [-verbose]`

**作用**：用 XMSS^MT-SM3 私钥签名。

**帮助中需要先理解的参数**：

- `-verbose`：本机帮助描述：Print public key and signature

<details><summary>展开本机 `-help` 原文</summary>

```text
usage: xmssmtsign -key file [-in file] [-out file] [-verbose]

Options
    -key file                   Input private key file
    -in file                    Input data file (if not using stdin)
    -out file                   Output signature file
    -verbose                    Print public key and signature
```

</details>

### `gmssl xmssmtverify`

**帮助命令**：`gmssl xmssmtverify -help`。**用法**：`usage: xmssmtverify -pubkey file [-in file] -sig file [-verbose]`

**作用**：用 XMSS^MT-SM3 公钥验签。

**帮助中需要先理解的参数**：

- `-verbose`：本机帮助描述：Print public key and signature

<details><summary>展开本机 `-help` 原文</summary>

```text
usage: xmssmtverify -pubkey file [-in file] -sig file [-verbose]

Options
    -pubkey file                Input public key file
    -in file                    Input data file (if not using stdin)
    -sig file                   Input signature file
    -verbose                    Print public key and signature
```

</details>

### `gmssl sphincskeygen`

**帮助命令**：`gmssl sphincskeygen -help`。**用法**：`usage: gmssl sphincskeygen -out file [-pubout file] [-verbose]`

**作用**：生成 SPHINCS+_128s-SM3 密钥对。

**帮助中需要先理解的参数**：

- `-verbose`：本机帮助描述：Print public key

<details><summary>展开本机 `-help` 原文</summary>

```text
usage: gmssl sphincskeygen -out file [-pubout file] [-verbose]

Options
    -out file                   Output private key
    -pubout file                Output public key
    -verbose                    Print public key
```

</details>

### `gmssl sphincssign`

**帮助命令**：`gmssl sphincssign -help`。**用法**：`usage: sphincssign -key file [-in file] [-out file] [-verbose]`

**作用**：用 SPHINCS+_128s-SM3 私钥签名。

**帮助中需要先理解的参数**：

- `-verbose`：本机帮助描述：Print public key and signature

<details><summary>展开本机 `-help` 原文</summary>

```text
usage: sphincssign -key file [-in file] [-out file] [-verbose]

Options
    -key file                   Input private key file
    -in file                    Input data file (if not using stdin)
    -out file                   Output signature file
    -verbose                    Print public key and signature
```

</details>

### `gmssl sphincsverify`

**帮助命令**：`gmssl sphincsverify -help`。**用法**：`usage: sphincsverify -pubkey file [-in file] -sig file [-verbose]`

**作用**：用 SPHINCS+_128s-SM3 公钥验签。

**帮助中需要先理解的参数**：

- `-verbose`：本机帮助描述：Print public key and signature

<details><summary>展开本机 `-help` 原文</summary>

```text
usage: sphincsverify -pubkey file [-in file] -sig file [-verbose]

Options
    -pubkey file                Input public key file
    -in file                    Input data file (if not using stdin)
    -sig file                   Input signature file
    -verbose                    Print public key and signature
```

</details>

### `gmssl kyberkeygen`

**帮助命令**：`gmssl kyberkeygen -help`。**用法**：`usage: gmssl kyberkeygen -out file [-pubout file] [-verbose]`

**作用**：生成 Kyber KEM 公私钥对。

**帮助中需要先理解的参数**：

- `-verbose`：本机帮助描述：Print public key

<details><summary>展开本机 `-help` 原文</summary>

```text
usage: gmssl kyberkeygen -out file [-pubout file] [-verbose]

Options
    -out file                   Output private key
    -pubout file                Output public key
    -verbose                    Print public key
```

</details>

### `gmssl kyberencap`

**帮助命令**：`gmssl kyberencap -help`。**用法**：`usage: kyberencap -pubkey file [-out file] -outkey file [-verbose]`

**作用**：用 Kyber 公钥封装共享秘密并输出 KEM 密文。

**参数解读**：KEM 产生密文和共享秘密，不直接对文件明文加密。

**帮助中需要先理解的参数**：

- `-verbose`：本机帮助描述：Print public key and ciphertext

<details><summary>展开本机 `-help` 原文</summary>

```text
usage: kyberencap -pubkey file [-out file] -outkey file [-verbose]

Options
    -pubkey file                Input public key file
    -out file                   Output ciphertext (decapsulated secret)
    -outkey file                Output secret
    -verbose                    Print public key and ciphertext
```

</details>

### `gmssl kyberdecap`

**帮助命令**：`gmssl kyberdecap -help`。**用法**：`usage: kyberdecap -key file [-in file] [-out file] [-verbose]`

**作用**：用 Kyber 私钥解封装共享秘密。

**参数解读**：用 KEM 私钥从密文恢复共享秘密；需与封装结果比较。

**帮助中需要先理解的参数**：

- `-verbose`：本机帮助描述：Print public key and ciphertext

<details><summary>展开本机 `-help` 原文</summary>

```text
usage: kyberdecap -key file [-in file] [-out file] [-verbose]

Options
    -key file                   Input private key file
    -in file                    Input ciphertext (encapsulated secret)
    -out file                   Output decapsulated secret
    -verbose                    Print public key and ciphertext
```

</details>

## SDF 与 SKF 设备接口

### `gmssl sdfinfo`

**帮助命令**：`gmssl sdfinfo -help`。**用法**：`usage: gmssl sdfinfo -lib so_path`

**作用**：读取 SDF 设备信息。

**帮助给出的命令示例（未作为本项目验收）**：

```bash
gmssl sdfinfo
```

**运行条件**：必须有授权的设备、厂商动态库和测试密钥；这里只验证帮助信息。

<details><summary>展开本机 `-help` 原文</summary>

```text
usage: gmssl sdfinfo -lib so_path

Options

    -lib so_path        Vendor's SDF dynamic library

Examples

    gmssl sdfinfo
```

</details>

### `gmssl sdfdigest`

**帮助命令**：`gmssl sdfdigest -help`。**用法**：`usage: gmssl sdfdigest -lib so_path [-hex|-bin] [-pubkey pem [-id str]] [-in file|-in_str str] [-out file]`

**作用**：调用 SDF 设备计算 SM3 摘要。

**帮助中需要先理解的参数**：

- `-hex`：本机帮助描述：Output hash value as hex string (by default)
- `-bin`：本机帮助描述：Output hash value as binary

**帮助给出的命令示例（未作为本项目验收）**：

```bash
gmssl sdfdigest -in_str abc
```

**运行条件**：必须有授权的设备、厂商动态库和测试密钥；这里只验证帮助信息。

<details><summary>展开本机 `-help` 原文</summary>

```text
usage: gmssl sdfdigest -lib so_path [-hex|-bin] [-pubkey pem [-id str]] [-in file|-in_str str] [-out file]
Options

    -lib so_path           Vendor's SDF dynamic library
    -hex                   Output hash value as hex string (by default)
    -bin                   Output hash value as binary
    -pubkey pem            Signer's SM2 public key
                           When `-pubkey` is specified, hash with SM2 Z value
    -id str                SM2 Signer's ID string
    -id_hex hex            SM2 Signer's ID in hex format
                           `-id` and `-id_hex` should be used with `-pubkey`
                           `-id` and `-id_hex` should not be used together
                           If `-pubkey` is specified without `-id` or `id_hex`,
                           the default ID string '1234567812345678' is used
    -in_str str            To be hashed string
    -in file | stdin       To be hashed file path
                           `-in_str` and `-in` should not be used together
                           If neither `-in` nor `-in_str` specified, read from stdin
    -out file | stdout     Output file path. If not specified, output to stdout

Examples

    gmssl sdfdigest -in_str abc

    gmssl sdfdigest -in_str abc -bin

    gmssl sdfdigest -in /path/to/file

    gmssl sdfdigest -pubkey sm2pubkey.pem -id alice -in /path/to/file -bin

    When reading from stdin, make sure the trailing newline character is removed

    Linux/Mac:
    echo -n abc | gmssl sdfdigest

    Windows:
    echo |set/p="abc" | gmssl sdfdigest
```

</details>

### `gmssl sdfexport`

**帮助命令**：`gmssl sdfexport -help`。**用法**：`usage: gmssl sdfexport -lib so_path {-sign|-encrypt} -key num [-out file]`

**作用**：从 SDF 设备导出指定槽位的 SM2 公钥。

**帮助中需要先理解的参数**：

- `-encrypt`：选择加密动作；本机帮助描述：Export encryption public key
- `-sign`：选择签名动作或私钥；本机帮助描述：Export signing public key

**帮助给出的命令示例（未作为本项目验收）**：

```bash
gmssl sdfexport -sign -key 1 -out sm2signpub.pem
```

**运行条件**：必须有授权的设备、厂商动态库和测试密钥；这里只验证帮助信息。

<details><summary>展开本机 `-help` 原文</summary>

```text
usage: gmssl sdfexport -lib so_path {-sign|-encrypt} -key num [-out file]

Options

    -lib so_path         Vendor's SDF dynamic library
    -sign                Export signing public key
    -encrypt             Export encryption public key
    -key num             Private key index number
    -out file | stdout   Output public key in PEM format

Examples

    gmssl sdfexport -sign -key 1 -out sm2signpub.pem
    gmssl sdfexport -encrypt -key 1 -out sm2signpub.pem
```

</details>

### `gmssl sdfsign`

**帮助命令**：`gmssl sdfsign -help`。**用法**：`usage: gmssl sdfsign -lib so_path -key num [-pass str] [-id str] [-in file] [-out file]`

**作用**：用 SDF 设备内私钥生成 SM2 签名。

**帮助给出的命令示例（未作为本项目验收）**：

```bash
echo -n 'message to be signed' | gmssl sdfsign -lib libsoftsdf.so -key 1 -pass P@ssw0rd -out sm2.sig
```

**运行条件**：必须有授权的设备、厂商动态库和测试密钥；这里只验证帮助信息。

<details><summary>展开本机 `-help` 原文</summary>

```text
usage: gmssl sdfsign -lib so_path -key num [-pass str] [-id str] [-in file] [-out file]

Options

    -lib so_path        Vendor's SDF dynamic library
    -key num            Signing private key index number
    -pass str           Password to get the private key access right, prompt if not given
    -id str             Signer's identity string, '1234567812345678' by default
    -in file | stdin    To be signed file or data
    -out file | stdout  Output signature in binary DER encoding

Examples

    echo -n 'message to be signed' | gmssl sdfsign -lib libsoftsdf.so -key 1 -pass P@ssw0rd -out sm2.sig
    gmssl sdfexport -lib libsoftsdf.so -sign -key 1 -out sm2pub.pem
    echo -n 'message to be signed' | gmssl sm2verify -pubkey sm2pub.pem -sig sm2.sig
```

</details>

### `gmssl sdfencrypt`

**帮助命令**：`gmssl sdfencrypt -help`。**用法**：`usage: gmssl sdfencrypt -lib so_path (-pubkey pem | -cert pem) [-in file] [-out file]`

**作用**：调用 SDF 设备完成 SM2/SM4-CBC 混合加密。

**帮助给出的命令示例（未作为本项目验收）**：

```bash
echo 'Secret message' | gmssl sdfencrypt -lib libsoftsdf.so -pubkey sm2encpub.pem -out sdf_ciphertext.bin
```

**运行条件**：必须有授权的设备、厂商动态库和测试密钥；这里只验证帮助信息。

<details><summary>展开本机 `-help` 原文</summary>

```text
usage: gmssl sdfencrypt -lib so_path (-pubkey pem | -cert pem) [-in file] [-out file]

Options

    -lib so_path        Vendor's SDF dynamic library
    -pubkey pem         Recepient's public key file in PEM format
    -cert pem           Recipient's certificate in PEM format
    -in file | stdin    Input data
    -out file | stdout  Output data

Examples

    gmssl sdfexport -encrypt -key 1 -lib libsoftsdf.so -out sm2encpub.pem
    echo 'Secret message' | gmssl sdfencrypt -lib libsoftsdf.so -pubkey sm2encpub.pem -out sdf_ciphertext.bin
    gmssl sdfdecrypt -lib libsoftsdf.so -key 1 -pass P@ssw0rd -in sdf_ciphertext.bin
```

</details>

### `gmssl sdfdecrypt`

**帮助命令**：`gmssl sdfdecrypt -help`。**用法**：`usage: gmssl sdfdecrypt -lib so_path -key num [-pass str] [-in file] [-out file]`

**作用**：调用 SDF 设备完成 SM2/SM4-CBC 混合解密。

**帮助给出的命令示例（未作为本项目验收）**：

```bash
gmssl sdfdecrypt -lib libsoftsdf.so -key 1 -pass P@ssw0rd -in sdf_ciphertext.bin
```

**运行条件**：必须有授权的设备、厂商动态库和测试密钥；这里只验证帮助信息。

<details><summary>展开本机 `-help` 原文</summary>

```text
usage: gmssl sdfdecrypt -lib so_path -key num [-pass str] [-in file] [-out file]

Options

    -lib so_path        Vendor's SDF dynamic library
    -key num            Decryption private key index number
    -pass str           Password to get the private key access right, prompt if not given
    -in file | stdin    Input data
    -out file | stdout  Output data

Examples

    gmssl sdfexport -encrypt -key 1 -lib libsoftsdf.so -out sm2encpub.pem
    echo 'Secret message' | gmssl sdfencrypt -lib libsoftsdf.so -pubkey sm2encpub.pem -out sdf_ciphertext.bin
    gmssl sdfdecrypt -lib libsoftsdf.so -key 1 -pass P@ssw0rd -in sdf_ciphertext.bin
```

</details>

### `gmssl sdftest`

**帮助命令**：`gmssl sdftest -help`。**用法**：`usage: gmssl sdftest -lib so_path -kek num -key num [-pass str]`

**作用**：按设备、KEK 和密钥槽位运行 SDF 测试。

**帮助给出的命令示例（未作为本项目验收）**：

```bash
gmssl sdftest -lib soft_sdf.so -kek 1 -key 1 -pass P@ssw0rd
```

**运行条件**：必须有授权的设备、厂商动态库和测试密钥；这里只验证帮助信息。

<details><summary>展开本机 `-help` 原文</summary>

```text
usage: gmssl sdftest -lib so_path -kek num -key num [-pass str]

Options

    -lib so_path        Path to vendor's SDF dynamic lib (.so or .dylib)
    -kek num            KEK index
    -key num            Private key index
    -pass str           Password for accessing the private key, prompt if not given

Examples

    gmssl sdftest -lib soft_sdf.so -kek 1 -key 1 -pass P@ssw0rd
```

</details>

### `gmssl skfutil`

**帮助命令**：`gmssl skfutil -help`。**用法**：`usage: skfutil -lib so_path -dev str -devinfo`

**作用**：对 SKF 设备的应用、容器、公钥、签名及随机数进行操作。

**参数解读**：帮助列出多个设备/应用/容器子模式，必须有 SKF 设备与厂商库。

**运行条件**：必须有授权的设备、厂商动态库和测试密钥；这里只验证帮助信息。

<details><summary>展开本机 `-help` 原文</summary>

```text
usage:
  skfutil -lib so_path -dev str -devinfo
  skfutil -lib so_path -dev str -app str [-pass str] -container str -exportpubkey [-out file]
  skfutil -lib so_path -dev str -app str [-pass str] -container str -sign [-in file] [-out file]
  skfutil -lib so_path -dev str -rand num [-out file]
```

</details>

## TLCP、TLS 与 QUIC 网络工具

### `gmssl tlcp_client`

**帮助命令**：`gmssl tlcp_client -help`。**用法**：`usage: gmssl tlcp_client -host str [-port num] [-cacert pem] [-cert pem -key pem [-pass str]] [-certout pem] [-get path|-in file] [-alpn str] [-trusted_ca_keys] [-verbose]`

**作用**：连接并诊断 TLCP 服务端。

**帮助中需要先理解的参数**：

- `-client_cert_optional`：本机帮助描述：Allow client send empty Certificate
- `-trusted_ca_keys`：本机帮助描述：Send trusted_ca_keys request
- `-status_request`：本机帮助描述：Send status_request (OCSP Stapling) request
- `-verbose`：本机帮助描述：Print TLS handshake messages

**帮助给出的命令示例（未作为本项目验收）**：

```bash
gmssl tlcp_client -host 127.0.0.1 -port 4431 -server_name localhost -cacert sm2_root_ca_cert.pem \
-cipher_suite TLS_ECC_SM4_CBC_SM3 -in message.txt
```

**运行条件**：需要受控网络端点、可信证书或测试服务；这里只验证帮助信息。

<details><summary>展开本机 `-help` 原文</summary>

```text
usage: gmssl tlcp_client -host str [-port num] [-cacert pem] [-cert pem -key pem [-pass str]] [-certout pem] [-get path|-in file] [-alpn str] [-trusted_ca_keys] [-verbose]

Options

    -host str              Domain name or IP address of remote host
    -port num              Port number of remote host, default 443
    -cipher_suite str      Supported cipher suites, may appear multiple times, higher priority first
    -supported_group str   Supported elliptic curves, may appear multiple times, higher priority first
    -sig_alg str           Supported signature algorithms
    -cacert pem            Trusted CA certificate(s) in PEM format
    -verify_depth num      Certificate verification depth
    -cert pem              Client certificate(s) in PEM format, TLCP ECDHE requires a double certificate chain
    -key pem               Private key of client certificate in PEM format, TLCP ECDHE requires signing and encryption keys
    -pass password         Password of encrypted private key, prompt if not given
    -client_cert_optional  Allow client send empty Certificate
    -get path              Send a GET request with given path of URI
    -in file | stdin       Send input data and read response until close or timeout
    -certout pem           Save server certificates to a PEM file
    -server_name str       Send server_name (SNI) request
    -trusted_ca_keys       Send trusted_ca_keys request
    -alpn str              Application protocol name, may appear multiple times, higher priority first
    -status_request        Send status_request (OCSP Stapling) request
    -verbose               Print TLS handshake messages


Supported cipher suites:
    TLS_ECC_SM4_CBC_SM3
    TLS_ECC_SM4_GCM_SM3
    TLS_ECDHE_SM4_CBC_SM3
    TLS_ECDHE_SM4_GCM_SM3


Examples

    gmssl sm2keygen -pass P@ssw0rd -out sm2_root_ca_key.pem
    gmssl certgen -C CN -ST Beijing -L Haidian -O GmSSL -OU Test -CN "GmSSL SM2 Test Root CA" \
        -days 3650 -key sm2_root_ca_key.pem -pass P@ssw0rd -out sm2_root_ca_cert.pem \
        -key_usage keyCertSign -key_usage cRLSign -ca

    gmssl sm2keygen -pass P@ssw0rd -out sm2_tlcp_ca_key.pem
    gmssl reqgen -C CN -ST Beijing -L Haidian -O GmSSL -OU Test -CN "GmSSL SM2 TLCP CA" \
        -key sm2_tlcp_ca_key.pem -pass P@ssw0rd -out sm2_tlcp_ca_req.pem
    gmssl reqsign -in sm2_tlcp_ca_req.pem -days 1825 -key_usage keyCertSign \
        -key_usage cRLSign -path_len_constraint 0 -cacert sm2_root_ca_cert.pem \
        -key sm2_root_ca_key.pem -pass P@ssw0rd -out sm2_tlcp_ca_cert.pem -ca

    gmssl sm2keygen -pass P@ssw0rd -out sm2_tlcp_server_sign_key.pem
    gmssl reqgen -C CN -ST Beijing -L Haidian -O GmSSL -OU Test -CN "GmSSL SM2 TLCP Server" \
        -key sm2_tlcp_server_sign_key.pem -pass P@ssw0rd -out sm2_tlcp_server_sign_req.pem
    gmssl reqsign -in sm2_tlcp_server_sign_req.pem -days 365 -key_usage digitalSignature \
        -ext_key_usage serverAuth -subject_dns_name localhost -cacert sm2_tlcp_ca_cert.pem \
        -key sm2_tlcp_ca_key.pem -pass P@ssw0rd -out sm2_tlcp_server_sign_cert.pem
    gmssl sm2keygen -pass P@ssw0rd -out sm2_tlcp_server_enc_key.pem
    gmssl reqgen -C CN -ST Beijing -L Haidian -O GmSSL -OU Test -CN "GmSSL SM2 TLCP Server" \
        -key sm2_tlcp_server_enc_key.pem -pass P@ssw0rd -out sm2_tlcp_server_enc_req.pem
    gmssl reqsign -in sm2_tlcp_server_enc_req.pem -days 365 -key_usage keyEncipherment \
        -ext_key_usage serverAuth -subject_dns_name localhost -cacert sm2_tlcp_ca_cert.pem \
        -key sm2_tlcp_ca_key.pem -pass P@ssw0rd -out sm2_tlcp_server_enc_cert.pem

    cat sm2_tlcp_server_sign_cert.pem > sm2_tlcp_server_certs.pem
    cat sm2_tlcp_server_enc_cert.pem >> sm2_tlcp_server_certs.pem
    cat sm2_tlcp_ca_cert.pem >> sm2_tlcp_server_certs.pem
    cat sm2_tlcp_server_sign_key.pem > sm2_tlcp_server_keys.pem
    cat sm2_tlcp_server_enc_key.pem >> sm2_tlcp_server_keys.pem

    gmssl sm2keygen -pass P@ssw0rd -out sm2_tls_client_key.pem
    gmssl reqgen -C CN -ST Beijing -L Haidian -O GmSSL -OU Test -CN "GmSSL SM2 TLS Client" \
        -key sm2_tls_client_key.pem -pass P@ssw0rd -out sm2_tls_client_req.pem
    gmssl reqsign -in sm2_tls_client_req.pem -days 365 -key_usage digitalSignature \
        -ext_key_usage clientAuth -cacert sm2_tlcp_ca_cert.pem -key sm2_tlcp_ca_key.pem \
        -pass P@ssw0rd -out sm2_tls_client_cert.pem
    cat sm2_tls_client_cert.pem > sm2_tls_client_certs.pem
    cat sm2_tlcp_ca_cert.pem >> sm2_tls_client_certs.pem

    printf 'hello tlcp\n' > message.txt

    gmssl tlcp_server -port 4431 -cert sm2_tlcp_server_certs.pem -key sm2_tlcp_server_keys.pem -pass P@ssw0rd \
        -cipher_suite TLS_ECC_SM4_CBC_SM3
    gmssl tlcp_client -host 127.0.0.1 -port 4431 -server_name localhost -cacert sm2_root_ca_cert.pem \
        -cipher_suite TLS_ECC_SM4_CBC_SM3 -in message.txt

    gmssl tlcp_server -port 4436 -cert sm2_tlcp_server_certs.pem -key sm2_tlcp_server_keys.pem -pass P@ssw0rd \
        -cipher_suite TLS_ECC_SM4_GCM_SM3 -cacert sm2_root_ca_cert.pem -cert_request
    gmssl tlcp_client -host 127.0.0.1 -port 4436 -server_name localhost -cacert sm2_root_ca_cert.pem \
        -cipher_suite TLS_ECC_SM4_GCM_SM3 \
        -cert sm2_tls_client_certs.pem -key sm2_tls_client_key.pem -pass P@ssw0rd \
        -in message.txt
```

</details>

### `gmssl tlcp_server`

**帮助命令**：`gmssl tlcp_server -help`。**用法**：`usage: tlcp_server [-port num] -cert pem -key pem [-pass str] [-cipher_suite str] [-alpn str] [-cert_request] [-cacert pem] [-www] [-verbose]`

**作用**：启动使用证书和私钥的 TLCP 测试服务端。

**帮助中需要先理解的参数**：

- `-cert_request`：本机帮助描述：Client certificate request
- `-www`：本机帮助描述：Return HTTP 200 OK and echo client request data as text
- `-verbose`：本机帮助描述：Print TLS handshake messages

**帮助给出的命令示例（未作为本项目验收）**：

```bash
gmssl tlcp_server -port 4431 -cert sm2_tlcp_server_certs.pem -key sm2_tlcp_server_keys.pem -pass P@ssw0rd \
-cipher_suite TLS_ECC_SM4_CBC_SM3
```

**运行条件**：需要受控网络端点、可信证书或测试服务；这里只验证帮助信息。

<details><summary>展开本机 `-help` 原文</summary>

```text
usage: tlcp_server [-port num] -cert pem -key pem [-pass str] [-cipher_suite str] [-alpn str] [-cert_request] [-cacert pem] [-www] [-verbose]
Options

    -port num              Listening port number, default 443
    -cert pem              Server's certificate chain in PEM format, may appear multiple times
    -key pem               Server's signing and encryption private keys in PEM format: signing key first, encryption key second, may appear multiple times
    -pass str              Password to decrypt both private keys in the same -key PEM, may appear multiple times, prompt if not given
    -cipher_suite str      Supported cipher suites, may appear multiple times, higher priority first
    -alpn str              Application protocol name, may appear multiple times, higher priority first
    -cert_request          Client certificate request
    -cacert pem            CA certificate for client certificate verification
    -www                   Return HTTP 200 OK and echo client request data as text
    -verbose               Print TLS handshake messages


Supported cipher suites:
    TLS_ECC_SM4_CBC_SM3
    TLS_ECC_SM4_GCM_SM3
    TLS_ECDHE_SM4_CBC_SM3
    TLS_ECDHE_SM4_GCM_SM3


Examples

    gmssl sm2keygen -pass P@ssw0rd -out sm2_root_ca_key.pem
    gmssl certgen -C CN -ST Beijing -L Haidian -O GmSSL -OU Test -CN "GmSSL SM2 Test Root CA" \
        -days 3650 -key sm2_root_ca_key.pem -pass P@ssw0rd -out sm2_root_ca_cert.pem \
        -key_usage keyCertSign -key_usage cRLSign -ca

    gmssl sm2keygen -pass P@ssw0rd -out sm2_tlcp_ca_key.pem
    gmssl reqgen -C CN -ST Beijing -L Haidian -O GmSSL -OU Test -CN "GmSSL SM2 TLCP CA" \
        -key sm2_tlcp_ca_key.pem -pass P@ssw0rd -out sm2_tlcp_ca_req.pem
    gmssl reqsign -in sm2_tlcp_ca_req.pem -days 1825 -key_usage keyCertSign \
        -key_usage cRLSign -path_len_constraint 0 -cacert sm2_root_ca_cert.pem \
        -key sm2_root_ca_key.pem -pass P@ssw0rd -out sm2_tlcp_ca_cert.pem -ca

    gmssl sm2keygen -pass P@ssw0rd -out sm2_tlcp_server_sign_key.pem
    gmssl reqgen -C CN -ST Beijing -L Haidian -O GmSSL -OU Test -CN "GmSSL SM2 TLCP Server" \
        -key sm2_tlcp_server_sign_key.pem -pass P@ssw0rd -out sm2_tlcp_server_sign_req.pem
    gmssl reqsign -in sm2_tlcp_server_sign_req.pem -days 365 -key_usage digitalSignature \
        -ext_key_usage serverAuth -subject_dns_name localhost -cacert sm2_tlcp_ca_cert.pem \
        -key sm2_tlcp_ca_key.pem -pass P@ssw0rd -out sm2_tlcp_server_sign_cert.pem
    gmssl sm2keygen -pass P@ssw0rd -out sm2_tlcp_server_enc_key.pem
    gmssl reqgen -C CN -ST Beijing -L Haidian -O GmSSL -OU Test -CN "GmSSL SM2 TLCP Server" \
        -key sm2_tlcp_server_enc_key.pem -pass P@ssw0rd -out sm2_tlcp_server_enc_req.pem
    gmssl reqsign -in sm2_tlcp_server_enc_req.pem -days 365 -key_usage keyEncipherment \
        -ext_key_usage serverAuth -subject_dns_name localhost -cacert sm2_tlcp_ca_cert.pem \
        -key sm2_tlcp_ca_key.pem -pass P@ssw0rd -out sm2_tlcp_server_enc_cert.pem

    cat sm2_tlcp_server_sign_cert.pem > sm2_tlcp_server_certs.pem
    cat sm2_tlcp_server_enc_cert.pem >> sm2_tlcp_server_certs.pem
    cat sm2_tlcp_ca_cert.pem >> sm2_tlcp_server_certs.pem
    cat sm2_tlcp_server_sign_key.pem > sm2_tlcp_server_keys.pem
    cat sm2_tlcp_server_enc_key.pem >> sm2_tlcp_server_keys.pem

    gmssl sm2keygen -pass P@ssw0rd -out sm2_tls_client_key.pem
    gmssl reqgen -C CN -ST Beijing -L Haidian -O GmSSL -OU Test -CN "GmSSL SM2 TLS Client" \
        -key sm2_tls_client_key.pem -pass P@ssw0rd -out sm2_tls_client_req.pem
    gmssl reqsign -in sm2_tls_client_req.pem -days 365 -key_usage digitalSignature \
        -ext_key_usage clientAuth -cacert sm2_tlcp_ca_cert.pem -key sm2_tlcp_ca_key.pem \
        -pass P@ssw0rd -out sm2_tls_client_cert.pem
    cat sm2_tls_client_cert.pem > sm2_tls_client_certs.pem
    cat sm2_tlcp_ca_cert.pem >> sm2_tls_client_certs.pem

    printf 'hello tlcp\n' > message.txt

    gmssl tlcp_server -port 4431 -cert sm2_tlcp_server_certs.pem -key sm2_tlcp_server_keys.pem -pass P@ssw0rd \
        -cipher_suite TLS_ECC_SM4_CBC_SM3
    gmssl tlcp_client -host 127.0.0.1 -port 4431 -server_name localhost -cacert sm2_root_ca_cert.pem \
        -cipher_suite TLS_ECC_SM4_CBC_SM3 -in message.txt

    gmssl tlcp_server -port 4436 -cert sm2_tlcp_server_certs.pem -key sm2_tlcp_server_keys.pem -pass P@ssw0rd \
        -cipher_suite TLS_ECC_SM4_GCM_SM3 -cacert sm2_root_ca_cert.pem -cert_request
    gmssl tlcp_client -host 127.0.0.1 -port 4436 -server_name localhost -cacert sm2_root_ca_cert.pem \
        -cipher_suite TLS_ECC_SM4_GCM_SM3 \
        -cert sm2_tls_client_certs.pem -key sm2_tls_client_key.pem -pass P@ssw0rd \
        -in message.txt
```

</details>

### `gmssl tls12_client`

**帮助命令**：`gmssl tls12_client -help`。**用法**：`usage: tls12_client -host str [-port num] [-cacert pem] [-cert pem -key pem [-pass str]] [-get path|-in file] [-trusted_ca_keys] [-verbose]`

**作用**：连接并诊断 TLS 1.2 服务端。

**帮助中需要先理解的参数**：

- `-client_cert_optional`：本机帮助描述：Allow client send empty Certificate
- `-trusted_ca_keys`：本机帮助描述：Send trusted_ca_keys request
- `-renegotiation_info`：本机帮助描述：Send renegotiation_info extension
- `-renegotiation_info_scsv`：本机帮助描述：Send TLS_EMPTY_RENEGOTIATION_INFO_SCSV
- `-status_request`：本机帮助描述：Send status_request (OCSP Stapling) request
- `-verbose`：本机帮助描述：Print TLS handshake messages

**帮助给出的命令示例（未作为本项目验收）**：

```bash
gmssl tls12_client -host 127.0.0.1 -port 4432 -server_name localhost -cacert sm2_root_ca_cert.pem \
-cipher_suite TLS_ECDHE_SM4_CBC_SM3 -supported_group sm2p256v1 -sig_alg sm2sig_sm3 \
-in message.txt
```

**运行条件**：需要受控网络端点、可信证书或测试服务；这里只验证帮助信息。

<details><summary>展开本机 `-help` 原文</summary>

```text
usage: tls12_client -host str [-port num] [-cacert pem] [-cert pem -key pem [-pass str]] [-get path|-in file] [-trusted_ca_keys] [-verbose]
Options

    -host str              Server's hostname
    -port num              Server's port number, default 443
    -cipher_suite str      Supported cipher suites, may appear multiple times, higher priority first
    -supported_group str   Supported elliptic curves, may appear multiple times, higher priority first
    -sig_alg str           Supported signature algorithms
    -cacert pem            Root CA certificate in PEM format
    -verify_depth num      Certificate verification depth
    -cert pem              Client's certificate chain in PEM format
    -key pem               Client's encrypted private key in PEM format
    -pass str              Password to decrypt private key, prompt if not given
    -client_cert_optional  Allow client send empty Certificate
    -server_name str       Send server_name (SNI) request
    -trusted_ca_keys       Send trusted_ca_keys request
    -renegotiation_info    Send renegotiation_info extension
    -renegotiation_info_scsv  Send TLS_EMPTY_RENEGOTIATION_INFO_SCSV
    -status_request        Send status_request (OCSP Stapling) request
    -get path              Send a HTTP GET request and read response until close or timeout
    -in file | stdin       Send input data and read response until close or timeout
    -verbose               Print TLS handshake messages


Supported cipher suites:
    TLS_ECDHE_SM4_CBC_SM3
    TLS_ECDHE_SM4_GCM_SM3
    TLS_ECDHE_ECDSA_WITH_AES_128_CBC_SHA256
    TLS_ECDHE_ECDSA_WITH_AES_128_GCM_SHA256
    TLS_ECDHE_ECDSA_WITH_AES_128_CCM


Examples

    gmssl sm2keygen -pass P@ssw0rd -out sm2_root_ca_key.pem
    gmssl certgen -C CN -ST Beijing -L Haidian -O GmSSL -OU Test -CN "GmSSL SM2 Test Root CA" \
        -days 3650 -key sm2_root_ca_key.pem -pass P@ssw0rd -out sm2_root_ca_cert.pem \
        -key_usage keyCertSign -key_usage cRLSign -ca

    gmssl sm2keygen -pass P@ssw0rd -out sm2_tls_ca_key.pem
    gmssl reqgen -C CN -ST Beijing -L Haidian -O GmSSL -OU Test -CN "GmSSL SM2 TLS CA" \
        -key sm2_tls_ca_key.pem -pass P@ssw0rd -out sm2_tls_ca_req.pem
    gmssl reqsign -in sm2_tls_ca_req.pem -days 1825 -key_usage keyCertSign \
        -key_usage cRLSign -path_len_constraint 0 -cacert sm2_root_ca_cert.pem \
        -key sm2_root_ca_key.pem -pass P@ssw0rd -out sm2_tls_ca_cert.pem -ca

    gmssl sm2keygen -pass P@ssw0rd -out sm2_tls_server_key.pem
    gmssl reqgen -C CN -ST Beijing -L Haidian -O GmSSL -OU Test -CN "GmSSL SM2 TLS Server" \
        -key sm2_tls_server_key.pem -pass P@ssw0rd -out sm2_tls_server_req.pem
    gmssl reqsign -in sm2_tls_server_req.pem -days 365 -key_usage digitalSignature \
        -ext_key_usage serverAuth -subject_dns_name localhost -cacert sm2_tls_ca_cert.pem \
        -key sm2_tls_ca_key.pem -pass P@ssw0rd -out sm2_tls_server_cert.pem
    cat sm2_tls_server_cert.pem > sm2_tls_server_certs.pem
    cat sm2_tls_ca_cert.pem >> sm2_tls_server_certs.pem

    gmssl sm2keygen -pass P@ssw0rd -out sm2_tls_client_key.pem
    gmssl reqgen -C CN -ST Beijing -L Haidian -O GmSSL -OU Test -CN "GmSSL SM2 TLS Client" \
        -key sm2_tls_client_key.pem -pass P@ssw0rd -out sm2_tls_client_req.pem
    gmssl reqsign -in sm2_tls_client_req.pem -days 365 -key_usage digitalSignature \
        -ext_key_usage clientAuth -cacert sm2_tls_ca_cert.pem -key sm2_tls_ca_key.pem \
        -pass P@ssw0rd -out sm2_tls_client_cert.pem
    cat sm2_tls_client_cert.pem > sm2_tls_client_certs.pem
    cat sm2_tls_ca_cert.pem >> sm2_tls_client_certs.pem

    printf 'hello tls12\n' > message.txt

    gmssl tls12_server -port 4432 -cert sm2_tls_server_certs.pem -key sm2_tls_server_key.pem -pass P@ssw0rd \
        -cipher_suite TLS_ECDHE_SM4_CBC_SM3 -supported_group sm2p256v1 -sig_alg sm2sig_sm3
    gmssl tls12_client -host 127.0.0.1 -port 4432 -server_name localhost -cacert sm2_root_ca_cert.pem \
        -cipher_suite TLS_ECDHE_SM4_CBC_SM3 -supported_group sm2p256v1 -sig_alg sm2sig_sm3 \
        -in message.txt

    gmssl tls12_server -port 4438 -cert sm2_tls_server_certs.pem -key sm2_tls_server_key.pem -pass P@ssw0rd \
        -cipher_suite TLS_ECDHE_SM4_GCM_SM3 -supported_group sm2p256v1 -sig_alg sm2sig_sm3 \
        -cacert sm2_root_ca_cert.pem -cert_request
    gmssl tls12_client -host 127.0.0.1 -port 4438 -server_name localhost -cacert sm2_root_ca_cert.pem \
        -cipher_suite TLS_ECDHE_SM4_GCM_SM3 -supported_group sm2p256v1 -sig_alg sm2sig_sm3 \
        -cert sm2_tls_client_certs.pem -key sm2_tls_client_key.pem -pass P@ssw0rd \
        -in message.txt
```

</details>

### `gmssl tls12_server`

**帮助命令**：`gmssl tls12_server -help`。**用法**：`usage: tls12_server [-port num] -cert pem -key pem [-pass str] [-cacert pem] [-www] [-verbose]`

**作用**：启动 TLS 1.2 测试服务端。

**帮助中需要先理解的参数**：

- `-cert_request`：本机帮助描述：Client certificate request
- `-client_cert_optional`：本机帮助描述：Allow client send empty Certificate
- `-renegotiation_info`：本机帮助描述：Enable RFC 5746 renegotiation_info response
- `-www`：本机帮助描述：Return HTTP 200 OK and echo client request data as text
- `-verbose`：本机帮助描述：Print TLS handshake messages

**帮助给出的命令示例（未作为本项目验收）**：

```bash
gmssl tls12_server -port 4432 -cert sm2_tls_server_certs.pem -key sm2_tls_server_key.pem -pass P@ssw0rd \
-cipher_suite TLS_ECDHE_SM4_CBC_SM3 -supported_group sm2p256v1 -sig_alg sm2sig_sm3
```

**运行条件**：需要受控网络端点、可信证书或测试服务；这里只验证帮助信息。

<details><summary>展开本机 `-help` 原文</summary>

```text
usage: tls12_server [-port num] -cert pem -key pem [-pass str] [-cacert pem] [-www] [-verbose]
Options

    -port num              Listening port number, default 443
    -cipher_suite str      Supported cipher suites, may appear multiple times, higher priority first
    -supported_group str   Supported elliptic curves, may appear multiple times, higher priority first
    -sig_alg str           Supported signature algorithms
    -cert pem              Server's certificate chain in PEM format
    -key pem               Server's encrypted private key in PEM format
    -pass str              Password to decrypt private key, prompt if not given
    -cert_request          Client certificate request
    -cacert pem            CA certificate for client certificate verification
    -verify_depth num      Certificate verification depth
    -client_cert_optional  Allow client send empty Certificate
    -renegotiation_info    Enable RFC 5746 renegotiation_info response
    -www                   Return HTTP 200 OK and echo client request data as text
    -verbose               Print TLS handshake messages


Supported cipher suites:
    TLS_ECDHE_SM4_CBC_SM3
    TLS_ECDHE_SM4_GCM_SM3
    TLS_ECDHE_ECDSA_WITH_AES_128_CBC_SHA256
    TLS_ECDHE_ECDSA_WITH_AES_128_GCM_SHA256
    TLS_ECDHE_ECDSA_WITH_AES_128_CCM


Examples

    gmssl sm2keygen -pass P@ssw0rd -out sm2_root_ca_key.pem
    gmssl certgen -C CN -ST Beijing -L Haidian -O GmSSL -OU Test -CN "GmSSL SM2 Test Root CA" \
        -days 3650 -key sm2_root_ca_key.pem -pass P@ssw0rd -out sm2_root_ca_cert.pem \
        -key_usage keyCertSign -key_usage cRLSign -ca

    gmssl sm2keygen -pass P@ssw0rd -out sm2_tls_ca_key.pem
    gmssl reqgen -C CN -ST Beijing -L Haidian -O GmSSL -OU Test -CN "GmSSL SM2 TLS CA" \
        -key sm2_tls_ca_key.pem -pass P@ssw0rd -out sm2_tls_ca_req.pem
    gmssl reqsign -in sm2_tls_ca_req.pem -days 1825 -key_usage keyCertSign \
        -key_usage cRLSign -path_len_constraint 0 -cacert sm2_root_ca_cert.pem \
        -key sm2_root_ca_key.pem -pass P@ssw0rd -out sm2_tls_ca_cert.pem -ca

    gmssl sm2keygen -pass P@ssw0rd -out sm2_tls_server_key.pem
    gmssl reqgen -C CN -ST Beijing -L Haidian -O GmSSL -OU Test -CN "GmSSL SM2 TLS Server" \
        -key sm2_tls_server_key.pem -pass P@ssw0rd -out sm2_tls_server_req.pem
    gmssl reqsign -in sm2_tls_server_req.pem -days 365 -key_usage digitalSignature \
        -ext_key_usage serverAuth -subject_dns_name localhost -cacert sm2_tls_ca_cert.pem \
        -key sm2_tls_ca_key.pem -pass P@ssw0rd -out sm2_tls_server_cert.pem
    cat sm2_tls_server_cert.pem > sm2_tls_server_certs.pem
    cat sm2_tls_ca_cert.pem >> sm2_tls_server_certs.pem

    gmssl sm2keygen -pass P@ssw0rd -out sm2_tls_client_key.pem
    gmssl reqgen -C CN -ST Beijing -L Haidian -O GmSSL -OU Test -CN "GmSSL SM2 TLS Client" \
        -key sm2_tls_client_key.pem -pass P@ssw0rd -out sm2_tls_client_req.pem
    gmssl reqsign -in sm2_tls_client_req.pem -days 365 -key_usage digitalSignature \
        -ext_key_usage clientAuth -cacert sm2_tls_ca_cert.pem -key sm2_tls_ca_key.pem \
        -pass P@ssw0rd -out sm2_tls_client_cert.pem
    cat sm2_tls_client_cert.pem > sm2_tls_client_certs.pem
    cat sm2_tls_ca_cert.pem >> sm2_tls_client_certs.pem

    printf 'hello tls12\n' > message.txt

    gmssl tls12_server -port 4432 -cert sm2_tls_server_certs.pem -key sm2_tls_server_key.pem -pass P@ssw0rd \
        -cipher_suite TLS_ECDHE_SM4_CBC_SM3 -supported_group sm2p256v1 -sig_alg sm2sig_sm3
    gmssl tls12_client -host 127.0.0.1 -port 4432 -server_name localhost -cacert sm2_root_ca_cert.pem \
        -cipher_suite TLS_ECDHE_SM4_CBC_SM3 -supported_group sm2p256v1 -sig_alg sm2sig_sm3 \
        -in message.txt

    gmssl tls12_server -port 4438 -cert sm2_tls_server_certs.pem -key sm2_tls_server_key.pem -pass P@ssw0rd \
        -cipher_suite TLS_ECDHE_SM4_GCM_SM3 -supported_group sm2p256v1 -sig_alg sm2sig_sm3 \
        -cacert sm2_root_ca_cert.pem -cert_request
    gmssl tls12_client -host 127.0.0.1 -port 4438 -server_name localhost -cacert sm2_root_ca_cert.pem \
        -cipher_suite TLS_ECDHE_SM4_GCM_SM3 -supported_group sm2p256v1 -sig_alg sm2sig_sm3 \
        -cert sm2_tls_client_certs.pem -key sm2_tls_client_key.pem -pass P@ssw0rd \
        -in message.txt
```

</details>

### `gmssl tls13_client`

**帮助命令**：`gmssl tls13_client -help`。**用法**：`usage: tls13_client -host str [-port num] [-cacert pem] [-cert pem -key pem [-pass str]] [-get path|-in file] [-verbose]`

**作用**：连接并诊断 TLS 1.3 服务端。

**帮助中需要先理解的参数**：

- `-signature_algorithms_cert`：本机帮助描述：Send signature_algorithms_cert extension
- `-certificate_authorities`：本机帮助描述：Send certificate_authorities extension
- `-status_request`：本机帮助描述：Send status_request (OCSP Stapling) request
- `-ct`：本机帮助描述：Send signed_certificate_timestamp (SCT) request
- `-psk_ke`：本机帮助描述：Support PSK-only key exchange
- `-psk_dhe_ke`：本机帮助描述：Support PSK with (EC)DHE key exchange

**帮助给出的命令示例（未作为本项目验收）**：

```bash
gmssl tls13_client -host 127.0.0.1 -port 4433 -server_name localhost -cacert sm2_root_ca_cert.pem \
-cipher_suite TLS_SM4_GCM_SM3 -supported_group sm2p256v1 -sig_alg sm2sig_sm3 \
-in message.txt
```

**运行条件**：需要受控网络端点、可信证书或测试服务；这里只验证帮助信息。

<details><summary>展开本机 `-help` 原文</summary>

```text
usage: tls13_client -host str [-port num] [-cacert pem] [-cert pem -key pem [-pass str]] [-get path|-in file] [-verbose]
Options

    -host str                 Server's hostname
    -port num                 Server's port number, default 443
    -cipher_suite str         Supported cipher suites, may appear multiple times, higher priority first
    -supported_group str      Supported elliptic curves, may appear multiple times, higher priority first
    -sig_alg str              Supported signature algorithms
    -max_key_exchanges num    Number of key exchanges in key_share extension
    -cacert pem               Root CA certificate in PEM format
    -verify_depth num         Certificate verification depth
    -cert pem                 Client's certificate chain in PEM format
    -key pem                  Client's encrypted private key in PEM format
    -pass str                 Password to decrypt private key, prompt if not given
    -server_name str          Send server_name (SNI) request
    -signature_algorithms_cert  Send signature_algorithms_cert extension
    -certificate_authorities  Send certificate_authorities extension
    -status_request           Send status_request (OCSP Stapling) request
    -ct                       Send signed_certificate_timestamp (SCT) request
    -psk_ke                   Support PSK-only key exchange
    -psk_dhe_ke               Support PSK with (EC)DHE key exchange
    -psk_identity str         PSK Identity
    -psk_cipher_suite str     PSK cipher suite
    -psk_key hex              PSK key in HEX format, of PSK hash length
    -sess_in                  Load server's session ticket file
    -sess_out                 Save server's session ticket file
    -early_data file          Send early data, -psk_ke and/or -psk_dhe_ke should be set
    -key_update_seq_num num   Send KeyUpdate handshake after sending/receiving <num> records
    -post_handshake_auth      Support post_handshake_auth
    -client_cert_optional     Allow client send empty Certificate
    -tls13_change_cipher_spec  Support ChangeCipherSpec in TLS 1.3 to be compatible with middlebox
    -get path                 Send a HTTP GET request and read response until close or timeout
    -in file | stdin          Send input data and read response until close or timeout
    -verbose                  Print TLS handshake messages


Supported cipher suites:
    TLS_SM4_GCM_SM3
    TLS_SM4_CCM_SM3
    TLS_AES_128_GCM_SHA256
    TLS_AES_128_CCM_SHA256


Examples

    gmssl sm2keygen -pass P@ssw0rd -out sm2_root_ca_key.pem
    gmssl certgen -C CN -ST Beijing -L Haidian -O GmSSL -OU Test -CN "GmSSL SM2 Test Root CA" \
        -days 3650 -key sm2_root_ca_key.pem -pass P@ssw0rd -out sm2_root_ca_cert.pem \
        -key_usage keyCertSign -key_usage cRLSign -ca

    gmssl sm2keygen -pass P@ssw0rd -out sm2_tls_ca_key.pem
    gmssl reqgen -C CN -ST Beijing -L Haidian -O GmSSL -OU Test -CN "GmSSL SM2 TLS CA" \
        -key sm2_tls_ca_key.pem -pass P@ssw0rd -out sm2_tls_ca_req.pem
    gmssl reqsign -in sm2_tls_ca_req.pem -days 1825 -key_usage keyCertSign \
        -key_usage cRLSign -path_len_constraint 0 -cacert sm2_root_ca_cert.pem \
        -key sm2_root_ca_key.pem -pass P@ssw0rd -out sm2_tls_ca_cert.pem -ca

    gmssl sm2keygen -pass P@ssw0rd -out sm2_tls_server_key.pem
    gmssl reqgen -C CN -ST Beijing -L Haidian -O GmSSL -OU Test -CN "GmSSL SM2 TLS Server" \
        -key sm2_tls_server_key.pem -pass P@ssw0rd -out sm2_tls_server_req.pem
    gmssl reqsign -in sm2_tls_server_req.pem -days 365 -key_usage digitalSignature \
        -ext_key_usage serverAuth -subject_dns_name localhost -cacert sm2_tls_ca_cert.pem \
        -key sm2_tls_ca_key.pem -pass P@ssw0rd -out sm2_tls_server_cert.pem
    cat sm2_tls_server_cert.pem > sm2_tls_server_certs.pem
    cat sm2_tls_ca_cert.pem >> sm2_tls_server_certs.pem

    gmssl sm2keygen -pass P@ssw0rd -out sm2_tls_client_key.pem
    gmssl reqgen -C CN -ST Beijing -L Haidian -O GmSSL -OU Test -CN "GmSSL SM2 TLS Client" \
        -key sm2_tls_client_key.pem -pass P@ssw0rd -out sm2_tls_client_req.pem
    gmssl reqsign -in sm2_tls_client_req.pem -days 365 -key_usage digitalSignature \
        -ext_key_usage clientAuth -cacert sm2_tls_ca_cert.pem -key sm2_tls_ca_key.pem \
        -pass P@ssw0rd -out sm2_tls_client_cert.pem
    cat sm2_tls_client_cert.pem > sm2_tls_client_certs.pem
    cat sm2_tls_ca_cert.pem >> sm2_tls_client_certs.pem

    printf 'hello tls13\n' > message.txt

    gmssl tls13_server -port 4433 -cert sm2_tls_server_certs.pem -key sm2_tls_server_key.pem -pass P@ssw0rd \
        -cipher_suite TLS_SM4_GCM_SM3 -supported_group sm2p256v1 -sig_alg sm2sig_sm3
    gmssl tls13_client -host 127.0.0.1 -port 4433 -server_name localhost -cacert sm2_root_ca_cert.pem \
        -cipher_suite TLS_SM4_GCM_SM3 -supported_group sm2p256v1 -sig_alg sm2sig_sm3 \
        -in message.txt

    gmssl tls13_server -port 4439 -cert sm2_tls_server_certs.pem -key sm2_tls_server_key.pem -pass P@ssw0rd \
        -cipher_suite TLS_SM4_GCM_SM3 -supported_group sm2p256v1 -sig_alg sm2sig_sm3 \
        -cacert sm2_root_ca_cert.pem -cert_request
    gmssl tls13_client -host 127.0.0.1 -port 4439 -server_name localhost -cacert sm2_root_ca_cert.pem \
        -cipher_suite TLS_SM4_GCM_SM3 -supported_group sm2p256v1 -sig_alg sm2sig_sm3 \
        -cert sm2_tls_client_certs.pem -key sm2_tls_client_key.pem -pass P@ssw0rd \
        -in message.txt
```

</details>

### `gmssl tls13_server`

**帮助命令**：`gmssl tls13_server -help`。**用法**：`usage: tls13_server [-port num] -cert pem -key pem [-pass str] [-cacert pem] [-www] [-verbose]`

**作用**：启动 TLS 1.3 测试服务端。

**帮助中需要先理解的参数**：

- `-cert_request`：本机帮助描述：Client certificate request
- `-client_cert_optional`：本机帮助描述：Allow client send empty Certificate
- `-psk_ke`：本机帮助描述：Support PSK-only key exchange
- `-psk_dhe_ke`：本机帮助描述：Support PSK with (EC)DHE key exchange
- `-early_data`：本机帮助描述：Accept EarlyData, support 0-RTT
- `-tls13_change_cipher_spec`：本机帮助描述：Support ChangeCipherSpec in TLS 1.3 to be compatible with middlebox

**帮助给出的命令示例（未作为本项目验收）**：

```bash
gmssl tls13_server -port 4433 -cert sm2_tls_server_certs.pem -key sm2_tls_server_key.pem -pass P@ssw0rd \
-cipher_suite TLS_SM4_GCM_SM3 -supported_group sm2p256v1 -sig_alg sm2sig_sm3
```

**运行条件**：需要受控网络端点、可信证书或测试服务；这里只验证帮助信息。

<details><summary>展开本机 `-help` 原文</summary>

```text
usage: tls13_server [-port num] -cert pem -key pem [-pass str] [-cacert pem] [-www] [-verbose]
Options

    -port num                 Listening port number, default 443
    -cipher_suite str         Client's cipher suites, may appear multiple times, higher priority first
    -supported_group str      Supported elliptic curves, may appear multiple times, higher priority first
    -sig_alg str              Supported signature algorithms
    -cert pem                 Server's certificate chain in PEM format
    -key pem                  Server's encrypted private key in PEM format
    -pass str                 Password to decrypt private key, prompt if not given
    -cert_request             Client certificate request
    -client_cert_optional     Allow client send empty Certificate
    -cacert pem               CA certificate for client certificate verification
    -verify_depth num         Certificate verification depth
    -psk_ke                   Support PSK-only key exchange
    -psk_dhe_ke               Support PSK with (EC)DHE key exchange
    -psk_identity str         PSK Identity
    -psk_cipher_suite str     PSK cipher suite
    -psk_key hex              PSK key in HEX format, of PSK hash length
    -early_data               Accept EarlyData, support 0-RTT
    -max_early_data_size num  Set extension max_early_data_size
    -new_session_ticket num   Send NewSessionTicket <num> times
    -ticket_key hex           Session ticket encrypt/decrypt key in HEX format
    -key_update_seq_num num   Send KeyUpdate handshake after sending/receiving <num> records
    -tls13_change_cipher_spec  Support ChangeCipherSpec in TLS 1.3 to be compatible with middlebox
    -www                      Return HTTP 200 OK and echo client request data as text
    -verbose                  Print TLS handshake messages


Supported cipher suites:
    TLS_SM4_GCM_SM3
    TLS_SM4_CCM_SM3
    TLS_AES_128_GCM_SHA256
    TLS_AES_128_CCM_SHA256


Examples

    gmssl sm2keygen -pass P@ssw0rd -out sm2_root_ca_key.pem
    gmssl certgen -C CN -ST Beijing -L Haidian -O GmSSL -OU Test -CN "GmSSL SM2 Test Root CA" \
        -days 3650 -key sm2_root_ca_key.pem -pass P@ssw0rd -out sm2_root_ca_cert.pem \
        -key_usage keyCertSign -key_usage cRLSign -ca

    gmssl sm2keygen -pass P@ssw0rd -out sm2_tls_ca_key.pem
    gmssl reqgen -C CN -ST Beijing -L Haidian -O GmSSL -OU Test -CN "GmSSL SM2 TLS CA" \
        -key sm2_tls_ca_key.pem -pass P@ssw0rd -out sm2_tls_ca_req.pem
    gmssl reqsign -in sm2_tls_ca_req.pem -days 1825 -key_usage keyCertSign \
        -key_usage cRLSign -path_len_constraint 0 -cacert sm2_root_ca_cert.pem \
        -key sm2_root_ca_key.pem -pass P@ssw0rd -out sm2_tls_ca_cert.pem -ca

    gmssl sm2keygen -pass P@ssw0rd -out sm2_tls_server_key.pem
    gmssl reqgen -C CN -ST Beijing -L Haidian -O GmSSL -OU Test -CN "GmSSL SM2 TLS Server" \
        -key sm2_tls_server_key.pem -pass P@ssw0rd -out sm2_tls_server_req.pem
    gmssl reqsign -in sm2_tls_server_req.pem -days 365 -key_usage digitalSignature \
        -ext_key_usage serverAuth -subject_dns_name localhost -cacert sm2_tls_ca_cert.pem \
        -key sm2_tls_ca_key.pem -pass P@ssw0rd -out sm2_tls_server_cert.pem
    cat sm2_tls_server_cert.pem > sm2_tls_server_certs.pem
    cat sm2_tls_ca_cert.pem >> sm2_tls_server_certs.pem

    gmssl sm2keygen -pass P@ssw0rd -out sm2_tls_client_key.pem
    gmssl reqgen -C CN -ST Beijing -L Haidian -O GmSSL -OU Test -CN "GmSSL SM2 TLS Client" \
        -key sm2_tls_client_key.pem -pass P@ssw0rd -out sm2_tls_client_req.pem
    gmssl reqsign -in sm2_tls_client_req.pem -days 365 -key_usage digitalSignature \
        -ext_key_usage clientAuth -cacert sm2_tls_ca_cert.pem -key sm2_tls_ca_key.pem \
        -pass P@ssw0rd -out sm2_tls_client_cert.pem
    cat sm2_tls_client_cert.pem > sm2_tls_client_certs.pem
    cat sm2_tls_ca_cert.pem >> sm2_tls_client_certs.pem

    printf 'hello tls13\n' > message.txt

    gmssl tls13_server -port 4433 -cert sm2_tls_server_certs.pem -key sm2_tls_server_key.pem -pass P@ssw0rd \
        -cipher_suite TLS_SM4_GCM_SM3 -supported_group sm2p256v1 -sig_alg sm2sig_sm3
    gmssl tls13_client -host 127.0.0.1 -port 4433 -server_name localhost -cacert sm2_root_ca_cert.pem \
        -cipher_suite TLS_SM4_GCM_SM3 -supported_group sm2p256v1 -sig_alg sm2sig_sm3 \
        -in message.txt

    gmssl tls13_server -port 4439 -cert sm2_tls_server_certs.pem -key sm2_tls_server_key.pem -pass P@ssw0rd \
        -cipher_suite TLS_SM4_GCM_SM3 -supported_group sm2p256v1 -sig_alg sm2sig_sm3 \
        -cacert sm2_root_ca_cert.pem -cert_request
    gmssl tls13_client -host 127.0.0.1 -port 4439 -server_name localhost -cacert sm2_root_ca_cert.pem \
        -cipher_suite TLS_SM4_GCM_SM3 -supported_group sm2p256v1 -sig_alg sm2sig_sm3 \
        -cert sm2_tls_client_certs.pem -key sm2_tls_client_key.pem -pass P@ssw0rd \
        -in message.txt
```

</details>

### `gmssl quic_client`

**帮助命令**：`gmssl quic_client -help`。**用法**：`usage: quic_client -host str [-port num] [-server_name str] [-cipher_suite str] [-supported_group str] [-sig_alg str] [-get path] [-verbose]`

**作用**：通过 QUIC/TLS 连接测试服务端。

**帮助中需要先理解的参数**：

- `-verbose`：本机帮助描述：Print QUIC packet, frame and TLS handshake messages

**帮助给出的命令示例（未作为本项目验收）**：

```bash
gmssl quic_client -host 127.0.0.1 -port 4433 -server_name localhost \
-cipher_suite TLS_AES_128_GCM_SHA256 -supported_group prime256v1 \
-sig_alg ecdsa_secp256r1_sha256 -get / -verbose
```

**运行条件**：需要受控网络端点、可信证书或测试服务；这里只验证帮助信息。

<details><summary>展开本机 `-help` 原文</summary>

```text
usage: quic_client -host str [-port num] [-server_name str] [-cipher_suite str] [-supported_group str] [-sig_alg str] [-get path] [-verbose]
Options

    -host str                 Server's hostname
    -port num                 Server's UDP port number, default 443
    -server_name str          Send server_name (SNI) request
    -cipher_suite str         TLS 1.3 cipher suite, default TLS_AES_128_GCM_SHA256
    -supported_group str      Supported elliptic curve, default prime256v1
    -sig_alg str              Supported signature algorithm, default ecdsa_secp256r1_sha256
    -get path                 HTTP/3 request path kept for future use
    -verbose                  Print QUIC packet, frame and TLS handshake messages


Supported cipher suites:
    TLS_AES_128_GCM_SHA256
    TLS_AES_128_CCM_SHA256
    TLS_SM4_GCM_SM3
    TLS_SM4_CCM_SM3

Examples

    gmssl quic_server -port 4433 -cert p256_tls_server_certs.pem -key p256_tls_server_key.pem \
        -pass P@ssw0rd -cipher_suite TLS_AES_128_GCM_SHA256 -supported_group prime256v1 \
        -sig_alg ecdsa_secp256r1_sha256 -verbose
    gmssl quic_client -host 127.0.0.1 -port 4433 -server_name localhost \
        -cipher_suite TLS_AES_128_GCM_SHA256 -supported_group prime256v1 \
        -sig_alg ecdsa_secp256r1_sha256 -get / -verbose

    gmssl quic_server -port 4434 -cert sm2_tls_server_certs.pem -key sm2_tls_server_key.pem \
        -pass P@ssw0rd -cipher_suite TLS_SM4_GCM_SM3 -supported_group sm2p256v1 \
        -sig_alg sm2sig_sm3 -verbose
    gmssl quic_client -host 127.0.0.1 -port 4434 -server_name localhost \
        -cipher_suite TLS_SM4_GCM_SM3 -supported_group sm2p256v1 -sig_alg sm2sig_sm3 \
        -get / -verbose

    ngtcp2/examples/osslserver --groups=P-256 --ciphers=TLS_AES_128_GCM_SHA256 \
        -d htdocs 127.0.0.1 4435 p256-key.pem p256-cert.pem
    gmssl quic_client -host 127.0.0.1 -port 4435 -server_name localhost \
        -cipher_suite TLS_AES_128_GCM_SHA256 -supported_group prime256v1 \
        -sig_alg ecdsa_secp256r1_sha256 -get / -verbose
```

</details>

### `gmssl quic_server`

**帮助命令**：`gmssl quic_server -help`。**用法**：`usage: quic_server [-port num] -cert pem -key pem [-pass str] [-cipher_suite str] [-supported_group str] [-sig_alg str] [-verbose]`

**作用**：启动 QUIC/TLS 测试服务端。

**帮助中需要先理解的参数**：

- `-verbose`：本机帮助描述：Print QUIC packet, frame and TLS handshake messages

**帮助给出的命令示例（未作为本项目验收）**：

```bash
gmssl quic_server -port 4433 -cert p256_tls_server_certs.pem -key p256_tls_server_key.pem \
-pass P@ssw0rd -cipher_suite TLS_AES_128_GCM_SHA256 -supported_group prime256v1 \
-sig_alg ecdsa_secp256r1_sha256 -verbose
```

**运行条件**：需要受控网络端点、可信证书或测试服务；这里只验证帮助信息。

<details><summary>展开本机 `-help` 原文</summary>

```text
usage: quic_server [-port num] -cert pem -key pem [-pass str] [-cipher_suite str] [-supported_group str] [-sig_alg str] [-verbose]
Options

    -port num                 Listening UDP port number, default 443
    -cert pem                 Server's certificate chain in PEM format
    -key pem                  Server's encrypted private key in PEM format
    -pass str                 Password to decrypt private key, prompt if not given
    -cipher_suite str         TLS 1.3 cipher suite, default TLS_AES_128_GCM_SHA256 and TLS_AES_128_CCM_SHA256
    -supported_group str      Supported elliptic curve, default prime256v1
    -sig_alg str              Supported signature algorithm, default ecdsa_secp256r1_sha256
    -verbose                  Print QUIC packet, frame and TLS handshake messages


Supported cipher suites:
    TLS_AES_128_GCM_SHA256
    TLS_AES_128_CCM_SHA256
    TLS_SM4_GCM_SM3
    TLS_SM4_CCM_SM3

Examples

    gmssl quic_server -port 4433 -cert p256_tls_server_certs.pem -key p256_tls_server_key.pem \
        -pass P@ssw0rd -cipher_suite TLS_AES_128_GCM_SHA256 -supported_group prime256v1 \
        -sig_alg ecdsa_secp256r1_sha256 -verbose
    gmssl quic_client -host 127.0.0.1 -port 4433 -server_name localhost \
        -cipher_suite TLS_AES_128_GCM_SHA256 -supported_group prime256v1 \
        -sig_alg ecdsa_secp256r1_sha256 -get / -verbose

    gmssl quic_server -port 4434 -cert sm2_tls_server_certs.pem -key sm2_tls_server_key.pem \
        -pass P@ssw0rd -cipher_suite TLS_SM4_GCM_SM3 -supported_group sm2p256v1 \
        -sig_alg sm2sig_sm3 -verbose
    gmssl quic_client -host 127.0.0.1 -port 4434 -server_name localhost \
        -cipher_suite TLS_SM4_GCM_SM3 -supported_group sm2p256v1 -sig_alg sm2sig_sm3 \
        -get / -verbose

    ngtcp2/examples/osslserver --groups=P-256 --ciphers=TLS_AES_128_GCM_SHA256 \
        -d htdocs 127.0.0.1 4435 p256-key.pem p256-cert.pem
    gmssl quic_client -host 127.0.0.1 -port 4435 -server_name localhost \
        -cipher_suite TLS_AES_128_GCM_SHA256 -supported_group prime256v1 \
        -sig_alg ecdsa_secp256r1_sha256 -get / -verbose
```

</details>

# OpenSSL 与 GmSSL 命令行速查

本文给出可在临时教学数据上运行的摘要、密钥生成、签名验签、证书与加解密例子。两个程序的完整子命令目录及逐项 `-help` 见 [OpenSSL 帮助索引](CLI-OPENSSL-HELP.md) 和 [GmSSL 帮助索引](CLI-GMSSL-HELP.md)：前者覆盖 53 个标准命令、19 个摘要别名和 79 个加密别名，后者覆盖 90 个子命令。本文是**本机可执行程序的操作参考**，不是 Agent 或 MCP 已实现功能清单。实现顺序仍以 [Roadmap](ROADMAP.md) 为准：V1 先接 SHA-256 只读摘要，V4 再开放经过授权和审批的写操作。新增 Provider 时先在命令行核对能力，再封装固定的程序和参数数组；模型只能传资源 ID 与允许列表中的业务参数。

## 版本、路径与练习约定

以下命令按 2026-10-13 本机 `openssl version` 得到的 **OpenSSL 3.0.2**，以及 `.local/gmssl/bin/gmssl version` 得到的 **GmSSL 3.3.0-dev.1183** 和各子命令的 `-help` 核对。版本变化后重新查看本机帮助；OpenSSL 的算法可用性还受编译选项和 Provider 配置影响。

在 `Agent-development-code` 根目录开始；示例只处理临时目录里的合成数据：

```bash
cd /home/zsw/work/agent_development/Agent-development-code
umask 077
OPENSSL_BIN=$(command -v openssl)
GMSSL_BIN="$PWD/../.local/gmssl/bin/gmssl"
WORK=$(mktemp -d)
printf abc > "$WORK/plain.txt"  # 恰好 3 字节，没有换行
"$OPENSSL_BIN" version
"$GMSSL_BIN" version
```

下文代码块复用同一终端中的 `OPENSSL_BIN`、`GMSSL_BIN`、`WORK`。完成后核对并删除自己创建的临时目录。不要把真实私钥、口令、明文、随机 key 或解密产物写进文档、提交到 Git，或送回模型。`gmssl sm2keygen/sm2sign/sm2decrypt -pass` 和 `gmssl sm4_gcm -key` 等参数会进入子进程命令行；以下口令 `demo-only` 只能用于一次性教学实验，生产用法需要另行设计秘密传递方式。

## 摘要：OpenSSL SHA-256、GmSSL SM3

```bash
"$OPENSSL_BIN" dgst -sha256 "$WORK/plain.txt"
"$GMSSL_BIN" sm3 -in "$WORK/plain.txt"
```

| 命令与参数 | 含义 | 对 `abc` 的预期结果 |
|---|---|---|
| `openssl dgst -sha256 <file>` | 对文件**原始字节**计算 SHA-256；可加 `-binary` 得到 32 字节二进制摘要 | `ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad` |
| `gmssl sm3 -in <file>` | 对文件原始字节计算 SM3；默认十六进制，`-bin` 为 32 字节二进制摘要 | `66c7f0f462eeedd9d1f2d46bdc10e4e24167c4875cf2f7a2297da02b8f4ba8e0` |

GmSSL 还提供 `sm3 -in_str <string>` 和默认 stdin 输入；`-in` 与 `-in_str` 不可同时使用。`sm3 -pubkey ... -id ...` 会加入 SM2 的 Z 值，不等于普通文件 SM3 摘要。Agent 首个 `digest_file` 固定为 OpenSSL/SHA-256，后续再按允许列表增加 GmSSL/SM3。[V1 单工具步骤](stages/V1-CORE-DEMO.md#first-demo)

**带密钥的 SM3 与口令派生是不同操作。**本机 `sm3_hmac -help` 要求十六进制密钥；`sm3_pbkdf2 -help` 要求口令、8–64 字节盐、迭代次数和输出长度：

```bash
HMAC_KEY=$("$GMSSL_BIN" rand -outlen 16 -hex)
"$GMSSL_BIN" sm3_hmac -key "$HMAC_KEY" -in "$WORK/plain.txt"
PBKDF2_SALT=$("$GMSSL_BIN" rand -outlen 16 -hex)
"$GMSSL_BIN" sm3_pbkdf2 -pass demo-only -salt "$PBKDF2_SALT" \
  -iter 10000 -outlen 16 -hex
```

`sm3_hmac` 的 `-key` 与 `-in` 分别表示密钥和消息；默认输出十六进制标签，`-bin` 输出原始字节。`sm3_pbkdf2` 的 `-outlen` 是**派生字节数**，不是十六进制字符数；上例输出 16 字节派生结果的 32 个十六进制字符。`-pass demo-only` 会暴露在进程参数中，只可用在临时教学数据。[GmSSL `sm3_hmac` 帮助](CLI-GMSSL-HELP.md#gmssl-sm3_hmac)、[GmSSL `sm3_pbkdf2` 帮助](CLI-GMSSL-HELP.md#gmssl-sm3_pbkdf2)

## OpenSSL：RSA 密钥、短消息加解密与文件签名

先生成一次性教学口令文件、加密的 RSA 私钥及其公钥：

```bash
"$OPENSSL_BIN" rand -hex 32 > "$WORK/pass.txt"
"$OPENSSL_BIN" genpkey -algorithm RSA -pkeyopt rsa_keygen_bits:2048 \
  -aes-256-cbc -pass "file:$WORK/pass.txt" -out "$WORK/rsa-private.pem"
"$OPENSSL_BIN" pkey -in "$WORK/rsa-private.pem" \
  -passin "file:$WORK/pass.txt" -pubout -out "$WORK/rsa-public.pem"
```

| 参数 | 作用 |
|---|---|
| `genpkey -algorithm RSA` | 生成 RSA 私钥；`-pkeyopt rsa_keygen_bits:2048` 指定密钥位数。 |
| `-aes-256-cbc -pass file:<path>` | 加密输出的私钥，并从服务端文件读取保护口令；`-out` 指定 PEM 私钥文件。 |
| `pkey -in ... -passin file:... -pubout -out ...` | 从受口令保护的私钥导出 PEM 公钥；`-passin` 是**读取现有私钥**的口令来源。 |

RSA-OAEP **只用于很短的数据**；下例明确将 OAEP 和 MGF1 都设为 SHA-256，并在解密时保持完全相同：

```bash
"$OPENSSL_BIN" pkeyutl -encrypt -pubin -inkey "$WORK/rsa-public.pem" \
  -pkeyopt rsa_padding_mode:oaep -pkeyopt rsa_oaep_md:sha256 \
  -pkeyopt rsa_mgf1_md:sha256 \
  -in "$WORK/plain.txt" -out "$WORK/rsa-cipher.bin"
"$OPENSSL_BIN" pkeyutl -decrypt -inkey "$WORK/rsa-private.pem" \
  -passin "file:$WORK/pass.txt" \
  -pkeyopt rsa_padding_mode:oaep -pkeyopt rsa_oaep_md:sha256 \
  -pkeyopt rsa_mgf1_md:sha256 \
  -in "$WORK/rsa-cipher.bin" -out "$WORK/rsa-recovered.txt"
cmp "$WORK/plain.txt" "$WORK/rsa-recovered.txt"
```

`-pubin` 说明 `-inkey` 指向公钥；`-encrypt`/`-decrypt` 选择动作。2048 位 RSA 配 OAEP/SHA-256 时，明文最多 `256 − 2×32 − 2 = 190` 字节；这是 RSA-OAEP 的单次消息上限，不能拿来加密文件。[RFC 8017](https://www.rfc-editor.org/rfc/rfc8017.html) 大文件加密需要经过核对的对称/混合加密方案。

文件签名由 `dgst` 先计算 SHA-256 摘要，再用私钥签名；文件本身不受上面的 190 字节 OAEP 限制：

```bash
"$OPENSSL_BIN" dgst -sha256 -sign "$WORK/rsa-private.pem" \
  -passin "file:$WORK/pass.txt" -out "$WORK/rsa.sig" "$WORK/plain.txt"
"$OPENSSL_BIN" dgst -sha256 -verify "$WORK/rsa-public.pem" \
  -signature "$WORK/rsa.sig" "$WORK/plain.txt"
```

| 参数 | 作用 |
|---|---|
| `dgst -sha256` | 先对输入文件计算 SHA-256；签名、验签必须使用相同方案。 |
| `-sign <private.pem>` / `-verify <public.pem>` | 分别指定签名私钥和验签公钥。 |
| `-passin file:<path>` / `-signature <file>` | 分别指定私钥口令来源和**二进制签名文件**。 |

验签成功的命令输出包含 `Verified OK`；程序应同时检查退出码，不能仅凭模型复述认定成功。这里的 RSA 签名方案要和未来 Provider 的固定 profile 一起确定。[OpenSSL `dgst` 文档](https://docs.openssl.org/3.0/man1/openssl-dgst/)

### OpenSSL CSR、证书字段与信任验证

`req -new` 用现有私钥生成 CSR；`-subj` 是请求的主体，不是被验证的主机名：

```bash
"$OPENSSL_BIN" req -new -sha256 -key "$WORK/rsa-private.pem" \
  -passin "file:$WORK/pass.txt" -subj /CN=localhost -out "$WORK/request.pem"
"$OPENSSL_BIN" req -in "$WORK/request.pem" -noout -verify -text
```

下一步生成仅供本地教学的自签证书，加入 `localhost` 的 SAN；分别检查字段和**显式信任这个测试证书**后的主机名验证：

```bash
"$OPENSSL_BIN" req -new -x509 -sha256 -key "$WORK/rsa-private.pem" \
  -passin "file:$WORK/pass.txt" -subj /CN=localhost -days 1 \
  -addext 'subjectAltName=DNS:localhost' -out "$WORK/cert.pem"
"$OPENSSL_BIN" x509 -in "$WORK/cert.pem" -noout \
  -subject -issuer -dates -fingerprint -sha256
"$OPENSSL_BIN" verify -CAfile "$WORK/cert.pem" \
  -verify_hostname localhost "$WORK/cert.pem"
```

`req -x509` 输出证书而不是 CSR；`-days` 指有效天数。`x509 -noout` 只展示字段，不能据此宣称证书链可信。`verify -CAfile` 在这个例子中**人为把测试自签证书加入信任锚**，返回 OK 只说明这套指定输入条件通过；它不意味着该证书被公共 CA 信任。[OpenSSL `req` 帮助](CLI-OPENSSL-HELP.md#openssl-req)、[OpenSSL `verify` 帮助](CLI-OPENSSL-HELP.md#openssl-verify)

## OpenSSL：对称加解密命令的边界

下面的 AES-256-CBC 命令仅用于理解 `enc` 的参数和往返文件操作：

```bash
"$OPENSSL_BIN" enc -aes-256-cbc -e -salt -pbkdf2 -iter 200000 \
  -pass "file:$WORK/pass.txt" -in "$WORK/plain.txt" -out "$WORK/aes-cbc.bin"
"$OPENSSL_BIN" enc -aes-256-cbc -d -pbkdf2 -iter 200000 \
  -pass "file:$WORK/pass.txt" -in "$WORK/aes-cbc.bin" -out "$WORK/aes-recovered.txt"
cmp "$WORK/plain.txt" "$WORK/aes-recovered.txt"
```

`-e`/`-d` 选择加密/解密，`-in`/`-out` 指定文件，`-pass file:...` 指定口令来源；`-salt` 为加密添加盐，`-pbkdf2 -iter 200000` 指定口令派生方式，解密必须使用相同迭代次数。**CBC 不提供认证**：解密完成或 `cmp` 相等不代表它满足项目 V4 的认证加密要求。`openssl enc` 命令也不支持 GCM/CCM；OpenSSL *库* 支持这些算法，不能据此推断该命令支持。[OpenSSL `enc` 文档](https://docs.openssl.org/3.0/man1/openssl-enc/)

本机的另一条 CLI 路线是 CMS 容器：已用上面创建的教学证书验证 `cms -aes-256-gcm` 加解密往返。它的输出是 **CMS DER 容器**，不能与 `enc` 的裸文件格式混用：

```bash
"$OPENSSL_BIN" cms -encrypt -binary -aes-256-gcm \
  -in "$WORK/plain.txt" -outform DER -out "$WORK/cms.der" "$WORK/cert.pem"
"$OPENSSL_BIN" cms -decrypt -binary -inform DER -in "$WORK/cms.der" \
  -recip "$WORK/cert.pem" -inkey "$WORK/rsa-private.pem" \
  -passin "file:$WORK/pass.txt" -out "$WORK/cms-recovered.txt"
cmp "$WORK/plain.txt" "$WORK/cms-recovered.txt"
```

`-encrypt` 最后的位置参数是接收者证书，`-decrypt` 的 `-recip`/`-inkey` 是接收者证书/私钥；`-binary` 避免文本规范化改变输入字节，`-outform DER` 与 `-inform DER` 必须配对。本机命令往返成功只证明此组合可运行；V4 接入前仍要固定证书授权、容器格式、篡改失败处理、临时输出和审批。[OpenSSL `cms` 帮助](CLI-OPENSSL-HELP.md#openssl-cms)、[V4 密码写操作](stages/V4-APPROVAL-CRYPTO.md)

## GmSSL：SM2 密钥、签名验签与短消息加解密

```bash
"$GMSSL_BIN" sm2keygen -pass demo-only \
  -out "$WORK/sm2-private.pem" -pubout "$WORK/sm2-public.pem"
"$GMSSL_BIN" sm2sign -key "$WORK/sm2-private.pem" -pass demo-only \
  -id 1234567812345678 -in "$WORK/plain.txt" -out "$WORK/sm2.sig"
"$GMSSL_BIN" sm2verify -pubkey "$WORK/sm2-public.pem" \
  -id 1234567812345678 -in "$WORK/plain.txt" -sig "$WORK/sm2.sig"
```

| 命令与参数 | 作用 |
|---|---|
| `sm2keygen -pass ... -out <private.pem> -pubout <public.pem>` | 生成受口令保护的 PKCS #8 PEM 私钥和 PEM 公钥。当前代码中的 `keystore.py` 管理教学密钥 ID 与文件；不要让模型传私钥路径或口令。 |
| `sm2sign -key <private.pem> -pass ... -id <identity> -in <file> -out <sig>` | 对文件签名；输出为**二进制 DER** 签名。省略 `-in`/`-out` 时分别使用 stdin/stdout。 |
| `sm2verify -pubkey <public.pem> -id <identity> -in <file> -sig <sig>` | 用同一原文、签名和 signer ID 验签；也可用 `-cert` 指定证书代替 `-pubkey`。 |

`-id` 必须在签名和验签时一致；未给出时本机帮助显示默认值为 `1234567812345678`。当前项目把它固定在 [GmSSL Provider](../Agent-development-code/packages/crypto/providers/gmssl_cli.py)，实际调用仍要核对结果。现有文件签名的 **1 MiB** 上限是项目策略，并非 `sm2sign` 算法的统一最大消息长度。

SM2 公钥加密是**短消息操作**。本机 `sm2encrypt -help` 明确写明明文最多 **255 字节**；密文是二进制 DER：

```bash
"$GMSSL_BIN" sm2encrypt -pubkey "$WORK/sm2-public.pem" \
  -in "$WORK/plain.txt" -out "$WORK/sm2-cipher.der"
"$GMSSL_BIN" sm2decrypt -key "$WORK/sm2-private.pem" -pass demo-only \
  -in "$WORK/sm2-cipher.der" -out "$WORK/sm2-recovered.txt"
cmp "$WORK/plain.txt" "$WORK/sm2-recovered.txt"
```

`sm2encrypt` 还接受 `-cert <recipient.pem>` 代替 `-pubkey`；`sm2decrypt` 需私钥和口令。不要将“SM2 文件签名允许 1 MiB”理解为“SM2 公钥加密允许 1 MiB”。

### GmSSL CSR、CA 签发与证书验证

`certgen` 创建教学根证书；`reqgen` 为另一把密钥创建 CSR；`reqsign` 由根证书和根私钥签发服务器叶子证书。`certverify` 默认针对 TLCP 服务端，下面的 TLS 服务器证书**显式**使用 `-server`：

```bash
"$GMSSL_BIN" sm2keygen -pass demo-only \
  -out "$WORK/ca-key.pem" -pubout "$WORK/ca-pub.pem"
"$GMSSL_BIN" certgen -C CN -CN DemoRoot -serial_len 16 -days 30 \
  -key "$WORK/ca-key.pem" -pass demo-only -ca -path_len_constraint 1 \
  -key_usage keyCertSign -key_usage cRLSign -out "$WORK/ca-cert.pem"
"$GMSSL_BIN" sm2keygen -pass demo-only \
  -out "$WORK/leaf-key.pem" -pubout "$WORK/leaf-pub.pem"
"$GMSSL_BIN" reqgen -C CN -CN localhost -key "$WORK/leaf-key.pem" \
  -pass demo-only -out "$WORK/leaf.csr.pem"
"$GMSSL_BIN" reqsign -in "$WORK/leaf.csr.pem" -serial_len 16 -days 1 \
  -cacert "$WORK/ca-cert.pem" -key "$WORK/ca-key.pem" -pass demo-only \
  -key_usage digitalSignature -ext_key_usage serverAuth \
  -subject_dns_name localhost -out "$WORK/leaf-cert.pem"
"$GMSSL_BIN" certparse -in "$WORK/leaf-cert.pem"
"$GMSSL_BIN" certverify -server -in "$WORK/leaf-cert.pem" \
  -cacert "$WORK/ca-cert.pem" -hostname localhost
```

`-ca`、`keyCertSign` 与 `cRLSign` 使根证书承担 CA 用途；`reqsign` 的 `-cacert`/`-key` 是**签发者**证书/私钥，`serverAuth`、`subject_dns_name` 是**叶子**证书用途/主机名。`certparse` 只解析字段；`certverify -server` 才按指定 CA 和主机名验证。用自签根证书直接当服务器叶子证书验证会失败，这也是为什么不能把“证书生成成功”当成“TLS 服务端验证通过”。[GmSSL `reqsign` 帮助](CLI-GMSSL-HELP.md#gmssl-reqsign)、[GmSSL `certverify` 帮助](CLI-GMSSL-HELP.md#gmssl-certverify)

## GmSSL：SM4-GCM 认证加解密

本机 `sm4_gcm -help` 给出的关键参数为 `-encrypt|-decrypt`、`-key <hex>`、`-iv <hex>`、可选的 `-aad`/`-aad_hex`、`-taglen <bytes>` 与 `-in`/`-out`。以下示例只处理临时教学文件：

```bash
SM4_KEY=$("$GMSSL_BIN" rand -outlen 16 -hex)
SM4_IV=$("$GMSSL_BIN" rand -outlen 12 -hex)
"$GMSSL_BIN" sm4_gcm -encrypt -key "$SM4_KEY" -iv "$SM4_IV" \
  -aad_hex 001122 -in "$WORK/plain.txt" -out "$WORK/sm4-gcm.bin"
"$GMSSL_BIN" sm4_gcm -decrypt -key "$SM4_KEY" -iv "$SM4_IV" \
  -aad_hex 001122 -in "$WORK/sm4-gcm.bin" -out "$WORK/sm4-recovered.txt"
cmp "$WORK/plain.txt" "$WORK/sm4-recovered.txt"
```

| 参数 | 含义与约束 |
|---|---|
| `-key <hex>` | SM4 密钥为 16 字节，即 32 个十六进制字符；示例把它放在命令行，仅可用于教学。 |
| `-iv <hex>` | nonce/IV；本机帮助推荐 12 字节，即 24 个十六进制字符。同一密钥下**不能复用 nonce**；解密使用对应的原 nonce。 |
| `-aad_hex <hex>` | 只认证、不加密的附加数据；解密时必须提供相同内容。`-aad <string>` 是文本形式，两者择一。 |
| `-taglen <bytes>` | 认证标签长度，默认 16 字节；解密时要和加密时一致。 |
| `-in <file>` / `-out <file>` | 解密输入格式是 `ciphertext || tag`，即密文后接标签；解密输出是明文。 |

认证失败必须视为整个解密失败。本机错误 AAD 测试返回非零，但 `-out` 路径仍留下 **0 字节文件**；Provider 应写受控临时路径，验证成功后才发布产物，并在失败时清理。上面的 SM4-GCM 命令只能证明 CLI 有此能力，**不代表本项目已经接入 V4 加解密工具**。

同一个本机程序还支持 SM4-CCM；本机帮助限定 IV 为 7–13 字节、标签为 4–16 字节。这里使用 12 字节 IV 和默认标签长度：

```bash
SM4_CCM_KEY=$("$GMSSL_BIN" rand -outlen 16 -hex)
SM4_CCM_IV=$("$GMSSL_BIN" rand -outlen 12 -hex)
"$GMSSL_BIN" sm4_ccm -encrypt -key "$SM4_CCM_KEY" -iv "$SM4_CCM_IV" \
  -aad_hex 001122 -in "$WORK/plain.txt" -out "$WORK/sm4-ccm.bin"
"$GMSSL_BIN" sm4_ccm -decrypt -key "$SM4_CCM_KEY" -iv "$SM4_CCM_IV" \
  -aad_hex 001122 -in "$WORK/sm4-ccm.bin" -out "$WORK/sm4-ccm-recovered.txt"
cmp "$WORK/plain.txt" "$WORK/sm4-ccm-recovered.txt"
```

`sm4_ccm` 的解密输入同样是 `ciphertext || tag`；密钥、IV、AAD 和 tag 长度须与加密一致。CBC 命令有另一套参数：`-key`、`-iv` 均为 16 字节值的十六进制编码，`-pkcs7_padding` 让任意字节长度可处理：

```bash
SM4_CBC_KEY=$("$GMSSL_BIN" rand -outlen 16 -hex)
SM4_CBC_IV=$("$GMSSL_BIN" rand -outlen 16 -hex)
"$GMSSL_BIN" sm4_cbc -encrypt -pkcs7_padding \
  -key "$SM4_CBC_KEY" -iv "$SM4_CBC_IV" \
  -in "$WORK/plain.txt" -out "$WORK/sm4-cbc.bin"
"$GMSSL_BIN" sm4_cbc -decrypt -pkcs7_padding \
  -key "$SM4_CBC_KEY" -iv "$SM4_CBC_IV" \
  -in "$WORK/sm4-cbc.bin" -out "$WORK/sm4-cbc-recovered.txt"
cmp "$WORK/plain.txt" "$WORK/sm4-cbc-recovered.txt"
```

SM4-CBC 没有 GCM/CCM 的认证标签，**不能替代 V4 的 AEAD**。三个模式的命令行往返都已经用临时 `abc` 文件验证；这只覆盖正常路径，不能代替篡改、重复 nonce、权限和失败清理验证。[GmSSL `sm4_cbc` 帮助](CLI-GMSSL-HELP.md#gmssl-sm4_cbc)、[GmSSL `sm4_ccm` 帮助](CLI-GMSSL-HELP.md#gmssl-sm4_ccm)

## GmSSL：SM9 身份密码与 Kyber KEM 示例

这些不是当前 Agent 的开放工具。以下流程仅说明本机帮助中的 `-alg`、主公钥/主私钥、用户 `-id` 和 KEM 产物如何配对，测试数据仍保存在 `WORK`：

```bash
"$GMSSL_BIN" sm9setup -alg sm9sign -pass demo-only \
  -out "$WORK/sm9-sign-master.pem" -pubout "$WORK/sm9-sign-public.pem"
"$GMSSL_BIN" sm9keygen -alg sm9sign -in "$WORK/sm9-sign-master.pem" \
  -inpass demo-only -id Alice -out "$WORK/sm9-sign-alice.pem" -outpass demo-only
"$GMSSL_BIN" sm9sign -key "$WORK/sm9-sign-alice.pem" -pass demo-only \
  -in "$WORK/plain.txt" -out "$WORK/sm9.sig"
"$GMSSL_BIN" sm9verify -pubmaster "$WORK/sm9-sign-public.pem" \
  -id Alice -in "$WORK/plain.txt" -sig "$WORK/sm9.sig"
```

`sm9setup` 的 `-alg sm9sign` 生成签名用途主密钥；`sm9keygen` 从它和身份 `Alice` 派生用户签名私钥；验签用主公钥、相同身份、原文与签名。加密用途需要**另建** `-alg sm9encrypt` 主密钥，不能拿签名用途密钥替代：[SM9 逐项帮助](CLI-GMSSL-HELP.md#sm9-身份密码)。

```bash
"$GMSSL_BIN" sm9setup -alg sm9encrypt -pass demo-only \
  -out "$WORK/sm9-enc-master.pem" -pubout "$WORK/sm9-enc-public.pem"
"$GMSSL_BIN" sm9keygen -alg sm9encrypt -in "$WORK/sm9-enc-master.pem" \
  -inpass demo-only -id Alice -out "$WORK/sm9-enc-alice.pem" -outpass demo-only
"$GMSSL_BIN" sm9encrypt -pubmaster "$WORK/sm9-enc-public.pem" \
  -id Alice -in "$WORK/plain.txt" -out "$WORK/sm9.der"
"$GMSSL_BIN" sm9decrypt -key "$WORK/sm9-enc-alice.pem" -pass demo-only \
  -id Alice -in "$WORK/sm9.der" -out "$WORK/sm9-recovered.txt"
cmp "$WORK/plain.txt" "$WORK/sm9-recovered.txt"
```

Kyber 的 `encap/decap` 是**共享秘密封装与解封装**，不是把 `plain.txt` 直接加密。`-out` 是 KEM 密文，`-outkey` 是封装得到的共享秘密；解封装结果应与之相等：

```bash
"$GMSSL_BIN" kyberkeygen -out "$WORK/kyber-private.bin" \
  -pubout "$WORK/kyber-public.bin"
"$GMSSL_BIN" kyberencap -pubkey "$WORK/kyber-public.bin" \
  -out "$WORK/kyber-cipher.bin" -outkey "$WORK/kyber-key.bin"
"$GMSSL_BIN" kyberdecap -key "$WORK/kyber-private.bin" \
  -in "$WORK/kyber-cipher.bin" -out "$WORK/kyber-recovered-key.bin"
cmp "$WORK/kyber-key.bin" "$WORK/kyber-recovered-key.bin"
```

上述 SM9 与 Kyber 正常路径已用本机 CLI 跑通；身份错误、篡改、密钥版本及秘密存储尚需另测，不能据此开放 MCP 工具。[GmSSL SM9 帮助](CLI-GMSSL-HELP.md#sm9-身份密码)、[GmSSL Kyber 帮助](CLI-GMSSL-HELP.md#椭圆曲线哈希签名与-kem)

## 接入项目时的对应关系

| 命令行能力 | Provider | MCP 工具 | 当前状态 |
|---|---|---|---|
| OpenSSL SHA-256 | `packages/crypto/providers/openssl_cli.py` | `mcp_integration/server_crypto/openssl_tools/tools.py` 的 `digest_file` | V1 待实现；先独立算摘要，再接 MCP/Agent。 |
| GmSSL SM3 | `packages/crypto/providers/gmssl_cli.py` 后续函数 | 在同一个 Crypto MCP Server 中注册只读摘要工具或固定算法选项 | 待实现；先核对与 SHA-256 的结果/参数区分。 |
| GmSSL SM2 密钥、签名、验签 | `packages/crypto/keystore.py` 与 `gmssl_cli.py` | `gmssl_tools/sm_tools.py` | 教学 Demo 已实现；正式权限/审批仍待后续阶段。 |
| RSA/SM2 加解密、SM4-GCM 等写操作 | 先确定本机真实支持的命令与受控服务 | V4 先接一种固定审批的认证加密；其他能力按阶段需求扩展 | 命令示例只是练习，不能据此宣称 MCP 已开放。 |

命令帮助是本机参数的最终核对入口：`"$OPENSSL_BIN" <command> -help` 与 `"$GMSSL_BIN" <command> -help`。OpenSSL 参考：[genpkey](https://docs.openssl.org/3.0/man1/openssl-genpkey/)、[pkeyutl](https://docs.openssl.org/3.0/man1/openssl-pkeyutl/)、[dgst](https://docs.openssl.org/3.0/man1/openssl-dgst/)、[enc](https://docs.openssl.org/3.0/man1/openssl-enc/)；GmSSL 参数以本机 `3.3.0-dev.1183` 的各子命令帮助为准。文件上限、权限、审批和失败验证分别按 [V1](stages/V1-CORE-DEMO.md)、[V3](stages/V3-MCP.md)、[V4](stages/V4-APPROVAL-CRYPTO.md) 阶段验收。

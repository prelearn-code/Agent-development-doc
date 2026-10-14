# OpenSSL 全部标准子命令：本机 `-help` 与解读

本页逐项运行并整理 OpenSSL 3.0.2 的 **53 个子命令**。每节先列本机 `-help` 的用法，再解释作用和关键参数；折叠块保留帮助内容供逐项核对。绝对可执行文件路径已缩写为 `openssl`，行末空白已去除，参数和示例内容不改。**帮助可显示不等于实际业务已运行通过**。

入口：`openssl help`，查看单项：`openssl <command> -help`。`[]` 表示可选参数，`|` 表示互斥选择；格式和默认值以当前安装版本为准。可运行的教学命令与参数间配对见[常用例子](CLI-CRYPTO-REFERENCE.md)。

涉及证书、网络、设备、CA 或用户密钥的命令需要对应测试资源；此页只声明 help 已核对，未将这些外部流程冒充验证完成。私钥、口令和对称密钥不作为模型参数传入。

## 入口、配置与诊断

### `openssl help`

**帮助命令**：`openssl help -help`。**用法**：`Usage: help [options] [command]`

**作用**：列出可用命令及某个命令的帮助。

<details><summary>展开本机 `-help` 原文</summary>

```text
Usage: help [options] [command]

General options:
 -help      Display this summary

Parameters:
 command    Name of command to display help (optional)
```

</details>

### `openssl version`

**帮助命令**：`openssl version -help`。**用法**：`Usage: version [options]`

**作用**：查看 CLI、编译与安装版本信息。

**帮助中需要先理解的参数**：

- `-a`：本机帮助描述：Show all data
- `-b`：本机帮助描述：Show build date
- `-d`：本机帮助描述：Show configuration directory
- `-e`：本机帮助描述：Show engines directory
- `-m`：本机帮助描述：Show modules directory
- `-f`：本机帮助描述：Show compiler flags used

<details><summary>展开本机 `-help` 原文</summary>

```text
Usage: version [options]

General options:
 -help  Display this summary

Output options:
 -a     Show all data
 -b     Show build date
 -d     Show configuration directory
 -e     Show engines directory
 -m     Show modules directory
 -f     Show compiler flags used
 -o     Show some internal datatype options
 -p     Show target build platform
 -r     Show random seeding options
 -v     Show library version
 -c     Show CPU settings info
```

</details>

### `openssl list`

**帮助命令**：`openssl list -help`。**用法**：`Usage: list [options]`

**作用**：列出算法、Provider、命令与支持能力；可用性仍需运行验证。

**帮助中需要先理解的参数**：

- `-verbose`：本机帮助描述：Verbose listing
- `-commands`：本机帮助描述：List of standard commands
- `-standard-commands`：本机帮助描述：List of standard commands
- `-digest-commands`：本机帮助描述：List of message digest commands (deprecated)
- `-digest-algorithms`：本机帮助描述：List of message digest algorithms
- `-kdf-algorithms`：本机帮助描述：List of key derivation and pseudo random function algorithms

<details><summary>展开本机 `-help` 原文</summary>

```text
Usage: list [options]

General options:
 -help                     Display this summary

Output options:
 -1                        List in one column
 -verbose                  Verbose listing
 -select val               Select a single algorithm
 -commands                 List of standard commands
 -standard-commands        List of standard commands
 -digest-commands          List of message digest commands (deprecated)
 -digest-algorithms        List of message digest algorithms
 -kdf-algorithms           List of key derivation and pseudo random function algorithms
 -random-instances         List the primary, public and private random number generator details
 -random-generators        List of random number generators
 -mac-algorithms           List of message authentication code algorithms
 -cipher-commands          List of cipher commands (deprecated)
 -cipher-algorithms        List of cipher algorithms
 -encoders                 List of encoding methods
 -decoders                 List of decoding methods
 -key-managers             List of key managers
 -key-exchange-algorithms  List of key exchange algorithms
 -kem-algorithms           List of key encapsulation mechanism algorithms
 -signature-algorithms     List of signature algorithms
 -asymcipher-algorithms    List of asymmetric cipher algorithms
 -public-key-algorithms    List of public key algorithms
 -public-key-methods       List of public key methods
 -store-loaders            List of store loaders
 -providers                List of provider information
 -engines                  List of loaded engines
 -disabled                 List of disabled features
 -options val              List options for specified command
 -objects                  List built in objects (OID<->name mappings)

Provider options:
 -provider-path val        Provider load path (must be before 'provider' argument if required)
 -provider val             Provider to load (can be specified multiple times)
 -propquery val            Property query used when fetching algorithms
```

</details>

### `openssl info`

**帮助命令**：`openssl info -help`。**用法**：`Usage: info [options]`

**作用**：打印 OpenSSL 安装目录与运行时信息。

**帮助中需要先理解的参数**：

- `-configdir`：本机帮助描述：Default configuration file directory
- `-enginesdir`：本机帮助描述：Default engine module directory
- `-modulesdir`：本机帮助描述：Default module directory (other than engine modules)
- `-dsoext`：本机帮助描述：Configured extension for modules
- `-dirnamesep`：本机帮助描述：Directory-filename separator
- `-listsep`：本机帮助描述：List separator character

<details><summary>展开本机 `-help` 原文</summary>

```text
Usage: info [options]

General options:
 -help         Display this summary

Output options:
 -configdir    Default configuration file directory
 -enginesdir   Default engine module directory
 -modulesdir   Default module directory (other than engine modules)
 -dsoext       Configured extension for modules
 -dirnamesep   Directory-filename separator
 -listsep      List separator character
 -seeds        Seed sources
 -cpusettings  CPU settings info
```

</details>

### `openssl errstr`

**帮助命令**：`openssl errstr -help`。**用法**：`Usage: errstr [options] errnum...`

**作用**：把 OpenSSL 数字错误码转换为文本。

<details><summary>展开本机 `-help` 原文</summary>

```text
Usage: errstr [options] errnum...

General options:
 -help     Display this summary

Parameters:
 errnum    Error number(s) to decode
```

</details>

### `openssl engine`

**帮助命令**：`openssl engine -help`。**用法**：`Usage: engine [options] engine...`

**作用**：列出或测试旧式 ENGINE 组件；OpenSSL 3 更常使用 Provider。

**帮助中需要先理解的参数**：

- `-t`：本机帮助描述：Check that specified engine is available
- `-v`：本机帮助描述：List 'control commands' For each specified engine
- `-vv`：本机帮助描述：Also display each command's description
- `-vvv`：本机帮助描述：Also add the input flags for each command
- `-vvvv`：本机帮助描述：Also show internal input flags
- `-c`：本机帮助描述：List the capabilities of specified engine

<details><summary>展开本机 `-help` 原文</summary>

```text
Usage: engine [options] engine...

General options:
 -help      Display this summary
 -t         Check that specified engine is available
 -pre val   Run command against the ENGINE before loading it
 -post val  Run command against the ENGINE after loading it

Output options:
 -v         List 'control commands' For each specified engine
 -vv        Also display each command's description
 -vvv       Also add the input flags for each command
 -vvvv      Also show internal input flags
 -c         List the capabilities of specified engine
 -tt        Display error trace for unavailable engines
            Commands are like "SO_PATH:/lib/libdriver.so"

Parameters:
 engine     ID of engine(s) to load
```

</details>

### `openssl fipsinstall`

**帮助命令**：`openssl fipsinstall -help`。**用法**：`Usage: fipsinstall [options]`

**作用**：为 FIPS Provider 生成或校验配置，需已安装对应模块。

**帮助中需要先理解的参数**：

- `-verify`：选择验签动作或公钥；本机帮助描述：Verify a config file instead of generating one
- `-no_conditional_errors`：本机帮助描述：Disable the ability of the fips module to enter an error state if any conditional self tests fail
- `-no_security_checks`：本机帮助描述：Disable the run-time FIPS security checks in the module
- `-self_test_onload`：本机帮助描述：Forces self tests to always run on module load
- `-noout`：本机帮助描述：Disable logging of self test events
- `-quiet`：本机帮助描述：No messages, just exit status

<details><summary>展开本机 `-help` 原文</summary>

```text
Usage: fipsinstall [options]

General options:
 -help                   Display this summary
 -verify                 Verify a config file instead of generating one
 -module infile          File name of the provider module
 -provider_name val      FIPS provider name
 -section_name val       FIPS Provider config section name (optional)
 -no_conditional_errors  Disable the ability of the fips module to enter an error state if any conditional self tests fail
 -no_security_checks     Disable the run-time FIPS security checks in the module
 -self_test_onload       Forces self tests to always run on module load

Input options:
 -in infile              Input config file, used when verifying

Output options:
 -out outfile            Output config file, used when generating
 -mac_name val           MAC name
 -macopt val             MAC algorithm parameters in n:v form. See 'PARAMETER NAMES' in the EVP_MAC_ docs
 -noout                  Disable logging of self test events
 -corrupt_desc val       Corrupt a self test by description
 -corrupt_type val       Corrupt a self test by type
 -config infile          The parent config to verify
 -quiet                  No messages, just exit status
```

</details>

### `openssl speed`

**帮助命令**：`openssl speed -help`。**用法**：`Usage: speed [options] [algorithm...]`

**作用**：测试算法速度；结果与机器及构建有关。

**帮助中需要先理解的参数**：

- `-decrypt`：选择解密动作；本机帮助描述：Time decryption instead of encryption (only EVP)
- `-mb`：本机帮助描述：Enable (tls1>=1) multi-block mode on EVP-named cipher
- `-mr`：本机帮助描述：Produce machine readable output
- `-aead`：本机帮助描述：Benchmark EVP-named AEAD cipher in TLS-like sequence
- `-elapsed`：本机帮助描述：Use wall-clock time instead of CPU user time as divisor

<details><summary>展开本机 `-help` 原文</summary>

```text
Usage: speed [options] [algorithm...]

General options:
 -help               Display this summary
 -mb                 Enable (tls1>=1) multi-block mode on EVP-named cipher
 -mr                 Produce machine readable output
 -multi +int         Run benchmarks in parallel
 -async_jobs +int    Enable async mode and start specified number of jobs
 -engine val         Use engine, possibly a hardware device
 -primes +int        Specify number of primes (for RSA only)

Selection options:
 -evp val            Use EVP-named cipher or digest
 -hmac val           HMAC using EVP-named digest
 -cmac val           CMAC using EVP-named cipher
 -decrypt            Time decryption instead of encryption (only EVP)
 -aead               Benchmark EVP-named AEAD cipher in TLS-like sequence

Timing options:
 -elapsed            Use wall-clock time instead of CPU user time as divisor
 -seconds +int       Run benchmarks for specified amount of seconds
 -bytes +int         Run [non-PKI] benchmarks on custom-sized buffer
 -misalign +int      Use specified offset to mis-align buffers

Random state options:
 -rand val           Load the given file(s) into the random number generator
 -writerand outfile  Write random data to the specified file

Provider options:
 -provider-path val  Provider load path (must be before 'provider' argument if required)
 -provider val       Provider to load (can be specified multiple times)
 -propquery val      Property query used when fetching algorithms

Parameters:
 algorithm           Algorithm(s) to test (optional; otherwise tests all)
```

</details>

### `openssl asn1parse`

**帮助命令**：`openssl asn1parse -help`。**用法**：`Usage: asn1parse [options]`

**作用**：解析 ASN.1 DER/PEM 结构、偏移与嵌套字段。

**帮助中需要先理解的参数**：

- `-noout`：本机帮助描述：do not produce any output
- `-strictpem`：本机帮助描述：do not attempt base64 decode outside PEM markers
- `-i`：本机帮助描述：indents the output
- `-dump`：本机帮助描述：unknown data in hex form

<details><summary>展开本机 `-help` 原文</summary>

```text
Usage: asn1parse [options]

General options:
 -help            Display this summary
 -oid infile      file of extra oid definitions

I/O options:
 -inform PEM|DER  input format - one of DER PEM
 -in infile       input file
 -out outfile     output file (output format is always DER)
 -noout           do not produce any output
 -offset +int     offset into file
 -length +int     length of section in file
 -strparse +int   offset; a series of these can be used to 'dig'
 -genstr val      string to generate ASN1 structure from
                  into multiple ASN1 blob wrappings
 -genconf val     file to generate ASN1 structure from
 -strictpem       do not attempt base64 decode outside PEM markers
 -item val        item to parse and print
                  (-inform  will be ignored)

Formatting options:
 -i               indents the output
 -dump            unknown data in hex form
 -dlimit +int     dump the first arg bytes of unknown data in hex form
```

</details>

## 摘要、MAC、派生和随机数

### `openssl dgst`

**帮助命令**：`openssl dgst -help`。**用法**：`Usage: dgst [options] [file...]`

**作用**：计算摘要，也能先摘要再生成/验证数字签名。

**参数解读**：`-sha256` 指定摘要，`-sign` 用私钥、`-verify` 用公钥、`-signature` 指定二进制签名文件。

**帮助中需要先理解的参数**：

- `-list`：本机帮助描述：List digests
- `-engine_impl`：本机帮助描述：Also use engine given by -engine for digest operations
- `-c`：本机帮助描述：Print the digest with separating colons
- `-r`：本机帮助描述：Print the digest in coreutils format
- `-hex`：本机帮助描述：Print as hex dump
- `-binary`：本机帮助描述：Print in binary form

<details><summary>展开本机 `-help` 原文</summary>

```text
Usage: dgst [options] [file...]

General options:
 -help               Display this summary
 -list               List digests
 -engine val         Use engine e, possibly a hardware device
 -engine_impl        Also use engine given by -engine for digest operations
 -passin val         Input file pass phrase source

Output options:
 -c                  Print the digest with separating colons
 -r                  Print the digest in coreutils format
 -out outfile        Output to filename rather than stdout
 -keyform format     Key file format (ENGINE, other values ignored)
 -hex                Print as hex dump
 -binary             Print in binary form
 -xoflen +int        Output length for XOF algorithms
 -d                  Print debug info
 -debug              Print debug info

Signing options:
 -sign val           Sign digest using private key
 -verify val         Verify a signature using public key
 -prverify val       Verify a signature using private key
 -sigopt val         Signature parameter in n:v form
 -signature infile   File with signature to verify
 -hmac val           Create hashed MAC with key
 -mac val            Create MAC (not necessarily HMAC)
 -macopt val         MAC algorithm parameters in n:v form or key
 -*                  Any supported digest
 -fips-fingerprint   Compute HMAC with the key used in OpenSSL-FIPS fingerprint

Random state options:
 -rand val           Load the given file(s) into the random number generator
 -writerand outfile  Write random data to the specified file

Provider options:
 -provider-path val  Provider load path (must be before 'provider' argument if required)
 -provider val       Provider to load (can be specified multiple times)
 -propquery val      Property query used when fetching algorithms

Parameters:
 file                Files to digest (optional; default is stdin)
```

</details>

### `openssl mac`

**帮助命令**：`openssl mac -help`。**用法**：`Usage: mac [options] mac_name`

**作用**：使用指定 MAC 算法对输入计算标签。

**帮助中需要先理解的参数**：

- `-binary`：本机帮助描述：Output in binary format (default is hexadecimal)

<details><summary>展开本机 `-help` 原文</summary>

```text
Usage: mac [options] mac_name

General options:
 -help               Display this summary
 -macopt val         MAC algorithm parameters in n:v form
 -cipher val         Cipher
 -digest val         Digest
                     See 'PARAMETER NAMES' in the EVP_MAC_ docs

Input options:
 -in infile          Input file to MAC (default is stdin)

Output options:
 -out outfile        Output to filename rather than stdout
 -binary             Output in binary format (default is hexadecimal)

Provider options:
 -provider-path val  Provider load path (must be before 'provider' argument if required)
 -provider val       Provider to load (can be specified multiple times)
 -propquery val      Property query used when fetching algorithms

Parameters:
 mac_name            MAC algorithm
```

</details>

### `openssl kdf`

**帮助命令**：`openssl kdf -help`。**用法**：`Usage: kdf [options] kdf_name`

**作用**：调用指定 KDF，以参数派生固定长度密钥。

**帮助中需要先理解的参数**：

- `-binary`：本机帮助描述：Output in binary format (default is hexadecimal)

<details><summary>展开本机 `-help` 原文</summary>

```text
Usage: kdf [options] kdf_name

General options:
 -help               Display this summary
 -kdfopt val         KDF algorithm control parameters in n:v form
 -cipher val         Cipher
 -digest val         Digest
 -mac val            MAC
                     See 'Supported Controls' in the EVP_KDF_ docs

 -keylen val         The size of the output derived key

Output options:
 -out outfile        Output to filename rather than stdout
 -binary             Output in binary format (default is hexadecimal)

Provider options:
 -provider-path val  Provider load path (must be before 'provider' argument if required)
 -provider val       Provider to load (can be specified multiple times)
 -propquery val      Property query used when fetching algorithms

Parameters:
 kdf_name            Name of the KDF algorithm
```

</details>

### `openssl rand`

**帮助命令**：`openssl rand -help`。**用法**：`Usage: rand [options] num`

**作用**：生成指定字节数的随机数据。

**帮助中需要先理解的参数**：

- `-base64`：本机帮助描述：Base64 encode output
- `-hex`：本机帮助描述：Hex encode output

<details><summary>展开本机 `-help` 原文</summary>

```text
Usage: rand [options] num

General options:
 -help               Display this summary
 -engine val         Use engine, possibly a hardware device

Output options:
 -out outfile        Output file
 -base64             Base64 encode output
 -hex                Hex encode output

Random state options:
 -rand val           Load the given file(s) into the random number generator
 -writerand outfile  Write random data to the specified file

Provider options:
 -provider-path val  Provider load path (must be before 'provider' argument if required)
 -provider val       Provider to load (can be specified multiple times)
 -propquery val      Property query used when fetching algorithms

Parameters:
 num                 Number of bytes to generate
```

</details>

### `openssl passwd`

**帮助命令**：`openssl passwd -help`。**用法**：`Usage: passwd [options] [password]`

**作用**：产生口令哈希，不能当作文件加密。

**帮助中需要先理解的参数**：

- `-noverify`：本机帮助描述：Never verify when reading password from terminal
- `-stdin`：本机帮助描述：Read passwords from stdin
- `-quiet`：本机帮助描述：No warnings
- `-table`：本机帮助描述：Format output as table
- `-reverse`：本机帮助描述：Switch table columns
- `-apr1`：本机帮助描述：MD5-based password algorithm, Apache variant

<details><summary>展开本机 `-help` 原文</summary>

```text
Usage: passwd [options] [password]

General options:
 -help               Display this summary

Input options:
 -in infile          Read passwords from file
 -noverify           Never verify when reading password from terminal
 -stdin              Read passwords from stdin

Output options:
 -quiet              No warnings
 -table              Format output as table
 -reverse            Switch table columns

Cryptographic options:
 -salt val           Use provided salt
 -6                  SHA512-based password algorithm
 -5                  SHA256-based password algorithm
 -apr1               MD5-based password algorithm, Apache variant
 -1                  MD5-based password algorithm
 -aixmd5             AIX MD5-based password algorithm

Random state options:
 -rand val           Load the given file(s) into the random number generator
 -writerand outfile  Write random data to the specified file

Provider options:
 -provider-path val  Provider load path (must be before 'provider' argument if required)
 -provider val       Provider to load (can be specified multiple times)
 -propquery val      Property query used when fetching algorithms

Parameters:
 password            Password text to digest (optional)
```

</details>

## 密钥、参数与公钥运算

### `openssl genpkey`

**帮助命令**：`openssl genpkey -help`。**用法**：`Usage: genpkey [options]`

**作用**：按算法与选项生成私钥或参数。

**参数解读**：`-algorithm`、`-pkeyopt` 固定密钥类型/参数；`-pass` 指定输出私钥的口令来源。

**帮助中需要先理解的参数**：

- `-quiet`：本机帮助描述：Do not output status while generating keys
- `-genparam`：本机帮助描述：Generate parameters, not key
- `-text`：本机帮助描述：Print the in text

<details><summary>展开本机 `-help` 原文</summary>

```text
Usage: genpkey [options]

General options:
 -help               Display this summary
 -engine val         Use engine, possibly a hardware device
 -paramfile infile   Parameters file
 -algorithm val      The public key algorithm
 -quiet              Do not output status while generating keys
 -pkeyopt val        Set the public key algorithm option as opt:value
 -config infile      Load a configuration file (this may load modules)

Output options:
 -out outfile        Output file
 -outform PEM|DER    output format (DER or PEM)
 -pass val           Output file pass phrase source
 -genparam           Generate parameters, not key
 -text               Print the in text
 -*                  Cipher to use to encrypt the key

Provider options:
 -provider-path val  Provider load path (must be before 'provider' argument if required)
 -provider val       Provider to load (can be specified multiple times)
 -propquery val      Property query used when fetching algorithms
Order of options may be important!  See the documentation.
```

</details>

### `openssl pkey`

**帮助命令**：`openssl pkey -help`。**用法**：`Usage: pkey [options]`

**作用**：读取、检查、转换私钥/公钥并导出公钥。

**帮助中需要先理解的参数**：

- `-check`：本机帮助描述：Check key consistency
- `-pubcheck`：本机帮助描述：Check public key consistency
- `-pubin`：本机帮助描述：Read only public components from key input
- `-traditional`：本机帮助描述：Use traditional format for private key PEM output
- `-pubout`：本机帮助描述：Restrict encoded output to public components
- `-noout`：本机帮助描述：Do not output the key in encoded form

<details><summary>展开本机 `-help` 原文</summary>

```text
Usage: pkey [options]

General options:
 -help               Display this summary
 -engine val         Use engine, possibly a hardware device

Provider options:
 -provider-path val  Provider load path (must be before 'provider' argument if required)
 -provider val       Provider to load (can be specified multiple times)
 -propquery val      Property query used when fetching algorithms
 -check              Check key consistency
 -pubcheck           Check public key consistency

Input options:
 -in val             Input key
 -inform format      Key input format (ENGINE, other values ignored)
 -passin val         Key input pass phrase source
 -pubin              Read only public components from key input

Output options:
 -out outfile        Output file for encoded and/or text output
 -outform PEM|DER    Output encoding format (DER or PEM)
 -*                  Any supported cipher to be used for encryption
 -passout val        Output PEM file pass phrase source
 -traditional        Use traditional format for private key PEM output
 -pubout             Restrict encoded output to public components
 -noout              Do not output the key in encoded form
 -text               Output key components in plaintext
 -text_pub           Output only public key components in text form
 -ec_conv_form val   Specifies the EC point conversion form in the encoding
 -ec_param_enc val   Specifies the way the EC parameters are encoded
```

</details>

### `openssl pkeyparam`

**帮助命令**：`openssl pkeyparam -help`。**用法**：`Usage: pkeyparam [options]`

**作用**：检查或转换公钥算法参数。

**帮助中需要先理解的参数**：

- `-check`：本机帮助描述：Check key param consistency
- `-text`：本机帮助描述：Print parameters as text
- `-noout`：本机帮助描述：Don't output encoded parameters

<details><summary>展开本机 `-help` 原文</summary>

```text
Usage: pkeyparam [options]

General options:
 -help               Display this summary
 -engine val         Use engine, possibly a hardware device
 -check              Check key param consistency

Input options:
 -in infile          Input file

Output options:
 -out outfile        Output file
 -text               Print parameters as text
 -noout              Don't output encoded parameters

Provider options:
 -provider-path val  Provider load path (must be before 'provider' argument if required)
 -provider val       Provider to load (can be specified multiple times)
 -propquery val      Property query used when fetching algorithms
```

</details>

### `openssl pkeyutl`

**帮助命令**：`openssl pkeyutl -help`。**用法**：`Usage: pkeyutl [options]`

**作用**：执行非对称加解密、签名、验签或密钥协商。

**参数解读**：RSA-OAEP 的 padding、OAEP digest、MGF1 digest 必须在加解密两边固定。

**帮助中需要先理解的参数**：

- `-encrypt`：选择加密动作；本机帮助描述：Encrypt input data with public key
- `-decrypt`：选择解密动作；本机帮助描述：Decrypt input data with private key
- `-sign`：选择签名动作或私钥；本机帮助描述：Sign input data with private key
- `-verify`：选择验签动作或公钥；本机帮助描述：Verify with public key
- `-engine_impl`：本机帮助描述：Also use engine given by -engine for crypto operations
- `-derive`：本机帮助描述：Derive shared secret

<details><summary>展开本机 `-help` 原文</summary>

```text
Usage: pkeyutl [options]

General options:
 -help                     Display this summary
 -engine val               Use engine, possibly a hardware device
 -engine_impl              Also use engine given by -engine for crypto operations
 -sign                     Sign input data with private key
 -verify                   Verify with public key
 -encrypt                  Encrypt input data with public key
 -decrypt                  Decrypt input data with private key
 -derive                   Derive shared secret
 -config infile            Load a configuration file (this may load modules)

Input options:
 -in infile                Input file - default stdin
 -rawin                    Indicate the input data is in raw form
 -pubin                    Input is a public key
 -inkey val                Input private key file
 -passin val               Input file pass phrase source
 -peerkey val              Peer key file used in key derivation
 -peerform PEM|DER|ENGINE  Peer key format (DER/PEM/P12/ENGINE)
 -certin                   Input is a cert with a public key
 -rev                      Reverse the order of the input buffer
 -sigfile infile           Signature file (verify operation only)
 -keyform PEM|DER|ENGINE   Private key format (ENGINE, other values ignored)

Output options:
 -out outfile              Output file - default stdout
 -asn1parse                asn1parse the output data
 -hexdump                  Hex dump output
 -verifyrecover            Verify with public key, recover original data

Signing/Derivation options:
 -digest val               Specify the digest algorithm when signing the raw input data
 -pkeyopt val              Public key options as opt:value
 -pkeyopt_passin val       Public key option that is read as a passphrase argument opt:passphrase
 -kdf val                  Use KDF algorithm
 -kdflen +int              KDF algorithm output length

Random state options:
 -rand val                 Load the given file(s) into the random number generator
 -writerand outfile        Write random data to the specified file

Provider options:
 -provider-path val        Provider load path (must be before 'provider' argument if required)
 -provider val             Provider to load (can be specified multiple times)
 -propquery val            Property query used when fetching algorithms
```

</details>

### `openssl genrsa`

**帮助命令**：`openssl genrsa -help`。**用法**：`Usage: genrsa [options] numbits`

**作用**：传统 RSA 私钥生成入口；新实现优先核对 genpkey。

**帮助中需要先理解的参数**：

- `-F4`：本机帮助描述：Use the Fermat number F4 (0x10001) for the E value
- `-f4`：本机帮助描述：Use the Fermat number F4 (0x10001) for the E value
- `-verbose`：本机帮助描述：Verbose output
- `-traditional`：本机帮助描述：Use traditional format for private keys

<details><summary>展开本机 `-help` 原文</summary>

```text
Usage: genrsa [options] numbits

General options:
 -help               Display this summary
 -engine val         Use engine, possibly a hardware device

Input options:
 -3                  (deprecated) Use 3 for the E value
 -F4                 Use the Fermat number F4 (0x10001) for the E value
 -f4                 Use the Fermat number F4 (0x10001) for the E value

Output options:
 -out outfile        Output the key to specified file
 -passout val        Output file pass phrase source
 -primes +int        Specify number of primes
 -verbose            Verbose output
 -traditional        Use traditional format for private keys
 -*                  Encrypt the output with any supported cipher

Random state options:
 -rand val           Load the given file(s) into the random number generator
 -writerand outfile  Write random data to the specified file

Provider options:
 -provider-path val  Provider load path (must be before 'provider' argument if required)
 -provider val       Provider to load (can be specified multiple times)
 -propquery val      Property query used when fetching algorithms

Parameters:
 numbits             Size of key in bits
```

</details>

### `openssl rsa`

**帮助命令**：`openssl rsa -help`。**用法**：`Usage: rsa [options]`

**作用**：读取、转换或打印传统 RSA 密钥。

**帮助中需要先理解的参数**：

- `-check`：本机帮助描述：Verify key consistency
- `-pubin`：本机帮助描述：Expect a public key in input file
- `-RSAPublicKey_in`：本机帮助描述：Input is an RSAPublicKey
- `-pubout`：本机帮助描述：Output a public key
- `-RSAPublicKey_out`：本机帮助描述：Output is an RSAPublicKey
- `-noout`：本机帮助描述：Don't print key out

<details><summary>展开本机 `-help` 原文</summary>

```text
Usage: rsa [options]

General options:
 -help               Display this summary
 -check              Verify key consistency
 -*                  Any supported cipher
 -engine val         Use engine, possibly a hardware device

Input options:
 -in val             Input file
 -inform format      Input format (DER/PEM/P12/ENGINE
 -pubin              Expect a public key in input file
 -RSAPublicKey_in    Input is an RSAPublicKey
 -passin val         Input file pass phrase source

Output options:
 -out outfile        Output file
 -outform format     Output format, one of DER PEM PVK
 -pubout             Output a public key
 -RSAPublicKey_out   Output is an RSAPublicKey
 -passout val        Output file pass phrase source
 -noout              Don't print key out
 -text               Print the key in text
 -modulus            Print the RSA key modulus
 -traditional        Use traditional format for private keys

PVK options:
 -pvk-strong         Enable 'Strong' PVK encoding level (default)
 -pvk-weak           Enable 'Weak' PVK encoding level
 -pvk-none           Don't enforce PVK encoding

Provider options:
 -provider-path val  Provider load path (must be before 'provider' argument if required)
 -provider val       Provider to load (can be specified multiple times)
 -propquery val      Property query used when fetching algorithms
```

</details>

### `openssl rsautl`

**帮助命令**：`openssl rsautl -help`。**用法**：`Usage: rsautl [options]`

**作用**：旧 RSA 运算入口；优先使用 pkeyutl。

**参数解读**：这是旧入口，本项目若需非对称运算用 `pkeyutl` 并固定 padding。

**帮助中需要先理解的参数**：

- `-encrypt`：选择加密动作；本机帮助描述：Encrypt with public key
- `-decrypt`：选择解密动作；本机帮助描述：Decrypt with private key
- `-sign`：选择签名动作或私钥；本机帮助描述：Sign with private key
- `-verify`：选择验签动作或公钥；本机帮助描述：Verify with public key
- `-pubin`：本机帮助描述：Input is an RSA public
- `-certin`：本机帮助描述：Input is a cert carrying an RSA public key

<details><summary>展开本机 `-help` 原文</summary>

```text
The command rsautl was deprecated in version 3.0. Use 'pkeyutl' instead.
Usage: rsautl [options]

General options:
 -help                    Display this summary
 -sign                    Sign with private key
 -verify                  Verify with public key
 -encrypt                 Encrypt with public key
 -decrypt                 Decrypt with private key
 -engine val              Use engine, possibly a hardware device

Input options:
 -in infile               Input file
 -inkey val               Input key
 -keyform PEM|DER|ENGINE  Private key format (ENGINE, other values ignored)
 -pubin                   Input is an RSA public
 -certin                  Input is a cert carrying an RSA public key
 -rev                     Reverse the order of the input buffer
 -passin val              Input file pass phrase source

Output options:
 -out outfile             Output file
 -raw                     Use no padding
 -pkcs                    Use PKCS#1 v1.5 padding (default)
 -x931                    Use ANSI X9.31 padding
 -oaep                    Use PKCS#1 OAEP
 -asn1parse               Run output through asn1parse; useful with -verify
 -hexdump                 Hex dump output

Random state options:
 -rand val                Load the given file(s) into the random number generator
 -writerand outfile       Write random data to the specified file

Provider options:
 -provider-path val       Provider load path (must be before 'provider' argument if required)
 -provider val            Provider to load (can be specified multiple times)
 -propquery val           Property query used when fetching algorithms
```

</details>

### `openssl gendsa`

**帮助命令**：`openssl gendsa -help`。**用法**：`Usage: gendsa [options] dsaparam-file`

**作用**：依据 DSA 参数文件生成 DSA 私钥。

**帮助中需要先理解的参数**：

- `-verbose`：本机帮助描述：Verbose output

<details><summary>展开本机 `-help` 原文</summary>

```text
Usage: gendsa [options] dsaparam-file

General options:
 -help               Display this summary
 -engine val         Use engine, possibly a hardware device

Output options:
 -out outfile        Output the key to the specified file
 -passout val        Output file pass phrase source

Random state options:
 -rand val           Load the given file(s) into the random number generator
 -writerand outfile  Write random data to the specified file

Provider options:
 -provider-path val  Provider load path (must be before 'provider' argument if required)
 -provider val       Provider to load (can be specified multiple times)
 -propquery val      Property query used when fetching algorithms
 -*                  Encrypt the output with any supported cipher
 -verbose            Verbose output

Parameters:
 dsaparam-file       File containing DSA parameters
```

</details>

### `openssl dsa`

**帮助命令**：`openssl dsa -help`。**用法**：`Usage: dsa [options]`

**作用**：读取、转换或打印 DSA 密钥。

**帮助中需要先理解的参数**：

- `-pvk-strong`：本机帮助描述：Enable 'Strong' PVK encoding level (default)
- `-pvk-weak`：本机帮助描述：Enable 'Weak' PVK encoding level
- `-pvk-none`：本机帮助描述：Don't enforce PVK encoding
- `-pubin`：本机帮助描述：Expect a public key in input file
- `-noout`：本机帮助描述：Don't print key out
- `-text`：本机帮助描述：Print the key in text

<details><summary>展开本机 `-help` 原文</summary>

```text
Usage: dsa [options]

General options:
 -help               Display this summary
 -*                  Any supported cipher
 -pvk-strong         Enable 'Strong' PVK encoding level (default)
 -pvk-weak           Enable 'Weak' PVK encoding level
 -pvk-none           Don't enforce PVK encoding
 -engine val         Use engine e, possibly a hardware device

Input options:
 -in val             Input key
 -inform format      Input format (DER/PEM/PVK); has no effect
 -pubin              Expect a public key in input file
 -passin val         Input file pass phrase source

Output options:
 -out outfile        Output file
 -outform format     Output format, DER PEM PVK
 -noout              Don't print key out
 -text               Print the key in text
 -modulus            Print the DSA public value
 -pubout             Output public key, not private
 -passout val        Output file pass phrase source

Provider options:
 -provider-path val  Provider load path (must be before 'provider' argument if required)
 -provider val       Provider to load (can be specified multiple times)
 -propquery val      Property query used when fetching algorithms
```

</details>

### `openssl dsaparam`

**帮助命令**：`openssl dsaparam -help`。**用法**：`Usage: dsaparam [options] [numbits]`

**作用**：生成或检查 DSA 参数。

**帮助中需要先理解的参数**：

- `-text`：本机帮助描述：Print as text
- `-noout`：本机帮助描述：No output
- `-verbose`：本机帮助描述：Verbose output
- `-genkey`：本机帮助描述：Generate a DSA key

<details><summary>展开本机 `-help` 原文</summary>

```text
Usage: dsaparam [options] [numbits]

General options:
 -help               Display this summary
 -engine val         Use engine e, possibly a hardware device

Input options:
 -in infile          Input file
 -inform PEM|DER     Input format - DER or PEM

Output options:
 -out outfile        Output file
 -outform PEM|DER    Output format - DER or PEM
 -text               Print as text
 -noout              No output
 -verbose            Verbose output
 -genkey             Generate a DSA key

Random state options:
 -rand val           Load the given file(s) into the random number generator
 -writerand outfile  Write random data to the specified file

Provider options:
 -provider-path val  Provider load path (must be before 'provider' argument if required)
 -provider val       Provider to load (can be specified multiple times)
 -propquery val      Property query used when fetching algorithms

Parameters:
 numbits             Number of bits if generating parameters (optional)
```

</details>

### `openssl ec`

**帮助命令**：`openssl ec -help`。**用法**：`Usage: ec [options]`

**作用**：读取、转换或打印椭圆曲线密钥。

**帮助中需要先理解的参数**：

- `-pubin`：本机帮助描述：Expect a public key in input file
- `-check`：本机帮助描述：check key consistency
- `-noout`：本机帮助描述：Don't print key out
- `-text`：本机帮助描述：Print the key
- `-param_out`：本机帮助描述：Print the elliptic curve parameters
- `-pubout`：本机帮助描述：Output public key, not private

<details><summary>展开本机 `-help` 原文</summary>

```text
Usage: ec [options]

General options:
 -help               Display this summary
 -engine val         Use engine, possibly a hardware device

Input options:
 -in val             Input file
 -inform format      Input format (DER/PEM/P12/ENGINE)
 -pubin              Expect a public key in input file
 -passin val         Input file pass phrase source
 -check              check key consistency
 -*                  Any supported cipher
 -param_enc val      Specifies the way the ec parameters are encoded
 -conv_form val      Specifies the point conversion form

Output options:
 -out outfile        Output file
 -outform PEM|DER    Output format - DER or PEM
 -noout              Don't print key out
 -text               Print the key
 -param_out          Print the elliptic curve parameters
 -pubout             Output public key, not private
 -no_public          exclude public key from private key
 -passout val        Output file pass phrase source

Provider options:
 -provider-path val  Provider load path (must be before 'provider' argument if required)
 -provider val       Provider to load (can be specified multiple times)
 -propquery val      Property query used when fetching algorithms
```

</details>

### `openssl ecparam`

**帮助命令**：`openssl ecparam -help`。**用法**：`Usage: ecparam [options]`

**作用**：列出曲线、生成或检查曲线参数。

**帮助中需要先理解的参数**：

- `-list_curves`：本机帮助描述：Prints a list of all curve 'short names'
- `-genkey`：本机帮助描述：Generate ec key
- `-text`：本机帮助描述：Print the ec parameters in text form
- `-noout`：本机帮助描述：Do not print the ec parameter
- `-check`：本机帮助描述：Validate the ec parameters
- `-check_named`：本机帮助描述：Check that named EC curve parameters have not been modified

<details><summary>展开本机 `-help` 原文</summary>

```text
Usage: ecparam [options]

General options:
 -help               Display this summary
 -list_curves        Prints a list of all curve 'short names'
 -engine val         Use engine, possibly a hardware device
 -genkey             Generate ec key
 -in infile          Input file  - default stdin
 -inform PEM|DER     Input format - default PEM (DER or PEM)
 -out outfile        Output file - default stdout
 -outform PEM|DER    Output format - default PEM

Output options:
 -text               Print the ec parameters in text form
 -noout              Do not print the ec parameter
 -param_enc val      Specifies the way the ec parameters are encoded

Parameter options:
 -check              Validate the ec parameters
 -check_named        Check that named EC curve parameters have not been modified
 -no_seed            If 'explicit' parameters are chosen do not use the seed
 -name val           Use the ec parameters with specified 'short name'
 -conv_form val      Specifies the point conversion form

Random state options:
 -rand val           Load the given file(s) into the random number generator
 -writerand outfile  Write random data to the specified file

Provider options:
 -provider-path val  Provider load path (must be before 'provider' argument if required)
 -provider val       Provider to load (can be specified multiple times)
 -propquery val      Property query used when fetching algorithms
```

</details>

### `openssl dhparam`

**帮助命令**：`openssl dhparam -help`。**用法**：`Usage: dhparam [options] [numbits]`

**作用**：生成或检查传统 DH 参数。

**帮助中需要先理解的参数**：

- `-check`：本机帮助描述：Check the DH parameters
- `-dsaparam`：本机帮助描述：Read or generate DSA parameters, convert to DH
- `-text`：本机帮助描述：Print a text form of the DH parameters
- `-noout`：本机帮助描述：Don't output any DH parameters

<details><summary>展开本机 `-help` 原文</summary>

```text
Usage: dhparam [options] [numbits]

General options:
 -help               Display this summary
 -check              Check the DH parameters
 -dsaparam           Read or generate DSA parameters, convert to DH
 -engine val         Use engine e, possibly a hardware device

Input options:
 -in infile          Input file
 -inform PEM|DER     Input format, DER or PEM

Output options:
 -out outfile        Output file
 -outform PEM|DER    Output format, DER or PEM
 -text               Print a text form of the DH parameters
 -noout              Don't output any DH parameters
 -2                  Generate parameters using 2 as the generator value
 -3                  Generate parameters using 3 as the generator value
 -5                  Generate parameters using 5 as the generator value

Random state options:
 -rand val           Load the given file(s) into the random number generator
 -writerand outfile  Write random data to the specified file

Provider options:
 -provider-path val  Provider load path (must be before 'provider' argument if required)
 -provider val       Provider to load (can be specified multiple times)
 -propquery val      Property query used when fetching algorithms

Parameters:
 numbits             Number of bits if generating parameters (optional)
```

</details>

### `openssl prime`

**帮助命令**：`openssl prime -help`。**用法**：`Usage: prime [options] [number...]`

**作用**：检查或生成大素数，属于参数工具。

**帮助中需要先理解的参数**：

- `-hex`：本机帮助描述：Hex output
- `-generate`：本机帮助描述：Generate a prime
- `-safe`：本机帮助描述：When used with -generate, generate a safe prime

<details><summary>展开本机 `-help` 原文</summary>

```text
Usage: prime [options] [number...]

General options:
 -help               Display this summary
 -bits +int          Size of number in bits
 -checks +int        Number of checks

Output options:
 -hex                Hex output
 -generate           Generate a prime
 -safe               When used with -generate, generate a safe prime

Provider options:
 -provider-path val  Provider load path (must be before 'provider' argument if required)
 -provider val       Provider to load (can be specified multiple times)
 -propquery val      Property query used when fetching algorithms

Parameters:
 number              Number(s) to check for primality if not generating
```

</details>

## 对称文件操作

### `openssl enc`

**帮助命令**：`openssl enc -help`。**用法**：`Usage: enc [options]`

**作用**：对称文件加解密与编码；该 CLI 不提供 GCM/CCM。

**参数解读**：`-pass`、`-pbkdf2`、`-iter`、`-salt` 是口令文件示例的关键参数；本 CLI 不支持 GCM/CCM。

**帮助中需要先理解的参数**：

- `-list`：本机帮助描述：List ciphers
- `-ciphers`：本机帮助描述：Alias for -list
- `-e`：本机帮助描述：Encrypt
- `-d`：本机帮助描述：Decrypt
- `-p`：本机帮助描述：Print the iv/key
- `-P`：本机帮助描述：Print the iv/key and exit

<details><summary>展开本机 `-help` 原文</summary>

```text
Usage: enc [options]

General options:
 -help               Display this summary
 -list               List ciphers
 -ciphers            Alias for -list
 -e                  Encrypt
 -d                  Decrypt
 -p                  Print the iv/key
 -P                  Print the iv/key and exit
 -engine val         Use engine, possibly a hardware device

Input options:
 -in infile          Input file
 -k val              Passphrase
 -kfile infile       Read passphrase from file

Output options:
 -out outfile        Output file
 -pass val           Passphrase source
 -v                  Verbose output
 -a                  Base64 encode/decode, depending on encryption flag
 -base64             Same as option -a
 -A                  Used with -[base64|a] to specify base64 buffer as a single line

Encryption options:
 -nopad              Disable standard block padding
 -salt               Use salt in the KDF (default)
 -nosalt             Do not use salt in the KDF
 -debug              Print debug info
 -bufsize val        Buffer size
 -K val              Raw key, in hex
 -S val              Salt, in hex
 -iv val             IV in hex
 -md val             Use specified digest to create a key from the passphrase
 -iter +int          Specify the iteration count and force use of PBKDF2
 -pbkdf2             Use password-based key derivation function 2
 -none               Don't encrypt
 -*                  Any supported cipher

Random state options:
 -rand val           Load the given file(s) into the random number generator
 -writerand outfile  Write random data to the specified file

Provider options:
 -provider-path val  Provider load path (must be before 'provider' argument if required)
 -provider val       Provider to load (can be specified multiple times)
 -propquery val      Property query used when fetching algorithms
```

</details>

## 请求、证书、吊销、容器与信任

### `openssl req`

**帮助命令**：`openssl req -help`。**用法**：`Usage: req [options]`

**作用**：生成/检查 CSR，也可创建自签测试证书。

**参数解读**：`-new` 生成 CSR，`-x509` 改为证书；`-subj`/`-addext` 控制身份与扩展。

**帮助中需要先理解的参数**：

- `-pubkey`：公钥文件；本机帮助描述：Output public key
- `-verify`：选择验签动作或公钥；本机帮助描述：Verify self-signature on the request
- `-new`：本机帮助描述：New request
- `-utf8`：本机帮助描述：Input characters are UTF8 (default ASCII)
- `-text`：本机帮助描述：Text form of request
- `-x509`：本机帮助描述：Output an X.509 certificate structure instead of a cert request

<details><summary>展开本机 `-help` 原文</summary>

```text
Usage: req [options]

General options:
 -help                 Display this summary
 -engine val           Use engine, possibly a hardware device
 -keygen_engine val    Specify engine to be used for key generation operations
 -in infile            X.509 request input file (default stdin)
 -inform PEM|DER       Input format - DER or PEM
 -verify               Verify self-signature on the request

Certificate options:
 -new                  New request
 -config infile        Request template file
 -section val          Config section to use (default "req")
 -utf8                 Input characters are UTF8 (default ASCII)
 -nameopt val          Certificate subject/issuer name printing options
 -reqopt val           Various request text options
 -text                 Text form of request
 -x509                 Output an X.509 certificate structure instead of a cert request
 -CA infile            Issuer cert to use for signing a cert, implies -x509
 -CAkey val            Issuer private key to use with -CA; default is -CA arg
                       (Required by some CA's)
 -subj val             Set or modify subject of request or cert
 -subject              Print the subject of the output request or cert
 -multivalue-rdn       Deprecated; multi-valued RDNs support is always on.
 -days +int            Number of days cert is valid for
 -set_serial val       Serial number to use
 -copy_extensions val  copy extensions from request when using -x509
 -addext val           Additional cert extension key=value pair (may be given more than once)
 -extensions val       Cert extension section (override value in config file)
 -reqexts val          Request extension section (override value in config file)
 -precert              Add a poison extension to the generated cert (implies -new)

Keys and Signing options:
 -key val              Key for signing, and to include unless -in given
 -keyform format       Key file format (ENGINE, other values ignored)
 -pubkey               Output public key
 -keyout outfile       File to write private key to
 -passin val           Private key and certificate password source
 -passout val          Output file pass phrase source
 -newkey val           Generate new key with [<alg>:]<nbits> or <alg>[:<file>] or param:<file>
 -pkeyopt val          Public key options as opt:value
 -sigopt val           Signature parameter in n:v form
 -vfyopt val           Verification parameter in n:v form
 -*                    Any supported digest

Output options:
 -out outfile          Output file
 -outform PEM|DER      Output format - DER or PEM
 -batch                Do not ask anything during request generation
 -verbose              Verbose output
 -noenc                Don't encrypt private keys
 -nodes                Don't encrypt private keys; deprecated
 -noout                Do not output REQ
 -newhdr               Output "NEW" in the header lines
 -modulus              RSA modulus

Random state options:
 -rand val             Load the given file(s) into the random number generator
 -writerand outfile    Write random data to the specified file

Provider options:
 -provider-path val    Provider load path (must be before 'provider' argument if required)
 -provider val         Provider to load (can be specified multiple times)
 -propquery val        Property query used when fetching algorithms
```

</details>

### `openssl x509`

**帮助命令**：`openssl x509 -help`。**用法**：`Usage: x509 [options]`

**作用**：打印、转换、检查或签发 X.509 证书。

**参数解读**：`-noout -subject -issuer -dates` 只展示字段；验证信任应使用 `verify`。

**帮助中需要先理解的参数**：

- `-pubkey`：公钥文件；本机帮助描述：Print the public key in PEM format
- `-new`：本机帮助描述：Generate a certificate from scratch
- `-x509toreq`：本机帮助描述：Output a certification request (rather than a certificate)
- `-req`：本机帮助描述：Input is a CSR file (rather than a certificate)
- `-nocert`：本机帮助描述：No cert output (except for requested printing)
- `-noout`：本机帮助描述：No output (except for requested printing)

<details><summary>展开本机 `-help` 原文</summary>

```text
Usage: x509 [options]

General options:
 -help                      Display this summary
 -in infile                 Certificate input, or CSR input file with -req (default stdin)
 -passin val                Private key and cert file pass-phrase source
 -new                       Generate a certificate from scratch
 -x509toreq                 Output a certification request (rather than a certificate)
 -req                       Input is a CSR file (rather than a certificate)
 -copy_extensions val       copy extensions when converting from CSR to x509 or vice versa
 -inform format             CSR input file format (DER or PEM) - default PEM
 -vfyopt val                CSR verification parameter in n:v form
 -key val                   Key for signing, and to include unless using -force_pubkey
 -signkey val               Same as -key
 -keyform PEM|DER|ENGINE    Key input format (ENGINE, other values ignored)
 -out outfile               Output file - default stdout
 -outform format            Output format (DER or PEM) - default PEM
 -nocert                    No cert output (except for requested printing)
 -noout                     No output (except for requested printing)

Certificate printing options:
 -text                      Print the certificate in text form
 -dateopt val               Datetime format used for printing. (rfc_822/iso_8601). Default is rfc_822.
 -certopt val               Various certificate text printing options
 -fingerprint               Print the certificate fingerprint
 -alias                     Print certificate alias
 -serial                    Print serial number value
 -startdate                 Print the notBefore field
 -enddate                   Print the notAfter field
 -dates                     Print both notBefore and notAfter fields
 -subject                   Print subject DN
 -issuer                    Print issuer DN
 -nameopt val               Certificate subject/issuer name printing options
 -email                     Print email address(es)
 -hash                      Synonym for -subject_hash (for backward compat)
 -subject_hash              Print subject hash value
 -subject_hash_old          Print old-style (MD5) subject hash value
 -issuer_hash               Print issuer hash value
 -issuer_hash_old           Print old-style (MD5) issuer hash value
 -ext val                   Restrict which X.509 extensions to print and/or copy
 -ocspid                    Print OCSP hash values for the subject name and public key
 -ocsp_uri                  Print OCSP Responder URL(s)
 -purpose                   Print out certificate purposes
 -pubkey                    Print the public key in PEM format
 -modulus                   Print the RSA key modulus

Certificate checking options:
 -checkend intmax           Check whether cert expires in the next arg seconds
                            Exit 1 (failure) if so, 0 if not
 -checkhost val             Check certificate matches host
 -checkemail val            Check certificate matches email
 -checkip val               Check certificate matches ipaddr

Certificate output options:
 -set_serial val            Serial number to use, overrides -CAserial
 -next_serial               Increment current certificate serial number
 -days int                  Number of days until newly generated certificate expires - default 30
 -preserve_dates            Preserve existing validity dates
 -subj val                  Set or override certificate subject (and issuer)
 -force_pubkey infile       Place the given key in new certificate
 -clrext                    Do not take over any extensions from the source certificate or request
 -extfile infile            Config file with X509V3 extensions to add
 -extensions val            Section of extfile to use - default: unnamed section
 -sigopt val                Signature parameter, in n:v form
 -badsig                    Corrupt last byte of certificate signature (for test)
 -*                         Any supported digest, used for signing and printing

Micro-CA options:
 -CA infile                 Use the given CA certificate, conflicts with -key
 -CAform PEM|DER            CA cert format (PEM/DER/P12); has no effect
 -CAkey val                 The corresponding CA key; default is -CA arg
 -CAkeyform PEM|DER|ENGINE  CA key format (ENGINE, other values ignored)
 -CAserial val              File that keeps track of CA-generated serial number
 -CAcreateserial            Create CA serial number file if it does not exist

Certificate trust output options:
 -trustout                  Mark certificate PEM output as trusted
 -setalias val              Set certificate alias (nickname)
 -clrtrust                  Clear all trusted purposes
 -addtrust val              Trust certificate for a given purpose
 -clrreject                 Clears all the prohibited or rejected uses of the certificate
 -addreject val             Reject certificate for a given purpose

Random state options:
 -rand val                  Load the given file(s) into the random number generator
 -writerand outfile         Write random data to the specified file
 -engine val                Use engine, possibly a hardware device

Provider options:
 -provider-path val         Provider load path (must be before 'provider' argument if required)
 -provider val              Provider to load (can be specified multiple times)
 -propquery val             Property query used when fetching algorithms
```

</details>

### `openssl verify`

**帮助命令**：`openssl verify -help`。**用法**：`Usage: verify [options] [cert...]`

**作用**：根据可信锚、用途与目标名称验证证书链。

**参数解读**：`-CAfile` 是可信根；`-verify_hostname` 用于目标名称校验，不能只看链通过。

**帮助中需要先理解的参数**：

- `-verbose`：本机帮助描述：Print extra information about the operations being performed.
- `-no-CAfile`：本机帮助描述：Do not load the default trusted certificates file
- `-no-CApath`：本机帮助描述：Do not load trusted certificates from the default directory
- `-no-CAstore`：本机帮助描述：Do not load trusted certificates from the default certificates store
- `-crl_download`：本机帮助描述：Try downloading CRL information for certificates via their CDP entries
- `-show_chain`：本机帮助描述：Display information about the certificate chain

<details><summary>展开本机 `-help` 原文</summary>

```text
Usage: verify [options] [cert...]

General options:
 -help                 Display this summary
 -engine val           Use engine, possibly a hardware device
 -verbose              Print extra information about the operations being performed.
 -nameopt val          Certificate subject/issuer name printing options

Certificate chain options:
 -trusted infile       A file of trusted certificates
 -CAfile infile        A file of trusted certificates
 -CApath dir           A directory of files with trusted certificates
 -CAstore uri          URI to a store of trusted certificates
 -no-CAfile            Do not load the default trusted certificates file
 -no-CApath            Do not load trusted certificates from the default directory
 -no-CAstore           Do not load trusted certificates from the default certificates store
 -untrusted infile     A file of untrusted certificates
 -CRLfile infile       File containing one or more CRL's (in PEM format) to load
 -crl_download         Try downloading CRL information for certificates via their CDP entries
 -show_chain           Display information about the certificate chain

Validation options:
 -policy val           adds policy to the acceptable policy set
 -purpose val          certificate chain purpose
 -verify_name val      verification policy name
 -verify_depth int     chain depth limit
 -auth_level int       chain authentication security level
 -attime intmax        verification epoch time
 -verify_hostname val  expected peer hostname
 -verify_email val     expected peer email
 -verify_ip val        expected peer IP address
 -ignore_critical      permit unhandled critical extensions
 -issuer_checks        (deprecated)
 -crl_check            check leaf certificate revocation
 -crl_check_all        check full chain revocation
 -policy_check         perform rfc5280 policy checks
 -explicit_policy      set policy variable require-explicit-policy
 -inhibit_any          set policy variable inhibit-any-policy
 -inhibit_map          set policy variable inhibit-policy-mapping
 -x509_strict          disable certificate compatibility work-arounds
 -extended_crl         enable extended CRL features
 -use_deltas           use delta CRLs
 -policy_print         print policy processing diagnostics
 -check_ss_sig         check root CA self-signatures
 -trusted_first        search trust store first (default)
 -suiteB_128_only      Suite B 128-bit-only mode
 -suiteB_128           Suite B 128-bit mode allowing 192-bit algorithms
 -suiteB_192           Suite B 192-bit-only mode
 -partial_chain        accept chains anchored by intermediate trust-store CAs
 -no_alt_chains        (deprecated)
 -no_check_time        ignore certificate validity time
 -allow_proxy_certs    allow the use of proxy certificates
 -vfyopt val           Verification parameter in n:v form

Provider options:
 -provider-path val    Provider load path (must be before 'provider' argument if required)
 -provider val         Provider to load (can be specified multiple times)
 -propquery val        Property query used when fetching algorithms

Parameters:
 cert                  Certificate(s) to verify (optional; stdin used otherwise)

Recognized certificate chain purposes:
  sslclient        SSL client
  sslserver        SSL server
  nssslserver      Netscape SSL server
  smimesign        S/MIME signing
  smimeencrypt     S/MIME encryption
  crlsign          CRL signing
  any              Any Purpose
  ocsphelper       OCSP helper
  timestampsign    Time Stamp signing
Recognized certificate policy names:
  default
  pkcs7
  smime_sign
  ssl_client
  ssl_server
```

</details>

### `openssl ca`

**帮助命令**：`openssl ca -help`。**用法**：`Usage: ca [options] [certreq...]`

**作用**：根据 CA 配置签发证书、处理吊销与证书数据库。

**参数解读**：需要配置文件与受控 CA 数据库，不能把测试签发直接接成无审批工具。

**帮助中需要先理解的参数**：

- `-verbose`：本机帮助描述：Verbose output during processing
- `-infiles`：本机帮助描述：The last argument, requests to process
- `-notext`：本机帮助描述：Do not print the generated certificate
- `-batch`：本机帮助描述：Don't ask questions
- `-msie_hack`：本机帮助描述：msie modifications to handle all Universal Strings
- `-utf8`：本机帮助描述：Input characters are UTF8; default ASCII

<details><summary>展开本机 `-help` 原文</summary>

```text
Usage: ca [options] [certreq...]

General options:
 -help                   Display this summary
 -verbose                Verbose output during processing
 -outdir dir             Where to put output cert
 -in infile              The input cert request(s)
 -inform PEM|DER         CSR input format (DER or PEM); default PEM
 -infiles                The last argument, requests to process
 -out outfile            Where to put the output file(s)
 -dateopt val            Datetime format used for printing. (rfc_822/iso_8601). Default is rfc_822.
 -notext                 Do not print the generated certificate
 -batch                  Don't ask questions
 -msie_hack              msie modifications to handle all Universal Strings
 -ss_cert infile         File contains a self signed cert to sign
 -spkac infile           File contains DN and signed public key and challenge
 -engine val             Use engine, possibly a hardware device

Configuration options:
 -config val             A config file
 -name val               The particular CA definition to use
 -section val            An alias for -name
 -policy val             The CA 'policy' to support

Certificate options:
 -subj val               Use arg instead of request's subject
 -utf8                   Input characters are UTF8; default ASCII
 -create_serial          If reading serial fails, create a new random serial
 -rand_serial            Always create a random serial; do not store it
 -multivalue-rdn         Deprecated; multi-valued RDNs support is always on.
 -startdate val          Cert notBefore, YYMMDDHHMMSSZ
 -enddate val            YYMMDDHHMMSSZ cert notAfter (overrides -days)
 -days +int              Number of days to certify the cert for
 -extensions val         Extension section (override value in config file)
 -extfile infile         Configuration file with X509v3 extensions to add
 -preserveDN             Don't re-order the DN
 -noemailDN              Don't add the EMAIL field to the DN

Signing options:
 -md val                 Digest to use, such as sha256
 -keyfile val            The CA private key
 -keyform format         Private key file format (ENGINE, other values ignored)
 -passin val             Key and cert input file pass phrase source
 -key val                Key to decrypt the private key or cert files if encrypted. Better use -passin
 -cert infile            The CA cert
 -certform PEM|DER       Certificate input format (DER/PEM/P12); has no effect
 -selfsign               Sign a cert with the key associated with it
 -sigopt val             Signature parameter in n:v form
 -vfyopt val             Verification parameter in n:v form

Revocation options:
 -gencrl                 Generate a new CRL
 -valid val              Add a Valid(not-revoked) DB entry about a cert (given in file)
 -status val             Shows cert status given the serial number
 -updatedb               Updates db for expired cert
 -crlexts val            CRL extension section (override value in config file)
 -crl_reason val         revocation reason
 -crl_hold val           the hold instruction, an OID. Sets revocation reason to certificateHold
 -crl_compromise val     sets compromise time to val and the revocation reason to keyCompromise
 -crl_CA_compromise val  sets compromise time to val and the revocation reason to CACompromise
 -crl_lastupdate val     Sets the CRL lastUpdate time to val (YYMMDDHHMMSSZ or YYYYMMDDHHMMSSZ)
 -crl_nextupdate val     Sets the CRL nextUpdate time to val (YYMMDDHHMMSSZ or YYYYMMDDHHMMSSZ)
 -crldays +int           Days until the next CRL is due
 -crlhours +int          Hours until the next CRL is due
 -crlsec +int            Seconds until the next CRL is due
 -revoke infile          Revoke a cert (given in file)

Random state options:
 -rand val               Load the given file(s) into the random number generator
 -writerand outfile      Write random data to the specified file

Provider options:
 -provider-path val      Provider load path (must be before 'provider' argument if required)
 -provider val           Provider to load (can be specified multiple times)
 -propquery val          Property query used when fetching algorithms

Parameters:
 certreq                 Certificate requests to be signed (optional)
```

</details>

### `openssl crl`

**帮助命令**：`openssl crl -help`。**用法**：`Usage: crl [options]`

**作用**：解析、转换与检查证书吊销列表。

**帮助中需要先理解的参数**：

- `-verify`：选择验签动作或公钥；本机帮助描述：Verify CRL signature
- `-text`：本机帮助描述：Print out a text format version
- `-hash`：本机帮助描述：Print hash value
- `-hash_old`：本机帮助描述：Print old-style (MD5) hash value
- `-issuer`：本机帮助描述：Print issuer DN
- `-lastupdate`：本机帮助描述：Set lastUpdate field

<details><summary>展开本机 `-help` 原文</summary>

```text
Usage: crl [options]

General options:
 -help               Display this summary
 -verify             Verify CRL signature

Input options:
 -in infile          Input file - default stdin
 -inform PEM|DER     CRL input format (DER or PEM); has no effect
 -key infile         CRL signing Private key to use
 -keyform PEM|DER    Private key file format (DER/PEM/P12); has no effect

Output options:
 -out outfile        output file - default stdout
 -outform PEM|DER    Output format - default PEM
 -dateopt val        Datetime format used for printing. (rfc_822/iso_8601). Default is rfc_822.
 -text               Print out a text format version
 -hash               Print hash value
 -hash_old           Print old-style (MD5) hash value
 -nameopt val        Certificate subject/issuer name printing options
 -*                  Any supported digest

CRL options:
 -issuer             Print issuer DN
 -lastupdate         Set lastUpdate field
 -nextupdate         Set nextUpdate field
 -noout              No CRL output
 -fingerprint        Print the crl fingerprint
 -crlnumber          Print CRL number
 -badsig             Corrupt last byte of loaded CRL signature (for test)
 -gendelta infile    Other CRL to compare/diff to the Input one

Certificate options:
 -CApath dir         Verify CRL using certificates in dir
 -CAfile infile      Verify CRL using certificates in file name
 -CAstore uri        Verify CRL using certificates in store URI
 -no-CAfile          Do not load the default certificates file
 -no-CApath          Do not load certificates from the default certificates directory
 -no-CAstore         Do not load certificates from the default certificates store

Provider options:
 -provider-path val  Provider load path (must be before 'provider' argument if required)
 -provider val       Provider to load (can be specified multiple times)
 -propquery val      Property query used when fetching algorithms
```

</details>

### `openssl crl2pkcs7`

**帮助命令**：`openssl crl2pkcs7 -help`。**用法**：`Usage: crl2pkcs7 [options]`

**作用**：把证书/CRL 装入 PKCS#7 容器。

**帮助中需要先理解的参数**：

- `-nocrl`：本机帮助描述：No crl to load, just certs from '-certfile'

<details><summary>展开本机 `-help` 原文</summary>

```text
Usage: crl2pkcs7 [options]

General options:
 -help               Display this summary

Input options:
 -in infile          Input file
 -inform PEM|DER     Input format - DER or PEM
 -nocrl              No crl to load, just certs from '-certfile'
 -certfile infile    File of chain of certs to a trusted CA; can be repeated

Output options:
 -out outfile        Output file
 -outform PEM|DER    Output format - DER or PEM

Provider options:
 -provider-path val  Provider load path (must be before 'provider' argument if required)
 -provider val       Provider to load (can be specified multiple times)
 -propquery val      Property query used when fetching algorithms
```

</details>

### `openssl pkcs7`

**帮助命令**：`openssl pkcs7 -help`。**用法**：`Usage: pkcs7 [options]`

**作用**：解析、转换或打印 PKCS#7 容器。

**帮助中需要先理解的参数**：

- `-noout`：本机帮助描述：Don't output encoded data
- `-text`：本机帮助描述：Print full details of certificates
- `-print`：本机帮助描述：Print out all fields of the PKCS7 structure
- `-print_certs`：本机帮助描述：Print_certs  print any certs or crl in the input

<details><summary>展开本机 `-help` 原文</summary>

```text
Usage: pkcs7 [options]

General options:
 -help               Display this summary
 -engine val         Use engine, possibly a hardware device

Input options:
 -in infile          Input file
 -inform PEM|DER     Input format - DER or PEM

Output options:
 -outform PEM|DER    Output format - DER or PEM
 -out outfile        Output file
 -noout              Don't output encoded data
 -text               Print full details of certificates
 -print              Print out all fields of the PKCS7 structure
 -print_certs        Print_certs  print any certs or crl in the input

Provider options:
 -provider-path val  Provider load path (must be before 'provider' argument if required)
 -provider val       Provider to load (can be specified multiple times)
 -propquery val      Property query used when fetching algorithms
```

</details>

### `openssl pkcs8`

**帮助命令**：`openssl pkcs8 -help`。**用法**：`Usage: pkcs8 [options]`

**作用**：转换或保护 PKCS#8 私钥。

**帮助中需要先理解的参数**：

- `-nocrypt`：本机帮助描述：Use or expect unencrypted private key
- `-topk8`：本机帮助描述：Output PKCS8 file
- `-traditional`：本机帮助描述：use traditional format private key
- `-noiter`：本机帮助描述：Use 1 as iteration count
- `-scrypt`：本机帮助描述：Use scrypt algorithm

<details><summary>展开本机 `-help` 原文</summary>

```text
Usage: pkcs8 [options]

General options:
 -help               Display this summary
 -engine val         Use engine, possibly a hardware device
 -v1 val             Use PKCS#5 v1.5 and cipher
 -v2 val             Use PKCS#5 v2.0 and cipher
 -v2prf val          Set the PRF algorithm to use with PKCS#5 v2.0

Input options:
 -in infile          Input file
 -inform PEM|DER     Input format (DER or PEM)
 -passin val         Input file pass phrase source
 -nocrypt            Use or expect unencrypted private key

Output options:
 -out outfile        Output file
 -outform PEM|DER    Output format (DER or PEM)
 -topk8              Output PKCS8 file
 -passout val        Output file pass phrase source
 -traditional        use traditional format private key
 -iter +int          Specify the iteration count
 -noiter             Use 1 as iteration count

Scrypt options:
 -scrypt             Use scrypt algorithm
 -scrypt_N val       Set scrypt N parameter
 -scrypt_r val       Set scrypt r parameter
 -scrypt_p val       Set scrypt p parameter

Random state options:
 -rand val           Load the given file(s) into the random number generator
 -writerand outfile  Write random data to the specified file

Provider options:
 -provider-path val  Provider load path (must be before 'provider' argument if required)
 -provider val       Provider to load (can be specified multiple times)
 -propquery val      Property query used when fetching algorithms
```

</details>

### `openssl pkcs12`

**帮助命令**：`openssl pkcs12 -help`。**用法**：`Usage: pkcs12 [options]`

**作用**：导入或导出 PKCS#12 密钥/证书容器。

**参数解读**：`-export` 创建容器；`-passin`/`-passout` 区分输入和输出口令。

**帮助中需要先理解的参数**：

- `-twopass`：本机帮助描述：Separate MAC, encryption passwords
- `-nokeys`：本机帮助描述：Don't output private keys
- `-nocerts`：本机帮助描述：Don't output certificates
- `-noout`：本机帮助描述：Don't output anything, just verify PKCS#12 input
- `-legacy`：本机帮助描述：Use legacy encryption: 3DES_CBC for keys, RC2_CBC for certs
- `-info`：本机帮助描述：Print info about PKCS#12 structure

<details><summary>展开本机 `-help` 原文</summary>

```text
Usage: pkcs12 [options]

General options:
 -help               Display this summary
 -in infile          Input file
 -out outfile        Output file
 -passin val         Input file pass phrase source
 -passout val        Output file pass phrase source
 -password val       Set PKCS#12 import/export password source
 -twopass            Separate MAC, encryption passwords
 -nokeys             Don't output private keys
 -nocerts            Don't output certificates
 -noout              Don't output anything, just verify PKCS#12 input
 -legacy             Use legacy encryption: 3DES_CBC for keys, RC2_CBC for certs
 -engine val         Use engine, possibly a hardware device

Provider options:
 -provider-path val  Provider load path (must be before 'provider' argument if required)
 -provider val       Provider to load (can be specified multiple times)
 -propquery val      Property query used when fetching algorithms

Random state options:
 -rand val           Load the given file(s) into the random number generator
 -writerand outfile  Write random data to the specified file

PKCS#12 import (parsing PKCS#12) options:
 -info               Print info about PKCS#12 structure
 -nomacver           Don't verify integrity MAC
 -clcerts            Only output client certificates
 -cacerts            Only output CA certificates
 -*                  Any supported cipher for output encryption
 -noenc              Don't encrypt private keys
 -nodes              Don't encrypt private keys; deprecated

PKCS#12 output (export) options:
 -export             Create PKCS12 file
 -inkey val          Private key, else read from -in input file
 -certfile infile    Extra certificates for PKCS12 output
 -passcerts val      Certificate file pass phrase source
 -chain              Build and add certificate chain for EE cert,
                     which is the 1st cert from -in matching the private key (if given)
 -untrusted infile   Untrusted certificates for chain building
 -CAfile infile      PEM-format file of CA's
 -CApath dir         PEM-format directory of CA's
 -CAstore uri        URI to store of CA's
 -no-CAfile          Do not load the default certificates file
 -no-CApath          Do not load certificates from the default certificates directory
 -no-CAstore         Do not load certificates from the default certificates store
 -name val           Use name as friendly name
 -caname val         Use name as CA friendly name (can be repeated)
 -CSP val            Microsoft CSP name
 -LMK                Add local machine keyset attribute to private key
 -keyex              Set key type to MS key exchange
 -keysig             Set key type to MS key signature
 -keypbe val         Private key PBE algorithm (default AES-256 CBC)
 -certpbe val        Certificate PBE algorithm (default PBES2 with PBKDF2 and AES-256 CBC)
 -descert            Encrypt output with 3DES (default PBES2 with PBKDF2 and AES-256 CBC)
 -macalg val         Digest algorithm to use in MAC (default SHA1)
 -iter +int          Specify the iteration count for encryption and MAC
 -noiter             Don't use encryption iteration
 -nomaciter          Don't use MAC iteration)
 -maciter            Unused, kept for backwards compatibility
 -nomac              Don't generate MAC
```

</details>

### `openssl rehash`

**帮助命令**：`openssl rehash -help`。**用法**：`Usage: rehash [options] [directory...]`

**作用**：为受信任证书目录建立哈希链接。

**帮助中需要先理解的参数**：

- `-h`：本机帮助描述：Display this summary
- `-compat`：本机帮助描述：Create both new- and old-style hash links
- `-old`：本机帮助描述：Use old-style hash to generate links
- `-n`：本机帮助描述：Do not remove existing links
- `-v`：本机帮助描述：Verbose output

<details><summary>展开本机 `-help` 原文</summary>

```text
Usage: rehash [options] [directory...]

General options:
 -help               Display this summary
 -h                  Display this summary
 -compat             Create both new- and old-style hash links
 -old                Use old-style hash to generate links
 -n                  Do not remove existing links

Output options:
 -v                  Verbose output

Provider options:
 -provider-path val  Provider load path (must be before 'provider' argument if required)
 -provider val       Provider to load (can be specified multiple times)
 -propquery val      Property query used when fetching algorithms

Parameters:
 directory           One or more directories to process (optional)
```

</details>

### `openssl ocsp`

**帮助命令**：`openssl ocsp -help`。**用法**：`Usage: ocsp [options]`

**作用**：发起或响应 OCSP 证书状态请求。

**参数解读**：请求/响应两侧需要证书与可信链，帮助信息不证明在线服务可用。

**帮助中需要先理解的参数**：

- `-ignore_err`：本机帮助描述：Ignore error on OCSP request or response and continue running
- `-no-CAfile`：本机帮助描述：Do not load the default certificates file
- `-no-CApath`：本机帮助描述：Do not load certificates from the default certificates directory
- `-no-CAstore`：本机帮助描述：Do not load certificates from the default certificates store
- `-resp_no_certs`：本机帮助描述：Don't include any certificates in response
- `-no_certs`：本机帮助描述：Don't include any certificates in signed request

<details><summary>展开本机 `-help` 原文</summary>

```text
Usage: ocsp [options]

General options:
 -help                   Display this summary
 -ignore_err             Ignore error on OCSP request or response and continue running
 -CAfile infile          Trusted certificates file
 -CApath infile          Trusted certificates directory
 -CAstore uri            Trusted certificates store URI
 -no-CAfile              Do not load the default certificates file
 -no-CApath              Do not load certificates from the default certificates directory
 -no-CAstore             Do not load certificates from the default certificates store

Responder options:
 -timeout +int           Connection timeout (in seconds) to the OCSP responder
 -resp_no_certs          Don't include any certificates in response
 -multi +int             run multiple responder processes
 -no_certs               Don't include any certificates in signed request
 -badsig                 Corrupt last byte of loaded OSCP response signature (for test)
 -CA infile              CA certificate
 -nmin +int              Number of minutes before next update
 -nrequest +int          Number of requests to accept (default unlimited)
 -reqin val              File with the DER-encoded request
 -signer infile          Certificate to sign OCSP request with
 -sign_other infile      Additional certificates to include in signed request
 -index infile           Certificate status index file
 -ndays +int             Number of days before next update
 -rsigner infile         Responder certificate to sign responses with
 -rkey infile            Responder key to sign responses with
 -passin val             Responder key pass phrase source
 -rother infile          Other certificates to include in response
 -rmd val                Digest Algorithm to use in signature of OCSP response
 -rsigopt val            OCSP response signature parameter in n:v form
 -header val             key=value header to add
 -rcid val               Use specified algorithm for cert id in response
 -*                      Any supported digest algorithm (sha1,sha256, ... )

Client options:
 -url val                Responder URL
 -host val               TCP/IP hostname:port to connect to
 -port nonneg            Port to run responder on
 -path val               Path to use in OCSP request
 -proxy val              [http[s]://]host[:port][/path] of HTTP(S) proxy to use; path is ignored
 -no_proxy val           List of addresses of servers not to use HTTP(S) proxy for
                         Default from environment variable 'no_proxy', else 'NO_PROXY', else none
 -out outfile            Output filename
 -noverify               Don't verify response at all
 -nonce                  Add OCSP nonce to request
 -no_nonce               Don't add OCSP nonce to request
 -no_signature_verify    Don't check signature on response
 -resp_key_id            Identify response by signing certificate key ID
 -no_cert_verify         Don't check signing certificate
 -text                   Print text form of request and response
 -req_text               Print text form of request
 -resp_text              Print text form of response
 -no_chain               Don't chain verify response
 -no_cert_checks         Don't do additional checks on signing certificate
 -no_explicit            Do not explicitly check the chain, just verify the root
 -trust_other            Don't verify additional certificates
 -no_intern              Don't search certificates contained in response for signer
 -respin val             File with the DER-encoded response
 -VAfile infile          Validator certificates file
 -verify_other infile    Additional certificates to search for signer
 -cert infile            Certificate to check
 -serial val             Serial number to check
 -validity_period ulong  Maximum validity discrepancy in seconds
 -signkey val            Private key to sign OCSP request with
 -reqout val             Output file for the DER-encoded request
 -respout val            Output file for the DER-encoded response
 -issuer infile          Issuer certificate
 -status_age +int        Maximum status age in seconds

Validation options:
 -policy val             adds policy to the acceptable policy set
 -purpose val            certificate chain purpose
 -verify_name val        verification policy name
 -verify_depth int       chain depth limit
 -auth_level int         chain authentication security level
 -attime intmax          verification epoch time
 -verify_hostname val    expected peer hostname
 -verify_email val       expected peer email
 -verify_ip val          expected peer IP address
 -ignore_critical        permit unhandled critical extensions
 -issuer_checks          (deprecated)
 -crl_check              check leaf certificate revocation
 -crl_check_all          check full chain revocation
 -policy_check           perform rfc5280 policy checks
 -explicit_policy        set policy variable require-explicit-policy
 -inhibit_any            set policy variable inhibit-any-policy
 -inhibit_map            set policy variable inhibit-policy-mapping
 -x509_strict            disable certificate compatibility work-arounds
 -extended_crl           enable extended CRL features
 -use_deltas             use delta CRLs
 -policy_print           print policy processing diagnostics
 -check_ss_sig           check root CA self-signatures
 -trusted_first          search trust store first (default)
 -suiteB_128_only        Suite B 128-bit-only mode
 -suiteB_128             Suite B 128-bit mode allowing 192-bit algorithms
 -suiteB_192             Suite B 192-bit-only mode
 -partial_chain          accept chains anchored by intermediate trust-store CAs
 -no_alt_chains          (deprecated)
 -no_check_time          ignore certificate validity time
 -allow_proxy_certs      allow the use of proxy certificates

Provider options:
 -provider-path val      Provider load path (must be before 'provider' argument if required)
 -provider val           Provider to load (can be specified multiple times)
 -propquery val          Property query used when fetching algorithms
```

</details>

### `openssl ts`

**帮助命令**：`openssl ts -help`。**用法**：`Usage: ts [options]`

**作用**：产生或验证时间戳请求与响应。

**帮助中需要先理解的参数**：

- `-cert`：证书文件；本机帮助描述：Put cert request into query
- `-verify`：选择验签动作或公钥；本机帮助描述：Verify a TS response
- `-token_in`：本机帮助描述：Input is a PKCS#7 file
- `-token_out`：本机帮助描述：Output is a PKCS#7 file
- `-query`：本机帮助描述：Generate a TS query
- `-reply`：本机帮助描述：Generate a TS reply

<details><summary>展开本机 `-help` 原文</summary>

```text
Usage: ts [options]

General options:
 -help                 Display this summary
 -config infile        Configuration file
 -section val          Section to use within config file
 -engine val           Use engine, possibly a hardware device
 -inkey val            File with private key for reply
 -signer val           Signer certificate file
 -chain infile         File with signer CA chain
 -CAfile infile        File with trusted CA certs
 -CApath dir           Path to trusted CA files
 -CAstore uri          URI to trusted CA store
 -untrusted infile     Extra untrusted certs
 -token_in             Input is a PKCS#7 file
 -token_out            Output is a PKCS#7 file
 -passin val           Input file pass phrase source
 -*                    Any supported digest

Query options:
 -query                Generate a TS query
 -data infile          File to hash
 -digest val           Digest (as a hex string)
 -queryfile infile     File containing a TS query
 -cert                 Put cert request into query
 -in infile            Input file

Verify options:
 -verify               Verify a TS response
 -reply                Generate a TS reply
 -tspolicy val         Policy OID to use
 -no_nonce             Do not include a nonce
 -out outfile          Output file
 -text                 Output text (not DER)

Random state options:
 -rand val             Load the given file(s) into the random number generator
 -writerand outfile    Write random data to the specified file

Validation options:
 -policy val           adds policy to the acceptable policy set
 -purpose val          certificate chain purpose
 -verify_name val      verification policy name
 -verify_depth int     chain depth limit
 -auth_level int       chain authentication security level
 -attime intmax        verification epoch time
 -verify_hostname val  expected peer hostname
 -verify_email val     expected peer email
 -verify_ip val        expected peer IP address
 -ignore_critical      permit unhandled critical extensions
 -issuer_checks        (deprecated)
 -crl_check            check leaf certificate revocation
 -crl_check_all        check full chain revocation
 -policy_check         perform rfc5280 policy checks
 -explicit_policy      set policy variable require-explicit-policy
 -inhibit_any          set policy variable inhibit-any-policy
 -inhibit_map          set policy variable inhibit-policy-mapping
 -x509_strict          disable certificate compatibility work-arounds
 -extended_crl         enable extended CRL features
 -use_deltas           use delta CRLs
 -policy_print         print policy processing diagnostics
 -check_ss_sig         check root CA self-signatures
 -trusted_first        search trust store first (default)
 -suiteB_128_only      Suite B 128-bit-only mode
 -suiteB_128           Suite B 128-bit mode allowing 192-bit algorithms
 -suiteB_192           Suite B 192-bit-only mode
 -partial_chain        accept chains anchored by intermediate trust-store CAs
 -no_alt_chains        (deprecated)
 -no_check_time        ignore certificate validity time
 -allow_proxy_certs    allow the use of proxy certificates

Provider options:
 -provider-path val    Provider load path (must be before 'provider' argument if required)
 -provider val         Provider to load (can be specified multiple times)
 -propquery val        Property query used when fetching algorithms

Typical uses:
 openssl ts -query [-rand file...] [-config file] [-data file]
    [-digest hexstring] [-tspolicy oid] [-no_nonce] [-cert]
    [-in file] [-out file] [-text]

 openssl ts -reply [-config file] [-section tsa_section]
    [-queryfile file] [-passin password]
    [-signer tsa_cert.pem] [-inkey private_key.pem]
    [-chain certs_file.pem] [-tspolicy oid]
    [-in file] [-token_in] [-out file] [-token_out]
    [-text] [-engine id]

 openssl ts -verify -CApath dir -CAfile root-cert.pem -CAstore uri
   -untrusted extra-certs.pem [-data file] [-digest hexstring]
    [-queryfile request.tsq] -in response.tsr [-token_in] ...
```

</details>

### `openssl spkac`

**帮助命令**：`openssl spkac -help`。**用法**：`Usage: spkac [options]`

**作用**：处理 SignedPublicKeyAndChallenge 旧格式。

**帮助中需要先理解的参数**：

- `-pubkey`：公钥文件；本机帮助描述：Output public key
- `-verify`：选择验签动作或公钥；本机帮助描述：Verify SPKAC signature
- `-noout`：本机帮助描述：Don't print SPKAC

<details><summary>展开本机 `-help` 原文</summary>

```text
Usage: spkac [options]

General options:
 -help               Display this summary
 -spksect val        Specify the name of an SPKAC-dedicated section of configuration
 -engine val         Use engine, possibly a hardware device

Input options:
 -in infile          Input file
 -key infile         Create SPKAC using private key
 -keyform format     Private key file format (ENGINE, other values ignored)
 -passin val         Input file pass phrase source
 -challenge val      Challenge string
 -spkac val          Alternative SPKAC name

Output options:
 -digest val         Sign new SPKAC with the specified digest (default: MD5)
 -out outfile        Output file
 -noout              Don't print SPKAC
 -pubkey             Output public key
 -verify             Verify SPKAC signature

Provider options:
 -provider-path val  Provider load path (must be before 'provider' argument if required)
 -provider val       Provider to load (can be specified multiple times)
 -propquery val      Property query used when fetching algorithms
```

</details>

### `openssl nseq`

**帮助命令**：`openssl nseq -help`。**用法**：`Usage: nseq [options]`

**作用**：处理 Netscape 证书序列格式。

**帮助中需要先理解的参数**：

- `-toseq`：本机帮助描述：Output NS Sequence file

<details><summary>展开本机 `-help` 原文</summary>

```text
Usage: nseq [options]

General options:
 -help               Display this summary

Input options:
 -in infile          Input file

Output options:
 -toseq              Output NS Sequence file
 -out outfile        Output file

Provider options:
 -provider-path val  Provider load path (must be before 'provider' argument if required)
 -provider val       Provider to load (can be specified multiple times)
 -propquery val      Property query used when fetching algorithms
```

</details>

### `openssl storeutl`

**帮助命令**：`openssl storeutl -help`。**用法**：`Usage: storeutl [options] uri`

**作用**：从 URI 或存储后端读取密钥、证书等对象。

**帮助中需要先理解的参数**：

- `-certs`：本机帮助描述：Search for certificates only
- `-keys`：本机帮助描述：Search for keys only
- `-crls`：本机帮助描述：Search for CRLs only
- `-r`：本机帮助描述：Recurse through names
- `-text`：本机帮助描述：Print a text form of the objects
- `-noout`：本机帮助描述：No PEM output, just status

<details><summary>展开本机 `-help` 原文</summary>

```text
Usage: storeutl [options] uri

General options:
 -help               Display this summary
 -*                  Any supported digest
 -engine val         Use engine, possibly a hardware device

Search options:
 -certs              Search for certificates only
 -keys               Search for keys only
 -crls               Search for CRLs only
 -subject val        Search by subject
 -issuer val         Search by issuer and serial, issuer name
 -serial val         Search by issuer and serial, serial number
 -fingerprint val    Search by public key fingerprint, given in hex
 -alias val          Search by alias
 -r                  Recurse through names

Input options:
 -passin val         Input file pass phrase source

Output options:
 -out outfile        Output file - default stdout
 -text               Print a text form of the objects
 -noout              No PEM output, just status

Provider options:
 -provider-path val  Provider load path (must be before 'provider' argument if required)
 -provider val       Provider to load (can be specified multiple times)
 -propquery val      Property query used when fetching algorithms

Parameters:
 uri                 URI of the store object
```

</details>

### `openssl cmp`

**帮助命令**：`openssl cmp -help`。**用法**：`Usage: cmp [options]`

**作用**：运行证书管理协议 CMP 客户端，需服务器与受信任配置。

**帮助中需要先理解的参数**：

- `-san_nodefault`：本机帮助描述：Do not take default SANs from reference certificate (see -oldcert)
- `-policy_oids_critical`：本机帮助描述：Flag the policy OID(s) given with -policy_oids as critical
- `-implicit_confirm`：本机帮助描述：Request implicit confirmation of newly enrolled certificates
- `-disable_confirm`：本机帮助描述：Do not confirm newly enrolled certificate w/o requesting implicit
- `-ignore_keyusage`：本机帮助描述：Ignore CMP signer cert key usage, else 'digitalSignature' must be allowed
- `-unprotected_errors`：本机帮助描述：Accept missing or invalid protection of regular error messages and negative

<details><summary>展开本机 `-help` 原文</summary>

```text
cmp_main:../apps/cmp.c:2751:CMP info: using section(s) 'cmp' of OpenSSL configuration file '/usr/lib/ssl/openssl.cnf'
cmp_main:../apps/cmp.c:2759:CMP info: no [cmp] section found in config file '/usr/lib/ssl/openssl.cnf'; will thus use just [default] and unnamed section if present

Usage: cmp [options]
Valid options are:
 -help                  Display this summary
 -config val            Configuration file to use. "" = none. Default from env variable OPENSSL_CONF
 -section val           Section(s) in config file to get options from. "" = 'default'. Default 'cmp'
 -verbosity nonneg      Log level; 3=ERR, 4=WARN, 6=INFO, 7=DEBUG, 8=TRACE. Default 6 = INFO

Generic message options:
 -cmd val               CMP request to send: ir/cr/kur/p10cr/rr/genm
 -infotype val          InfoType name for requesting specific info in genm, e.g. 'signKeyPairTypes'
 -geninfo val           generalInfo integer values to place in request PKIHeader with given OID
                        specified in the form <OID>:int:<n>, e.g. "1.2.3.4:int:56789"

Certificate enrollment options:
 -newkey val            Private or public key for the requested cert. Default: CSR key or client key
 -newkeypass val        New private key pass phrase source
 -subject val           Distinguished Name (DN) of subject to use in the requested cert template
                        For kur, default is subject of -csr arg or reference cert (see -oldcert)
                        this default is used for ir and cr only if no Subject Alt Names are set
 -issuer val            DN of the issuer to place in the requested certificate template
                        also used as recipient if neither -recipient nor -srvcert are given
 -days nonneg           Requested validity time of the new certificate in number of days
 -reqexts val           Name of config file section defining certificate request extensions.
                        Augments or replaces any extensions contained CSR given with -csr
 -sans val              Subject Alt Names (IPADDR/DNS/URI) to add as (critical) cert req extension
 -san_nodefault         Do not take default SANs from reference certificate (see -oldcert)
 -policies val          Name of config file section defining policies certificate request extension
 -policy_oids val       Policy OID(s) to add as policies certificate request extension
 -policy_oids_critical  Flag the policy OID(s) given with -policy_oids as critical
 -popo int              Proof-of-Possession (POPO) method to use for ir/cr/kur where
                        -1 = NONE, 0 = RAVERIFIED, 1 = SIGNATURE (default), 2 = KEYENC
 -csr val               PKCS#10 CSR file in PEM or DER format to convert or to use in p10cr
 -out_trusted val       Certificates to trust when verifying newly enrolled certificates
 -implicit_confirm      Request implicit confirmation of newly enrolled certificates
 -disable_confirm       Do not confirm newly enrolled certificate w/o requesting implicit
                        confirmation. WARNING: This leads to behavior violating RFC 4210
 -certout val           File to save newly enrolled certificate
 -chainout val          File to save the chain of newly enrolled certificate

Certificate enrollment and revocation options:
 -oldcert val           Certificate to be updated (defaulting to -cert) or to be revoked in rr;
                        also used as reference (defaulting to -cert) for subject DN and SANs.
                        Issuer is used as recipient unless -recipient, -srvcert, or -issuer given
 -revreason int         Reason code to include in revocation request (rr); possible values:
                        0..6, 8..10 (see RFC5280, 5.3.1) or -1. Default -1 = none included

Message transfer options:
 -server val            [http[s]://]address[:port][/path] of CMP server. Default port 80 or 443.
                        address may be a DNS name or an IP address; path can be overridden by -path
 -proxy val             [http[s]://]address[:port][/path] of HTTP(S) proxy to use; path is ignored
 -no_proxy val          List of addresses of servers not to use HTTP(S) proxy for
                        Default from environment variable 'no_proxy', else 'NO_PROXY', else none
 -recipient val         DN of CA. Default: subject of -srvcert, -issuer, issuer of -oldcert or -cert
 -path val              HTTP path (aka CMP alias) at the CMP server. Default from -server, else "/"
 -keep_alive nonneg     Persistent HTTP connections. 0: no, 1 (the default): request, 2: require
 -msg_timeout nonneg    Number of seconds allowed per CMP message round trip, or 0 for infinite
 -total_timeout nonneg  Overall time an enrollment incl. polling may take. Default 0 = infinite

Server authentication options:
 -trusted val           Certificates to trust as chain roots when verifying signed CMP responses
                        unless -srvcert is given
 -untrusted val         Intermediate CA certs for chain construction for CMP/TLS/enrolled certs
 -srvcert val           Server cert to pin and trust directly when verifying signed CMP responses
 -expect_sender val     DN of expected sender of responses. Defaults to subject of -srvcert, if any
 -ignore_keyusage       Ignore CMP signer cert key usage, else 'digitalSignature' must be allowed
 -unprotected_errors    Accept missing or invalid protection of regular error messages and negative
                        certificate responses (ip/cp/kup), revocation responses (rp), and PKIConf
                        WARNING: This setting leads to behavior allowing violation of RFC 4210
 -extracertsout val     File to save extra certificates received in the extraCerts field
 -cacertsout val        File to save CA certificates received in the caPubs field of 'ip' messages

Client authentication options:
 -ref val               Reference value to use as senderKID in case no -cert is given
 -secret val            Prefer PBM (over signatures) for protecting msgs with given password source
 -cert val              Client's CMP signer certificate; its public key must match the -key argument
                        This also used as default reference for subject DN and SANs.
                        Any further certs included are appended to the untrusted certs
 -own_trusted val       Optional certs to verify chain building for own CMP signer cert
 -key val               CMP signer private key, not used when -secret given
 -keypass val           Client private key (and cert and old cert) pass phrase source
 -digest val            Digest to use in message protection and POPO signatures. Default "sha256"
 -mac val               MAC algorithm to use in PBM-based message protection. Default "hmac-sha1"
 -extracerts val        Certificates to append in extraCerts field of outgoing messages.
                        This can be used as the default CMP signer cert chain to include
 -unprotected_requests  Send messages without CMP-level protection

Credentials format options:
 -certform val          Format (PEM or DER) to use when saving a certificate to a file. Default PEM
 -keyform val           Format of the key input (ENGINE, other values ignored)
 -otherpass val         Pass phrase source potentially needed for loading certificates of others
 -engine val            Use crypto engine with given identifier, possibly a hardware device.
                        Engines may also be defined in OpenSSL config file engine section.

Provider options:
 -provider-path val     Provider load path (must be before 'provider' argument if required)
 -provider val          Provider to load (can be specified multiple times)
 -propquery val         Property query used when fetching algorithms

Random state options:
 -rand val              Load the given file(s) into the random number generator
 -writerand outfile     Write random data to the specified file

TLS connection options:
 -tls_used              Enable using TLS (also when other TLS options are not set)
 -tls_cert val          Client's TLS certificate. May include chain to be provided to TLS server
 -tls_key val           Private key for the client's TLS certificate
 -tls_keypass val       Pass phrase source for the client's private TLS key (and TLS cert)
 -tls_extra val         Extra certificates to provide to TLS server during TLS handshake
 -tls_trusted val       Trusted certificates to use for verifying the TLS server certificate;
                        this implies host name validation
 -tls_host val          Address to be checked (rather than -server) during TLS host name validation

Client-side debugging options:
 -batch                 Do not interactively prompt for input when a password is required etc.
 -repeat +int           Invoke the transaction the given positive number of times. Default 1
 -reqin val             Take sequence of CMP requests from file(s)
 -reqin_new_tid         Use fresh transactionID for CMP requests read from -reqin
 -reqout val            Save sequence of CMP requests to file(s)
 -rspin val             Process sequence of CMP responses provided in file(s), skipping server
 -rspout val            Save sequence of CMP responses to file(s)
 -use_mock_srv          Use internal mock server at API level, bypassing socket-based HTTP

Mock server options:
 -port val              Act as HTTP-based mock server listening on given port
 -max_msgs nonneg       max number of messages handled by HTTP mock server. Default: 0 = unlimited
 -srv_ref val           Reference value to use as senderKID of server in case no -srv_cert is given
 -srv_secret val        Password source for server authentication with a pre-shared key (secret)
 -srv_cert val          Certificate of the server
 -srv_key val           Private key used by the server for signing messages
 -srv_keypass val       Server private key (and cert) pass phrase source
 -srv_trusted val       Trusted certificates for client authentication
 -srv_untrusted val     Intermediate certs that may be useful for verifying CMP protection
 -rsp_cert val          Certificate to be returned as mock enrollment result
 -rsp_extracerts val    Extra certificates to be included in mock certification responses
 -rsp_capubs val        CA certificates to be included in mock ip response
 -poll_count nonneg     Number of times the client must poll before receiving a certificate
 -check_after nonneg    The check_after value (time to wait) to include in poll response
 -grant_implicitconf    Grant implicit confirmation of newly enrolled certificate
 -pkistatus nonneg      PKIStatus to be included in server response. Possible values: 0..6
 -failure nonneg        A single failure info bit number to include in server response, 0..26
 -failurebits nonneg    Number representing failure bits to include in server response, 0..2^27 - 1
 -statusstring val      Status string to be included in server response
 -send_error            Force server to reply with error message
 -send_unprotected      Send response messages without CMP-level protection
 -send_unprot_err       In case of negative responses, server shall send unprotected error messages,
                        certificate responses (ip/cp/kup), and revocation responses (rp).
                        WARNING: This setting leads to behavior violating RFC 4210
 -accept_unprotected    Accept missing or invalid protection of requests
 -accept_unprot_err     Accept unprotected error messages from client
 -accept_raverified     Accept RAVERIFIED as proof-of-possession (POPO)

Validation options:
 -policy val            adds policy to the acceptable policy set
 -purpose val           certificate chain purpose
 -verify_name val       verification policy name
 -verify_depth int      chain depth limit
 -auth_level int        chain authentication security level
 -attime intmax         verification epoch time
 -verify_hostname val   expected peer hostname
 -verify_email val      expected peer email
 -verify_ip val         expected peer IP address
 -ignore_critical       permit unhandled critical extensions
 -issuer_checks         (deprecated)
 -crl_check             check leaf certificate revocation
 -crl_check_all         check full chain revocation
 -policy_check          perform rfc5280 policy checks
 -explicit_policy       set policy variable require-explicit-policy
 -inhibit_any           set policy variable inhibit-any-policy
 -inhibit_map           set policy variable inhibit-policy-mapping
 -x509_strict           disable certificate compatibility work-arounds
 -extended_crl          enable extended CRL features
 -use_deltas            use delta CRLs
 -policy_print          print policy processing diagnostics
 -check_ss_sig          check root CA self-signatures
 -trusted_first         search trust store first (default)
 -suiteB_128_only       Suite B 128-bit-only mode
 -suiteB_128            Suite B 128-bit mode allowing 192-bit algorithms
 -suiteB_192            Suite B 192-bit-only mode
 -partial_chain         accept chains anchored by intermediate trust-store CAs
 -no_alt_chains         (deprecated)
 -no_check_time         ignore certificate validity time
 -allow_proxy_certs     allow the use of proxy certificates
```

</details>

## CMS、S/MIME 和 TLS

### `openssl cms`

**帮助命令**：`openssl cms -help`。**用法**：`Usage: cms [options] [cert...]`

**作用**：生成或读取 CMS 加密、签名等容器，需证书或密钥。

**参数解读**：`-encrypt`/`-decrypt`、`-sign`/`-verify` 是不同动作；输入输出格式要明确。

**帮助中需要先理解的参数**：

- `-encrypt`：选择加密动作；本机帮助描述：Encrypt message
- `-decrypt`：选择解密动作；本机帮助描述：Decrypt encrypted message
- `-sign`：选择签名动作或私钥；本机帮助描述：Sign message
- `-verify`：选择验签动作或公钥；本机帮助描述：Verify signed message
- `-resign`：本机帮助描述：Resign a signed message
- `-sign_receipt`：本机帮助描述：Generate a signed receipt for a message

<details><summary>展开本机 `-help` 原文</summary>

```text
Usage: cms [options] [cert...]
 -help                      Display this summary

General options:
 -in infile                 Input file
 -out outfile               Output file
 -config infile             Load a configuration file (this may load modules)

Operation options:
 -encrypt                   Encrypt message
 -decrypt                   Decrypt encrypted message
 -sign                      Sign message
 -verify                    Verify signed message
 -resign                    Resign a signed message
 -sign_receipt              Generate a signed receipt for a message
 -verify_receipt infile     Verify receipts; exit if receipt signatures do not verify
 -digest_create             Create a CMS "DigestedData" object
 -digest_verify             Verify a CMS "DigestedData" object and output it
 -compress                  Create a CMS "CompressedData" object
 -uncompress                Uncompress a CMS "CompressedData" object
 -EncryptedData_encrypt     Create CMS "EncryptedData" object using symmetric key
 -EncryptedData_decrypt     Decrypt CMS "EncryptedData" object using symmetric key
 -data_create               Create a CMS "Data" object
 -data_out                  Copy CMS "Data" object to output
 -cmsout                    Output CMS structure

File format options:
 -inform parm               Input format SMIME (default), PEM or DER
 -outform parm              Output format SMIME (default), PEM or DER
 -rctform PEM|DER           Receipt file format
 -stream                    Enable CMS streaming
 -indef                     Same as -stream
 -noindef                   Disable CMS streaming
 -binary                    Treat input as binary: do not translate to canonical form
 -crlfeol                   Use CRLF as EOL termination instead of CR only
 -asciicrlf                 Perform CRLF canonicalisation when signing

Keys and passwords options:
 -pwri_password val         Specific password for recipient
 -secretkey val             Use specified hex-encoded key to decrypt/encrypt recipients or content
 -secretkeyid val           Identity of the -secretkey for CMS "KEKRecipientInfo" object
 -inkey val                 Input private key (if not signer or recipient)
 -passin val                Input file pass phrase source
 -keyopt val                Set public key parameters as n:v pairs
 -keyform format            Input private key format (ENGINE, other values ignored)
 -engine val                Use engine e, possibly a hardware device

Provider options:
 -provider-path val         Provider load path (must be before 'provider' argument if required)
 -provider val              Provider to load (can be specified multiple times)
 -propquery val             Property query used when fetching algorithms

Random state options:
 -rand val                  Load the given file(s) into the random number generator
 -writerand outfile         Write random data to the specified file

Encryption and decryption options:
 -originator val            Originator certificate file
 -recip infile              Recipient cert file
 -cert... parm              Recipient certs (optional; used only when encrypting)
 -*                         The encryption algorithm to use (any supported cipher)
 -wrap val                  Key wrap algorithm to use when encrypting with key agreement
 -aes128-wrap               Use AES128 to wrap key
 -aes192-wrap               Use AES192 to wrap key
 -aes256-wrap               Use AES256 to wrap key
 -des3-wrap                 Use 3DES-EDE to wrap key
 -debug_decrypt             Disable MMA protection, return error if no recipient found (see doc)

Signing options:
 -md val                    Digest algorithm to use
 -signer val                Signer certificate input file
 -certfile infile           Other certificates file
 -cades                     Include signingCertificate attribute (CAdES-BES)
 -nodetach                  Use opaque signing
 -nocerts                   Don't include signer's certificate when signing
 -noattr                    Don't include any signed attributes
 -nosmimecap                Omit the SMIMECapabilities attribute
 -receipt_request_all       When signing, create a receipt request for all recipients
 -receipt_request_first     When signing, create a receipt request for first recipient
 -receipt_request_from val  Create signed receipt request with specified email address
 -receipt_request_to val    Create signed receipt targeted to specified address

Verification options:
 -signer val                Signer certificate(s) output file
 -content infile            Supply or override content for detached signature
 -no_content_verify         Do not verify signed content signatures
 -no_attr_verify            Do not verify signed attribute signatures
 -nosigs                    Don't verify message signature
 -noverify                  Don't verify signers certificate
 -nointern                  Don't search certificates in message for signer
 -cades                     Check signingCertificate (CAdES-BES)
 -verify_retcode            Exit non-zero on verification failure
 -CAfile infile             Trusted certificates file
 -CApath dir                Trusted certificates directory
 -CAstore uri               Trusted certificates store URI
 -no-CAfile                 Do not load the default certificates file
 -no-CApath                 Do not load certificates from the default certificates directory
 -no-CAstore                Do not load certificates from the default certificates store

Output options:
 -keyid                     Use subject key identifier
 -econtent_type val         OID for external content
 -text                      Include or delete text MIME headers
 -certsout outfile          Certificate output file
 -to val                    To address
 -from val                  From address
 -subject val               Subject

Printing options:
 -noout                     For the -cmsout operation do not output the parsed CMS structure
 -print                     For the -cmsout operation print out all fields of the CMS structure
 -nameopt val               For the -print option specifies various strings printing options
 -receipt_request_print     Print CMS Receipt Request

Validation options:
 -policy val                adds policy to the acceptable policy set
 -purpose val               certificate chain purpose
 -verify_name val           verification policy name
 -verify_depth int          chain depth limit
 -auth_level int            chain authentication security level
 -attime intmax             verification epoch time
 -verify_hostname val       expected peer hostname
 -verify_email val          expected peer email
 -verify_ip val             expected peer IP address
 -ignore_critical           permit unhandled critical extensions
 -issuer_checks             (deprecated)
 -crl_check                 check leaf certificate revocation
 -crl_check_all             check full chain revocation
 -policy_check              perform rfc5280 policy checks
 -explicit_policy           set policy variable require-explicit-policy
 -inhibit_any               set policy variable inhibit-any-policy
 -inhibit_map               set policy variable inhibit-policy-mapping
 -x509_strict               disable certificate compatibility work-arounds
 -extended_crl              enable extended CRL features
 -use_deltas                use delta CRLs
 -policy_print              print policy processing diagnostics
 -check_ss_sig              check root CA self-signatures
 -trusted_first             search trust store first (default)
 -suiteB_128_only           Suite B 128-bit-only mode
 -suiteB_128                Suite B 128-bit mode allowing 192-bit algorithms
 -suiteB_192                Suite B 192-bit-only mode
 -partial_chain             accept chains anchored by intermediate trust-store CAs
 -no_alt_chains             (deprecated)
 -no_check_time             ignore certificate validity time
 -allow_proxy_certs         allow the use of proxy certificates
```

</details>

### `openssl smime`

**帮助命令**：`openssl smime -help`。**用法**：`Usage: smime [options] [cert...]`

**作用**：处理 S/MIME 签名/加密邮件格式。

**帮助中需要先理解的参数**：

- `-encrypt`：选择加密动作；本机帮助描述：Encrypt message
- `-decrypt`：选择解密动作；本机帮助描述：Decrypt encrypted message
- `-sign`：选择签名动作或私钥；本机帮助描述：Sign message
- `-verify`：选择验签动作或公钥；本机帮助描述：Verify signed message
- `-stream`：本机帮助描述：Enable CMS streaming
- `-indef`：本机帮助描述：Same as -stream

<details><summary>展开本机 `-help` 原文</summary>

```text
Usage: smime [options] [cert...]

General options:
 -help                 Display this summary
 -in infile            Input file
 -inform parm          Input format SMIME (default), PEM or DER
 -out outfile          Output file
 -outform parm         Output format SMIME (default), PEM or DER
 -inkey val            Input private key (if not signer or recipient)
 -keyform format       Input private key format (ENGINE, other values ignored)
 -engine val           Use engine, possibly a hardware device
 -stream               Enable CMS streaming
 -indef                Same as -stream
 -noindef              Disable CMS streaming
 -config infile        Load a configuration file (this may load modules)

Action options:
 -encrypt              Encrypt message
 -decrypt              Decrypt encrypted message
 -sign                 Sign message
 -resign               Resign a signed message
 -verify               Verify signed message

Signing/Encryption options:
 -passin val           Input file pass phrase source
 -md val               Digest algorithm to use when signing or resigning
 -*                    Any supported cipher
 -pk7out               Output PKCS#7 structure
 -nointern             Don't search certificates in message for signer
 -nodetach             Use opaque signing
 -noattr               Don't include any signed attributes
 -binary               Don't translate message to text
 -signer val           Signer certificate file
 -content infile       Supply or override content for detached signature
 -nocerts              Don't include signers certificate when signing

Verification/Decryption options:
 -nosigs               Don't verify message signature
 -noverify             Don't verify signers certificate
 -certfile infile      Other certificates file
 -recip infile         Recipient certificate file for decryption

Email options:
 -to val               To address
 -from val             From address
 -subject val          Subject
 -text                 Include or delete text MIME headers
 -nosmimecap           Omit the SMIMECapabilities attribute

Certificate chain options:
 -CApath dir           Trusted certificates directory
 -CAfile infile        Trusted certificates file
 -CAstore uri          Trusted certificates store URI
 -no-CAfile            Do not load the default certificates file
 -no-CApath            Do not load certificates from the default certificates directory
 -no-CAstore           Do not load certificates from the default certificates store
 -nochain              set PKCS7_NOCHAIN so certificates contained in the message are not used as untrusted CAs
 -crlfeol              Use CRLF as EOL termination instead of CR only

Random state options:
 -rand val             Load the given file(s) into the random number generator
 -writerand outfile    Write random data to the specified file

Validation options:
 -policy val           adds policy to the acceptable policy set
 -purpose val          certificate chain purpose
 -verify_name val      verification policy name
 -verify_depth int     chain depth limit
 -auth_level int       chain authentication security level
 -attime intmax        verification epoch time
 -verify_hostname val  expected peer hostname
 -verify_email val     expected peer email
 -verify_ip val        expected peer IP address
 -ignore_critical      permit unhandled critical extensions
 -issuer_checks        (deprecated)
 -crl_check            check leaf certificate revocation
 -crl_check_all        check full chain revocation
 -policy_check         perform rfc5280 policy checks
 -explicit_policy      set policy variable require-explicit-policy
 -inhibit_any          set policy variable inhibit-any-policy
 -inhibit_map          set policy variable inhibit-policy-mapping
 -x509_strict          disable certificate compatibility work-arounds
 -extended_crl         enable extended CRL features
 -use_deltas           use delta CRLs
 -policy_print         print policy processing diagnostics
 -check_ss_sig         check root CA self-signatures
 -trusted_first        search trust store first (default)
 -suiteB_128_only      Suite B 128-bit-only mode
 -suiteB_128           Suite B 128-bit mode allowing 192-bit algorithms
 -suiteB_192           Suite B 192-bit-only mode
 -partial_chain        accept chains anchored by intermediate trust-store CAs
 -no_alt_chains        (deprecated)
 -no_check_time        ignore certificate validity time
 -allow_proxy_certs    allow the use of proxy certificates

Provider options:
 -provider-path val    Provider load path (must be before 'provider' argument if required)
 -provider val         Provider to load (can be specified multiple times)
 -propquery val        Property query used when fetching algorithms

Parameters:
 cert                  Recipient certs, used when encrypting
```

</details>

### `openssl ciphers`

**帮助命令**：`openssl ciphers -help`。**用法**：`Usage: ciphers [options] [cipher]`

**作用**：列出并筛选 TLS 密码套件；不是文件加密命令。

**帮助中需要先理解的参数**：

- `-v`：本机帮助描述：Verbose listing of the SSL/TLS ciphers
- `-V`：本机帮助描述：Even more verbose
- `-stdname`：本机帮助描述：Show standard cipher names
- `-s`：本机帮助描述：Only supported ciphers
- `-tls1`：本机帮助描述：Ciphers compatible with TLS1
- `-tls1_1`：本机帮助描述：Ciphers compatible with TLS1.1

<details><summary>展开本机 `-help` 原文</summary>

```text
Usage: ciphers [options] [cipher]

General options:
 -help               Display this summary

Output options:
 -v                  Verbose listing of the SSL/TLS ciphers
 -V                  Even more verbose
 -stdname            Show standard cipher names
 -convert val        Convert standard name into OpenSSL name

Cipher specification options:
 -s                  Only supported ciphers
 -tls1               Ciphers compatible with TLS1
 -tls1_1             Ciphers compatible with TLS1.1
 -tls1_2             Ciphers compatible with TLS1.2
 -tls1_3             Ciphers compatible with TLS1.3
 -psk                Include ciphersuites requiring PSK
 -srp                (deprecated) Include ciphersuites requiring SRP
 -ciphersuites val   Configure the TLSv1.3 ciphersuites to use

Provider options:
 -provider-path val  Provider load path (must be before 'provider' argument if required)
 -provider val       Provider to load (can be specified multiple times)
 -propquery val      Property query used when fetching algorithms

Parameters:
 cipher              Cipher string to decode (optional)
```

</details>

### `openssl s_client`

**帮助命令**：`openssl s_client -help`。**用法**：`Usage: s_client [options] [host:port]`

**作用**：连接 TLS 服务并查看握手、证书与协议诊断。

**参数解读**：可用 `-connect` 和 `-servername` 指定目标，证书展示不自动等于验证通过。

**帮助中需要先理解的参数**：

- `-ct`：本机帮助描述：Request and parse SCTs (also enables OCSP stapling)
- `-noct`：本机帮助描述：Do not request or parse SCTs (default)
- `-fallback_scsv`：本机帮助描述：Send the fallback SCSV
- `-build_chain`：本机帮助描述：Build client certificate chain
- `-no-CAfile`：本机帮助描述：Do not load the default certificates file
- `-no-CApath`：本机帮助描述：Do not load certificates from the default certificates directory

<details><summary>展开本机 `-help` 原文</summary>

```text
Usage: s_client [options] [host:port]

General options:
 -help                      Display this summary
 -engine val                Use engine, possibly a hardware device
 -ssl_client_engine val     Specify engine to be used for client certificate operations
 -ssl_config val            Use specified section for SSL_CTX configuration
 -ct                        Request and parse SCTs (also enables OCSP stapling)
 -noct                      Do not request or parse SCTs (default)
 -ctlogfile infile          CT log list CONF file

Network options:
 -host val                  Use -connect instead
 -port +int                 Use -connect instead
 -connect val               TCP/IP where to connect; default: 4433)
 -bind val                  bind local address for connection
 -proxy val                 Connect to via specified proxy to the real server
 -proxy_user val            UserID for proxy authentication
 -proxy_pass val            Proxy authentication password source
 -unix val                  Connect over the specified Unix-domain socket
 -4                         Use IPv4 only
 -6                         Use IPv6 only
 -maxfraglen +int           Enable Maximum Fragment Length Negotiation (len values: 512, 1024, 2048 and 4096)
 -max_send_frag +int        Maximum Size of send frames
 -split_send_frag +int      Size used to split data for encrypt pipelines
 -max_pipelines +int        Maximum number of encrypt/decrypt pipelines to be used
 -read_buf +int             Default read buffer size to be used for connections
 -fallback_scsv             Send the fallback SCSV

Identity options:
 -cert infile               Client certificate file to use
 -certform PEM|DER          Client certificate file format (PEM/DER/P12); has no effect
 -cert_chain infile         Client certificate chain file (in PEM format)
 -build_chain               Build client certificate chain
 -key val                   Private key file to use; default: -cert file
 -keyform PEM|DER|ENGINE    Key format (ENGINE, other values ignored)
 -pass val                  Private key and cert file pass phrase source
 -verify +int               Turn on peer certificate verification
 -nameopt val               Certificate subject/issuer name printing options
 -CApath dir                PEM format directory of CA's
 -CAfile infile             PEM format file of CA's
 -CAstore uri               URI to store of CA's
 -no-CAfile                 Do not load the default certificates file
 -no-CApath                 Do not load certificates from the default certificates directory
 -no-CAstore                Do not load certificates from the default certificates store
 -requestCAfile infile      PEM format file of CA names to send to the server
 -dane_tlsa_domain val      DANE TLSA base domain
 -dane_tlsa_rrdata val      DANE TLSA rrdata presentation form
 -dane_ee_no_namechecks     Disable name checks when matching DANE-EE(3) TLSA records
 -psk_identity val          PSK identity
 -psk val                   PSK in hex (without 0x)
 -psk_session infile        File to read PSK SSL session from
 -name val                  Hostname to use for "-starttls lmtp", "-starttls smtp" or "-starttls xmpp[-server]"

Session options:
 -reconnect                 Drop and re-make the connection with the same Session-ID
 -sess_out outfile          File to write SSL session to
 -sess_in infile            File to read SSL session from

Input/Output options:
 -crlf                      Convert LF from terminal into CRLF
 -quiet                     No s_client output
 -ign_eof                   Ignore input eof (default when -quiet)
 -no_ign_eof                Don't ignore input eof
 -starttls val              Use the appropriate STARTTLS command before starting TLS
 -xmpphost val              Alias of -name option for "-starttls xmpp[-server]"
 -brief                     Restrict output to brief summary of connection parameters
 -prexit                    Print session information when the program exits

Debug options:
 -showcerts                 Show all certificates sent by the server
 -debug                     Extra output
 -msg                       Show protocol messages
 -msgfile outfile           File to send output of -msg or -trace, instead of stdout
 -nbio_test                 More ssl protocol testing
 -state                     Print the ssl states
 -keymatexport val          Export keying material using label
 -keymatexportlen +int      Export len bytes of keying material; default 20
 -security_debug            Enable security debug messages
 -security_debug_verbose    Output more security debug output
 -trace                     Show trace output of protocol messages
 -keylogfile outfile        Write TLS secrets to file
 -nocommands                Do not use interactive command letters
 -servername val            Set TLS extension servername (SNI) in ClientHello (default)
 -noservername              Do not send the server name (SNI) extension in the ClientHello
 -tlsextdebug               Hex dump of all TLS extensions received
 -ignore_unexpected_eof     Do not treat lack of close_notify from a peer as an error
 -status                    Request certificate status from server
 -serverinfo val            types  Send empty ClientHello extensions (comma-separated numbers)
 -alpn val                  Enable ALPN extension, considering named protocols supported (comma-separated list)
 -async                     Support asynchronous operation
 -nbio                      Use non-blocking IO

Protocol and version options:
 -tls1                      Just use TLSv1
 -tls1_1                    Just use TLSv1.1
 -tls1_2                    Just use TLSv1.2
 -tls1_3                    Just use TLSv1.3
 -dtls                      Use any version of DTLS
 -timeout                   Enable send/receive timeout on DTLS connections
 -mtu +int                  Set the link layer MTU
 -dtls1                     Just use DTLSv1
 -dtls1_2                   Just use DTLSv1.2
 -nextprotoneg val          Enable NPN extension, considering named protocols supported (comma-separated list)
 -early_data infile         File to send as early data
 -enable_pha                Enable post-handshake-authentication
 -use_srtp val              Offer SRTP key management with a colon-separated profile list
 -srpuser val               (deprecated) SRP authentication for 'user'
 -srppass val               (deprecated) Password for 'user'
 -srp_lateuser              (deprecated) SRP username into second ClientHello message
 -srp_moregroups            (deprecated) Tolerate other than the known g N values.
 -srp_strength +int         (deprecated) Minimal length in bits for N

Random state options:
 -rand val                  Load the given file(s) into the random number generator
 -writerand outfile         Write random data to the specified file

TLS/SSL options:
 -no_ssl3                   Just disable SSLv3
 -no_tls1                   Just disable TLSv1
 -no_tls1_1                 Just disable TLSv1.1
 -no_tls1_2                 Just disable TLSv1.2
 -no_tls1_3                 Just disable TLSv1.3
 -bugs                      Turn on SSL bug compatibility
 -no_comp                   Disable SSL/TLS compression (default)
 -comp                      Use SSL/TLS-level compression
 -no_ticket                 Disable use of TLS session tickets
 -serverpref                Use server's cipher preferences
 -legacy_renegotiation      Enable use of legacy renegotiation (dangerous)
 -client_renegotiation      Allow client-initiated renegotiation
 -no_renegotiation          Disable all renegotiation.
 -legacy_server_connect     Allow initial connection to servers that don't support RI
 -no_resumption_on_reneg    Disallow session resumption on renegotiation
 -no_legacy_server_connect  Disallow initial connection to servers that don't support RI
 -allow_no_dhe_kex          In TLSv1.3 allow non-(ec)dhe based key exchange on resumption
 -prioritize_chacha         Prioritize ChaCha ciphers when preferred by clients
 -strict                    Enforce strict certificate checks as per TLS standard
 -sigalgs val               Signature algorithms to support (colon-separated list)
 -client_sigalgs val        Signature algorithms to support for client certificate authentication (colon-separated list)
 -groups val                Groups to advertise (colon-separated list)
 -curves val                Groups to advertise (colon-separated list)
 -named_curve val           Elliptic curve used for ECDHE (server-side only)
 -cipher val                Specify TLSv1.2 and below cipher list to be used
 -ciphersuites val          Specify TLSv1.3 ciphersuites to be used
 -min_protocol val          Specify the minimum protocol version to be used
 -max_protocol val          Specify the maximum protocol version to be used
 -record_padding val        Block size to pad TLS 1.3 records to.
 -debug_broken_protocol     Perform all sorts of protocol violations for testing purposes
 -no_middlebox              Disable TLSv1.3 middlebox compat mode
 -no_etm                    Disable Encrypt-then-Mac extension

Validation options:
 -policy val                adds policy to the acceptable policy set
 -purpose val               certificate chain purpose
 -verify_name val           verification policy name
 -verify_depth int          chain depth limit
 -auth_level int            chain authentication security level
 -attime intmax             verification epoch time
 -verify_hostname val       expected peer hostname
 -verify_email val          expected peer email
 -verify_ip val             expected peer IP address
 -ignore_critical           permit unhandled critical extensions
 -issuer_checks             (deprecated)
 -crl_check                 check leaf certificate revocation
 -crl_check_all             check full chain revocation
 -policy_check              perform rfc5280 policy checks
 -explicit_policy           set policy variable require-explicit-policy
 -inhibit_any               set policy variable inhibit-any-policy
 -inhibit_map               set policy variable inhibit-policy-mapping
 -x509_strict               disable certificate compatibility work-arounds
 -extended_crl              enable extended CRL features
 -use_deltas                use delta CRLs
 -policy_print              print policy processing diagnostics
 -check_ss_sig              check root CA self-signatures
 -trusted_first             search trust store first (default)
 -suiteB_128_only           Suite B 128-bit-only mode
 -suiteB_128                Suite B 128-bit mode allowing 192-bit algorithms
 -suiteB_192                Suite B 192-bit-only mode
 -partial_chain             accept chains anchored by intermediate trust-store CAs
 -no_alt_chains             (deprecated)
 -no_check_time             ignore certificate validity time
 -allow_proxy_certs         allow the use of proxy certificates
 -CRL infile                CRL file to use
 -crl_download              Download CRL from distribution points
 -CRLform PEM|DER           CRL format (PEM or DER); default PEM
 -verify_return_error       Close connection on verification error
 -verify_quiet              Restrict verify output to errors
 -chainCAfile infile        CA file for certificate chain (PEM format)
 -chainCApath dir           Use dir as certificate store path to build CA certificate chain
 -chainCAstore uri          CA store URI for certificate chain
 -verifyCAfile infile       CA file for certificate verification (PEM format)
 -verifyCApath dir          Use dir as certificate store path to verify CA certificate
 -verifyCAstore uri         CA store URI for certificate verification

Extended certificate options:
 -xkey infile               key for Extended certificates
 -xcert infile              cert for Extended certificates
 -xchain infile             chain for Extended certificates
 -xchain_build              build certificate chain for the extended certificates
 -xcertform PEM|DER         format of Extended certificate (PEM/DER/P12); has no effect
 -xkeyform PEM|DER          format of Extended certificate's key (DER/PEM/P12); has no effect

Provider options:
 -provider-path val         Provider load path (must be before 'provider' argument if required)
 -provider val              Provider to load (can be specified multiple times)
 -propquery val             Property query used when fetching algorithms

Parameters:
 host:port                  Where to connect; same as -connect option
```

</details>

### `openssl s_server`

**帮助命令**：`openssl s_server -help`。**用法**：`Usage: s_server [options]`

**作用**：启动测试 TLS 服务端，需证书/私钥与端口。

**参数解读**：需要可用证书和私钥；只用于隔离测试环境。

**帮助中需要先理解的参数**：

- `-trace`：本机帮助描述：trace protocol messages
- `-unlink`：本机帮助描述：For -unix, unlink existing socket first
- `-no-CAfile`：本机帮助描述：Do not load the default certificates file
- `-no-CApath`：本机帮助描述：Do not load certificates from the default certificates directory
- `-no-CAstore`：本机帮助描述：Do not load certificates from the default certificates store URI
- `-nocert`：本机帮助描述：Don't use any certificates (Anon-DH)

<details><summary>展开本机 `-help` 原文</summary>

```text
Usage: s_server [options]

General options:
 -help                      Display this summary
 -ssl_config val            Configure SSL_CTX using the given configuration value
 -trace                     trace protocol messages
 -engine val                Use engine, possibly a hardware device

Network options:
 -port +int                 TCP/IP port to listen on for connections (default is 4433)
 -accept val                TCP/IP optional host and port to listen on for connections (default is *:4433)
 -unix val                  Unix domain socket to accept on
 -unlink                    For -unix, unlink existing socket first
 -4                         Use IPv4 only
 -6                         Use IPv6 only

Identity options:
 -context val               Set session ID context
 -CAfile infile             PEM format file of CA's
 -CApath dir                PEM format directory of CA's
 -CAstore uri               URI to store of CA's
 -no-CAfile                 Do not load the default certificates file
 -no-CApath                 Do not load certificates from the default certificates directory
 -no-CAstore                Do not load certificates from the default certificates store URI
 -nocert                    Don't use any certificates (Anon-DH)
 -verify int                Turn on peer certificate verification
 -Verify int                Turn on peer certificate verification, must have a cert
 -nameopt val               Certificate subject/issuer name printing options
 -cert infile               Server certificate file to use; default server.pem
 -cert2 infile              Certificate file to use for servername; default server2.pem
 -certform PEM|DER          Server certificate file format (PEM/DER/P12); has no effect
 -cert_chain infile         Server certificate chain file in PEM format
 -build_chain               Build server certificate chain
 -serverinfo val            PEM serverinfo file for certificate
 -key val                   Private key file to use; default is -cert file or elseserver.pem
 -key2 infile               -Private Key file to use for servername if not in -cert2
 -keyform format            Key format (ENGINE, other values ignored)
 -pass val                  Private key and cert file pass phrase source
 -dcert infile              Second server certificate file to use (usually for DSA)
 -dcertform PEM|DER         Second server certificate file format (PEM/DER/P12); has no effect
 -dcert_chain infile        second server certificate chain file in PEM format
 -dkey infile               Second private key file to use (usually for DSA)
 -dkeyform PEM|DER          Second key file format (ENGINE, other values ignored)
 -dpass val                 Second private key and cert file pass phrase source
 -dhparam infile            DH parameters file to use
 -servername val            Servername for HostName TLS extension
 -servername_fatal          On servername mismatch send fatal alert (default warning alert)
 -nbio_test                 Test with the non-blocking test bio
 -crlf                      Convert LF from terminal into CRLF
 -quiet                     No server output
 -no_resume_ephemeral       Disable caching and tickets if ephemeral (EC)DH is used
 -www                       Respond to a 'GET /' with a status page
 -WWW                       Respond to a 'GET with the file ./path
 -ignore_unexpected_eof     Do not treat lack of close_notify from a peer as an error
 -tlsextdebug               Hex dump of all TLS extensions received
 -HTTP                      Like -WWW but ./path includes HTTP headers
 -id_prefix val             Generate SSL/TLS session IDs prefixed by arg
 -keymatexport val          Export keying material using label
 -keymatexportlen +int      Export len bytes of keying material; default 20
 -CRL infile                CRL file to use
 -CRLform PEM|DER           CRL file format (PEM or DER); default PEM
 -crl_download              Download CRLs from distribution points in certificate CDP entries
 -chainCAfile infile        CA file for certificate chain (PEM format)
 -chainCApath dir           use dir as certificate store path to build CA certificate chain
 -chainCAstore uri          use URI as certificate store to build CA certificate chain
 -verifyCAfile infile       CA file for certificate verification (PEM format)
 -verifyCApath dir          use dir as certificate store path to verify CA certificate
 -verifyCAstore uri         use URI as certificate store to verify CA certificate
 -no_cache                  Disable session cache
 -ext_cache                 Disable internal cache, set up and use external cache
 -verify_return_error       Close connection on verification error
 -verify_quiet              No verify output except verify errors
 -ign_eof                   Ignore input EOF (default when -quiet)
 -no_ign_eof                Do not ignore input EOF

OCSP options:
 -status                    Request certificate status from server
 -status_verbose            Print more output in certificate status callback
 -status_timeout int        Status request responder timeout
 -status_url val            Status request fallback URL
 -proxy val                 [http[s]://]host[:port][/path] of HTTP(S) proxy to use; path is ignored
 -no_proxy val              List of addresses of servers not to use HTTP(S) proxy for
                            Default from environment variable 'no_proxy', else 'NO_PROXY', else none
 -status_file infile        File containing DER encoded OCSP Response

Debug options:
 -security_debug            Print output from SSL/TLS security framework
 -security_debug_verbose    Print more output from SSL/TLS security framework
 -brief                     Restrict output to brief summary of connection parameters
 -rev                       act as an echo server that sends back received text reversed
 -debug                     Print more output
 -msg                       Show protocol messages
 -msgfile outfile           File to send output of -msg or -trace, instead of stdout
 -state                     Print the SSL states
 -async                     Operate in asynchronous mode
 -max_pipelines +int        Maximum number of encrypt/decrypt pipelines to be used
 -naccept +int              Terminate after #num connections
 -keylogfile outfile        Write TLS secrets to file

Network options:
 -nbio                      Use non-blocking IO
 -timeout                   Enable timeouts
 -mtu +int                  Set link-layer MTU
 -read_buf +int             Default read buffer size to be used for connections
 -split_send_frag +int      Size used to split data for encrypt pipelines
 -max_send_frag +int        Maximum Size of send frames

Server identity options:
 -psk_identity val          PSK identity to expect
 -psk_hint val              PSK identity hint to use
 -psk val                   PSK in hex (without 0x)
 -psk_session infile        File to read PSK SSL session from
 -srpvfile infile           (deprecated) The verifier file for SRP
 -srpuserseed val           (deprecated) A seed string for a default user salt

Protocol and version options:
 -max_early_data int        The maximum number of bytes of early data as advertised in tickets
 -recv_max_early_data int   The maximum number of bytes of early data (hard limit)
 -early_data                Attempt to read early data
 -num_tickets int           The number of TLSv1.3 session tickets that a server will automatically issue
 -anti_replay               Switch on anti-replay protection (default)
 -no_anti_replay            Switch off anti-replay protection
 -http_server_binmode       opening files in binary mode when acting as http server (-WWW and -HTTP)
 -no_ca_names               Disable TLS Extension CA Names
 -stateless                 Require TLSv1.3 cookies
 -tls1                      Just talk TLSv1
 -tls1_1                    Just talk TLSv1.1
 -tls1_2                    just talk TLSv1.2
 -tls1_3                    just talk TLSv1.3
 -dtls                      Use any DTLS version
 -listen                    Listen for a DTLS ClientHello with a cookie and then connect
 -dtls1                     Just talk DTLSv1
 -dtls1_2                   Just talk DTLSv1.2
 -use_srtp val              Offer SRTP key management with a colon-separated profile list
 -no_dhe                    Disable ephemeral DH
 -nextprotoneg val          Set the advertised protocols for the NPN extension (comma-separated list)
 -alpn val                  Set the advertised protocols for the ALPN extension (comma-separated list)
 -sendfile                  Use sendfile to response file with -WWW

Random state options:
 -rand val                  Load the given file(s) into the random number generator
 -writerand outfile         Write random data to the specified file

TLS/SSL options:
 -no_ssl3                   Just disable SSLv3
 -no_tls1                   Just disable TLSv1
 -no_tls1_1                 Just disable TLSv1.1
 -no_tls1_2                 Just disable TLSv1.2
 -no_tls1_3                 Just disable TLSv1.3
 -bugs                      Turn on SSL bug compatibility
 -no_comp                   Disable SSL/TLS compression (default)
 -comp                      Use SSL/TLS-level compression
 -no_ticket                 Disable use of TLS session tickets
 -serverpref                Use server's cipher preferences
 -legacy_renegotiation      Enable use of legacy renegotiation (dangerous)
 -client_renegotiation      Allow client-initiated renegotiation
 -no_renegotiation          Disable all renegotiation.
 -legacy_server_connect     Allow initial connection to servers that don't support RI
 -no_resumption_on_reneg    Disallow session resumption on renegotiation
 -no_legacy_server_connect  Disallow initial connection to servers that don't support RI
 -allow_no_dhe_kex          In TLSv1.3 allow non-(ec)dhe based key exchange on resumption
 -prioritize_chacha         Prioritize ChaCha ciphers when preferred by clients
 -strict                    Enforce strict certificate checks as per TLS standard
 -sigalgs val               Signature algorithms to support (colon-separated list)
 -client_sigalgs val        Signature algorithms to support for client certificate authentication (colon-separated list)
 -groups val                Groups to advertise (colon-separated list)
 -curves val                Groups to advertise (colon-separated list)
 -named_curve val           Elliptic curve used for ECDHE (server-side only)
 -cipher val                Specify TLSv1.2 and below cipher list to be used
 -ciphersuites val          Specify TLSv1.3 ciphersuites to be used
 -min_protocol val          Specify the minimum protocol version to be used
 -max_protocol val          Specify the maximum protocol version to be used
 -record_padding val        Block size to pad TLS 1.3 records to.
 -debug_broken_protocol     Perform all sorts of protocol violations for testing purposes
 -no_middlebox              Disable TLSv1.3 middlebox compat mode
 -no_etm                    Disable Encrypt-then-Mac extension

Validation options:
 -policy val                adds policy to the acceptable policy set
 -purpose val               certificate chain purpose
 -verify_name val           verification policy name
 -verify_depth int          chain depth limit
 -auth_level int            chain authentication security level
 -attime intmax             verification epoch time
 -verify_hostname val       expected peer hostname
 -verify_email val          expected peer email
 -verify_ip val             expected peer IP address
 -ignore_critical           permit unhandled critical extensions
 -issuer_checks             (deprecated)
 -crl_check                 check leaf certificate revocation
 -crl_check_all             check full chain revocation
 -policy_check              perform rfc5280 policy checks
 -explicit_policy           set policy variable require-explicit-policy
 -inhibit_any               set policy variable inhibit-any-policy
 -inhibit_map               set policy variable inhibit-policy-mapping
 -x509_strict               disable certificate compatibility work-arounds
 -extended_crl              enable extended CRL features
 -use_deltas                use delta CRLs
 -policy_print              print policy processing diagnostics
 -check_ss_sig              check root CA self-signatures
 -trusted_first             search trust store first (default)
 -suiteB_128_only           Suite B 128-bit-only mode
 -suiteB_128                Suite B 128-bit mode allowing 192-bit algorithms
 -suiteB_192                Suite B 192-bit-only mode
 -partial_chain             accept chains anchored by intermediate trust-store CAs
 -no_alt_chains             (deprecated)
 -no_check_time             ignore certificate validity time
 -allow_proxy_certs         allow the use of proxy certificates

Extended certificate options:
 -xkey infile               key for Extended certificates
 -xcert infile              cert for Extended certificates
 -xchain infile             chain for Extended certificates
 -xchain_build              build certificate chain for the extended certificates
 -xcertform PEM|DER         format of Extended certificate (PEM/DER/P12); has no effect
 -xkeyform PEM|DER          format of Extended certificate's key (DER/PEM/P12); has no effect

Provider options:
 -provider-path val         Provider load path (must be before 'provider' argument if required)
 -provider val              Provider to load (can be specified multiple times)
 -propquery val             Property query used when fetching algorithms
```

</details>

### `openssl s_time`

**帮助命令**：`openssl s_time -help`。**用法**：`Usage: s_time [options]`

**作用**：对 TLS 服务连接执行简单计时测试。

**帮助中需要先理解的参数**：

- `-new`：本机帮助描述：Just time new connections
- `-reuse`：本机帮助描述：Just time connection reuse
- `-bugs`：本机帮助描述：Turn on SSL bug compatibility
- `-tls1`：本机帮助描述：Just use TLSv1.0
- `-tls1_1`：本机帮助描述：Just use TLSv1.1
- `-tls1_2`：本机帮助描述：Just use TLSv1.2

<details><summary>展开本机 `-help` 原文</summary>

```text
Usage: s_time [options]

General options:
 -help               Display this summary

Connection options:
 -connect val        Where to connect as post:port (default is localhost:4433)
 -new                Just time new connections
 -reuse              Just time connection reuse
 -bugs               Turn on SSL bug compatibility
 -cipher val         TLSv1.2 and below cipher list to be used
 -ciphersuites val   Specify TLSv1.3 ciphersuites to be used
 -tls1               Just use TLSv1.0
 -tls1_1             Just use TLSv1.1
 -tls1_2             Just use TLSv1.2
 -tls1_3             Just use TLSv1.3
 -verify +int        Turn on peer certificate verification, set depth
 -time +int          Seconds to collect data, default 30
 -www val            Fetch specified page from the site

Certificate options:
 -nameopt val        Certificate subject/issuer name printing options
 -cert infile        Cert file to use, PEM format assumed
 -key infile         File with key, PEM; default is -cert file
 -cafile infile      PEM format file of CA's
 -CAfile infile      PEM format file of CA's
 -CApath dir         PEM format directory of CA's
 -CAstore uri        URI to store of CA's
 -no-CAfile          Do not load the default certificates file
 -no-CApath          Do not load certificates from the default certificates directory
 -no-CAstore         Do not load certificates from the default certificates store URI

Provider options:
 -provider-path val  Provider load path (must be before 'provider' argument if required)
 -provider val       Provider to load (can be specified multiple times)
 -propquery val      Property query used when fetching algorithms
```

</details>

### `openssl sess_id`

**帮助命令**：`openssl sess_id -help`。**用法**：`Usage: sess_id [options]`

**作用**：解析/转换 TLS 会话参数。

**帮助中需要先理解的参数**：

- `-cert`：证书文件；本机帮助描述：Output certificate
- `-text`：本机帮助描述：Print ssl session id details
- `-noout`：本机帮助描述：Don't output the encoded session info

<details><summary>展开本机 `-help` 原文</summary>

```text
Usage: sess_id [options]

General options:
 -help            Display this summary
 -context val     Set the session ID context

Input options:
 -in val          Input file - default stdin
 -inform PEM|DER  Input format - default PEM (DER or PEM)

Output options:
 -out outfile     Output file - default stdout
 -outform format  Output format - default PEM (PEM, DER or NSS)
 -text            Print ssl session id details
 -cert            Output certificate
 -noout           Don't output the encoded session info
```

</details>

### `openssl srp`

**帮助命令**：`openssl srp -help`。**用法**：`Usage: srp [options] [user...]`

**作用**：管理 SRP 用户/验证器数据。

**帮助中需要先理解的参数**：

- `-verbose`：本机帮助描述：Talk a lot while doing things
- `-add`：本机帮助描述：Add a user and SRP verifier
- `-modify`：本机帮助描述：Modify the SRP verifier of an existing user
- `-delete`：本机帮助描述：Delete user from verifier file
- `-list`：本机帮助描述：List users

<details><summary>展开本机 `-help` 原文</summary>

```text
Usage: srp [options] [user...]

General options:
 -help               Display this summary
 -verbose            Talk a lot while doing things
 -config infile      A config file
 -name val           The particular srp definition to use
 -engine val         Use engine, possibly a hardware device

Action options:
 -add                Add a user and SRP verifier
 -modify             Modify the SRP verifier of an existing user
 -delete             Delete user from verifier file
 -list               List users

Configuration options:
 -srpvfile infile    The srp verifier file name
 -gn val             Set g and N values to be used for new verifier
 -userinfo val       Additional info to be set for user
 -passin val         Input file pass phrase source
 -passout val        Output file pass phrase source

Random state options:
 -rand val           Load the given file(s) into the random number generator
 -writerand outfile  Write random data to the specified file

Provider options:
 -provider-path val  Provider load path (must be before 'provider' argument if required)
 -provider val       Provider to load (can be specified multiple times)
 -propquery val      Property query used when fetching algorithms

Parameters:
 user                Username(s) to process (optional)
```

</details>

## `openssl help` 中的摘要与加密别名（逐项核对）

除了上面的 53 个标准子命令，本机 `openssl help` 还列出 19 个摘要别名和 79 个加密/编码别名。已逐个执行 `openssl <alias> -help`；这些入口的参数分别沿用 [`dgst`](#openssl-dgst) 或 [`enc`](#openssl-enc) 的体系。下表逐项列出帮助用法；真正执行某算法前还要检查当前 Provider 是否提供它。帮助列出 MD4、RC4、DES 等历史算法不代表本项目允许使用它们。

### 摘要别名

参数说明见 `openssl dgst -help`。下表的每条 `-help` 均已在本机执行并返回退出码 0。

| 别名 | 对应帮助命令 | 本机 Usage |
|---|---|---|
| `blake2b512` | `openssl blake2b512 -help` | `Usage: blake2b512 [options] [file...]` |
| `blake2s256` | `openssl blake2s256 -help` | `Usage: blake2s256 [options] [file...]` |
| `md4` | `openssl md4 -help` | `Usage: md4 [options] [file...]` |
| `md5` | `openssl md5 -help` | `Usage: md5 [options] [file...]` |
| `rmd160` | `openssl rmd160 -help` | `Usage: rmd160 [options] [file...]` |
| `sha1` | `openssl sha1 -help` | `Usage: sha1 [options] [file...]` |
| `sha224` | `openssl sha224 -help` | `Usage: sha224 [options] [file...]` |
| `sha256` | `openssl sha256 -help` | `Usage: sha256 [options] [file...]` |
| `sha3-224` | `openssl sha3-224 -help` | `Usage: sha3-224 [options] [file...]` |
| `sha3-256` | `openssl sha3-256 -help` | `Usage: sha3-256 [options] [file...]` |
| `sha3-384` | `openssl sha3-384 -help` | `Usage: sha3-384 [options] [file...]` |
| `sha3-512` | `openssl sha3-512 -help` | `Usage: sha3-512 [options] [file...]` |
| `sha384` | `openssl sha384 -help` | `Usage: sha384 [options] [file...]` |
| `sha512` | `openssl sha512 -help` | `Usage: sha512 [options] [file...]` |
| `sha512-224` | `openssl sha512-224 -help` | `Usage: sha512-224 [options] [file...]` |
| `sha512-256` | `openssl sha512-256 -help` | `Usage: sha512-256 [options] [file...]` |
| `shake128` | `openssl shake128 -help` | `Usage: shake128 [options] [file...]` |
| `shake256` | `openssl shake256 -help` | `Usage: shake256 [options] [file...]` |
| `sm3` | `openssl sm3 -help` | `Usage: sm3 [options] [file...]` |

#### `openssl blake2b512`

**帮助命令**：`openssl blake2b512 -help`。**用法**：`Usage: blake2b512 [options] [file...]`

**解读**：这是固定摘要名 `blake2b512` 的 `dgst` 入口；文件原始字节作为输入，`-hex` 或 `-binary` 决定输出编码。若使用签名参数，仍须按 [`dgst`](#openssl-dgst) 的签名/验签合同检查密钥与方案。

<details><summary>展开本机 `-help` 内容</summary>

```text
Usage: blake2b512 [options] [file...]

General options:
 -help               Display this summary
 -list               List digests
 -engine val         Use engine e, possibly a hardware device
 -engine_impl        Also use engine given by -engine for digest operations
 -passin val         Input file pass phrase source

Output options:
 -c                  Print the digest with separating colons
 -r                  Print the digest in coreutils format
 -out outfile        Output to filename rather than stdout
 -keyform format     Key file format (ENGINE, other values ignored)
 -hex                Print as hex dump
 -binary             Print in binary form
 -xoflen +int        Output length for XOF algorithms
 -d                  Print debug info
 -debug              Print debug info

Signing options:
 -sign val           Sign digest using private key
 -verify val         Verify a signature using public key
 -prverify val       Verify a signature using private key
 -sigopt val         Signature parameter in n:v form
 -signature infile   File with signature to verify
 -hmac val           Create hashed MAC with key
 -mac val            Create MAC (not necessarily HMAC)
 -macopt val         MAC algorithm parameters in n:v form or key
 -*                  Any supported digest
 -fips-fingerprint   Compute HMAC with the key used in OpenSSL-FIPS fingerprint

Random state options:
 -rand val           Load the given file(s) into the random number generator
 -writerand outfile  Write random data to the specified file

Provider options:
 -provider-path val  Provider load path (must be before 'provider' argument if required)
 -provider val       Provider to load (can be specified multiple times)
 -propquery val      Property query used when fetching algorithms

Parameters:
 file                Files to digest (optional; default is stdin)
```

</details>

#### `openssl blake2s256`

**帮助命令**：`openssl blake2s256 -help`。**用法**：`Usage: blake2s256 [options] [file...]`

**解读**：这是固定摘要名 `blake2s256` 的 `dgst` 入口；文件原始字节作为输入，`-hex` 或 `-binary` 决定输出编码。若使用签名参数，仍须按 [`dgst`](#openssl-dgst) 的签名/验签合同检查密钥与方案。

<details><summary>展开本机 `-help` 内容</summary>

```text
Usage: blake2s256 [options] [file...]

General options:
 -help               Display this summary
 -list               List digests
 -engine val         Use engine e, possibly a hardware device
 -engine_impl        Also use engine given by -engine for digest operations
 -passin val         Input file pass phrase source

Output options:
 -c                  Print the digest with separating colons
 -r                  Print the digest in coreutils format
 -out outfile        Output to filename rather than stdout
 -keyform format     Key file format (ENGINE, other values ignored)
 -hex                Print as hex dump
 -binary             Print in binary form
 -xoflen +int        Output length for XOF algorithms
 -d                  Print debug info
 -debug              Print debug info

Signing options:
 -sign val           Sign digest using private key
 -verify val         Verify a signature using public key
 -prverify val       Verify a signature using private key
 -sigopt val         Signature parameter in n:v form
 -signature infile   File with signature to verify
 -hmac val           Create hashed MAC with key
 -mac val            Create MAC (not necessarily HMAC)
 -macopt val         MAC algorithm parameters in n:v form or key
 -*                  Any supported digest
 -fips-fingerprint   Compute HMAC with the key used in OpenSSL-FIPS fingerprint

Random state options:
 -rand val           Load the given file(s) into the random number generator
 -writerand outfile  Write random data to the specified file

Provider options:
 -provider-path val  Provider load path (must be before 'provider' argument if required)
 -provider val       Provider to load (can be specified multiple times)
 -propquery val      Property query used when fetching algorithms

Parameters:
 file                Files to digest (optional; default is stdin)
```

</details>

#### `openssl md4`

**帮助命令**：`openssl md4 -help`。**用法**：`Usage: md4 [options] [file...]`

**解读**：这是固定摘要名 `md4` 的 `dgst` 入口；文件原始字节作为输入，`-hex` 或 `-binary` 决定输出编码。若使用签名参数，仍须按 [`dgst`](#openssl-dgst) 的签名/验签合同检查密钥与方案。

<details><summary>展开本机 `-help` 内容</summary>

```text
Usage: md4 [options] [file...]

General options:
 -help               Display this summary
 -list               List digests
 -engine val         Use engine e, possibly a hardware device
 -engine_impl        Also use engine given by -engine for digest operations
 -passin val         Input file pass phrase source

Output options:
 -c                  Print the digest with separating colons
 -r                  Print the digest in coreutils format
 -out outfile        Output to filename rather than stdout
 -keyform format     Key file format (ENGINE, other values ignored)
 -hex                Print as hex dump
 -binary             Print in binary form
 -xoflen +int        Output length for XOF algorithms
 -d                  Print debug info
 -debug              Print debug info

Signing options:
 -sign val           Sign digest using private key
 -verify val         Verify a signature using public key
 -prverify val       Verify a signature using private key
 -sigopt val         Signature parameter in n:v form
 -signature infile   File with signature to verify
 -hmac val           Create hashed MAC with key
 -mac val            Create MAC (not necessarily HMAC)
 -macopt val         MAC algorithm parameters in n:v form or key
 -*                  Any supported digest
 -fips-fingerprint   Compute HMAC with the key used in OpenSSL-FIPS fingerprint

Random state options:
 -rand val           Load the given file(s) into the random number generator
 -writerand outfile  Write random data to the specified file

Provider options:
 -provider-path val  Provider load path (must be before 'provider' argument if required)
 -provider val       Provider to load (can be specified multiple times)
 -propquery val      Property query used when fetching algorithms

Parameters:
 file                Files to digest (optional; default is stdin)
```

</details>

#### `openssl md5`

**帮助命令**：`openssl md5 -help`。**用法**：`Usage: md5 [options] [file...]`

**解读**：这是固定摘要名 `md5` 的 `dgst` 入口；文件原始字节作为输入，`-hex` 或 `-binary` 决定输出编码。若使用签名参数，仍须按 [`dgst`](#openssl-dgst) 的签名/验签合同检查密钥与方案。

<details><summary>展开本机 `-help` 内容</summary>

```text
Usage: md5 [options] [file...]

General options:
 -help               Display this summary
 -list               List digests
 -engine val         Use engine e, possibly a hardware device
 -engine_impl        Also use engine given by -engine for digest operations
 -passin val         Input file pass phrase source

Output options:
 -c                  Print the digest with separating colons
 -r                  Print the digest in coreutils format
 -out outfile        Output to filename rather than stdout
 -keyform format     Key file format (ENGINE, other values ignored)
 -hex                Print as hex dump
 -binary             Print in binary form
 -xoflen +int        Output length for XOF algorithms
 -d                  Print debug info
 -debug              Print debug info

Signing options:
 -sign val           Sign digest using private key
 -verify val         Verify a signature using public key
 -prverify val       Verify a signature using private key
 -sigopt val         Signature parameter in n:v form
 -signature infile   File with signature to verify
 -hmac val           Create hashed MAC with key
 -mac val            Create MAC (not necessarily HMAC)
 -macopt val         MAC algorithm parameters in n:v form or key
 -*                  Any supported digest
 -fips-fingerprint   Compute HMAC with the key used in OpenSSL-FIPS fingerprint

Random state options:
 -rand val           Load the given file(s) into the random number generator
 -writerand outfile  Write random data to the specified file

Provider options:
 -provider-path val  Provider load path (must be before 'provider' argument if required)
 -provider val       Provider to load (can be specified multiple times)
 -propquery val      Property query used when fetching algorithms

Parameters:
 file                Files to digest (optional; default is stdin)
```

</details>

#### `openssl rmd160`

**帮助命令**：`openssl rmd160 -help`。**用法**：`Usage: rmd160 [options] [file...]`

**解读**：这是固定摘要名 `rmd160` 的 `dgst` 入口；文件原始字节作为输入，`-hex` 或 `-binary` 决定输出编码。若使用签名参数，仍须按 [`dgst`](#openssl-dgst) 的签名/验签合同检查密钥与方案。

<details><summary>展开本机 `-help` 内容</summary>

```text
Usage: rmd160 [options] [file...]

General options:
 -help               Display this summary
 -list               List digests
 -engine val         Use engine e, possibly a hardware device
 -engine_impl        Also use engine given by -engine for digest operations
 -passin val         Input file pass phrase source

Output options:
 -c                  Print the digest with separating colons
 -r                  Print the digest in coreutils format
 -out outfile        Output to filename rather than stdout
 -keyform format     Key file format (ENGINE, other values ignored)
 -hex                Print as hex dump
 -binary             Print in binary form
 -xoflen +int        Output length for XOF algorithms
 -d                  Print debug info
 -debug              Print debug info

Signing options:
 -sign val           Sign digest using private key
 -verify val         Verify a signature using public key
 -prverify val       Verify a signature using private key
 -sigopt val         Signature parameter in n:v form
 -signature infile   File with signature to verify
 -hmac val           Create hashed MAC with key
 -mac val            Create MAC (not necessarily HMAC)
 -macopt val         MAC algorithm parameters in n:v form or key
 -*                  Any supported digest
 -fips-fingerprint   Compute HMAC with the key used in OpenSSL-FIPS fingerprint

Random state options:
 -rand val           Load the given file(s) into the random number generator
 -writerand outfile  Write random data to the specified file

Provider options:
 -provider-path val  Provider load path (must be before 'provider' argument if required)
 -provider val       Provider to load (can be specified multiple times)
 -propquery val      Property query used when fetching algorithms

Parameters:
 file                Files to digest (optional; default is stdin)
```

</details>

#### `openssl sha1`

**帮助命令**：`openssl sha1 -help`。**用法**：`Usage: sha1 [options] [file...]`

**解读**：这是固定摘要名 `sha1` 的 `dgst` 入口；文件原始字节作为输入，`-hex` 或 `-binary` 决定输出编码。若使用签名参数，仍须按 [`dgst`](#openssl-dgst) 的签名/验签合同检查密钥与方案。

<details><summary>展开本机 `-help` 内容</summary>

```text
Usage: sha1 [options] [file...]

General options:
 -help               Display this summary
 -list               List digests
 -engine val         Use engine e, possibly a hardware device
 -engine_impl        Also use engine given by -engine for digest operations
 -passin val         Input file pass phrase source

Output options:
 -c                  Print the digest with separating colons
 -r                  Print the digest in coreutils format
 -out outfile        Output to filename rather than stdout
 -keyform format     Key file format (ENGINE, other values ignored)
 -hex                Print as hex dump
 -binary             Print in binary form
 -xoflen +int        Output length for XOF algorithms
 -d                  Print debug info
 -debug              Print debug info

Signing options:
 -sign val           Sign digest using private key
 -verify val         Verify a signature using public key
 -prverify val       Verify a signature using private key
 -sigopt val         Signature parameter in n:v form
 -signature infile   File with signature to verify
 -hmac val           Create hashed MAC with key
 -mac val            Create MAC (not necessarily HMAC)
 -macopt val         MAC algorithm parameters in n:v form or key
 -*                  Any supported digest
 -fips-fingerprint   Compute HMAC with the key used in OpenSSL-FIPS fingerprint

Random state options:
 -rand val           Load the given file(s) into the random number generator
 -writerand outfile  Write random data to the specified file

Provider options:
 -provider-path val  Provider load path (must be before 'provider' argument if required)
 -provider val       Provider to load (can be specified multiple times)
 -propquery val      Property query used when fetching algorithms

Parameters:
 file                Files to digest (optional; default is stdin)
```

</details>

#### `openssl sha224`

**帮助命令**：`openssl sha224 -help`。**用法**：`Usage: sha224 [options] [file...]`

**解读**：这是固定摘要名 `sha224` 的 `dgst` 入口；文件原始字节作为输入，`-hex` 或 `-binary` 决定输出编码。若使用签名参数，仍须按 [`dgst`](#openssl-dgst) 的签名/验签合同检查密钥与方案。

<details><summary>展开本机 `-help` 内容</summary>

```text
Usage: sha224 [options] [file...]

General options:
 -help               Display this summary
 -list               List digests
 -engine val         Use engine e, possibly a hardware device
 -engine_impl        Also use engine given by -engine for digest operations
 -passin val         Input file pass phrase source

Output options:
 -c                  Print the digest with separating colons
 -r                  Print the digest in coreutils format
 -out outfile        Output to filename rather than stdout
 -keyform format     Key file format (ENGINE, other values ignored)
 -hex                Print as hex dump
 -binary             Print in binary form
 -xoflen +int        Output length for XOF algorithms
 -d                  Print debug info
 -debug              Print debug info

Signing options:
 -sign val           Sign digest using private key
 -verify val         Verify a signature using public key
 -prverify val       Verify a signature using private key
 -sigopt val         Signature parameter in n:v form
 -signature infile   File with signature to verify
 -hmac val           Create hashed MAC with key
 -mac val            Create MAC (not necessarily HMAC)
 -macopt val         MAC algorithm parameters in n:v form or key
 -*                  Any supported digest
 -fips-fingerprint   Compute HMAC with the key used in OpenSSL-FIPS fingerprint

Random state options:
 -rand val           Load the given file(s) into the random number generator
 -writerand outfile  Write random data to the specified file

Provider options:
 -provider-path val  Provider load path (must be before 'provider' argument if required)
 -provider val       Provider to load (can be specified multiple times)
 -propquery val      Property query used when fetching algorithms

Parameters:
 file                Files to digest (optional; default is stdin)
```

</details>

#### `openssl sha256`

**帮助命令**：`openssl sha256 -help`。**用法**：`Usage: sha256 [options] [file...]`

**解读**：这是固定摘要名 `sha256` 的 `dgst` 入口；文件原始字节作为输入，`-hex` 或 `-binary` 决定输出编码。若使用签名参数，仍须按 [`dgst`](#openssl-dgst) 的签名/验签合同检查密钥与方案。

<details><summary>展开本机 `-help` 内容</summary>

```text
Usage: sha256 [options] [file...]

General options:
 -help               Display this summary
 -list               List digests
 -engine val         Use engine e, possibly a hardware device
 -engine_impl        Also use engine given by -engine for digest operations
 -passin val         Input file pass phrase source

Output options:
 -c                  Print the digest with separating colons
 -r                  Print the digest in coreutils format
 -out outfile        Output to filename rather than stdout
 -keyform format     Key file format (ENGINE, other values ignored)
 -hex                Print as hex dump
 -binary             Print in binary form
 -xoflen +int        Output length for XOF algorithms
 -d                  Print debug info
 -debug              Print debug info

Signing options:
 -sign val           Sign digest using private key
 -verify val         Verify a signature using public key
 -prverify val       Verify a signature using private key
 -sigopt val         Signature parameter in n:v form
 -signature infile   File with signature to verify
 -hmac val           Create hashed MAC with key
 -mac val            Create MAC (not necessarily HMAC)
 -macopt val         MAC algorithm parameters in n:v form or key
 -*                  Any supported digest
 -fips-fingerprint   Compute HMAC with the key used in OpenSSL-FIPS fingerprint

Random state options:
 -rand val           Load the given file(s) into the random number generator
 -writerand outfile  Write random data to the specified file

Provider options:
 -provider-path val  Provider load path (must be before 'provider' argument if required)
 -provider val       Provider to load (can be specified multiple times)
 -propquery val      Property query used when fetching algorithms

Parameters:
 file                Files to digest (optional; default is stdin)
```

</details>

#### `openssl sha3-224`

**帮助命令**：`openssl sha3-224 -help`。**用法**：`Usage: sha3-224 [options] [file...]`

**解读**：这是固定摘要名 `sha3-224` 的 `dgst` 入口；文件原始字节作为输入，`-hex` 或 `-binary` 决定输出编码。若使用签名参数，仍须按 [`dgst`](#openssl-dgst) 的签名/验签合同检查密钥与方案。

<details><summary>展开本机 `-help` 内容</summary>

```text
Usage: sha3-224 [options] [file...]

General options:
 -help               Display this summary
 -list               List digests
 -engine val         Use engine e, possibly a hardware device
 -engine_impl        Also use engine given by -engine for digest operations
 -passin val         Input file pass phrase source

Output options:
 -c                  Print the digest with separating colons
 -r                  Print the digest in coreutils format
 -out outfile        Output to filename rather than stdout
 -keyform format     Key file format (ENGINE, other values ignored)
 -hex                Print as hex dump
 -binary             Print in binary form
 -xoflen +int        Output length for XOF algorithms
 -d                  Print debug info
 -debug              Print debug info

Signing options:
 -sign val           Sign digest using private key
 -verify val         Verify a signature using public key
 -prverify val       Verify a signature using private key
 -sigopt val         Signature parameter in n:v form
 -signature infile   File with signature to verify
 -hmac val           Create hashed MAC with key
 -mac val            Create MAC (not necessarily HMAC)
 -macopt val         MAC algorithm parameters in n:v form or key
 -*                  Any supported digest
 -fips-fingerprint   Compute HMAC with the key used in OpenSSL-FIPS fingerprint

Random state options:
 -rand val           Load the given file(s) into the random number generator
 -writerand outfile  Write random data to the specified file

Provider options:
 -provider-path val  Provider load path (must be before 'provider' argument if required)
 -provider val       Provider to load (can be specified multiple times)
 -propquery val      Property query used when fetching algorithms

Parameters:
 file                Files to digest (optional; default is stdin)
```

</details>

#### `openssl sha3-256`

**帮助命令**：`openssl sha3-256 -help`。**用法**：`Usage: sha3-256 [options] [file...]`

**解读**：这是固定摘要名 `sha3-256` 的 `dgst` 入口；文件原始字节作为输入，`-hex` 或 `-binary` 决定输出编码。若使用签名参数，仍须按 [`dgst`](#openssl-dgst) 的签名/验签合同检查密钥与方案。

<details><summary>展开本机 `-help` 内容</summary>

```text
Usage: sha3-256 [options] [file...]

General options:
 -help               Display this summary
 -list               List digests
 -engine val         Use engine e, possibly a hardware device
 -engine_impl        Also use engine given by -engine for digest operations
 -passin val         Input file pass phrase source

Output options:
 -c                  Print the digest with separating colons
 -r                  Print the digest in coreutils format
 -out outfile        Output to filename rather than stdout
 -keyform format     Key file format (ENGINE, other values ignored)
 -hex                Print as hex dump
 -binary             Print in binary form
 -xoflen +int        Output length for XOF algorithms
 -d                  Print debug info
 -debug              Print debug info

Signing options:
 -sign val           Sign digest using private key
 -verify val         Verify a signature using public key
 -prverify val       Verify a signature using private key
 -sigopt val         Signature parameter in n:v form
 -signature infile   File with signature to verify
 -hmac val           Create hashed MAC with key
 -mac val            Create MAC (not necessarily HMAC)
 -macopt val         MAC algorithm parameters in n:v form or key
 -*                  Any supported digest
 -fips-fingerprint   Compute HMAC with the key used in OpenSSL-FIPS fingerprint

Random state options:
 -rand val           Load the given file(s) into the random number generator
 -writerand outfile  Write random data to the specified file

Provider options:
 -provider-path val  Provider load path (must be before 'provider' argument if required)
 -provider val       Provider to load (can be specified multiple times)
 -propquery val      Property query used when fetching algorithms

Parameters:
 file                Files to digest (optional; default is stdin)
```

</details>

#### `openssl sha3-384`

**帮助命令**：`openssl sha3-384 -help`。**用法**：`Usage: sha3-384 [options] [file...]`

**解读**：这是固定摘要名 `sha3-384` 的 `dgst` 入口；文件原始字节作为输入，`-hex` 或 `-binary` 决定输出编码。若使用签名参数，仍须按 [`dgst`](#openssl-dgst) 的签名/验签合同检查密钥与方案。

<details><summary>展开本机 `-help` 内容</summary>

```text
Usage: sha3-384 [options] [file...]

General options:
 -help               Display this summary
 -list               List digests
 -engine val         Use engine e, possibly a hardware device
 -engine_impl        Also use engine given by -engine for digest operations
 -passin val         Input file pass phrase source

Output options:
 -c                  Print the digest with separating colons
 -r                  Print the digest in coreutils format
 -out outfile        Output to filename rather than stdout
 -keyform format     Key file format (ENGINE, other values ignored)
 -hex                Print as hex dump
 -binary             Print in binary form
 -xoflen +int        Output length for XOF algorithms
 -d                  Print debug info
 -debug              Print debug info

Signing options:
 -sign val           Sign digest using private key
 -verify val         Verify a signature using public key
 -prverify val       Verify a signature using private key
 -sigopt val         Signature parameter in n:v form
 -signature infile   File with signature to verify
 -hmac val           Create hashed MAC with key
 -mac val            Create MAC (not necessarily HMAC)
 -macopt val         MAC algorithm parameters in n:v form or key
 -*                  Any supported digest
 -fips-fingerprint   Compute HMAC with the key used in OpenSSL-FIPS fingerprint

Random state options:
 -rand val           Load the given file(s) into the random number generator
 -writerand outfile  Write random data to the specified file

Provider options:
 -provider-path val  Provider load path (must be before 'provider' argument if required)
 -provider val       Provider to load (can be specified multiple times)
 -propquery val      Property query used when fetching algorithms

Parameters:
 file                Files to digest (optional; default is stdin)
```

</details>

#### `openssl sha3-512`

**帮助命令**：`openssl sha3-512 -help`。**用法**：`Usage: sha3-512 [options] [file...]`

**解读**：这是固定摘要名 `sha3-512` 的 `dgst` 入口；文件原始字节作为输入，`-hex` 或 `-binary` 决定输出编码。若使用签名参数，仍须按 [`dgst`](#openssl-dgst) 的签名/验签合同检查密钥与方案。

<details><summary>展开本机 `-help` 内容</summary>

```text
Usage: sha3-512 [options] [file...]

General options:
 -help               Display this summary
 -list               List digests
 -engine val         Use engine e, possibly a hardware device
 -engine_impl        Also use engine given by -engine for digest operations
 -passin val         Input file pass phrase source

Output options:
 -c                  Print the digest with separating colons
 -r                  Print the digest in coreutils format
 -out outfile        Output to filename rather than stdout
 -keyform format     Key file format (ENGINE, other values ignored)
 -hex                Print as hex dump
 -binary             Print in binary form
 -xoflen +int        Output length for XOF algorithms
 -d                  Print debug info
 -debug              Print debug info

Signing options:
 -sign val           Sign digest using private key
 -verify val         Verify a signature using public key
 -prverify val       Verify a signature using private key
 -sigopt val         Signature parameter in n:v form
 -signature infile   File with signature to verify
 -hmac val           Create hashed MAC with key
 -mac val            Create MAC (not necessarily HMAC)
 -macopt val         MAC algorithm parameters in n:v form or key
 -*                  Any supported digest
 -fips-fingerprint   Compute HMAC with the key used in OpenSSL-FIPS fingerprint

Random state options:
 -rand val           Load the given file(s) into the random number generator
 -writerand outfile  Write random data to the specified file

Provider options:
 -provider-path val  Provider load path (must be before 'provider' argument if required)
 -provider val       Provider to load (can be specified multiple times)
 -propquery val      Property query used when fetching algorithms

Parameters:
 file                Files to digest (optional; default is stdin)
```

</details>

#### `openssl sha384`

**帮助命令**：`openssl sha384 -help`。**用法**：`Usage: sha384 [options] [file...]`

**解读**：这是固定摘要名 `sha384` 的 `dgst` 入口；文件原始字节作为输入，`-hex` 或 `-binary` 决定输出编码。若使用签名参数，仍须按 [`dgst`](#openssl-dgst) 的签名/验签合同检查密钥与方案。

<details><summary>展开本机 `-help` 内容</summary>

```text
Usage: sha384 [options] [file...]

General options:
 -help               Display this summary
 -list               List digests
 -engine val         Use engine e, possibly a hardware device
 -engine_impl        Also use engine given by -engine for digest operations
 -passin val         Input file pass phrase source

Output options:
 -c                  Print the digest with separating colons
 -r                  Print the digest in coreutils format
 -out outfile        Output to filename rather than stdout
 -keyform format     Key file format (ENGINE, other values ignored)
 -hex                Print as hex dump
 -binary             Print in binary form
 -xoflen +int        Output length for XOF algorithms
 -d                  Print debug info
 -debug              Print debug info

Signing options:
 -sign val           Sign digest using private key
 -verify val         Verify a signature using public key
 -prverify val       Verify a signature using private key
 -sigopt val         Signature parameter in n:v form
 -signature infile   File with signature to verify
 -hmac val           Create hashed MAC with key
 -mac val            Create MAC (not necessarily HMAC)
 -macopt val         MAC algorithm parameters in n:v form or key
 -*                  Any supported digest
 -fips-fingerprint   Compute HMAC with the key used in OpenSSL-FIPS fingerprint

Random state options:
 -rand val           Load the given file(s) into the random number generator
 -writerand outfile  Write random data to the specified file

Provider options:
 -provider-path val  Provider load path (must be before 'provider' argument if required)
 -provider val       Provider to load (can be specified multiple times)
 -propquery val      Property query used when fetching algorithms

Parameters:
 file                Files to digest (optional; default is stdin)
```

</details>

#### `openssl sha512`

**帮助命令**：`openssl sha512 -help`。**用法**：`Usage: sha512 [options] [file...]`

**解读**：这是固定摘要名 `sha512` 的 `dgst` 入口；文件原始字节作为输入，`-hex` 或 `-binary` 决定输出编码。若使用签名参数，仍须按 [`dgst`](#openssl-dgst) 的签名/验签合同检查密钥与方案。

<details><summary>展开本机 `-help` 内容</summary>

```text
Usage: sha512 [options] [file...]

General options:
 -help               Display this summary
 -list               List digests
 -engine val         Use engine e, possibly a hardware device
 -engine_impl        Also use engine given by -engine for digest operations
 -passin val         Input file pass phrase source

Output options:
 -c                  Print the digest with separating colons
 -r                  Print the digest in coreutils format
 -out outfile        Output to filename rather than stdout
 -keyform format     Key file format (ENGINE, other values ignored)
 -hex                Print as hex dump
 -binary             Print in binary form
 -xoflen +int        Output length for XOF algorithms
 -d                  Print debug info
 -debug              Print debug info

Signing options:
 -sign val           Sign digest using private key
 -verify val         Verify a signature using public key
 -prverify val       Verify a signature using private key
 -sigopt val         Signature parameter in n:v form
 -signature infile   File with signature to verify
 -hmac val           Create hashed MAC with key
 -mac val            Create MAC (not necessarily HMAC)
 -macopt val         MAC algorithm parameters in n:v form or key
 -*                  Any supported digest
 -fips-fingerprint   Compute HMAC with the key used in OpenSSL-FIPS fingerprint

Random state options:
 -rand val           Load the given file(s) into the random number generator
 -writerand outfile  Write random data to the specified file

Provider options:
 -provider-path val  Provider load path (must be before 'provider' argument if required)
 -provider val       Provider to load (can be specified multiple times)
 -propquery val      Property query used when fetching algorithms

Parameters:
 file                Files to digest (optional; default is stdin)
```

</details>

#### `openssl sha512-224`

**帮助命令**：`openssl sha512-224 -help`。**用法**：`Usage: sha512-224 [options] [file...]`

**解读**：这是固定摘要名 `sha512-224` 的 `dgst` 入口；文件原始字节作为输入，`-hex` 或 `-binary` 决定输出编码。若使用签名参数，仍须按 [`dgst`](#openssl-dgst) 的签名/验签合同检查密钥与方案。

<details><summary>展开本机 `-help` 内容</summary>

```text
Usage: sha512-224 [options] [file...]

General options:
 -help               Display this summary
 -list               List digests
 -engine val         Use engine e, possibly a hardware device
 -engine_impl        Also use engine given by -engine for digest operations
 -passin val         Input file pass phrase source

Output options:
 -c                  Print the digest with separating colons
 -r                  Print the digest in coreutils format
 -out outfile        Output to filename rather than stdout
 -keyform format     Key file format (ENGINE, other values ignored)
 -hex                Print as hex dump
 -binary             Print in binary form
 -xoflen +int        Output length for XOF algorithms
 -d                  Print debug info
 -debug              Print debug info

Signing options:
 -sign val           Sign digest using private key
 -verify val         Verify a signature using public key
 -prverify val       Verify a signature using private key
 -sigopt val         Signature parameter in n:v form
 -signature infile   File with signature to verify
 -hmac val           Create hashed MAC with key
 -mac val            Create MAC (not necessarily HMAC)
 -macopt val         MAC algorithm parameters in n:v form or key
 -*                  Any supported digest
 -fips-fingerprint   Compute HMAC with the key used in OpenSSL-FIPS fingerprint

Random state options:
 -rand val           Load the given file(s) into the random number generator
 -writerand outfile  Write random data to the specified file

Provider options:
 -provider-path val  Provider load path (must be before 'provider' argument if required)
 -provider val       Provider to load (can be specified multiple times)
 -propquery val      Property query used when fetching algorithms

Parameters:
 file                Files to digest (optional; default is stdin)
```

</details>

#### `openssl sha512-256`

**帮助命令**：`openssl sha512-256 -help`。**用法**：`Usage: sha512-256 [options] [file...]`

**解读**：这是固定摘要名 `sha512-256` 的 `dgst` 入口；文件原始字节作为输入，`-hex` 或 `-binary` 决定输出编码。若使用签名参数，仍须按 [`dgst`](#openssl-dgst) 的签名/验签合同检查密钥与方案。

<details><summary>展开本机 `-help` 内容</summary>

```text
Usage: sha512-256 [options] [file...]

General options:
 -help               Display this summary
 -list               List digests
 -engine val         Use engine e, possibly a hardware device
 -engine_impl        Also use engine given by -engine for digest operations
 -passin val         Input file pass phrase source

Output options:
 -c                  Print the digest with separating colons
 -r                  Print the digest in coreutils format
 -out outfile        Output to filename rather than stdout
 -keyform format     Key file format (ENGINE, other values ignored)
 -hex                Print as hex dump
 -binary             Print in binary form
 -xoflen +int        Output length for XOF algorithms
 -d                  Print debug info
 -debug              Print debug info

Signing options:
 -sign val           Sign digest using private key
 -verify val         Verify a signature using public key
 -prverify val       Verify a signature using private key
 -sigopt val         Signature parameter in n:v form
 -signature infile   File with signature to verify
 -hmac val           Create hashed MAC with key
 -mac val            Create MAC (not necessarily HMAC)
 -macopt val         MAC algorithm parameters in n:v form or key
 -*                  Any supported digest
 -fips-fingerprint   Compute HMAC with the key used in OpenSSL-FIPS fingerprint

Random state options:
 -rand val           Load the given file(s) into the random number generator
 -writerand outfile  Write random data to the specified file

Provider options:
 -provider-path val  Provider load path (must be before 'provider' argument if required)
 -provider val       Provider to load (can be specified multiple times)
 -propquery val      Property query used when fetching algorithms

Parameters:
 file                Files to digest (optional; default is stdin)
```

</details>

#### `openssl shake128`

**帮助命令**：`openssl shake128 -help`。**用法**：`Usage: shake128 [options] [file...]`

**解读**：这是固定摘要名 `shake128` 的 `dgst` 入口；文件原始字节作为输入，`-hex` 或 `-binary` 决定输出编码。若使用签名参数，仍须按 [`dgst`](#openssl-dgst) 的签名/验签合同检查密钥与方案。

<details><summary>展开本机 `-help` 内容</summary>

```text
Usage: shake128 [options] [file...]

General options:
 -help               Display this summary
 -list               List digests
 -engine val         Use engine e, possibly a hardware device
 -engine_impl        Also use engine given by -engine for digest operations
 -passin val         Input file pass phrase source

Output options:
 -c                  Print the digest with separating colons
 -r                  Print the digest in coreutils format
 -out outfile        Output to filename rather than stdout
 -keyform format     Key file format (ENGINE, other values ignored)
 -hex                Print as hex dump
 -binary             Print in binary form
 -xoflen +int        Output length for XOF algorithms
 -d                  Print debug info
 -debug              Print debug info

Signing options:
 -sign val           Sign digest using private key
 -verify val         Verify a signature using public key
 -prverify val       Verify a signature using private key
 -sigopt val         Signature parameter in n:v form
 -signature infile   File with signature to verify
 -hmac val           Create hashed MAC with key
 -mac val            Create MAC (not necessarily HMAC)
 -macopt val         MAC algorithm parameters in n:v form or key
 -*                  Any supported digest
 -fips-fingerprint   Compute HMAC with the key used in OpenSSL-FIPS fingerprint

Random state options:
 -rand val           Load the given file(s) into the random number generator
 -writerand outfile  Write random data to the specified file

Provider options:
 -provider-path val  Provider load path (must be before 'provider' argument if required)
 -provider val       Provider to load (can be specified multiple times)
 -propquery val      Property query used when fetching algorithms

Parameters:
 file                Files to digest (optional; default is stdin)
```

</details>

#### `openssl shake256`

**帮助命令**：`openssl shake256 -help`。**用法**：`Usage: shake256 [options] [file...]`

**解读**：这是固定摘要名 `shake256` 的 `dgst` 入口；文件原始字节作为输入，`-hex` 或 `-binary` 决定输出编码。若使用签名参数，仍须按 [`dgst`](#openssl-dgst) 的签名/验签合同检查密钥与方案。

<details><summary>展开本机 `-help` 内容</summary>

```text
Usage: shake256 [options] [file...]

General options:
 -help               Display this summary
 -list               List digests
 -engine val         Use engine e, possibly a hardware device
 -engine_impl        Also use engine given by -engine for digest operations
 -passin val         Input file pass phrase source

Output options:
 -c                  Print the digest with separating colons
 -r                  Print the digest in coreutils format
 -out outfile        Output to filename rather than stdout
 -keyform format     Key file format (ENGINE, other values ignored)
 -hex                Print as hex dump
 -binary             Print in binary form
 -xoflen +int        Output length for XOF algorithms
 -d                  Print debug info
 -debug              Print debug info

Signing options:
 -sign val           Sign digest using private key
 -verify val         Verify a signature using public key
 -prverify val       Verify a signature using private key
 -sigopt val         Signature parameter in n:v form
 -signature infile   File with signature to verify
 -hmac val           Create hashed MAC with key
 -mac val            Create MAC (not necessarily HMAC)
 -macopt val         MAC algorithm parameters in n:v form or key
 -*                  Any supported digest
 -fips-fingerprint   Compute HMAC with the key used in OpenSSL-FIPS fingerprint

Random state options:
 -rand val           Load the given file(s) into the random number generator
 -writerand outfile  Write random data to the specified file

Provider options:
 -provider-path val  Provider load path (must be before 'provider' argument if required)
 -provider val       Provider to load (can be specified multiple times)
 -propquery val      Property query used when fetching algorithms

Parameters:
 file                Files to digest (optional; default is stdin)
```

</details>

#### `openssl sm3`

**帮助命令**：`openssl sm3 -help`。**用法**：`Usage: sm3 [options] [file...]`

**解读**：这是固定摘要名 `sm3` 的 `dgst` 入口；文件原始字节作为输入，`-hex` 或 `-binary` 决定输出编码。若使用签名参数，仍须按 [`dgst`](#openssl-dgst) 的签名/验签合同检查密钥与方案。

<details><summary>展开本机 `-help` 内容</summary>

```text
Usage: sm3 [options] [file...]

General options:
 -help               Display this summary
 -list               List digests
 -engine val         Use engine e, possibly a hardware device
 -engine_impl        Also use engine given by -engine for digest operations
 -passin val         Input file pass phrase source

Output options:
 -c                  Print the digest with separating colons
 -r                  Print the digest in coreutils format
 -out outfile        Output to filename rather than stdout
 -keyform format     Key file format (ENGINE, other values ignored)
 -hex                Print as hex dump
 -binary             Print in binary form
 -xoflen +int        Output length for XOF algorithms
 -d                  Print debug info
 -debug              Print debug info

Signing options:
 -sign val           Sign digest using private key
 -verify val         Verify a signature using public key
 -prverify val       Verify a signature using private key
 -sigopt val         Signature parameter in n:v form
 -signature infile   File with signature to verify
 -hmac val           Create hashed MAC with key
 -mac val            Create MAC (not necessarily HMAC)
 -macopt val         MAC algorithm parameters in n:v form or key
 -*                  Any supported digest
 -fips-fingerprint   Compute HMAC with the key used in OpenSSL-FIPS fingerprint

Random state options:
 -rand val           Load the given file(s) into the random number generator
 -writerand outfile  Write random data to the specified file

Provider options:
 -provider-path val  Provider load path (must be before 'provider' argument if required)
 -provider val       Provider to load (can be specified multiple times)
 -propquery val      Property query used when fetching algorithms

Parameters:
 file                Files to digest (optional; default is stdin)
```

</details>

### 加密与编码别名

参数说明见 `openssl enc -help`。下表的每条 `-help` 均已在本机执行并返回退出码 0。

| 别名 | 对应帮助命令 | 本机 Usage |
|---|---|---|
| `aes-128-cbc` | `openssl aes-128-cbc -help` | `Usage: aes-128-cbc [options]` |
| `aes-128-ecb` | `openssl aes-128-ecb -help` | `Usage: aes-128-ecb [options]` |
| `aes-192-cbc` | `openssl aes-192-cbc -help` | `Usage: aes-192-cbc [options]` |
| `aes-192-ecb` | `openssl aes-192-ecb -help` | `Usage: aes-192-ecb [options]` |
| `aes-256-cbc` | `openssl aes-256-cbc -help` | `Usage: aes-256-cbc [options]` |
| `aes-256-ecb` | `openssl aes-256-ecb -help` | `Usage: aes-256-ecb [options]` |
| `aria-128-cbc` | `openssl aria-128-cbc -help` | `Usage: aria-128-cbc [options]` |
| `aria-128-cfb` | `openssl aria-128-cfb -help` | `Usage: aria-128-cfb [options]` |
| `aria-128-cfb1` | `openssl aria-128-cfb1 -help` | `Usage: aria-128-cfb1 [options]` |
| `aria-128-cfb8` | `openssl aria-128-cfb8 -help` | `Usage: aria-128-cfb8 [options]` |
| `aria-128-ctr` | `openssl aria-128-ctr -help` | `Usage: aria-128-ctr [options]` |
| `aria-128-ecb` | `openssl aria-128-ecb -help` | `Usage: aria-128-ecb [options]` |
| `aria-128-ofb` | `openssl aria-128-ofb -help` | `Usage: aria-128-ofb [options]` |
| `aria-192-cbc` | `openssl aria-192-cbc -help` | `Usage: aria-192-cbc [options]` |
| `aria-192-cfb` | `openssl aria-192-cfb -help` | `Usage: aria-192-cfb [options]` |
| `aria-192-cfb1` | `openssl aria-192-cfb1 -help` | `Usage: aria-192-cfb1 [options]` |
| `aria-192-cfb8` | `openssl aria-192-cfb8 -help` | `Usage: aria-192-cfb8 [options]` |
| `aria-192-ctr` | `openssl aria-192-ctr -help` | `Usage: aria-192-ctr [options]` |
| `aria-192-ecb` | `openssl aria-192-ecb -help` | `Usage: aria-192-ecb [options]` |
| `aria-192-ofb` | `openssl aria-192-ofb -help` | `Usage: aria-192-ofb [options]` |
| `aria-256-cbc` | `openssl aria-256-cbc -help` | `Usage: aria-256-cbc [options]` |
| `aria-256-cfb` | `openssl aria-256-cfb -help` | `Usage: aria-256-cfb [options]` |
| `aria-256-cfb1` | `openssl aria-256-cfb1 -help` | `Usage: aria-256-cfb1 [options]` |
| `aria-256-cfb8` | `openssl aria-256-cfb8 -help` | `Usage: aria-256-cfb8 [options]` |
| `aria-256-ctr` | `openssl aria-256-ctr -help` | `Usage: aria-256-ctr [options]` |
| `aria-256-ecb` | `openssl aria-256-ecb -help` | `Usage: aria-256-ecb [options]` |
| `aria-256-ofb` | `openssl aria-256-ofb -help` | `Usage: aria-256-ofb [options]` |
| `base64` | `openssl base64 -help` | `Usage: base64 [options]` |
| `bf` | `openssl bf -help` | `Usage: bf [options]` |
| `bf-cbc` | `openssl bf-cbc -help` | `Usage: bf-cbc [options]` |
| `bf-cfb` | `openssl bf-cfb -help` | `Usage: bf-cfb [options]` |
| `bf-ecb` | `openssl bf-ecb -help` | `Usage: bf-ecb [options]` |
| `bf-ofb` | `openssl bf-ofb -help` | `Usage: bf-ofb [options]` |
| `camellia-128-cbc` | `openssl camellia-128-cbc -help` | `Usage: camellia-128-cbc [options]` |
| `camellia-128-ecb` | `openssl camellia-128-ecb -help` | `Usage: camellia-128-ecb [options]` |
| `camellia-192-cbc` | `openssl camellia-192-cbc -help` | `Usage: camellia-192-cbc [options]` |
| `camellia-192-ecb` | `openssl camellia-192-ecb -help` | `Usage: camellia-192-ecb [options]` |
| `camellia-256-cbc` | `openssl camellia-256-cbc -help` | `Usage: camellia-256-cbc [options]` |
| `camellia-256-ecb` | `openssl camellia-256-ecb -help` | `Usage: camellia-256-ecb [options]` |
| `cast` | `openssl cast -help` | `Usage: cast [options]` |
| `cast-cbc` | `openssl cast-cbc -help` | `Usage: cast-cbc [options]` |
| `cast5-cbc` | `openssl cast5-cbc -help` | `Usage: cast5-cbc [options]` |
| `cast5-cfb` | `openssl cast5-cfb -help` | `Usage: cast5-cfb [options]` |
| `cast5-ecb` | `openssl cast5-ecb -help` | `Usage: cast5-ecb [options]` |
| `cast5-ofb` | `openssl cast5-ofb -help` | `Usage: cast5-ofb [options]` |
| `des` | `openssl des -help` | `Usage: des [options]` |
| `des-cbc` | `openssl des-cbc -help` | `Usage: des-cbc [options]` |
| `des-cfb` | `openssl des-cfb -help` | `Usage: des-cfb [options]` |
| `des-ecb` | `openssl des-ecb -help` | `Usage: des-ecb [options]` |
| `des-ede` | `openssl des-ede -help` | `Usage: des-ede [options]` |
| `des-ede-cbc` | `openssl des-ede-cbc -help` | `Usage: des-ede-cbc [options]` |
| `des-ede-cfb` | `openssl des-ede-cfb -help` | `Usage: des-ede-cfb [options]` |
| `des-ede-ofb` | `openssl des-ede-ofb -help` | `Usage: des-ede-ofb [options]` |
| `des-ede3` | `openssl des-ede3 -help` | `Usage: des-ede3 [options]` |
| `des-ede3-cbc` | `openssl des-ede3-cbc -help` | `Usage: des-ede3-cbc [options]` |
| `des-ede3-cfb` | `openssl des-ede3-cfb -help` | `Usage: des-ede3-cfb [options]` |
| `des-ede3-ofb` | `openssl des-ede3-ofb -help` | `Usage: des-ede3-ofb [options]` |
| `des-ofb` | `openssl des-ofb -help` | `Usage: des-ofb [options]` |
| `des3` | `openssl des3 -help` | `Usage: des3 [options]` |
| `desx` | `openssl desx -help` | `Usage: desx [options]` |
| `rc2` | `openssl rc2 -help` | `Usage: rc2 [options]` |
| `rc2-40-cbc` | `openssl rc2-40-cbc -help` | `Usage: rc2-40-cbc [options]` |
| `rc2-64-cbc` | `openssl rc2-64-cbc -help` | `Usage: rc2-64-cbc [options]` |
| `rc2-cbc` | `openssl rc2-cbc -help` | `Usage: rc2-cbc [options]` |
| `rc2-cfb` | `openssl rc2-cfb -help` | `Usage: rc2-cfb [options]` |
| `rc2-ecb` | `openssl rc2-ecb -help` | `Usage: rc2-ecb [options]` |
| `rc2-ofb` | `openssl rc2-ofb -help` | `Usage: rc2-ofb [options]` |
| `rc4` | `openssl rc4 -help` | `Usage: rc4 [options]` |
| `rc4-40` | `openssl rc4-40 -help` | `Usage: rc4-40 [options]` |
| `seed` | `openssl seed -help` | `Usage: seed [options]` |
| `seed-cbc` | `openssl seed-cbc -help` | `Usage: seed-cbc [options]` |
| `seed-cfb` | `openssl seed-cfb -help` | `Usage: seed-cfb [options]` |
| `seed-ecb` | `openssl seed-ecb -help` | `Usage: seed-ecb [options]` |
| `seed-ofb` | `openssl seed-ofb -help` | `Usage: seed-ofb [options]` |
| `sm4-cbc` | `openssl sm4-cbc -help` | `Usage: sm4-cbc [options]` |
| `sm4-cfb` | `openssl sm4-cfb -help` | `Usage: sm4-cfb [options]` |
| `sm4-ctr` | `openssl sm4-ctr -help` | `Usage: sm4-ctr [options]` |
| `sm4-ecb` | `openssl sm4-ecb -help` | `Usage: sm4-ecb [options]` |
| `sm4-ofb` | `openssl sm4-ofb -help` | `Usage: sm4-ofb [options]` |

#### `openssl aes-128-cbc`

**帮助命令**：`openssl aes-128-cbc -help`。**用法**：`Usage: aes-128-cbc [options]`

**解读**：这是固定密码名称 `aes-128-cbc` 的 `enc` 入口；`-e`/`-d` 控制文件加解密，密钥或口令、IV、输入输出必须按 [`enc`](#openssl-enc) 说明固定。帮助可见不等于本项目允许该算法或模式。

<details><summary>展开本机 `-help` 内容</summary>

```text
Usage: aes-128-cbc [options]

General options:
 -help               Display this summary
 -list               List ciphers
 -ciphers            Alias for -list
 -e                  Encrypt
 -d                  Decrypt
 -p                  Print the iv/key
 -P                  Print the iv/key and exit
 -engine val         Use engine, possibly a hardware device

Input options:
 -in infile          Input file
 -k val              Passphrase
 -kfile infile       Read passphrase from file

Output options:
 -out outfile        Output file
 -pass val           Passphrase source
 -v                  Verbose output
 -a                  Base64 encode/decode, depending on encryption flag
 -base64             Same as option -a
 -A                  Used with -[base64|a] to specify base64 buffer as a single line

Encryption options:
 -nopad              Disable standard block padding
 -salt               Use salt in the KDF (default)
 -nosalt             Do not use salt in the KDF
 -debug              Print debug info
 -bufsize val        Buffer size
 -K val              Raw key, in hex
 -S val              Salt, in hex
 -iv val             IV in hex
 -md val             Use specified digest to create a key from the passphrase
 -iter +int          Specify the iteration count and force use of PBKDF2
 -pbkdf2             Use password-based key derivation function 2
 -none               Don't encrypt
 -*                  Any supported cipher

Random state options:
 -rand val           Load the given file(s) into the random number generator
 -writerand outfile  Write random data to the specified file

Provider options:
 -provider-path val  Provider load path (must be before 'provider' argument if required)
 -provider val       Provider to load (can be specified multiple times)
 -propquery val      Property query used when fetching algorithms
```

</details>

#### `openssl aes-128-ecb`

**帮助命令**：`openssl aes-128-ecb -help`。**用法**：`Usage: aes-128-ecb [options]`

**解读**：这是固定密码名称 `aes-128-ecb` 的 `enc` 入口；`-e`/`-d` 控制文件加解密，密钥或口令、IV、输入输出必须按 [`enc`](#openssl-enc) 说明固定。帮助可见不等于本项目允许该算法或模式。

<details><summary>展开本机 `-help` 内容</summary>

```text
Usage: aes-128-ecb [options]

General options:
 -help               Display this summary
 -list               List ciphers
 -ciphers            Alias for -list
 -e                  Encrypt
 -d                  Decrypt
 -p                  Print the iv/key
 -P                  Print the iv/key and exit
 -engine val         Use engine, possibly a hardware device

Input options:
 -in infile          Input file
 -k val              Passphrase
 -kfile infile       Read passphrase from file

Output options:
 -out outfile        Output file
 -pass val           Passphrase source
 -v                  Verbose output
 -a                  Base64 encode/decode, depending on encryption flag
 -base64             Same as option -a
 -A                  Used with -[base64|a] to specify base64 buffer as a single line

Encryption options:
 -nopad              Disable standard block padding
 -salt               Use salt in the KDF (default)
 -nosalt             Do not use salt in the KDF
 -debug              Print debug info
 -bufsize val        Buffer size
 -K val              Raw key, in hex
 -S val              Salt, in hex
 -iv val             IV in hex
 -md val             Use specified digest to create a key from the passphrase
 -iter +int          Specify the iteration count and force use of PBKDF2
 -pbkdf2             Use password-based key derivation function 2
 -none               Don't encrypt
 -*                  Any supported cipher

Random state options:
 -rand val           Load the given file(s) into the random number generator
 -writerand outfile  Write random data to the specified file

Provider options:
 -provider-path val  Provider load path (must be before 'provider' argument if required)
 -provider val       Provider to load (can be specified multiple times)
 -propquery val      Property query used when fetching algorithms
```

</details>

#### `openssl aes-192-cbc`

**帮助命令**：`openssl aes-192-cbc -help`。**用法**：`Usage: aes-192-cbc [options]`

**解读**：这是固定密码名称 `aes-192-cbc` 的 `enc` 入口；`-e`/`-d` 控制文件加解密，密钥或口令、IV、输入输出必须按 [`enc`](#openssl-enc) 说明固定。帮助可见不等于本项目允许该算法或模式。

<details><summary>展开本机 `-help` 内容</summary>

```text
Usage: aes-192-cbc [options]

General options:
 -help               Display this summary
 -list               List ciphers
 -ciphers            Alias for -list
 -e                  Encrypt
 -d                  Decrypt
 -p                  Print the iv/key
 -P                  Print the iv/key and exit
 -engine val         Use engine, possibly a hardware device

Input options:
 -in infile          Input file
 -k val              Passphrase
 -kfile infile       Read passphrase from file

Output options:
 -out outfile        Output file
 -pass val           Passphrase source
 -v                  Verbose output
 -a                  Base64 encode/decode, depending on encryption flag
 -base64             Same as option -a
 -A                  Used with -[base64|a] to specify base64 buffer as a single line

Encryption options:
 -nopad              Disable standard block padding
 -salt               Use salt in the KDF (default)
 -nosalt             Do not use salt in the KDF
 -debug              Print debug info
 -bufsize val        Buffer size
 -K val              Raw key, in hex
 -S val              Salt, in hex
 -iv val             IV in hex
 -md val             Use specified digest to create a key from the passphrase
 -iter +int          Specify the iteration count and force use of PBKDF2
 -pbkdf2             Use password-based key derivation function 2
 -none               Don't encrypt
 -*                  Any supported cipher

Random state options:
 -rand val           Load the given file(s) into the random number generator
 -writerand outfile  Write random data to the specified file

Provider options:
 -provider-path val  Provider load path (must be before 'provider' argument if required)
 -provider val       Provider to load (can be specified multiple times)
 -propquery val      Property query used when fetching algorithms
```

</details>

#### `openssl aes-192-ecb`

**帮助命令**：`openssl aes-192-ecb -help`。**用法**：`Usage: aes-192-ecb [options]`

**解读**：这是固定密码名称 `aes-192-ecb` 的 `enc` 入口；`-e`/`-d` 控制文件加解密，密钥或口令、IV、输入输出必须按 [`enc`](#openssl-enc) 说明固定。帮助可见不等于本项目允许该算法或模式。

<details><summary>展开本机 `-help` 内容</summary>

```text
Usage: aes-192-ecb [options]

General options:
 -help               Display this summary
 -list               List ciphers
 -ciphers            Alias for -list
 -e                  Encrypt
 -d                  Decrypt
 -p                  Print the iv/key
 -P                  Print the iv/key and exit
 -engine val         Use engine, possibly a hardware device

Input options:
 -in infile          Input file
 -k val              Passphrase
 -kfile infile       Read passphrase from file

Output options:
 -out outfile        Output file
 -pass val           Passphrase source
 -v                  Verbose output
 -a                  Base64 encode/decode, depending on encryption flag
 -base64             Same as option -a
 -A                  Used with -[base64|a] to specify base64 buffer as a single line

Encryption options:
 -nopad              Disable standard block padding
 -salt               Use salt in the KDF (default)
 -nosalt             Do not use salt in the KDF
 -debug              Print debug info
 -bufsize val        Buffer size
 -K val              Raw key, in hex
 -S val              Salt, in hex
 -iv val             IV in hex
 -md val             Use specified digest to create a key from the passphrase
 -iter +int          Specify the iteration count and force use of PBKDF2
 -pbkdf2             Use password-based key derivation function 2
 -none               Don't encrypt
 -*                  Any supported cipher

Random state options:
 -rand val           Load the given file(s) into the random number generator
 -writerand outfile  Write random data to the specified file

Provider options:
 -provider-path val  Provider load path (must be before 'provider' argument if required)
 -provider val       Provider to load (can be specified multiple times)
 -propquery val      Property query used when fetching algorithms
```

</details>

#### `openssl aes-256-cbc`

**帮助命令**：`openssl aes-256-cbc -help`。**用法**：`Usage: aes-256-cbc [options]`

**解读**：这是固定密码名称 `aes-256-cbc` 的 `enc` 入口；`-e`/`-d` 控制文件加解密，密钥或口令、IV、输入输出必须按 [`enc`](#openssl-enc) 说明固定。帮助可见不等于本项目允许该算法或模式。

<details><summary>展开本机 `-help` 内容</summary>

```text
Usage: aes-256-cbc [options]

General options:
 -help               Display this summary
 -list               List ciphers
 -ciphers            Alias for -list
 -e                  Encrypt
 -d                  Decrypt
 -p                  Print the iv/key
 -P                  Print the iv/key and exit
 -engine val         Use engine, possibly a hardware device

Input options:
 -in infile          Input file
 -k val              Passphrase
 -kfile infile       Read passphrase from file

Output options:
 -out outfile        Output file
 -pass val           Passphrase source
 -v                  Verbose output
 -a                  Base64 encode/decode, depending on encryption flag
 -base64             Same as option -a
 -A                  Used with -[base64|a] to specify base64 buffer as a single line

Encryption options:
 -nopad              Disable standard block padding
 -salt               Use salt in the KDF (default)
 -nosalt             Do not use salt in the KDF
 -debug              Print debug info
 -bufsize val        Buffer size
 -K val              Raw key, in hex
 -S val              Salt, in hex
 -iv val             IV in hex
 -md val             Use specified digest to create a key from the passphrase
 -iter +int          Specify the iteration count and force use of PBKDF2
 -pbkdf2             Use password-based key derivation function 2
 -none               Don't encrypt
 -*                  Any supported cipher

Random state options:
 -rand val           Load the given file(s) into the random number generator
 -writerand outfile  Write random data to the specified file

Provider options:
 -provider-path val  Provider load path (must be before 'provider' argument if required)
 -provider val       Provider to load (can be specified multiple times)
 -propquery val      Property query used when fetching algorithms
```

</details>

#### `openssl aes-256-ecb`

**帮助命令**：`openssl aes-256-ecb -help`。**用法**：`Usage: aes-256-ecb [options]`

**解读**：这是固定密码名称 `aes-256-ecb` 的 `enc` 入口；`-e`/`-d` 控制文件加解密，密钥或口令、IV、输入输出必须按 [`enc`](#openssl-enc) 说明固定。帮助可见不等于本项目允许该算法或模式。

<details><summary>展开本机 `-help` 内容</summary>

```text
Usage: aes-256-ecb [options]

General options:
 -help               Display this summary
 -list               List ciphers
 -ciphers            Alias for -list
 -e                  Encrypt
 -d                  Decrypt
 -p                  Print the iv/key
 -P                  Print the iv/key and exit
 -engine val         Use engine, possibly a hardware device

Input options:
 -in infile          Input file
 -k val              Passphrase
 -kfile infile       Read passphrase from file

Output options:
 -out outfile        Output file
 -pass val           Passphrase source
 -v                  Verbose output
 -a                  Base64 encode/decode, depending on encryption flag
 -base64             Same as option -a
 -A                  Used with -[base64|a] to specify base64 buffer as a single line

Encryption options:
 -nopad              Disable standard block padding
 -salt               Use salt in the KDF (default)
 -nosalt             Do not use salt in the KDF
 -debug              Print debug info
 -bufsize val        Buffer size
 -K val              Raw key, in hex
 -S val              Salt, in hex
 -iv val             IV in hex
 -md val             Use specified digest to create a key from the passphrase
 -iter +int          Specify the iteration count and force use of PBKDF2
 -pbkdf2             Use password-based key derivation function 2
 -none               Don't encrypt
 -*                  Any supported cipher

Random state options:
 -rand val           Load the given file(s) into the random number generator
 -writerand outfile  Write random data to the specified file

Provider options:
 -provider-path val  Provider load path (must be before 'provider' argument if required)
 -provider val       Provider to load (can be specified multiple times)
 -propquery val      Property query used when fetching algorithms
```

</details>

#### `openssl aria-128-cbc`

**帮助命令**：`openssl aria-128-cbc -help`。**用法**：`Usage: aria-128-cbc [options]`

**解读**：这是固定密码名称 `aria-128-cbc` 的 `enc` 入口；`-e`/`-d` 控制文件加解密，密钥或口令、IV、输入输出必须按 [`enc`](#openssl-enc) 说明固定。帮助可见不等于本项目允许该算法或模式。

<details><summary>展开本机 `-help` 内容</summary>

```text
Usage: aria-128-cbc [options]

General options:
 -help               Display this summary
 -list               List ciphers
 -ciphers            Alias for -list
 -e                  Encrypt
 -d                  Decrypt
 -p                  Print the iv/key
 -P                  Print the iv/key and exit
 -engine val         Use engine, possibly a hardware device

Input options:
 -in infile          Input file
 -k val              Passphrase
 -kfile infile       Read passphrase from file

Output options:
 -out outfile        Output file
 -pass val           Passphrase source
 -v                  Verbose output
 -a                  Base64 encode/decode, depending on encryption flag
 -base64             Same as option -a
 -A                  Used with -[base64|a] to specify base64 buffer as a single line

Encryption options:
 -nopad              Disable standard block padding
 -salt               Use salt in the KDF (default)
 -nosalt             Do not use salt in the KDF
 -debug              Print debug info
 -bufsize val        Buffer size
 -K val              Raw key, in hex
 -S val              Salt, in hex
 -iv val             IV in hex
 -md val             Use specified digest to create a key from the passphrase
 -iter +int          Specify the iteration count and force use of PBKDF2
 -pbkdf2             Use password-based key derivation function 2
 -none               Don't encrypt
 -*                  Any supported cipher

Random state options:
 -rand val           Load the given file(s) into the random number generator
 -writerand outfile  Write random data to the specified file

Provider options:
 -provider-path val  Provider load path (must be before 'provider' argument if required)
 -provider val       Provider to load (can be specified multiple times)
 -propquery val      Property query used when fetching algorithms
```

</details>

#### `openssl aria-128-cfb`

**帮助命令**：`openssl aria-128-cfb -help`。**用法**：`Usage: aria-128-cfb [options]`

**解读**：这是固定密码名称 `aria-128-cfb` 的 `enc` 入口；`-e`/`-d` 控制文件加解密，密钥或口令、IV、输入输出必须按 [`enc`](#openssl-enc) 说明固定。帮助可见不等于本项目允许该算法或模式。

<details><summary>展开本机 `-help` 内容</summary>

```text
Usage: aria-128-cfb [options]

General options:
 -help               Display this summary
 -list               List ciphers
 -ciphers            Alias for -list
 -e                  Encrypt
 -d                  Decrypt
 -p                  Print the iv/key
 -P                  Print the iv/key and exit
 -engine val         Use engine, possibly a hardware device

Input options:
 -in infile          Input file
 -k val              Passphrase
 -kfile infile       Read passphrase from file

Output options:
 -out outfile        Output file
 -pass val           Passphrase source
 -v                  Verbose output
 -a                  Base64 encode/decode, depending on encryption flag
 -base64             Same as option -a
 -A                  Used with -[base64|a] to specify base64 buffer as a single line

Encryption options:
 -nopad              Disable standard block padding
 -salt               Use salt in the KDF (default)
 -nosalt             Do not use salt in the KDF
 -debug              Print debug info
 -bufsize val        Buffer size
 -K val              Raw key, in hex
 -S val              Salt, in hex
 -iv val             IV in hex
 -md val             Use specified digest to create a key from the passphrase
 -iter +int          Specify the iteration count and force use of PBKDF2
 -pbkdf2             Use password-based key derivation function 2
 -none               Don't encrypt
 -*                  Any supported cipher

Random state options:
 -rand val           Load the given file(s) into the random number generator
 -writerand outfile  Write random data to the specified file

Provider options:
 -provider-path val  Provider load path (must be before 'provider' argument if required)
 -provider val       Provider to load (can be specified multiple times)
 -propquery val      Property query used when fetching algorithms
```

</details>

#### `openssl aria-128-cfb1`

**帮助命令**：`openssl aria-128-cfb1 -help`。**用法**：`Usage: aria-128-cfb1 [options]`

**解读**：这是固定密码名称 `aria-128-cfb1` 的 `enc` 入口；`-e`/`-d` 控制文件加解密，密钥或口令、IV、输入输出必须按 [`enc`](#openssl-enc) 说明固定。帮助可见不等于本项目允许该算法或模式。

<details><summary>展开本机 `-help` 内容</summary>

```text
Usage: aria-128-cfb1 [options]

General options:
 -help               Display this summary
 -list               List ciphers
 -ciphers            Alias for -list
 -e                  Encrypt
 -d                  Decrypt
 -p                  Print the iv/key
 -P                  Print the iv/key and exit
 -engine val         Use engine, possibly a hardware device

Input options:
 -in infile          Input file
 -k val              Passphrase
 -kfile infile       Read passphrase from file

Output options:
 -out outfile        Output file
 -pass val           Passphrase source
 -v                  Verbose output
 -a                  Base64 encode/decode, depending on encryption flag
 -base64             Same as option -a
 -A                  Used with -[base64|a] to specify base64 buffer as a single line

Encryption options:
 -nopad              Disable standard block padding
 -salt               Use salt in the KDF (default)
 -nosalt             Do not use salt in the KDF
 -debug              Print debug info
 -bufsize val        Buffer size
 -K val              Raw key, in hex
 -S val              Salt, in hex
 -iv val             IV in hex
 -md val             Use specified digest to create a key from the passphrase
 -iter +int          Specify the iteration count and force use of PBKDF2
 -pbkdf2             Use password-based key derivation function 2
 -none               Don't encrypt
 -*                  Any supported cipher

Random state options:
 -rand val           Load the given file(s) into the random number generator
 -writerand outfile  Write random data to the specified file

Provider options:
 -provider-path val  Provider load path (must be before 'provider' argument if required)
 -provider val       Provider to load (can be specified multiple times)
 -propquery val      Property query used when fetching algorithms
```

</details>

#### `openssl aria-128-cfb8`

**帮助命令**：`openssl aria-128-cfb8 -help`。**用法**：`Usage: aria-128-cfb8 [options]`

**解读**：这是固定密码名称 `aria-128-cfb8` 的 `enc` 入口；`-e`/`-d` 控制文件加解密，密钥或口令、IV、输入输出必须按 [`enc`](#openssl-enc) 说明固定。帮助可见不等于本项目允许该算法或模式。

<details><summary>展开本机 `-help` 内容</summary>

```text
Usage: aria-128-cfb8 [options]

General options:
 -help               Display this summary
 -list               List ciphers
 -ciphers            Alias for -list
 -e                  Encrypt
 -d                  Decrypt
 -p                  Print the iv/key
 -P                  Print the iv/key and exit
 -engine val         Use engine, possibly a hardware device

Input options:
 -in infile          Input file
 -k val              Passphrase
 -kfile infile       Read passphrase from file

Output options:
 -out outfile        Output file
 -pass val           Passphrase source
 -v                  Verbose output
 -a                  Base64 encode/decode, depending on encryption flag
 -base64             Same as option -a
 -A                  Used with -[base64|a] to specify base64 buffer as a single line

Encryption options:
 -nopad              Disable standard block padding
 -salt               Use salt in the KDF (default)
 -nosalt             Do not use salt in the KDF
 -debug              Print debug info
 -bufsize val        Buffer size
 -K val              Raw key, in hex
 -S val              Salt, in hex
 -iv val             IV in hex
 -md val             Use specified digest to create a key from the passphrase
 -iter +int          Specify the iteration count and force use of PBKDF2
 -pbkdf2             Use password-based key derivation function 2
 -none               Don't encrypt
 -*                  Any supported cipher

Random state options:
 -rand val           Load the given file(s) into the random number generator
 -writerand outfile  Write random data to the specified file

Provider options:
 -provider-path val  Provider load path (must be before 'provider' argument if required)
 -provider val       Provider to load (can be specified multiple times)
 -propquery val      Property query used when fetching algorithms
```

</details>

#### `openssl aria-128-ctr`

**帮助命令**：`openssl aria-128-ctr -help`。**用法**：`Usage: aria-128-ctr [options]`

**解读**：这是固定密码名称 `aria-128-ctr` 的 `enc` 入口；`-e`/`-d` 控制文件加解密，密钥或口令、IV、输入输出必须按 [`enc`](#openssl-enc) 说明固定。帮助可见不等于本项目允许该算法或模式。

<details><summary>展开本机 `-help` 内容</summary>

```text
Usage: aria-128-ctr [options]

General options:
 -help               Display this summary
 -list               List ciphers
 -ciphers            Alias for -list
 -e                  Encrypt
 -d                  Decrypt
 -p                  Print the iv/key
 -P                  Print the iv/key and exit
 -engine val         Use engine, possibly a hardware device

Input options:
 -in infile          Input file
 -k val              Passphrase
 -kfile infile       Read passphrase from file

Output options:
 -out outfile        Output file
 -pass val           Passphrase source
 -v                  Verbose output
 -a                  Base64 encode/decode, depending on encryption flag
 -base64             Same as option -a
 -A                  Used with -[base64|a] to specify base64 buffer as a single line

Encryption options:
 -nopad              Disable standard block padding
 -salt               Use salt in the KDF (default)
 -nosalt             Do not use salt in the KDF
 -debug              Print debug info
 -bufsize val        Buffer size
 -K val              Raw key, in hex
 -S val              Salt, in hex
 -iv val             IV in hex
 -md val             Use specified digest to create a key from the passphrase
 -iter +int          Specify the iteration count and force use of PBKDF2
 -pbkdf2             Use password-based key derivation function 2
 -none               Don't encrypt
 -*                  Any supported cipher

Random state options:
 -rand val           Load the given file(s) into the random number generator
 -writerand outfile  Write random data to the specified file

Provider options:
 -provider-path val  Provider load path (must be before 'provider' argument if required)
 -provider val       Provider to load (can be specified multiple times)
 -propquery val      Property query used when fetching algorithms
```

</details>

#### `openssl aria-128-ecb`

**帮助命令**：`openssl aria-128-ecb -help`。**用法**：`Usage: aria-128-ecb [options]`

**解读**：这是固定密码名称 `aria-128-ecb` 的 `enc` 入口；`-e`/`-d` 控制文件加解密，密钥或口令、IV、输入输出必须按 [`enc`](#openssl-enc) 说明固定。帮助可见不等于本项目允许该算法或模式。

<details><summary>展开本机 `-help` 内容</summary>

```text
Usage: aria-128-ecb [options]

General options:
 -help               Display this summary
 -list               List ciphers
 -ciphers            Alias for -list
 -e                  Encrypt
 -d                  Decrypt
 -p                  Print the iv/key
 -P                  Print the iv/key and exit
 -engine val         Use engine, possibly a hardware device

Input options:
 -in infile          Input file
 -k val              Passphrase
 -kfile infile       Read passphrase from file

Output options:
 -out outfile        Output file
 -pass val           Passphrase source
 -v                  Verbose output
 -a                  Base64 encode/decode, depending on encryption flag
 -base64             Same as option -a
 -A                  Used with -[base64|a] to specify base64 buffer as a single line

Encryption options:
 -nopad              Disable standard block padding
 -salt               Use salt in the KDF (default)
 -nosalt             Do not use salt in the KDF
 -debug              Print debug info
 -bufsize val        Buffer size
 -K val              Raw key, in hex
 -S val              Salt, in hex
 -iv val             IV in hex
 -md val             Use specified digest to create a key from the passphrase
 -iter +int          Specify the iteration count and force use of PBKDF2
 -pbkdf2             Use password-based key derivation function 2
 -none               Don't encrypt
 -*                  Any supported cipher

Random state options:
 -rand val           Load the given file(s) into the random number generator
 -writerand outfile  Write random data to the specified file

Provider options:
 -provider-path val  Provider load path (must be before 'provider' argument if required)
 -provider val       Provider to load (can be specified multiple times)
 -propquery val      Property query used when fetching algorithms
```

</details>

#### `openssl aria-128-ofb`

**帮助命令**：`openssl aria-128-ofb -help`。**用法**：`Usage: aria-128-ofb [options]`

**解读**：这是固定密码名称 `aria-128-ofb` 的 `enc` 入口；`-e`/`-d` 控制文件加解密，密钥或口令、IV、输入输出必须按 [`enc`](#openssl-enc) 说明固定。帮助可见不等于本项目允许该算法或模式。

<details><summary>展开本机 `-help` 内容</summary>

```text
Usage: aria-128-ofb [options]

General options:
 -help               Display this summary
 -list               List ciphers
 -ciphers            Alias for -list
 -e                  Encrypt
 -d                  Decrypt
 -p                  Print the iv/key
 -P                  Print the iv/key and exit
 -engine val         Use engine, possibly a hardware device

Input options:
 -in infile          Input file
 -k val              Passphrase
 -kfile infile       Read passphrase from file

Output options:
 -out outfile        Output file
 -pass val           Passphrase source
 -v                  Verbose output
 -a                  Base64 encode/decode, depending on encryption flag
 -base64             Same as option -a
 -A                  Used with -[base64|a] to specify base64 buffer as a single line

Encryption options:
 -nopad              Disable standard block padding
 -salt               Use salt in the KDF (default)
 -nosalt             Do not use salt in the KDF
 -debug              Print debug info
 -bufsize val        Buffer size
 -K val              Raw key, in hex
 -S val              Salt, in hex
 -iv val             IV in hex
 -md val             Use specified digest to create a key from the passphrase
 -iter +int          Specify the iteration count and force use of PBKDF2
 -pbkdf2             Use password-based key derivation function 2
 -none               Don't encrypt
 -*                  Any supported cipher

Random state options:
 -rand val           Load the given file(s) into the random number generator
 -writerand outfile  Write random data to the specified file

Provider options:
 -provider-path val  Provider load path (must be before 'provider' argument if required)
 -provider val       Provider to load (can be specified multiple times)
 -propquery val      Property query used when fetching algorithms
```

</details>

#### `openssl aria-192-cbc`

**帮助命令**：`openssl aria-192-cbc -help`。**用法**：`Usage: aria-192-cbc [options]`

**解读**：这是固定密码名称 `aria-192-cbc` 的 `enc` 入口；`-e`/`-d` 控制文件加解密，密钥或口令、IV、输入输出必须按 [`enc`](#openssl-enc) 说明固定。帮助可见不等于本项目允许该算法或模式。

<details><summary>展开本机 `-help` 内容</summary>

```text
Usage: aria-192-cbc [options]

General options:
 -help               Display this summary
 -list               List ciphers
 -ciphers            Alias for -list
 -e                  Encrypt
 -d                  Decrypt
 -p                  Print the iv/key
 -P                  Print the iv/key and exit
 -engine val         Use engine, possibly a hardware device

Input options:
 -in infile          Input file
 -k val              Passphrase
 -kfile infile       Read passphrase from file

Output options:
 -out outfile        Output file
 -pass val           Passphrase source
 -v                  Verbose output
 -a                  Base64 encode/decode, depending on encryption flag
 -base64             Same as option -a
 -A                  Used with -[base64|a] to specify base64 buffer as a single line

Encryption options:
 -nopad              Disable standard block padding
 -salt               Use salt in the KDF (default)
 -nosalt             Do not use salt in the KDF
 -debug              Print debug info
 -bufsize val        Buffer size
 -K val              Raw key, in hex
 -S val              Salt, in hex
 -iv val             IV in hex
 -md val             Use specified digest to create a key from the passphrase
 -iter +int          Specify the iteration count and force use of PBKDF2
 -pbkdf2             Use password-based key derivation function 2
 -none               Don't encrypt
 -*                  Any supported cipher

Random state options:
 -rand val           Load the given file(s) into the random number generator
 -writerand outfile  Write random data to the specified file

Provider options:
 -provider-path val  Provider load path (must be before 'provider' argument if required)
 -provider val       Provider to load (can be specified multiple times)
 -propquery val      Property query used when fetching algorithms
```

</details>

#### `openssl aria-192-cfb`

**帮助命令**：`openssl aria-192-cfb -help`。**用法**：`Usage: aria-192-cfb [options]`

**解读**：这是固定密码名称 `aria-192-cfb` 的 `enc` 入口；`-e`/`-d` 控制文件加解密，密钥或口令、IV、输入输出必须按 [`enc`](#openssl-enc) 说明固定。帮助可见不等于本项目允许该算法或模式。

<details><summary>展开本机 `-help` 内容</summary>

```text
Usage: aria-192-cfb [options]

General options:
 -help               Display this summary
 -list               List ciphers
 -ciphers            Alias for -list
 -e                  Encrypt
 -d                  Decrypt
 -p                  Print the iv/key
 -P                  Print the iv/key and exit
 -engine val         Use engine, possibly a hardware device

Input options:
 -in infile          Input file
 -k val              Passphrase
 -kfile infile       Read passphrase from file

Output options:
 -out outfile        Output file
 -pass val           Passphrase source
 -v                  Verbose output
 -a                  Base64 encode/decode, depending on encryption flag
 -base64             Same as option -a
 -A                  Used with -[base64|a] to specify base64 buffer as a single line

Encryption options:
 -nopad              Disable standard block padding
 -salt               Use salt in the KDF (default)
 -nosalt             Do not use salt in the KDF
 -debug              Print debug info
 -bufsize val        Buffer size
 -K val              Raw key, in hex
 -S val              Salt, in hex
 -iv val             IV in hex
 -md val             Use specified digest to create a key from the passphrase
 -iter +int          Specify the iteration count and force use of PBKDF2
 -pbkdf2             Use password-based key derivation function 2
 -none               Don't encrypt
 -*                  Any supported cipher

Random state options:
 -rand val           Load the given file(s) into the random number generator
 -writerand outfile  Write random data to the specified file

Provider options:
 -provider-path val  Provider load path (must be before 'provider' argument if required)
 -provider val       Provider to load (can be specified multiple times)
 -propquery val      Property query used when fetching algorithms
```

</details>

#### `openssl aria-192-cfb1`

**帮助命令**：`openssl aria-192-cfb1 -help`。**用法**：`Usage: aria-192-cfb1 [options]`

**解读**：这是固定密码名称 `aria-192-cfb1` 的 `enc` 入口；`-e`/`-d` 控制文件加解密，密钥或口令、IV、输入输出必须按 [`enc`](#openssl-enc) 说明固定。帮助可见不等于本项目允许该算法或模式。

<details><summary>展开本机 `-help` 内容</summary>

```text
Usage: aria-192-cfb1 [options]

General options:
 -help               Display this summary
 -list               List ciphers
 -ciphers            Alias for -list
 -e                  Encrypt
 -d                  Decrypt
 -p                  Print the iv/key
 -P                  Print the iv/key and exit
 -engine val         Use engine, possibly a hardware device

Input options:
 -in infile          Input file
 -k val              Passphrase
 -kfile infile       Read passphrase from file

Output options:
 -out outfile        Output file
 -pass val           Passphrase source
 -v                  Verbose output
 -a                  Base64 encode/decode, depending on encryption flag
 -base64             Same as option -a
 -A                  Used with -[base64|a] to specify base64 buffer as a single line

Encryption options:
 -nopad              Disable standard block padding
 -salt               Use salt in the KDF (default)
 -nosalt             Do not use salt in the KDF
 -debug              Print debug info
 -bufsize val        Buffer size
 -K val              Raw key, in hex
 -S val              Salt, in hex
 -iv val             IV in hex
 -md val             Use specified digest to create a key from the passphrase
 -iter +int          Specify the iteration count and force use of PBKDF2
 -pbkdf2             Use password-based key derivation function 2
 -none               Don't encrypt
 -*                  Any supported cipher

Random state options:
 -rand val           Load the given file(s) into the random number generator
 -writerand outfile  Write random data to the specified file

Provider options:
 -provider-path val  Provider load path (must be before 'provider' argument if required)
 -provider val       Provider to load (can be specified multiple times)
 -propquery val      Property query used when fetching algorithms
```

</details>

#### `openssl aria-192-cfb8`

**帮助命令**：`openssl aria-192-cfb8 -help`。**用法**：`Usage: aria-192-cfb8 [options]`

**解读**：这是固定密码名称 `aria-192-cfb8` 的 `enc` 入口；`-e`/`-d` 控制文件加解密，密钥或口令、IV、输入输出必须按 [`enc`](#openssl-enc) 说明固定。帮助可见不等于本项目允许该算法或模式。

<details><summary>展开本机 `-help` 内容</summary>

```text
Usage: aria-192-cfb8 [options]

General options:
 -help               Display this summary
 -list               List ciphers
 -ciphers            Alias for -list
 -e                  Encrypt
 -d                  Decrypt
 -p                  Print the iv/key
 -P                  Print the iv/key and exit
 -engine val         Use engine, possibly a hardware device

Input options:
 -in infile          Input file
 -k val              Passphrase
 -kfile infile       Read passphrase from file

Output options:
 -out outfile        Output file
 -pass val           Passphrase source
 -v                  Verbose output
 -a                  Base64 encode/decode, depending on encryption flag
 -base64             Same as option -a
 -A                  Used with -[base64|a] to specify base64 buffer as a single line

Encryption options:
 -nopad              Disable standard block padding
 -salt               Use salt in the KDF (default)
 -nosalt             Do not use salt in the KDF
 -debug              Print debug info
 -bufsize val        Buffer size
 -K val              Raw key, in hex
 -S val              Salt, in hex
 -iv val             IV in hex
 -md val             Use specified digest to create a key from the passphrase
 -iter +int          Specify the iteration count and force use of PBKDF2
 -pbkdf2             Use password-based key derivation function 2
 -none               Don't encrypt
 -*                  Any supported cipher

Random state options:
 -rand val           Load the given file(s) into the random number generator
 -writerand outfile  Write random data to the specified file

Provider options:
 -provider-path val  Provider load path (must be before 'provider' argument if required)
 -provider val       Provider to load (can be specified multiple times)
 -propquery val      Property query used when fetching algorithms
```

</details>

#### `openssl aria-192-ctr`

**帮助命令**：`openssl aria-192-ctr -help`。**用法**：`Usage: aria-192-ctr [options]`

**解读**：这是固定密码名称 `aria-192-ctr` 的 `enc` 入口；`-e`/`-d` 控制文件加解密，密钥或口令、IV、输入输出必须按 [`enc`](#openssl-enc) 说明固定。帮助可见不等于本项目允许该算法或模式。

<details><summary>展开本机 `-help` 内容</summary>

```text
Usage: aria-192-ctr [options]

General options:
 -help               Display this summary
 -list               List ciphers
 -ciphers            Alias for -list
 -e                  Encrypt
 -d                  Decrypt
 -p                  Print the iv/key
 -P                  Print the iv/key and exit
 -engine val         Use engine, possibly a hardware device

Input options:
 -in infile          Input file
 -k val              Passphrase
 -kfile infile       Read passphrase from file

Output options:
 -out outfile        Output file
 -pass val           Passphrase source
 -v                  Verbose output
 -a                  Base64 encode/decode, depending on encryption flag
 -base64             Same as option -a
 -A                  Used with -[base64|a] to specify base64 buffer as a single line

Encryption options:
 -nopad              Disable standard block padding
 -salt               Use salt in the KDF (default)
 -nosalt             Do not use salt in the KDF
 -debug              Print debug info
 -bufsize val        Buffer size
 -K val              Raw key, in hex
 -S val              Salt, in hex
 -iv val             IV in hex
 -md val             Use specified digest to create a key from the passphrase
 -iter +int          Specify the iteration count and force use of PBKDF2
 -pbkdf2             Use password-based key derivation function 2
 -none               Don't encrypt
 -*                  Any supported cipher

Random state options:
 -rand val           Load the given file(s) into the random number generator
 -writerand outfile  Write random data to the specified file

Provider options:
 -provider-path val  Provider load path (must be before 'provider' argument if required)
 -provider val       Provider to load (can be specified multiple times)
 -propquery val      Property query used when fetching algorithms
```

</details>

#### `openssl aria-192-ecb`

**帮助命令**：`openssl aria-192-ecb -help`。**用法**：`Usage: aria-192-ecb [options]`

**解读**：这是固定密码名称 `aria-192-ecb` 的 `enc` 入口；`-e`/`-d` 控制文件加解密，密钥或口令、IV、输入输出必须按 [`enc`](#openssl-enc) 说明固定。帮助可见不等于本项目允许该算法或模式。

<details><summary>展开本机 `-help` 内容</summary>

```text
Usage: aria-192-ecb [options]

General options:
 -help               Display this summary
 -list               List ciphers
 -ciphers            Alias for -list
 -e                  Encrypt
 -d                  Decrypt
 -p                  Print the iv/key
 -P                  Print the iv/key and exit
 -engine val         Use engine, possibly a hardware device

Input options:
 -in infile          Input file
 -k val              Passphrase
 -kfile infile       Read passphrase from file

Output options:
 -out outfile        Output file
 -pass val           Passphrase source
 -v                  Verbose output
 -a                  Base64 encode/decode, depending on encryption flag
 -base64             Same as option -a
 -A                  Used with -[base64|a] to specify base64 buffer as a single line

Encryption options:
 -nopad              Disable standard block padding
 -salt               Use salt in the KDF (default)
 -nosalt             Do not use salt in the KDF
 -debug              Print debug info
 -bufsize val        Buffer size
 -K val              Raw key, in hex
 -S val              Salt, in hex
 -iv val             IV in hex
 -md val             Use specified digest to create a key from the passphrase
 -iter +int          Specify the iteration count and force use of PBKDF2
 -pbkdf2             Use password-based key derivation function 2
 -none               Don't encrypt
 -*                  Any supported cipher

Random state options:
 -rand val           Load the given file(s) into the random number generator
 -writerand outfile  Write random data to the specified file

Provider options:
 -provider-path val  Provider load path (must be before 'provider' argument if required)
 -provider val       Provider to load (can be specified multiple times)
 -propquery val      Property query used when fetching algorithms
```

</details>

#### `openssl aria-192-ofb`

**帮助命令**：`openssl aria-192-ofb -help`。**用法**：`Usage: aria-192-ofb [options]`

**解读**：这是固定密码名称 `aria-192-ofb` 的 `enc` 入口；`-e`/`-d` 控制文件加解密，密钥或口令、IV、输入输出必须按 [`enc`](#openssl-enc) 说明固定。帮助可见不等于本项目允许该算法或模式。

<details><summary>展开本机 `-help` 内容</summary>

```text
Usage: aria-192-ofb [options]

General options:
 -help               Display this summary
 -list               List ciphers
 -ciphers            Alias for -list
 -e                  Encrypt
 -d                  Decrypt
 -p                  Print the iv/key
 -P                  Print the iv/key and exit
 -engine val         Use engine, possibly a hardware device

Input options:
 -in infile          Input file
 -k val              Passphrase
 -kfile infile       Read passphrase from file

Output options:
 -out outfile        Output file
 -pass val           Passphrase source
 -v                  Verbose output
 -a                  Base64 encode/decode, depending on encryption flag
 -base64             Same as option -a
 -A                  Used with -[base64|a] to specify base64 buffer as a single line

Encryption options:
 -nopad              Disable standard block padding
 -salt               Use salt in the KDF (default)
 -nosalt             Do not use salt in the KDF
 -debug              Print debug info
 -bufsize val        Buffer size
 -K val              Raw key, in hex
 -S val              Salt, in hex
 -iv val             IV in hex
 -md val             Use specified digest to create a key from the passphrase
 -iter +int          Specify the iteration count and force use of PBKDF2
 -pbkdf2             Use password-based key derivation function 2
 -none               Don't encrypt
 -*                  Any supported cipher

Random state options:
 -rand val           Load the given file(s) into the random number generator
 -writerand outfile  Write random data to the specified file

Provider options:
 -provider-path val  Provider load path (must be before 'provider' argument if required)
 -provider val       Provider to load (can be specified multiple times)
 -propquery val      Property query used when fetching algorithms
```

</details>

#### `openssl aria-256-cbc`

**帮助命令**：`openssl aria-256-cbc -help`。**用法**：`Usage: aria-256-cbc [options]`

**解读**：这是固定密码名称 `aria-256-cbc` 的 `enc` 入口；`-e`/`-d` 控制文件加解密，密钥或口令、IV、输入输出必须按 [`enc`](#openssl-enc) 说明固定。帮助可见不等于本项目允许该算法或模式。

<details><summary>展开本机 `-help` 内容</summary>

```text
Usage: aria-256-cbc [options]

General options:
 -help               Display this summary
 -list               List ciphers
 -ciphers            Alias for -list
 -e                  Encrypt
 -d                  Decrypt
 -p                  Print the iv/key
 -P                  Print the iv/key and exit
 -engine val         Use engine, possibly a hardware device

Input options:
 -in infile          Input file
 -k val              Passphrase
 -kfile infile       Read passphrase from file

Output options:
 -out outfile        Output file
 -pass val           Passphrase source
 -v                  Verbose output
 -a                  Base64 encode/decode, depending on encryption flag
 -base64             Same as option -a
 -A                  Used with -[base64|a] to specify base64 buffer as a single line

Encryption options:
 -nopad              Disable standard block padding
 -salt               Use salt in the KDF (default)
 -nosalt             Do not use salt in the KDF
 -debug              Print debug info
 -bufsize val        Buffer size
 -K val              Raw key, in hex
 -S val              Salt, in hex
 -iv val             IV in hex
 -md val             Use specified digest to create a key from the passphrase
 -iter +int          Specify the iteration count and force use of PBKDF2
 -pbkdf2             Use password-based key derivation function 2
 -none               Don't encrypt
 -*                  Any supported cipher

Random state options:
 -rand val           Load the given file(s) into the random number generator
 -writerand outfile  Write random data to the specified file

Provider options:
 -provider-path val  Provider load path (must be before 'provider' argument if required)
 -provider val       Provider to load (can be specified multiple times)
 -propquery val      Property query used when fetching algorithms
```

</details>

#### `openssl aria-256-cfb`

**帮助命令**：`openssl aria-256-cfb -help`。**用法**：`Usage: aria-256-cfb [options]`

**解读**：这是固定密码名称 `aria-256-cfb` 的 `enc` 入口；`-e`/`-d` 控制文件加解密，密钥或口令、IV、输入输出必须按 [`enc`](#openssl-enc) 说明固定。帮助可见不等于本项目允许该算法或模式。

<details><summary>展开本机 `-help` 内容</summary>

```text
Usage: aria-256-cfb [options]

General options:
 -help               Display this summary
 -list               List ciphers
 -ciphers            Alias for -list
 -e                  Encrypt
 -d                  Decrypt
 -p                  Print the iv/key
 -P                  Print the iv/key and exit
 -engine val         Use engine, possibly a hardware device

Input options:
 -in infile          Input file
 -k val              Passphrase
 -kfile infile       Read passphrase from file

Output options:
 -out outfile        Output file
 -pass val           Passphrase source
 -v                  Verbose output
 -a                  Base64 encode/decode, depending on encryption flag
 -base64             Same as option -a
 -A                  Used with -[base64|a] to specify base64 buffer as a single line

Encryption options:
 -nopad              Disable standard block padding
 -salt               Use salt in the KDF (default)
 -nosalt             Do not use salt in the KDF
 -debug              Print debug info
 -bufsize val        Buffer size
 -K val              Raw key, in hex
 -S val              Salt, in hex
 -iv val             IV in hex
 -md val             Use specified digest to create a key from the passphrase
 -iter +int          Specify the iteration count and force use of PBKDF2
 -pbkdf2             Use password-based key derivation function 2
 -none               Don't encrypt
 -*                  Any supported cipher

Random state options:
 -rand val           Load the given file(s) into the random number generator
 -writerand outfile  Write random data to the specified file

Provider options:
 -provider-path val  Provider load path (must be before 'provider' argument if required)
 -provider val       Provider to load (can be specified multiple times)
 -propquery val      Property query used when fetching algorithms
```

</details>

#### `openssl aria-256-cfb1`

**帮助命令**：`openssl aria-256-cfb1 -help`。**用法**：`Usage: aria-256-cfb1 [options]`

**解读**：这是固定密码名称 `aria-256-cfb1` 的 `enc` 入口；`-e`/`-d` 控制文件加解密，密钥或口令、IV、输入输出必须按 [`enc`](#openssl-enc) 说明固定。帮助可见不等于本项目允许该算法或模式。

<details><summary>展开本机 `-help` 内容</summary>

```text
Usage: aria-256-cfb1 [options]

General options:
 -help               Display this summary
 -list               List ciphers
 -ciphers            Alias for -list
 -e                  Encrypt
 -d                  Decrypt
 -p                  Print the iv/key
 -P                  Print the iv/key and exit
 -engine val         Use engine, possibly a hardware device

Input options:
 -in infile          Input file
 -k val              Passphrase
 -kfile infile       Read passphrase from file

Output options:
 -out outfile        Output file
 -pass val           Passphrase source
 -v                  Verbose output
 -a                  Base64 encode/decode, depending on encryption flag
 -base64             Same as option -a
 -A                  Used with -[base64|a] to specify base64 buffer as a single line

Encryption options:
 -nopad              Disable standard block padding
 -salt               Use salt in the KDF (default)
 -nosalt             Do not use salt in the KDF
 -debug              Print debug info
 -bufsize val        Buffer size
 -K val              Raw key, in hex
 -S val              Salt, in hex
 -iv val             IV in hex
 -md val             Use specified digest to create a key from the passphrase
 -iter +int          Specify the iteration count and force use of PBKDF2
 -pbkdf2             Use password-based key derivation function 2
 -none               Don't encrypt
 -*                  Any supported cipher

Random state options:
 -rand val           Load the given file(s) into the random number generator
 -writerand outfile  Write random data to the specified file

Provider options:
 -provider-path val  Provider load path (must be before 'provider' argument if required)
 -provider val       Provider to load (can be specified multiple times)
 -propquery val      Property query used when fetching algorithms
```

</details>

#### `openssl aria-256-cfb8`

**帮助命令**：`openssl aria-256-cfb8 -help`。**用法**：`Usage: aria-256-cfb8 [options]`

**解读**：这是固定密码名称 `aria-256-cfb8` 的 `enc` 入口；`-e`/`-d` 控制文件加解密，密钥或口令、IV、输入输出必须按 [`enc`](#openssl-enc) 说明固定。帮助可见不等于本项目允许该算法或模式。

<details><summary>展开本机 `-help` 内容</summary>

```text
Usage: aria-256-cfb8 [options]

General options:
 -help               Display this summary
 -list               List ciphers
 -ciphers            Alias for -list
 -e                  Encrypt
 -d                  Decrypt
 -p                  Print the iv/key
 -P                  Print the iv/key and exit
 -engine val         Use engine, possibly a hardware device

Input options:
 -in infile          Input file
 -k val              Passphrase
 -kfile infile       Read passphrase from file

Output options:
 -out outfile        Output file
 -pass val           Passphrase source
 -v                  Verbose output
 -a                  Base64 encode/decode, depending on encryption flag
 -base64             Same as option -a
 -A                  Used with -[base64|a] to specify base64 buffer as a single line

Encryption options:
 -nopad              Disable standard block padding
 -salt               Use salt in the KDF (default)
 -nosalt             Do not use salt in the KDF
 -debug              Print debug info
 -bufsize val        Buffer size
 -K val              Raw key, in hex
 -S val              Salt, in hex
 -iv val             IV in hex
 -md val             Use specified digest to create a key from the passphrase
 -iter +int          Specify the iteration count and force use of PBKDF2
 -pbkdf2             Use password-based key derivation function 2
 -none               Don't encrypt
 -*                  Any supported cipher

Random state options:
 -rand val           Load the given file(s) into the random number generator
 -writerand outfile  Write random data to the specified file

Provider options:
 -provider-path val  Provider load path (must be before 'provider' argument if required)
 -provider val       Provider to load (can be specified multiple times)
 -propquery val      Property query used when fetching algorithms
```

</details>

#### `openssl aria-256-ctr`

**帮助命令**：`openssl aria-256-ctr -help`。**用法**：`Usage: aria-256-ctr [options]`

**解读**：这是固定密码名称 `aria-256-ctr` 的 `enc` 入口；`-e`/`-d` 控制文件加解密，密钥或口令、IV、输入输出必须按 [`enc`](#openssl-enc) 说明固定。帮助可见不等于本项目允许该算法或模式。

<details><summary>展开本机 `-help` 内容</summary>

```text
Usage: aria-256-ctr [options]

General options:
 -help               Display this summary
 -list               List ciphers
 -ciphers            Alias for -list
 -e                  Encrypt
 -d                  Decrypt
 -p                  Print the iv/key
 -P                  Print the iv/key and exit
 -engine val         Use engine, possibly a hardware device

Input options:
 -in infile          Input file
 -k val              Passphrase
 -kfile infile       Read passphrase from file

Output options:
 -out outfile        Output file
 -pass val           Passphrase source
 -v                  Verbose output
 -a                  Base64 encode/decode, depending on encryption flag
 -base64             Same as option -a
 -A                  Used with -[base64|a] to specify base64 buffer as a single line

Encryption options:
 -nopad              Disable standard block padding
 -salt               Use salt in the KDF (default)
 -nosalt             Do not use salt in the KDF
 -debug              Print debug info
 -bufsize val        Buffer size
 -K val              Raw key, in hex
 -S val              Salt, in hex
 -iv val             IV in hex
 -md val             Use specified digest to create a key from the passphrase
 -iter +int          Specify the iteration count and force use of PBKDF2
 -pbkdf2             Use password-based key derivation function 2
 -none               Don't encrypt
 -*                  Any supported cipher

Random state options:
 -rand val           Load the given file(s) into the random number generator
 -writerand outfile  Write random data to the specified file

Provider options:
 -provider-path val  Provider load path (must be before 'provider' argument if required)
 -provider val       Provider to load (can be specified multiple times)
 -propquery val      Property query used when fetching algorithms
```

</details>

#### `openssl aria-256-ecb`

**帮助命令**：`openssl aria-256-ecb -help`。**用法**：`Usage: aria-256-ecb [options]`

**解读**：这是固定密码名称 `aria-256-ecb` 的 `enc` 入口；`-e`/`-d` 控制文件加解密，密钥或口令、IV、输入输出必须按 [`enc`](#openssl-enc) 说明固定。帮助可见不等于本项目允许该算法或模式。

<details><summary>展开本机 `-help` 内容</summary>

```text
Usage: aria-256-ecb [options]

General options:
 -help               Display this summary
 -list               List ciphers
 -ciphers            Alias for -list
 -e                  Encrypt
 -d                  Decrypt
 -p                  Print the iv/key
 -P                  Print the iv/key and exit
 -engine val         Use engine, possibly a hardware device

Input options:
 -in infile          Input file
 -k val              Passphrase
 -kfile infile       Read passphrase from file

Output options:
 -out outfile        Output file
 -pass val           Passphrase source
 -v                  Verbose output
 -a                  Base64 encode/decode, depending on encryption flag
 -base64             Same as option -a
 -A                  Used with -[base64|a] to specify base64 buffer as a single line

Encryption options:
 -nopad              Disable standard block padding
 -salt               Use salt in the KDF (default)
 -nosalt             Do not use salt in the KDF
 -debug              Print debug info
 -bufsize val        Buffer size
 -K val              Raw key, in hex
 -S val              Salt, in hex
 -iv val             IV in hex
 -md val             Use specified digest to create a key from the passphrase
 -iter +int          Specify the iteration count and force use of PBKDF2
 -pbkdf2             Use password-based key derivation function 2
 -none               Don't encrypt
 -*                  Any supported cipher

Random state options:
 -rand val           Load the given file(s) into the random number generator
 -writerand outfile  Write random data to the specified file

Provider options:
 -provider-path val  Provider load path (must be before 'provider' argument if required)
 -provider val       Provider to load (can be specified multiple times)
 -propquery val      Property query used when fetching algorithms
```

</details>

#### `openssl aria-256-ofb`

**帮助命令**：`openssl aria-256-ofb -help`。**用法**：`Usage: aria-256-ofb [options]`

**解读**：这是固定密码名称 `aria-256-ofb` 的 `enc` 入口；`-e`/`-d` 控制文件加解密，密钥或口令、IV、输入输出必须按 [`enc`](#openssl-enc) 说明固定。帮助可见不等于本项目允许该算法或模式。

<details><summary>展开本机 `-help` 内容</summary>

```text
Usage: aria-256-ofb [options]

General options:
 -help               Display this summary
 -list               List ciphers
 -ciphers            Alias for -list
 -e                  Encrypt
 -d                  Decrypt
 -p                  Print the iv/key
 -P                  Print the iv/key and exit
 -engine val         Use engine, possibly a hardware device

Input options:
 -in infile          Input file
 -k val              Passphrase
 -kfile infile       Read passphrase from file

Output options:
 -out outfile        Output file
 -pass val           Passphrase source
 -v                  Verbose output
 -a                  Base64 encode/decode, depending on encryption flag
 -base64             Same as option -a
 -A                  Used with -[base64|a] to specify base64 buffer as a single line

Encryption options:
 -nopad              Disable standard block padding
 -salt               Use salt in the KDF (default)
 -nosalt             Do not use salt in the KDF
 -debug              Print debug info
 -bufsize val        Buffer size
 -K val              Raw key, in hex
 -S val              Salt, in hex
 -iv val             IV in hex
 -md val             Use specified digest to create a key from the passphrase
 -iter +int          Specify the iteration count and force use of PBKDF2
 -pbkdf2             Use password-based key derivation function 2
 -none               Don't encrypt
 -*                  Any supported cipher

Random state options:
 -rand val           Load the given file(s) into the random number generator
 -writerand outfile  Write random data to the specified file

Provider options:
 -provider-path val  Provider load path (must be before 'provider' argument if required)
 -provider val       Provider to load (can be specified multiple times)
 -propquery val      Property query used when fetching algorithms
```

</details>

#### `openssl base64`

**帮助命令**：`openssl base64 -help`。**用法**：`Usage: base64 [options]`

**解读**：这是编码/解码命令，不提供机密性或认证；`-e`/`-d` 选择方向，输入/输出文件选项继承 `enc`。

<details><summary>展开本机 `-help` 内容</summary>

```text
Usage: base64 [options]

General options:
 -help               Display this summary
 -list               List ciphers
 -ciphers            Alias for -list
 -e                  Encrypt
 -d                  Decrypt
 -p                  Print the iv/key
 -P                  Print the iv/key and exit
 -engine val         Use engine, possibly a hardware device

Input options:
 -in infile          Input file
 -k val              Passphrase
 -kfile infile       Read passphrase from file

Output options:
 -out outfile        Output file
 -pass val           Passphrase source
 -v                  Verbose output
 -a                  Base64 encode/decode, depending on encryption flag
 -base64             Same as option -a
 -A                  Used with -[base64|a] to specify base64 buffer as a single line

Encryption options:
 -nopad              Disable standard block padding
 -salt               Use salt in the KDF (default)
 -nosalt             Do not use salt in the KDF
 -debug              Print debug info
 -bufsize val        Buffer size
 -K val              Raw key, in hex
 -S val              Salt, in hex
 -iv val             IV in hex
 -md val             Use specified digest to create a key from the passphrase
 -iter +int          Specify the iteration count and force use of PBKDF2
 -pbkdf2             Use password-based key derivation function 2
 -none               Don't encrypt
 -*                  Any supported cipher

Random state options:
 -rand val           Load the given file(s) into the random number generator
 -writerand outfile  Write random data to the specified file

Provider options:
 -provider-path val  Provider load path (must be before 'provider' argument if required)
 -provider val       Provider to load (can be specified multiple times)
 -propquery val      Property query used when fetching algorithms
```

</details>

#### `openssl bf`

**帮助命令**：`openssl bf -help`。**用法**：`Usage: bf [options]`

**解读**：这是固定密码名称 `bf` 的 `enc` 入口；`-e`/`-d` 控制文件加解密，密钥或口令、IV、输入输出必须按 [`enc`](#openssl-enc) 说明固定。帮助可见不等于本项目允许该算法或模式。

<details><summary>展开本机 `-help` 内容</summary>

```text
Usage: bf [options]

General options:
 -help               Display this summary
 -list               List ciphers
 -ciphers            Alias for -list
 -e                  Encrypt
 -d                  Decrypt
 -p                  Print the iv/key
 -P                  Print the iv/key and exit
 -engine val         Use engine, possibly a hardware device

Input options:
 -in infile          Input file
 -k val              Passphrase
 -kfile infile       Read passphrase from file

Output options:
 -out outfile        Output file
 -pass val           Passphrase source
 -v                  Verbose output
 -a                  Base64 encode/decode, depending on encryption flag
 -base64             Same as option -a
 -A                  Used with -[base64|a] to specify base64 buffer as a single line

Encryption options:
 -nopad              Disable standard block padding
 -salt               Use salt in the KDF (default)
 -nosalt             Do not use salt in the KDF
 -debug              Print debug info
 -bufsize val        Buffer size
 -K val              Raw key, in hex
 -S val              Salt, in hex
 -iv val             IV in hex
 -md val             Use specified digest to create a key from the passphrase
 -iter +int          Specify the iteration count and force use of PBKDF2
 -pbkdf2             Use password-based key derivation function 2
 -none               Don't encrypt
 -*                  Any supported cipher

Random state options:
 -rand val           Load the given file(s) into the random number generator
 -writerand outfile  Write random data to the specified file

Provider options:
 -provider-path val  Provider load path (must be before 'provider' argument if required)
 -provider val       Provider to load (can be specified multiple times)
 -propquery val      Property query used when fetching algorithms
```

</details>

#### `openssl bf-cbc`

**帮助命令**：`openssl bf-cbc -help`。**用法**：`Usage: bf-cbc [options]`

**解读**：这是固定密码名称 `bf-cbc` 的 `enc` 入口；`-e`/`-d` 控制文件加解密，密钥或口令、IV、输入输出必须按 [`enc`](#openssl-enc) 说明固定。帮助可见不等于本项目允许该算法或模式。

<details><summary>展开本机 `-help` 内容</summary>

```text
Usage: bf-cbc [options]

General options:
 -help               Display this summary
 -list               List ciphers
 -ciphers            Alias for -list
 -e                  Encrypt
 -d                  Decrypt
 -p                  Print the iv/key
 -P                  Print the iv/key and exit
 -engine val         Use engine, possibly a hardware device

Input options:
 -in infile          Input file
 -k val              Passphrase
 -kfile infile       Read passphrase from file

Output options:
 -out outfile        Output file
 -pass val           Passphrase source
 -v                  Verbose output
 -a                  Base64 encode/decode, depending on encryption flag
 -base64             Same as option -a
 -A                  Used with -[base64|a] to specify base64 buffer as a single line

Encryption options:
 -nopad              Disable standard block padding
 -salt               Use salt in the KDF (default)
 -nosalt             Do not use salt in the KDF
 -debug              Print debug info
 -bufsize val        Buffer size
 -K val              Raw key, in hex
 -S val              Salt, in hex
 -iv val             IV in hex
 -md val             Use specified digest to create a key from the passphrase
 -iter +int          Specify the iteration count and force use of PBKDF2
 -pbkdf2             Use password-based key derivation function 2
 -none               Don't encrypt
 -*                  Any supported cipher

Random state options:
 -rand val           Load the given file(s) into the random number generator
 -writerand outfile  Write random data to the specified file

Provider options:
 -provider-path val  Provider load path (must be before 'provider' argument if required)
 -provider val       Provider to load (can be specified multiple times)
 -propquery val      Property query used when fetching algorithms
```

</details>

#### `openssl bf-cfb`

**帮助命令**：`openssl bf-cfb -help`。**用法**：`Usage: bf-cfb [options]`

**解读**：这是固定密码名称 `bf-cfb` 的 `enc` 入口；`-e`/`-d` 控制文件加解密，密钥或口令、IV、输入输出必须按 [`enc`](#openssl-enc) 说明固定。帮助可见不等于本项目允许该算法或模式。

<details><summary>展开本机 `-help` 内容</summary>

```text
Usage: bf-cfb [options]

General options:
 -help               Display this summary
 -list               List ciphers
 -ciphers            Alias for -list
 -e                  Encrypt
 -d                  Decrypt
 -p                  Print the iv/key
 -P                  Print the iv/key and exit
 -engine val         Use engine, possibly a hardware device

Input options:
 -in infile          Input file
 -k val              Passphrase
 -kfile infile       Read passphrase from file

Output options:
 -out outfile        Output file
 -pass val           Passphrase source
 -v                  Verbose output
 -a                  Base64 encode/decode, depending on encryption flag
 -base64             Same as option -a
 -A                  Used with -[base64|a] to specify base64 buffer as a single line

Encryption options:
 -nopad              Disable standard block padding
 -salt               Use salt in the KDF (default)
 -nosalt             Do not use salt in the KDF
 -debug              Print debug info
 -bufsize val        Buffer size
 -K val              Raw key, in hex
 -S val              Salt, in hex
 -iv val             IV in hex
 -md val             Use specified digest to create a key from the passphrase
 -iter +int          Specify the iteration count and force use of PBKDF2
 -pbkdf2             Use password-based key derivation function 2
 -none               Don't encrypt
 -*                  Any supported cipher

Random state options:
 -rand val           Load the given file(s) into the random number generator
 -writerand outfile  Write random data to the specified file

Provider options:
 -provider-path val  Provider load path (must be before 'provider' argument if required)
 -provider val       Provider to load (can be specified multiple times)
 -propquery val      Property query used when fetching algorithms
```

</details>

#### `openssl bf-ecb`

**帮助命令**：`openssl bf-ecb -help`。**用法**：`Usage: bf-ecb [options]`

**解读**：这是固定密码名称 `bf-ecb` 的 `enc` 入口；`-e`/`-d` 控制文件加解密，密钥或口令、IV、输入输出必须按 [`enc`](#openssl-enc) 说明固定。帮助可见不等于本项目允许该算法或模式。

<details><summary>展开本机 `-help` 内容</summary>

```text
Usage: bf-ecb [options]

General options:
 -help               Display this summary
 -list               List ciphers
 -ciphers            Alias for -list
 -e                  Encrypt
 -d                  Decrypt
 -p                  Print the iv/key
 -P                  Print the iv/key and exit
 -engine val         Use engine, possibly a hardware device

Input options:
 -in infile          Input file
 -k val              Passphrase
 -kfile infile       Read passphrase from file

Output options:
 -out outfile        Output file
 -pass val           Passphrase source
 -v                  Verbose output
 -a                  Base64 encode/decode, depending on encryption flag
 -base64             Same as option -a
 -A                  Used with -[base64|a] to specify base64 buffer as a single line

Encryption options:
 -nopad              Disable standard block padding
 -salt               Use salt in the KDF (default)
 -nosalt             Do not use salt in the KDF
 -debug              Print debug info
 -bufsize val        Buffer size
 -K val              Raw key, in hex
 -S val              Salt, in hex
 -iv val             IV in hex
 -md val             Use specified digest to create a key from the passphrase
 -iter +int          Specify the iteration count and force use of PBKDF2
 -pbkdf2             Use password-based key derivation function 2
 -none               Don't encrypt
 -*                  Any supported cipher

Random state options:
 -rand val           Load the given file(s) into the random number generator
 -writerand outfile  Write random data to the specified file

Provider options:
 -provider-path val  Provider load path (must be before 'provider' argument if required)
 -provider val       Provider to load (can be specified multiple times)
 -propquery val      Property query used when fetching algorithms
```

</details>

#### `openssl bf-ofb`

**帮助命令**：`openssl bf-ofb -help`。**用法**：`Usage: bf-ofb [options]`

**解读**：这是固定密码名称 `bf-ofb` 的 `enc` 入口；`-e`/`-d` 控制文件加解密，密钥或口令、IV、输入输出必须按 [`enc`](#openssl-enc) 说明固定。帮助可见不等于本项目允许该算法或模式。

<details><summary>展开本机 `-help` 内容</summary>

```text
Usage: bf-ofb [options]

General options:
 -help               Display this summary
 -list               List ciphers
 -ciphers            Alias for -list
 -e                  Encrypt
 -d                  Decrypt
 -p                  Print the iv/key
 -P                  Print the iv/key and exit
 -engine val         Use engine, possibly a hardware device

Input options:
 -in infile          Input file
 -k val              Passphrase
 -kfile infile       Read passphrase from file

Output options:
 -out outfile        Output file
 -pass val           Passphrase source
 -v                  Verbose output
 -a                  Base64 encode/decode, depending on encryption flag
 -base64             Same as option -a
 -A                  Used with -[base64|a] to specify base64 buffer as a single line

Encryption options:
 -nopad              Disable standard block padding
 -salt               Use salt in the KDF (default)
 -nosalt             Do not use salt in the KDF
 -debug              Print debug info
 -bufsize val        Buffer size
 -K val              Raw key, in hex
 -S val              Salt, in hex
 -iv val             IV in hex
 -md val             Use specified digest to create a key from the passphrase
 -iter +int          Specify the iteration count and force use of PBKDF2
 -pbkdf2             Use password-based key derivation function 2
 -none               Don't encrypt
 -*                  Any supported cipher

Random state options:
 -rand val           Load the given file(s) into the random number generator
 -writerand outfile  Write random data to the specified file

Provider options:
 -provider-path val  Provider load path (must be before 'provider' argument if required)
 -provider val       Provider to load (can be specified multiple times)
 -propquery val      Property query used when fetching algorithms
```

</details>

#### `openssl camellia-128-cbc`

**帮助命令**：`openssl camellia-128-cbc -help`。**用法**：`Usage: camellia-128-cbc [options]`

**解读**：这是固定密码名称 `camellia-128-cbc` 的 `enc` 入口；`-e`/`-d` 控制文件加解密，密钥或口令、IV、输入输出必须按 [`enc`](#openssl-enc) 说明固定。帮助可见不等于本项目允许该算法或模式。

<details><summary>展开本机 `-help` 内容</summary>

```text
Usage: camellia-128-cbc [options]

General options:
 -help               Display this summary
 -list               List ciphers
 -ciphers            Alias for -list
 -e                  Encrypt
 -d                  Decrypt
 -p                  Print the iv/key
 -P                  Print the iv/key and exit
 -engine val         Use engine, possibly a hardware device

Input options:
 -in infile          Input file
 -k val              Passphrase
 -kfile infile       Read passphrase from file

Output options:
 -out outfile        Output file
 -pass val           Passphrase source
 -v                  Verbose output
 -a                  Base64 encode/decode, depending on encryption flag
 -base64             Same as option -a
 -A                  Used with -[base64|a] to specify base64 buffer as a single line

Encryption options:
 -nopad              Disable standard block padding
 -salt               Use salt in the KDF (default)
 -nosalt             Do not use salt in the KDF
 -debug              Print debug info
 -bufsize val        Buffer size
 -K val              Raw key, in hex
 -S val              Salt, in hex
 -iv val             IV in hex
 -md val             Use specified digest to create a key from the passphrase
 -iter +int          Specify the iteration count and force use of PBKDF2
 -pbkdf2             Use password-based key derivation function 2
 -none               Don't encrypt
 -*                  Any supported cipher

Random state options:
 -rand val           Load the given file(s) into the random number generator
 -writerand outfile  Write random data to the specified file

Provider options:
 -provider-path val  Provider load path (must be before 'provider' argument if required)
 -provider val       Provider to load (can be specified multiple times)
 -propquery val      Property query used when fetching algorithms
```

</details>

#### `openssl camellia-128-ecb`

**帮助命令**：`openssl camellia-128-ecb -help`。**用法**：`Usage: camellia-128-ecb [options]`

**解读**：这是固定密码名称 `camellia-128-ecb` 的 `enc` 入口；`-e`/`-d` 控制文件加解密，密钥或口令、IV、输入输出必须按 [`enc`](#openssl-enc) 说明固定。帮助可见不等于本项目允许该算法或模式。

<details><summary>展开本机 `-help` 内容</summary>

```text
Usage: camellia-128-ecb [options]

General options:
 -help               Display this summary
 -list               List ciphers
 -ciphers            Alias for -list
 -e                  Encrypt
 -d                  Decrypt
 -p                  Print the iv/key
 -P                  Print the iv/key and exit
 -engine val         Use engine, possibly a hardware device

Input options:
 -in infile          Input file
 -k val              Passphrase
 -kfile infile       Read passphrase from file

Output options:
 -out outfile        Output file
 -pass val           Passphrase source
 -v                  Verbose output
 -a                  Base64 encode/decode, depending on encryption flag
 -base64             Same as option -a
 -A                  Used with -[base64|a] to specify base64 buffer as a single line

Encryption options:
 -nopad              Disable standard block padding
 -salt               Use salt in the KDF (default)
 -nosalt             Do not use salt in the KDF
 -debug              Print debug info
 -bufsize val        Buffer size
 -K val              Raw key, in hex
 -S val              Salt, in hex
 -iv val             IV in hex
 -md val             Use specified digest to create a key from the passphrase
 -iter +int          Specify the iteration count and force use of PBKDF2
 -pbkdf2             Use password-based key derivation function 2
 -none               Don't encrypt
 -*                  Any supported cipher

Random state options:
 -rand val           Load the given file(s) into the random number generator
 -writerand outfile  Write random data to the specified file

Provider options:
 -provider-path val  Provider load path (must be before 'provider' argument if required)
 -provider val       Provider to load (can be specified multiple times)
 -propquery val      Property query used when fetching algorithms
```

</details>

#### `openssl camellia-192-cbc`

**帮助命令**：`openssl camellia-192-cbc -help`。**用法**：`Usage: camellia-192-cbc [options]`

**解读**：这是固定密码名称 `camellia-192-cbc` 的 `enc` 入口；`-e`/`-d` 控制文件加解密，密钥或口令、IV、输入输出必须按 [`enc`](#openssl-enc) 说明固定。帮助可见不等于本项目允许该算法或模式。

<details><summary>展开本机 `-help` 内容</summary>

```text
Usage: camellia-192-cbc [options]

General options:
 -help               Display this summary
 -list               List ciphers
 -ciphers            Alias for -list
 -e                  Encrypt
 -d                  Decrypt
 -p                  Print the iv/key
 -P                  Print the iv/key and exit
 -engine val         Use engine, possibly a hardware device

Input options:
 -in infile          Input file
 -k val              Passphrase
 -kfile infile       Read passphrase from file

Output options:
 -out outfile        Output file
 -pass val           Passphrase source
 -v                  Verbose output
 -a                  Base64 encode/decode, depending on encryption flag
 -base64             Same as option -a
 -A                  Used with -[base64|a] to specify base64 buffer as a single line

Encryption options:
 -nopad              Disable standard block padding
 -salt               Use salt in the KDF (default)
 -nosalt             Do not use salt in the KDF
 -debug              Print debug info
 -bufsize val        Buffer size
 -K val              Raw key, in hex
 -S val              Salt, in hex
 -iv val             IV in hex
 -md val             Use specified digest to create a key from the passphrase
 -iter +int          Specify the iteration count and force use of PBKDF2
 -pbkdf2             Use password-based key derivation function 2
 -none               Don't encrypt
 -*                  Any supported cipher

Random state options:
 -rand val           Load the given file(s) into the random number generator
 -writerand outfile  Write random data to the specified file

Provider options:
 -provider-path val  Provider load path (must be before 'provider' argument if required)
 -provider val       Provider to load (can be specified multiple times)
 -propquery val      Property query used when fetching algorithms
```

</details>

#### `openssl camellia-192-ecb`

**帮助命令**：`openssl camellia-192-ecb -help`。**用法**：`Usage: camellia-192-ecb [options]`

**解读**：这是固定密码名称 `camellia-192-ecb` 的 `enc` 入口；`-e`/`-d` 控制文件加解密，密钥或口令、IV、输入输出必须按 [`enc`](#openssl-enc) 说明固定。帮助可见不等于本项目允许该算法或模式。

<details><summary>展开本机 `-help` 内容</summary>

```text
Usage: camellia-192-ecb [options]

General options:
 -help               Display this summary
 -list               List ciphers
 -ciphers            Alias for -list
 -e                  Encrypt
 -d                  Decrypt
 -p                  Print the iv/key
 -P                  Print the iv/key and exit
 -engine val         Use engine, possibly a hardware device

Input options:
 -in infile          Input file
 -k val              Passphrase
 -kfile infile       Read passphrase from file

Output options:
 -out outfile        Output file
 -pass val           Passphrase source
 -v                  Verbose output
 -a                  Base64 encode/decode, depending on encryption flag
 -base64             Same as option -a
 -A                  Used with -[base64|a] to specify base64 buffer as a single line

Encryption options:
 -nopad              Disable standard block padding
 -salt               Use salt in the KDF (default)
 -nosalt             Do not use salt in the KDF
 -debug              Print debug info
 -bufsize val        Buffer size
 -K val              Raw key, in hex
 -S val              Salt, in hex
 -iv val             IV in hex
 -md val             Use specified digest to create a key from the passphrase
 -iter +int          Specify the iteration count and force use of PBKDF2
 -pbkdf2             Use password-based key derivation function 2
 -none               Don't encrypt
 -*                  Any supported cipher

Random state options:
 -rand val           Load the given file(s) into the random number generator
 -writerand outfile  Write random data to the specified file

Provider options:
 -provider-path val  Provider load path (must be before 'provider' argument if required)
 -provider val       Provider to load (can be specified multiple times)
 -propquery val      Property query used when fetching algorithms
```

</details>

#### `openssl camellia-256-cbc`

**帮助命令**：`openssl camellia-256-cbc -help`。**用法**：`Usage: camellia-256-cbc [options]`

**解读**：这是固定密码名称 `camellia-256-cbc` 的 `enc` 入口；`-e`/`-d` 控制文件加解密，密钥或口令、IV、输入输出必须按 [`enc`](#openssl-enc) 说明固定。帮助可见不等于本项目允许该算法或模式。

<details><summary>展开本机 `-help` 内容</summary>

```text
Usage: camellia-256-cbc [options]

General options:
 -help               Display this summary
 -list               List ciphers
 -ciphers            Alias for -list
 -e                  Encrypt
 -d                  Decrypt
 -p                  Print the iv/key
 -P                  Print the iv/key and exit
 -engine val         Use engine, possibly a hardware device

Input options:
 -in infile          Input file
 -k val              Passphrase
 -kfile infile       Read passphrase from file

Output options:
 -out outfile        Output file
 -pass val           Passphrase source
 -v                  Verbose output
 -a                  Base64 encode/decode, depending on encryption flag
 -base64             Same as option -a
 -A                  Used with -[base64|a] to specify base64 buffer as a single line

Encryption options:
 -nopad              Disable standard block padding
 -salt               Use salt in the KDF (default)
 -nosalt             Do not use salt in the KDF
 -debug              Print debug info
 -bufsize val        Buffer size
 -K val              Raw key, in hex
 -S val              Salt, in hex
 -iv val             IV in hex
 -md val             Use specified digest to create a key from the passphrase
 -iter +int          Specify the iteration count and force use of PBKDF2
 -pbkdf2             Use password-based key derivation function 2
 -none               Don't encrypt
 -*                  Any supported cipher

Random state options:
 -rand val           Load the given file(s) into the random number generator
 -writerand outfile  Write random data to the specified file

Provider options:
 -provider-path val  Provider load path (must be before 'provider' argument if required)
 -provider val       Provider to load (can be specified multiple times)
 -propquery val      Property query used when fetching algorithms
```

</details>

#### `openssl camellia-256-ecb`

**帮助命令**：`openssl camellia-256-ecb -help`。**用法**：`Usage: camellia-256-ecb [options]`

**解读**：这是固定密码名称 `camellia-256-ecb` 的 `enc` 入口；`-e`/`-d` 控制文件加解密，密钥或口令、IV、输入输出必须按 [`enc`](#openssl-enc) 说明固定。帮助可见不等于本项目允许该算法或模式。

<details><summary>展开本机 `-help` 内容</summary>

```text
Usage: camellia-256-ecb [options]

General options:
 -help               Display this summary
 -list               List ciphers
 -ciphers            Alias for -list
 -e                  Encrypt
 -d                  Decrypt
 -p                  Print the iv/key
 -P                  Print the iv/key and exit
 -engine val         Use engine, possibly a hardware device

Input options:
 -in infile          Input file
 -k val              Passphrase
 -kfile infile       Read passphrase from file

Output options:
 -out outfile        Output file
 -pass val           Passphrase source
 -v                  Verbose output
 -a                  Base64 encode/decode, depending on encryption flag
 -base64             Same as option -a
 -A                  Used with -[base64|a] to specify base64 buffer as a single line

Encryption options:
 -nopad              Disable standard block padding
 -salt               Use salt in the KDF (default)
 -nosalt             Do not use salt in the KDF
 -debug              Print debug info
 -bufsize val        Buffer size
 -K val              Raw key, in hex
 -S val              Salt, in hex
 -iv val             IV in hex
 -md val             Use specified digest to create a key from the passphrase
 -iter +int          Specify the iteration count and force use of PBKDF2
 -pbkdf2             Use password-based key derivation function 2
 -none               Don't encrypt
 -*                  Any supported cipher

Random state options:
 -rand val           Load the given file(s) into the random number generator
 -writerand outfile  Write random data to the specified file

Provider options:
 -provider-path val  Provider load path (must be before 'provider' argument if required)
 -provider val       Provider to load (can be specified multiple times)
 -propquery val      Property query used when fetching algorithms
```

</details>

#### `openssl cast`

**帮助命令**：`openssl cast -help`。**用法**：`Usage: cast [options]`

**解读**：这是固定密码名称 `cast` 的 `enc` 入口；`-e`/`-d` 控制文件加解密，密钥或口令、IV、输入输出必须按 [`enc`](#openssl-enc) 说明固定。帮助可见不等于本项目允许该算法或模式。

<details><summary>展开本机 `-help` 内容</summary>

```text
Usage: cast [options]

General options:
 -help               Display this summary
 -list               List ciphers
 -ciphers            Alias for -list
 -e                  Encrypt
 -d                  Decrypt
 -p                  Print the iv/key
 -P                  Print the iv/key and exit
 -engine val         Use engine, possibly a hardware device

Input options:
 -in infile          Input file
 -k val              Passphrase
 -kfile infile       Read passphrase from file

Output options:
 -out outfile        Output file
 -pass val           Passphrase source
 -v                  Verbose output
 -a                  Base64 encode/decode, depending on encryption flag
 -base64             Same as option -a
 -A                  Used with -[base64|a] to specify base64 buffer as a single line

Encryption options:
 -nopad              Disable standard block padding
 -salt               Use salt in the KDF (default)
 -nosalt             Do not use salt in the KDF
 -debug              Print debug info
 -bufsize val        Buffer size
 -K val              Raw key, in hex
 -S val              Salt, in hex
 -iv val             IV in hex
 -md val             Use specified digest to create a key from the passphrase
 -iter +int          Specify the iteration count and force use of PBKDF2
 -pbkdf2             Use password-based key derivation function 2
 -none               Don't encrypt
 -*                  Any supported cipher

Random state options:
 -rand val           Load the given file(s) into the random number generator
 -writerand outfile  Write random data to the specified file

Provider options:
 -provider-path val  Provider load path (must be before 'provider' argument if required)
 -provider val       Provider to load (can be specified multiple times)
 -propquery val      Property query used when fetching algorithms
```

</details>

#### `openssl cast-cbc`

**帮助命令**：`openssl cast-cbc -help`。**用法**：`Usage: cast-cbc [options]`

**解读**：这是固定密码名称 `cast-cbc` 的 `enc` 入口；`-e`/`-d` 控制文件加解密，密钥或口令、IV、输入输出必须按 [`enc`](#openssl-enc) 说明固定。帮助可见不等于本项目允许该算法或模式。

<details><summary>展开本机 `-help` 内容</summary>

```text
Usage: cast-cbc [options]

General options:
 -help               Display this summary
 -list               List ciphers
 -ciphers            Alias for -list
 -e                  Encrypt
 -d                  Decrypt
 -p                  Print the iv/key
 -P                  Print the iv/key and exit
 -engine val         Use engine, possibly a hardware device

Input options:
 -in infile          Input file
 -k val              Passphrase
 -kfile infile       Read passphrase from file

Output options:
 -out outfile        Output file
 -pass val           Passphrase source
 -v                  Verbose output
 -a                  Base64 encode/decode, depending on encryption flag
 -base64             Same as option -a
 -A                  Used with -[base64|a] to specify base64 buffer as a single line

Encryption options:
 -nopad              Disable standard block padding
 -salt               Use salt in the KDF (default)
 -nosalt             Do not use salt in the KDF
 -debug              Print debug info
 -bufsize val        Buffer size
 -K val              Raw key, in hex
 -S val              Salt, in hex
 -iv val             IV in hex
 -md val             Use specified digest to create a key from the passphrase
 -iter +int          Specify the iteration count and force use of PBKDF2
 -pbkdf2             Use password-based key derivation function 2
 -none               Don't encrypt
 -*                  Any supported cipher

Random state options:
 -rand val           Load the given file(s) into the random number generator
 -writerand outfile  Write random data to the specified file

Provider options:
 -provider-path val  Provider load path (must be before 'provider' argument if required)
 -provider val       Provider to load (can be specified multiple times)
 -propquery val      Property query used when fetching algorithms
```

</details>

#### `openssl cast5-cbc`

**帮助命令**：`openssl cast5-cbc -help`。**用法**：`Usage: cast5-cbc [options]`

**解读**：这是固定密码名称 `cast5-cbc` 的 `enc` 入口；`-e`/`-d` 控制文件加解密，密钥或口令、IV、输入输出必须按 [`enc`](#openssl-enc) 说明固定。帮助可见不等于本项目允许该算法或模式。

<details><summary>展开本机 `-help` 内容</summary>

```text
Usage: cast5-cbc [options]

General options:
 -help               Display this summary
 -list               List ciphers
 -ciphers            Alias for -list
 -e                  Encrypt
 -d                  Decrypt
 -p                  Print the iv/key
 -P                  Print the iv/key and exit
 -engine val         Use engine, possibly a hardware device

Input options:
 -in infile          Input file
 -k val              Passphrase
 -kfile infile       Read passphrase from file

Output options:
 -out outfile        Output file
 -pass val           Passphrase source
 -v                  Verbose output
 -a                  Base64 encode/decode, depending on encryption flag
 -base64             Same as option -a
 -A                  Used with -[base64|a] to specify base64 buffer as a single line

Encryption options:
 -nopad              Disable standard block padding
 -salt               Use salt in the KDF (default)
 -nosalt             Do not use salt in the KDF
 -debug              Print debug info
 -bufsize val        Buffer size
 -K val              Raw key, in hex
 -S val              Salt, in hex
 -iv val             IV in hex
 -md val             Use specified digest to create a key from the passphrase
 -iter +int          Specify the iteration count and force use of PBKDF2
 -pbkdf2             Use password-based key derivation function 2
 -none               Don't encrypt
 -*                  Any supported cipher

Random state options:
 -rand val           Load the given file(s) into the random number generator
 -writerand outfile  Write random data to the specified file

Provider options:
 -provider-path val  Provider load path (must be before 'provider' argument if required)
 -provider val       Provider to load (can be specified multiple times)
 -propquery val      Property query used when fetching algorithms
```

</details>

#### `openssl cast5-cfb`

**帮助命令**：`openssl cast5-cfb -help`。**用法**：`Usage: cast5-cfb [options]`

**解读**：这是固定密码名称 `cast5-cfb` 的 `enc` 入口；`-e`/`-d` 控制文件加解密，密钥或口令、IV、输入输出必须按 [`enc`](#openssl-enc) 说明固定。帮助可见不等于本项目允许该算法或模式。

<details><summary>展开本机 `-help` 内容</summary>

```text
Usage: cast5-cfb [options]

General options:
 -help               Display this summary
 -list               List ciphers
 -ciphers            Alias for -list
 -e                  Encrypt
 -d                  Decrypt
 -p                  Print the iv/key
 -P                  Print the iv/key and exit
 -engine val         Use engine, possibly a hardware device

Input options:
 -in infile          Input file
 -k val              Passphrase
 -kfile infile       Read passphrase from file

Output options:
 -out outfile        Output file
 -pass val           Passphrase source
 -v                  Verbose output
 -a                  Base64 encode/decode, depending on encryption flag
 -base64             Same as option -a
 -A                  Used with -[base64|a] to specify base64 buffer as a single line

Encryption options:
 -nopad              Disable standard block padding
 -salt               Use salt in the KDF (default)
 -nosalt             Do not use salt in the KDF
 -debug              Print debug info
 -bufsize val        Buffer size
 -K val              Raw key, in hex
 -S val              Salt, in hex
 -iv val             IV in hex
 -md val             Use specified digest to create a key from the passphrase
 -iter +int          Specify the iteration count and force use of PBKDF2
 -pbkdf2             Use password-based key derivation function 2
 -none               Don't encrypt
 -*                  Any supported cipher

Random state options:
 -rand val           Load the given file(s) into the random number generator
 -writerand outfile  Write random data to the specified file

Provider options:
 -provider-path val  Provider load path (must be before 'provider' argument if required)
 -provider val       Provider to load (can be specified multiple times)
 -propquery val      Property query used when fetching algorithms
```

</details>

#### `openssl cast5-ecb`

**帮助命令**：`openssl cast5-ecb -help`。**用法**：`Usage: cast5-ecb [options]`

**解读**：这是固定密码名称 `cast5-ecb` 的 `enc` 入口；`-e`/`-d` 控制文件加解密，密钥或口令、IV、输入输出必须按 [`enc`](#openssl-enc) 说明固定。帮助可见不等于本项目允许该算法或模式。

<details><summary>展开本机 `-help` 内容</summary>

```text
Usage: cast5-ecb [options]

General options:
 -help               Display this summary
 -list               List ciphers
 -ciphers            Alias for -list
 -e                  Encrypt
 -d                  Decrypt
 -p                  Print the iv/key
 -P                  Print the iv/key and exit
 -engine val         Use engine, possibly a hardware device

Input options:
 -in infile          Input file
 -k val              Passphrase
 -kfile infile       Read passphrase from file

Output options:
 -out outfile        Output file
 -pass val           Passphrase source
 -v                  Verbose output
 -a                  Base64 encode/decode, depending on encryption flag
 -base64             Same as option -a
 -A                  Used with -[base64|a] to specify base64 buffer as a single line

Encryption options:
 -nopad              Disable standard block padding
 -salt               Use salt in the KDF (default)
 -nosalt             Do not use salt in the KDF
 -debug              Print debug info
 -bufsize val        Buffer size
 -K val              Raw key, in hex
 -S val              Salt, in hex
 -iv val             IV in hex
 -md val             Use specified digest to create a key from the passphrase
 -iter +int          Specify the iteration count and force use of PBKDF2
 -pbkdf2             Use password-based key derivation function 2
 -none               Don't encrypt
 -*                  Any supported cipher

Random state options:
 -rand val           Load the given file(s) into the random number generator
 -writerand outfile  Write random data to the specified file

Provider options:
 -provider-path val  Provider load path (must be before 'provider' argument if required)
 -provider val       Provider to load (can be specified multiple times)
 -propquery val      Property query used when fetching algorithms
```

</details>

#### `openssl cast5-ofb`

**帮助命令**：`openssl cast5-ofb -help`。**用法**：`Usage: cast5-ofb [options]`

**解读**：这是固定密码名称 `cast5-ofb` 的 `enc` 入口；`-e`/`-d` 控制文件加解密，密钥或口令、IV、输入输出必须按 [`enc`](#openssl-enc) 说明固定。帮助可见不等于本项目允许该算法或模式。

<details><summary>展开本机 `-help` 内容</summary>

```text
Usage: cast5-ofb [options]

General options:
 -help               Display this summary
 -list               List ciphers
 -ciphers            Alias for -list
 -e                  Encrypt
 -d                  Decrypt
 -p                  Print the iv/key
 -P                  Print the iv/key and exit
 -engine val         Use engine, possibly a hardware device

Input options:
 -in infile          Input file
 -k val              Passphrase
 -kfile infile       Read passphrase from file

Output options:
 -out outfile        Output file
 -pass val           Passphrase source
 -v                  Verbose output
 -a                  Base64 encode/decode, depending on encryption flag
 -base64             Same as option -a
 -A                  Used with -[base64|a] to specify base64 buffer as a single line

Encryption options:
 -nopad              Disable standard block padding
 -salt               Use salt in the KDF (default)
 -nosalt             Do not use salt in the KDF
 -debug              Print debug info
 -bufsize val        Buffer size
 -K val              Raw key, in hex
 -S val              Salt, in hex
 -iv val             IV in hex
 -md val             Use specified digest to create a key from the passphrase
 -iter +int          Specify the iteration count and force use of PBKDF2
 -pbkdf2             Use password-based key derivation function 2
 -none               Don't encrypt
 -*                  Any supported cipher

Random state options:
 -rand val           Load the given file(s) into the random number generator
 -writerand outfile  Write random data to the specified file

Provider options:
 -provider-path val  Provider load path (must be before 'provider' argument if required)
 -provider val       Provider to load (can be specified multiple times)
 -propquery val      Property query used when fetching algorithms
```

</details>

#### `openssl des`

**帮助命令**：`openssl des -help`。**用法**：`Usage: des [options]`

**解读**：这是固定密码名称 `des` 的 `enc` 入口；`-e`/`-d` 控制文件加解密，密钥或口令、IV、输入输出必须按 [`enc`](#openssl-enc) 说明固定。帮助可见不等于本项目允许该算法或模式。

<details><summary>展开本机 `-help` 内容</summary>

```text
Usage: des [options]

General options:
 -help               Display this summary
 -list               List ciphers
 -ciphers            Alias for -list
 -e                  Encrypt
 -d                  Decrypt
 -p                  Print the iv/key
 -P                  Print the iv/key and exit
 -engine val         Use engine, possibly a hardware device

Input options:
 -in infile          Input file
 -k val              Passphrase
 -kfile infile       Read passphrase from file

Output options:
 -out outfile        Output file
 -pass val           Passphrase source
 -v                  Verbose output
 -a                  Base64 encode/decode, depending on encryption flag
 -base64             Same as option -a
 -A                  Used with -[base64|a] to specify base64 buffer as a single line

Encryption options:
 -nopad              Disable standard block padding
 -salt               Use salt in the KDF (default)
 -nosalt             Do not use salt in the KDF
 -debug              Print debug info
 -bufsize val        Buffer size
 -K val              Raw key, in hex
 -S val              Salt, in hex
 -iv val             IV in hex
 -md val             Use specified digest to create a key from the passphrase
 -iter +int          Specify the iteration count and force use of PBKDF2
 -pbkdf2             Use password-based key derivation function 2
 -none               Don't encrypt
 -*                  Any supported cipher

Random state options:
 -rand val           Load the given file(s) into the random number generator
 -writerand outfile  Write random data to the specified file

Provider options:
 -provider-path val  Provider load path (must be before 'provider' argument if required)
 -provider val       Provider to load (can be specified multiple times)
 -propquery val      Property query used when fetching algorithms
```

</details>

#### `openssl des-cbc`

**帮助命令**：`openssl des-cbc -help`。**用法**：`Usage: des-cbc [options]`

**解读**：这是固定密码名称 `des-cbc` 的 `enc` 入口；`-e`/`-d` 控制文件加解密，密钥或口令、IV、输入输出必须按 [`enc`](#openssl-enc) 说明固定。帮助可见不等于本项目允许该算法或模式。

<details><summary>展开本机 `-help` 内容</summary>

```text
Usage: des-cbc [options]

General options:
 -help               Display this summary
 -list               List ciphers
 -ciphers            Alias for -list
 -e                  Encrypt
 -d                  Decrypt
 -p                  Print the iv/key
 -P                  Print the iv/key and exit
 -engine val         Use engine, possibly a hardware device

Input options:
 -in infile          Input file
 -k val              Passphrase
 -kfile infile       Read passphrase from file

Output options:
 -out outfile        Output file
 -pass val           Passphrase source
 -v                  Verbose output
 -a                  Base64 encode/decode, depending on encryption flag
 -base64             Same as option -a
 -A                  Used with -[base64|a] to specify base64 buffer as a single line

Encryption options:
 -nopad              Disable standard block padding
 -salt               Use salt in the KDF (default)
 -nosalt             Do not use salt in the KDF
 -debug              Print debug info
 -bufsize val        Buffer size
 -K val              Raw key, in hex
 -S val              Salt, in hex
 -iv val             IV in hex
 -md val             Use specified digest to create a key from the passphrase
 -iter +int          Specify the iteration count and force use of PBKDF2
 -pbkdf2             Use password-based key derivation function 2
 -none               Don't encrypt
 -*                  Any supported cipher

Random state options:
 -rand val           Load the given file(s) into the random number generator
 -writerand outfile  Write random data to the specified file

Provider options:
 -provider-path val  Provider load path (must be before 'provider' argument if required)
 -provider val       Provider to load (can be specified multiple times)
 -propquery val      Property query used when fetching algorithms
```

</details>

#### `openssl des-cfb`

**帮助命令**：`openssl des-cfb -help`。**用法**：`Usage: des-cfb [options]`

**解读**：这是固定密码名称 `des-cfb` 的 `enc` 入口；`-e`/`-d` 控制文件加解密，密钥或口令、IV、输入输出必须按 [`enc`](#openssl-enc) 说明固定。帮助可见不等于本项目允许该算法或模式。

<details><summary>展开本机 `-help` 内容</summary>

```text
Usage: des-cfb [options]

General options:
 -help               Display this summary
 -list               List ciphers
 -ciphers            Alias for -list
 -e                  Encrypt
 -d                  Decrypt
 -p                  Print the iv/key
 -P                  Print the iv/key and exit
 -engine val         Use engine, possibly a hardware device

Input options:
 -in infile          Input file
 -k val              Passphrase
 -kfile infile       Read passphrase from file

Output options:
 -out outfile        Output file
 -pass val           Passphrase source
 -v                  Verbose output
 -a                  Base64 encode/decode, depending on encryption flag
 -base64             Same as option -a
 -A                  Used with -[base64|a] to specify base64 buffer as a single line

Encryption options:
 -nopad              Disable standard block padding
 -salt               Use salt in the KDF (default)
 -nosalt             Do not use salt in the KDF
 -debug              Print debug info
 -bufsize val        Buffer size
 -K val              Raw key, in hex
 -S val              Salt, in hex
 -iv val             IV in hex
 -md val             Use specified digest to create a key from the passphrase
 -iter +int          Specify the iteration count and force use of PBKDF2
 -pbkdf2             Use password-based key derivation function 2
 -none               Don't encrypt
 -*                  Any supported cipher

Random state options:
 -rand val           Load the given file(s) into the random number generator
 -writerand outfile  Write random data to the specified file

Provider options:
 -provider-path val  Provider load path (must be before 'provider' argument if required)
 -provider val       Provider to load (can be specified multiple times)
 -propquery val      Property query used when fetching algorithms
```

</details>

#### `openssl des-ecb`

**帮助命令**：`openssl des-ecb -help`。**用法**：`Usage: des-ecb [options]`

**解读**：这是固定密码名称 `des-ecb` 的 `enc` 入口；`-e`/`-d` 控制文件加解密，密钥或口令、IV、输入输出必须按 [`enc`](#openssl-enc) 说明固定。帮助可见不等于本项目允许该算法或模式。

<details><summary>展开本机 `-help` 内容</summary>

```text
Usage: des-ecb [options]

General options:
 -help               Display this summary
 -list               List ciphers
 -ciphers            Alias for -list
 -e                  Encrypt
 -d                  Decrypt
 -p                  Print the iv/key
 -P                  Print the iv/key and exit
 -engine val         Use engine, possibly a hardware device

Input options:
 -in infile          Input file
 -k val              Passphrase
 -kfile infile       Read passphrase from file

Output options:
 -out outfile        Output file
 -pass val           Passphrase source
 -v                  Verbose output
 -a                  Base64 encode/decode, depending on encryption flag
 -base64             Same as option -a
 -A                  Used with -[base64|a] to specify base64 buffer as a single line

Encryption options:
 -nopad              Disable standard block padding
 -salt               Use salt in the KDF (default)
 -nosalt             Do not use salt in the KDF
 -debug              Print debug info
 -bufsize val        Buffer size
 -K val              Raw key, in hex
 -S val              Salt, in hex
 -iv val             IV in hex
 -md val             Use specified digest to create a key from the passphrase
 -iter +int          Specify the iteration count and force use of PBKDF2
 -pbkdf2             Use password-based key derivation function 2
 -none               Don't encrypt
 -*                  Any supported cipher

Random state options:
 -rand val           Load the given file(s) into the random number generator
 -writerand outfile  Write random data to the specified file

Provider options:
 -provider-path val  Provider load path (must be before 'provider' argument if required)
 -provider val       Provider to load (can be specified multiple times)
 -propquery val      Property query used when fetching algorithms
```

</details>

#### `openssl des-ede`

**帮助命令**：`openssl des-ede -help`。**用法**：`Usage: des-ede [options]`

**解读**：这是固定密码名称 `des-ede` 的 `enc` 入口；`-e`/`-d` 控制文件加解密，密钥或口令、IV、输入输出必须按 [`enc`](#openssl-enc) 说明固定。帮助可见不等于本项目允许该算法或模式。

<details><summary>展开本机 `-help` 内容</summary>

```text
Usage: des-ede [options]

General options:
 -help               Display this summary
 -list               List ciphers
 -ciphers            Alias for -list
 -e                  Encrypt
 -d                  Decrypt
 -p                  Print the iv/key
 -P                  Print the iv/key and exit
 -engine val         Use engine, possibly a hardware device

Input options:
 -in infile          Input file
 -k val              Passphrase
 -kfile infile       Read passphrase from file

Output options:
 -out outfile        Output file
 -pass val           Passphrase source
 -v                  Verbose output
 -a                  Base64 encode/decode, depending on encryption flag
 -base64             Same as option -a
 -A                  Used with -[base64|a] to specify base64 buffer as a single line

Encryption options:
 -nopad              Disable standard block padding
 -salt               Use salt in the KDF (default)
 -nosalt             Do not use salt in the KDF
 -debug              Print debug info
 -bufsize val        Buffer size
 -K val              Raw key, in hex
 -S val              Salt, in hex
 -iv val             IV in hex
 -md val             Use specified digest to create a key from the passphrase
 -iter +int          Specify the iteration count and force use of PBKDF2
 -pbkdf2             Use password-based key derivation function 2
 -none               Don't encrypt
 -*                  Any supported cipher

Random state options:
 -rand val           Load the given file(s) into the random number generator
 -writerand outfile  Write random data to the specified file

Provider options:
 -provider-path val  Provider load path (must be before 'provider' argument if required)
 -provider val       Provider to load (can be specified multiple times)
 -propquery val      Property query used when fetching algorithms
```

</details>

#### `openssl des-ede-cbc`

**帮助命令**：`openssl des-ede-cbc -help`。**用法**：`Usage: des-ede-cbc [options]`

**解读**：这是固定密码名称 `des-ede-cbc` 的 `enc` 入口；`-e`/`-d` 控制文件加解密，密钥或口令、IV、输入输出必须按 [`enc`](#openssl-enc) 说明固定。帮助可见不等于本项目允许该算法或模式。

<details><summary>展开本机 `-help` 内容</summary>

```text
Usage: des-ede-cbc [options]

General options:
 -help               Display this summary
 -list               List ciphers
 -ciphers            Alias for -list
 -e                  Encrypt
 -d                  Decrypt
 -p                  Print the iv/key
 -P                  Print the iv/key and exit
 -engine val         Use engine, possibly a hardware device

Input options:
 -in infile          Input file
 -k val              Passphrase
 -kfile infile       Read passphrase from file

Output options:
 -out outfile        Output file
 -pass val           Passphrase source
 -v                  Verbose output
 -a                  Base64 encode/decode, depending on encryption flag
 -base64             Same as option -a
 -A                  Used with -[base64|a] to specify base64 buffer as a single line

Encryption options:
 -nopad              Disable standard block padding
 -salt               Use salt in the KDF (default)
 -nosalt             Do not use salt in the KDF
 -debug              Print debug info
 -bufsize val        Buffer size
 -K val              Raw key, in hex
 -S val              Salt, in hex
 -iv val             IV in hex
 -md val             Use specified digest to create a key from the passphrase
 -iter +int          Specify the iteration count and force use of PBKDF2
 -pbkdf2             Use password-based key derivation function 2
 -none               Don't encrypt
 -*                  Any supported cipher

Random state options:
 -rand val           Load the given file(s) into the random number generator
 -writerand outfile  Write random data to the specified file

Provider options:
 -provider-path val  Provider load path (must be before 'provider' argument if required)
 -provider val       Provider to load (can be specified multiple times)
 -propquery val      Property query used when fetching algorithms
```

</details>

#### `openssl des-ede-cfb`

**帮助命令**：`openssl des-ede-cfb -help`。**用法**：`Usage: des-ede-cfb [options]`

**解读**：这是固定密码名称 `des-ede-cfb` 的 `enc` 入口；`-e`/`-d` 控制文件加解密，密钥或口令、IV、输入输出必须按 [`enc`](#openssl-enc) 说明固定。帮助可见不等于本项目允许该算法或模式。

<details><summary>展开本机 `-help` 内容</summary>

```text
Usage: des-ede-cfb [options]

General options:
 -help               Display this summary
 -list               List ciphers
 -ciphers            Alias for -list
 -e                  Encrypt
 -d                  Decrypt
 -p                  Print the iv/key
 -P                  Print the iv/key and exit
 -engine val         Use engine, possibly a hardware device

Input options:
 -in infile          Input file
 -k val              Passphrase
 -kfile infile       Read passphrase from file

Output options:
 -out outfile        Output file
 -pass val           Passphrase source
 -v                  Verbose output
 -a                  Base64 encode/decode, depending on encryption flag
 -base64             Same as option -a
 -A                  Used with -[base64|a] to specify base64 buffer as a single line

Encryption options:
 -nopad              Disable standard block padding
 -salt               Use salt in the KDF (default)
 -nosalt             Do not use salt in the KDF
 -debug              Print debug info
 -bufsize val        Buffer size
 -K val              Raw key, in hex
 -S val              Salt, in hex
 -iv val             IV in hex
 -md val             Use specified digest to create a key from the passphrase
 -iter +int          Specify the iteration count and force use of PBKDF2
 -pbkdf2             Use password-based key derivation function 2
 -none               Don't encrypt
 -*                  Any supported cipher

Random state options:
 -rand val           Load the given file(s) into the random number generator
 -writerand outfile  Write random data to the specified file

Provider options:
 -provider-path val  Provider load path (must be before 'provider' argument if required)
 -provider val       Provider to load (can be specified multiple times)
 -propquery val      Property query used when fetching algorithms
```

</details>

#### `openssl des-ede-ofb`

**帮助命令**：`openssl des-ede-ofb -help`。**用法**：`Usage: des-ede-ofb [options]`

**解读**：这是固定密码名称 `des-ede-ofb` 的 `enc` 入口；`-e`/`-d` 控制文件加解密，密钥或口令、IV、输入输出必须按 [`enc`](#openssl-enc) 说明固定。帮助可见不等于本项目允许该算法或模式。

<details><summary>展开本机 `-help` 内容</summary>

```text
Usage: des-ede-ofb [options]

General options:
 -help               Display this summary
 -list               List ciphers
 -ciphers            Alias for -list
 -e                  Encrypt
 -d                  Decrypt
 -p                  Print the iv/key
 -P                  Print the iv/key and exit
 -engine val         Use engine, possibly a hardware device

Input options:
 -in infile          Input file
 -k val              Passphrase
 -kfile infile       Read passphrase from file

Output options:
 -out outfile        Output file
 -pass val           Passphrase source
 -v                  Verbose output
 -a                  Base64 encode/decode, depending on encryption flag
 -base64             Same as option -a
 -A                  Used with -[base64|a] to specify base64 buffer as a single line

Encryption options:
 -nopad              Disable standard block padding
 -salt               Use salt in the KDF (default)
 -nosalt             Do not use salt in the KDF
 -debug              Print debug info
 -bufsize val        Buffer size
 -K val              Raw key, in hex
 -S val              Salt, in hex
 -iv val             IV in hex
 -md val             Use specified digest to create a key from the passphrase
 -iter +int          Specify the iteration count and force use of PBKDF2
 -pbkdf2             Use password-based key derivation function 2
 -none               Don't encrypt
 -*                  Any supported cipher

Random state options:
 -rand val           Load the given file(s) into the random number generator
 -writerand outfile  Write random data to the specified file

Provider options:
 -provider-path val  Provider load path (must be before 'provider' argument if required)
 -provider val       Provider to load (can be specified multiple times)
 -propquery val      Property query used when fetching algorithms
```

</details>

#### `openssl des-ede3`

**帮助命令**：`openssl des-ede3 -help`。**用法**：`Usage: des-ede3 [options]`

**解读**：这是固定密码名称 `des-ede3` 的 `enc` 入口；`-e`/`-d` 控制文件加解密，密钥或口令、IV、输入输出必须按 [`enc`](#openssl-enc) 说明固定。帮助可见不等于本项目允许该算法或模式。

<details><summary>展开本机 `-help` 内容</summary>

```text
Usage: des-ede3 [options]

General options:
 -help               Display this summary
 -list               List ciphers
 -ciphers            Alias for -list
 -e                  Encrypt
 -d                  Decrypt
 -p                  Print the iv/key
 -P                  Print the iv/key and exit
 -engine val         Use engine, possibly a hardware device

Input options:
 -in infile          Input file
 -k val              Passphrase
 -kfile infile       Read passphrase from file

Output options:
 -out outfile        Output file
 -pass val           Passphrase source
 -v                  Verbose output
 -a                  Base64 encode/decode, depending on encryption flag
 -base64             Same as option -a
 -A                  Used with -[base64|a] to specify base64 buffer as a single line

Encryption options:
 -nopad              Disable standard block padding
 -salt               Use salt in the KDF (default)
 -nosalt             Do not use salt in the KDF
 -debug              Print debug info
 -bufsize val        Buffer size
 -K val              Raw key, in hex
 -S val              Salt, in hex
 -iv val             IV in hex
 -md val             Use specified digest to create a key from the passphrase
 -iter +int          Specify the iteration count and force use of PBKDF2
 -pbkdf2             Use password-based key derivation function 2
 -none               Don't encrypt
 -*                  Any supported cipher

Random state options:
 -rand val           Load the given file(s) into the random number generator
 -writerand outfile  Write random data to the specified file

Provider options:
 -provider-path val  Provider load path (must be before 'provider' argument if required)
 -provider val       Provider to load (can be specified multiple times)
 -propquery val      Property query used when fetching algorithms
```

</details>

#### `openssl des-ede3-cbc`

**帮助命令**：`openssl des-ede3-cbc -help`。**用法**：`Usage: des-ede3-cbc [options]`

**解读**：这是固定密码名称 `des-ede3-cbc` 的 `enc` 入口；`-e`/`-d` 控制文件加解密，密钥或口令、IV、输入输出必须按 [`enc`](#openssl-enc) 说明固定。帮助可见不等于本项目允许该算法或模式。

<details><summary>展开本机 `-help` 内容</summary>

```text
Usage: des-ede3-cbc [options]

General options:
 -help               Display this summary
 -list               List ciphers
 -ciphers            Alias for -list
 -e                  Encrypt
 -d                  Decrypt
 -p                  Print the iv/key
 -P                  Print the iv/key and exit
 -engine val         Use engine, possibly a hardware device

Input options:
 -in infile          Input file
 -k val              Passphrase
 -kfile infile       Read passphrase from file

Output options:
 -out outfile        Output file
 -pass val           Passphrase source
 -v                  Verbose output
 -a                  Base64 encode/decode, depending on encryption flag
 -base64             Same as option -a
 -A                  Used with -[base64|a] to specify base64 buffer as a single line

Encryption options:
 -nopad              Disable standard block padding
 -salt               Use salt in the KDF (default)
 -nosalt             Do not use salt in the KDF
 -debug              Print debug info
 -bufsize val        Buffer size
 -K val              Raw key, in hex
 -S val              Salt, in hex
 -iv val             IV in hex
 -md val             Use specified digest to create a key from the passphrase
 -iter +int          Specify the iteration count and force use of PBKDF2
 -pbkdf2             Use password-based key derivation function 2
 -none               Don't encrypt
 -*                  Any supported cipher

Random state options:
 -rand val           Load the given file(s) into the random number generator
 -writerand outfile  Write random data to the specified file

Provider options:
 -provider-path val  Provider load path (must be before 'provider' argument if required)
 -provider val       Provider to load (can be specified multiple times)
 -propquery val      Property query used when fetching algorithms
```

</details>

#### `openssl des-ede3-cfb`

**帮助命令**：`openssl des-ede3-cfb -help`。**用法**：`Usage: des-ede3-cfb [options]`

**解读**：这是固定密码名称 `des-ede3-cfb` 的 `enc` 入口；`-e`/`-d` 控制文件加解密，密钥或口令、IV、输入输出必须按 [`enc`](#openssl-enc) 说明固定。帮助可见不等于本项目允许该算法或模式。

<details><summary>展开本机 `-help` 内容</summary>

```text
Usage: des-ede3-cfb [options]

General options:
 -help               Display this summary
 -list               List ciphers
 -ciphers            Alias for -list
 -e                  Encrypt
 -d                  Decrypt
 -p                  Print the iv/key
 -P                  Print the iv/key and exit
 -engine val         Use engine, possibly a hardware device

Input options:
 -in infile          Input file
 -k val              Passphrase
 -kfile infile       Read passphrase from file

Output options:
 -out outfile        Output file
 -pass val           Passphrase source
 -v                  Verbose output
 -a                  Base64 encode/decode, depending on encryption flag
 -base64             Same as option -a
 -A                  Used with -[base64|a] to specify base64 buffer as a single line

Encryption options:
 -nopad              Disable standard block padding
 -salt               Use salt in the KDF (default)
 -nosalt             Do not use salt in the KDF
 -debug              Print debug info
 -bufsize val        Buffer size
 -K val              Raw key, in hex
 -S val              Salt, in hex
 -iv val             IV in hex
 -md val             Use specified digest to create a key from the passphrase
 -iter +int          Specify the iteration count and force use of PBKDF2
 -pbkdf2             Use password-based key derivation function 2
 -none               Don't encrypt
 -*                  Any supported cipher

Random state options:
 -rand val           Load the given file(s) into the random number generator
 -writerand outfile  Write random data to the specified file

Provider options:
 -provider-path val  Provider load path (must be before 'provider' argument if required)
 -provider val       Provider to load (can be specified multiple times)
 -propquery val      Property query used when fetching algorithms
```

</details>

#### `openssl des-ede3-ofb`

**帮助命令**：`openssl des-ede3-ofb -help`。**用法**：`Usage: des-ede3-ofb [options]`

**解读**：这是固定密码名称 `des-ede3-ofb` 的 `enc` 入口；`-e`/`-d` 控制文件加解密，密钥或口令、IV、输入输出必须按 [`enc`](#openssl-enc) 说明固定。帮助可见不等于本项目允许该算法或模式。

<details><summary>展开本机 `-help` 内容</summary>

```text
Usage: des-ede3-ofb [options]

General options:
 -help               Display this summary
 -list               List ciphers
 -ciphers            Alias for -list
 -e                  Encrypt
 -d                  Decrypt
 -p                  Print the iv/key
 -P                  Print the iv/key and exit
 -engine val         Use engine, possibly a hardware device

Input options:
 -in infile          Input file
 -k val              Passphrase
 -kfile infile       Read passphrase from file

Output options:
 -out outfile        Output file
 -pass val           Passphrase source
 -v                  Verbose output
 -a                  Base64 encode/decode, depending on encryption flag
 -base64             Same as option -a
 -A                  Used with -[base64|a] to specify base64 buffer as a single line

Encryption options:
 -nopad              Disable standard block padding
 -salt               Use salt in the KDF (default)
 -nosalt             Do not use salt in the KDF
 -debug              Print debug info
 -bufsize val        Buffer size
 -K val              Raw key, in hex
 -S val              Salt, in hex
 -iv val             IV in hex
 -md val             Use specified digest to create a key from the passphrase
 -iter +int          Specify the iteration count and force use of PBKDF2
 -pbkdf2             Use password-based key derivation function 2
 -none               Don't encrypt
 -*                  Any supported cipher

Random state options:
 -rand val           Load the given file(s) into the random number generator
 -writerand outfile  Write random data to the specified file

Provider options:
 -provider-path val  Provider load path (must be before 'provider' argument if required)
 -provider val       Provider to load (can be specified multiple times)
 -propquery val      Property query used when fetching algorithms
```

</details>

#### `openssl des-ofb`

**帮助命令**：`openssl des-ofb -help`。**用法**：`Usage: des-ofb [options]`

**解读**：这是固定密码名称 `des-ofb` 的 `enc` 入口；`-e`/`-d` 控制文件加解密，密钥或口令、IV、输入输出必须按 [`enc`](#openssl-enc) 说明固定。帮助可见不等于本项目允许该算法或模式。

<details><summary>展开本机 `-help` 内容</summary>

```text
Usage: des-ofb [options]

General options:
 -help               Display this summary
 -list               List ciphers
 -ciphers            Alias for -list
 -e                  Encrypt
 -d                  Decrypt
 -p                  Print the iv/key
 -P                  Print the iv/key and exit
 -engine val         Use engine, possibly a hardware device

Input options:
 -in infile          Input file
 -k val              Passphrase
 -kfile infile       Read passphrase from file

Output options:
 -out outfile        Output file
 -pass val           Passphrase source
 -v                  Verbose output
 -a                  Base64 encode/decode, depending on encryption flag
 -base64             Same as option -a
 -A                  Used with -[base64|a] to specify base64 buffer as a single line

Encryption options:
 -nopad              Disable standard block padding
 -salt               Use salt in the KDF (default)
 -nosalt             Do not use salt in the KDF
 -debug              Print debug info
 -bufsize val        Buffer size
 -K val              Raw key, in hex
 -S val              Salt, in hex
 -iv val             IV in hex
 -md val             Use specified digest to create a key from the passphrase
 -iter +int          Specify the iteration count and force use of PBKDF2
 -pbkdf2             Use password-based key derivation function 2
 -none               Don't encrypt
 -*                  Any supported cipher

Random state options:
 -rand val           Load the given file(s) into the random number generator
 -writerand outfile  Write random data to the specified file

Provider options:
 -provider-path val  Provider load path (must be before 'provider' argument if required)
 -provider val       Provider to load (can be specified multiple times)
 -propquery val      Property query used when fetching algorithms
```

</details>

#### `openssl des3`

**帮助命令**：`openssl des3 -help`。**用法**：`Usage: des3 [options]`

**解读**：这是固定密码名称 `des3` 的 `enc` 入口；`-e`/`-d` 控制文件加解密，密钥或口令、IV、输入输出必须按 [`enc`](#openssl-enc) 说明固定。帮助可见不等于本项目允许该算法或模式。

<details><summary>展开本机 `-help` 内容</summary>

```text
Usage: des3 [options]

General options:
 -help               Display this summary
 -list               List ciphers
 -ciphers            Alias for -list
 -e                  Encrypt
 -d                  Decrypt
 -p                  Print the iv/key
 -P                  Print the iv/key and exit
 -engine val         Use engine, possibly a hardware device

Input options:
 -in infile          Input file
 -k val              Passphrase
 -kfile infile       Read passphrase from file

Output options:
 -out outfile        Output file
 -pass val           Passphrase source
 -v                  Verbose output
 -a                  Base64 encode/decode, depending on encryption flag
 -base64             Same as option -a
 -A                  Used with -[base64|a] to specify base64 buffer as a single line

Encryption options:
 -nopad              Disable standard block padding
 -salt               Use salt in the KDF (default)
 -nosalt             Do not use salt in the KDF
 -debug              Print debug info
 -bufsize val        Buffer size
 -K val              Raw key, in hex
 -S val              Salt, in hex
 -iv val             IV in hex
 -md val             Use specified digest to create a key from the passphrase
 -iter +int          Specify the iteration count and force use of PBKDF2
 -pbkdf2             Use password-based key derivation function 2
 -none               Don't encrypt
 -*                  Any supported cipher

Random state options:
 -rand val           Load the given file(s) into the random number generator
 -writerand outfile  Write random data to the specified file

Provider options:
 -provider-path val  Provider load path (must be before 'provider' argument if required)
 -provider val       Provider to load (can be specified multiple times)
 -propquery val      Property query used when fetching algorithms
```

</details>

#### `openssl desx`

**帮助命令**：`openssl desx -help`。**用法**：`Usage: desx [options]`

**解读**：这是固定密码名称 `desx` 的 `enc` 入口；`-e`/`-d` 控制文件加解密，密钥或口令、IV、输入输出必须按 [`enc`](#openssl-enc) 说明固定。帮助可见不等于本项目允许该算法或模式。

<details><summary>展开本机 `-help` 内容</summary>

```text
Usage: desx [options]

General options:
 -help               Display this summary
 -list               List ciphers
 -ciphers            Alias for -list
 -e                  Encrypt
 -d                  Decrypt
 -p                  Print the iv/key
 -P                  Print the iv/key and exit
 -engine val         Use engine, possibly a hardware device

Input options:
 -in infile          Input file
 -k val              Passphrase
 -kfile infile       Read passphrase from file

Output options:
 -out outfile        Output file
 -pass val           Passphrase source
 -v                  Verbose output
 -a                  Base64 encode/decode, depending on encryption flag
 -base64             Same as option -a
 -A                  Used with -[base64|a] to specify base64 buffer as a single line

Encryption options:
 -nopad              Disable standard block padding
 -salt               Use salt in the KDF (default)
 -nosalt             Do not use salt in the KDF
 -debug              Print debug info
 -bufsize val        Buffer size
 -K val              Raw key, in hex
 -S val              Salt, in hex
 -iv val             IV in hex
 -md val             Use specified digest to create a key from the passphrase
 -iter +int          Specify the iteration count and force use of PBKDF2
 -pbkdf2             Use password-based key derivation function 2
 -none               Don't encrypt
 -*                  Any supported cipher

Random state options:
 -rand val           Load the given file(s) into the random number generator
 -writerand outfile  Write random data to the specified file

Provider options:
 -provider-path val  Provider load path (must be before 'provider' argument if required)
 -provider val       Provider to load (can be specified multiple times)
 -propquery val      Property query used when fetching algorithms
```

</details>

#### `openssl rc2`

**帮助命令**：`openssl rc2 -help`。**用法**：`Usage: rc2 [options]`

**解读**：这是固定密码名称 `rc2` 的 `enc` 入口；`-e`/`-d` 控制文件加解密，密钥或口令、IV、输入输出必须按 [`enc`](#openssl-enc) 说明固定。帮助可见不等于本项目允许该算法或模式。

<details><summary>展开本机 `-help` 内容</summary>

```text
Usage: rc2 [options]

General options:
 -help               Display this summary
 -list               List ciphers
 -ciphers            Alias for -list
 -e                  Encrypt
 -d                  Decrypt
 -p                  Print the iv/key
 -P                  Print the iv/key and exit
 -engine val         Use engine, possibly a hardware device

Input options:
 -in infile          Input file
 -k val              Passphrase
 -kfile infile       Read passphrase from file

Output options:
 -out outfile        Output file
 -pass val           Passphrase source
 -v                  Verbose output
 -a                  Base64 encode/decode, depending on encryption flag
 -base64             Same as option -a
 -A                  Used with -[base64|a] to specify base64 buffer as a single line

Encryption options:
 -nopad              Disable standard block padding
 -salt               Use salt in the KDF (default)
 -nosalt             Do not use salt in the KDF
 -debug              Print debug info
 -bufsize val        Buffer size
 -K val              Raw key, in hex
 -S val              Salt, in hex
 -iv val             IV in hex
 -md val             Use specified digest to create a key from the passphrase
 -iter +int          Specify the iteration count and force use of PBKDF2
 -pbkdf2             Use password-based key derivation function 2
 -none               Don't encrypt
 -*                  Any supported cipher

Random state options:
 -rand val           Load the given file(s) into the random number generator
 -writerand outfile  Write random data to the specified file

Provider options:
 -provider-path val  Provider load path (must be before 'provider' argument if required)
 -provider val       Provider to load (can be specified multiple times)
 -propquery val      Property query used when fetching algorithms
```

</details>

#### `openssl rc2-40-cbc`

**帮助命令**：`openssl rc2-40-cbc -help`。**用法**：`Usage: rc2-40-cbc [options]`

**解读**：这是固定密码名称 `rc2-40-cbc` 的 `enc` 入口；`-e`/`-d` 控制文件加解密，密钥或口令、IV、输入输出必须按 [`enc`](#openssl-enc) 说明固定。帮助可见不等于本项目允许该算法或模式。

<details><summary>展开本机 `-help` 内容</summary>

```text
Usage: rc2-40-cbc [options]

General options:
 -help               Display this summary
 -list               List ciphers
 -ciphers            Alias for -list
 -e                  Encrypt
 -d                  Decrypt
 -p                  Print the iv/key
 -P                  Print the iv/key and exit
 -engine val         Use engine, possibly a hardware device

Input options:
 -in infile          Input file
 -k val              Passphrase
 -kfile infile       Read passphrase from file

Output options:
 -out outfile        Output file
 -pass val           Passphrase source
 -v                  Verbose output
 -a                  Base64 encode/decode, depending on encryption flag
 -base64             Same as option -a
 -A                  Used with -[base64|a] to specify base64 buffer as a single line

Encryption options:
 -nopad              Disable standard block padding
 -salt               Use salt in the KDF (default)
 -nosalt             Do not use salt in the KDF
 -debug              Print debug info
 -bufsize val        Buffer size
 -K val              Raw key, in hex
 -S val              Salt, in hex
 -iv val             IV in hex
 -md val             Use specified digest to create a key from the passphrase
 -iter +int          Specify the iteration count and force use of PBKDF2
 -pbkdf2             Use password-based key derivation function 2
 -none               Don't encrypt
 -*                  Any supported cipher

Random state options:
 -rand val           Load the given file(s) into the random number generator
 -writerand outfile  Write random data to the specified file

Provider options:
 -provider-path val  Provider load path (must be before 'provider' argument if required)
 -provider val       Provider to load (can be specified multiple times)
 -propquery val      Property query used when fetching algorithms
```

</details>

#### `openssl rc2-64-cbc`

**帮助命令**：`openssl rc2-64-cbc -help`。**用法**：`Usage: rc2-64-cbc [options]`

**解读**：这是固定密码名称 `rc2-64-cbc` 的 `enc` 入口；`-e`/`-d` 控制文件加解密，密钥或口令、IV、输入输出必须按 [`enc`](#openssl-enc) 说明固定。帮助可见不等于本项目允许该算法或模式。

<details><summary>展开本机 `-help` 内容</summary>

```text
Usage: rc2-64-cbc [options]

General options:
 -help               Display this summary
 -list               List ciphers
 -ciphers            Alias for -list
 -e                  Encrypt
 -d                  Decrypt
 -p                  Print the iv/key
 -P                  Print the iv/key and exit
 -engine val         Use engine, possibly a hardware device

Input options:
 -in infile          Input file
 -k val              Passphrase
 -kfile infile       Read passphrase from file

Output options:
 -out outfile        Output file
 -pass val           Passphrase source
 -v                  Verbose output
 -a                  Base64 encode/decode, depending on encryption flag
 -base64             Same as option -a
 -A                  Used with -[base64|a] to specify base64 buffer as a single line

Encryption options:
 -nopad              Disable standard block padding
 -salt               Use salt in the KDF (default)
 -nosalt             Do not use salt in the KDF
 -debug              Print debug info
 -bufsize val        Buffer size
 -K val              Raw key, in hex
 -S val              Salt, in hex
 -iv val             IV in hex
 -md val             Use specified digest to create a key from the passphrase
 -iter +int          Specify the iteration count and force use of PBKDF2
 -pbkdf2             Use password-based key derivation function 2
 -none               Don't encrypt
 -*                  Any supported cipher

Random state options:
 -rand val           Load the given file(s) into the random number generator
 -writerand outfile  Write random data to the specified file

Provider options:
 -provider-path val  Provider load path (must be before 'provider' argument if required)
 -provider val       Provider to load (can be specified multiple times)
 -propquery val      Property query used when fetching algorithms
```

</details>

#### `openssl rc2-cbc`

**帮助命令**：`openssl rc2-cbc -help`。**用法**：`Usage: rc2-cbc [options]`

**解读**：这是固定密码名称 `rc2-cbc` 的 `enc` 入口；`-e`/`-d` 控制文件加解密，密钥或口令、IV、输入输出必须按 [`enc`](#openssl-enc) 说明固定。帮助可见不等于本项目允许该算法或模式。

<details><summary>展开本机 `-help` 内容</summary>

```text
Usage: rc2-cbc [options]

General options:
 -help               Display this summary
 -list               List ciphers
 -ciphers            Alias for -list
 -e                  Encrypt
 -d                  Decrypt
 -p                  Print the iv/key
 -P                  Print the iv/key and exit
 -engine val         Use engine, possibly a hardware device

Input options:
 -in infile          Input file
 -k val              Passphrase
 -kfile infile       Read passphrase from file

Output options:
 -out outfile        Output file
 -pass val           Passphrase source
 -v                  Verbose output
 -a                  Base64 encode/decode, depending on encryption flag
 -base64             Same as option -a
 -A                  Used with -[base64|a] to specify base64 buffer as a single line

Encryption options:
 -nopad              Disable standard block padding
 -salt               Use salt in the KDF (default)
 -nosalt             Do not use salt in the KDF
 -debug              Print debug info
 -bufsize val        Buffer size
 -K val              Raw key, in hex
 -S val              Salt, in hex
 -iv val             IV in hex
 -md val             Use specified digest to create a key from the passphrase
 -iter +int          Specify the iteration count and force use of PBKDF2
 -pbkdf2             Use password-based key derivation function 2
 -none               Don't encrypt
 -*                  Any supported cipher

Random state options:
 -rand val           Load the given file(s) into the random number generator
 -writerand outfile  Write random data to the specified file

Provider options:
 -provider-path val  Provider load path (must be before 'provider' argument if required)
 -provider val       Provider to load (can be specified multiple times)
 -propquery val      Property query used when fetching algorithms
```

</details>

#### `openssl rc2-cfb`

**帮助命令**：`openssl rc2-cfb -help`。**用法**：`Usage: rc2-cfb [options]`

**解读**：这是固定密码名称 `rc2-cfb` 的 `enc` 入口；`-e`/`-d` 控制文件加解密，密钥或口令、IV、输入输出必须按 [`enc`](#openssl-enc) 说明固定。帮助可见不等于本项目允许该算法或模式。

<details><summary>展开本机 `-help` 内容</summary>

```text
Usage: rc2-cfb [options]

General options:
 -help               Display this summary
 -list               List ciphers
 -ciphers            Alias for -list
 -e                  Encrypt
 -d                  Decrypt
 -p                  Print the iv/key
 -P                  Print the iv/key and exit
 -engine val         Use engine, possibly a hardware device

Input options:
 -in infile          Input file
 -k val              Passphrase
 -kfile infile       Read passphrase from file

Output options:
 -out outfile        Output file
 -pass val           Passphrase source
 -v                  Verbose output
 -a                  Base64 encode/decode, depending on encryption flag
 -base64             Same as option -a
 -A                  Used with -[base64|a] to specify base64 buffer as a single line

Encryption options:
 -nopad              Disable standard block padding
 -salt               Use salt in the KDF (default)
 -nosalt             Do not use salt in the KDF
 -debug              Print debug info
 -bufsize val        Buffer size
 -K val              Raw key, in hex
 -S val              Salt, in hex
 -iv val             IV in hex
 -md val             Use specified digest to create a key from the passphrase
 -iter +int          Specify the iteration count and force use of PBKDF2
 -pbkdf2             Use password-based key derivation function 2
 -none               Don't encrypt
 -*                  Any supported cipher

Random state options:
 -rand val           Load the given file(s) into the random number generator
 -writerand outfile  Write random data to the specified file

Provider options:
 -provider-path val  Provider load path (must be before 'provider' argument if required)
 -provider val       Provider to load (can be specified multiple times)
 -propquery val      Property query used when fetching algorithms
```

</details>

#### `openssl rc2-ecb`

**帮助命令**：`openssl rc2-ecb -help`。**用法**：`Usage: rc2-ecb [options]`

**解读**：这是固定密码名称 `rc2-ecb` 的 `enc` 入口；`-e`/`-d` 控制文件加解密，密钥或口令、IV、输入输出必须按 [`enc`](#openssl-enc) 说明固定。帮助可见不等于本项目允许该算法或模式。

<details><summary>展开本机 `-help` 内容</summary>

```text
Usage: rc2-ecb [options]

General options:
 -help               Display this summary
 -list               List ciphers
 -ciphers            Alias for -list
 -e                  Encrypt
 -d                  Decrypt
 -p                  Print the iv/key
 -P                  Print the iv/key and exit
 -engine val         Use engine, possibly a hardware device

Input options:
 -in infile          Input file
 -k val              Passphrase
 -kfile infile       Read passphrase from file

Output options:
 -out outfile        Output file
 -pass val           Passphrase source
 -v                  Verbose output
 -a                  Base64 encode/decode, depending on encryption flag
 -base64             Same as option -a
 -A                  Used with -[base64|a] to specify base64 buffer as a single line

Encryption options:
 -nopad              Disable standard block padding
 -salt               Use salt in the KDF (default)
 -nosalt             Do not use salt in the KDF
 -debug              Print debug info
 -bufsize val        Buffer size
 -K val              Raw key, in hex
 -S val              Salt, in hex
 -iv val             IV in hex
 -md val             Use specified digest to create a key from the passphrase
 -iter +int          Specify the iteration count and force use of PBKDF2
 -pbkdf2             Use password-based key derivation function 2
 -none               Don't encrypt
 -*                  Any supported cipher

Random state options:
 -rand val           Load the given file(s) into the random number generator
 -writerand outfile  Write random data to the specified file

Provider options:
 -provider-path val  Provider load path (must be before 'provider' argument if required)
 -provider val       Provider to load (can be specified multiple times)
 -propquery val      Property query used when fetching algorithms
```

</details>

#### `openssl rc2-ofb`

**帮助命令**：`openssl rc2-ofb -help`。**用法**：`Usage: rc2-ofb [options]`

**解读**：这是固定密码名称 `rc2-ofb` 的 `enc` 入口；`-e`/`-d` 控制文件加解密，密钥或口令、IV、输入输出必须按 [`enc`](#openssl-enc) 说明固定。帮助可见不等于本项目允许该算法或模式。

<details><summary>展开本机 `-help` 内容</summary>

```text
Usage: rc2-ofb [options]

General options:
 -help               Display this summary
 -list               List ciphers
 -ciphers            Alias for -list
 -e                  Encrypt
 -d                  Decrypt
 -p                  Print the iv/key
 -P                  Print the iv/key and exit
 -engine val         Use engine, possibly a hardware device

Input options:
 -in infile          Input file
 -k val              Passphrase
 -kfile infile       Read passphrase from file

Output options:
 -out outfile        Output file
 -pass val           Passphrase source
 -v                  Verbose output
 -a                  Base64 encode/decode, depending on encryption flag
 -base64             Same as option -a
 -A                  Used with -[base64|a] to specify base64 buffer as a single line

Encryption options:
 -nopad              Disable standard block padding
 -salt               Use salt in the KDF (default)
 -nosalt             Do not use salt in the KDF
 -debug              Print debug info
 -bufsize val        Buffer size
 -K val              Raw key, in hex
 -S val              Salt, in hex
 -iv val             IV in hex
 -md val             Use specified digest to create a key from the passphrase
 -iter +int          Specify the iteration count and force use of PBKDF2
 -pbkdf2             Use password-based key derivation function 2
 -none               Don't encrypt
 -*                  Any supported cipher

Random state options:
 -rand val           Load the given file(s) into the random number generator
 -writerand outfile  Write random data to the specified file

Provider options:
 -provider-path val  Provider load path (must be before 'provider' argument if required)
 -provider val       Provider to load (can be specified multiple times)
 -propquery val      Property query used when fetching algorithms
```

</details>

#### `openssl rc4`

**帮助命令**：`openssl rc4 -help`。**用法**：`Usage: rc4 [options]`

**解读**：这是固定密码名称 `rc4` 的 `enc` 入口；`-e`/`-d` 控制文件加解密，密钥或口令、IV、输入输出必须按 [`enc`](#openssl-enc) 说明固定。帮助可见不等于本项目允许该算法或模式。

<details><summary>展开本机 `-help` 内容</summary>

```text
Usage: rc4 [options]

General options:
 -help               Display this summary
 -list               List ciphers
 -ciphers            Alias for -list
 -e                  Encrypt
 -d                  Decrypt
 -p                  Print the iv/key
 -P                  Print the iv/key and exit
 -engine val         Use engine, possibly a hardware device

Input options:
 -in infile          Input file
 -k val              Passphrase
 -kfile infile       Read passphrase from file

Output options:
 -out outfile        Output file
 -pass val           Passphrase source
 -v                  Verbose output
 -a                  Base64 encode/decode, depending on encryption flag
 -base64             Same as option -a
 -A                  Used with -[base64|a] to specify base64 buffer as a single line

Encryption options:
 -nopad              Disable standard block padding
 -salt               Use salt in the KDF (default)
 -nosalt             Do not use salt in the KDF
 -debug              Print debug info
 -bufsize val        Buffer size
 -K val              Raw key, in hex
 -S val              Salt, in hex
 -iv val             IV in hex
 -md val             Use specified digest to create a key from the passphrase
 -iter +int          Specify the iteration count and force use of PBKDF2
 -pbkdf2             Use password-based key derivation function 2
 -none               Don't encrypt
 -*                  Any supported cipher

Random state options:
 -rand val           Load the given file(s) into the random number generator
 -writerand outfile  Write random data to the specified file

Provider options:
 -provider-path val  Provider load path (must be before 'provider' argument if required)
 -provider val       Provider to load (can be specified multiple times)
 -propquery val      Property query used when fetching algorithms
```

</details>

#### `openssl rc4-40`

**帮助命令**：`openssl rc4-40 -help`。**用法**：`Usage: rc4-40 [options]`

**解读**：这是固定密码名称 `rc4-40` 的 `enc` 入口；`-e`/`-d` 控制文件加解密，密钥或口令、IV、输入输出必须按 [`enc`](#openssl-enc) 说明固定。帮助可见不等于本项目允许该算法或模式。

<details><summary>展开本机 `-help` 内容</summary>

```text
Usage: rc4-40 [options]

General options:
 -help               Display this summary
 -list               List ciphers
 -ciphers            Alias for -list
 -e                  Encrypt
 -d                  Decrypt
 -p                  Print the iv/key
 -P                  Print the iv/key and exit
 -engine val         Use engine, possibly a hardware device

Input options:
 -in infile          Input file
 -k val              Passphrase
 -kfile infile       Read passphrase from file

Output options:
 -out outfile        Output file
 -pass val           Passphrase source
 -v                  Verbose output
 -a                  Base64 encode/decode, depending on encryption flag
 -base64             Same as option -a
 -A                  Used with -[base64|a] to specify base64 buffer as a single line

Encryption options:
 -nopad              Disable standard block padding
 -salt               Use salt in the KDF (default)
 -nosalt             Do not use salt in the KDF
 -debug              Print debug info
 -bufsize val        Buffer size
 -K val              Raw key, in hex
 -S val              Salt, in hex
 -iv val             IV in hex
 -md val             Use specified digest to create a key from the passphrase
 -iter +int          Specify the iteration count and force use of PBKDF2
 -pbkdf2             Use password-based key derivation function 2
 -none               Don't encrypt
 -*                  Any supported cipher

Random state options:
 -rand val           Load the given file(s) into the random number generator
 -writerand outfile  Write random data to the specified file

Provider options:
 -provider-path val  Provider load path (must be before 'provider' argument if required)
 -provider val       Provider to load (can be specified multiple times)
 -propquery val      Property query used when fetching algorithms
```

</details>

#### `openssl seed`

**帮助命令**：`openssl seed -help`。**用法**：`Usage: seed [options]`

**解读**：这是固定密码名称 `seed` 的 `enc` 入口；`-e`/`-d` 控制文件加解密，密钥或口令、IV、输入输出必须按 [`enc`](#openssl-enc) 说明固定。帮助可见不等于本项目允许该算法或模式。

<details><summary>展开本机 `-help` 内容</summary>

```text
Usage: seed [options]

General options:
 -help               Display this summary
 -list               List ciphers
 -ciphers            Alias for -list
 -e                  Encrypt
 -d                  Decrypt
 -p                  Print the iv/key
 -P                  Print the iv/key and exit
 -engine val         Use engine, possibly a hardware device

Input options:
 -in infile          Input file
 -k val              Passphrase
 -kfile infile       Read passphrase from file

Output options:
 -out outfile        Output file
 -pass val           Passphrase source
 -v                  Verbose output
 -a                  Base64 encode/decode, depending on encryption flag
 -base64             Same as option -a
 -A                  Used with -[base64|a] to specify base64 buffer as a single line

Encryption options:
 -nopad              Disable standard block padding
 -salt               Use salt in the KDF (default)
 -nosalt             Do not use salt in the KDF
 -debug              Print debug info
 -bufsize val        Buffer size
 -K val              Raw key, in hex
 -S val              Salt, in hex
 -iv val             IV in hex
 -md val             Use specified digest to create a key from the passphrase
 -iter +int          Specify the iteration count and force use of PBKDF2
 -pbkdf2             Use password-based key derivation function 2
 -none               Don't encrypt
 -*                  Any supported cipher

Random state options:
 -rand val           Load the given file(s) into the random number generator
 -writerand outfile  Write random data to the specified file

Provider options:
 -provider-path val  Provider load path (must be before 'provider' argument if required)
 -provider val       Provider to load (can be specified multiple times)
 -propquery val      Property query used when fetching algorithms
```

</details>

#### `openssl seed-cbc`

**帮助命令**：`openssl seed-cbc -help`。**用法**：`Usage: seed-cbc [options]`

**解读**：这是固定密码名称 `seed-cbc` 的 `enc` 入口；`-e`/`-d` 控制文件加解密，密钥或口令、IV、输入输出必须按 [`enc`](#openssl-enc) 说明固定。帮助可见不等于本项目允许该算法或模式。

<details><summary>展开本机 `-help` 内容</summary>

```text
Usage: seed-cbc [options]

General options:
 -help               Display this summary
 -list               List ciphers
 -ciphers            Alias for -list
 -e                  Encrypt
 -d                  Decrypt
 -p                  Print the iv/key
 -P                  Print the iv/key and exit
 -engine val         Use engine, possibly a hardware device

Input options:
 -in infile          Input file
 -k val              Passphrase
 -kfile infile       Read passphrase from file

Output options:
 -out outfile        Output file
 -pass val           Passphrase source
 -v                  Verbose output
 -a                  Base64 encode/decode, depending on encryption flag
 -base64             Same as option -a
 -A                  Used with -[base64|a] to specify base64 buffer as a single line

Encryption options:
 -nopad              Disable standard block padding
 -salt               Use salt in the KDF (default)
 -nosalt             Do not use salt in the KDF
 -debug              Print debug info
 -bufsize val        Buffer size
 -K val              Raw key, in hex
 -S val              Salt, in hex
 -iv val             IV in hex
 -md val             Use specified digest to create a key from the passphrase
 -iter +int          Specify the iteration count and force use of PBKDF2
 -pbkdf2             Use password-based key derivation function 2
 -none               Don't encrypt
 -*                  Any supported cipher

Random state options:
 -rand val           Load the given file(s) into the random number generator
 -writerand outfile  Write random data to the specified file

Provider options:
 -provider-path val  Provider load path (must be before 'provider' argument if required)
 -provider val       Provider to load (can be specified multiple times)
 -propquery val      Property query used when fetching algorithms
```

</details>

#### `openssl seed-cfb`

**帮助命令**：`openssl seed-cfb -help`。**用法**：`Usage: seed-cfb [options]`

**解读**：这是固定密码名称 `seed-cfb` 的 `enc` 入口；`-e`/`-d` 控制文件加解密，密钥或口令、IV、输入输出必须按 [`enc`](#openssl-enc) 说明固定。帮助可见不等于本项目允许该算法或模式。

<details><summary>展开本机 `-help` 内容</summary>

```text
Usage: seed-cfb [options]

General options:
 -help               Display this summary
 -list               List ciphers
 -ciphers            Alias for -list
 -e                  Encrypt
 -d                  Decrypt
 -p                  Print the iv/key
 -P                  Print the iv/key and exit
 -engine val         Use engine, possibly a hardware device

Input options:
 -in infile          Input file
 -k val              Passphrase
 -kfile infile       Read passphrase from file

Output options:
 -out outfile        Output file
 -pass val           Passphrase source
 -v                  Verbose output
 -a                  Base64 encode/decode, depending on encryption flag
 -base64             Same as option -a
 -A                  Used with -[base64|a] to specify base64 buffer as a single line

Encryption options:
 -nopad              Disable standard block padding
 -salt               Use salt in the KDF (default)
 -nosalt             Do not use salt in the KDF
 -debug              Print debug info
 -bufsize val        Buffer size
 -K val              Raw key, in hex
 -S val              Salt, in hex
 -iv val             IV in hex
 -md val             Use specified digest to create a key from the passphrase
 -iter +int          Specify the iteration count and force use of PBKDF2
 -pbkdf2             Use password-based key derivation function 2
 -none               Don't encrypt
 -*                  Any supported cipher

Random state options:
 -rand val           Load the given file(s) into the random number generator
 -writerand outfile  Write random data to the specified file

Provider options:
 -provider-path val  Provider load path (must be before 'provider' argument if required)
 -provider val       Provider to load (can be specified multiple times)
 -propquery val      Property query used when fetching algorithms
```

</details>

#### `openssl seed-ecb`

**帮助命令**：`openssl seed-ecb -help`。**用法**：`Usage: seed-ecb [options]`

**解读**：这是固定密码名称 `seed-ecb` 的 `enc` 入口；`-e`/`-d` 控制文件加解密，密钥或口令、IV、输入输出必须按 [`enc`](#openssl-enc) 说明固定。帮助可见不等于本项目允许该算法或模式。

<details><summary>展开本机 `-help` 内容</summary>

```text
Usage: seed-ecb [options]

General options:
 -help               Display this summary
 -list               List ciphers
 -ciphers            Alias for -list
 -e                  Encrypt
 -d                  Decrypt
 -p                  Print the iv/key
 -P                  Print the iv/key and exit
 -engine val         Use engine, possibly a hardware device

Input options:
 -in infile          Input file
 -k val              Passphrase
 -kfile infile       Read passphrase from file

Output options:
 -out outfile        Output file
 -pass val           Passphrase source
 -v                  Verbose output
 -a                  Base64 encode/decode, depending on encryption flag
 -base64             Same as option -a
 -A                  Used with -[base64|a] to specify base64 buffer as a single line

Encryption options:
 -nopad              Disable standard block padding
 -salt               Use salt in the KDF (default)
 -nosalt             Do not use salt in the KDF
 -debug              Print debug info
 -bufsize val        Buffer size
 -K val              Raw key, in hex
 -S val              Salt, in hex
 -iv val             IV in hex
 -md val             Use specified digest to create a key from the passphrase
 -iter +int          Specify the iteration count and force use of PBKDF2
 -pbkdf2             Use password-based key derivation function 2
 -none               Don't encrypt
 -*                  Any supported cipher

Random state options:
 -rand val           Load the given file(s) into the random number generator
 -writerand outfile  Write random data to the specified file

Provider options:
 -provider-path val  Provider load path (must be before 'provider' argument if required)
 -provider val       Provider to load (can be specified multiple times)
 -propquery val      Property query used when fetching algorithms
```

</details>

#### `openssl seed-ofb`

**帮助命令**：`openssl seed-ofb -help`。**用法**：`Usage: seed-ofb [options]`

**解读**：这是固定密码名称 `seed-ofb` 的 `enc` 入口；`-e`/`-d` 控制文件加解密，密钥或口令、IV、输入输出必须按 [`enc`](#openssl-enc) 说明固定。帮助可见不等于本项目允许该算法或模式。

<details><summary>展开本机 `-help` 内容</summary>

```text
Usage: seed-ofb [options]

General options:
 -help               Display this summary
 -list               List ciphers
 -ciphers            Alias for -list
 -e                  Encrypt
 -d                  Decrypt
 -p                  Print the iv/key
 -P                  Print the iv/key and exit
 -engine val         Use engine, possibly a hardware device

Input options:
 -in infile          Input file
 -k val              Passphrase
 -kfile infile       Read passphrase from file

Output options:
 -out outfile        Output file
 -pass val           Passphrase source
 -v                  Verbose output
 -a                  Base64 encode/decode, depending on encryption flag
 -base64             Same as option -a
 -A                  Used with -[base64|a] to specify base64 buffer as a single line

Encryption options:
 -nopad              Disable standard block padding
 -salt               Use salt in the KDF (default)
 -nosalt             Do not use salt in the KDF
 -debug              Print debug info
 -bufsize val        Buffer size
 -K val              Raw key, in hex
 -S val              Salt, in hex
 -iv val             IV in hex
 -md val             Use specified digest to create a key from the passphrase
 -iter +int          Specify the iteration count and force use of PBKDF2
 -pbkdf2             Use password-based key derivation function 2
 -none               Don't encrypt
 -*                  Any supported cipher

Random state options:
 -rand val           Load the given file(s) into the random number generator
 -writerand outfile  Write random data to the specified file

Provider options:
 -provider-path val  Provider load path (must be before 'provider' argument if required)
 -provider val       Provider to load (can be specified multiple times)
 -propquery val      Property query used when fetching algorithms
```

</details>

#### `openssl sm4-cbc`

**帮助命令**：`openssl sm4-cbc -help`。**用法**：`Usage: sm4-cbc [options]`

**解读**：这是固定密码名称 `sm4-cbc` 的 `enc` 入口；`-e`/`-d` 控制文件加解密，密钥或口令、IV、输入输出必须按 [`enc`](#openssl-enc) 说明固定。帮助可见不等于本项目允许该算法或模式。

<details><summary>展开本机 `-help` 内容</summary>

```text
Usage: sm4-cbc [options]

General options:
 -help               Display this summary
 -list               List ciphers
 -ciphers            Alias for -list
 -e                  Encrypt
 -d                  Decrypt
 -p                  Print the iv/key
 -P                  Print the iv/key and exit
 -engine val         Use engine, possibly a hardware device

Input options:
 -in infile          Input file
 -k val              Passphrase
 -kfile infile       Read passphrase from file

Output options:
 -out outfile        Output file
 -pass val           Passphrase source
 -v                  Verbose output
 -a                  Base64 encode/decode, depending on encryption flag
 -base64             Same as option -a
 -A                  Used with -[base64|a] to specify base64 buffer as a single line

Encryption options:
 -nopad              Disable standard block padding
 -salt               Use salt in the KDF (default)
 -nosalt             Do not use salt in the KDF
 -debug              Print debug info
 -bufsize val        Buffer size
 -K val              Raw key, in hex
 -S val              Salt, in hex
 -iv val             IV in hex
 -md val             Use specified digest to create a key from the passphrase
 -iter +int          Specify the iteration count and force use of PBKDF2
 -pbkdf2             Use password-based key derivation function 2
 -none               Don't encrypt
 -*                  Any supported cipher

Random state options:
 -rand val           Load the given file(s) into the random number generator
 -writerand outfile  Write random data to the specified file

Provider options:
 -provider-path val  Provider load path (must be before 'provider' argument if required)
 -provider val       Provider to load (can be specified multiple times)
 -propquery val      Property query used when fetching algorithms
```

</details>

#### `openssl sm4-cfb`

**帮助命令**：`openssl sm4-cfb -help`。**用法**：`Usage: sm4-cfb [options]`

**解读**：这是固定密码名称 `sm4-cfb` 的 `enc` 入口；`-e`/`-d` 控制文件加解密，密钥或口令、IV、输入输出必须按 [`enc`](#openssl-enc) 说明固定。帮助可见不等于本项目允许该算法或模式。

<details><summary>展开本机 `-help` 内容</summary>

```text
Usage: sm4-cfb [options]

General options:
 -help               Display this summary
 -list               List ciphers
 -ciphers            Alias for -list
 -e                  Encrypt
 -d                  Decrypt
 -p                  Print the iv/key
 -P                  Print the iv/key and exit
 -engine val         Use engine, possibly a hardware device

Input options:
 -in infile          Input file
 -k val              Passphrase
 -kfile infile       Read passphrase from file

Output options:
 -out outfile        Output file
 -pass val           Passphrase source
 -v                  Verbose output
 -a                  Base64 encode/decode, depending on encryption flag
 -base64             Same as option -a
 -A                  Used with -[base64|a] to specify base64 buffer as a single line

Encryption options:
 -nopad              Disable standard block padding
 -salt               Use salt in the KDF (default)
 -nosalt             Do not use salt in the KDF
 -debug              Print debug info
 -bufsize val        Buffer size
 -K val              Raw key, in hex
 -S val              Salt, in hex
 -iv val             IV in hex
 -md val             Use specified digest to create a key from the passphrase
 -iter +int          Specify the iteration count and force use of PBKDF2
 -pbkdf2             Use password-based key derivation function 2
 -none               Don't encrypt
 -*                  Any supported cipher

Random state options:
 -rand val           Load the given file(s) into the random number generator
 -writerand outfile  Write random data to the specified file

Provider options:
 -provider-path val  Provider load path (must be before 'provider' argument if required)
 -provider val       Provider to load (can be specified multiple times)
 -propquery val      Property query used when fetching algorithms
```

</details>

#### `openssl sm4-ctr`

**帮助命令**：`openssl sm4-ctr -help`。**用法**：`Usage: sm4-ctr [options]`

**解读**：这是固定密码名称 `sm4-ctr` 的 `enc` 入口；`-e`/`-d` 控制文件加解密，密钥或口令、IV、输入输出必须按 [`enc`](#openssl-enc) 说明固定。帮助可见不等于本项目允许该算法或模式。

<details><summary>展开本机 `-help` 内容</summary>

```text
Usage: sm4-ctr [options]

General options:
 -help               Display this summary
 -list               List ciphers
 -ciphers            Alias for -list
 -e                  Encrypt
 -d                  Decrypt
 -p                  Print the iv/key
 -P                  Print the iv/key and exit
 -engine val         Use engine, possibly a hardware device

Input options:
 -in infile          Input file
 -k val              Passphrase
 -kfile infile       Read passphrase from file

Output options:
 -out outfile        Output file
 -pass val           Passphrase source
 -v                  Verbose output
 -a                  Base64 encode/decode, depending on encryption flag
 -base64             Same as option -a
 -A                  Used with -[base64|a] to specify base64 buffer as a single line

Encryption options:
 -nopad              Disable standard block padding
 -salt               Use salt in the KDF (default)
 -nosalt             Do not use salt in the KDF
 -debug              Print debug info
 -bufsize val        Buffer size
 -K val              Raw key, in hex
 -S val              Salt, in hex
 -iv val             IV in hex
 -md val             Use specified digest to create a key from the passphrase
 -iter +int          Specify the iteration count and force use of PBKDF2
 -pbkdf2             Use password-based key derivation function 2
 -none               Don't encrypt
 -*                  Any supported cipher

Random state options:
 -rand val           Load the given file(s) into the random number generator
 -writerand outfile  Write random data to the specified file

Provider options:
 -provider-path val  Provider load path (must be before 'provider' argument if required)
 -provider val       Provider to load (can be specified multiple times)
 -propquery val      Property query used when fetching algorithms
```

</details>

#### `openssl sm4-ecb`

**帮助命令**：`openssl sm4-ecb -help`。**用法**：`Usage: sm4-ecb [options]`

**解读**：这是固定密码名称 `sm4-ecb` 的 `enc` 入口；`-e`/`-d` 控制文件加解密，密钥或口令、IV、输入输出必须按 [`enc`](#openssl-enc) 说明固定。帮助可见不等于本项目允许该算法或模式。

<details><summary>展开本机 `-help` 内容</summary>

```text
Usage: sm4-ecb [options]

General options:
 -help               Display this summary
 -list               List ciphers
 -ciphers            Alias for -list
 -e                  Encrypt
 -d                  Decrypt
 -p                  Print the iv/key
 -P                  Print the iv/key and exit
 -engine val         Use engine, possibly a hardware device

Input options:
 -in infile          Input file
 -k val              Passphrase
 -kfile infile       Read passphrase from file

Output options:
 -out outfile        Output file
 -pass val           Passphrase source
 -v                  Verbose output
 -a                  Base64 encode/decode, depending on encryption flag
 -base64             Same as option -a
 -A                  Used with -[base64|a] to specify base64 buffer as a single line

Encryption options:
 -nopad              Disable standard block padding
 -salt               Use salt in the KDF (default)
 -nosalt             Do not use salt in the KDF
 -debug              Print debug info
 -bufsize val        Buffer size
 -K val              Raw key, in hex
 -S val              Salt, in hex
 -iv val             IV in hex
 -md val             Use specified digest to create a key from the passphrase
 -iter +int          Specify the iteration count and force use of PBKDF2
 -pbkdf2             Use password-based key derivation function 2
 -none               Don't encrypt
 -*                  Any supported cipher

Random state options:
 -rand val           Load the given file(s) into the random number generator
 -writerand outfile  Write random data to the specified file

Provider options:
 -provider-path val  Provider load path (must be before 'provider' argument if required)
 -provider val       Provider to load (can be specified multiple times)
 -propquery val      Property query used when fetching algorithms
```

</details>

#### `openssl sm4-ofb`

**帮助命令**：`openssl sm4-ofb -help`。**用法**：`Usage: sm4-ofb [options]`

**解读**：这是固定密码名称 `sm4-ofb` 的 `enc` 入口；`-e`/`-d` 控制文件加解密，密钥或口令、IV、输入输出必须按 [`enc`](#openssl-enc) 说明固定。帮助可见不等于本项目允许该算法或模式。

<details><summary>展开本机 `-help` 内容</summary>

```text
Usage: sm4-ofb [options]

General options:
 -help               Display this summary
 -list               List ciphers
 -ciphers            Alias for -list
 -e                  Encrypt
 -d                  Decrypt
 -p                  Print the iv/key
 -P                  Print the iv/key and exit
 -engine val         Use engine, possibly a hardware device

Input options:
 -in infile          Input file
 -k val              Passphrase
 -kfile infile       Read passphrase from file

Output options:
 -out outfile        Output file
 -pass val           Passphrase source
 -v                  Verbose output
 -a                  Base64 encode/decode, depending on encryption flag
 -base64             Same as option -a
 -A                  Used with -[base64|a] to specify base64 buffer as a single line

Encryption options:
 -nopad              Disable standard block padding
 -salt               Use salt in the KDF (default)
 -nosalt             Do not use salt in the KDF
 -debug              Print debug info
 -bufsize val        Buffer size
 -K val              Raw key, in hex
 -S val              Salt, in hex
 -iv val             IV in hex
 -md val             Use specified digest to create a key from the passphrase
 -iter +int          Specify the iteration count and force use of PBKDF2
 -pbkdf2             Use password-based key derivation function 2
 -none               Don't encrypt
 -*                  Any supported cipher

Random state options:
 -rand val           Load the given file(s) into the random number generator
 -writerand outfile  Write random data to the specified file

Provider options:
 -provider-path val  Provider load path (must be before 'provider' argument if required)
 -provider val       Provider to load (can be specified multiple times)
 -propquery val      Property query used when fetching algorithms
```

</details>

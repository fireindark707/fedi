# fedi

## 要求

- Flask
- dynaconf
- cryptography
- requests

## 使用说明

1. 请先按照说明修改settings-example.toml
2. 生成私钥与公钥，使用http_utils.RSAKeyPairGenerator，例如：from http_utils import RSAKeyPairGenerator; key_generator = RSAKeyPairGenerator(); key_generator.run();
3. 启动服务器bash run.sh，访问 localhost:5000/users/<user_name> (user_name需与settings.toml中一致)，确认运作正常
4. 域名配置（略）
5. 配置nginx等反向代理，类似3测试能否访问用户资料
6. 编辑test内的follow、create等测试脚本，填入相应内容后，运行 python -m test.脚本名

## Installation

Install the package in editable mode
```
pip install -e .
```

Install the pre-commit
```
pre-commit install
```

Run the pre-commit for all files
```
pre-commit run --all-files
```


## config.yml example
```
Platform:
  general:
    configuration:

    log:
      level: INFO
      format: "<green>{time}</green> {level} | {message}"
      colorize: true
      remove_stderr: false

  environments:
    web:
      browser: Chrome
      host: http://localhost/
      email: admin@protectimus.com
      password: secret
    api:
      api_url: http://api.localhost/
      api_login: admin@protectimus.com
      api_key: secret
      password: =S3cREt_P@sSW0rd=

  postgres:
    host: localhost
    database: protectimus
    user: postgres
    password: postgres
    connector: postgresql
    dump_path: "/some/path/dump_file"

  mailhog:
    host: http://localhost:8025/
```

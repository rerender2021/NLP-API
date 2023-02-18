<p align="center">
    <img width="450" src="./docs/logo.svg">
</p>

<div align="center">
</div>
 
# Introduction

This is a NLP API server.

# Usage

- Download it from [release](https://github.com/rerender2021/NLP-API/releases)

- Unzip it, and click `run.bat`

![run-from-cmd](./docs/run-from-cmd.png)

# API

- Default host: `http://localhost:8100`
  
## POST /translate

- Description: offline translation
- Example:

![api-translate](./docs/api-translate.png)

# Dev

- Install

```bash
> virtualenv venv --python=python3.8.10
> pip install -r requirements.txt
```

- Download model

```bash
> python ./script/download.py
```

Then, adjust `model` folder structure like this:

```
- ...
- model
    - opus-mt-en-zh
- ...
- README.md
```

- Run

```bash
> python ./src/main.py
```

# Package

```bash
> build
```

# License

[MIT](./LICENSE)

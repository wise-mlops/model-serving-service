# Python FastAPI Template

[![PythonVersion](https://img.shields.io/badge/python-3.9.13-blue)](https://www.python.org/downloads/release/python-3913/)
[![FastAPIVersion](https://img.shields.io/badge/fastapi-0.110.0-yellowgreen)](https://fastapi.tiangolo.com/release-notes/#01110)
[![loguru](https://img.shields.io/badge/loguru-0.7.2-orange)](https://loguru.readthedocs.io/en/stable/project/changelog.html)

## AI플랫폼팀 전용 FastAPI 개발 템플릿 

> API 명세는 와이즈넛 [Restful API 디자인 가이드](https://docs.google.com/document/d/1tSniwfrVaTIaTT4MxhBRAmv-S_ECcoSFAXlYrsg4K0Y/edit#heading=h.60fu2rc04bck)를 따른다.

Python FastAPI Template 은 아래와 같은 특징을 갖고 있다.
1. Python 3.9: 높은 호환성
   > 다른 파이썬 버전도 호환이 가능하나 완벽히 테스트되지 않은 상태
2. MSA 구조에 적합한 FastAPI 템플릿
3. 의존성: Poetry (`pyproject.toml`으로 한 번에 관리)
4. 환경 변수를 통한 전체적인 프로젝트 변수를 간단하게 관리
5. 도커 환경 구성 (개발 및 배포용 Dockerfile 구성)
6. Gunicorn으로 multi process 환경 구성
7. 내부망 환경 구성
8. gitlab-ci로 _build, unit test (pytest), lint test (ruff, mypy, pyright), deploy_ 수행

## Getting started

### 1. Create Project
> 총 3가지 방법이 존재함 (**Create from template** 방법의 경우, GitLab 프로젝트 이동으로 인해 사용불가)
1. **Create blank project**
   1. GitLab `Create new project` 을 통해 새로운 프로젝트 생성
   2. _Project name, Project description (optional)_ 등을 작성하고 `Create project` 선택
   3. Python FastAPI Template을 Download source code (zip, tar.gz, tar.bz2, tar)를 통해 받아서 Push
2. **Create project using fork**
   1. `Create new Fork` or `Fork`를 통해서 새로운 프로젝트 생성
   2. _Project name, Project description (optional)_ 등을 작성하고 `Fork Project` 선택
   3. 프로젝트 생성 후 Fork 해제    
      Fork를 해제하지 않으면 새로 생성한 프로젝트의 MR이 Python FastAPI Template에 올라오거나 Issue를 통해 Create merge request 불가
3. **_(Deprecated) Create from template_**
   1. GitLab `Create new project` 을 통해 새로운 프로젝트 생성
   2. `Create from template` 선택
   3. `Group` 선택
   4. Python FastAPI Template 에서 `Use template` 선택
   5. _Project name, Project description (optional)_ 등을 작성하고 `Create project` 선택

> 🔴 **gitlab-ci Container Registry Deploy**를 위해 프로젝트 생성시 무조건 `Settings > Repository > Deploy tokens`에 **gitlab+deploy-token** 이름으로 토큰 생성하기

### 2. Development Environment Setting
1. 로컬 개발 환경에 `git clone ...` 
2. Pycharm 을 열고 `open project ...`
3. Interpreter Setting
   - **Poetry**
     1. Poetry 설치 ([poetry docs](https://python-poetry.org/docs/#installation) 참고)
     2. **Add New Interpreter** 선택
     3. **Add Local Interpreter** 선택
     4. **Poetry Environment** 선택 
     5. Python version에 맞게 환경 설정 (현재는 3.9.13 사용중)
     6. **Install packages from pyproject.toml** 체크
        - `UnicodeError` 발생 할 경우, **Settings > Editor > Global Encoding, Project Encoding, Properties Files** 모두 'UTF-8' 로 설정 
        - 🐛 해결이 안 될 경우, 체크 표시 해제하고 poetry 가상환경 생성한 후 poetry venv 터미널에 `poetry install`로 직접 Installs the project dependencies
     7. **OK** 선택
     > 추가 의존성이 필요할 경우, `poetry add ${package-name-to-add}`로 추가하면 자동으로 `pyproject.toml` 파일에 의존성이 추가 (자세한 사항은 Poetry 공식 docs 확인)
   - _Virtualenv (deprecated)_
     1. **Add New Interpreter** 선택
     2. **Add Local Interpreter** 선택
     3. **Virtualenv Environment** 선택 
     4. 로컬에 설치된 Python 3.9 경로를 Base Interpreter 로 설정
     5. `pip install .` (`pyproject.toml`에 작성한 의존성 설치, 아래 **3. Extra Setting** 참고)

## 3. Extra Setting (Optional)
### `.env`
> 환경 변수로 앱 구동 및 관련 설정 진행
- `PORT`: fastapi server port
- `SERVICE_NAME`: 서비스명
- `SERVICE_CODE`: 서비스코드
- `MAJOR_VERSION`: API 메이저 버전
- `STATUS`: API 상태 (개발용: `dev`, 배포용: `prod`)
- 로그 관련 설정: [loguru](https://github.com/Delgan/loguru) 사용하여 로그 세팅
  - `LEVEL`: 로그 레벨 설정 
  - `JSON_LOG`: stdout 형식 JSON 출력 여부 결정 (로그 저장도 해당 형식으로 진행됨)
  - `LOGURU_FORMAT`: 로그 포맷팅 설정
    - loguru 라이브러리를 사용해서 환경변수로 설정이 가능하다.
    - 자세한 로그 포맷은 [loguru 공식 문서](https://loguru.readthedocs.io/en/stable/api/logger.html#record)에서 확인 바람
  - `SAVE`: 로그 파일 저장 여부
  - `LOG_SAVE_PATH`: 디렉토리명까지 설정, (default = `YYYY/MM/*.log` 디렉토리 생성)
  - `ROTATION`: 매일 `mm:ss`시에 새로운 로그 파일 생성
  - `RETENTION`: 설정한 시간 이후에 제거 (ex. "1 month 2 weeks", "10h")
  - `COMPRESSION`: 압축 형식 ("gz", "bz2", "xz", "lzma", "tar", "tar.gz", "tar.bz2", "tar.xz", "zip" 등의 형식 지원)
    > `ROTATION`, `RETENTION`, `COMPRESSION`, `LOGURU_FORMAT` 모두 loguru에 있는 파라미터로 자세한 파라미터 정보는 [공식 문서](https://loguru.readthedocs.io/en/stable/api/logger.html#file:~:text=See%20datetime.datetime-,The%20time%20formatting,-To%20use%20your) 확인
- 서비스 관련 설정
  - `X_TOKEN`: API 사용을 위한 토큰값 설정
### Docker run
- ❗ 도커 빌드 및 실행할 경우, `version.py` 실행 사전 작업 필수 ❗
  (없을 경우에도 정상작동 되지만 필요한 정보를 볼 수 없음)
  👉 `version_info.py` 정보 생성 과정
  ```python
  service: str = 'FastAPI Sample'
  version: str = 'v1.6a6b8b0'
  git_branch: str = '21-refectoring-intialize'
  git_revision: str = '6a6b8b01cffcb7519013317f052dd104e1c39e56'
  git_short_revision: str = '6a6b8b0'
  build_date: str = '2024-05-29 09:16:40'
  ```
- `pyproject.toml` 작성 (참고: [Declaring project metadata](https://packaging.python.org/en/latest/specifications/declaring-project-metadata/))
   - project 메타데이터 작성 (_name_, _version_, ... etc)
   - 의존성 작성: _dependencies_
   - 개발 의존성 작성: _project.optional-dependencies_


### 4. Run
- local run
  - `$HOME/main.py`
    - `FileNotFoundError` or `ImportError` 발생시 _Working Directory_ (Working Directory = `$HOME`) 확인하기
  - _http :8000/openapi.json_ or _http://localhost:8000/docs_ 로 API 명세 확인 및 테스트
- docker run    
  `docker build ...` && `docker run -d -p ...` 로 컨테이너 빌드 & 구동
  ```shell
  # 도커 이미지 빌드
  docker build -t python-fastapi-template:0.1.5-dev -f Dockerfile .
  # 컨테이너 구동
  docker run -d --name python-fastapi-template -p 8000:8000 -e DEFAULT_X_TOKEN=fake-super-secret-token -e DEFAULT_TOKEN=default-token python-fastapi-template:0.1.5-dev
  ```

## 📚 MSA
> @tiangolo(FastAPI 개발자)가 제공하는 유형(ex. api, crud, 모델, 스키마)별로 파일을 구분하는 프로젝트 구조
- 출처: https://fastapi.tiangolo.com/tutorial/bigger-applications/
```
.
├── app                  # "app" is a Python package
│   ├── __init__.py      # 
│   ├── main.py          # 
│   ├── dependencies.py  # 
│   ├── exceptions.py  # custom exception
│   ├── models.py  # 
│   ├── schemas.py  # 데이터베이스를 사용할 경우
│   ├── database.py  # 데이터베이스를 사용할 경우
│   ├── crud.py  # 데이터베이스를 사용할 경우
│   └── routers          # (API Endpoints) "routers" is a "Python subpackage" 
│   │   ├── __init__.py  # 
│   │   ├── items.py     # 
│   │   └── users.py     # 
│   └── internal         # 
│       ├── __init__.py  # 
│       └── admin.py     # 
│   └── src         # (Main Functions) "src" is a "Python subpackage"
│       ├── __init__.py  # 
├── tests                  # app directory architecture 에 맞게 unit test 구성
│   ├── __init__.py      # 
│   └── routers          # 
│   │   ├── __init__.py  # 
│   │   ├── test_items.py     # 
│   │   └── test_users.py     # 
│   └── internal         # 
│       ├── __init__.py  # 
│       └── test_admin.py     # 
│   └── src         # 
│       ├── __init__.py  #
```

- **routers**: API Endpoint. 작성한 API들은 `$HOME/app/main.py`에 router를 추가한다. (ex. `app.include_router(users.router)`)
- **src**: 모듈 메인 기능
- unit test
  - 👉 유닛 테스트는 기본적으로 `$HOME/app`의 디렉토리 구조에 맞게 구성한다.
  - 유닛 테스트 종류로는 기능 테스트, API 엔드포인트 테스트, Pydantic 모델 유효성 테스트, 보안 테스트가 있다.
- **Dockerfile**
  - `Dockerfile`(=Dockerfile.dev 역할): 개발을 위해 필요한 도구 및 라이브러리와 같은 추가적인 종속성을 설치하기 위한 라이브러리들이 설치된 환경
  - `product.Dockerfile`: 최종 제품을 배포하기 위해 필요한 것들만 포함한 환경


# Guide for each environment
## Multi Process
> **Gunicorn 사용**    

### What is Gunicorn?
> Gunicorn의 프로세스는 프로세스 기반의 처리 방식을 채택하고 있으며, 이는 내부적으로 크게 master process와 worker process로 나뉘어 집니다.
> Gunicorn이 실행되면, 그 프로세스 자체가 master process이며, fork를 사용하여 설정에 부여된 worker 수대로 worker process가 생성 됩니다. 
> master process는 worker process를 관리하는 역할을 하고, worker process는 웹어플리케이션을 임포트하며, 요청을 받아 웹어플리케이션 코드로 전달하여 처리하도록 하는 역할을 합니다.

- Gunicorn 적용
  - Before: FastAPI 단독 실행 (Uvicorn 서버로 실행) = 1 process 로 TA 모듈 서버 구동
  - After: Gunicorn으로 FastAPI 다중 실행 (n*worker) = n+1 process (= 1*master + n*worker) 로 TA 모듈 서버 구동

### How to use Gunicorn
```shell
# 의존성 설치
(venv) pip install --extra-index-url https://download.pytorch.org/whl/cpu .[gunicorn]
# 실행
gunicorn --bind 0:8000 --max-requests 20 -w 4 -k uvicorn.workers.UvicornWorker app.main:app
```
- Gunicorn 설정 참고
  - 기본 옵션 설명
    - `-w ${num_of_worker}`: request 를 처리할 app 을 지정된 워커 수 만큼 생성 미지정시 1
    - `--bind 0:8000`: `host:port` 형태로 바인딩할 소켓을 지정. 미지정시 `['127.0.0.1:8000']`
    - `-k uvicorn.workers.UvicornWorker`: fastapi 구동을 위한 설정이므로 워커 클래스는 `uvicorn`으로 고정해서 사용
    - `--max-requests 1000`: 각 워커에 해당 설정값 이상으로 요청이 몰릴 경우 다시 시작하여 메모리 누수 방지
    - 자세한 설정 옵션은 [Gunicorn 공식 문서 Settings](https://docs.gunicorn.org/en/stable/settings.html) 참고
  - 커맨드로 옵션을 설정할 수 있지만 편리성을 위해 Gunicorn 설정파일인 `gunicorn.conf.py`에서 진행한다.
    - Configuration File은 `./gunicorn.conf.py`가 디폴트로 설정되어있고, 다른 경로를 설정하고 싶은 경우, `-c CONFIG` or `--config CONFIG`로 설정한다.
    - 자세한 사용법은 하단 링크 참고
      - https://github.com/benoitc/gunicorn/blob/master/examples/example_config.py
      - https://zetawiki.com/wiki/Gunicorn.conf.py
- 주의사항
  - 요청이 올 수 있는 수준으로 최적값으로 설정하여 필요 이상으로 설정할 경우 OOM 발생
  - 공식문서를 참고하여 사용 환경에 맞는 설정 필요

## MSA: 내부망
### 배포 가이드
1. `pyproject.toml` 작성 (참고: [Declaring project metadata](https://packaging.python.org/en/latest/specifications/declaring-project-metadata/))
   - project 메타데이터 작성 (_name_, _version_, ... etc)
   - 의존성 작성: _dependencies_
   - 개발 의존성 작성: _project.optional-dependencies_
2. 패키지 whl 파일 내려받기
   1. 내부망과 동일한 운영체제, 아키텍처, 파이썬 버전으로 `pip download $HOME[pyproject.toml이 위치한 경로] --dest [다운로드 받은 wheel파일 경로]` 진행
       - (ex) `pip download . --dest .\pypi\package\`
   2. 파이썬 모듈 내부에 아래와 같은 구조로 준비 완료

### 실행가이드
1. 가상 환경 구성 및 진입
   1. 가상 환경 구성: `python -m venv venv`
   2. 가상 환경 진입: `.\venv\Scripts\activate` or `source .venv/bin/activate`
2. 의존성 설치: `pip install $HOME[pyproject.toml이 위치한 경로] --no-index --find-links [wheel 파일 경로]`
   - (ex) `pip install . --no-index --find-links $HOME\pypi\package\*.whl`
3. `python app/main.py` 실행


# 📚 참고 사항 📚   
- 해당 템플릿은 크게 **msa**와 **monlith** 두 가지로 나뉜다. (@TODO: monolith)
- Default는 **msa**(`$HOME/app`)로 해당 템플릿을 그대로 사용하면 된다.
- TODO
    > @tiangolo 가 제공하는 유형(예: api, crud, 모델, 스키마)별로 파일을 구분하는 프로젝트 구조는 범위가 적은 마이크로 서비스 또는 프로젝트에 적합하지만 많은 도메인이 있는 모놀리식에는 맞출 수 없다.
    > 더 확장 가능하고 진화할 수 있는 구조는 Netflix의 Dispatch 에서 영감을 얻었다.
  - 출처: https://github.com/zhanymkanov/fastapi-best-practices
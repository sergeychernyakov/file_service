# file_service

## Test task

Нужно написать минимальный HTTP веб-сервис, который будет реализовывать прием файлов. Сервис должен уметь принимать файлы, складывать в хранилище (на ваш выбор), иметь возможность отдать список имеющихся файлов, возможность скачать загруженные ранее файлы и иметь хелзчек (критерий – на ваше усмотрение). Размер файлов – не больше 1 МиБ. Сервис должен иметь возможность конфигурирования (порт, параметры хранилища и т.д.), например json файл. Сервис должен журналировать все операции пользователя в лог. Сервис должен иметь возможность авторизовать пользователя (тип авторизации на ваше усмотрение, но чтобы можно было использовать curl). Покрыть сервис юнит тестами. Сервис должен работать, используя Python 3.5 на Linux и использовать минимум сторонних пакетов (веб-фреймворк на ваше усмотрение). Установка и запуск минимальным количеством ручных операций. Необходима инструкция по запуску.

Пользовательские сценарии:
- Пользователь через curl отправляет файл на этот веб-сервис.
- Пользователь через curl может получить список файлов (имя, размер, дата записи).
- Пользователь может скачать необходимый файл с помощью HTTP GET запроса.

## Requirements

- Python 3.5
- Flask==3.0.3

## Setup
To set up the app locally, follow these steps:

1. Clone the repository to your local machine:
    ```sh
    git clone https://github.com/your-username/file_service.git
    ```

2. Create a virtual environment:
    ```sh
    python3 -m venv venv
    ```

3. Activate the virtual environment:
    ```sh
    source venv/bin/activate
    ```

4. Install the required dependencies:
    ```sh
    pip install -r requirements.txt
    ```

### File structure

file_service/
│
├── README.md            # Project description and instructions for setup and usage
├── config.py            # Configuration file containing project settings
├── requirements.txt     # List of dependencies required for the project
├── test_task_demo.mov   # Demo video for the test task (assumed)
├── wsgi.py              # File for running the project via a WSGI-compatible server
├── app.py               # Main application file containing the application logic
├── storage/             # Directory for storing files processed by the service
└── tests/               # Directory for unit and integration tests
    ├── test_app.py      # Tests for checking the functionality of the main application

### Configuration

1. Create a `.env` file by copying the example file:
    ```sh
    cp .env.example .env
    ```

2. Update the `.env` file with your desired configuration:
    ```env
      PORT=5002
      STORAGE_PATH='./storage'
      MAX_FILE_SIZE=1048576
      USERNAME='admin'
      PASSWORD='password'
    ```

### Running the App

To run the application, execute:
```sh
flask run --port 5002
```

### Usage

#### Upload a File

To upload a file, use the following `curl` command:
```sh
curl -u admin:password -F "file=@img.jpg" http://localhost:5002/upload
```

#### List Files

To get a list of uploaded files, use the following `curl` command:
```sh
curl -u admin:password http://localhost:5002/files
```

#### Download a File

To download a file, use the following `curl` command:
```sh
curl -u admin:password -O http://localhost:5002/files/c5f7e558180f4c2998c92614e0ed5776.jpg
```

#### Health Check

To check the health of the service, use the following `curl` command:
```sh
curl http://localhost:5002/health
```

### Running Tests

To run the unit tests, execute:
```sh
python -m unittest discover -s tests
```

### Author
Sergey Chernyakov
```

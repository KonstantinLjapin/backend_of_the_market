# market_backend

### Технологии
- python3.12
- FASTAPI 
- poetry 
- Ruff 
### Используемые API


### Задача
- Выполнить бекенд проекта
- ROAD MAP 
- деплой CI/CD
- Выбор лицензии распостронения 


### Запуск проекта
- git clone {project url}
#### быстрый старт докер
  + #####  sudo chmod +x start_test_Mtv288.sh 
  + #####  ./start_test.sh запустит скрит докер компосе по завершению очистит
- * ###### http://127.0.0.1:8080/ping проверка
#### для разработчиков
  + #####  poetry env use python3.12 создаст виртуальное окружение
  + #####  poetry install
## Холодный старт
- poetry init -n --python "^3.12"
- poetry config virtualenvs.in-project true
- poetry env use python3.12 создаст виртуальное окружение
- mkdir src
- poetry install --no-root

## Установка требует
  * python3.12
    * poetry
        * ##### Linux/macOS
        - *      curl -sSL https://install.python-poetry.org | python3 -
        * ##### Windows (PowerShell)
        - *     (Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | py -
        * ### Oсновные команды poetry
          #### Активировать окружение
          - poetry shell
          #### Добавить новую зависимость
          - poetry add package-name
          #### Обновить зависимости
          - poetry update
          #### Запустить приложение
          - poetry run python src/main.py 
          #### Проверить и исправить код
          -  poetry run ruff check . --fix

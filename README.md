# Telegram бот для поиска дешевых авиабилетов

Этот бот помогает найти самые дешевые авиабилеты для ваших путешествий через сервис Aviasales не выходя из Telegram.

**Использование**
Найдите бота в Telegram по названию @myBot20042251_bot
Нажмите кнопку "Start" или введите команду "/start".
Бот имеет несколько функций:

- 1команда - start. Подскажет как пользоваться ботом


- 2 команда - поиск билета из точки А в точку Б. есть выбор: 
  - с точной датой
  - в определённом отрезке времени на пример с 01.05.2023 до 10.05.2023. 
  - без точной даты. бот присылает 5-10 вариантов самых дешевых билетов на любые даты в разрезе 6 месяцев на пример.


- 3 команда - команда для любителей спонтанно перемещаться. 
  - Поиск билетов не важно куда, но с указываем город вылета.


- 4 команда - история. Покажет вашу историю просмотров 


- 5 команда - help. Подскажет какие команды есть у бота.
  

**Установка**
Чтобы установить этого бота на свой сервер, выполните следующие шаги:

1. Клонируйте репозиторий с помощью команды git clone https://gitlab.skillbox.ru/veniamin_alekseev/python_basic_diploma.git.
2. Переходим в папку с загруженной программой, открываем терминал.
3. Устанавливает виртуальное окружение командой python3 -m venv venv
На OS Windows python -m venv venv
4. Активируем ВО source venv/bin/activate
На OS Windows venv\Scripts\activate
5. Устанавливаем зависимости pip install -r requirements.txt
6. Переименуйте файл .env.template в .env 
7. Вставьте ваши токеты Telegram и Aviasales.

Запустить бота можно IDE или из терминала, набрав команду python3 main.py на OS Windows python main.py
 вас есть какие-либо вопросы или предложения по улучшению бота, свяжитесь со мной по адресу email@example.com. Буду рад получить ваше сообщение!
Здраствуйте.

Запуск бота выполняеться через main.py.

Что бы запустить бота:

    1) Создайте в корне проекта файл ".env"
    2) Напишите константу BOT_TOKEN и запишите в нее токен бота
    !!!Пример лежит в файле ".env_template"!!!

В keyboard_for_bot.py содержиться вся клавиатура котороый пользуется бот.

В work_a_data_base.py есть три(3) функции которые отвечают за работу с БД

Рассмотрим пакет handlers: он содержит:

	-main_commands_bot.py :
		в нем основные команды бота : [/start, /help, /high, /low, /custom, /cancel]
            -message_custom : здесь текстовые обработчики для custom

	-пакет callback : 
		-custom.py : пустой Pytnon файл
		-high.py : все CallbackQuery относящиеся к команде /high и к FSMState High 
		-low.py : все CallbackQuery относящиеся к команде /low и к FSMState Low
		-custom.py : все CallbackQuery Относящиеся к команде /custom и к FSMState Custom

Рассмотрим пакет all_class: он содержит:

	-factory_callback.py : Фабрика CallbackData для клавиатуры и регистрации callback_qury_handler, что бы ловить клавиатуру
	-fsm_class.py : Здесь все классы FSM состояния для бота : [High, Low, Custom]

Рассмотрим пакет api_requests: он содержит:

	-check_photo.py : Проверяются  фотографии по размерам и подготавливаются для отправки ботом
	-handler_info_text.py : Подготавливаеться текст который будет отправлять бот
	-requests_for_high_and_low.py : Выполняется запрос к API и вытаскивается нужная информация для дальнейшей работы с текстом и фотографиями
    -requests_for_custom.py : Выполняется запрос к API И вытаскивается нужная информация для дальнейшей работы с текстом и фотографиями

В файле requirements.txt находится весь список зависимостей для этого Бота
Здраствуйте.

Токен бота надо записать в create_bot.py.

Запуск бота выполняеться через main.py.

В keyboard_for_bot.py содержиться вся клавиатура котороый пользуется бот.

Рассмотрим пакет handlers: он содержит:

	-main_commands_bot.py :
		в нем основные команды бота : [/start, /help, /high, /low, /cancel]

	-пакет callback : 
		-custom.py : пустой Pytnon файл
		-high.py : все CallbackQuery относящиеся к команде /high и к FSMState High 
		-low.py : все CallbackQuery относящиеся к команде /low и к FSMState Low
		
Рассмотрим пакет all_class: он содержит:

	-factory_callback.py : Фабрика CallbackData для клавиатуры и регистрации callback_qury_handler, что бы ловить клавиатуру
	-fsm_class.py : Здесь все классы FSM состояния для бота : [High, Low]

Рассмотрим пакет api_requests: он содержит:

	-check_photo.py : Проверяются  фотографии по размерам и подготавливаются для отправки ботом
	-handler_info_text.py : Подготавливаеться текст который будет отправлять бот
	-requests_for_high_and_low.py : Выполняеться запрос к API и вытаскиваеться нужная информация для дальнейшей работы с текстом и фотографиями

В файле requirements.txt находится весь список зависимостей для этого Бота
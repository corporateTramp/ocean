К установке:
	1. Pip
		Установка на linux-x86_64 Ubuntu
		--------------------------------
		sudo apt-get install python-pip
		
	2. Дополнительные модули
	   ---------------------------------
	   pip install requests html5lib beautifulsoup4
	   sudo apt-get install python-psycopg2

Работа с функциями Python 2.7 через командную строку на linux-x86_64 Ubuntu
		----------------------------------------------------------
		python -c "from instagram_parser import *; функция(аргументы)"
		например,
		python -c "from instagram_parser import *; start()"
	   
Функции:
	1. Работа с БД
		--------------------------------
		создать таблицы по заданной структуре:
			create_tables ([db_data="dbname=Localhosts user=postgres password =postgres"])
		удалить таблицы парсера: 
			delete_tables([db_data="dbname=Localhosts user=postgres password =postgres"])
		просмотр таблицы в командной строке (основные данные):
			see_table([table = "accounts", db_data="dbname=Localhosts user=postgres password =postgres"])
	
	2. Парсинг инстаграмма
		---------------------------------
		добавление/обновление данных* :
			start([link='http://www.t30p.ru/Instagram.aspx', wait = 10, db_data="dbname=Localhosts user=postgres password =postgres"])

* скрипт настроен на получение информации из базы (при обновлении) в кодировке "UTF-8", запись происходит в UNICODE

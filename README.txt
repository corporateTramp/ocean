К установке:
	1. PhantomJS
		Установка на linux-x86_64 Ubuntu
		--------------------------------
		wget https://storage.googleapis.com/google-code-archive-downloads/v2/code.google.com/phantomjs/phantomjs-1.9.2-linux-x86_64.tar.bz2
		tar xf phantomjs-1.9.2-linux-x86_64.tar.bz2
		rm phantomjs-1.9.2-linux-x86_64.tar.bz2
		mv phantomjs-1.9.2-linux-x86_64/ phantomjs
	
	2. Pip
		Установка на linux-x86_64 Ubuntu
		--------------------------------
		sudo apt-get install python-pip
		
	3. Дополнительные модули
	   ---------------------------------
	   pip install requests html5lib bs4
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

Дополнительно
	pgrep phantomjs | xargs kill
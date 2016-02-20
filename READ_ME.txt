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
		
	3. Дополнительные батарейки
	   pip install ...
	   ---------------------------------
	   pip install selenium requests html5lib bs4 psycopg2

Работа с функциями Python 2.7 через командную строку на linux-x86_64 Ubuntu
		----------------------------------------------------------
		python -c "from instagram_parser import *; функция(аргументы)"
	   
Функции:
	1. Работа с БД
		--------------------------------
		создать таблицы по заданной структуре:
			create_tables ([db_data="dbname=postgres user=postgres password =postgres"])
		удалить таблицы парсера: 
			delete_tables([db_data="dbname=postgres user=postgres password =postgres"])
		просмотр страницы в командной строке:
			see_table([table = "accounts", db_data="dbname=postgres user=postgres password =postgres"])
	
	2. Парсинг инстаграмма с 
		---------------------------------
		первый запуск:
			start([link='http://www.t30p.ru/Instagram.aspx', db_data="dbname=postgres user=postgres password =postgres"])
		добавление/обновление данных:
			update([link='http://www.t30p.ru/Instagram.aspx', db_data="dbname=postgres user=postgres password =postgres"])


Дополнительно:
	pgrep phantomjs | xargs kill
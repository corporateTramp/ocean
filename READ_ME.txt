� ���������:
	1. PhantomJS
		��������� �� linux-x86_64 Ubuntu
		--------------------------------
		wget https://storage.googleapis.com/google-code-archive-downloads/v2/code.google.com/phantomjs/phantomjs-1.9.2-linux-x86_64.tar.bz2
		tar xf phantomjs-1.9.2-linux-x86_64.tar.bz2
		rm phantomjs-1.9.2-linux-x86_64.tar.bz2
		mv phantomjs-1.9.2-linux-x86_64/ phantomjs
	
	2. Pip
		��������� �� linux-x86_64 Ubuntu
		--------------------------------
		sudo apt-get install python-pip
		
	3. �������������� ���������
	   pip install ...
	   ---------------------------------
	   pip install selenium requests html5lib bs4 psycopg2

������ � ��������� Python 2.7 ����� ��������� ������ �� linux-x86_64 Ubuntu
		----------------------------------------------------------
		python -c "from instagram_parser import *; �������(���������)"
	   
�������:
	1. ������ � ��
		--------------------------------
		������� ������� �� �������� ���������:
			create_tables ([db_data="dbname=postgres user=postgres password =postgres"])
		������� ������� �������: 
			delete_tables([db_data="dbname=postgres user=postgres password =postgres"])
		�������� �������� � ��������� ������:
			see_table([table = "accounts", db_data="dbname=postgres user=postgres password =postgres"])
	
	2. ������� ����������� � 
		---------------------------------
		������ ������:
			start([link='http://www.t30p.ru/Instagram.aspx', db_data="dbname=postgres user=postgres password =postgres"])
		����������/���������� ������:
			update([link='http://www.t30p.ru/Instagram.aspx', db_data="dbname=postgres user=postgres password =postgres"])


�������������:
	pgrep phantomjs | xargs kill
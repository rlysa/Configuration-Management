import pytest, tempfile, os
from config_parser import *


def test_parse_1():
    test_input = '''=begin
Server settings
=end
let serverName = [[ myserver ]]
let port = 8080
let enableHttps = [[ true ]]

let maxConnections = 100
=begin
Maximum number of connections
=end
let dbHost = [[ localhost ]]
let dbPort = 8080
let dbUser = [[ admin ]]
let dbPassword = [[ secret ]]'''

    config_parser = ConfigParser()
    config_parser.parse(test_input)
    xml_output = config_parser.to_xml()

    # Проверяем правильность парсинга
    assert xml_output == ('''<?xml version="1.0" encoding="utf-8"?>
<Configuration>
	<Constants>
		<Constant name="serverName">myserver</Constant>
		<Constant name="port">8080</Constant>
		<Constant name="enableHttps">true</Constant>
		<Constant name="maxConnections">100</Constant>
		<Constant name="dbHost">localhost</Constant>
		<Constant name="dbPort">8080</Constant>
		<Constant name="dbUser">admin</Constant>
		<Constant name="dbPassword">secret</Constant>
	</Constants>
</Configuration>
''')


def test_parse_2():
    test_input = '''=begin Параметры эксперимента =end
let experimentName = [[ Testing a new medicines ]]
let dosageMg = 50
let durationWeeks = 10

d = {
    dosageMg -> !(dosageMg 10 *).
    durationWeeks -> !(durationWeeks 2 +).
    outcomeVariable -> [[ reduction of symptoms ]].
}'''

    config_parser = ConfigParser()
    config_parser.parse(test_input)
    xml_output = config_parser.to_xml()

    assert xml_output == ('''<?xml version="1.0" encoding="utf-8"?>
<Configuration>
	<Constants>
		<Constant name="experimentName">Testing a new medicines</Constant>
		<Constant name="dosageMg">50</Constant>
		<Constant name="durationWeeks">10</Constant>
	</Constants>
	<Dictionaries>
		<Dictionary>
			<Item key="dosageMg">500.0</Item>
			<Item key="durationWeeks">12.0</Item>
			<Item key="outcomeVariable">reduction of symptoms</Item>
		</Dictionary>
	</Dictionaries>
</Configuration>
''')


def test_parse_3():
    test_input = '''d1 = {
    projectName -> [[ Development ]].
    projectManager -> [[ Ivanov ]].
}

d2 = {
    projectName -> [[ Testing ]].
    projectManager -> [[ Smirnov ]].
}

d3 = {
    projectName -> [[ Implementation ]].
    projectManager -> [[ Petrov ]].
}
'''

    config_parser = ConfigParser()
    config_parser.parse(test_input)
    xml_output = config_parser.to_xml()

    assert xml_output == ('''<?xml version="1.0" encoding="utf-8"?>
<Configuration>
	<Dictionaries>
		<Dictionary>
			<Item key="projectName">Development</Item>
			<Item key="projectManager">Ivanov</Item>
		</Dictionary>
		<Dictionary>
			<Item key="projectName">Testing</Item>
			<Item key="projectManager">Smirnov</Item>
		</Dictionary>
		<Dictionary>
			<Item key="projectName">Implementation</Item>
			<Item key="projectManager">Petrov</Item>
		</Dictionary>
	</Dictionaries>
</Configuration>
''')

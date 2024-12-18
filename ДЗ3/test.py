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
		<serverName>myserver</serverName>
		<port>8080</port>
		<enableHttps>true</enableHttps>
		<maxConnections>100</maxConnections>
		<dbHost>localhost</dbHost>
		<dbPort>8080</dbPort>
		<dbUser>admin</dbUser>
		<dbPassword>secret</dbPassword>
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
		<experimentName>Testing a new medicines</experimentName>
		<dosageMg>50</dosageMg>
		<durationWeeks>10</durationWeeks>
	</Constants>
	<Dictionaries>
		<d>
			<dosageMg>500.0</dosageMg>
			<durationWeeks>12.0</durationWeeks>
			<outcomeVariable>reduction of symptoms</outcomeVariable>
		</d>
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
		<d1>
			<projectName>Development</projectName>
			<projectManager>Ivanov</projectManager>
		</d1>
		<d2>
			<projectName>Testing</projectName>
			<projectManager>Smirnov</projectManager>
		</d2>
		<d3>
			<projectName>Implementation</projectName>
			<projectManager>Petrov</projectManager>
		</d3>
	</Dictionaries>
</Configuration>
''')

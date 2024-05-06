from os import system
import sys

csv = sys.argv[1]

template_start = '''create table if not exists `{table_name}` (
'''

tempalate_end = '''
)
ENGINE = InnoDB
DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci ;

'''

with open(csv) as f:
	schema = f.read().split('\n')

schema_details = dict()

for column in schema:
	if column == '':
		continue
	table_name = column.split(',')[0]
	column_name = column.split(',')[1]
	data_type = column.split(',')[2]

	if table_name in schema_details.keys():
		schema_details[table_name][column_name] = data_type
	else:
		schema_details[table_name] = dict({column_name: data_type})

schema_script = ''

for table in schema_details:
	schema_script += template_start.format(table_name=table)
	for column in schema_details[table]:
		schema_script += f'\t`{column}` {schema_details[table][column]},\n'

	schema_script = schema_script[:-2]
	schema_script += tempalate_end

file_name = f"{csv.split('.')[0]}.sql"
with open(file_name, 'w') as f:
	print(schema_script)
	print(schema_script, file=f)
	system(f'start notepad++ "{file_name}"')
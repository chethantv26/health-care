import sys
import json

from os import system

csv = sys.argv[1]

template_start = '''create table if not exists `{table_name}` (
'''

tempalate_end = '''
)
ENGINE = InnoDB
DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci ;

'''

primary_key = '''primary key (`{pk}`)'''

foreign_key = '''foreign key (`{col1}`) references `{tbl2}`(`{col2}`)'''

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
		if data_type.lower() == 'pk':
			schema_details[table_name]['Primary_Key'] = column_name
		elif data_type.lower() == 'fk':
			if 'Foreign_Key' in schema_details[table_name]:
				schema_details[table_name]['Foreign_Key'][column_name] = dict({column.split(',')[3]: column.split(',')[4]})
			else:
				schema_details[table_name]['Foreign_Key'] = dict({column_name: dict({column.split(',')[3]: column.split(',')[4]})})
		else:
			schema_details[table_name][column_name] = data_type
	else:
		if data_type.lower() == 'pk':
			schema_details[table_name] = dict({'Primary_Key': column_name})
		else:
			schema_details[table_name] = dict({column_name: data_type})

schema_script = ''

for table in schema_details:
	schema_script += template_start.format(table_name=table)
	for column in schema_details[table]:
		if column.lower() == 'primary_key':
			schema_script += '\t' + primary_key.format(pk=schema_details[table][column]) + ',\n'
			continue
		elif column.lower() == 'foreign_key':
			for fkey in schema_details[table][column].keys():
				col1 = fkey
				tbl2 = list(schema_details[table][column][fkey].keys())[0]
				col2 = list(schema_details[table][column][fkey].values())[0]
				schema_script += '\t' + foreign_key.format(col1=col1, tbl2=tbl2, col2=col2) + ',\n'
		else:
			schema_script += f'\t`{column}` {schema_details[table][column]},\n'

	schema_script = schema_script[:-2]
	schema_script += tempalate_end

json_object = json.dumps(schema_details, indent=4)

with open("schema.json", "w") as outfile:
	outfile.write(json_object)

file_name = f"{csv.split('.')[0]}.sql"

with open(file_name, 'w') as f:
	print(schema_script, file=f)

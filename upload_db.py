import pandas as pd
import os
import MySQLdb
import datetime
import re


data_path = ""
slide_creation_date = datetime.date.today().strftime("%m/%d/%Y")


DB_NAME = 'histoqc'
DB_IP = 'localhost'
DB_PORT = 3306
DB_USER = 'root'
DB_PASSWORD = 'histoqcweb'
DB_TABLE = 'file'

db = MySQLdb.connect(host=db_ip, port=db_port, user=db_user, passwd=db_password, db=db_name)
cursor = db.cursor()
db.set_character_set('utf8')


file_list = pd.read_csv('./histoqc_upload.txt', sep='\t', header=0)


db_command = "INSERT INTO file VALUES"

for i, row in file_list.iterrows():
        
    cur_file = row["filename"]
    attributes = []
    command = "("
    
    comments = row["comment"]
    result = re.search(r'Date = ([0-9]{2}/[0-9]{2}/)([0-9]{2})', comments)
    if result:
        cur_creation_date = result.group(1) + "20" + result.group(2)
    else:
        cur_creation_date = slide_creation_date
        
    attributes.append('%s%s' % (os.path.splitext(cur_file)[0], '.png'))
    attributes.append(cur_file)
    attributes.append(datetime.date.today().strftime("%m/%d/%Y"))
    attributes.append("axj232@case.edu")
    attributes.append("Breast")
    attributes.append(cur_creation_date)
    attributes.append(row["Magnification"])
    attributes.append(row["comments"])
    attributes.append("H&E")
    attributes.append(row["comment"])
    attributes.append(str(row["width"])+'x'+str(row["height"]))
    attributes.append(round(os.path.getsize(data_path + cur_file) / float(1024 * 1024 * 1024), 2))
    attributes.append(os.path.splitext(cur_file)[1])
    attributes.append("Aperio")
    attributes.append("FFPE")
    attributes.append("Resection")
    
    for j, attribute_val in enumerate(attributes):
        command += "'" + str(attribute_val) + "'"
        if j == len(attributes) - 1:
            command += ")"
        else:
            command += ","
    
    db_command += command
    if i == len(file_list) - 1:
        db_command += ";"
    else:
        db_command += ","


cursor.execute(db_command)
db.commit()

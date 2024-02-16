import psycopg2 as ps
import pandas as pd
import pathlib, os
from datetime import datetime
from dotenv import load_dotenv
from mailer import send_email

load_dotenv()


SMTP_CONFIG = {
    "smtp_host": os.getenv('HOST'),
    "smtp_user": os.getenv('USER'),
    "smtp_password": os.getenv('PASSWORD'),
    "smtp_port": os.getenv('PORT')
}

conn = ps.connect(
        dbname=os.getenv('DB'),
        user=os.getenv('UDB'),
        password=os.getenv('PDB'),
        host=os.getenv('HDB'),
        port=os.getenv('PDB'),
    )
with conn:
    with conn.cursor() as cursor:
        cursor.execute("SELECT \"FormJson\" FROM public.lk_orders WHERE \"IdProduct_id\" = 67")
        data = cursor.fetchall()
        form_data = []
        print(data)
        for row in data:
            print(row[0], end="\n")
            row_dict = {
                'ИНН' : row[0].get('inn1'),
                'Организация' : row[0].get('orgName'),
                'Имя' : row[0].get('name'),
                'Телефон' : row[0].get('phoneNumber'),
                'Дата' : datetime.now().strftime('%Y-%m-%d'),
                'Банк' : 'Сбер',
                'Источник' : 'Платформа'
                
            }
            form_data.append(row_dict)
        df = pd.DataFrame(form_data)
        df.to_excel(pathlib.Path(__file__).parent.joinpath('fromDB.xlsx'),index=False)
        send_email(
            smtp_config=SMTP_CONFIG,
            receiver_to='info@ate-vent.ru',
            message_subject='таблица',
            attachments=['fromDB.xlsx']
            
        )
        
    

print("Подключение установлено!")
conn.close()
# Банк - со значением “Сбер”
# Источник - со значением “Платформа”
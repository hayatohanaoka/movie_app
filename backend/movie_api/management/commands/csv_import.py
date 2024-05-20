import csv
import os
from pathlib import Path
from typing import Any
import sqlite3

from django.core.management import BaseCommand
from django.contrib import auth
from ...models import Comment, Movie, Role, Staff 

class Command(BaseCommand):

    def handle(self, *args: Any, **options: Any) -> str | None:
        """
        CSVデータをデータベースに移管する
        """
        csv_dir_path = os.path.join(Path(__file__).resolve().parent, 'csvs')

        # user -> movie -> comment の順で紐づくため、この順番でないとダメ
        models = (auth.get_user_model(), Movie, Comment, Role, Staff)
        files  = ('user.csv', 'movie.csv', 'comment.csv', 'role.csv', 'staff.csv')

        for file, model in zip(files, models):
            path = os.path.join(csv_dir_path, file)
            data = self._read_csv_file(path)
            self._insert_csv_data(model, data)
        
        # staffs と roles のブリッジテーブルへのデータインサート
        QUERY    = 'INSERT INTO tbl_staffs_roles (id, staff_id, role_id) VALUES (?,?,?)'
        csv_path = os.path.join(csv_dir_path, 'staff_roles.csv')
        data     = self._read_csv_file(csv_path, is_dict=False)
        for row in data[1:]:
            self._insert_bridge_table(QUERY, row)


    def _read_csv_file(self, file_path, is_dict: bool=True):
        with open(file_path, 'r', encoding='utf-8', newline='') as f:
            if is_dict:
                data = [row_dict for row_dict in csv.DictReader(f)]
            else:
                data = [row_dict for row_dict in csv.reader(f)]
        f.close()
        return data


    def _insert_csv_data(self, model, data: dict):
        insert_list = []
        for row in data:
            new = model(**row)
            if model == auth.get_user_model():
                new.set_password(raw_password='12345678')
            insert_list.append(new)
        model.objects.bulk_create(insert_list)


    def _insert_bridge_table(self, insert_query, insert_data):
        if insert_query.lower().startswith('INSERT'):
            raise ValueError('query is not start "insert"')
        
        db = sqlite3.connect('./db.sqlite3')
        cursor = db.cursor()
        cursor.execute(insert_query, insert_data)
        db.commit()
        cursor.close()

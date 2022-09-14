# Encode from pydantic model to ORM
# TODO: ORMとPydantic Modelの橋渡しコードを作成
# 基本的にはPydanticクラスを用い、DBとの操作が必要な場合のみORMクラスを作成する
"""
基本的な流れについて
1. main.py からリクエストを受け取り、class名は"~~In"とすること
2. データベースのCRUD処理が必要な場合は、Pydantic Modelを作成した後、
crud.py にORMモデルにして渡す。
Pydantic Model class名は"~~Model"とする。
ORM class名は"~~ORM"とすること。
3.　CRUD処理後が正常に終了した場合は取得データを元のPydantic Modelへ反映し、
レスポンスを返す。class名は"~~Out"とする。



"""
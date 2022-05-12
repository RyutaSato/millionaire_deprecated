## 仕様
## 1. Backend
    Language: Python(3.10.4)
    Web Application: FastAPI(0.75.1)


## Naming and Coding roles

### 1.ファイル名
    データベース処理ファイルはdb_???.pyとします
### 2.静的ファイル
    HTML, CSS, JPEG，PNG等はsrcフォルダーに入れます

## Development:
- ゲーム盤面
- DB操作プログラム

## Issue:
- プログラムの開始地点がmain.pyからである．
   - setup.pyからに変更する．
- postgresql_connect.pyのファイル名が冗長である
   - db_connect.pyに変更する．

## Resolved:
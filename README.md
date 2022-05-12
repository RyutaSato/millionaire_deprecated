## 仕様
## 1. Backend
    Language: Python(3.10.4)
    Web Application: FastAPI(0.75.1)

## 2. Label
### 

## Naming and Coding roles

### 1.ファイル名
* **db_???.py**: データベース関連ファイル
* 
### 2.静的ファイル
    HTML, CSS, JPEG，PNG等はsrcディレクトリに入れます
### 3.テストファイル
    テストファイルはtestディレクトリに入れます


## Development:
- ゲーム盤面
- DB操作プログラム

## Issue:
- プログラムの開始地点がmain.pyからである．
   - setup.pyからに変更する．
- postgresql_connect.pyのファイル名が冗長である
   - db_connect.pyに変更する．

## Resolved:
# Data to HTML
## 한국어 버전(korean version)

이 사이트는 MYSQL과 google sheet, xlsx, tsv등 다양한 데이터를 테이블로 변환해주는 사이트입니다.

### API
API링크는
- MySQL to HTML Table(post): https://data-to-html.onrender.com/sqlapi
- Google Sheets to HTML Table(post): https://data-to-html.onrender.com/sheetapi
이 있습니다
#### sqlapi
이 api는 sql테이블을 html 테이블로 바꿔주는 api입니다

##### 폼파라미터
- `host`: 데이터베이스 호스트 
- `database`: 데이터베이스 이름 
- `user`: 사용자 이름 
- `password`: 비밀번호
- `query`: 실행할 SQL 쿼리(select 쿼리문만 가능함)
- `port`: 데이터베이스 포트 번호 

##### 반환값(Json)
- `table`:해당 퀴리문의 결과 테이블 코드
#### sheetapi
이 api는 google sheet를 html 테이블로 바꿔주는 api입니다

##### 폼파라미터
- `url`: 구글 시트 url(해당 시트는 공개상태가 되야할것)

##### 반환값(Json)
- `table`:해당 시트의 테이블 코드
## English Version

This site converts various data types such as MySQL, Google Sheets, XLSX, TSV, etc., into HTML tables.

### API

API links are:
- MySQL to HTML Table(post): https://data-to-html.onrender.com/sqlapi
- Google Sheets to HTML Table(post): https://data-to-html.onrender.com/sheetapi

#### sqlapi
This API converts SQL tables to HTML tables.

##### Form Parameters
- `host`: Database host
- `database`: Database name
- `user`: Username
- `password`: Password
- `query`: SQL query (only SELECT queries are allowed)
- `port`: Database port number

##### Return Value (JSON)
- `table`: The HTML table code of the query result

#### sheetapi
This API converts Google Sheets to HTML tables.

##### Form Parameters
- `url`: Google Sheets URL (the sheet must be public)

##### Return Value (JSON)
- `table`: The HTML table code of the sheet

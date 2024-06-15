from fastapi import FastAPI,Form,Request,HTTPException,UploadFile,File
from fastapi.responses import FileResponse,JSONResponse,HTMLResponse
from fastapi.staticfiles import StaticFiles
from SQLConn import MYSQLConn
import re
from io import StringIO,BytesIO
import pandas as pd
import html
from fastapi.templating import Jinja2Templates
import markdown
import requests

app=FastAPI()
app.mount("/img",StaticFiles(directory="img"))
app.mount("/js",StaticFiles(directory="js"))
templates = Jinja2Templates(directory="templates")

def alert(request:Request, msg:str):
    return templates.TemplateResponse("arlert.html", {"request": request, "msg": msg})

def view(request:Request,title: str, table: str,kind:str,enkind:str=None,herf:str="/"):
    codearr=table.split("\n")
    rows=len(codearr)
    temp={"request": request, "title": title, "table": table,"rows":rows,"kind":kind,"herf":herf}
    temp['enkind']=enkind if enkind else kind
    return templates.TemplateResponse("view.html", temp)

@app.get("/")
def index():
    return FileResponse('index.html')
@app.get("/sqlupload")
def sqlupload():
    return FileResponse('sqlupload.html')
@app.get('/fileupload')
def sheetupload():
    return FileResponse('fileupload.html')
@app.get("/sheetupload")
def sheetupload():
    return FileResponse('sheetupload.html')
@app.get("/apidocs")
def apidocs():
    with open("README.md", "r", encoding="utf-8") as f:
        readme_content = f.read()
    html_content = markdown.markdown(readme_content)
    return HTMLResponse(html_content)
@app.post("/sql")
def sql(request:Request,host:str=Form(...),database:str=Form(...),user:str=Form(...),password:str=Form(...),query:str=Form(...),port:int=Form(...)):
    query=query.lower().replace('select*','select *')
    try:#호스트나 유저명 db명, 포트, 비밀번호, db명이 다르면
        conn=MYSQLConn(host=host,user=user,database=database,password=password,port=port)
    except Exception as e:
        return alert(request,f'DB정보를 다시 확인해주세요(check DB info):{html.unescape(e)}')
    try:#명령어가 잘못되면?
        df=conn.to_DataFrame(query)
    except Exception as e:
        return alert(request,f'쿼리를 다시 확인해주세요 (check query): {html.unescape(e)}')
    pattern = r"^select\s+.*\s+from\s+(\w+)"
    title=re.search(pattern,query,re.IGNORECASE).group(1)
    code=df.to_html(index=False,escape=False).replace(' class="dataframe"',"").replace(' style="text-align: right;"',"")
    return view(request,title,code,"DB")
@app.post("/sqlapi")
def api(host:str=Form(...),database:str=Form(...),user:str=Form(...),password:str=Form(...),query:str=Form(...),port:int=Form(...)):
    if not query.lower().startswith('select'):
        raise HTTPException(detail=f'쿼리문은 오직 select문만 가능합니다.(qurey support only "select")',status_code=400)
    try:
        conn=MYSQLConn(host=host,user=user,database=database,password=password,port=port)
    except Exception as e:
        raise HTTPException(detail=f'DB정보를 다시 확인해주세요(check DB info):{e}',status_code=400)
    try:
        df=conn.to_DataFrame(query)
    except Exception as e:
        raise HTTPException(detail=f'쿼리를 다시 확인해주세요 (check query): {e}',status_code=400)
    code=df.to_html(index=False,escape=False).replace(' class="dataframe"',"").replace(' style="text-align: right;"',"")
    return JSONResponse(content={'table':code},status_code=200)
@app.post("/sheetapi")
def sheet(url:str=Form(...)):
    paths=url.split('/')
    idx=paths.index('d')+1
    id=paths[idx]
    sheet_url = f"https://docs.google.com/spreadsheets/d/{id}/export?format=xlsx"

    response = requests.get(sheet_url)
    if response.status_code%400<100:
        return HTTPException(requests,"url을 확인해 주세요(check url)")
    elif response.status_code%500<100:
        return HTTPException(requests,"서버에 문제가 생겼습니다(error server)")
    df=pd.read_excel(BytesIO(response.content),engine='openpyxl')
    code = df.to_html(index=False, escape=False).replace(' class="dataframe"', "").replace(' style="text-align: right;"', "")
    return JSONResponse(content={'table':code},status_code=200)

@app.post("/file")
async def file(request:Request,file:UploadFile=File(...)):
    name=file.filename
    data= await file.read()
    try:#csv파일인가?
        df=pd.read_csv(StringIO(data.decode("UTF-8")))
    except:#아니면
        try:#tsv 파일인가?
            df=pd.read_csv(StringIO(data.decode("UTF-8")),sep='\t')
        except:#그것도 아니면 excel파일이구나
            df=pd.read_excel(BytesIO(data.decode("UTF-8")))
    code=df.to_html(index=False,escape=False).replace(' class="dataframe"',"").replace(' style="text-align: right;"',"")
    return view(request,name,code,"파일","file","/fileupload")
@app.post("/sheet")
def sheet(request:Request,url:str=Form(...)):
    id=url.split('/')[5]
    sheet_url = f"https://docs.google.com/spreadsheets/d/{id}/export?format=xlsx"
    response = requests.get(sheet_url)
    if response.status_code >= 400 and response.status_code < 500:
        raise HTTPException(status_code=400, detail="URL을 확인해 주세요 (check URL)")
    elif response.status_code >= 500:
        raise HTTPException(status_code=500, detail="서버에 문제가 생겼습니다 (server error)")
    df=pd.read_excel(BytesIO(response.content),engine='openpyxl')
    code = df.to_html(index=False, escape=False).replace(' class="dataframe"', "").replace(' style="text-align: right;"', "")
    return view(request,"시트결과",code,"시트","sheet","/sheetupload")
# Import flask and datetime module for showing date and time
from flask import Flask, render_template
from backend.database.CH_DBModel import db, TestTable # 引入資料庫相關的東西，已經打包成一個 py 檔案
from backend.database.CH_DBRequiredInformation import POSTGRES
from backend.database.CH_queryDB import queryDB
from backend.database.CH_insertDB import write_random_data
import datetime
  
x = datetime.datetime.now()
  
# Initializing flask app
app = Flask(__name__, static_folder="./frontend/static", template_folder="./frontend/templates")
  

@app.route('/')
def index():
    return render_template('index.html')
  
@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/chart')
def chart():
    return render_template('charts.html')

### 資料庫相關 ###

# 設定資料庫相關的連線內容
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://%(user)s:\
%(password)s@%(host)s:%(port)s/%(database)s' % POSTGRES

# 初始化資料庫模型
db.init_app(app)

# 資料庫查詢並顯示的路由
@app.route('/table')
def table():
    # 查詢 TestTable 資料表中的所有資料
    rows = queryDB(TestTable)
    return render_template('tables.html', rows=rows)

@app.route('/db_insert')
def db_insert():
    # 資料表為空的話取 idx 會報錯，因此直接給 0
    try:
        lastIdx = queryDB(TestTable)[-1].idx
    except:
        lastIdx = 0

    # 防呆，其實可以不用
    if lastIdx is not None:
        write_random_data('./static/data.csv', db, lastIdx)

    return 'ok'

### 資料庫相關 ###
      
# Running app
if __name__ == '__main__':
    app.run(debug=True)
    # app.run(debug=False)
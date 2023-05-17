# flask_bootstrap_template

## 參考樣板：https://github.com/startbootstrap/startbootstrap-sb-admin-2

### 主要更動：

透過flask建立路由，並且與backend資料庫做簡單的連接(有待優化)

使用jinja將sidebar、topbar、footer等通用模板放入base_templates，並引入base.html，刪減原本樣板的重複性code

針對index.html、chart.html、table.html做修改，與flask設定route做連接


### 資料庫使用：

修改DBRequireInformation.py

將DBRequireInformation.py引入server.py

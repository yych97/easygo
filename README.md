# easygo
 An easygo heatmap data spider	

-----
1. 需自行购买QQ号
2. 自动拖动滑块功能还未完善

### 已完成：
* 部署多账号，Selenium自动登陆、获取cookies
* 指定区域爬取（已测试上海市范围稳定运行）

### 运行环境：
* python3.6.8
* scrapy1.6.0

### 使用方法：
1. 项目python环境安装，在项目根目录打开cmd输入(建议使用国内的pip镜像进行安装):  
```
pip install -r requirements.txt
```
2. 需要安装Chrome浏览器以及对应版本的Chromedriver，并放入项目根目录
3. 建议使用conda命令新建一个python环境运行
4. 建议安装vscode用于爬虫的调试运行
5. 项目文件夹中：  
    * */start.py* 为爬虫程序入口  
    * */sh_noCM.txt* 为抓取范围的中心点集  
    * */user_agents.py* 为爬虫使用的伪装请求头，越多越不容易被识别为爬虫  
    * */transCoordinateSystem.py* 用于坐标转换
    * */qq_list_all.yaml* 为qq号存储文件，请参照其中的格式输入使用的qq号
    * */data* 此目录为运行后抓取到的腾讯用户密度数据 
    * */easygo* 此目录中为爬虫的所有模块
    * */easygo/settings.py* 为爬虫的配置文件，包括Scrapy配置项与本项目的自定义配置项
6. 开始爬取前，请先编辑*start.py*文件，每天的第一次使用可将第39行修改为**job([0, 1])**，代表使用qq_list_all.yaml文件中的第一二个qq号进行爬取，第二第三次...以此类推
7. 开始爬取，在项目根目录打开cmd，输入：
```
python start.py
```
8. 也可以使用其他IDE(如vscode)运行start.py，网络稳定情况下大概三分钟即可爬取完上海大陆部分。如遇滑块验证请手动拖动滑块进行验证。
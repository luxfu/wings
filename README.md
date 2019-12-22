# wings
python+PyQ5实现一个简单的mock小程序
由于项目需要mock工具，网上找了下没有合适的，正好在学习python，于是尝试性的编写了这个小工具。
使用python+PyQt5编写GUI界面，有flask搭建后台服务，数据保存在本地data文件（没有使用数据库），最后用pyinstaller打包成exe可执行文件
命令如下：
pyinstaller -F ui.py
如果执行顺利会在当前文件夹生成一个dist目录，目录下生成ui.exe
也可以不打包直接执行ui.py

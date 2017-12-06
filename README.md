# Python-Pack
第一：Python 文件的编写
这个给大家提供一个模板，这个模板支持cocopods管理的项目，已经支持可XCODE 9打包。还有蒲公英，fir.im ,AppStore上传。
https://github.com/HanWait/Python-Pack

第二：plist
我提供的那个文件夹里面有Plist文件，里面只是改了Ent.Plist,其他的要自己修改，Plist的主要作用是打包的时候生成ExportOptions.plist文件，不知道配置的Plist文件写什么，可以自己先打个包看一下。然后把ExportOptions.plist里面的内容全部拷贝一遍到Ent.Plist里面。
￼￼￼￼￼￼￼￼￼￼￼![image.png](http://upload-images.jianshu.io/upload_images/3410393-db417e551c57bb7e.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
第三：打包
当你把所有的参数都弄好了，开始打包。
1.把AutoBuild文件夹放在你要打包的项目的根目录里面，把autobuild.py也放在项目的根目录里面
2.打开终端，cd到项目的根目录里面
3.在终端输入  python autobuild.py
上面三个步骤完成之后，终端就会开始打包，** EXPORT SUCCEEDED **出现这个字样就是打包成功，打好的包会在你的项目的根目录里面Packge文件夹里面。

补充：放在外面的autobuild.py和文件夹里面的不一样，外面的这个是最新修改的，支持打包到桌面上，文件夹里面的是打包到项目工程文件夹里面。

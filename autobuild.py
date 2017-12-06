#-*-coding:utf-8-*-
#!/usr/bin/env python

#./autobuild.py -p youproject.xcodeproj -t youproject -o ~/Desktop/youproject.ipa
#./autobuild.py -w youproject.xcworkspace -s youproject -o ~/Desktop/youproject.ipa
from email.mime.text import MIMEText
from optparse import OptionParser
import subprocess
import smtplib
import os
import getpass
import datetime
# 需要改动的地方 (根据自己的项目信息改动改动)
PROJECT_NAME = "HAHA" 	    #项目名称 如HAHA.xcodeproj
VERSION = "1.1.0.11"  						#打包版本号 会根据不同的版本创建文件夹（与项目本身的版本号无关）
TAGREAT_NAME = "%s" %(PROJECT_NAME) 	#就是对应的target
CONFIGURATION = "Release" 				#Release 环境  Debug 环境
CONFIGURATIONNAME = "iPhone Distribution: ******" 			#配置名   苹果官网证书Profie的配置文件的名字
PROFILE = "Ent" 						#配置文件分为四种 AdHoc  Dev  AppStore Ent 分别对应四种配置文件
TIME = datetime.datetime.now()
#OUTPUT = "./Packge/%s" %(CONFIGURATION) #打包导出ipa文件路径（请确保 “%s” 之前的文件夹正确并存在）

OUTPUT = "/Users/" + getpass.getuser() + "/"+ "Desktop" #打包导出ipa文件路径（请确保 “%s” 之前的文件夹正确并存在）//这个是打包的文件直接放在桌面上，与压缩包里面的就这点不一样

WORKSPACE = "%s.xcworkspace" %(PROJECT_NAME)
PROJECT = "%s.xcodeproj" %(PROJECT_NAME)
SDK = "iphoneos"
#注意：如果在项目中用到 pod 请启用此行！！！！！！
PROJECT = None

#蒲公英上传
OPEN_PYUPLOAD = False  	#是否开启蒲公英上传功能  True  False
USER_KEY = "***"
API_KEY = "*****"

#fir.im 上传
OPEN_FIR_UPLOAD = False  	#是否开启fir.im上传功能  True  False

#AppStore上传
OPEN_APPSTORE_UPLOAD = False  #是否开启AppStore上传上传功能  True  False
USER_NAME = "****************"
USER_PASSWORD = "****************"

# 输入Email地址和口令:
from_addr = "123456789@qq.com"
password = "gjgqxogqdrbgdfih"
# 输入收件人地址:
to_addr = "123456789@qq.com"
# 输入SMTP服务器地址:
smtp_server = "smtp.qq.com"

#发送邮件
def sendmail_func(sendContent):
    server = smtplib.SMTP_SSL(smtp_server, 465) # SMTP协议默认端口是25
    server.set_debuglevel(1)
    server.login(from_addr, password)
    msg = MIMEText(sendContent, 'plain', 'utf-8')
    server.sendmail(from_addr, [to_addr], msg.as_string())
    server.quit()
#启动打印函数
def printStart():
	print "*****************************************************************"
	print "*****************************************************************"
	print "                       开始打包                             "
	print "  项目名称：%s" %(PROJECT_NAME)
	print "  Target：%s" %(TAGREAT_NAME)
	print "  版 本 号：%s" %(VERSION)
	print "  编译环境：%s" %(CONFIGURATION)
	print "  证书配置：%s" %(PROFILE)
	print "  是否上传蒲公英：%s" %(OPEN_PYUPLOAD)
	print "  是否上传FIR.IM：%s" %(OPEN_FIR_UPLOAD)
	print "  是否上传AppStore：%s\n" %(OPEN_APPSTORE_UPLOAD)
	print "*****************************************************************"
	print "*****************************************************************"

#结束打印函数
def printEnd():
	print "*****************************************************************"
	print "*****************************************************************"
	print "                       结束打包                             "
	print "  项目名称：%s" %(PROJECT_NAME)
	print "  Target：%s" %(TAGREAT_NAME)
	print "  版 本 号：%s" %(VERSION)
	print "  编译环境：%s" %(CONFIGURATION)
	print "  证书配置：%s" %(PROFILE)
	print "  是否上传蒲公英：%s" %(OPEN_PYUPLOAD)
	print "  是否上传FIR.IM：%s" %(OPEN_FIR_UPLOAD)
	print "  是否上传AppStore：%s\n" %(OPEN_APPSTORE_UPLOAD)
	print "*****************************************************************"
	print "*****************************************************************"

#清除 build 目录
def cleanBuildDir(buildDir):
	cleanCmd = "rm -r %s" %(buildDir)
	process = subprocess.Popen(cleanCmd, shell = True)
	process.wait()

#创建路径
def createDir(ipaDir):
	createCmd = "mkdir %s" %(ipaDir)
	process = subprocess.Popen(createCmd, shell = True)
	process.wait()

def uploadPgy(ipaPath):
	print "\n***************开始上传到蒲公英*********************\n"
	uploadCmd = 'curl -F \"file=@%s\" -F \"uKey=%s\" -F \"_api_key=%s\" https://www.pgyer.com/apiv1/app/upload' %(ipaPath, USER_KEY, API_KEY)
	process = subprocess.Popen(uploadCmd, shell = True)
	process.wait()
	print "\n\n***************上传结束 Code=0 为上传成功*********************\n"

def uploadFir(ipaPath):
	print "\n***************开始上传到FIR.IM*********************\n"
	uploadCmd = 'fir p %s' %(ipaPath)
	process = subprocess.Popen(uploadCmd, shell = True)
	process.wait()
	print "\n\n***************上传结束 Published succeed 为上传成功*********************\n"
	

def uploadAppStore(ipaPath):

	altool = "/Applications/Xcode.app/Contents/Applications/Application\ Loader.app/Contents/Frameworks/ITunesSoftwareService.framework/Versions/A/Support/altool"

	print "\n***************开始上传到AppStore*********************\n"
	uploadCmd = '%s --upload-app -f %s -t ios -u %s -p %s' %(altool, ipaPath, USER_NAME, USER_PASSWORD)
	process = subprocess.Popen(uploadCmd, shell = True)
	process.wait()
	print "\n\n***************上传结束 No errors uploading 为上传成功*********************\n"
	print "***************上传成功后，稍等片刻才能在 iTunes Connect 上更新*********************\n"



#打包
def xcbuild():
	#配置打包命令
	if PROJECT is None and WORKSPACE is None:
		pass
	elif PROJECT is not None:
		buildCmd = 'xcodebuild archive -project %s -scheme %s -sdk %s -configuration %s  ONLY_ACTIVE_ARCH=NO -archivePath ./build/%s.xcarchive' %(PROJECT, TAGREAT_NAME, SDK, CONFIGURATION,PROJECT_NAME)
		pass
	elif WORKSPACE is not None:
		buildCmd = 'xcodebuild archive -workspace %s -scheme %s -sdk %s -configuration %s  ONLY_ACTIVE_ARCH=NO -archivePath ./build/%s.xcarchive' %(WORKSPACE, TAGREAT_NAME, SDK, CONFIGURATION, PROJECT_NAME)
		pass
	
	printStart()

	#开始执行打包命令
	process = subprocess.Popen(buildCmd, shell = True)
	process.wait()

	#创建目录
	createDir(OUTPUT)
	filepath = OUTPUT+"/"+TAGREAT_NAME+"_%s" %VERSION
	#createDir(filepath)

	#执行签名验证导出命令
#xcode 8.3 以前
#	signCmd = 'xcodebuild -exportArchive -archivePath ./build/%s.xcarchive  -exportPath %s/%s/%s_%s_%s -exportFormat ipa -exportProvisioningProfile \"%s\"' %(PROJECT_NAME, OUTPUT, VERSION,PROJECT_NAME,VERSION,CONFIGURATION,CONFIGURATIONNAME)
#xcode 8.3 
	signCmd = 'xcodebuild -exportArchive -archivePath ./build/%s.xcarchive  -exportPath %s/%s_%s_%s -exportOptionsPlist ./AutoBuild/plist/%s.plist' %(PROJECT_NAME, OUTPUT,PROJECT_NAME,TIME,CONFIGURATION,PROFILE)
	process = subprocess.Popen(signCmd, shell = True)
	process.wait()

	printEnd()

	#ipaPath = "%s/%s_%s_%s/%s.ipa" %(OUTPUT,PROJECT_NAME,VERSION,CONFIGURATION,TAGREAT_NAME)
	ipaPath = "%s/%s.ipa" %(filepath,TAGREAT_NAME)
	
	sendContent = '你好,打包完成，文件保存在 '+os.path.abspath(ipaPath)
	# sendmail_func(sendContent)
	
	#蒲公英上传
	if OPEN_PYUPLOAD == True:
		uploadPgy(ipaPath)

	#FIR.IM上传
	if OPEN_FIR_UPLOAD == True:
		uploadFir(ipaPath)

	#AppStore上传
	if OPEN_APPSTORE_UPLOAD == True:
		uploadAppStore(ipaPath)

	#清理build目录
	cleanBuildDir("./build")


def main():

	xcbuild()

if __name__ == '__main__':
	main()

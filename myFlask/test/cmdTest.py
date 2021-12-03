#!/usr/bin/python
# -*- coding:utf-8 -*-
# @File  : cmdTest.py
# @Author: p_lixuanzhu
# @date 2021/12/3

import os
from testLogger import testLogger
from config import data_path
import shutil


def compileProto():
    """
    :Author:  p_lixuanzhu
    :Update:  2021/12/3 20:20
    :desc:    执行该方法前，先执行copyProto()
    """
    mktTmpDir = os.path.join(data_path,'marketingTmpDir')
    #获取mktTmpDir目录下所有的文件名
    files = os.listdir(mktTmpDir) #为一个数组
    testLogger.info(files)
    #执行python命令：python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. ./ao_vb_marketing_act_server.proto
    testLogger.info("编译proto文件开始。。。。。")
    try:
        for file in files:
            if file.split('.')[1] == 'proto':
                cmdStr = "python -m grpc_tools.protoc -I%s --python_out=%s --grpc_python_out=%s %s\%s" % (mktTmpDir,mktTmpDir,mktTmpDir,mktTmpDir,file)
                # testLogger.debug(cmdStr)
                p = os.popen(cmdStr)
                f = p.read()
                testLogger.info(f)
        testLogger.info("编译proto文件结束")
    except Exception as err:
        testLogger.error(err)

def copyProto():
    """
    :Author:  p_lixuanzhu
    :Update:  2021/12/3 15:09
    :desc:    读取开发的proto文件，并放置至marketingTmpDir目录（覆盖式放进去）
    """
    #获取开发proto文件夹路径
    devProtoDir = r"D:\work\codeDev\proto_files\vb\marketing"

    #获取marketingTmpDir文件夹路径
    mktTmpDir = os.path.join(data_path, 'marketingTmpDir')

    #遍历目录下proto文件，包含子目录，进行复制到marketingTmpDir目录下
    msg = "拷贝文件开始,源地址：%s，目标地址：%s" % (devProtoDir,mktTmpDir)
    testLogger.info(msg)
    getCopyDir(devProtoDir,mktTmpDir,fileType='proto')
    testLogger.info("拷贝文件结束")

def getFilePathList(srcDir,fileType):
    try:
        filePathList = []
        for i, j, k in os.walk(srcDir):
            #如果第三个列表有值，筛选为.proto文件，拼接第一个值，即为proto文件完整路径，再append进list中
            if k:
                for f in k:
                    if f.split('.')[1] == fileType:
                        filePathList.append(os.path.join(i,f))
        testLogger.info(filePathList)
        return filePathList
    except Exception as err:
        testLogger.error(err)

def getCopyDir(srcDir,dstDir,fileType=None):
    """
    :Author:  p_lixuanzhu
    :Update:  2021/12/3 20:08
    :desc:    fileType:筛选要复制的文件类型，不传则默认全部复制
    """
    try:
        for i, j, k in os.walk(srcDir):
            #如果第三个列表有值，筛选为.proto文件，拼接第一个值，即为src proto文件完整路径，再拼接dst proto文件完整路径，最后再把src文件copy进dst文件，即形成一个复制后的文件夹
            if k:
                for f in k:
                    if fileType:
                        if f.split('.')[1] == fileType:
                            srcFilePath = os.path.join(i,f)
                            dstFilePath = os.path.join(dstDir,f)
                            shutil.copyfile(srcFilePath, dstFilePath)
                    else:
                        srcFilePath = os.path.join(i, f)
                        dstFilePath = os.path.join(dstDir, f)
                        shutil.copyfile(srcFilePath, dstFilePath)
    except Exception as err:
        testLogger.error(err)

if __name__ == '__main__':
    copyProto()
    compileProto()
    testLogger.info("test.....")
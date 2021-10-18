from PyQt5.QtGui import  QImage, QPixmap
from multiprocessing import Process
import numpy as np  
import cv2 
import threading
import datetime
import time
from Lib.Utils import *
from PyQt5.QtCore import *
#from Lib.ft2 import *
"""相机操作类""" 
class CvCamera(QObject):
    stopFlowSignal = pyqtSignal()
    playVideoSignal = pyqtSignal(QPixmap)
    def __init__(self,qlabel,width,height):
       #获取当前相机
       self.cap = cv2.VideoCapture(0)
       #ret, frame = self.cap.read()
       #设置相机图像格式
       #self.cap.set(cv2.CAP_PROP_FOURCC,cv2.VideoWriter_fourcc('M','J','P','G'))
       #设置显示图像宽高
       self.cap.set(cv2.CAP_PROP_FRAME_WIDTH,480)
       self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT,320)

       self.experimentId = ""
       self.experimentStepIndex = 0
       self.experimentFlag = False

       #self.ft = put_chinese_text('/home/pi/Downloads/11/Lib/msyh.ttf')
      
       #设置相机FPS
       self.cap.set(cv2.CAP_PROP_FPS ,30)
       self.fourcc = None
       self.out = None
       self.workFlag = True
       self.recordFlag = False
       self.width = width
       self.height = height
       self.viewLabel = qlabel
       self.viewLabel.setVisible(False)
       self.avg = None
       self.fj=None
       self.firstBG=None
       self.startExperimentTime=0
       super().__init__()

    def start(self):
        try:
            self.workFlag = True
            #单独线程供相机使用
            t = threading.Thread(target=self.videoWork,args=(self.viewLabel,self.width,self.height))
            t.start()
        except Exception as e:
            print(e)
    def stop(self):
        self.workFlag = False

    #显示图像
    def show(self):
       self.viewLabel.setVisible(True)
    #隐藏图像
    def hide(self):
       self.viewLabel.setVisible(False)
    #开始记录
    def startRecord(self,width,height):
       self.fourcc = cv2.VideoWriter_fourcc(*'XVID')
       self.out = cv2.VideoWriter("Resources/Video/" + datetime.datetime.now().strftime("%Y%m%d%H%M%S") + '.avi', self.fourcc,21.0,(width,height))
       self.recordFlag = True
    #停止记录
    def stopRecord(self):
       self.recordFlag = False
       if(self.out):
           self.out.release()
    #释放资源
    def release(self):
       self.workFlag = False
       time.sleep(0.2)
       if(self.out):
           self.out.release()
       self.cap.release()
       
    # 定义旋转rotate函数
    def rotate(self,image, angle, center=None, scale=1.0):
        # 获取图像尺寸
        (h, w) = image.shape[:2]

        # 若未指定旋转中心，则将图像中心设为旋转中心
        if center is None:
            center = (w / 2, h / 2)

        # 执行旋转
        M = cv2.getRotationMatrix2D(center, angle, scale)
        rotated = cv2.warpAffine(image, M, (w, h))

        # 返回旋转后的图像
        return rotated

    #相机图像分析
    def videoWork(self,qlable,vwidth,vheight):
        #qlable.resize(vwidth,vheight)
        avgFrameCount = 0
        d = None
        startTime = 0
        statusTxt = 'Not started'
        firstIndex=0;
        self.firstBG=None
        self.avg=None
        self.fj=None
        experimentFlag=False
        self.startExperimentTime=0
        while(self.workFlag):
            try:
                # 当实验开始并且开始时间为0时获取当前时间
                if(self.experimentFlag == True and startTime == 0):
                    statusTxt = 'Initializing...'
                    startTime = time.time()

                #if(self.experimentFlag == True and (time.time() - startTime) >= 3):
                    #statusTxt = 'Monitoring...'
                # 统计开始时间
                t = cv2.getTickCount()
                # 从摄像头逐帧捕获数据
                ret, frame = self.cap.read()
                # 旋转图像
                frame = np.rot90(frame)  
                frame = frame.copy()
                if(self.fourcc and self.out and self.recordFlag):
                    self.out.write(frame)


                height, width, bytesPerComponent = frame.shape
                bytesPerLine = bytesPerComponent * width

                # 转换为灰阶图像并进行模糊
                gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
                gray = cv2.GaussianBlur(gray,(21,21),0)

                if(self.firstBG is None):
                    firstIndex+=1;
                    if(firstIndex==2):
                        self.firstBG=gray.copy().astype("float")
                if(self.experimentFlag == True and startTime == 0 and self.fj is None):
                    self.fj=gray.copy().astype("float")
                #gray = gray[50:300,30:100]
                # 如果平均帧是None，初始化它
                if(self.experimentFlag == True and startTime!=0 and (time.time() - startTime) >= 3 and self.avg is None):
                    statusTxt = 'Monitoring...'
                    self.avg = gray.copy().astype("float")
                if(self.avg is not None):
                    cv2.accumulateWeighted(gray,self.avg,0.5)
                    cnts=self.Frameabsdiff(gray,self.avg,12)
                    # 遍历轮廓线
                    count = 0
                    for c in cnts:
                        if cv2.contourArea(c) < 60:
                            continue
                        # 计算轮廓线的外框, 在当前帧上画出外框
                        # 并且更新文本
                        (x, y, w, h) = cv2.boundingRect(c)
                        if((x + w) < 200 and (x + w) > 100 and y<150):
                            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 1)
                            count+=1
                    if(self.experimentFlag == True and (time.time() - startTime) >= 3 and count > 0):
                        cp=self.fj.copy()
                        cv2.accumulateWeighted(gray,self.fj,0.5)
                        cnts1=self.Frameabsdiff(gray,self.fj,35)
                        self.fj=cp
                        count1=0;
                        for c1 in cnts1:
                            if cv2.contourArea(c1) < 200:
                                continue
                            # 计算轮廓线的外框, 在当前帧上画出外框
                            # 并且更新文本
                            (x1, y1, w1, h1) = cv2.boundingRect(c1)
                            if((x1 + w1) < 200 and (y1 + h1) > 200):
                                cv2.rectangle(frame, (x1, y1), (x1 + w1, y1 + h1), (0, 255, 0), 1)
                                count1+=1

                        if(count1==0):
                            self.stopFlowSignal.emit()
                            self.avg=None
                            self.fj=None
                            firstIndex=0;
                            self.startExperimentTime=0
                            path = "/home/pi/Downloads/11/Resources/EXImages/{0}".format(self.experimentId)
                            Utils.mkdir(path)
                            cv2.imwrite("/home/pi/Downloads/11/Resources/EXImages/{0}/{1}.jpg".format(self.experimentId,self.experimentStepIndex),cv2.resize(frame,(480,640),interpolation=cv2.INTER_CUBIC))
                            self.experimentFlag = False  
                            startTime = 0
                            statusTxt = "Not started"
                                             
                t = (cv2.getTickCount() - t) / cv2.getTickFrequency()
                str1 = "FPS:" + str(round(1.0 / t,2))
                cv2.putText(frame, str1,(6, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX,
                            0.30, (0, 0, 255), 1)

                cv2.putText(frame, "Tanyo",(width - 38, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX,
                            0.35, (0, 0, 255), 1)
                cv2.putText(frame, statusTxt,(3, 15), cv2.FONT_HERSHEY_SIMPLEX,
                            0.35, (0, 255, 0), 1)

                
                if(self.startExperimentTime!=0):
                    currentExperimentTime=(int(round(time.time() * 1000)))
                    diffTime=round((currentExperimentTime-self.startExperimentTime)/1000,1)
                    cv2.putText(frame, str(diffTime)+"s",(width - 38, 15), cv2.FONT_HERSHEY_SIMPLEX,
                                0.35, (0, 0, 255), 1)
                #frame= self.ft.draw_text(frame, (3, 3), statusTxt, 13,
                #(0,255,0))

                frame = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
                self.image = QImage(frame.data,width,height,bytesPerLine, QImage.Format_RGB888)
                #qlable.setPixmap(QPixmap.fromImage(self.image).scaled(vwidth,vheight))
                self.playVideoSignal.emit(QPixmap.fromImage(self.image).scaled(vwidth,vheight))

            except Exception as e:  
                print(e)
    
    def Frameabsdiff(self,currentFrame,bgFrame,thresholdValue):
        frameDelta = cv2.absdiff(currentFrame,  cv2.convertScaleAbs(bgFrame))
        # 对变化图像进行阀值化, 膨胀阀值图像来填补
        # 梯度图像中不大于25的任何像素都设置为0（黑色）。 否则，像素设置为255（白色）
        thresh = cv2.threshold(frameDelta, thresholdValue, 255,
                                            cv2.THRESH_BINARY)[1]
        thresh = cv2.dilate(thresh, None, iterations=4)
        (_, cnts,_) = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
                                                cv2.CHAIN_APPROX_SIMPLE)
        return cnts
import cv2
import numpy
import socket
import struct
from socket import*
from time import sleep

#yingjian
in11 = 24
in12 = 23
in13 =12
in14 = 16
en11 = 25
en12 = 26

in21 = 6
in22 = 5
in23 = 17
in24 = 27
en21 = 13
en22 = 22

temp1=1



s = socket(AF_INET,SOCK_DGRAM)
# raspberry pi IP
s.bind(("192.168.137.135", 6000))
print("UDP on port 6000...")
print('send frames...')
# opencv camera
capture=cv2.VideoCapture(0)

data, addr = s.recvfrom(1024)
# resolution
capture.set(3, 720)
capture.set(4, 480)


while True:
    
    success,frame=capture.read()
    while not success and frame is None:
        success,frame=capture.read() #获取视频帧
     
    # opencv quality
    result,imgencode=cv2.imencode('.jpg',frame,[cv2.IMWRITE_JPEG_QUALITY,40])
    
    # video pack
    s.sendto(struct.pack('i',imgencode.shape[0]), addr)
    
    # sent
    s.sendto(imgencode, addr)







    udp_socket=socket(AF_INET,SOCK_DGRAM)
    
    local_addr=('',8002)#ip地址和端口号，IP不写表示本机任何一个ip
    
    udp_socket.bind(local_addr)
    
    #3、等待接收对方发送的数据
    
    recv_data=udp_socket.recvfrom(1024)#1024表示本次接收的最大字节
    
    #recv_data存储的是一个元组（发送方ip，Port）
    
    recv_msg=recv_data[0]
    
    send_addr=recv_data[1]
    #4、显示接收到的数据
    con_code=0
    con_code=int(recv_msg.decode("gbk"))
    
    udp_socket.close()
    
    if con_code==0:
        GPIO.output(in11,GPIO.LOW)
        GPIO.output(in12,GPIO.LOW)
        
        GPIO.output(in13,GPIO.LOW)
        GPIO.output(in14,GPIO.LOW)
        
        GPIO.output(in21,GPIO.LOW)
        GPIO.output(in22,GPIO.LOW)
        
        GPIO.output(in23,GPIO.LOW)
        GPIO.output(in24,GPIO.LOW)
    elif con_code==1:
        p1.ChangeDutyCycle(85)
        GPIO.output(in11,GPIO.HIGH)
        GPIO.output(in12,GPIO.LOW)
                    
        p2.ChangeDutyCycle(85)
        GPIO.output(in13,GPIO.HIGH)
        GPIO.output(in14,GPIO.LOW)
                    
        p3.ChangeDutyCycle(85)
        GPIO.output(in21,GPIO.HIGH)
        GPIO.output(in22,GPIO.LOW)
                    
        p4.ChangeDutyCycle(85)
        GPIO.output(in23,GPIO.LOW)
        GPIO.output(in24,GPIO.HIGH)
    elif con_code==2:
        p1.ChangeDutyCycle(85)
        GPIO.output(in11,GPIO.HIGH)
        GPIO.output(in12,GPIO.LOW)
        
        p2.ChangeDutyCycle(85)
        GPIO.output(in13,GPIO.LOW)
        GPIO.output(in14,GPIO.HIGH)
        
        p3.ChangeDutyCycle(85)
        GPIO.output(in21,GPIO.HIGH)
        GPIO.output(in22,GPIO.LOW)
        
        p4.ChangeDutyCycle(85)
        GPIO.output(in23,GPIO.HIGH)
        GPIO.output(in24,GPIO.LOW)
    elif con_code==3:
        p1.ChangeDutyCycle(85)
        GPIO.output(in11,GPIO.LOW)
        GPIO.output(in12,GPIO.HIGH)
        
        p2.ChangeDutyCycle(85)
        GPIO.output(in13,GPIO.LOW)
        GPIO.output(in14,GPIO.HIGH)
        
        p3.ChangeDutyCycle(85)
        GPIO.output(in21,GPIO.LOW)
        GPIO.output(in22,GPIO.HIGH)
        
        p4.ChangeDutyCycle(85)
        GPIO.output(in23,GPIO.HIGH)
        GPIO.output(in24,GPIO.LOW)
    elif con_code==4:
        p1.ChangeDutyCycle(85)
        GPIO.output(in11,GPIO.LOW)
        GPIO.output(in12,GPIO.HIGH)
        
        p2.ChangeDutyCycle(85)
        GPIO.output(in13,GPIO.HIGH)
        GPIO.output(in14,GPIO.LOW)
        
        p3.ChangeDutyCycle(85)
        GPIO.output(in21,GPIO.LOW)
        GPIO.output(in22,GPIO.HIGH)
        
        p4.ChangeDutyCycle(85)
        GPIO.output(in23,GPIO.LOW)
        GPIO.output(in24,GPIO.HIGH)
    elif con_code==5:
        p1.ChangeDutyCycle(85)
        GPIO.output(in11,GPIO.LOW)
        GPIO.output(in12,GPIO.HIGH)
                    
        p2.ChangeDutyCycle(85)
        GPIO.output(in13,GPIO.HIGH)
        GPIO.output(in14,GPIO.LOW)
                    
        p3.ChangeDutyCycle(85)
        GPIO.output(in21,GPIO.HIGH)
        GPIO.output(in22,GPIO.LOW)
                    
        p4.ChangeDutyCycle(85)
        GPIO.output(in23,GPIO.HIGH)
        GPIO.output(in24,GPIO.LOW)
    elif con_code==6:
        p1.ChangeDutyCycle(85)
        GPIO.output(in11,GPIO.HIGH)
        GPIO.output(in12,GPIO.LOW)
                    
        p2.ChangeDutyCycle(85)
        GPIO.output(in13,GPIO.LOW)
        GPIO.output(in14,GPIO.HIGH)
                    
        p3.ChangeDutyCycle(85)
        GPIO.output(in21,GPIO.LOW)
        GPIO.output(in22,GPIO.HIGH)
                    
        p4.ChangeDutyCycle(85)
        GPIO.output(in23,GPIO.LOW)
        GPIO.output(in24,GPIO.HIGH)
    elif con_code==7:
        p1.ChangeDutyCycle(85)
        GPIO.output(in11,GPIO.HIGH)
        GPIO.output(in12,GPIO.LOW)
        
        GPIO.output(in13,GPIO.LOW)
        GPIO.output(in14,GPIO.LOW)
        
        p3.ChangeDutyCycle(85)
        GPIO.output(in21,GPIO.HIGH)
        GPIO.output(in22,GPIO.LOW)
        
        GPIO.output(in23,GPIO.LOW)
        GPIO.output(in24,GPIO.LOW)
    elif con_code==8:
        GPIO.output(in11,GPIO.LOW)
        GPIO.output(in12,GPIO.LOW)
        
        p2.ChangeDutyCycle(85)
        GPIO.output(in13,GPIO.HIGH)
        GPIO.output(in14,GPIO.LOW)
        
        GPIO.output(in21,GPIO.LOW)
        GPIO.output(in22,GPIO.LOW)
        
        p4.ChangeDutyCycle(85)
        GPIO.output(in23,GPIO.LOW)
        GPIO.output(in24,GPIO.HIGH)
    elif con_code==9:
        GPIO.output(in11,GPIO.LOW)
        GPIO.output(in12,GPIO.LOW)
        
        p2.ChangeDutyCycle(85)
        GPIO.output(in13,GPIO.LOW)
        GPIO.output(in14,GPIO.HIGH)
        
        GPIO.output(in21,GPIO.LOW)
        GPIO.output(in22,GPIO.LOW)
        
        p4.ChangeDutyCycle(85)
        GPIO.output(in23,GPIO.HIGH)
        GPIO.output(in24,GPIO.LOW)
    elif con_code==10:
        p1.ChangeDutyCycle(85)
        GPIO.output(in11,GPIO.LOW)
        GPIO.output(in12,GPIO.HIGH)
        
        GPIO.output(in13,GPIO.LOW)
        GPIO.output(in14,GPIO.LOW)
        
        p3.ChangeDutyCycle(85)
        GPIO.output(in21,GPIO.LOW)
        GPIO.output(in22,GPIO.HIGH)
        
        GPIO.output(in23,GPIO.LOW)
        GPIO.output(in24,GPIO.LOW)
    
    
    
    
    
s.close()



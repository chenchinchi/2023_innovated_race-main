import time
import multiprocessing
from v5_shoppingcart import *
from PyQt5 import QtWidgets
from controller2 import main_page_controller
import os
import sys

def process1(event): #建立第一進程
    ROI = [[0,0],[640,240]]
    IOU = [None,None]
    reg =[None,None]
    index2item = ["redtea","milktea","greentea"]
    # Load the YOLOv8 model
    model = YOLO('best.pt')
    # Open the video file   
    video_path = 0 #"path/to/your/video/file.mp4"
    cap = cv2.VideoCapture(video_path)
    #init
    frames_num =10
    total_price = 0
    motion = [None,None]
    frames = 0
    while cap.isOpened() and not event.is_set():
        # Read a frame from the video
        success, frame = cap.read()      
        frames = frames+1
        if success:
            frame=cv2.resize(frame, (640,480))
            # Run YOLOv8 inference on the frame
            results = model(frame,conf=0.5)
            # Visualize the results on the frame
            annotated_frame = results[0].plot()
            boxes = results[0].boxes
            annotated_frame = show(annotated_frame)
            # Display the annotated frame
            cv2.imshow("YOLOv8 Inference", annotated_frame)
        else:
            # Break the loop if the end of the video is reached
            break
        if frames==frames_num:
            frames = 0
            try:
                iou = get_iou(boxes.xyxy[-1],)
                push(IOU,iou)
                
                sign = in_or_out(IOU)
                push(motion,[sign,index2item[int(boxes.cls[-1])]])
                if motion[0]!=motion[1]:
                    shop_list(sign,index2item[int(boxes.cls[-1])])
                   # totalprice = final_list(reg_dict)
            except:
                IOU = [None,None]
                reg =[None,None]
                motion = [None,None]
        #print(event.is_set())
        # Break the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord("q") or event.is_set():
            cap.release()
            cv2.destroyAllWindows()
            break

def process2(event):#建立第二進程
    while not event.is_set():
        app = QtWidgets.QApplication(sys.argv)
        window = main_page_controller()
        window.show()
        sys.exit(app.exec_())

if __name__ == "__main__":
    # 创建一个事件，用于通知子进程结束
    event = multiprocessing.Event()

    # 创建两个子进程，分别运行process1和process2函数
    p1 = multiprocessing.Process(target=process1, args=(event,))
    p2 = multiprocessing.Process(target=process2, args=(event,))

    # 启动子进程
    p1.start()
    p2.start()

    # 等待子进程2结束
    p2.join()

    # 设置事件，通知子进程1结束
    event.set()
     
    # 等待子进程1结束
    p1.join()

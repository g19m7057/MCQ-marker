from pdf2image import convert_from_path
import cv2
import imutils
import numpy as np
import matplotlib.pyplot as plt
from imutils import contours
import csv
   

def findCnt(thresh):
    cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    questionCnts = []
    # loop over the contours
    for c in cnts:
        area = cv2.contourArea(c)
        (x,y),radius = cv2.minEnclosingCircle(c)
        #print(area2
        if (radius >= 13 and radius <= 15 and area >= 400):
            questionCnts.append(c) 
            
    questionCnts = contours.sort_contours(questionCnts,method="left-to-right")[0]
    
    return questionCnts

def getCoords(box):
    x1 = box[0][0]
    y1 = box[1][1]
    x2 = box[2][0]
    y2 = box[2][1]
    return (x1,y1,x2,y2)

def markQuestions(questionCnts,thresh,offset): 
    answers = []
    for(q,i) in enumerate(np.arange(0,len(questionCnts),5)):
        cnts = contours.sort_contours(questionCnts[i:i+5]) 
        bubbled = None
        
        #print(i)
        #print(q)
        first = questionCnts[i:i+5]
        index = 1
        number = 1
        if q+1 >= 0: 
            if q+1 == 23 and offset < 1:
                continue
            if(q+1 <= 22):
                questionNum = q+1
            else:
                questionNum = q
            row = []
            for j in first:
                rect = cv2.minAreaRect(j)
                box = cv2.boxPoints(rect)
                box = np.int0(box)
                x1,y1,x2,y2 = getCoords(box)
                
                if(index==1):
                    if y2 - y1 < 25:
                        y2 =y1 + 25
                    row = thresh[y1:y2+10,:]
                    
                    #print("height: ",y2-y1)
                index = index + 1
            
            questions = findCnt(row) 
            res = 0
            biggest = 300
            ind = 1
            for k in questions:
                rect = cv2.minAreaRect(k)
                box = cv2.boxPoints(rect)
                box = np.int0(box)
                x1,y1,x2,y2 = getCoords(box)
                if y2 - y1 < 25:
                    y2 =y1 + 25
                if x2 - x1 < 25:
                    x2 =x1 + 25
                roi = row[:,x1:x2]
                
                    
                total = cv2.countNonZero(roi)
                if(q+1 == 42):
                    print(total)
                    #cv2.imshow("row",row)
                    #cv2.waitKey(0)
                #print(total)
                
                
               
                if(total > biggest):
                    #biggest = total 
                    res = ind
                    answers.append((questionNum + offset,res))
                ind = ind + 1
              
           # if res > 0:
                
    print(answers)
    print()
    return answers

def markQuestions2(questionCnts,thresh,offset): 
    answers = []
    for(q,i) in enumerate(np.arange(0,len(questionCnts),5)):
        cnts = contours.sort_contours(questionCnts[i:i+5]) 
        bubbled = None
        
        #print(i)
        #print(q)
        first = questionCnts[i:i+5]
        index = 1
        number = 1
        if q+1 >= 0: 
            
            questionNum = q+1
            row = []
            for j in first:
                rect = cv2.minAreaRect(j)
                box = cv2.boxPoints(rect)
                box = np.int0(box)
                x1,y1,x2,y2 = getCoords(box)
                
                if(index==1):
                    if y2 - y1 < 25:
                        y2 =y1 + 25
                    row = thresh[y1:y2+10,:]
                    
                    #print("height: ",y2-y1)
                index = index + 1
            
            questions = findCnt(row) 
            res = 0
            biggest = 300
            ind = 1
            for k in questions:
                rect = cv2.minAreaRect(k)
                box = cv2.boxPoints(rect)
                box = np.int0(box)
                x1,y1,x2,y2 = getCoords(box)
                if y2 - y1 < 25:
                    y2 =y1 + 25
                if x2 - x1 < 25:
                    x2 =x1 + 25
                roi = row[:,x1:x2]
                
                    
                total = cv2.countNonZero(roi)
                if(q+1 == 42-offset):
                    print(total)
                    #cv2.imshow("row",row)
                    #cv2.waitKey(0)
                #print(total)
                
                
               
                if(total > biggest):
                    #biggest = total 
                    res = ind
                    answers.append((questionNum + offset,res))
                ind = ind + 1
              
           # if res > 0:
    print("===============================2nd=================")           
    print(answers)
    print()
    return answers

def findDocument(img):
    grey = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    grey = cv2.bilateralFilter(grey, 3, 75, 75)
    edged = cv2.Canny(grey, 75, 200)
    
    
    cnts = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL,
	cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    docCnt = None
    
    if len(cnts) > 0:
        cnts = sorted(cnts, key=cv2.contourArea, reverse=True)
        
    for c in cnts:
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.02 * peri, True)
        
        if len(approx) == 4:
            docCnt = approx
            break
    
    #docCnt = cnts[0]
    rect = cv2.minAreaRect(docCnt)
    box = cv2.boxPoints(rect)
    box = np.int0(box)
    x1 = box[0][0]
    y1 = box[1][1]
    x2 = box[2][0]
    y2 = box[0][1]
    focus = img[y1+10:y2-10,x1+10:x2-10]
    
    return focus

def getInfo(thresh):
    cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
	cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    for i in cnts:
        rect = cv2.minAreaRect(i)
        box = cv2.boxPoints(rect)
        box = np.int0(box)
        
    if len(cnts) > 0:
        cnts = sorted(cnts, key=cv2.contourArea, reverse=True)
    rect = cv2.minAreaRect(cnts[0])
    box = cv2.boxPoints(rect)
    box = np.int0(box)
    return box 
   
def getHalf(questions,offset):
    grey = cv2.cvtColor(questions,cv2.COLOR_BGR2GRAY)
    thresh = cv2.threshold(grey, 0, 255,cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]  
    cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    questionCnts = []
    # loop over the contours
    
    for c in cnts:
        area = cv2.contourArea(c)
        (x,y),radius = cv2.minEnclosingCircle(c)
        if (radius >= 13 and radius <= 15 ):
            questionCnts.append(c)
            
    for i in questionCnts: 
        (x,y),radius = cv2.minEnclosingCircle(i)
        #cv2.circle(questions1,(int(x),int(y)),int(radius),(0,255,0),2)   
    questionCnts = contours.sort_contours(questionCnts,method="top-to-bottom")[0]
    answers = []
    twotwo = False
    if offset == 0:
        answers = markQuestions(questionCnts, thresh, offset)
    else:
        answers = markQuestions2(questionCnts, thresh, offset)
    return answers

def getData(half):
    data = []
    for i in half:
        question,response = i
        if response == 1:
            answer = "A"
        elif response == 2:
            answer = "B"
        elif response == 3:
            answer = "C"
        elif response == 4:
            answer = "D"
        elif response == 5:
            answer = "E"
        elif response == 6:
            answer = "F"
        elif response == 7:
            answer = "G"
        elif response == 8:
            answer = "H"
        elif response == 9:
            answer = "I"
        elif response == 10:
            answer = "J"
        elif response == 11:
            answer = "K"
        elif response == 12:
            answer = "L"
        elif response == 13:
            answer = "M"
        elif response == 14:
            answer = "N"
        elif response == 15:
            answer = "O"
        elif response == 16:
            answer = "P"
        elif response == 17:
            answer = "Q"
        elif response == 18:
            answer = "R"
        elif response == 19:
            answer = "S"
        elif response == 20:
            answer = "T"
        elif response == 21:
            answer = "U"
        elif response == 22:
            answer = "V"
        elif response == 23:
            answer = "W"
        elif response == 24:
            answer = "X"
        elif response == 25:
            answer = "Y"
        elif response == 26:
            answer = "Z"
        data.append((question,answer))
    return data
           
        
def writeData(half1,half2,task,q1,q2,q3,q4,q5,q6,q7):
    fields = ["student_number","task","question","answers"]
    data1 = getData(half1)
    data2 = getData(half2)
    _,alf = q3[0]
    num = str(q1) + str(q2) + str(alf) + str(q4) + str(q5) + str(q6) + str(q7)
    print(num)
    rows = []
    row = []
    index = None
    for i in range (len(data1)):
        question,answer = data1[i]
        row.append(num)
        row.append(task)
        row.append(question)
        row.append(answer)
        rows.append(row)
        row=[]
    rows2 = []
    for i in range (len(data2)):
        question,answer = data2[i]
        row.append(num)
        row.append(task)
        row.append(question)
        row.append(answer)
        rows2.append(row)
        row=[]
        
    
    filename = "data.csv"
    with open(filename,'w',newline='') as csvfile:
        csvwriter = csv.writer(csvfile) 
        csvwriter.writerow(fields)
        csvwriter.writerows(rows)
        csvwriter.writerows(rows2)

def ideal(focus,taska,taskb,q1,q2,q3,q4,q5,q6,q7):
    grey = cv2.cvtColor(focus,cv2.COLOR_BGR2GRAY)
    thresh = cv2.threshold(grey, 0, 255,cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
    
    box = getInfo(thresh)
    x = box[1][0]
    questions = focus[:,x+10:]
     #devide into 2
    width = questions.shape[1] // 2
    questions1 = questions[:,:width]
    questions2 = questions[:,width+1:] 
    
    #deal with first half
    first = getHalf(questions1,0)
    second = getHalf(questions2,30)
    task = str(taska) + str(taskb)
    q3 = getData([(0,q3)])
    writeData(first, second,task,q1,q2,q3,q4,q5,q6,q7)
    
def getInfoAndTask(thresh,information):
    cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
	cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    task =None
    info = None
    for i in cnts:
        area = cv2.contourArea(i)
        if(area >= 30000 and area <= 35000):
            task = i
        elif(area > 100000):
            info = i
        rect = cv2.minAreaRect(i)
        box = cv2.boxPoints(rect)
        box = np.int0(box)
        if(area >= 30000):
            cv2.drawContours(information,[box],0,(0,255,0),2)
    
    rect = cv2.minAreaRect(info)
    box = cv2.boxPoints(rect)
    box1 = np.int0(box)
    
    rect = cv2.minAreaRect(task)
    box = cv2.boxPoints(rect)
    box2 = np.int0(box)
    
    return box1,box2   

def devide(questions):
    width = questions.shape[1] // 2
    questions1 = questions[:,:width]
    questions2 = questions[:,width+1:] 
    return questions1,questions2

def devide8(questions):
    width = questions.shape[1] // 8
    questions1 = questions[:,width:width*2]
    questions2 = questions[:,width*2:width*3]
    questions3 = questions[:,width*3:width*4]
    questions4 = questions[:,width*4:width*5]
    questions5 = questions[:,width*5:width*6]
    questions6 = questions[:,width*6:width*7]
    questions7 = questions[:,width*7:]
    return questions1,questions2,questions3,questions4,questions5,questions6,questions7

def markTask(half):
    grey = cv2.cvtColor(half,cv2.COLOR_BGR2GRAY)
    thresh = cv2.threshold(grey, 0, 255,cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]  
    cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    questionCnts = []
    # loop over the contours
    for c in cnts:
        area = cv2.contourArea(c)
        (x,y),radius = cv2.minEnclosingCircle(c)
        if (radius >= 13 and radius <= 17 ):
           
            questionCnts.append(c)
            
    for i in questionCnts: 
        (x,y),radius = cv2.minEnclosingCircle(i)
        cv2.circle(half,(int(x),int(y)),int(radius),(0,255,0),2)   
    questionCnts = contours.sort_contours(questionCnts,method="top-to-bottom")[0]
    index = 0
    biggest = 0
    answer = []
    res = None
    for j in questionCnts:
        rect = cv2.minAreaRect(j)
        box = cv2.boxPoints(rect)
        box = np.int0(box)
        x1,y1,x2,y2 = getCoords(box) 
        if y2 - y1 < 25:
            y2 =y1 + 25
        row = thresh[y1:y2,:]
        total = cv2.countNonZero(row) 
        if(total > biggest):
            res = index
            biggest = total 
        index = index + 1
    return res

def main():
    path = "2018.pdf"
    images = convert_from_path(path)
    for i in range(len(images)):
       images[i].save('sheet' + str(i) + '.jpg','JPEG')
    img = cv2.imread("sheet0.jpg")
    focus = findDocument(img)
    grey = cv2.cvtColor(focus,cv2.COLOR_BGR2GRAY)
    thresh = cv2.threshold(grey, 0, 255,cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
    
    box = getInfo(thresh)
    x = box[1][0] 
    
    #deal with info
    x1,y1,x2,y2 = getCoords(box)
    information = focus[y1:y2,x1:x2+20]
    grey = cv2.cvtColor(information,cv2.COLOR_BGR2GRAY)
    thresh = cv2.threshold(grey, 0, 255,cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
    info,task = getInfoAndTask(thresh, information)
    
    
    #task
    x1,y1,x2,y2 = getCoords(task)
    tasks = information[y1:y2,x1:x2]
    first,second = devide(tasks)
    a,b =markTask(first),markTask(second)
    
    #info
    x1,y1,x2,y2 = getCoords(info)
    info = information[y1:y2,x1:x2]
    q1,q2,q3,q4,q5,q6,q7 = devide8(info)
    q1,q2,q3,q4,q5,q6,q7 = markTask(q1),markTask(q2),markTask(q3),markTask(q4),markTask(q5),markTask(q6),markTask(q7)
    
   # cv2.imshow("img",q7)
    #cv2.waitKey(0)
    
    ideal(focus,a,b,q1,q2,q3,q4,q5,q6,q7)
    
if __name__ == "__main__":
    main()
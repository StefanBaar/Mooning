import pafy
import cv2


#### segmentation function
#### creates a zero mask where the outline pixels are 255
#### called in line 26
def segmentation(data):
    data           = cv2.bilateralFilter(data[:,:,2],10,100,100)
    data[data<10]  = 0
    data[data>20]  = 255
    ret, thresh    = cv2.threshold(data,1,1,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
    return cv2.Canny(thresh,1,1,apertureSize = 7)

url = "https://www.youtube.com/watch?v=sPABbaavn-0&list=PLomb3VSQH7wjgtTfy1cDproNuqpMI4d3h&index=8&t=0s"
video = pafy.new(url)
best = video.streams[1]     ### change video quality 0 is better but might be slow


capture = cv2.VideoCapture()
capture.open(best.url)

success,image = capture.read()

while success:
    canny             = segmentation(image)
    image[canny==255] = [0,255,0]

    cv2.imshow('frame', image)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    success,image = capture.read()

cv2.destroyAllWindows()
capture.release()

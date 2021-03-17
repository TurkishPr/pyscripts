import os
import glob
import argparse
import cv2
import re
import copy
import shutil
import numpy as np

parser = argparse.ArgumentParser()
parser.add_argument('-path', required=True)
args = parser.parse_args()
path = args.path

class PointDrawer(object):
    def __init__(self, img_paths, log_path, folder_path):
        self.done = False
        self.img_paths = img_paths
        self.log_file = open(log_path, 'w')
        print(log_path)
        self.point_y = -1
        self.window_name = 'image'
        self.end = False
        self.complete_image = []
        self.folder_path = folder_path

    def on_mouse(self, event, x, y, buttons, img):
        if self.done: 
            return
        if event == cv2.EVENT_LBUTTONDOWN:
            self.point_y = y
            self.img_clone = copy.deepcopy(img)
            cv2.circle(self.img_clone, ( int(img.shape[1]/2),y), 1, (243, 250, 140), 2)
            cv2.line(self.img_clone, (0, y), (int(img.shape[1]-1),y), (243, 250, 140), 1)
        elif event == cv2.EVENT_RBUTTONDOWN and self.point_y >= 0:
            self.done = True
            self.log_file.write( '{} {}\n'.format(os.path.basename(self.img_path), str(self.point_y) ) )
            self.complete_image.append( self.img_path )


    def run(self):
        cv2.namedWindow(self.window_name)

        for idx, img_path in enumerate(self.img_paths):
            self.img_path = img_path
            img = imreadEX(img_path)
            self.img_clone = copy.deepcopy(img)
            cv2.setMouseCallback(self.window_name, self.on_mouse, img)
            
            while(not self.done and not self.end):
                cv2.imshow(self.window_name, self.img_clone)
                if cv2.waitKey(50) == 27:
                    self.end = True

            if self.end:
                break
            self.done = False
            self.point_y = -1

        count = 0
        while True:
            new_complete_path = os.path.join( self.folder_path, 'complete_{}'.format(count))
            if not os.path.isdir( new_complete_path ):
                os.makedirs( new_complete_path )
                break
            count +=1

        self.log_file.close()

        for complete_img in self.complete_image:
            shutil.move( complete_img, os.path.join(new_complete_path, os.path.basename(complete_img)))
        shutil.move( log_path, os.path.join(new_complete_path, 'log_{}.txt'.format(count)) )

        
def imreadEX(image_path):
    if re.compile('[^ㄱ-ㅣ가-힣]+').sub('', image_path):
            stream = open(image_path, "rb")
            bytes = bytearray(stream.read())
            numpyarray = np.asarray(bytes, dtype=np.uint8)
            img = cv2.imdecode(numpyarray, cv2.IMREAD_UNCHANGED)
            if not img is None:
                return img
            else:
                file_tmp=tempfile.NamedTemporaryFile().name
                shutil.copy(image_path,file_tmp)
                image_path=file_tmp
    img = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)
    return img

images = glob.glob( path + '/*.png' )
log_path = path+'/log.txt'
pd = PointDrawer(images, log_path, path)
pd.run()

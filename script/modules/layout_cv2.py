import cv2
import numpy as np 

"""!
__brief__: this modules allows to create layouts with opencv2 
"""


def illegal_call():
    print("ILLEGAL CALL")
    exit(0)

class View: 

    COLOR_BG = (255,255,255)

    @staticmethod
    def RGB_TO_BGR(rgb):
        return (rgb[2],rgb[1],rgb[0])
 
    def __init__(self):
        self.color_bg = -1 #View.COLOR_BG
        self.parent = None 

    def set_color_bg(self,_color_bg):
        self.color_bg = View.RGB_TO_BGR(_color_bg)

    def set_parent(self,_parent):
        self.parent = _parent 

    def get_color_bg(self):
        if(self.color_bg != -1):
            return self.color_bg
        if(self.parent == None):
            return View.COLOR_BG
        return self.parent.get_color_bg()

    def create_image_empty(self,size):
        width = size[0]
        height = size[1]
        image = np.zeros((height,width,3), np.uint8)
        image[:,0:width] = self.get_color_bg()
        return image 

    def copy(self,img_base,img_element,position):
        img_base[position[1]:position[1]+img_element.shape[0], 
                 position[0]:position[0]+img_element.shape[1]] = img_element
        return img_base

    def generate(self):
        illegal_call() 

  
    
class ViewImage(View):

    def __init__(self,_path):
        View.__init__(self)
        self.path = _path 
        self.size = None 

    def set_path(self,_path):
        self.path = _path 

    def set_size(self,_size):
        self.size = _size

    def generate(self):
        image = cv2.imread(self.path)
        if(self.size != None):
            image = cv2.resize(image,self.size)
        color_bg = self.get_color_bg() 
        for y in range(image.shape[0]):
            for x in range(image.shape[1]):
                p = image[y,x]
                if(p[0] == 0 and p[1] == 0 and p[2] == 0):
                    image[y,x] = color_bg
        return image 
    
class ViewLabel(View):

    FONT_SIZE = 3
    FONT_COLOR = (255,255,255)

    def __init__(self,_text):
        View.__init__(self)
        self.text = _text
        self.font_size = ViewLabel.FONT_SIZE
        self.font_color = ViewLabel.FONT_COLOR

    def set_text(self,_text):
        self.text = _text

    def set_font_size(self,_font_size):
        self.font_size = _font_size 

    def set_font_color(self,_font_color):
        self.font_color = _font_color

    def generate(self):
        width = len(self.text) * self.font_size * 20
        height = self.font_size * 40
        self.size = (width,height)
        image = self.create_image_empty(self.size)
        cv2.putText(image,
                    self.text, 
                    (0,int(2*height/3)), 
                    2, 
                    self.font_size,
                    self.font_color,
                    2)
        return image


class Layout(View): 
    def __init__(self):
        View.__init__(self)
        self.contents = []
        
    def add(self,view):
        self.contents.append(view)
        view.set_parent(self)

    def generate(self):
        illegal_call()

    def _compute_size(self,images):
        illegal_call() 

    

class LayoutVertical(Layout):

    def __init__(self):
        Layout.__init__(self)

    def _compute_size(self, images):
        height = 0
        width = -1 
        for image in images:
            image_w = image.shape[1]
            image_h = image.shape[0]
            # find the max width 
            if(width == -1 or image_w > width):
                width = image_w
            height += image_h
        return (width,height)
                 
    def generate(self):
        # get images 
        images = []
        for content in self.contents: 
            image = content.generate()
            images.append(image)
        # compute size final image 
        size = self._compute_size(images)
        image_result = self.create_image_empty(size)
        # generate the final image 
        current_height = 0
        for image in images:
            position = (0,current_height)
            current_height += image.shape[0] 
            self.copy(image_result,image,position)
        return image_result 


class LayoutHorizontal(Layout):

    def __init__(self):
        Layout.__init__(self)

    def _compute_size(self, images):
        height = -1
        width = 0 
        for image in images:
            image_w = image.shape[1]
            image_h = image.shape[0]
            # find the max width 
            if(height == -1 or image_h > height):
                height = image_h
            width += image_w
        return (width,height)
                 
    def generate(self):
        # get images 
        images = []
        for content in self.contents: 
            image = content.generate()
            images.append(image)
        # compute size final image 
        size = self._compute_size(images)
        image_result = self.create_image_empty(size)
        # generate the final image 
        current_width = 0
        for image in images:
            position = (current_width,0)
            current_width += image.shape[1] 
            self.copy(image_result,image,position)
        return image_result 



        


    


    

      


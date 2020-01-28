import cv2
import os 

import json 
import time 

import numpy as np
import copy 

from .layout_cv2 import * 


class Bpm: 
    def __init__(self,_min,_max,_freq):
        self.min = _min
        self.max = _max
        self.freq = _freq

    def get_min(self):
        return self.min

    def get_max(self):
        return self.max

    def get_freq(self):
        return self.freq 

class LevelPopUp:
    WARNING = "warning"
    FAIL = "fail"
    SUCCESS = "success"
    INFO = "info"
    UNKNOWN = "unknow"

class PopUpCV2:

    SETTINGS_GLOBAL = None
    SETTINGS_LEVEL = None

    def __init__(self,_type,_title,_content):
        self.type = _type
        self.title = _title
        self.content = _content
        
        self.config_level = PopUpCV2.SETTINGS_LEVEL[_type]
        self.config_colors = self.config_level["colors"]
        self.config_icon = self.config_level["icon"]
        self.config_bpm = self.config_level["bpm"]

        self.color_bg = self.config_colors["background"]
        self.update_alpha_bg()
        
        self.set_bpm()

    @staticmethod
    def LOAD_CONFIG(path_json,path_folder_icon):
        config = None
        with open(path_json) as json_file:
             config = json.load(json_file)

        PopUpCV2.SETTINGS_GLOBAL = config["global_settings"]
        PopUpCV2.SETTINGS_LEVEL = config["level_settings"]
        PopUpCV2.SETTINGS_GLOBAL_PATH_ICON = path_folder_icon 

    def CREATE_LABEL(image,content,font_size,rgb,position):
        cv2.putText(image,content, 
                    position, 
                    3, 
                    font_size,
                    rgb)
        #return label 
        
    def CREATE_IMAGE(path_img,width=None,height=None):
        image = cv2.imread(path_img)
        if(width != None and height != None):
            size = (width,height)
            image = cv2.resize(image,size)
        return image 

    def CREATE_FRAME(rgb,height,width):
        image = np.zeros((height,width,3), np.uint8)
        for y in range(height):
            for x in range(width):
                image[y,x] = rgb 

        #rgba = cv2.cvtColor(image, cv2.COLOR_RGB2RGBA)
        return image 

    def set_color_bg(self,rgb):
        self.color_bg = rgb

    def set_bpm(self):
        self.bpm = Bpm(self.config_bpm["min"],self.config_bpm["max"],self.config_bpm["freq"])
        self.bpm_current = self.bpm.get_max()
        self.bpm_sign = -1 

    def update_alpha_bg(self,alpha=255):
        colors = copy.copy(self.config_colors["background"])
        for i in range(len(colors)):
            colors[i] *= float(alpha)/255        
        self.color_bg = colors 


    def generate(self):

        layout_horizontal = LayoutHorizontal()
        layout_horizontal.set_color_bg(self.color_bg)

        icon = ViewImage(os.path.join(PopUpCV2.SETTINGS_GLOBAL_PATH_ICON,self.config_icon))
        icon_size = (PopUpCV2.SETTINGS_GLOBAL["image_size"]["width"],PopUpCV2.SETTINGS_GLOBAL["image_size"]["height"])
        icon.set_size(icon_size)

        layout_horizontal.add(icon)

        layout_vertical = LayoutVertical()

        title = ViewLabel(self.title)
        title.set_font_size(PopUpCV2.SETTINGS_GLOBAL["font_size"]["title"])
        title.set_font_color(self.config_colors["label_title"])
        layout_vertical.add(title)
    
        subtitle = ViewLabel(self.content)
        subtitle.set_font_size(PopUpCV2.SETTINGS_GLOBAL["font_size"]["subtitle"])
        subtitle.set_font_color(self.config_colors["label_subtitle"])
        layout_vertical.add(subtitle)

        layout_horizontal.add(layout_vertical)
        self.image = layout_horizontal.generate()

        return self.image 



    def callback_bg(self):
        if(self.bpm_current >= self.bpm.get_max()):
            self.bpm_sign = -1*self.config_level["bpm"]["step"]
        elif(self.bpm_current <= self.bpm.get_min()):
            self.bpm_sign = self.config_level["bpm"]["step"]
        
        self.bpm_current += self.bpm_sign
        self.update_alpha_bg(self.bpm_current)

 
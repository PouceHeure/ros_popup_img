#!/usr/bin/env python2.7

import os   
from modules.popup_cv2 import *  


from cv_bridge import CvBridge
from sensor_msgs.msg import Image
import rospy
from ros_popup_img.msg import PopUp



class PopUpROS:


    LEVEL_WARNING = 4
    LEVEL_FAIL = 3
    LEVEL_SUCCESS = 2
    LEVEL_INFO = 1

    def __init__(self,_topic_name_sub,_topic_name_pub):
        self.topic_name_sub = _topic_name_sub
        self.topic_name_pub = _topic_name_pub
        self.popup = None 
        self.br = CvBridge()


    def _decrypt_level(self,level_int):
        level = LevelPopUp.UNKNOWN 
        if(level_int == PopUpROS.LEVEL_WARNING):
            level = LevelPopUp.WARNING
        elif(level_int == PopUpROS.LEVEL_FAIL):
            level = LevelPopUp.FAIL
        elif(level_int == PopUpROS.LEVEL_SUCCESS):
            level = LevelPopUp.SUCCESS
        elif(level_int == PopUpROS.LEVEL_INFO):
            level = LevelPopUp.INFO
        return level 
            

    def callback(self,data):
        content_level = self._decrypt_level(data.level)
        content_title = data.title 
        content_subtitle = data.subtitle
        self.popup = PopUpCV2(content_level,content_title,content_subtitle)

    def run(self):
        sub = rospy.Subscriber(self.topic_name_sub,PopUp,self.callback)
        pub = rospy.Publisher(self.topic_name_pub, Image, queue_size=10)
        while not rospy.is_shutdown():
            if(self.popup != None):
                image = self.popup.generate() # generate image 
                pub.publish(self.br.cv2_to_imgmsg(image,encoding="bgr8"))
                self.popup.callback_bg()
            rospy.Rate(1)
    


    


if __name__=="__main__":
    rospy.init_node("generator_node", anonymous=True)

    # setup the current path 
    current_path_file = os.path.dirname(os.path.realpath(__file__))

    # setup path files 
    config_path_file = os.path.join(current_path_file,"./config/layout.json")
    icon_path_folder = os.path.join(current_path_file,"./img/icon/")
    
    # load config 
    PopUpCV2.LOAD_CONFIG(config_path_file,icon_path_folder)
 
    p = PopUpROS("image_sub","image_pub")
    p.run()


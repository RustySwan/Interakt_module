# -*- coding: utf-8 -*-
from lib import *
from naoqi import ALProxy
import socket


class Interakt:

    def __init__(self,IP, port,config_file,tag_file):
        
        self.config_file = config_file
        self.tag_file = tag_file

        try:
            socket.inet_aton(IP)
        except socket.error, e:
            print "Ip is not numeric"
            print "Error was: ", e  
            return

        try:
            self.posture_proxy = ALProxy("ALRobotPosture", IP, port)
        except Exception, e:
            print "Could not create proxy to ALRobotPosture"
            print "Error was: ", e
            return

        try:
           self.tts_proxy = ALProxy("ALTextToSpeech", IP, port)
        except Exception, e:
           print "Could not create proxy to ALTextToSpeech"
           print "Error was: ", e
           return

        try:
           self.animated_speech_proxy = ALProxy("ALAnimatedSpeech", IP, port)
        except Exception, e:
           print "Could not create proxy to ALAnimatedSpeech"
           print "Error was: ", e
           return

    def speech(self,sentence,mode):

        if isinstance(sentence, basestring) == True:
            pass
        else:
            return

        self.sentence = sentence
        if mode == 0:
            self.tts_proxy.say(sentence)
            print('Said(tts):'+sentence)
            return 0
        
        self.divided = divide_text(self.sentence)
        self.annotated = str()
        self.posture = self.posture_proxy.getPostureFamily()
        self.posture_ID = 1

        if self.posture == 'Standing':
            self.posture_ID = 0
        else:
            self.posture_ID = 1

        for i in self.divided:
            if instance_tag(i) != False:
                self.annotated = self.annotated + embed_tag(self.config_file, instance_tag(i),i,self.posture_ID)
            else:
                if find_tag(i,'tags.json') == '':
                    if mode == 2:
                        self.annotated = self.annotated + embed_tag('config.json','#discuss',i,0)
                    else:
                        self.annotated = self.annotated + i
                else:
                    self.annotated = self.annotated + embed_tag('config.json',find_tag(i,'tags.json'),i,self.posture_ID)   

        self.animated_speech_proxy.say(self.annotated)
        print(self.annotated)
        return 0


#m = Interakt('127.0.0.1',54120,'config.json','tags.json')
#m.speech('Ahoj, ako sa máš?',1)

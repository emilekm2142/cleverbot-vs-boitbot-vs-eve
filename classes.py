from selenium import webdriver
from time import sleep
import re
import os 
from random import choice
class IBot():
     def open( self ):
        raise NotImplementedError( "Should have implemented this" )
     def send_message( self ):
        raise NotImplementedError( "Should have implemented this" )

     def close(self):
        raise NotImplementedError( "Should have implemented this" )
class Conversation:
    def __init__(self,bot1,bot2):
        self.bot1=bot1
        self.bot2=bot2
        print("start")

        self.history = []
    def start(self,lenght, attitude="neutral", start="random"):
        #attitude not implemented yet,
        #start = "random" means that at the beginning of conversation bot1 will click button "think for me"

        self.bot1.open()
        self.bot2.open()
        #start
        if start=="random":
            ans = self.bot1.click_think_for_me()
            self.history.append(Message(ans,"1"))
        else:
            sleep(5)
            self.history.append(Message(start,"0"))
            ans = self.bot1.send_message(start)
            self.history.append(Message(ans,"1"))
        for i in range(lenght):
            ans2 = self.bot2.send_message(ans)
            print(ans2)
            self.history.append(Message(ans2,"2"))
            ans=self.bot1.send_message(ans2)
            print(ans)
            self.history.append(Message(ans,"1"))
    def end(self):
        self.bot1.browser.close()
        self.bot2.browser.close()

    def save_history_to_file(self,filename):
        with open(filename,'w', encoding='utf-8') as f:
            for n in self.history:
                f.write("{0}: {1}\n".format(n.side, n.msg))
    def change_language(self,lang):
        self.bot1.change_language("pl")
        self.bot2.change_laguage("pl")



class CleverBot(IBot):
    def __init__(self):
        pass
    def open(self):
        self.browser = webdriver.Chrome("chromedriver.exe")
        self.browser.get('http://cleverbot.com')
        sleep(3)
        self.input_box=self.browser.find_element_by_name("stimulus")
        self.send_button=self.browser.find_element_by_name("thinkaboutitbutton")
        self.form = self.browser.find_element_by_id("avatarform")
        self.conv = self.browser.find_element_by_id("conversationcontainer")
        self.think_for_me_button= self.browser.find_element_by_name("thinkformebutton")
        self.change_language("pl")
    #returns answer
    def send_message(self, message)->str:
        self.input_box.send_keys(message)
        self.send_button.click()
        last_lenght=0
        while self.form.get_attribute("class")=="inprogress":
            sleep(0.5)
        while True:
            sleep(0.5)
            answerTag=self.conv.find_element_by_id("line1")
            answerSpan = answerTag.get_attribute("innerHTML")
            if len(answerSpan)==last_lenght: break
            else: last_lenght=len(answerSpan)
        a = re.match('<span class="bot">(.+?)<\/span>', answerSpan).group(1)
        #a is answer in plain text
        return a
    #return random topic
    def change_language(self,lang="pl"):
        self.browser.execute_script('cleverbot.trackInGoogle("cb_asr_change_language");cleverbot.asr.setlanguage("{0}",0)'.format(lang))
    def click_think_for_me(self, lang="pl")->str:
        if lang!="en":
            self.browser.execute_script('cleverbot.trackInGoogle("cb_asr_change_language");cleverbot.asr.setlanguage("{0}",0)'.format(lang))
        self.think_for_me_button.click()
        last_lenght=0
        while self.form.get_attribute("class")=="inprogress":
            sleep(0.5)
        while True:
            sleep(0.5)
            answerTag=self.conv.find_element_by_id("line1")
            answerSpan = answerTag.get_attribute("innerHTML")
            if len(answerSpan)==last_lenght: break
            else: last_lenght=len(answerSpan)

        a = re.match('<span class="bot">(.+?)<\/span>', answerSpan).group(1)
        a = re.sub("<img.+",'',a)
        return a
    def close(self):
        self.browser.close()
class Existor(IBot):
    def __init__(self, mode):
        self.mode=mode
    def open(self):
        self.browser = webdriver.Chrome("chromedriver.exe")
        if self.mode=="Evie" or self.mode == "evie":
            self.browser.get('https://www.eviebot.com/')
        else :
            self.browser.get('https://www.boibot.com/')
        sleep(3)
        self.input_box=self.browser.find_element_by_name("stimulus")
        self.send_button=self.browser.find_element_by_name("sayitbutton")
        self.form = self.browser.find_element_by_id("avatarform")
        self.conv = self.browser.find_element_by_id("conversationcontainer")
        self.change_language("pl")
    #returns answer
    def send_message(self, message)->str:
        self.input_box.send_keys(message)
        while True:
            try:
                self.send_button.click()
            except:
                pass
            else:
                break

        last_lenght=0
        while self.form.get_attribute("class")=="inprogress":
            sleep(0.5)
        while True:
            sleep(0.5)
            answerTag=self.conv.find_element_by_id("line1")
            answerSpan = answerTag.get_attribute("innerHTML")
            if len(answerSpan)==last_lenght: break
            else: last_lenght=len(answerSpan)
        a = re.match('<span class="bot">(.+?)<\/span>', answerSpan).group(1)
        a = re.sub("<img.+",'',a)
        print(a)
        #a is answer in plain text
        return a
    #return random topic
    def change_language(self,lang):
        self.browser.execute_script('cleverbot.trackInGoogle("cb_asr_change_language");cleverbot.asr.setlanguage("{0}",0)'.format(lang))
    def close(self):
        self.browser.close()


class Message:
    def __init__(self, msg, side):
        self.msg=msg
        self.side=side

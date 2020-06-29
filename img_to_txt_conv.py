from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os
import sys
import time
import codecs


class Img_to_Text:
    def __init__(self,url,input_path,output_path,driver_path):
        self.data = []
        self.url = url
        self.input_path = input_path
        self.output_path = output_path
        self.input_files = os.listdir(self.input_path)
        driver_path = driver_path
        options  = Options()
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        self.driver = webdriver.Chrome(driver_path)
        self.driver.maximize_window()
        self.execute_main()

    def execute_main(self):
        if self.input_files:
            for each_file in self.input_files:
                self.file_path = self.input_path + each_file
                self.execute()
            print("\n Completed Converting the Input files")
            print("\n Output is present at {}".format(self.output_path))
            self.driver.close()
        else:
            print("\n No Input files to Execute")
            sys.exit(1)

    def execute(self):
        try:
            print("\n Starting the driver")
            print("\n Getting the website")
            self.url = self.url
            self.driver.get(self.url)
            time.sleep(5)
            self.driver.find_element_by_xpath("//*[@id='scrollstart']/div[1]/div[1]/div[4]/button[2]").click()
            time.sleep(5)
            up = self.driver.find_element_by_xpath("//*[@id='scrollstart']/div[1]/div[1]/div[4]/span/div/div[1]/i/input")
            up.send_keys(self.file_path)
            print("\n Uploaded the Input file",self.file_path)
            self.driver.find_element_by_xpath("//*[@id='scrollstart']/div[1]/div[1]/div[4]/span/button").click()
            self.driver.find_element_by_xpath("//*[@id='scrollstart']/div[1]/div[3]/div[1]/div/div[2]/div/div").click()
            self.driver.find_element_by_xpath("/html/body/div[4]/div[1]/div[2]/div/input").send_keys("Telugu")
            self.driver.find_element_by_xpath("/html/body/div[4]/div[2]/div/div/div").click()
            time.sleep(5)
            conv_txt = self.driver.find_element_by_xpath('//*[@id="scrollstart"]/div[1]/div[3]/div[2]/span')
            self.data = [conv_txt.text]
            self.write_output()
        except Exception as e:
            print("Exception Occured during Browser activity",e)
            self.driver.close()

    def write_output(self):
        try:
            print("\n Writing Converted Text to output file")
            op = codecs.open(self.output_path + "output_text.txt","a","utf-8")
            for each_content in self.data:
                op.write("\n ---------------------------------------------------------------")
                op.write("\nConverted text from {}".format(self.file_path))
                op.write("\n" + u'{}'.format(each_content))
                op.write("\n ---------------------------------------------------------------")
            op.close()
        except Exception as e:
            print("Exception Occured during Writing the Output to file",e)
            self.driver.close()


if __name__ == '__main__':
    """ Initializing Variables"""
    url = "http://aksharamukha.appspot.com/converter"
    input_path = "C:\\Users\\kvsla\\Documents\\Input\\"
    output_path = "C:\\Users\\kvsla\\Documents\\Output\\"
    driver_path = "C:\\Users\\kvsla\\Documents\\chromedriver_win32\\chromedriver.exe"
    obj = Img_to_Text(url,input_path,output_path,driver_path)

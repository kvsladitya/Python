from pdf2image import convert_from_path
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from wand.image import Image
import os
import time
import codecs
import pdb


class Pdf_to_txt:
    def __init__(self,filedir,output_path,poppler_path,driver_path,url):
        self.filedir = filedir
        self.output_path = output_path
        self.poppler_path = poppler_path
        self.driver_path = driver_path
        self.url = url
        options  = Options()
        options.headless  = True
        self.driver = webdriver.Chrome(driver_path,options=options)
        # self.driver.maximize_window()
        # self.driver.minimize_window()
        self.main_flow()

    def main_flow(self):

        for self.each_file in sorted(os.listdir(self.filedir)):
            if self.each_file.endswith("pdf"):
                final_path = self.output_path + self.each_file.split(".")[0] + "\\"
                if os.path.isdir(final_path):
                    pass
                else:
                    os.mkdir(final_path)
                final_input_path = self.filedir + self.each_file
                # pages = convert_from_path(final_input_path, poppler_path=self.poppler_path, output_file=final_path)
                # for number,page in enumerate(pages):
                #     page.save(final_path + "{}.jpeg".format(number), 'JPEG')
                #     print("\n Saving converted image ---->" + final_path + "{}.jpeg".format(number))
                pages = Image(filename=final_input_path, resolution=150)
                for number, page in enumerate(pages.sequence):
                    with Image(page)as img:
                        img.save(filename=final_path + "{}.jpeg".format(number))
                        print("\n Saving converted image ---->" + final_path + "{}.jpeg".format(number))
        self.execute_main()

    def execute_main(self):
        temp = []
        for self.each_file in sorted(os.listdir(self.output_path)):
            for each_sub in sorted(os.listdir(self.output_path + self.each_file)):
                temp.append(int(each_sub.split(".")[0]))
                temp = sorted(temp)
            for self.each_file in sorted(os.listdir(self.output_path)):
                for index,each_sub in enumerate(os.listdir(self.output_path + self.each_file)):
                    final_path = self.output_path + self.each_file +"\\"+str(temp[index]) + ".jpeg"
                    # pdb.set_trace()
                    self.execute(final_path)
        print("\n Completed Converting the Input files")
        print("\n Output is present at {}".format(self.output_path))
        self.driver.close()

    def execute(self,final_path):
        try:

            print("\n Starting the driver")
            print("\n Getting the website")
            self.driver.get(self.url)
            time.sleep(2)
            fileinput = self.driver.find_element_by_xpath('//*[@id="scrollstart"]/div[1]/div[1]/div[4]/span')
            self.driver.execute_script('arguments[0].style = ""; arguments[0].style.display = "block"; arguments[0].style.visibility = "visible";',fileinput)
            up = self.driver.find_element_by_xpath("//*[@id='scrollstart']/div[1]/div[1]/div[4]/span/div/div[1]/i/input")
            up.send_keys(final_path)
            print("\n Uploaded the Input file", final_path)
            self.driver.find_element_by_xpath("//*[@id='scrollstart']/div[1]/div[1]/div[4]/span/button").click()
            time.sleep(2)
            self.driver.find_element_by_xpath("//*[@id='scrollstart']/div[1]/div[3]/div[1]/div/i").click()
            time.sleep(3)
            lang = self.driver.find_element_by_xpath("/html/body/div[4]/div[1]/div[2]/div/input")
            lang.send_keys("Telugu")
            time.sleep(2)
            self.driver.find_element_by_xpath("/html/body/div[4]/div[2]/div").click()
            time.sleep(2)
            conv_txt = self.driver.find_element_by_xpath('//*[@id="scrollstart"]/div[1]/div[3]/div[2]/span')
            self.data = [conv_txt.text]
            if self.data:
                self.write_output(final_path)
        except Exception as e:
            print("Exception Occured during Browser activity", e)
            self.driver.close()

    def write_output(self,final_path):
        try:
            print("\n Writing Converted Text to output file")
            op = codecs.open(self.output_path +("{}.txt".format(self.each_file)) ,"a","utf-8")
            for each_content in self.data:
                op.write("\n ---------------------------------------------------------------")
                op.write("\nConverted text from {}".format(self.each_file))
                op.write("\n" + u'{}'.format(each_content))
                op.write("\n ---------------------------------------------------------------")
            op.close()
        except Exception as e:
            print("Exception Occured during Writing the Output to file",e)
            self.driver.close()


if __name__ == '__main__':
    file_dir = "C:\\Users\\kvsla\\Documents\\Input\\"
    output_path = 'C:\\Users\\kvsla\\Documents\\Output\\'
    poppler_path="D:\\Softwares\\poppler-0.68.0\\bin"
    url = "http://aksharamukha.appspot.com/converter"
    driver_path = "C:\\Users\\kvsla\\Documents\\chromedriver_win32\\chromedriver.exe"
    obj = Pdf_to_txt(file_dir,output_path,poppler_path,driver_path,url)




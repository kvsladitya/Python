from pdf2image import convert_from_path
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from wand.image import Image
import os
import time
import codecs
import sys


class Pdf_to_txt:
    def __init__(self,filedir,output_path,driver_path,url,mode="N"):
        self.filedir = filedir
        self.output_path = output_path
        self.driver_path = driver_path
        self.url = url
        if mode == "N":
            self.driver = webdriver.Chrome(executable_path=driver_path)
            self.driver.maximize_window()
            # self.driver.minimize_window()
        elif mode == "H":
            options  = Options()
            options.headless  = True
            self.driver = webdriver.Chrome(executable_path=self.driver_path,options=options)

    def pdf_to_img_splitter(self):
        for self.each_file in sorted(os.listdir(self.filedir)):
            if self.each_file.endswith("pdf"):
                self.final_path = self.output_path + self.each_file.split(".")[0] + "\\"
                if os.path.isdir(self.final_path):
                    pass
                else:
                    os.mkdir(self.final_path)
                final_input_path = self.filedir + self.each_file
                pages = Image(filename=final_input_path, resolution=150)
                for number, page in enumerate(pages.sequence):
                    with Image(page)as img:
                        img.save(filename=self.final_path + "{}.jpeg".format(number))
                        print("\n Saving converted image ---->" + self.final_path + "{}.jpeg".format(number))
        print(("\n Completed Converting PDF - {} to Images ").format(self.filedir))

    def img_to_text_converter(self):
        temp = []
        self.temp_count = 0
        for self.each_file in sorted(os.listdir(self.output_path)):
            for each_sub in sorted(os.listdir(self.output_path + self.each_file)):
                if each_sub.endswith(".jpeg"):
                    if int(each_sub.split(".")[0]) not in temp:
                        temp.append(int(each_sub.split(".")[0]))
                    temp = sorted(temp)
        start = time.time()
        for self.each_file in sorted(os.listdir(self.output_path)):
            for index,each_sub in enumerate(os.listdir(self.output_path + self.each_file)):
                self.final_path = self.output_path + self.each_file +"\\"+str(temp[index]) + ".jpeg"
                # print(self.final_path)
                self.driver.get(self.url)
                self.selenium_script()
        end = time.time()
        hours, rem = divmod(end - start, 3600)
        minutes, seconds = divmod(rem, 60)
        print("Selenium Script took total of {:0>2}:{:0>2}:{:05.2f} to execute".format(int(hours), int(minutes),seconds))
        print("\n Completed Converting the Input files")
        print("\n Output is present at {}".format(self.output_path))
        self.driver.close()

    def selenium_script(self):
        start = time.time()
        try:
            print("\n Started Selenium Script")
            if self.temp_count == 0:
                time.sleep(6)
            fileinput = self.driver.find_element_by_xpath('//*[@id="scrollstart"]/div[1]/div[1]/div[4]/span')
            self.driver.execute_script('arguments[0].style = ""; arguments[0].style.display = "block"; arguments[0].style.visibility = "visible";',fileinput)
            upload_btn = self.driver.find_element_by_xpath("//*[@id='scrollstart']/div[1]/div[1]/div[4]/span/div/div[1]/i/input")
            upload_btn.send_keys(self.final_path)
            print("\n Uploaded the Input file",self.final_path)
            if self.temp_count == 0:
                lang_btn = WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable((By.XPATH,"//*[@id='scrollstart']/div[1]/div[3]/div[1]/div/div[2]/div/div")))
                lang_btn.click()
                lang = self.driver.find_element_by_xpath("/html/body/div[4]/div[1]/div[2]/div/input")
                lang.send_keys("Telugu")
                time.sleep(4)
                self.driver.find_element_by_xpath("/html/body/div[4]/div[2]/div").click()
                self.temp_count = self.temp_count + 1
            convert_button = self.driver.find_element_by_xpath("//*[@id='scrollstart']/div[1]/div[1]/div[4]/span/button")
            convert_button.click()
            time.sleep(6)
            conv_txt = WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="scrollstart"]/div[1]/div[3]/div[2]/span')))
            self.data = [conv_txt.text]
            if self.data:
                self.text_to_filewrite()
            end = time.time()
            hours, rem = divmod(end - self.start, 3600)
            minutes, seconds = divmod(rem, 60)
            print("Selenium Function block took {:0>2}:{:0>2}:{:05.2f} to execute".format(int(hours), int(minutes),
                                                                                          seconds))
        except Exception as e:
            print("Exception Occured during Browser activity", e)
            count = 0
            if count <=2:
                self.driver.get(self.url)
                self.selenium_script()
                count = count + 1

    def text_to_filewrite(self):

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


def main():
    file_dir = "D:\\Input\\"
    output_path = 'D:\\Output\\'
    url = "http://aksharamukha.appspot.com/converter"
    driver_path = "D:\\Softwares\\chromedriver_win32\\chromedriver.exe"
    print("\n ======= Welcome to PDF to Text Converter =======")
    print("\n         1: PDF to Image ")
    print("\n         2: Image to Text")
    print("\n         3: PDF to Text  ")
    print("\n         4: Quit         ")
    print("\n ================================================")
    print("\n Please Enter any option from( 1 - 4 )")
    opt = int(input("\n"))
    if not opt and opt > 4:
        main()
    elif opt == 1:
        obj = Pdf_to_txt(file_dir, output_path, driver_path,url)
        obj.pdf_to_img_splitter()
    elif opt == 2:
        print("\n Do you want the Script to run in Normal mode or Headless mode ? ")
        print("\n Enter 'N' for Normal mode or 'H' for Headless mode")
        mode = input("\n")
        obj = Pdf_to_txt(file_dir, output_path, driver_path, url,mode)
        obj.img_to_text_converter()

    elif opt == 3:
        print("\n Do you want the Script to run in Normal mode or Headless mode ? ")
        print("\n Enter 'N' for Normal mode or 'H' for Headless mode")
        mode = input("\n")
        obj = Pdf_to_txt(file_dir, output_path, driver_path, url,mode)
        obj.pdf_to_img_splitter()
        obj.img_to_text_converter()
        print()
    else:
        print("\n Thank You for using this tool")
        sys.exit(0)


if __name__ == '__main__':
    main()





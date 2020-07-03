import os,io,sys,time,codecs
from wand.image import Image
from google.cloud import vision
from indic_transliteration import sanscript
from indic_transliteration.sanscript import transliterate


class Pdf_to_txt:
    def __init__(self,filedir,output_path,client):
        self.filedir = filedir
        self.output_path = output_path
        self.client = client

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
                self.google_api()
        end = time.time()
        hours, rem = divmod(end - start, 3600)
        minutes, seconds = divmod(rem, 60)
        print("Google API took total of {:0>2}:{:0>2}:{:05.2f} to execute".format(int(hours), int(minutes),seconds))
        print("\n Completed Converting the Input files")
        print("\n Output is present at {}".format(self.output_path))

    def google_api(self):
        with io.open(self.final_path, 'rb') as image_file:
            content = image_file.read()
        image = vision.types.Image(content=content)
        response = self.client.text_detection(image=image)
        texts = response.text_annotations
        # print("Texts:")
        temp = ""
        for index, text in enumerate(texts):
            if index == 0:
                print(text.description)
                temp = text.description
        # inp = detect(temp)
        # print(transliterate(temp, inp))
        self.data = [transliterate(temp, sanscript.DEVANAGARI,sanscript.TELUGU)]
        if self.data:
            self.text_to_filewrite()

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
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "D:/Google Tokens/ServiceAccessToken.json"
    client = vision.ImageAnnotatorClient()
    print("\n ======= Welcome to PDF to Text Converter =======")
    print("\n         1: PDF to Image ")
    print("\n         2: Image to Text")
    print("\n         3: PDF to Text  ")
    print("\n         4: Quit         ")
    print("\n ================================================")
    print("\n Please Enter any option from( 1 - 4 )")
    opt = int(input("\n"))
    obj = Pdf_to_txt(file_dir, output_path,client)
    if not opt and opt > 4:
        main()
    elif opt == 1:
        obj.pdf_to_img_splitter()
    elif opt == 2:
        obj.img_to_text_converter()
    elif opt == 3:
        obj.pdf_to_img_splitter()
        obj.img_to_text_converter()
        print()
    else:
        print("\n Thank You for using this tool")
        sys.exit(0)


if __name__ == '__main__':
    main()





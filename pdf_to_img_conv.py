import os
from pdf2image import convert_from_path


class Pdf_to_img:
    def __init__(self,filepath,output_path,poppler_path):
        self.filepath = filepath
        self.output_path = output_path
        self.poppler_path = poppler_path
        self.main_flow()

    def main_flow(self):
        for self.each_file in os.listdir(self.filepath):
            if self.each_file.endswith("pdf"):
                pages = convert_from_path(self.filepath + self.each_file, poppler_path=self.poppler_path, output_file=self.output_path)
                for number,page in enumerate(pages):
                    page.save(self.output_path + "{}-{}.jpeg".format(self.each_file.split(".")[0],number), 'JPEG')
                    print("\n Saving converted image ---->" + self.output_path + "{} - {}.jpeg".format(self.each_file.split(".")[0],number))


if __name__ == '__main__':
    filepath = 'C:\\Users\\kvsla\\Downloads\\'
    output_path = 'C:\\Users\\kvsla\\Documents\\pdf_output\\'
    poppler_path="D:\\Softwares\\poppler-0.68.0\\bin"
    obj = Pdf_to_img(filepath,output_path,poppler_path)

import pdfplumber
import codecs
import os


class Pdf_to_text:
    def __init__(self,filepath,output_path):
        self.filepath = filepath
        self.output_path = output_path
        self.data = []
        self.main_flow()

    def main_flow(self):
        for self.each_file in os.listdir(self.filepath):
            if self.each_file.endswith("pdf"):
                with pdfplumber.open(self.filepath + self.each_file) as pdf:
                    for each_page in pdf.pages:
                        data = (each_page.extract_text())
                        print("\n Writing Converted Text to output file")
                        op = codecs.open(self.output_path + "{}.txt".format(self.each_file), "a", "utf-8")
                        op.write("\n ---------------------------------------------------------------")
                        op.write("\nConverted text from {}".format(self.each_file))
                        op.write("\n" + u'{}'.format(data))
                        op.write("\n ---------------------------------------------------------------")
                        op.close()
                        print("\n Saving converted text ---->" + self.output_path + self.each_file)
                    print("\n Completed extracting text from {}".format(self.each_file))


if __name__ == '__main__':
    filepath = 'C:\\Users\\kvsla\\Downloads\\'
    output_path = 'C:\\Users\\kvsla\\Documents\\pdf_output\\text_output\\'
    obj = Pdf_to_text(filepath,output_path)
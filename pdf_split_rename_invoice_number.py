import os
import shutil
import tkinter as tk
from datetime import datetime
from tkinter import filedialog
from PyPDF2 import PdfFileWriter, PdfFileReader
import lxml.html
import pdfquery


def get_digit_count(number):
    count = 0
    while number > 0:
        number = number // 10
        count += 1
    return count


def get_count_files_in_folder(path):
    return len([name for name in os.listdir(path) if os.path.isfile(name)])


def get_list_files_in_folder(path):
    temp_list = []
    with os.scandir(path) as listOfEntries:
        for entry in listOfEntries:
            if entry.is_file() and entry.name.endswith(""):
                temp_list.append(entry.name)
    return temp_list


def split_pdf_pages(inputpdf: str, output_folder: str):
    inputpdf = PdfFileReader(open(inputpdf, 'rb'))
    fmt = get_digit_count(inputpdf.numPages)
    for i in range(inputpdf.numPages):
        output = PdfFileWriter()
        output.addPage(inputpdf.getPage(i))
        with open(output_folder + '/document-page%s.pdf' % str(i).zfill(fmt), 'wb') as outputStream:
            output.write(outputStream)


def pdf_to_xml(pdf_file_path):
    pdf = pdfquery.PDFQuery(pdf_file_path)
    pdf.load()
    strval = str(pdf.get_pyquery(None, page_numbers=[0]))
    pdf.file.close()
    return strval


def get_pdf_invoice_number(pdf_file_path):
    html = lxml.html.document_fromstring(pdf_to_xml(pdf_file_path))
    nodes = html.xpath('/html/body/pdfxml/ltpage/ltrect[1]/lttextlinehorizontal[7]/lttextboxhorizontal/ text()')
    txt = nodes[0].strip()
    # terscevir 14 karakter al sonra tekrar ters cevir temizle gonder
    return str(int(txt[::-1][:14][::-1].strip().replace('-', '')))


def pdf_files_rename(path, master):
    x = 0
    y = len(get_list_files_in_folder(path))
    for xname in get_list_files_in_folder(path):
        srcname = path + os.sep + xname
        desname = path + os.sep + get_pdf_invoice_number(path + '\\' + xname) + '.pdf'
        x += 1
        master.title(' ' + str(x) + '/' + str(y))
        master.update_idletasks()
        os.rename(srcname, desname)
        master.update_idletasks()


class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.with_of_window = 400
        self.height_of_window = 300
        self.screen_with = master.winfo_screenwidth()
        self.screen_height = master.winfo_screenheight()
        self.x_coordinate = (self.screen_with / 2) - (self.with_of_window / 2)
        self.y_coordinate = (self.screen_height / 2) - (self.height_of_window / 2)
        self.pdf_file = ''
        self.dir_path = ''
        self.folder_name = ''
        self.master.geometry(
            '%dx%d+%d+%d' % (self.with_of_window, self.height_of_window, self.x_coordinate, self.y_coordinate))
        self.master.title('Pdf Spliter')
        self.master.resizable(width=False, height=False)
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        self.btn_pdf_sec = tk.Button(self)
        self.btn_pdf_sec["text"] = "Pdf Dosyası Seçmek İçin\n(Tıklayınız)"
        self.btn_pdf_sec["command"] = self.select_pdf_file
        self.btn_pdf_sec.pack(side="top")

        self.quit = tk.Button(self, text="Çıkış", fg="red",
                              command=self.master.destroy)
        self.quit.pack(side="bottom")

    def select_pdf_file(self):
        self.pdf_file = filedialog.askopenfilename(initialdir='', title="Select pdf file ",
                                                   filetypes=(('', "*.pdf"),))
        if self.pdf_file.strip() == '':
            exit(1)
        self.btn_pdf_sec['text'] = 'Lütfen Bekleyiniz\n'
        self.btn_pdf_sec.update_idletasks()
        self.dir_path = os.path.dirname(os.path.realpath(self.pdf_file))
        self.folder_name = datetime.now().strftime("%Y-%m-%d-%H%M%S")
        out_folder = self.dir_path + os.sep + self.folder_name
        if os.path.isdir(out_folder):
            shutil.rmtree(out_folder, ignore_errors=True)
            os.mkdir(out_folder)
        else:
            os.mkdir(out_folder)

        split_pdf_pages(self.pdf_file, out_folder)
        pdf_files_rename(out_folder, self.master)
        self.btn_pdf_sec['text'] = 'İşlem Tamamlandı\n'


root = tk.Tk()

app = Application(master=root)
app.mainloop()

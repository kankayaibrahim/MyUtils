import codecs
import os


def get_count_files_in_folder(folder_path: str) -> int:
    return len([name for name in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, name))])


def get_list_files_in_folder(path):
    temp_list = []
    with os.scandir(path) as listOfEntries:
        for entry in listOfEntries:
            if entry.is_file() and entry.name.endswith(""):
                temp_list.append(entry.name)
    return temp_list


def change_encoding_file(inp_fname: str, outp_fname: str, src_enc: str, des_enc: str):
    with codecs.open(inp_fname, 'r', encoding=src_enc) as file:
        lines = file.read()

    with codecs.open(outp_fname, 'w', encoding=des_enc) as file:
        file.write(lines)

# cp1254
# utf8


def main():
    src_folder = r'C:\temp\train\1254_DATA'
    dst_folder = r'C:\temp\train\out2'
    tmp_cnt = get_count_files_in_folder(src_folder)
    cnt = 0
    if not os.path.exists(dst_folder):
        os.makedirs(dst_folder)
    mylist = get_list_files_in_folder(src_folder)
    for ls in mylist:
        inp = src_folder+os.sep+ls
        out = dst_folder+os.sep+ls
        change_encoding_file(inp, out, 'cp1254', 'utf8')
        cnt += 1
        print('\rEncodinc devam ediyor : '+str(cnt)+' / '+str(tmp_cnt) +' işlemdeki dosya: '+inp, end='', flush=True)
    print('\nİşlem tamamlandı kontrol ediniz.')            


if __name__ == "__main__":
    main()

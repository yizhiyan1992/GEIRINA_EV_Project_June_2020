import os
import zipfile

def file2zip(zip_file_name,file_path,file_names):
    with zipfile.ZipFile(zip_file_name,mode='w',compression=zipfile.ZIP_DEFLATED) as zf:
        for name in file_names:
            zf.write(file_path+name,arcname=name)
    print('files are zipped!')
    return

def main():
    zip_name=r'C:/Users/Zhiyan/Desktop/zip_test.zip'
    file_path=r'C:/Users/Zhiyan/Desktop/Crawl_record/'
    files=os.listdir(file_path)
    file2zip(zip_name,file_path,files)

if __name__=='__main__':
    main()

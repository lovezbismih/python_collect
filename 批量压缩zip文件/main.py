import os
import os.path as osp
import zipfile
import shutil
import glob
 
def extract_zip(zip_path, extract_dir):  
    with zipfile.ZipFile(zip_path, 'r') as zip_file:  
        # 首先确保提取目录存在  
        os.makedirs(extract_dir, exist_ok=True)
        zip_list = zip_file.namelist()  # 获取压缩文件中的文件路径列表
        old_dir = zip_list[0]  # 获取第一个文件的名称作为旧目录名称
        #print(old_dir)
        flag = False  # 设置标志变量，用于判断是否有重命名操作        
        # 遍历ZIP文件中的所有条目  
        for f in zip_list:  
            # 中文名称乱码解码  
            try:  
                new_name = f.encode('cp437').decode('gbk', errors='ignore')  
            except UnicodeDecodeError:  
                new_name = f
 
            if osp.exists(osp.join(extract_dir, new_name)):  # 如果文件已存在，则删除该文件或文件夹
                shutil.rmtree(osp.join(extract_dir, new_name))
            zip_file.extract(f, extract_dir)  # 将文件解压到指定工作目录
                               
            if f != new_name:  # 如果文件名与新名称不同，则进行重命名操作
                flag = True  # 设置标志变量为True
                if osp.exists(osp.join(extract_dir, new_name)):  #如果新名称的文件已存在，则删除该文件或文件夹
                    shutil.rmtree(osp.join(extract_dir, new_name))
                os.rename(osp.join(extract_dir, f), osp.join(extract_dir, new_name))  # 将文件重命名为新名称
 
        if flag:  # 如果进行了重命名操作
            if osp.exists(osp.join(extract_dir,old_dir)):  # 如果旧目录存在，则删除该目录
                shutil.rmtree(osp.join(extract_dir,old_dir))
 
if __name__ == '__main__':  
    data_dir = os.getcwd()  # 获取当前工作目录  
    zip_pathlist = glob.glob(osp.join(data_dir, '**', '*.zip'), recursive=True)  # 所有压缩文件的路径列表
    for zip_path in zip_pathlist:  
        # 为每个ZIP文件创建一个单独的目录来解压其内容  
        extract_dir = osp.basename(osp.join(data_dir, osp.splitext(osp.basename(zip_path))[0])) 
        extract_zip(zip_path, extract_dir)

import os
import zipfile
import sys
import shutil
import configparser
import json
from os.path import join

root_path = os.path.dirname(sys.argv[0])

def zipdir(path,src, ziph):
    # ziph is zipfile handle
    for root, dirs, files in os.walk(path):
        for file in files:
            if file != ".DS_Store":
                #print(root)
                #ziph.write(os.path.join(root, file),root)
                ziph.write(os.path.join(root, file), arcname=os.path.join(root.replace(path, "files"), file))
                _file,ext = file.split(".")
                #print(_file,ext)
        if len(dirs) != 0:
            src.append((root,dirs))

def clear_temp():
    src = join(root_path,"tmp")
    if os.path.exists(src):
        #print("tmp exist")
        shutil.rmtree(src)
        # for item in os.listdir(src):
        #     s = os.path.join(src, item)
        #     if os.path.isdir(s):
        #         shutil.rmtree(s)

def remove_cache_file(src):
    if os.path.exists(src):
        os.remove(src)
            

def create_temp_copy_files(src,dst,key):
    modules = {}
    #config = configparser.ConfigParser()
    

    if not os.path.exists(dst):
        os.makedirs(dst)
    for root, dirs, files in os.walk(src):
        #print("create_temp_copy_files",root,dirs,files)
        for file in files:
            #print("checking",root,"vs",join(src, key))
            if file != ".DS_Store" and root == join(src, key):
                
                #print("create_temp_copy_files",root,dirs,files)
                s = os.path.join(root, file)
                d = os.path.join(dst, file)
                if file == 'module.ini':
                    with open(s, 'r') as configfile:
                        #print(configfile.read())
                        _str = configfile.read()
                        #print(_str)
                        _list = json.loads(_str)
                        _key,_dict = _list
                        modules[_key] = _dict
                        configfile.close()
                else:
                    shutil.copy(s,d)

    # for item in os.listdir(src):
    #     s = os.path.join(src, item)
    #     d = os.path.join(dst, item)
    #     if os.path.isdir(s):
    #         shutil.copytree(s, d, False, None)
    
    #print(root_path)
    shutil.copy(join(root_path,"build_files/Setup.py"),join(root_path,"tmp/Setup.py"))
    shutil.copy(join(root_path,"build_files/files_list.py"),join(root_path,"tmp/files_list.py"))
    

    # ex_config = configparser.ConfigParser()
    # ex_config.read_dict(modules)
    #shutil.copy("./builds/compile_modules.ini","./tmp/compile_modules.txt")
    # with open(os.path.join("./tmp","compile_modules.ini"), 'w') as configfile:
    #     ex_config.write(configfile)
    #     configfile.close()
    with open(os.path.join(dst,"compile_modules.ini"), 'w') as configfile:
        configfile.write(json.dumps(modules,indent=4))
        configfile.close()


def pack_all(src,dst):
    clear_temp()
    create_temp_copy_files(join(root_path,"builds"),join(root_path,"tmp"),dst.lower())
    builds = join(root_path,"tmp")
    sources = []
    exports_path = join(root_path,"Exports")
    if not os.path.exists(exports_path):
        os.makedirs(exports_path)
    if not os.path.exists(join(exports_path,dst) ):
        os.makedirs(join(exports_path,dst) )
    zipf = zipfile.ZipFile(join(exports_path,dst,src), 'w', zipfile.ZIP_DEFLATED)
    
    zipdir(builds,sources, zipf)
    # #zipf.write("build_files/Setup.py")
    build_files = os.path.join(root_path,"build_files")

    #zipf.write(os.path.join(build_files, "Setup.py"), arcname=os.path.join(build_files.replace(build_files, "files"), os.path.join(build_files, "Setup.py")))
    zipf.close()
    # #shutil.move('Exports/' + src,dst + src)
    

if __name__ == '__main__':
    pack_all("Python.zip","Exports/cache/")
    
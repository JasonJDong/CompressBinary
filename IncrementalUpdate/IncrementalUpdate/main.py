import os
from config import config
from incremental_upload_handler import IncrementalUploadHandler
from Utils.util import FileUtil
from file_entity import FileEntity


def gen_test_data():

    server_file = os.path.join(config.server_folder,'test.txt')
    client_file = os.path.join(config.client_folder,'test.txt')

    data = ''
    len = 24
    for i in range(0,len):
        data += 'A'
    FileUtil.write_file_data(server_file,data)
    
    data = ''
    for i in range(0,len):
        if i == 14:
            data += 'B'
        else:
            data += 'A'
    FileUtil.write_file_data(client_file,data)

if __name__ == "__main__":
    
    gen_test_data()

    server_file_path = os.path.join(config.server_folder,'test.txt')
    client_file_path = os.path.join(config.client_folder,'test.txt')

    server_file = FileEntity(server_file_path)
    client_file = FileEntity(client_file_path)

    server_handler = IncrementalUploadHandler(server_file)
    server_handler.TEST_gen_server_blocks_map()
    adler32_pair = server_handler.compute_check_sum()

    #for i in range(0,len(adler32_pair) % 10):
    #    print adler32_pair[i]

    client_handler = IncrementalUploadHandler(client_file,adler32_pair)
    server_handler.server_adler32_pair = adler32_pair
    diffs = client_handler.diff()
    
    log = ''
    for  i in range(0,len(diffs)):
        log += str(diffs[i])
    FileUtil.write_file_data(r'D:\test\log.log',log)
    new_server_file_info = server_handler.gen_data_block(diffs)

    #for i in range(0,len(new_server_file_info)):
    #    print new_server_file_info[i]


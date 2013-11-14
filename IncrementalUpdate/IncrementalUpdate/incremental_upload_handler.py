import uuid
import os
from zlib import adler32
from http.communicator import Communicator
from config import config
from Utils.util import FileUtil

class IncrementalUploadHandler:
    
    def __init__(self,file,server_adler32_pair=None):
        self.file = file
        self.server_adler32_pair = server_adler32_pair

    def is_total_same(self):
        return Communicator.post_total_same(self.file)

    def compute_check_sum(self):
        return self.file.blocks


    def diff(self):
        check_size = config.block_size
        content = FileUtil.get_file_content(self.file.file_path)
        content_len = len(content)
        rolling_page = 0
        last_check_sum = -1
        diffs = []
        connector_diff = []
        offset = 0
        is_allow_push = False
        for i in range(0,content_len):
            adjust_offset = offset + (rolling_page * check_size)
            if adjust_offset + check_size <= content_len:
                if last_check_sum == -1:
                   check_content = content[adjust_offset:check_size + adjust_offset]
                   last_check_sum = adler32(check_content)
                   is_allow_push = False
                else:
                   #print last_check_sum,content[adjust_offset - 1:adjust_offset + check_size - 1]
                   last_check_sum = self._rolling_check_sum(last_check_sum,content[adjust_offset - 1],content[adjust_offset + check_size - 1],check_size)
                   check_content = content[adjust_offset - 1:adjust_offset + check_size - 1]
                   print adjust_offset,check_content
                server_sha256 = self._get_include_sha256(last_check_sum)
                if server_sha256 != None:
                    check_sha256 = FileUtil.compute_data_sha256(check_content)
                    #if adjust_offset == 15:
                        #print check_content
                    if check_sha256 == server_sha256:
                        if len(connector_diff) > 0:
                            diffs.append((self._join_list(connector_diff),(last_check_sum,server_sha256)))
                        diffs.append(('',(last_check_sum,server_sha256)))
                        rolling_page += 1
                        last_check_sum = -1
                        connector_diff = []
                    else:
                        #print content[adjust_offset]
                        connector_diff.append(content[adjust_offset])
                        offset += 1
                else:
                    #print content[adjust_offset]
                    connector_diff.append(content[adjust_offset])
                    offset += 1
            else:
                if adjust_offset != content_len:
                   tail_content = content[adjust_offset:]
                   connector_diff.append(tail_content)
                   diffs.append((self._join_list(connector_diff),(0,'')))
                break
        return diffs

    def gen_data_block(self,data_adler32_pair):
        blocks_info = []
        total_data = ''
        for data,adler32_pair in data_adler32_pair:
            adler32_value,sha256_value = adler32_pair
            file_name = self._search_for_block(adler32_value,sha256_value)
            if file_name == None:
                if data != '':
                   total_data += data
                break
            else:
                if data != '':
                   total_data += data
                block_data = FileUtil.get_file_content(file_name)
                total_data += block_data
        total_data_len = len(total_data)
        for i in range(0,total_data_len,config.block_size):
            if i != total_data_len and i + config.block_size > total_data_len:
               rest_data = total_data[i:]
               #print "================================="
               #print i,total_data_len
               #print "================================="
               replenish_len = config.block_size - len(rest_data)
               for j in range(0,replenish_len):
                   rest_data += '\0'
               rest_file_name = os.path.join(config.block_storage,str(uuid.uuid4()))
               FileUtil.write_file_data(rest_file_name,rest_data)
               rest_adler32_value = adler32(rest_data)
               rest_sha256 = FileUtil.compute_data_sha256(rest_data)
               self._update_global_block(rest_file_name,rest_adler32_value,rest_sha256)
               blocks_info.append((rest_adler32_value,rest_sha256))
            else:
                block_data = total_data[i:i + config.block_size]
                file_name = os.path.join(config.block_storage,str(uuid.uuid4()))
                FileUtil.write_file_data(file_name,block_data)
                adler32_value = adler32(block_data)
                sha256 = FileUtil.compute_data_sha256(block_data)
                self._update_global_block(file_name,adler32_value,sha256)
                blocks_info.append((adler32_value,sha256))
        return blocks_info

    def _search_for_block(self,adler32_value,sha256):
        for file_name,a_v,s in self.file.blocks:
            if a_v == adler32_value and s == sha256:
                return file_name
        return None

    def _rolling_check_sum(self,checksum,remove,add,block_size):
        MOD_VALUE = 65521
        a = checksum
        b = (a >> 16) & 0xffff
        a &= 0xffff

        a1 = (a - ord(remove) + ord(add)) % MOD_VALUE
        b1 = (b - (block_size * ord(remove)) + a1 - 1) % MOD_VALUE

        return (b1 << 16) | a1

    def _adler32(self,data):
        a = 1
        b = 0
        MOD_VALUE = 65521
        for char in data:
            a = (a + ord(char)) % MOD_VALUE
            b = (b + a) % MOD_VALUE
        return (b << 16) | a

    def _get_include_sha256(self,adler32_value):
        if self.server_adler32_pair == None:
            return None
        for _,a_v,sha256 in self.server_adler32_pair:
            if a_v == adler32_value:
                return sha256
        return None

    def _join_list(self,list):
        return ''.join(list)

    def _update_global_block(self,file_path,adler32_value,sha256):
        pass

    #TEST
    def TEST_gen_server_blocks_map(self):
        blocks_data = []
        content = FileUtil.get_file_content(self.file.file_path)
        content_len = len(content)
        for i in range(0,content_len,config.block_size):
            if i != content_len and i + config.block_size > content_len:
                rest_content = content[i:]
                rest_len = config.block_size - (content_len - i)
                for j in range(0,rest_len):
                    rest_content+='\0'
                blocks_data.append(rest_content)
            else:
                blocks_data.append(content[i:config.block_size + i])
        block_data_len = len(blocks_data)
        for i in range(0,block_data_len):
            guid = uuid.uuid4()
            block_name = os.path.join(config.block_storage,str(guid))
            FileUtil.write_file_data(block_name,blocks_data[i])
            self.file.blocks.append((block_name,adler32(blocks_data[i]),FileUtil.compute_data_sha256(blocks_data[i])))





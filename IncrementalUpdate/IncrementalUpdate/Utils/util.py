import hashlib

class FileUtil:

    @staticmethod
    def compute_data_sha256(data):
         try:
           m = hashlib.sha256()
           m.update(data)
           return m.hexdigest()
         except:
           return ''

    @staticmethod
    def compute_file_sha256(file_path):
         try:
             with open(file_path,'rb') as fd:
                content = fd.read()
                m = hashlib.sha256()
                m.update(content)
                return m.hexdigest()
         except:
           return ''
    
    @staticmethod
    def get_file_content(file_path):
        try:
            with open(file_path,'rb') as fd:
                content = fd.read()
                return content
        except:
            return None

    @staticmethod
    def write_file_data(file_path,data):
        try:
            with open(file_path,'wb') as fd:
                fd.write(data)
                return True
        except:
            return False


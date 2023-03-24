import requests, os    

class YaUploader:
    def __init__(self, token: str):
        self.token = token
        self.host = 'https://cloud-api.yandex.net/'
        self.headers = {'Content-Type': 'application/json', 'Authorization': f'OAuth {token}'}
    
    def get_list_file(self,folder_name):
        return os.listdir(folder_name)
                  
    def get_upload_link(self, disk_file_name):
        uri = 'v1/disk/resources/upload/'
        url = self.host + uri
        params = {'path': f'/{disk_file_name}'}
        response = requests.get(url, headers=self.headers, params=params)
        return response.json()['href']   

    def upload(self, file_path: str):
        file_list = self.get_list_file(file_path)
        for name in file_list:
            upload_link = self.get_upload_link(name)
            response = requests.put(upload_link, headers=self.headers, data=open(os.path.join(file_path, name), 'rb'))
            if response.status_code == 201:
                print(f'Загрузка файла {name} прошла успешно!')
            else:
                print(f'При загрузки файла {name} произошла ошибка {response.status_code}')
    
if __name__ == '__main__':
    path_to_file = str(input('Введите путь к файлу: '))
    token = str(input('Введите token для загрузки: '))
    uploader = YaUploader(token)
    result = uploader.upload(path_to_file)

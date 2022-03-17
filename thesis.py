import requests
import json
from PIL import Image
import yadisk
from tqdm import tqdm

id_vk = input('Введите id Vk: ')
token_ya = input('Введите token yadisk: ')
token = '958eb5d439726565e9333aa30e50e0f937ee432e927f0dbd541c541887d919a7c56f95c04217915c32008'
version = '5.131'
folder_name = input('Введите имя папки для сохранения фото: ')

class VkUser:
    def __init__(self, token, version):
        self.url = 'https://api.vk.com/method/photos.get'
        self.params = params= {'owner_id': id_vk,
                              'access_token': token,
                              'album_id': 'profile',
                              'extended': 'likes',
                              'photo_size': 1,
                              'v': version,
                              'count': 10 }

    def write_json(self, date):
        with open('photos.json', 'w') as file:
            json.dump(date, file, indent=2, ensure_ascii=False)


    def get_largest(self, size_dict):
        if size_dict['width'] >= size_dict['height']:
            return size_dict['width']
        else:
            return size_dict['height']

    def main(self, id_vk):
        response = requests.get(self.url, self.params)
        self.write_json(response.json())
        photos = json.load(open('photos.json'))['response']
        photo = photos['items']

        num_likes_array = []
        max_size_url_array = []

        for likes in photo:
            likes = likes['likes']
            num_likes = likes['count']
            num_likes_array.append(num_likes)

        for phot in photo:
            sizes = phot['sizes']
            max_size_url = max(sizes, key=self.get_largest)['url']
            max_size_url_array.append(max_size_url)

        return [max_size_url_array, num_likes_array]

if __name__ == '__main__':
    vk = VkUser(token, version)
    [url_arr, like_arr] = vk.main(id_vk)
    y = yadisk.YaDisk(token=token_ya)
    if (y.is_dir(folder_name) == True):
        y.remove(folder_name)
    y.mkdir(folder_name)

    for url_arr_k in tqdm(range(len(url_arr))):
        filename = '/'+folder_name+'/' + str(like_arr[url_arr_k]) + '.jpg'
        y.upload_url(url_arr[url_arr_k], filename)

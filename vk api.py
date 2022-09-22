from pprint import pprint
import requests

# create class where i can give login and token

class VkBackUp:
    URL = "https://api.vk.com/method/photos.getAll"

    def __init__(self, user_id):
        self.user_id = user_id

    @property
    def get_token(self):
        with open("token.txt", "r") as f:
            token = f.readline().strip()
        return token

    # function to get json
    def get_result(self):
        params = {
            "user_id": self.user_id,
            "access_token": self.get_token,
            "v": "5.131",
        }
        res = requests.get(self.URL, params=params).json()
        return res

    # function to get the highest quality image
    def get_image(self):
        res = self.get_result()
        pics_list = []
        for image in res["response"]["items"]:
            size = 0
            for element in image["sizes"]:
                if size <= element["height"] + element["width"]:
                    size = (element["height"] + element["width"])
                    photo = element["url"]
            pics_list.append(photo)
        return pics_list

    def write_image(self, pic_list):
        for pic in range(len(pic_list)):
            p = requests.get(pic_list[pic])
            name = f"{pic}_img.jpg"
            with open(name, "wb") as f:
                    f.write(p.content)
                    self.upload(name)
            print("success")

    upload_url = "https://cloud-api.yandex.net/v1/disk/resources/upload"

    @property
    def get_YDtoken(self):
        with open("YD.txt", "r") as f:
            return f.readline()

    @property
    def get_header(self):

        return {
            "Content-Type": "application/json",
            "Authorization":f"OAuth {self.get_YDtoken}"
        }

    def get_link(self, file_path):
        params = {"path": file_path, "overwrite": "true"}
        response = requests.get(self.upload_url, params=params, headers=self.get_header)
        return response.json()

    def upload(self, file):
        href = self.get_link(file).get("href")
        if not href:
            print('Error')
            return

        with open(file, "rb") as f:
            response = requests.put(href, data=f)
            if response.status_code == 201:
                print("Sucess")
            else:
                print("Error")



myprofilepic = VkBackUp("750067440")
print(myprofilepic.get_image())
mylist = myprofilepic.get_image()
myprofilepic.write_image(mylist)
#pprint(myprofilepic.get_result())
#pprint(myprofilepic.upload("token.txt"))

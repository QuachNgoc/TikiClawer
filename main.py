
from TikiClawer import TikiClawer
from data import *
import time
from tqdm import tqdm
from colorama import Fore, Style

import tkinter as tk

url_q = "https://tiki.vn/search?q="
file_path = "import_data.csv"
product_txt_path = "data.txt"

total = 100
completed = 0

print(Fore.YELLOW + 'Preparing to start...' + Style.RESET_ALL)

# Loop to simulate work being done
for i in range(total):
    time.sleep(0.05)  # Simulate some work being done
    completed += 1
    progress = completed / total
    bar_length = 50
    filled_length = int(round(bar_length * progress))
    bar = '█' * filled_length + '-' * (bar_length - filled_length)
    percentage = round(progress * 100, 2)

    # Print colored progress bar
    print(Fore.GREEN + f'\r[{bar}] {percentage}% ' + Style.RESET_ALL, end='', flush=True)

print(Fore.YELLOW + '\nProgram Start' + Style.RESET_ALL)

# create a Tkinter window
window = tk.Tk()
window.title("Tiki Clawer")


##----------------UI----------------------------##
searchInputLabel = tk.Label(window, text="Nhập các từ cần tìm cách nhau bởi dấu phẩy: ")
searchInputLabel.grid(column=0, row=0)

searchInputTxt = tk.Entry(window)
searchInputTxt.grid(column=0, row=1)

pageInputLabel =tk.Label(window, text="Số trang cần crawl: ")
pageInputLabel.grid(column=0, row=3)

scale = tk.Scale(window, from_=0, to=10, orient=tk.HORIZONTAL)
scale.grid(column=0, row=4)
##---------------------------------------------##

def display_output():
    # Const
    searchInput = searchInputTxt.get()
    listSearchInput = searchInput.split(", ")

    # lưu thông tin các sản phẩm crawl về
    totalProduct = []

    # cho đi đến trang thứ n
    pages = scale.get() + 1


    for searchinput in listSearchInput:
        # Gọi Object TikiCrawl ra
        tiki = TikiClawer()

        for i in range(1,pages):
            tiki.getUrl(f"{url_q}{searchinput}&page={i}")
            time.sleep(5)
            
            # lấy link sản phẩm và lưu thành array
            productLinks = tiki.getProductLinks(productLinksXpath)

            for link in productLinks:
                # đi vào đường link sản phẩm đó
                tiki.getUrl(link)

                # lấy tên sản phẩm đó
                tiki.name = tiki.getProductInfo(name_xpath)
                print(tiki.name.lower())
                if tiki.name == "Không tìm thấy sản phẩm":
                    continue
                else:
                    # tạo post name
                    tiki.createPostName(tiki.name)

                    # lấy giá
                    tiki.getPrices(prices_xpath)

                    # lấy brand
                    tiki.getBrand(brand_name_xpath)

                    # lấy type
                    tiki.getCate(tiki.name)
                    print(tiki.cat_txt)

                    # lấy Vị
                    tiki.getFavors(favor_xpath)
                    print(tiki.favor_txt)

                    tiki.getWeights(favor_xpath)
                    print(tiki.weight_txt)
                    
                    # lấy ảnh
                    tiki.getImages()

                    # lấy Description
                    tiki.getDescription()

                    tiki.appendtoTotalProduct(totalProduct)
            

        # Lưu file.txt ở đường dẫn nào đó
        tiki.savingData(totalProduct, product_txt_path)

        # lấy data từ data.txt
        data = tiki.exportData(product_txt_path)

        # chuyển thành file csv
        tiki.createCSV(data, file_path)

        tiki.stopProcess()

##-----------------UI-----------------##
button = tk.Button(window, text="Submit", command=display_output)
button.grid(column=0, row=5)

window.mainloop()












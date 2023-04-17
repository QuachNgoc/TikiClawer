
from TikiClawer import TikiClawer
from data import *
import time


import tkinter as tk
url_q = "https://tiki.vn/search?q="
file_path = "import_data.csv"
product_txt_path = "data.txt"


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
    pages = scale.get()


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
                if tiki.name == "Không tìm thấy sản phẩm":
                    continue
                else:
                    # tạo post name
                    tiki.createPostName(tiki.name)

                    # lấy giá
                    tiki.getPrices(prices_xpath)

                    # lấy brand
                    tiki.brand = tiki.getProductInfo(brand_name_xpath)

                    # lấy type
                    tiki.getType(tiki.name)

                    # lấy catory
                    tiki.getCatories(type_names_xapth)

                    # lấy colors
                    tiki.getColors(color_names_xpath)

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












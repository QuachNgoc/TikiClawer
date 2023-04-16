# nộp source code, file csv có thể import, ảnh chụp màn hình có thể import, optional: thêm 1 chương trình .exe, tách attribute bằng @
# git remote add origin https://github.com/QuachNgoc/TikiClawer.git
# git branch -M main
# git push -u origin main
from TikiClawer import TikiClawer
from data import *
import os

# Const
searchInput = input("Nhập các từ khóa cách nhau bởi dấu phẩy: ") # bàn phím cơ, bàn phím cơ gaming, bàn phím chơi game
listSearchInput = searchInput.split(", ")


url = "https://tiki.vn"
file_path = "import_data.csv"
new_file_path = "data.csv"
product_txt_path = "data.txt"

listXpath = [first_product_name_xpath, first_product_xpath, prices_xpath, brand_name_xpath, type_names_xapth, color_names_xpath]
totalProduct = []

for i in listSearchInput:
    print(i)
    # Gọi Object TikiCrawl ra
    tiki = TikiClawer(url, i, listXpath, product_txt_path)

    # Đi đến url đó
    tiki.getUrl()

    # Tìm kiếm sản phẩm bàn phím cơ
    tiki.sendSearchInput(i)
    tiki.deleteSearchInput()

    # Lưu các tên sản phẩm đã lấy name vào 1 file txt
    productNameList = tiki.getListProduct(xpath_list_product_names)

    # Lưu file.txt ở đường dẫn nào đó
    tiki.savingData(productNameList, product_txt_path)

    # Lấy dữ liệu từ file.txt đó
    listProductName = tiki.exportData(product_txt_path)

    for item in listProductName:
        tiki.sendSearchInput(item)
        tiki.name = item 

        try:
            first_item_name = tiki.getProductInfo(listXpath[0])
        except Exception as e:
            print(e)
            
        tiki.checking_item = tiki.name == first_item_name
        if tiki.checking_item == True:

            tiki.createPostName(tiki.name)
            print(tiki.post_name)

            tiki.clickItems(listXpath[1])

            tiki.getPrices(listXpath[2])
            print(tiki.regular_price)
            print(tiki.discounted_price)

            tiki.brand = tiki.getProductInfo(listXpath[3])
            print(tiki.brand)

            # lấy list các type
            tiki.getType(tiki.name)
            print(tiki.type_txt)
            

            # lấy catories
            tiki.getCatories(listXpath[4])
            print(tiki.cat_txt)

            tiki.getColors(listXpath[5])
            print(tiki.color_txt)

            tiki.appendtoTotalProduct(totalProduct)
        
        tiki.deleteSearchInput()
            

    # chuyển thành file csv
    
    if os.path.exists(file_path):
        print("CSV file exists!")
        tiki.mergeCsv(totalProduct,file_path, new_file_path)
    else:
        print("CSV file does not exist.")
        tiki.createCSV(totalProduct, file_path)
    
    # dừng tiến trình
    tiki.stopProcess()












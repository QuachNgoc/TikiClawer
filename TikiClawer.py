import os 
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import pandas as pd
import time
import chromedriver_autoinstaller 

chromedriver_autoinstaller.install()
opt = webdriver.ChromeOptions()
opt.add_argument("--window-size=800,600")

class TikiClawer:
    def __init__(self, url, search_name, listXpath, txt_path):
        # global variables
        self.driver = webdriver.Chrome(options=opt)
        self.url = url
        self.search_name = search_name
        self.sleep_time = 3
        self.search_input_xpath = '//*[@id="main-header"]/div/div[1]/div[1]/div[2]/div/input'

        self.name = ""
        self.color_txt = ""
        self.type_txt = ""
        self.cat_txt = ""
        self.post_name = ""
        self.discounted_price = ""
        self.regular_price = ""
        self.brand = ""
        self.checking_item  = False
        
        self.txt_path = txt_path

        self.listXpath = listXpath
        


    # Đi đến trang đó
    def getUrl(self):
        self.driver.get(self.url)

    def stopProcess(self):
        self.driver.quit()
    
    # Nhập text muốn tìm kiếm
    def sendSearchInput(self, text):
        search_input = self.driver.find_element(By.XPATH, self.search_input_xpath)
        search_input.send_keys(text)
        search_input.send_keys(Keys.ENTER)
        time.sleep(self.sleep_time) 

    # Xóa text đã tìm kiếm
    def deleteSearchInput(self):
        search_input = self.driver.find_element(By.XPATH,self.search_input_xpath)
        search_input.send_keys(Keys.CONTROL, 'a')
        search_input.send_keys(Keys.DELETE)
        time.sleep(self.sleep_time) 

    # Bấm vào item
    def clickItems(self, xpath):
        item = self.driver.find_element(By.XPATH, xpath)
        item.click()

    
    # Trả về một list của danh sách các tên sản phẩm
    def getListProduct(self, xpath):
        list = self.driver.find_elements(By.XPATH,xpath)
        list_names = [ i.text for i in list ]
        return list_names 

    # Trả về text của 1 web element
    def getProductInfo(self, xpath):
        info = self.driver.find_element(By.XPATH, xpath)
        return info.text

    # slug sản phẩm
    def createPostName(self, txt):
        self.post_name = txt.lower()
        self.post_name = self.post_name.replace("- ","")
        self.post_name = self.post_name.replace("+ ","")
        self.post_name = self.post_name.replace(", "," ")
        self.post_name = self.post_name.replace("/ ", " ")
        self.post_name = self.post_name.replace(" ", "-")
        self.post_name = self.post_name.replace("--", "-")
        self.post_name = self.post_name.replace("|-", "")
        

    # Lưu tên các sản phẩm trong 1 file.txt
    def savingData(self, data, path):
        with open(path, "a+", encoding="utf-8") as file:
            file.seek(0)
            existing_data = file.read().splitlines()

            for element in data:
                if str(element) not in existing_data:
                    file.write(str(element) + "\n")
        print(path + " created or updated!")
    
    # Dựa vào các data trong data.txt gõ tên sản phẩm đó lên search và nhấn enter
    def exportData(self, path):
        list = []
        with open(path, 'r', encoding="utf-8") as file:
            for line in file:
                list.append(line.strip('\n'))
        return list 
    
    def getPrices(self, xpath):
        # lấy giá
        try:
            flash_sale_regular_price_xpath = '//*[@id="__next"]/div[1]/main/div[3]/div[1]/div[3]/div[2]/div[1]/div[1]/div[1]/div[1]/div/span[1]'
            flash_sale_discount_price_xpath = '//*[@id="__next"]/div[1]/main/div[3]/div[1]/div[3]/div[2]/div[1]/div[1]/div[1]/div[1]/span'

            self.discounted_price = self.getProductInfo(flash_sale_discount_price_xpath)
            self.regular_price = self.getProductInfo(flash_sale_regular_price_xpath)


        except Exception as e:
            print(e)

        prices = self.getListProduct(xpath)
        # 0: giá khuyến mãi, 1: giá gốc
        # nếu len == 1 cho chỉ có giá gốc
        if len(prices) == 1:
            self.regular_price = prices[0]
            
        # nếu len == 3 pop()
        elif len(prices) == 3:
            prices.pop()
            self.discounted_price = prices[0]
            self.regular_price = prices[1]
        else:
            self.discounted_price = prices[0]
            self.regular_price = prices[1]

    def getType(self, item):
        name_product = item
        # cho type là Bluetooth nếu list rỗng
        if "bluetooth" in name_product or "không dây" in name_product:
            self.type_txt = "Bluetooth"
        else:
            self.type_txt = "Có Dây"


    def getCatories(self, xpath):
        catories = self.getListProduct(xpath)
        new_catories = list(filter(lambda x: x != "", catories))
        # không có cat nào hết
        if not new_catories:
            self.cat_txt = "Khác"
        else:
            self.cat_txt = ' | '.join(new_catories)


    def getColors(self, xpath):
        
        colors = self.getListProduct(xpath)
        new_colors = list(filter(lambda x: x != "", colors))
        if not new_colors:
            self.color_txt = "Màu như hình"
        else:
            self.color_txt = ' | '.join(new_colors)


    def appendtoTotalProduct(self, list):
        list.append({
            "post_title": self.name,
            "post_name": self.post_name,
            "post_status":"publish",
            "sku": 100,
            "downloadable":"no",
            "virtual":"no",
            "visibility":"visible",
            "images": "",
            "stock":"1", 
            "stock_status":"instock",
            "backorders":"no",
            "manage_stock":"no",
            "regular_price": self.regular_price,
            "sale_price": self.discounted_price,
            "tax_status":"taxable",
            "tax_class":"",
            "tax:product_type": "Bàn phím cơ",
            "tax:product_cat": self.type_txt,
            "tax:product_tag": self.cat_txt,
            "tax:product_brand": self.brand,
            "attribute:Color": self.color_txt,
            "attribute_data:Color":"0|1|1", # k bik cái nì
        })
        print("Added!")


    def createCSV(self, data, path):
        try:
            # Convert list of dictionaries to pandas dataframe
            df = pd.DataFrame(data)

            # Save dataframe to CSV file
            df.to_csv(path, sep="@", index=False)

        except Exception as e:
            pass

    
    def mergeCsv(self, new_data,path,  new_file_path):
        df_existing = pd.read_csv(path)
        df_new = pd.DataFrame(new_data)

        # concatenate existing DataFrame and new DataFrame
        df_concat = pd.concat([df_existing, df_new], ignore_index=True)

        # drop duplicate rows
        df_concat = df_concat.drop_duplicates(subset=['post_title'])

        # save final DataFrame to CSV file
        df_concat.to_csv(new_file_path, index=False)



            










        
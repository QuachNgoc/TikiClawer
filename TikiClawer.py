from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import pandas as pd
import time
import chromedriver_autoinstaller 
import ast
import re
import uuid

chromedriver_autoinstaller.install()
opt = webdriver.ChromeOptions()
opt.add_argument("--window-size=800,600")

class TikiClawer:
    def __init__(self):
        # global variables
        self.driver = webdriver.Chrome(options=opt)
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
        self.image = ""
        self.description = ""


    # Đi đến trang đó
    def getUrl(self, url):
        self.driver.get(url)

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


    
    # Trả về một list của danh sách các tên sản phẩm
    def getListProduct(self, xpath):
        list = self.driver.find_elements(By.XPATH,xpath)
        list_names = [ i.text for i in list ]
        return list_names 

    # Trả về text của 1 web element
    def getProductInfo(self, xpath):
        info = self.driver.find_elements(By.XPATH, xpath)
        if info:
            info = self.driver.find_element(By.XPATH, xpath)
            return info.text
        else:
            return "Không tìm thấy sản phẩm"

    # slug sản phẩm
    def createPostName(self, txt):
        self.post_name = txt.lower()
        self.post_name = self.post_name.replace("- ","")
        self.post_name = self.post_name.replace("+ ","")
        self.post_name = self.post_name.replace(", "," ")
        self.post_name = self.post_name.replace("/ ", " ")
        self.pot_name = self.post_name.replace("/", " ")
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


    
    # Dựa vào các data trong data.txt
    def exportData(self, path):
        list = []
        with open(path, 'r', encoding="utf-8") as file:

            for line in file:
                line = line.strip("\n")
                your_dict = ast.literal_eval(line)
                list.append(your_dict)
        return list 
    
    # lấy list link sản phẩm
    def getProductLinks(self, xpath):
        productLinks = self.driver.find_elements(By.XPATH, xpath)
        productLinks = [link.get_attribute("href") for link in productLinks]
        return productLinks
    
    def getImages(self):
        images = ""
        imagesEL = self.driver.find_elements(By.XPATH, '//a[contains(@data-view-id, "pdp_main_view_photo")]')

        for el in imagesEL:
            el.click()
            imageContainer = self.driver.find_element( By.XPATH, '//div[contains(@class, "thumbnail")]').get_attribute('innerHTML')
            if re.search(r'<picture class="webpimg-container">', imageContainer):
                images = images + re.search(r'src="([^"]+)"', imageContainer).group(1) + ", "
        
        self.image = images
    
    def getPrices(self, xpath):
        # lấy giá
        try:
            flash_sale = self.driver.find_elements(By.CLASS_NAME, "flash-sale-price")
            if flash_sale:
                flash_sale_regular_price_xpath = '//*[@id="__next"]/div[1]/main/div[3]/div[1]/div[3]/div[2]/div[1]/div[1]/div[1]/div[1]/div/span[1]'
                flash_sale_discount_price_xpath = '//*[@id="__next"]/div[1]/main/div[3]/div[1]/div[3]/div[2]/div[1]/div[1]/div[1]/div[1]/span'

                self.discounted_price = self.getProductInfo(flash_sale_discount_price_xpath)
                self.regular_price = self.getProductInfo(flash_sale_regular_price_xpath)
            else: 
                prices = self.getListProduct(xpath)
                # 0: giá khuyến mãi, 1: giá gốc
                # nếu len == 1 cho chỉ có giá gốc
                if len(prices) == 1:
                    self.regular_price = prices[0].replace(".", " ")
                    self.discounted_price = ""
                    
                # nếu len == 3 pop()
                elif len(prices) == 3:
                    prices.pop()
                    self.discounted_price = prices[0].replace(".", " ")
                    self.regular_price = prices[1].replace(".", " ")
                else:
                    self.discounted_price = prices[0].replace(".", " ")
                    self.regular_price = prices[1].replace(".", " ")

        except Exception as e:
            print(e)



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
    
    def generate_item_id(self):
        # Get the current timestamp in milliseconds
        timestamp = int(time.time() * 1000)
        
        # Generate a UUID
        uuid_str = str(uuid.uuid4())
        
        # Concatenate the timestamp and UUID to create a unique ID
        item_id = f"{timestamp}-{uuid_str}"
        
        return item_id
    
    def getDescription(self):
        self.description = self.driver.find_element(By.XPATH,'//div[contains(@class, "ToggleContent__View-sc-1dbmfaw-0 wyACs")]').get_attribute("innerHTML")


    def appendtoTotalProduct(self, list):
        list.append({
            "ID": self.generate_item_id()[0:8],
            "Type": self.type_txt,
            "SKU": "",
            "Name": self.name,
            "Published": 1,
            "Is featured?": 0,
            "Visibility in catalog": "visible",
            "Short description": "",
            "Description": self.description,
            "Date sale price start": "",
            "Date sale price ends": "",
            "Tax status": "taxable",
            "Tax class": "Standard",
            "In stock?": 1,
            "Stock": 100,
            "Low stock amount": "",
            "Backorders allowed?": 0,
            "Sold individually?": 0,
            "Weight (kg)": "",
            "Length (cm)": "",
            "Width (cm)": "",
            "Height (cm)": "",
            "Allow customer reviews?": 1,
            "Purchase note": "",
            "Sale price": self.discounted_price,
            "Regular price": self.regular_price,
            "Categories": self.cat_txt,
            "Tags": self.post_name,
            "Shipping class": "",
            "Images": self.image,
            "Download limit": "",
            "Download expiry days": "",
            "Parent": "",
            "Grouped products": "",
            "Upsells": "Cross-sells",
            "External URL": "",
            "Button text": "",
            "Position": 0,
            "Attribute 1 name": "Colors",
            "Attribute 1 value(s)": self.color_txt,
            "Attribute 1 visible": 0,
            "Attribute 1 global": 1,
            "Attribute 2 name": "",
            "Attribute 2 value(s)": "",
            "Attribute 2 visible": "",
            "Attribute 2 global": "",
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




            










        
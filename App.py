import tkinter
import tkinter.messagebox
import customtkinter
from TikiClawer import TikiClawer
from data import *
import time
from woocommerce import API
from tkinter import filedialog
import tkinter as tk
from PIL import Image
import json
import csv

customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("green")

url_q = "https://tiki.vn/search?q="
# file_path = "import_data.csv"
# product_txt_path = "data.txt"

file_path = "new_import_data.csv"
product_txt_path = "new_data.txt"

wcapi = API(
    url="http://localhost/giadungviet",
    consumer_key="ck_5c33f700ac22e46511e9f847a5cf71df4d26a6d8",
    consumer_secret="cs_517ed556cf4ef56349a99d5b3318c3acd4ac7fb4",
    version="wc/v3",
    wcapi=True
)

class App(customtkinter.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.toplevel_window = None
        # configure window
        self.title("NgocVietFood App")
        self.geometry(f"{1000}x{450}")

        # configure grid layout (4x4)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        self.data_str_app = ""
        self.toplevel_window = None

        #---------------Sidebar----------------------#
        ##-------------------Clawer-----------------------##
        self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)

        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="Tiki Clawer", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        
        self.searchInputTxt = customtkinter.CTkEntry(self.sidebar_frame, placeholder_text="Nhập keywords: ")
        self.searchInputTxt.grid(row=1, column=0, columnspan=2, padx=20, pady=10)

        self.pageInputTxt = customtkinter.CTkEntry(self.sidebar_frame, placeholder_text="Nhập số trang(1-10): ")
        self.pageInputTxt.grid(row=2, column=0, columnspan=2, padx=20, pady=10)
        
        self.submit_btn = customtkinter.CTkButton(self.sidebar_frame, command=self.display_output, text="Submit")
        self.submit_btn.grid(row=3, column=0, padx=20, pady=10)

        ##-------------------Clear btn-----------------------##
        self.clear_btn = customtkinter.CTkButton(self.sidebar_frame, command=self.clear, text="Clear")
        self.clear_btn.grid(row=4, column=0, padx=20, pady=(10,10))

        ##----------------Themes, Scale Window-------------------##
        self.appearance_mode_label = customtkinter.CTkLabel(self.sidebar_frame, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.grid(row=5, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["Light", "Dark", "System"],
                                                                       command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(row=6, column=0, padx=20, pady=(10, 10))
        self.scaling_label = customtkinter.CTkLabel(self.sidebar_frame, text="UI Scaling:", anchor="w")
        self.scaling_label.grid(row=7, column=0, padx=20, pady=(10, 0))
        self.scaling_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["80%", "90%", "100%", "110%", "120%"],
                                                               command=self.change_scaling_event)
        self.scaling_optionemenu.grid(row=8, column=0, padx=20, pady=(10, 20))

        #----------------Output Textbox -----------------#
        self.textbox = customtkinter.CTkTextbox(self)
        self.textbox.grid(row=0, column=1, rowspan=2, padx=20, pady=(20,0), sticky="nsew")  

        #----------------------Product Menu--------------------------#
        self.product_api = "products"
        self.product_att_api = "products/attributes"

        self.optionmenu_1_var = tkinter.StringVar()
        self.optionmenu_1_var.set("CRUD_1")

        self.tabview = customtkinter.CTkTabview(self, width=250)
        self.tabview.grid(row=0, column=2, padx=20, pady=10, sticky="nsew")
        self.tabview.add("Products")
        self.tabview.add("Coupons")
        self.tabview.add("Reports")

        self.tabview.tab("Products").grid_columnconfigure(0, weight=1)  # configure grid of individual tabs
        self.tabview.tab("Coupons").grid_columnconfigure(0, weight=1)

        ##------ Product tab -------------##
        ###------ CRUD Product -----------###
        self.optionmenu_1_label = customtkinter.CTkLabel(self.tabview.tab("Products"), text="Product: ", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.optionmenu_1_label.grid(row=0,column=0, padx=5, pady=(20, 10))
        self.optionmenu_1 = customtkinter.CTkOptionMenu(self.tabview.tab("Products"), dynamic_resizing=False, values=["CRUD_1", "Create_All", "List_All", "View_1"],variable=self.optionmenu_1_var, command = lambda name = self.optionmenu_1_var, name_api = self.product_api : self.execute_function(name, name_api))
        self.optionmenu_1.grid(row=0, column=1, padx=20, pady=(20, 10))

        ###------ CRUD Product Attribute-----------###
        self.optionmenu_2_label = customtkinter.CTkLabel(self.tabview.tab("Products"), text="Attribute: ", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.optionmenu_2_label.grid(row=1,column=0, padx=5, pady=(20, 10))
        self.optionmenu_2 = customtkinter.CTkOptionMenu(self.tabview.tab("Products"), dynamic_resizing=False, values=["CRUD_Att_1", "List_Att_All", "View_Att_1"],variable=self.optionmenu_1_var, command = lambda name = self.optionmenu_1_var, name_api = self.product_att_api : self.execute_function(name, name_api))
        self.optionmenu_2.grid(row=1, column=1, padx=20, pady=(20, 10))

    
    def update_data_str(self, new_data):
        self.data_str_app = new_data
        self.printOut(self.data_str_app)  # In ra giá trị mới của data_str

    def execute_function(self, name, name_api):
        function_name = f'{name}' # name là tên của function đó nha
        function = getattr(self, function_name)
        function(name_api)

    def CRUD_1(self, name_api):
        self.printOut("CRUD 1 "+ name_api)

        if self.toplevel_window is None or not self.toplevel_window.winfo_exists():
            self.toplevel_window = CreateAProductWindow(self, name_api , self.update_data_str)  # create window if its None or destroyed
                
        else:
            self.toplevel_window.focus()  # if window exists focus it

    def Create_All(self, name_api):  
        name_api = self.product_api
        data = []

        #Đọc dữ liệu từ file CSV và import vào WooCommerce
        with open(file_path, 'r',encoding="utf-8") as file:
            csv_data = csv.DictReader(file,delimiter='@')
            for row in csv_data:
                # Chuẩn bị dữ liệu từ dòng CSV để gửi lên WooCommerce
                images_list = []
                img_row = row['Images'].split(", ")
                for img in img_row:
                    image = {"src": img}
                    images_list.append(image)


                product_data = {
                    'name': row['Name'],
                    'type': row['Type'],
                    'description': row['Description'],
                    'manage_stock':True,
                    'stock_quantity': row['Stock'],
                    'regular_price': row['Regular price'],
                    'sale_price': row['Sale price'],
                    'images':images_list,
                }
                data.append(product_data)

        for d in data:
            self.printOut("Loading...")
            try:
                # Gửi yêu cầu API để tạo sản phẩm mới trên WooCommerce
                response = wcapi.post(name_api, d)

                # Kiểm tra phản hồi từ WooCommerce
                if response.status_code == 200 or response.status_code == 201 :
                    self.printOut(f'Successfully imported product: {d["name"]}')
                else:
                    self.printOut(f'Failed to import product: {d["name"]}')
            except Exception as e:
                pass


    def View_1(self, name_api):
        self.clear()
        dialog = customtkinter.CTkInputDialog(text="Nhập từ khóa tìm kiếm: ", title="ViewDialog")
        search_value = dialog.get_input()

        # Kiểm tra giá trị trong danh sách các dict và hiển thị kết quả
        found_results = False
        result_string = ""
        list_dict = wcapi.get(name_api).json()

        # Tìm kiếm
        for data in list_dict:
            if search_value in data.values():
                found_results = True
                result_string += json.dumps(data, indent=4) + "\n"
                        
        
        # hiển thị
        if found_results:
            self.printOut(result_string)
        else:
            self.printOut("Không tìm thấy kết quả.")


    def List_All(self,name_api):
        self.clear()
        dialog = customtkinter.CTkInputDialog(text="Nhập tên api: ", title="ViewDialog")
        if dialog.get_input() == name_api:
            self.printOut( json.dumps(wcapi.get(name_api).json(), indent=4) )

    def clear(self):
        self.textbox.delete("1.0", "end")
        self.searchInputTxt.delete(0, tk.END)
        self.pageInputTxt.delete(0, tk.END)

    def printOut(self, text):
        self.clear()
        self.textbox.insert("0.0", "\nOUTPUT\n\n" + text)

    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)

    def display_output(self):
        searchInput = self.searchInputTxt.get()
        listSearchInput = searchInput.split(", ")
        
        # lưu thông tin các sản phẩm crawl về
        totalProduct = []

        pages = int(self.pageInputTxt.get()) + 1

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



class CreateAProductWindow(customtkinter.CTkToplevel):
    def __init__(self, parent, name_api, callback):
        super().__init__(parent)
        self.geometry(f"{860}x{550}")
        self.title("Product")

        self.name_api = name_api
        self.callback = callback 

        self.display_images = []
        self.images = []

        self.data = {}
        self.data_str = ""

        self.id = ""
        self.name = ""
        self.type = ""
        self.re_price = ""
        self.sale_price =  ""
        self.des = ""
        self.short_des = ""
        self.stock_quantity =  0

        self.logo_label = customtkinter.CTkLabel(self, text=self.name +" " + self.name_api, font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=10, pady=10)
        
        #------- Names ----------#
        self.label = customtkinter.CTkLabel(self, text="Tên sản phẩm", font=customtkinter.CTkFont(size=14, weight="bold"))
        self.label.grid(row=1, column=0)
        self.nameProductInputTxt = customtkinter.CTkEntry(self, placeholder_text="Nhập tên sản phẩm: ")
        self.nameProductInputTxt.grid(row=1, column=1, sticky="nsew",padx=10, pady=10)

        #------- Types ----------#
        self.label1 = customtkinter.CTkLabel(self, text="Loại sản phẩm", font=customtkinter.CTkFont(size=14, weight="bold"))
        self.label1.grid(row=2, column=0)
        self.typeOptionmenu = customtkinter.CTkOptionMenu(self, dynamic_resizing=False, values=["simple", "..."])
        self.typeOptionmenu.grid(row=2, column=1, sticky="nsew", padx=10, pady=10)

        #--------- ID ------------#
        self.label8 = customtkinter.CTkLabel(self, text="ID", font=customtkinter.CTkFont(size=14, weight="bold"))
        self.label8.grid(row=1, column=2)
        self.idInputTxt = customtkinter.CTkEntry(self, placeholder_text="ID: ")
        self.idInputTxt.grid(row=1, column=3, sticky="nsew", padx=10, pady=10)
        self.idSubmit_button = customtkinter.CTkButton(self, command=self.submit, text="Submit")
        self.idSubmit_button.grid(row=1, column=4)

        #------- Regular Prices ----------#
        self.label2 = customtkinter.CTkLabel(self, text="Giá thường", font=customtkinter.CTkFont(size=14, weight="bold"))
        self.label2.grid(row=3, column=2)
        self.rePriceProductInputTxt = customtkinter.CTkEntry(self, placeholder_text="Giá thường: đ")
        self.rePriceProductInputTxt.grid(row=3, column=3, sticky="nsew", padx=10, pady=10)

        #------- Sale Prices ----------#
        self.label3 = customtkinter.CTkLabel(self, text="Giá Sale", font=customtkinter.CTkFont(size=14, weight="bold"))
        self.label3.grid(row=2, column=2)
        self.salePriceProductInputTxt = customtkinter.CTkEntry(self, placeholder_text="Giá sale: đ")
        self.salePriceProductInputTxt.grid(row=2, column=3, sticky="nsew", padx=10, pady=10)

        #------- Images ----------#
        self.label4 = customtkinter.CTkLabel(self, text="Images", font=customtkinter.CTkFont(size=14, weight="bold"))
        self.label4.grid(row=3, column=0)
        self.imageBtn = customtkinter.CTkButton(self, command=self.add_images,text="+")
        self.imageBtn.grid(row=3, column=1, sticky="nsew", padx=10, pady=10)

        #------- Des ----------#
        self.label5 = customtkinter.CTkLabel(self, text="Mô tả", font=customtkinter.CTkFont(size=14, weight="bold"))
        self.label5.grid(row=5, column=0)
        self.short_des_textbox = customtkinter.CTkTextbox(self, width=250)
        self.short_des_textbox.grid(row=6, column=0, sticky="nsew", columnspan=2, padx=10, pady=10)

        #------- Short Des ----------#
        self.label6 = customtkinter.CTkLabel(self, text="Mô tả Ngắn", font=customtkinter.CTkFont(size=14, weight="bold"))
        self.label6.grid(row=5, column=2)
        self.des_textbox = customtkinter.CTkTextbox(self, width=250)
        self.des_textbox.grid(row=6, column=2, columnspan=2,sticky="nsew", padx=10, pady=10)

        #------- Stocks quanity ----------#
        self.label7 = customtkinter.CTkLabel(self, text="Tồn kho", font=customtkinter.CTkFont(size=14, weight="bold"))
        self.label7.grid(row=7, column=0)
        self.stocksInputTxt = customtkinter.CTkEntry(self, placeholder_text="Tồn kho: ")
        self.stocksInputTxt.grid(row=7, column=1, sticky="nsew", padx=10, pady=10)

        #------- Create Button ----------#
        self.create_button = customtkinter.CTkButton(self, command=self.create, text="Create" )
        self.create_button.grid(row=8, column=0, sticky="nsew", padx=20, pady=10)

        #------- Update Button ----------#
        self.update_button = customtkinter.CTkButton(self, command=self.update, text="Update" )
        self.update_button.grid(row=8, column=1, sticky="nsew", padx=20, pady=10)

        #------- Delete Button ----------#
        self.update_button = customtkinter.CTkButton(self, command=self.delete, text="Delete" )
        self.update_button.grid(row=8, column=2, sticky="nsew", padx=20, pady=10)

    def add_images(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])

        if file_path:
            image = customtkinter.CTkImage(dark_image=Image.open(file_path), size=(40,40))
            self.display_images.append(image)  # Add the image to the list to display

            self.images.append(
                {
                    'src': file_path,
                }
            )

            for i in range(len(self.display_images)):
                image_label = customtkinter.CTkLabel(self, image=self.display_images[i], text="")
                image_label.grid(row=4, column=i+1, pady=(5,0))
            
    def create(self):
        self.name = self.nameProductInputTxt.get()
        self.type = self.typeOptionmenu.get()
        self.re_price = self.rePriceProductInputTxt.get()
        self.sale_price =  self.salePriceProductInputTxt.get()
        self.des = self.des_textbox.get("0.0", "end")
        self.short_des = self.short_des_textbox.get("0.0", "end")
        self.stock_quantity =  int(self.stocksInputTxt.get())

        self.data = {
            "name":self.name,
            "type":self.type,
            "regular_price": self.re_price,
            "sale_price": self.sale_price,
            "description":self.des,
            "short_description": self.short_des,
            "manage_stock":True,
            "stock_quantity": self.stock_quantity
        }

        my_created_data = wcapi.post(self.name_api, self.data)
        if my_created_data.status_code == 201 or my_created_data.status_code == 200:
            self.data_str = "Đã thêm Sản phẩm thành công!"
            self.callback(self.data_str)
        else:
            self.data_str = "Đã thêm Sản phẩm KHÔNG thành công!"
            self.callback(self.data_str)

    def changeEntry(self, entry, new_value):
        entry.delete(0, tk.END)  # Clear the current value in the entry widget
        entry.insert(0, new_value)  # Set the new value
        

    def submit(self):
        self.id = self.idInputTxt.get()

        # gọi API lấy 1 sản phẩm
        data = wcapi.get(self.name_api+"/"+self.id).json()

        name = data.get("name")
        regular_price = data.get("regular_price")
        sale_price = data.get("sale_price")
        stock_quantity = str(data.get("stock_quantity"))
        
        self.changeEntry(self.nameProductInputTxt, name)
        self.changeEntry(self.rePriceProductInputTxt, regular_price)
        self.changeEntry(self.salePriceProductInputTxt, sale_price)
        self.changeEntry(self.stocksInputTxt, stock_quantity)

        self.des_textbox.delete("1.0", "end")
        self.des_textbox.insert("0.0", data["description"])
        
        self.short_des_textbox.delete("1.0", "end")
        self.short_des_textbox.insert("0.0",data["short_description"])


    def update(self):
        self.id = self.idInputTxt.get()
        self.name = self.nameProductInputTxt.get()
        self.type = self.typeOptionmenu.get()
        self.re_price = self.rePriceProductInputTxt.get()
        self.sale_price =  self.salePriceProductInputTxt.get()
        self.des = self.des_textbox.get("0.0", "end")
        self.short_des = self.short_des_textbox.get("0.0", "end")
        self.stock_quantity =  int(self.stocksInputTxt.get())

        self.data = {
            "name":self.name,
            "type":self.type,
            "regular_price": self.re_price,
            "sale_price": self.sale_price,
            "description":self.des,
            "short_description": self.short_des,
            "manage_stock":True,
            "stock_quantity": self.stock_quantity
        }

        my_updated_data = wcapi.post(self.name_api+"/"+self.id, self.data)
        print(my_updated_data.status_code)

        if my_updated_data.status_code == 201 or my_updated_data.status_code == 200:
            self.data_str = "Cập nhật sản phẩm thành công! Bạn có thể View sản phẩm"
            self.callback(self.data_str)
        else:
            self.data_str = "Cập nhật không thành công!!"
            self.callback(self.data_str)

    def delete(self):
        self.id = self.idInputTxt.get()
        my_deleted_data = wcapi.delete(self.name_api+"/"+self.id, params={"force": True})

        if my_deleted_data.status_code == 201 or my_deleted_data.status_code == 200:
            self.data_str = "Đã xóa sản phẩm thành công."
            self.callback(self.data_str)
        else:
            self.callback(self.data_str)
        
        
        
        





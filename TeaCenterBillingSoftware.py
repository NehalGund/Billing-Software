'''Please read multiline comment, written at line number 47'''
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import datetime
import mysql.connector as connector
import maskpass

class bills:
    def __init__(self,tea,userName,passWord):
        self.tea = tea
        self.userName = userName
        self.passWord = passWord
        try:
            # Create Database named "Billing"
            self.bill = connector.connect(
                                    host ='localhost',
                                    user = self.userName,
                                    password = self.passWord
                                    )
            create_billing_database = "CREATE DATABASE IF NOT EXISTS Billing"
            billing_database_cursor = self.bill.cursor()
            billing_database_cursor.execute(create_billing_database)

            # Crearte Table to save information
            self.bill = connector.connect(
                                    host ='localhost',
                                    user = self.userName,
                                    password = self.passWord,
                                    database = 'Billing'
                                    )
            create_info_table = """CREATE TABLE IF NOT EXISTS info(
                                                                   Bill_No int, 
                                                                   Products varchar(255), 
                                                                   Quantity int, 
                                                                   Subtotal float, 
                                                                   Tax float, 
                                                                   Amount float, 
                                                                   add_time varchar(255)
                                                                   )"""
            info_table_cursor = self.bill.cursor()
            info_table_cursor.execute(create_info_table)
            self.bill.commit()

            # Insert default information in 'info' table
            # ******************************************************************************        
            ''' Uncomment following block of code from line number 52 to 55.
            Note: It is necessary to insert follwing information in 'info' table for first time, else it will show an error of 'Invalid MySQL Syntax'. 
            Comment again the same block of code otherwise it will duplication of data in 'info' table'''
            # ****************************************************************************** 

            # insert_default_info_query = """INSERT INTO info VALUES (0, '0', 0, 0, 0, 0, '0')"""
            # default_info_cursor = self.bill.cursor()
            # default_info_cursor.execute(insert_default_info_query)
            # self.bill.commit()


            # Application Geometry
            width_of_application = 900     
            height_of_application = 600 
            actual_screen_width = tea.winfo_screenwidth() 
            actual_screen_height = tea.winfo_screenheight() 
            margin_in_x_direction = int((actual_screen_width/2) - (width_of_application/2))
            margin_in_y_direction = int((actual_screen_height/2) - (height_of_application/2))
            self.tea.geometry(f'{width_of_application}x{height_of_application}+{margin_in_x_direction}+{margin_in_y_direction-20}')
            self.tea.title("Amrut Tea Center")

            # Bill Number - 
            bill_number = "SELECT Bill_No FROM info ORDER BY Bill_No DESC LIMIT 1"
            bill_number_cursor = self.bill.cursor()
            bill_number_cursor.execute(bill_number)
            fetch_bill_number = bill_number_cursor.fetchone()
            new_bill_number = int(fetch_bill_number[0]) + 1

            # -----------------Variables and it's Data Types---------------------------
            self.bill_number = StringVar()
            self.bill_number.set(new_bill_number)
            self.product = StringVar()
            self.prices = DoubleVar()
            self.quantity = IntVar()
            self.subtotal = DoubleVar()
            self.gst = DoubleVar()
            self.total = DoubleVar()
            self.amt = StringVar()
            self.tax = DoubleVar()
            self.tot = DoubleVar()
            self.prodAmt = DoubleVar()


            # Menu List
            # Category
            self.menu = ["Select Option","Tea","Coffee","Milk","Water Bottle","Cream Roll"]
            # Food Products
            # Tea submenu:
            self.tea_sub_menu = ["Select Option","Regular Tea (s)","Regular Tea (M)","Ginger Tea","Lemon Tea","Black Tea","Sugar Free Tea"]
            self.Regular_smallQuantity_tea_price = 9.524     
            # tea, milk, coffee submenu and price
            self.coffee_sub_menu = ["Select Option","Hot Coffee","Cold Coffee"]
            self.milk_sub_menu = ["Select Option","Turmeric Milk","Almond Milk"]
            self.common_price = 19.048
            # water bottle submenu and pirce
            self.water_sub_menu = ["Select Quantity","Water Bottle (0.5 L)","Water Bottle (1 L)"]
            self.water_500ml_price = 9.524
            self.water_1litre_price = 19.048
            # cream roll submenu and pirce
            self.cream_roll_sub_menu = ["Select Size","Cream Roll (M)","Cream Roll (L)"]
            self.medium_cream_roll_price = 14.286
            self.large_cream_roll_price = 28.572

            #-----------------------------------------------------------
            # Primary Label
            label_title = Label(self.tea,text="Amrut Tea Center",font=("times new roman",35,"bold"),bg="yellow",fg="brown")
            label_title.place(x=150,y=15, width=600, height=60)   

            # Primary main Frame
            main_frame = Frame(self.tea,bd = 5,relief = GROOVE,bg="brown")  
            main_frame.place(x= 100, y= 100, width = 700, height = 480)

            #-----------------------------------------------------------
            # Menu Frame:
            menu_frame = LabelFrame(main_frame,bd=5,text="Menu",font=("times new roman",16,"italic"),bg="lightyellow",fg="brown")
            menu_frame.place(x= 35, y= 35, width= 300, height= 180)

            #---------------------------------------Product--------------------------------------------
            # Menu Label
            self.menu_name_label = Label(menu_frame,font=("times new roman",14,"bold"),bg="lightyellow",text="Menu",bd=5)
            self.menu_name_label.grid(row=0,column=0,sticky=W,padx=3,pady=2)
            # Menu List
            self.menu_list_box = ttk.Combobox(menu_frame,value=self.menu,font=("times new roman",12,"bold"),width=15,state="readonly")
            self.menu_list_box.current(0)  # Default option
            self.menu_list_box.grid(row=0,column=1,sticky=W,padx=3,pady=2)
            self.menu_list_box.bind("<<ComboboxSelected>>",self.submenu)    

            #---------------------------------------Product Name-------------------------------------       
            # Product name Label
            self.product_name_label = Label(menu_frame,font=("times new roman",11,"bold"),bg="lightyellow",text="Product Name",bd=5)
            self.product_name_label.grid(row=1,column=0,sticky=W,padx=3,pady=2)
            # Product List
            self.product_name_list_box = ttk.Combobox(menu_frame,textvariable=self.product,font=("times new roman",12,"bold"),width=15,state="readonly")
            self.product_name_list_box.grid(row=1,column=1,sticky=W,padx=3,pady=2)
            self.product_name_list_box.bind("<<ComboboxSelected>>",self.getprice)

            #----------------------------------------price_box-----------------------------------------  
            # Price Label
            self.price_name_label = Label(menu_frame,font=("times new roman",14,"bold"),bg="lightyellow",text="Price",bd=5)
            self.price_name_label.grid(row=2,column=0,sticky=W,padx=3,pady=2)
            # Price Box
            self.price_box = ttk.Combobox(menu_frame,state="readonly",textvariable=self.prices,font=("times new roman",12,"bold"),width=15)  #Entry = 'readonly'
            self.price_box.grid(row=2,column=1,sticky=W,padx=3,pady=2)
            
            #----------------------------------------Quantity----------------------------------------- 
            # Qty Label
            self.quantity_name_label = Label(menu_frame,font=("times new roman",14,"bold"),bg="lightyellow",text="Quantity",bd=5)
            self.quantity_name_label.grid(row=3,column=0,sticky=W,padx=3,pady=2)
            # Entry Quantity
            self.enter_quantity = ttk.Entry(menu_frame,textvariable=self.quantity,font=("times new roman",12,"bold"),width=15)
            self.enter_quantity.grid(row=3,column=1,sticky=W,padx=3,pady=2)


            #----------------------------Bill Counter Frame------------------------------------
            bill_counter_frame = LabelFrame(main_frame,bd=5,text="Bill Counter",font=("times new roman",16,"italic"),bg="lightyellow",fg="brown")
            bill_counter_frame.place(x= 35, y= 250, width= 300, height= 180)
            
            # 1.sub total label
            self.subtotallbl = Label(bill_counter_frame,font=("times new roman",14,"bold"),bg="lightyellow",text="Sub Total",bd=5)
            self.subtotallbl.grid(row=0,column=0,sticky=W,padx=3,pady=2)
            # 1.sub total Entry 
            self.subtotalent = ttk.Entry(bill_counter_frame,textvariable=self.subtotal,font=("times new roman",12,"bold"),width=20)
            self.subtotalent.grid(row=0,column=1,sticky=W,padx=3,pady=2)
            
            # 2. GST label
            self.gstlbl = Label(bill_counter_frame,font=("times new roman",14,"bold"),bg="lightyellow",text="GST",bd=5)
            self.gstlbl.grid(row=1,column=0,sticky=W,padx=3,pady=2)
            # 2. GST Entry 
            self.gstent = ttk.Entry(bill_counter_frame,textvariable=self.gst,font=("times new roman",12,"bold"),width=20)
            self.gstent.grid(row=1,column=1,sticky=W,padx=3,pady=2)
            
            # 3. Amount label
            self.amountlbl = Label(bill_counter_frame,font=("times new roman",14,"bold"),bg="lightyellow",text="Amount",bd=5)
            self.amountlbl.grid(row=2,column=0,sticky=W,padx=3,pady=2)
            # 3. Amount Entry 
            self.amountent = ttk.Entry(bill_counter_frame,textvariable=self.total,font=("times new roman",12,"bold"),width=20)
            self.amountent.grid(row=2,column=1,sticky=W,padx=3,pady=2)


            #-------------------------------Recipt Frame-----------------------------------------
            # Receipt frame in main frame
            receiptframe = LabelFrame(main_frame,bd=5,text="Receipt",font=("times new roman",16,"italic"),bg="white",fg="brown")
            receiptframe.place(x= 360, y= 35, width= 300, height= 235) 
            
            # scroll bar 
            scroll_y = Scrollbar(receiptframe,orient=VERTICAL)
            self.receiptarea = Text(receiptframe,yscrollcommand=scroll_y.set,bg="lightyellow",fg="black",font=("monospaced sans serif",9))
            scroll_y.pack(side=RIGHT,fill=Y)  # position of scroll bar
            scroll_y.config(command=self.receiptarea.yview)  # Joining scroll bar to receiptarea
            self.receiptarea.pack(fill=BOTH,expand=1)  # Pack
            self.receipt()  # call the receipt function
            self.l = []  # Blank list for items


            #-------------------------------Button Frame-----------------------------------------
            # Button frame in main frame
            buttonframe = LabelFrame(main_frame,bd=5,text="Buttons",font=("times new roman",14,"italic"),bg="white",fg="brown")
            buttonframe.place(x= 360, y= 305, width= 300, height= 125)
            # 1.Add Button
            self.addbtn = Button(buttonframe,command=self.additem,height=2,text="Add",font=("arial",10,"bold"),bg="orangered",fg="white",width=15,cursor="hand2")
            self.addbtn.grid(row=0,column=0,padx=3,pady=0)
            # 2.Clear Button
            self.clearbtn = Button(buttonframe,command=self.clear,height=2,text="Clear",font=("arial",10,"bold"),bg="orangered",fg="white",width=15,cursor="hand2")
            self.clearbtn.grid(row=0,column=1,padx=3,pady=3)
            # 3.Generate Bill Button
            self.generatebtn = Button(buttonframe,height=2,command=self.generatebill,text="Generate Bill",font=("arial",10,"bold"),bg="orangered",fg="white",width=15,cursor="hand2")
            self.generatebtn.grid(row=1,column=0,padx=7,pady=0)
            # 4.Exit Button  by using self.object.destroy command, no need to define function to exit application
            self.exitbtn = Button(buttonframe,command=self.tea.destroy,height=2,text="Exit",font=("arial",10,"bold"),bg="orangered",fg="white",width=15,cursor="hand2")
            self.exitbtn.grid(row=1,column=1,padx=7,pady=3)
        except Exception:
            print("Invalid Details! Close the Application and Try Again")


    def submenu(self,event=""):
        if self.menu_list_box.get() == "Tea":
            self.product_name_list_box.config(value=self.tea_sub_menu)
            self.product_name_list_box.current(0)
        if self.menu_list_box.get() == "Coffee":
            self.product_name_list_box.config(value=self.coffee_sub_menu)
            self.product_name_list_box.current(0)
        if self.menu_list_box.get() == "Milk":
            self.product_name_list_box.config(value=self.milk_sub_menu)
            self.product_name_list_box.current(0)
        if self.menu_list_box.get() == "Water Bottle":
            self.product_name_list_box.config(value=self.water_sub_menu)
            self.product_name_list_box.current(0)
        if self.menu_list_box.get() == "Cream Roll":
            self.product_name_list_box.config(value=self.cream_roll_sub_menu)
            self.product_name_list_box.current(0)


    def getprice(self,event=""):
        if self.product_name_list_box.get() == "Regular Tea (s)":
            self.price_box.config(value=self.Regular_smallQuantity_tea_price)
            self.price_box.current(0)
            self.quantity.set(1)
        if self.product_name_list_box.get() in ["Regular Tea (M)","Ginger Tea","Lemon Tea","Black Tea","Sugar Free Tea","Hot Coffee","Cold Coffee","Turmeric Milk","Almond Milk"]:
            self.price_box.config(value=self.common_price)
            self.price_box.current(0)
            self.quantity.set(1)
        if self.product_name_list_box.get() == "Water Bottle (0.5 L)":
            self.price_box.config(value=self.water_500ml_price)
            self.price_box.current(0)
            self.quantity.set(1)
        if self.product_name_list_box.get() == "Water Bottle (1 L)":
            self.price_box.config(value=self.water_1litre_price)
            self.price_box.current(0)
            self.quantity.set(1)
        if self.product_name_list_box.get() == "Cream Roll (M)":
            self.price_box.config(value=self.medium_cream_roll_price)
            self.price_box.current(0)
            self.quantity.set(1)
        if self.product_name_list_box.get() == "Cream Roll (L)":
            self.price_box.config(value=self.large_cream_roll_price)
            self.price_box.current(0)
            self.quantity.set(1)

    
    def receipt(self):
        self.receiptarea.delete(1.0,END)
        self.receiptarea.insert(END,f"\nBill Number: {self.bill_number.get()}")   
        self.receiptarea.insert(END,"\n*****************************************************")
        self.receiptarea.insert(END,f"\nProducts\t\tQty\tAmount")
        self.receiptarea.insert(END,"\n*****************************************************")


    def additem(self):
        self.time = datetime.datetime.now()
        self.gst1 = 5
        self.tot = (self.quantity.get()*self.prices.get())
        self.tax = (self.tot*self.gst1/100)
        self.prodAmt = (self.tot + self.tax)
        self.l.append(self.tot)
        if self.product.get() == "":
            messagebox.showerror("Error","Please select a item")
        else:
            amt = str('Rs. %.2f'%(((self.tot)+((self.tot))*self.gst1/100)))
            self.receiptarea.insert(END,f"\n{self.product.get()}\t\t{self.quantity.get()}\t{amt}")
            
            insert = """INSERT INTO info (Bill_No, Products, Quantity, Subtotal, Tax, Amount, add_time) 
            VALUES ({0},'{1}',{2},'{3}','{4}','{5}','{6}')""".format(self.bill_number.get(),
            self.product.get(), self.quantity.get(), self.tot, self.tax, self.prodAmt, self.time)
            
            i1 = self.bill.cursor()
            i1.execute(insert)
            self.bill.commit()
            self.subtotal.set(str('Rs. %.3f'%(sum(self.l))))
            self.gst.set(str('Rs. %.3f'%(((sum(self.l))*self.gst1/100))))
            self.total.set(str('Rs. %.2f'%(((sum(self.l))+(((sum(self.l))*self.gst1/100))))))


    def generatebill(self):
        if self.product.get() == "":
            messagebox.showerror("Error","Please add a item.")
        else:
            self.receiptarea.insert(END,"\n------------------------------------------------------------------")
            self.receiptarea.insert(END,f"\n\tSub Amount\t\t{'Rs. %.3f'%(sum(self.l))}")
            self.receiptarea.insert(END,f"\n\tGST Amount\t\t{'Rs. %.3f'%(((sum(self.l))*self.gst1/100))}")
            self.receiptarea.insert(END,"\n------------------------------------------------------------------")
            self.receiptarea.insert(END,f"\n\tTotal Amount\t\t{'Rs. %.2f'%(((sum(self.l))+(((sum(self.l))*self.gst1/100))))}")
            self.receiptarea.insert(END,"\n------------------------------------------------------------------")


    def clear(self):
        clear = "DELETE FROM info WHERE Bill_No = {0}".format(self.bill_number.get())
        c1 = self.bill.cursor()
        c1.execute(clear)
        self.bill.commit()

        bill_number = "SELECT Bill_No FROM info ORDER BY Bill_No DESC LIMIT 1"
        bill_number_cursor = self.bill.cursor()
        bill_number_cursor.execute(bill_number)
        fetch_bill_number = bill_number_cursor.fetchone()
        new_bill_number = int(fetch_bill_number[0]) + 1

        self.receiptarea.delete(1.0,END)
        self.bill_number.set(str(new_bill_number))
        self.product.set("")
        self.prices.set("0.0")
        self.quantity.set(0)
        self.subtotal.set("0.0")
        self.gst.set("0.0")
        self.total.set("0.0")
        self.amt.set("0.0")
        self.receipt()
        self.l = []

tea = Tk()
bills(tea,input("Enter MYSQL Server's Username:"),maskpass.askpass("\nEnter MYSQL Server's Password:"))
tea.mainloop()
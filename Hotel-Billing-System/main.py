from tkinter import *
from tkinter import ttk
import tkinter.messagebox as tmsg
import os
import time

#===================Python Variables=======================
menu_category = ["Tea & Coffee","Beverages","Fast Food","South Indian","Starters","Main Course","Dessert"]

menu_category_dict = {"Tea & Coffee":"1 Tea & Coffee.txt","Beverages":"2 Beverages.txt",
                "Fast Food":"3 Fast Food.txt","South Indian":"4 South Indian.txt",
                "Starters":"5 Starters.txt","Main Course":"6 Main Course.txt",
                "Dessert":"7 Dessert.txt"}

order_dict = {}
for i in menu_category:
    order_dict[i] = {}

os.chdir(os.path.dirname(os.path.abspath(__file__)))
#====================Backend Functions===========================
def load_menu():
    menuCategory.set("")
    menu_tabel.delete(*menu_tabel.get_children())
    menu_file_list = os.listdir("Menu")
    for file in menu_file_list:
        f = open("Menu\\" + file , "r")
        category=""
        while True:
            line = f.readline()
            if(line==""):
                menu_tabel.insert('',END,values=["","",""])
                break
            elif (line=="\n"):
                continue
            elif(line[0]=='#'):
                category = line[1:-1]
                name = "\t\t"+line[:-1]
                price = ""
            elif(line[0]=='*'):
                name = line[:-1]
                price = ""
            else:
                name = line[:line.rfind(" ")]
                price = line[line.rfind(" ")+1:-3]
            
            menu_tabel.insert('',END,values=[name,price,category])
        #menu_tabel.insert('',END,values=["Masala Dosa","50"])

def load_order():
    order_tabel.delete(*order_tabel.get_children())
    for category in order_dict.keys():
        if order_dict[category]:
            for lis in order_dict[category].values():
                order_tabel.insert('',END,values=lis)
    update_total_price()

def add_button_operation():
    name = itemName.get()
    rate = itemRate.get()
    category = itemCategory.get()
    quantity = itemQuantity.get()

    if name in order_dict[category].keys():
        tmsg.showinfo("Error", "Item already exist in your order")
        return
    if not quantity.isdigit():
        tmsg.showinfo("Error", "Please Enter Valid Quantity")
        return
    lis = [name,rate,quantity,str(int(rate)*int(quantity)),category]
    order_dict[category][name] = lis
    load_order()
    
def load_item_from_menu(event):
    cursor_row = menu_tabel.focus()
    contents = menu_tabel.item(cursor_row)
    row = contents["values"]

    itemName.set(row[0])
    itemRate.set(row[1])
    itemCategory.set(row[2])
    itemQuantity.set("1")

def load_item_from_order(event):
    cursor_row = order_tabel.focus()
    contents = order_tabel.item(cursor_row)
    row = contents["values"]

    itemName.set(row[0])
    itemRate.set(row[1])
    itemQuantity.set(row[2])
    itemCategory.set(row[4])

def show_button_operation():
    category = menuCategory.get()
    if category not in menu_category:
        tmsg.showinfo("Error", "Please select valid Choice")
    else:
        menu_tabel.delete(*menu_tabel.get_children())
        f = open("Menu\\" + menu_category_dict[category] , "r")
        while True:
            line = f.readline()
            if(line==""):
                break
            if (line[0]=='#' or line=="\n"):
                continue
            if(line[0]=='*'):
                name = "\t"+line[:-1]
                menu_tabel.insert('',END,values=[name,"",""])
            else:
                name = line[:line.rfind(" ")]
                price = line[line.rfind(" ")+1:-3]
                menu_tabel.insert('',END,values=[name,price,category])

def clear_button_operation():
    itemName.set("")
    itemRate.set("")
    itemQuantity.set("")
    itemCategory.set("")

def cancel_button_operation():
    names = []
    for i in menu_category:
        names.extend(list(order_dict[i].keys()))
    if len(names)==0:
        tmsg.showinfo("Error", "Your order list is Empty")
        return
    ans = tmsg.askquestion("Cancel Order", "Are You Sure to Cancel Order?")
    if ans=="no":
        return
    order_tabel.delete(*order_tabel.get_children())
    for i in menu_category:
        order_dict[i] = {}
    clear_button_operation()
    update_total_price()

def update_button_operation():
    name = itemName.get()
    rate = itemRate.get()
    category = itemCategory.get()
    quantity = itemQuantity.get()

    if category=="":
        return
    if name not in order_dict[category].keys():
        tmsg.showinfo("Error", "Item is not in your order list")
        return
    if order_dict[category][name][2]==quantity:
        tmsg.showinfo("Error", "No changes in Quantity")
        return
    order_dict[category][name][2] = quantity
    order_dict[category][name][3] = str(int(rate)*int(quantity))
    load_order()

def remove_button_operation():
    name = itemName.get()
    category = itemCategory.get()

    if category=="":
        return
    if name not in order_dict[category].keys():
        tmsg.showinfo("Error", "Item is not in your order list")
        return
    del order_dict[category][name]
    load_order()

def update_total_price():
    price = 0
    for i in menu_category:
        for j in order_dict[i].keys():
            price += int(order_dict[i][j][3])
    if price == 0:
        totalPrice.set("")
    else:
        totalPrice.set("Rs. "+str(price)+" /-")

def bill_button_operation():
    customer_name = customerName.get()
    customer_contact = customerContact.get()
    names = []
    for i in menu_category:
        names.extend(list(order_dict[i].keys()))
    if len(names)==0:
        tmsg.showinfo("Error", "Your order list is Empty")
        return
    if customer_name=="" or customer_contact=="":
        tmsg.showinfo("Error", "Customer Details Required")
        return
    if not customerContact.get().isdigit():
        tmsg.showinfo("Error", "Invalid Customer Contact")
        return   
    ans = tmsg.askquestion("Generate Bill", "Are You Sure to Generate Bill?")
    ans = "yes"
    if ans=="yes":
        bill = Toplevel()
        bill.title("Bill")
        bill.geometry("670x500+300+100")
        bill.wm_iconbitmap("hotel.ico")
        bill_text_area = Text(bill, font=("arial", 12))
        st = "\t\t\t\tT.V.S Hotel\n\t\t\tNear Radham center, Ap-522256\n"
        st += "\t\t\tGST.NO:- ABCDADADMA\n"
        st += "-"*61 + "BILL" + "-"*61 + "\nDate:- "

        #Date and time
        t = time.localtime(time.time())
        week_day_dict = {0:"Monday",1:"Tuesday",2:"Wednesday",3:"Thursday",4:"Friday",5:"Saturday",
                            6:"Sunday"}
        st += f"{t.tm_mday} / {t.tm_mon} / {t.tm_year} ({week_day_dict[t.tm_wday]})"
        st += " "*10 + f"\t\t\t\t\t\tTime:- {t.tm_hour} : {t.tm_min} : {t.tm_sec}"

        #Customer Name & Contact
        st += f"\nCustomer Name:- {customer_name}\nCustomer Contact:- {customer_contact}\n"
        st += "-"*130 + "\n" + " "*4 + "DESCRIPTION\t\t\t\t\tRATE\tQUANTITY\t\tAMOUNT\n"
        st += "-"*130 + "\n"

        #List of Items
        for i in menu_category:
            for j in order_dict[i].keys():
                lis = order_dict[i][j]
                name = lis[0]
                rate = lis[1]
                quantity = lis[2]
                price = lis[3]
                st += name + "\t\t\t\t\t" + rate + "\t      " + quantity + "\t\t  " + price + "\n\n"
        st += "-"*130

        #Total Price
        st += f"\n\t\t\tTotal price : {totalPrice.get()}\n"
        st += "-"*130

        #display bill in new window
        bill_text_area.insert(1.0, st)

        #write into file
        folder = f"{t.tm_mday},{t.tm_mon},{t.tm_year}"
        if not os.path.exists(f"Bill Records\\{folder}"):
            os.makedirs(f"Bill Records\\{folder}")
        file = open(f"Bill Records\\{folder}\\{customer_name+customer_contact}.txt", "w")
        file.write(st)
        file.close()

        #Clear operaitons
        order_tabel.delete(*order_tabel.get_children())
        for i in menu_category:
            order_dict[i] = {}
        clear_button_operation()
        update_total_price()
        customerName.set("")
        customerContact.set("")

        bill_text_area.pack(expand=True, fill=BOTH)
        bill.focus_set()
        bill.protocol("WM_DELETE_WINDOW", close_window)

def close_window():
    tmsg.showinfo("Thanks", "Thanks for using our service")
    root.destroy()
#[name,rate,quantity,str(int(rate)*int(quantity)),category]
#==================Backend Code Ends===============

#================Frontend Code Start==============
root = Tk()
w, h = root.winfo_screenwidth(), root.winfo_screenheight()
root.geometry("%dx%d+0+0" % (w, h))
root.title("T.V.S Hotel")
root.wm_iconbitmap("hotel.ico")
#root.attributes('-fullscreen', True)
#root.resizable(1920, 1080)

#================Title==============
style_button = ttk.Style()
style_button.configure("TButton",font = ("arial",10,"bold"),
   background="lightgreen")

title_frame = Frame(root, bd=8, bg="teal", relief=GROOVE)
title_frame.pack(side=TOP, fill="x")

title_label = Label(title_frame, text=" 🙏 🙏* * * *   T.V.S Hotel  * * * *     🙏 🙏", 
                    font=("Comic sans ms", 30, "bold"),bg = "teal", fg="white", pady=5)
title_label.pack()

#==============Customer=============
customer_frame = LabelFrame(root,text="Customer Details",font=("times new roman", 15, "bold"),
                            bd=8, bg="lightblue", relief=GROOVE)
customer_frame.pack(side=TOP, fill="x")

customer_name_label = Label(customer_frame, text="Name", 
                    font=("arial", 15, "bold"),bg = "lightblue", fg="blue")
customer_name_label.grid(row = 0, column = 0)

customerName = StringVar()
customerName.set("")
customer_name_entry = Entry(customer_frame,width=20,font="arial 15",bd=5,
                                textvariable=customerName)
customer_name_entry.grid(row = 0, column=1,padx=50)

customer_contact_label = Label(customer_frame, text="Contact", 
                    font=("arial", 15, "bold"),bg = "lightblue", fg="blue")
customer_contact_label.grid(row = 0, column = 2)

customerContact = StringVar()
customerContact.set("")
customer_contact_entry = Entry(customer_frame,width=20,font="arial 15",bd=5,
                                textvariable=customerContact)
customer_contact_entry.grid(row = 0, column=3,padx=50)

#===============Menu===============
menu_frame = Frame(root,bd=8, bg="grey", relief=GROOVE)
menu_frame.place(x=0,y=145,height=650,width=680)

menu_label = Label(menu_frame, text="Menu", 
                    font=("times new roman", 20, "bold"),bg = "teal", fg="white", pady=0)
menu_label.pack(side=TOP,fill="x")

menu_category_frame = Frame(menu_frame,bg="lavender",pady=10)
menu_category_frame.pack(fill="x")

combo_lable = Label(menu_category_frame,text="Select Type", 
                    font=("arial", 12, "bold"),bg = "lavender", fg="blue")
combo_lable.grid(row=0,column=0,padx=10)

menuCategory = StringVar()
combo_menu = ttk.Combobox(menu_category_frame,values=menu_category,
                            textvariable=menuCategory)
combo_menu.grid(row=0,column=1,padx=30)

show_button = ttk.Button(menu_category_frame, text="Show",width=10,
                        command=show_button_operation)
show_button.grid(row=0,column=2,padx=60)

show_all_button = ttk.Button(menu_category_frame, text="Show All",
                        width=10,command=load_menu)
show_all_button.grid(row=0,column=3)

############################# Menu Tabel ##########################################
menu_tabel_frame = Frame(menu_frame)
menu_tabel_frame.pack(fill=BOTH,expand=1)

scrollbar_menu_x = Scrollbar(menu_tabel_frame,orient=HORIZONTAL)
scrollbar_menu_y = Scrollbar(menu_tabel_frame,orient=VERTICAL)

style = ttk.Style()
style.configure("Treeview.Heading",font=("arial",13, "bold"))
style.configure("Treeview",font=("arial",12),rowheight=25)

menu_tabel = ttk.Treeview(menu_tabel_frame,style = "Treeview",
            columns =("name","price","category"),xscrollcommand=scrollbar_menu_x.set,
            yscrollcommand=scrollbar_menu_y.set)

menu_tabel.heading("name",text="Name")
menu_tabel.heading("price",text="Price")
menu_tabel["displaycolumns"]=("name", "price")
menu_tabel["show"] = "headings"
menu_tabel.column("price",width=50,anchor='center')

scrollbar_menu_x.pack(side=BOTTOM,fill=X)
scrollbar_menu_y.pack(side=RIGHT,fill=Y)

scrollbar_menu_x.configure(command=menu_tabel.xview)
scrollbar_menu_y.configure(command=menu_tabel.yview)

menu_tabel.pack(fill=BOTH,expand=1)


#menu_tabel.insert('',END,values=["Masala Dosa","50"])
load_menu()
menu_tabel.bind("<ButtonRelease-1>",load_item_from_menu)

###########################################################################################

#===============Item Frame=============
item_frame = Frame(root,bd=8, bg="grey", relief=GROOVE)
item_frame.place(x=680,y=145,height=250,width=830)

item_title_label = Label(item_frame, text="Item", 
                    font=("times new roman", 20, "bold"),bg = "teal", fg="white")
item_title_label.pack(side=TOP,fill="x")

item_frame2 = Frame(item_frame, bg="lavender")
item_frame2.pack(fill=X)

item_name_label = Label(item_frame2, text="Name", 
                    font=("arial", 12, "bold"),bg = "lavender", fg="blue")
item_name_label.grid(row=0,column=0)

itemCategory = StringVar()
itemCategory.set("")

itemName = StringVar()
itemName.set("")
item_name = Entry(item_frame2, font="arial 12",textvariable=itemName,state=DISABLED, width=25)
item_name.grid(row=0,column=1,padx=10)

item_rate_label = Label(item_frame2, text="Rate", 
                    font=("arial", 12, "bold"),bg = "lavender", fg="blue")
item_rate_label.grid(row=0,column=2,padx=40)

itemRate = StringVar()
itemRate.set("")
item_rate = Entry(item_frame2, font="arial 12",textvariable=itemRate,state=DISABLED, width=10)
item_rate.grid(row=0,column=3,padx=10)

item_quantity_label = Label(item_frame2, text="Quantity", 
                    font=("arial", 12, "bold"),bg = "lavender", fg="blue")
item_quantity_label.grid(row=1,column=0,padx=30,pady=15)

itemQuantity = StringVar()
itemQuantity.set("")
item_quantity = Entry(item_frame2, font="arial 12",textvariable=itemQuantity, width=10)
item_quantity.grid(row=1,column=1)

item_frame3 = Frame(item_frame, bg="lavender")
item_frame3.pack(fill=X)

add_button = ttk.Button(item_frame3, text="Add Item"
                        ,command=add_button_operation)
add_button.grid(row=0,column=0,padx=40,pady=30)

remove_button = ttk.Button(item_frame3, text="Remove Item"
                        ,command=remove_button_operation)
remove_button.grid(row=0,column=1,padx=40,pady=30)

update_button = ttk.Button(item_frame3, text="Update Quantity"
                        ,command=update_button_operation)
update_button.grid(row=0,column=2,padx=40,pady=30)

clear_button = ttk.Button(item_frame3, text="Clear",
                        width=8,command=clear_button_operation)
clear_button.grid(row=0,column=3,padx=40,pady=30)

#==============Order Frame=====================
order_frame = Frame(root,bd=8, bg="teal", relief=GROOVE)
order_frame.place(x=680,y=335,height=450,width=830)

order_title_label = Label(order_frame, text="Your Order", 
                    font=("times new roman", 20, "bold"),bg = "teal", fg="white")
order_title_label.pack(side=TOP,fill="x")

############################## Order Tabel ###################################
order_tabel_frame = Frame(order_frame)
order_tabel_frame.place(x=0,y=40,height=320,width=830)

scrollbar_order_x = Scrollbar(order_tabel_frame,orient=HORIZONTAL)
scrollbar_order_y = Scrollbar(order_tabel_frame,orient=VERTICAL)

order_tabel = ttk.Treeview(order_tabel_frame,
            columns =("name","rate","quantity","price","category"),xscrollcommand=scrollbar_order_x.set,
            yscrollcommand=scrollbar_order_y.set)

order_tabel.heading("name",text="Name")
order_tabel.heading("rate",text="Rate")
order_tabel.heading("quantity",text="Quantity")
order_tabel.heading("price",text="Price")
order_tabel["displaycolumns"]=("name", "rate","quantity","price")
order_tabel["show"] = "headings"
order_tabel.column("rate",width=100,anchor='center', stretch=NO)
order_tabel.column("quantity",width=100,anchor='center', stretch=NO)
order_tabel.column("price",width=100,anchor='center', stretch=NO)

order_tabel.bind("<ButtonRelease-1>",load_item_from_order)

scrollbar_order_x.pack(side=BOTTOM,fill=X)
scrollbar_order_y.pack(side=RIGHT,fill=Y)

scrollbar_order_x.configure(command=order_tabel.xview)
scrollbar_order_y.configure(command=order_tabel.yview)

order_tabel.pack(fill=BOTH,expand=1)

# order_tabel.insert('',END,text="HEllo",values=["Masala Dosa","50","2","100"])
###########################################################################################

total_price_label = Label(order_frame, text=" Total Price ", 
                    font=("arial", 12, "bold"),bg = "lawngreen", fg="black")
total_price_label.pack(side=LEFT,anchor=SW,padx=20,pady=10)

totalPrice = StringVar()
totalPrice.set("")
total_price_entry = Entry(order_frame, font="arial 12",textvariable=totalPrice,state=DISABLED, 
                            width=10)
total_price_entry.pack(side=LEFT,anchor=SW,padx=0,pady=10)

bill_button = ttk.Button(order_frame, text=" Bill ",width=8,
                        command=bill_button_operation)
bill_button.pack(side=LEFT,anchor=SW,padx=80,pady=10)

cancel_button = ttk.Button(order_frame, text=" Cancel Order ",command=cancel_button_operation)
cancel_button.pack(side=LEFT,anchor=SW,padx=20,pady=10)

root.mainloop()
#====================Frontend code ends=====================

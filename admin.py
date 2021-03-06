from tkinter import *
from db import Database
from tkinter import ttk
from tkinter import messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from PIL import ImageTk, Image


database = Database("database/water_database.db")


def center_window(root, width, height):
    positionRight = int(root.winfo_screenwidth() / 2 - width / 2)
    positionDown = int(root.winfo_screenheight() / 2 - height / 2 - 60)

    root.geometry("%dx%d+%d+%d" % (width, height, positionRight, positionDown))


class WinAdd:
    def __init__(self, root, frame_tables):
        self.frame_table = frame_tables
        self.root = root

        self.labels = []
        self.entries = []
        self.win_add = Toplevel(self.root)
        self.win_add.title('Adding Things')
        center_window(self.win_add, 400, 400)
        # self.win_add.geometry("400x400")
        self.win_add.resizable(False, False)
        self.add_bg = ImageTk.PhotoImage(Image.open("images//WinAddUpdate_admin.png")
                                         .resize((400, 400), Image.ANTIALIAS))
        self.sub_btn = ImageTk.PhotoImage(Image.open("images//Sub_btn_admin.png").resize((90, 30), Image.ANTIALIAS))
        self.frame = Label()
        self.frame_form = LabelFrame()
        self.btn_sub = Button()

    def draw(self):
        nb = self.frame_table.get_notebook()
        table_name = nb.tab(nb.select(), "text")
        print(table_name)

        self.frame_form.destroy()
        self.frame = Label(self.win_add, image=self.add_bg, bg="white", relief=FLAT)
        self.frame.place(x=0, y=0)
        self.frame_form = LabelFrame(self.frame, bg="#facbcb", relief=FLAT)
        self.frame_form.place(x=82, y=75)

        columns = database.get_col(table_name)
        i_row = 0

        for column in columns:
            lb = Label(self.frame_form, text=column, bg="#facbcb", font=("Calibri", 10))
            lb.grid(row=i_row, column=0, padx=5, pady=5)
            en = Entry(self.frame_form)
            en.grid(row=i_row, column=1, columnspan=4, padx=5, pady=5)

            self.labels.append(lb)
            self.entries.append(en)

            i_row += 1

        self.btn_sub = Button(self.frame_form, image=self.sub_btn, bg="#facbcb", relief=FLAT,
                              command=lambda: self.submit(table_name), activebackground="#facbcb")
        self.btn_sub.grid(row=i_row, columnspan=5, padx=10, pady=10)

    def submit(self, table_name):
        columns = database.get_col(table_name)
        duplicate = database.search_exact(table_name, columns[0], self.entries[0].get())
        if len(duplicate) == 0:
            records = []
            for entry in self.entries:
                records.append(entry.get())
                entry.delete(0, END)
            database.insert_gui(table_name, tuple(records))

            self.frame_table.redraw()
        else:
            messagebox.showwarning(title=None, message='Duplicated ID')


class WinUpdate:
    def __init__(self, root, frame_tables):
        self.frame_table = frame_tables
        self.root = root

        self.labels = []
        self.entries = []
        self.win_update = Toplevel(self.root)
        self.win_update.title('Update Things')
        center_window(self.win_update, 400, 400)
        # self.win_update.geometry("400x400")
        self.win_update.resizable(False, False)
        self.frame = Label()
        self.add_bg = ImageTk.PhotoImage(Image.open("images//WinAddUpdate_admin.png")
                                         .resize((400, 400), Image.ANTIALIAS))
        self.sub_btn = ImageTk.PhotoImage(Image.open("images//Sub_btn_admin.png").resize((90, 30), Image.ANTIALIAS))
        self.frame_form = LabelFrame()
        self.btn_sub = Button()

    def draw(self):
        row = self.frame_table.curr_row
        if len(row) == 0:
            self.win_update.destroy()
            messagebox.showwarning(title=None, message="Please pick a Record")
        else:
            nb = self.frame_table.get_notebook()
            table_name = nb.tab(nb.select(), "text")

            self.frame_form.destroy()
            self.frame = Label(self.win_update, image=self.add_bg, bg="white", relief=FLAT)
            self.frame.place(x=0, y=0)
            self.frame_form = LabelFrame(self.frame, bg="#facbcb", relief=FLAT)
            self.frame_form.place(x=82, y=75)

            columns = database.get_col(table_name)
            i_row = 0

            for column in columns:
                lb = Label(self.frame_form, text=column, bg="#facbcb", font=("Calibri", 10))
                lb.grid(row=i_row, column=0, padx=5, pady=5)
                en = Entry(self.frame_form)
                en.grid(row=i_row, column=1, columnspan=4, padx=5, pady=5)
                en.insert(END, row[i_row])
                if i_row == 0:
                    en['state'] = DISABLED
                self.labels.append(lb)
                self.entries.append(en)

                i_row += 1

            self.btn_sub = Button(self.frame_form, image=self.sub_btn, bg="#facbcb", relief=FLAT,
                                  command=lambda: self.submit(table_name), activebackground="#facbcb")
            self.btn_sub.grid(row=i_row, columnspan=5, padx=10, pady=10)

    def submit(self, table_name):
        records = []
        for entry in self.entries:
            records.append(entry.get())

        database.update(table_name, records, records[0])

        self.frame_table.redraw()

        print("To be Update: ", table_name, records)
        self.win_update.destroy()


class WinDelete:
    def __init__(self, root, frame_tables):
        self.frame_table = frame_tables
        self.root = root

    def draw(self):
        row = self.frame_table.curr_row
        if len(row) == 0:
            messagebox.showwarning(title=None, message='Please pick a Record')
        else:
            nb = self.frame_table.get_notebook()
            table_name = nb.tab(nb.select(), "text")

            response = messagebox.askquestion("Delete ?", "Do you want to delete ?")
            if response == 'yes':
                database.delete_row(table_name, row[0])

            self.frame_table.redraw()


class FrameSelectWinChart:
    def __init__(self, root):
        self.root = root
        self.fr_select = LabelFrame()
        self.cbx_values = []
        self.lb_select = Label()
        self.lb_type = Label()
        self.btn_show = Button()
        self.cbx_select = ttk.Combobox()
        self.cbx_type = ttk.Combobox()
        self.btn_done = Button()

    def draw(self, fr_chart, cbx_values):
        self.fr_select = LabelFrame(self.root, bg="#ffcccc", relief=FLAT)
        self.fr_select.place(x=50, y=40)
        self.cbx_values = cbx_values
        self.lb_select = Label(self.fr_select, text="Get Info About", bg="#ffcccc")
        self.lb_select.grid(row=0, column=0, padx=5, pady=5)
        self.cbx_select = ttk.Combobox(self.fr_select, width=25, values=self.cbx_values)
        self.cbx_select.grid(row=0, column=1, padx=5, pady=5, columnspan=2)
        self.cbx_select.current(0)

        self.lb_type = Label(self.fr_select, text="Type ", bg="#ffcccc")
        self.lb_type.grid(row=1, column=0, padx=5, pady=5)
        self.cbx_type = ttk.Combobox(self.fr_select, width=25,
                                     values=['gender (pie chart)', 'gender (bar chart)', 'designation'])
        self.cbx_type.grid(row=1, column=1, padx=5, pady=5, columnspan=2)
        self.cbx_type.current(0)

        self.cbx_select.bind("<<ComboboxSelected>>", lambda _: self.change_cbx_type(self.cbx_select.get()))

        self.btn_show = Button(self.fr_select, text="Show", bg="#ffcccc",
                               command=lambda: fr_chart.draw([self.cbx_select.get(), self.cbx_type.get()]))
        self.btn_show.grid(row=1, column=3, padx=5, pady=5)

    def change_cbx_type(self, selection):
        if selection == 'employee':
            self.cbx_type['values'] = ['gender (pie chart)', 'gender (bar chart)', 'designation']
        elif selection == 'household':
            self.cbx_type['values'] = ['num in each area']
        elif selection == 'area':
            self.cbx_type['values'] = ['num of each supplier']
        elif selection == 'billing':
            self.cbx_type['values'] = ['amount of water in each area',
                                       'amount of water of each supplier',
                                       'amount of money in each area',
                                       'amount of money of each supplier',
                                       ]

        self.cbx_type.current(0)


class FrameChartWinChart:
    def __init__(self, root, fr_select):
        self.root = root
        self.fr_select = fr_select
        self.fr_chart = LabelFrame()
        self.c_type = []

    def draw(self, c_type):
        plt.close('all')
        self.fr_chart.destroy()
        self.fr_chart = LabelFrame(self.root, bg="#ffcccc", relief=FLAT)
        self.fr_chart.place(x=50, y=180)
        self.c_type = c_type
        if c_type[0] == 'employee':
            if c_type[1] == 'gender (pie chart)':
                self.draw_chart_emp_gender_pie_chart()
            elif c_type[1] == 'gender (bar chart)':
                self.draw_chart_emp_gender_bar_chart()
            elif c_type[1] == 'designation':
                self.draw_chart_emp_designation()
        elif c_type[0] == 'household':
            if c_type[1] == 'num in each area':
                self.draw_chart_hh_in_area()
        elif c_type[0] == 'area':
            if c_type[1] == 'num of each supplier':
                self.draw_chart_area_of_supplier()
        elif c_type[0] == 'billing':
            if c_type[1] == 'amount of water in each area':
                self.draw_chart_bill_water_area()
            elif c_type[1] == 'amount of water of each supplier':
                self.draw_chart_bill_water_supplier()
            elif c_type[1] == 'amount of money in each area':
                self.draw_chart_bill_money_area()
            elif c_type[1] == 'amount of money of each supplier':
                self.draw_chart_bill_money_supplier()

    def draw_chart_emp_gender_pie_chart(self):
        f = plt.figure(figsize=(15, 6), dpi=60)
        f.patch.set_facecolor('#ffcccc')
        labels = database.column_unique('employee', 'sex')
        values = database.num_of_value('employee', [{'sex': labels}])

        plt.pie(values, labels=['Male', 'Female'], radius=1.5, autopct="%0.2f%%")

        canvas = FigureCanvasTkAgg(f, self.fr_chart)
        canvas.draw()
        canvas.get_tk_widget().pack()

    def draw_chart_emp_gender_bar_chart(self):
        f = plt.figure(figsize=(15, 6), dpi=60)
        f.patch.set_facecolor('#ffcccc')
        labels = database.column_unique('employee', 'sex')
        values = database.num_of_value('employee', [{'sex': labels}])

        plt.bar(labels, values)
        plt.xlabel("Gender")
        plt.ylabel("Number of Employees")
        plt.title("Gender")
        canvas = FigureCanvasTkAgg(f, self.fr_chart)
        canvas.draw()
        canvas.get_tk_widget().pack()

    def draw_chart_emp_designation(self):
        f = plt.figure(figsize=(15, 6), dpi=60)
        f.patch.set_facecolor('#ffcccc')
        labels = database.column_unique('employee', 'designation')
        values = database.num_of_value('employee', [{'designation': labels}])

        plt.bar(labels, values)
        plt.xlabel("Designation")
        plt.ylabel("Number of Employees")
        plt.title("Designation")

        canvas = FigureCanvasTkAgg(f, self.fr_chart)
        canvas.draw()
        canvas.get_tk_widget().pack()

    def draw_chart_hh_in_area(self):
        f = plt.figure(figsize=(15, 6), dpi=60)
        f.patch.set_facecolor('#ffcccc')
        ids = database.get_all_col_record_in_table('area', 0)
        labels = database.get_all_col_record_in_table('area', 1)
        values = []
        for id_ in ids:
            values.append(database.total_household_by_area(id_)[0])

        plt.bar(labels, values)
        plt.xlabel("Areas")
        plt.ylabel("Number of households")
        plt.title("Number of households in each area")

        canvas = FigureCanvasTkAgg(f, self.fr_chart)
        canvas.draw()
        canvas.get_tk_widget().pack()

    def draw_chart_area_of_supplier(self):
        f = plt.figure(figsize=(15, 6), dpi=60)
        f.patch.set_facecolor('#ffcccc')
        ids = database.get_all_col_record_in_table('supplier', 0)
        labels = database.get_all_col_record_in_table('supplier', 1)
        values = database.num_area_of_suppliers(ids)

        plt.bar(labels, values)
        plt.xlabel("Suppliers")
        plt.ylabel("Number of areas")
        plt.title("Number of areas of each supplier")

        canvas = FigureCanvasTkAgg(f, self.fr_chart)
        canvas.draw()
        canvas.get_tk_widget().pack()

    def draw_chart_bill_water_area(self):
        f = plt.figure(figsize=(15, 6), dpi=60)
        f.patch.set_facecolor('#ffcccc')
        supplier_ids = database.get_all_col_record_in_table('area', 0)
        results = database.values_consumed_by_suppliers_or_areas([{'area_id': supplier_ids}], "water_consumption")
        labels = database.get_all_col_record_in_table('area', 1)

        values = []
        for result in results:
            values.append(result[1])

        plt.bar(labels, values)
        plt.xlabel("Areas")
        plt.ylabel("Amount of water")
        plt.title("Water spent in each area")

        canvas = FigureCanvasTkAgg(f, self.fr_chart)
        canvas.draw()
        canvas.get_tk_widget().pack()

    def draw_chart_bill_water_supplier(self):
        f = plt.figure(figsize=(15, 6), dpi=60)
        f.patch.set_facecolor('#ffcccc')
        supplier_ids = database.get_all_col_record_in_table('supplier', 0)
        results = database.values_consumed_by_suppliers_or_areas([{'area_id': supplier_ids}], "water_consumption")
        labels = database.get_all_col_record_in_table('supplier', 1)

        values = []
        for result in results:
            values.append(result[1])

        plt.bar(labels, values)
        plt.xlabel("Suppliers")
        plt.ylabel("Amount of water")
        plt.title("Water supplied of each supplier")

        canvas = FigureCanvasTkAgg(f, self.fr_chart)
        canvas.draw()
        canvas.get_tk_widget().pack()

    def draw_chart_bill_money_area(self):
        f = plt.figure(figsize=(15, 6), dpi=60)
        f.patch.set_facecolor('#ffcccc')
        area_ids = database.get_all_col_record_in_table('area', 0)
        results = database.values_consumed_by_suppliers_or_areas([{'area_id': area_ids}], "total_money")
        labels = database.get_all_col_record_in_table('area', 1)

        values = []
        for result in results:
            values.append(result[1])

        plt.bar(labels, values)
        plt.xlabel("Areas")
        plt.ylabel("Amount of money")
        plt.title("Money spent in each area")

        canvas = FigureCanvasTkAgg(f, self.fr_chart)
        canvas.draw()
        canvas.get_tk_widget().pack()

    def draw_chart_bill_money_supplier(self):
        f = plt.figure(figsize=(15, 6), dpi=60)
        f.patch.set_facecolor('#ffcccc')
        supplier_ids = database.get_all_col_record_in_table('supplier', 0)
        results = database.values_consumed_by_suppliers_or_areas([{'area_id': supplier_ids}], "total_money")
        labels = database.get_all_col_record_in_table('supplier', 1)

        values = []
        for result in results:
            values.append(result[1])

        plt.bar(labels, values)
        plt.xlabel("Suppliers")
        plt.ylabel("Amount of money")
        plt.title("Money gain in each supplier")

        canvas = FigureCanvasTkAgg(f, self.fr_chart)
        canvas.draw()
        canvas.get_tk_widget().pack()

    def draw_chart_area(self):
        lb = Label(self.fr_chart, text="Area Chart")
        lb.pack()


class WinCharts:
    def __init__(self, root):
        self.root = root

        self.win_charts = Toplevel(self.root)
        center_window(self.win_charts, 1000, 600)
        # self.win_charts.geometry("1000x600")
        self.win_charts.title('Charts Things')
        self.win_charts.resizable(False, False)
        self.chart_bg = ImageTk.PhotoImage(Image.open("images//Chart_admin.png").resize((1000, 600), Image.ANTIALIAS))
        self.frame = Label(self.win_charts, image=self.chart_bg, bg="white", relief=FLAT)
        self.fr_select = FrameSelectWinChart(self.win_charts)
        self.fr_chart = FrameChartWinChart(self.win_charts, self.fr_select)
        self.frame.place(x=0, y=0)

    def draw(self):
        plt.close()
        cbx_values = ['employee', 'household', 'area', 'billing']

        self.fr_select.draw(self.fr_chart, cbx_values)
        self.fr_chart.draw(self.fr_select.cbx_select.get())

        self.win_charts.mainloop()


class FrameFeatures:
    def __init__(self, root, frame, frame_tables):
        self.root = root
        self.frame_tables = frame_tables
        self.frame = frame
        self.frame_features = LabelFrame(self.frame, text="Features", bg="#ffe6ee", width=1000)
        self.frame_features.pack(fill="both", expand=True)

        self.btn_add = Button()
        self.btn_update = Button()
        self.btn_delete = Button()
        self.btn_charts = Button()

    def draw(self):
        # Button Add
        self.btn_add = Button(self.frame_features, text='Add', width=12, height=1, bg="#ffb3cb",
                              command=self.add)
        self.btn_add.grid(row=0, column=0, padx=5, pady=5)

        # Button Update
        self.btn_update = Button(self.frame_features, text='Update', width=12, height=1, bg="#ffb3cb",
                                 command=self.update)
        self.btn_update.grid(row=0, column=1, padx=5, pady=5)

        # Button Delete
        self.btn_delete = Button(self.frame_features, text='Delete', width=12, height=1, bg="#ffb3cb",
                                 command=self.delete)
        self.btn_delete.grid(row=0, column=2, padx=5, pady=5)

        # Button Charts
        self.btn_charts = Button(self.frame_features, text='Chart', width=12, height=1, bg="#ffb3cb",
                                 command=self.charts)
        self.btn_charts.grid(row=0, column=3, padx=5, pady=5)

    def add(self):
        win_add = WinAdd(self.root, self.frame_tables)
        win_add.draw()

    def update(self):
        win_update = WinUpdate(self.root, self.frame_tables)
        win_update.draw()

    def delete(self):
        win_delete = WinDelete(self.root, self.frame_tables)
        win_delete.draw()

    def charts(self):
        win_charts = WinCharts(self.root)
        win_charts.draw()


class WinSearchResults:
    def __init__(self, root):
        self.root = root
        self.win_search_results = Toplevel(self.root, bg="#ffe6ee")
        self.win_search_results.title('Search Results')
        center_window(self.win_search_results, 700, 250)
        self.table_results = ttk.Treeview()

    def draw(self, table, by_column, opt, txt):
        self.table_results = ttk.Treeview(self.win_search_results)
        columns = database.get_col(table)
        self.table_results['columns'] = columns

        self.table_results.column('#0', width=0, stretch=NO)

        for column in columns:
            self.table_results.column(column, anchor=CENTER, width=105, minwidth=25)
            self.table_results.heading(column, text=column, anchor=CENTER)

        data_results = []
        if opt == 'exact':
            data_results = database.search_exact(table, by_column, txt)
        elif opt == 'contains':
            data_results = database.search(table, by_column, txt)

        count_area = 0
        for record in data_results:
            self.table_results.insert(parent='', index='end', iid=count_area, values=record)
            count_area += 1

        self.table_results.pack(fill='both', padx=10, pady=10)


class FrameSearch:
    def __init__(self, frame):
        # self.root = root
        self.frame = frame
        self.frame_search = LabelFrame(self.frame, text='Search', bg="#ffe6ee", width=1000)
        self.frame_search.pack(fill="both", expand=True)
        self.cbx_tbl_search = ttk.Combobox()
        self.cbx_col_search = ttk.Combobox()
        self.cbx_opt_search = ttk.Combobox()
        self.en_search = Entry()
        self.btn_search = Button()

    def draw(self, table_names):
        self.cbx_tbl_search = ttk.Combobox(self.frame_search, width=10, values=table_names)
        self.cbx_tbl_search.current(0)
        self.cbx_tbl_search.grid(row=0, column=0, padx=5, pady=5)
        self.cbx_tbl_search.bind("<<ComboboxSelected>>", lambda _: self.change_cbx_col())

        columns = database.get_col(table_names[0])
        self.cbx_col_search = ttk.Combobox(self.frame_search, width=10, values=columns)
        self.cbx_col_search.current(0)
        self.cbx_col_search.grid(row=0, column=1, padx=5, pady=5)

        self.cbx_opt_search = ttk.Combobox(self.frame_search, width=10, values=['exact', 'contains'])
        self.cbx_opt_search.current(0)
        self.cbx_opt_search.grid(row=0, column=2, padx=5, pady=5)

        self.en_search = Entry(self.frame_search, width=25)
        self.en_search.grid(row=0, column=3, padx=5, pady=5)
        self.btn_search = Button(self.frame_search, text='Search', bg="#ffb3cb", command=lambda: self.search())
        self.btn_search.grid(row=0, column=4, padx=5, pady=5)

    def search(self):
        curr_tbl = self.cbx_tbl_search.get()
        curr_col = self.cbx_col_search.get()
        curr_opt = self.cbx_opt_search.get()
        curr_txt = self.en_search.get()

        win_search_results = WinSearchResults(self.frame)
        win_search_results.draw(curr_tbl, curr_col, curr_opt, curr_txt)

    def change_cbx_col(self):
        columns = database.get_col(self.cbx_tbl_search.get())
        self.cbx_col_search['values'] = columns
        self.cbx_col_search.current(0)


class FrameTable:
    def __init__(self, frame, table_names):
        # self.root = root
        self.frame = frame
        self.frame_tables = LabelFrame()
        self.table_names = table_names

        self.notebook = ttk.Notebook()
        self.tabs = []
        self.tables = []
        self.btn_redraw = Button()

        self.curr_row = []

    def get_notebook(self):
        return self.notebook

    def draw(self):
        self.frame_tables = LabelFrame(self.frame, text="Tables", bg="#ffe6ee", width=1000, height=500)
        self.frame_tables.pack(fill="both", expand=True)

        self.notebook = ttk.Notebook(self.frame_tables)
        self.notebook.pack(pady=15)

        for table_name in self.table_names:
            self.draw_tab(table_name)

    def redraw(self):
        self.frame_tables.destroy()
        self.draw()

    def draw_tab(self, table_name):
        tab = Frame(self.notebook)
        tab.pack(fill="both", expand=True)

        self.draw_table(tab, table_name)

    def draw_table(self, tab, table_name):
        self.notebook.add(tab, text=table_name)

        tree_scroll = Scrollbar(tab)
        tree_scroll.pack(side=RIGHT, fill=Y)

        table = ttk.Treeview(tab, yscrollcommand=tree_scroll.set, selectmode="extended")
        tree_scroll.config(command=table.yview)
        columns = database.get_col(table_name)
        table['columns'] = columns

        # Draw Cols
        table.column('#0', width=0, stretch=NO)
        for column in columns:
            table.column(column, anchor=CENTER, width=115, minwidth=25)
            table.heading(column, text=column, anchor=CENTER)

        # Draw Data
        data = database.show_table(table_name)
        count = 0
        for record in data:
            table.insert(parent='', index='end', iid=count, values=record)
            count += 1

        table.bind('<ButtonRelease-1>', lambda _: self.track_row(table))
        table.pack(fill='both')

    def track_row(self, table):
        curItem = table.focus()
        self.curr_row = table.item(curItem)['values']


class FrameSetting:
    def __init__(self, root, username):
        self.root = root
        self.setting_frame = LabelFrame()
        self.username = username
        self.entries = []
        self.image_fr = ImageTk.PhotoImage(Image.open("images//Change_pass_admin.png")
                                           .resize((882, 475), Image.ANTIALIAS))
        self.sub_btn = ImageTk.PhotoImage(Image.open("images//Sub_btn_admin.png").resize((90, 30), Image.ANTIALIAS))
        self.draw()

    def draw(self):
        self.setting_frame = Label(self.root, image=self.image_fr, bg="white", relief=FLAT)
        self.setting_frame.place(x=300, y=126)

        record = database.search_exact('adminlogin', 'username', self.username)[0]

        user_entry = Entry(self.setting_frame, relief="flat", width=21, font=("Calibri", 12), bg="#f9cbdf")
        user_entry.place(x=340, y=180)
        user_entry.insert(0, record[0])
        user_entry['state'] = DISABLED
        self.entries.append(user_entry)

        pass_entry = Entry(self.setting_frame, relief="flat", width=21, font=("Calibri", 12), bg="#f9cbdf")
        pass_entry.place(x=340, y=260)
        pass_entry.insert(0, record[1])
        self.entries.append(pass_entry)

        btn_submit = Button(self.setting_frame, image=self.sub_btn, command=self.submit, relief=FLAT, bg="#f9cbdf",
                            activebackground="#f9cbdf")
        btn_submit.place(x=390, y=330)

    def submit(self):
        records = []
        for entry in self.entries:
            records.append(entry.get())

        database.update('adminlogin', records, records[0])

        print("To be Update: ", 'adminlogi ', records)

        messagebox.showinfo(title=None, message='Changing Password Successfully')


class AdminWindow:
    def __init__(self, admin):
        self.admin_id = admin
        self.admin_win = Tk()
        center_window(self.admin_win, 1300, 720)
        # self.admin_win.geometry("1300x720")

        self.admin_win.title('Welcome back: Admin!')
        self.fr_result = LabelFrame()
        # =======================Set background image=====================
        image_bg = ImageTk.PhotoImage(Image.open("images//Admin_bg.png").resize((1300, 720), Image.ANTIALIAS))
        canvas = Canvas(self.admin_win)
        canvas.pack(fill="both", expand=True)
        canvas.create_image(0, 0, image=image_bg, anchor="nw")

        # =======================Set button=====================
        btn_frame = LabelFrame(self.admin_win, height=300, width=184.689, bg="#ff4d4d", relief="flat")
        btn_frame.place(x=106, y=200)

        # Home button
        home_btn = Button(btn_frame, text="HOME", font=("arial", 10, "bold"), width=22,
                          bg="#ff4d4d", fg="white", relief=GROOVE,
                          command=self.click_home)
        home_btn.place(x=-1, y=0)
        # Manage button
        mana_btn = Button(btn_frame, text="MANAGE", font=("arial", 10, "bold"), width=22,
                          bg="#ff4d4d", fg="white", relief=GROOVE,
                          command=self.click_manage)
        mana_btn.place(x=-1, y=27)
        # Setting button
        setting_btn = Button(btn_frame, text="SETTING", font=("arial", 10, "bold"), width=22,
                             bg="#ff4d4d", fg="white", relief=GROOVE,
                             command=self.click_setting)
        setting_btn.place(x=-1, y=54)
        # Exit button
        exit_btn = Button(btn_frame, text="EXIT", font=("arial", 10, "bold"), width=22,
                          bg="#ff4d4d", fg="white", relief=GROOVE,
                          command=self.click_exit)
        exit_btn.place(x=-1, y=81)

        # =============================Log out panel=======================
        panel = LabelFrame(self.admin_win, width=800, height=40, bg="white", relief=FLAT)
        panel.place(x=356, y=65)

        welcome = Label(panel, text="Hello, Admin", font=("arial", 12), bg='white', fg="#ff4d4d")
        welcome.place(x=530, y=9)

        # Log out button
        logout_btn = Button(panel, text="Log Out", command=self.click_logout, relief=FLAT,
                            font=("arial", 10), bg='white', fg="#ff4d4d", activebackground="white")
        logout_btn.place(x=720, y=6)

        self.click_home()

        self.admin_win.mainloop()

    def draw(self):
        self.fr_result.destroy()
        self.fr_result = LabelFrame(self.admin_win, width=882, height=475, relief=FLAT, bg="white")
        self.fr_result.place(x=300, y=126)

    def click_home(self):
        home_bg = ImageTk.PhotoImage(Image.open("images//home_frame_admin.png").resize((882, 475), Image.ANTIALIAS))
        self.fr_result = Label(self.admin_win, image=home_bg, relief=FLAT, bg="white")
        self.fr_result.place(x=300, y=126)

        # =================Total households=================
        house_num = database.total_num('household')
        total_households = Label(self.fr_result, text=str(house_num), bg="#f6b2cf", fg="white", font=("arial", 25))
        total_households.place(x=243, y=118)

        # =================Total employees=================
        emp_num = database.total_num('employee')
        total_emps = Label(self.fr_result, text=str(emp_num), bg="#f6b2cf", fg="white", font=("arial", 25))
        total_emps.place(x=593, y=118)

        # =================Total suppliers=================
        sup_num = database.total_num('supplier')
        total_sups = Label(self.fr_result, text=str(sup_num), bg="#f6b2cf", fg="white", font=("arial", 25))
        total_sups.place(x=253, y=308)

        # ==================Total areas=====================
        area_num = database.total_num('area')
        total_areas = Label(self.fr_result, text=str(area_num), bg="#f6b2cf", fg="white", font=("arial", 25))
        total_areas.place(x=593, y=308)
        self.admin_win.mainloop()

    def click_manage(self):
        self.draw()
        table_names = ['supplier', 'household', 'employee', 'address', 'billing', 'area', 'service', 'servicetype']

        frame_tables = FrameTable(self.fr_result, table_names)

        frame_features = FrameFeatures(self.admin_win, self.fr_result, frame_tables)
        frame_features.draw()

        frame_search = FrameSearch(self.fr_result)
        frame_search.draw(table_names)

        frame_tables.draw()

    def click_setting(self):
        self.draw()
        FrameSetting(self.admin_win, self.admin_id)

    def click_logout(self):
        ask = messagebox.askyesnocancel("Confirm Logout", "Are you sure you want to Log Out")
        if ask is True:
            from water import Login
            self.admin_win.destroy()
            win = Tk()
            Login(win)

    def click_exit(self):
        self.admin_win.deiconify()
        ask = messagebox.askyesnocancel("Confirm Exit", "Are you sure you want to Exit?")
        if ask is True:
            self.admin_win.destroy()


if __name__ == '__main__':
    AdminWindow('admin')

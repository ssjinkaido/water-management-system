import sqlite3
import datetime
from sqlite3 import Error


class Database:
    def __init__(self, filename):
        self.db = sqlite3.connect(filename)
        self.cursorObj = self.db.cursor()
        self.cursorObj.execute("PRAGMA foreign_keys = ON")

    def login(self, username, password):
        try:
            self.cursorObj.execute(f"SELECT * FROM adminlogin WHERE username= '{username}' and password='{password}'")
            results = self.cursorObj.fetchone()
            self.db.commit()
            return results
        except Error as e:
            return e

    def search(self, table, search_by, search_txt):
        try:
            self.cursorObj.execute(f"SELECT * FROM {table} WHERE {search_by} LIKE '%{search_txt}%'")
            self.db.commit()
            return list(self.cursorObj.fetchall())
        except Error as e:
            return e

    def search_exact(self, table, search_by, search_txt):
        try:
            self.cursorObj.execute(f"SELECT * FROM {table} WHERE {search_by} LIKE '{search_txt}'")
            self.db.commit()
            return list(self.cursorObj.fetchall())
        except Error as e:
            return e

    def browse_table(self, table_name):
        self.cursorObj.execute("SELECT * FROM %s ORDER BY 1 ASC;" % table_name)
        colnames = [desc[0] for desc in self.cursorObj.description]
        results = self.cursorObj.fetchall()
        rows = []
        for result in results:
            rows.append(list(result))
        return colnames, rows

    def insert_gui(self, table, data):
        # data in the form of tuple
        try:
            self.cursorObj.execute(f"INSERT INTO {table} VALUES {data}")
            self.db.commit()
            return self.cursorObj.execute(f"SELECT * FROM {table}")
        except Error as e:
            return e

    def get_col_type(self, table_name):
        query = "pragma table_info({})".format(table_name)
        results = self.cursorObj.execute(query).fetchall()
        rows = []
        for result in results:
            rows.append(result[2])
        return rows

    def get_col(self, table_name):
        self.cursorObj.execute('SELECT * FROM {}'.format(table_name))
        names = list(map(lambda x: x[0], self.cursorObj.description))
        return names

    def get_all_col_record_in_table(self, tablename, col):
        self.cursorObj.execute(f'SELECT * from {tablename}')
        records = self.cursorObj.fetchall()
        results = []
        for record in records:
            results.append(record[col])
        return results

    def show_table(self, table):
        try:
            self.cursorObj.execute(f"SELECT * FROM {table}")
            return self.cursorObj.fetchall()
        except Error as e:
            return e

    def insert_area(self, area_id, name, emp_id):
        data = [(int(area_id), name, int(emp_id))]
        self.cursorObj.executemany("INSERT INTO area VALUES(?,?,?)", data)
        self.db.commit()

    def update(self, table, changes, id_):
        try:
            columns = self.get_col(table)
            for i in range(len(changes)):
                key = columns[i]
                value = changes[i]
                self.cursorObj.execute(f"UPDATE {table} SET {key} = '{value}' where {columns[0]} LIKE '{id_}'")
                self.db.commit()
        except Error as e:
            return e

    def join_two_tables(self, table1, table2, attributes):
        sql = f'''SELECT * from {table1} JOIN {table2} ON '''
        print(len(attributes))
        if len(attributes) > 1:
            for i in range(len(attributes) - 1):
                sql += f'''{table1}.{attributes[i]} = {table2}.{attributes[i]} AND '''

        sql += f'''{table1}.{attributes[len(attributes) - 1]} = {table2}.{attributes[len(attributes) - 1]}'''
        print(sql)
        self.cursorObj.execute(sql)
        self.cursorObj.fetchall()

    def list_tables(self):
        try:
            sql_outputs = self.cursorObj.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()
            result = []
            for output in sql_outputs:
                for elem in output:
                    result.append(elem)
            return result
        except Error as e:
            return e

    def delete_row(self, table_name, id):
        columns = self.get_col(table_name)
        self.cursorObj.execute(f"DELETE FROM {table_name} WHERE {columns[0]} LIKE '{id}'")
        self.db.commit()

    def delete_rows(self, table, conditions):
        # delete_row('household', [{'household_id': [1, 2]}]
        try:
            for condition in conditions:
                for key, value in condition.items:
                    command = f"DELETE FROM {table} WHERE {key} LIKE '{value}'"
                    self.cursorObj.execute(command)
                    self.db.commit()
        except Error as e:
            return e

    def get_water_company_name(self, customer_id):
        self.cursorObj.execute("SELECT supplier_name from supplier,"
                               "household,billing WHERE household.household_id=billing.household_id "
                               "and billing.household_id='{}'".format(customer_id))

        result = self.cursorObj.fetchone()
        self.db.commit()
        return result

    # print bill
    def get_information_bill(self, household_id):
        self.cursorObj.execute(
            "SELECT * from billing WHERE household_id = '{}'".format(household_id))
        rows = self.cursorObj.fetchone()
        water_company_name = self.get_water_company_name(household_id)[0]
        customer_info = self.select_specific_customer(household_id)
        print(customer_info)
        customer_name = customer_info[1]
        no = rows[0]
        cust_id = rows[1]
        total_amount = rows[5]
        from_date = rows[3]
        to_date = rows[4]
        water_amount = rows[2]
        bill_name = 'bill_' + str(no) + '.txt'
        m = ""
        m += "============================================================\n"
        m += "\n"
        m += "                Water Bill" + "    " + "Bill number: %d\n\n" % no
        m += "              Customer Id: %d\n\n" % cust_id
        m += "------------------------------------------------------------\n"
        m += water_company_name + "\n"
        m += "Customer name:" + "      " + customer_name + "\n"
        m += "Customer address:" + "   " + customer_info[3] + "\n"
        m += "Customer phone:" + "     " + customer_info[4] + "\n"
        m += "Time use water:" + "   " + from_date + " " + "to" + " " + to_date + "\n"
        m += "Amount of water used:" + "   " + str(water_amount) + "m3" + "\n"
        m += "Total money:" + "   " + str(total_amount) + "VND" + "\n"
        m += "\n"
        m += "                                       " + str(datetime.date.today()) + "\n"
        m += "                                       " + "Signature" + "\n"
        m += "                                     " + water_company_name + "\n"
        m += "============================================================\n"
        bill = open(bill_name, 'w')
        bill.write(m)
        bill.close()

    def value_consumed_by_household(self, type="water_consumption", year="", month=""):
        try:
            result = []
            command = f"""SELECT household_id, SUM({type}) FROM billing """

            condition = ""
            if year:
                condition = f" WHERE to_date LIKE \'%{year}"

                if month:
                    condition += f"-{month}%\'"
                else:
                    condition += f"%\'"

            command += condition + " GROUP BY household_id"

            for row in self.cursorObj.execute(command):
                result.append(row)

            return result
        except Error as e:
            return e

    def num_area_of_suppliers(self, suppliers):
        try:
            result = []
            for supplier in suppliers:
                command = f"SELECT SUM(CASE WHEN supplier_id = \'{supplier}\' THEN 1 ELSE 0 END) FROM area"
                for row in self.cursorObj.execute(command):
                    result.append(row[0])
            return result
        except Error as e:
            print(e)

    def num_of_value(self, table, conditions):
        try:
            result = []
            for condition in conditions:
                for key, values in condition.items():
                    for value in values:
                        command = f"SELECT SUM(CASE WHEN {key} = \'{value}\' THEN 1 ELSE 0 END) FROM {table}"
                        for row in self.cursorObj.execute(command):
                            result.append(row[0])
            return result
        except Error as e:
            return e

    def values_consumed_by_suppliers_or_areas(self, ids, type="water_consumption", year="", month=""):
        try:
            result = []
            for id in ids:
                for key, values in id.items():
                    for value in values:
                        command = f"""SELECT area.{key}, sum({type})
                                    FROM billing 
                                    INNER JOIN household 
                                    ON household.household_id = billing.household_id 
                                    INNER JOIN address
                                    ON address.address_id = household.address_id
                                    INNER JOIN area
                                    ON area.area_id = address.area_id 
                                    """
                        condition = f"WHERE area.{key} = '{value}'"

                        if year:
                            condition += f" AND to_date LIKE \'%{year}"

                            if month:
                                condition += f"-{month}%\'"
                            else:
                                condition += "%\'"

                        command += condition + f" GROUP BY area.{key}"

                        for item in self.cursorObj.execute(command):
                            result.append(item)
            return result
        except Error as e:
            return e

    def total_num(self, table):
        try:
            self.cursorObj.execute(f"SELECT COUNT(*) FROM {table}")
            result = self.cursorObj.fetchone()
            return result[0]
        except Error as e:
            return e

    def total_household_by_area(self, id):
        try:
            self.cursorObj.execute(f"""select count(household_owner), area.areaname from household 
                                   inner join address on household.address_id = address.address_id 
                                   inner join area on address.area_id = area.area_id 
                                   where area.area_id = {id}""")
            result = self.cursorObj.fetchone()
            return result
        except Error as e:
            return e

    def households_by_area(self, area_id):
        try:
            result = []
            for row in self.cursorObj.execute(
                    f"""SELECT household.household_id, household.household_owner,household.address_id, household.phone 
                           FROM address
                           INNER JOIN household
                           ON household.address_id = address.address_id
                           WHERE address.area_id = '{area_id}'"""):
                result.append(row)
            return result
        except Error as e:
            return e

    def total_area_by_supplier(self):
        try:
            self.cursorObj.execute("select supplier_name, count(distinct area.areaname) as total_district_supply "
                                   "from supplier, area, address "
                                   "where area.area_id = address.area_id "
                                   "and area.supplier_id = supplier.supplier_id "
                                   "group by area.supplier_id")
            result = self.cursorObj.fetchall()
            return result
        except Error as e:
            return e

    def total_employee_by_area(self, id):
        try:
            self.cursorObj.execute(f"select count(*) from employee where area_id = {id}")
            result = self.cursorObj.fetchone()
            return result
        except Error as e:
            return e

    def total_household_not_paid(self, id):
        try:
            self.cursorObj.execute("select area.areaname, count(is_paid) as total from household "
                                   "inner join address on household.address_id = address.address_id "
                                   "inner join area on address.area_id = area.area_id "
                                   "inner join billing on billing.household_id = household.household_id "
                                   f"where area.area_id = {id} and billing.is_paid=0")
            result = self.cursorObj.fetchone()
            return result
        except Error as e:
            return e

    def water_consumed_per_month_by_year(self, id, year):
        try:
            self.cursorObj.execute(f"""SELECT water_consumption, from_date FROM billing 
                                    WHERE household_id = {id}""")
            data = self.cursorObj.fetchall()
            water_amounts = []
            months = []
            for record in data:
                if record[1][0:4] == year:
                    water_amounts.append(record[0])
                    months.append(record[1][5:7])
            return months, water_amounts
        except Error as e:
            return e

    def money_consumed_per_month_by_year(self, id, year):
        try:
            self.cursorObj.execute(f"""SELECT total_money, from_date FROM billing 
                                    WHERE household_id = {id}""")
            data = self.cursorObj.fetchall()
            amount_of_money = []
            months = []
            for record in data:
                if record[1][0:4] == year:
                    amount_of_money.append(record[0])
                    months.append(record[1][5:7])
            return months, amount_of_money
        except Error as e:
            return e

    def get_customer_info(self):
        try:
            self.cursorObj.execute("SELECT household.household_id, household.household_owner, area.areaname,"
                                   "address.address_name FROM household "
                                   "INNER JOIN address ON household.address_id = address.address_id "
                                   "INNER JOIN area ON area.area_id = address.area_id")
            results = self.cursorObj.fetchall()
            return results
        except Error as e:
            return e

    def column_unique(self, table, column):
        try:
            result = []
            command = f"""SELECT DISTINCT({column}) FROM {table}"""
            for value in self.cursorObj.execute(command):
                result.append(value[0])
            return result
        except Error as e:
            return e

    def average_money_by_address(self, list):
        try:
            self.cursorObj.execute(
                "select address.address_id,round(avg(total_money),2) as average_money from billing,household,address "
                "where household.household_id=billing.household_id and address.address_id=household.address_id "
                "group by household.address_id;")
            result = self.cursorObj.fetchall()
            print(result)
            final_results = []
            for i in list:
                for j in result:
                    if i == j[0]:
                        final_results.append((i, j[1]))

            return final_results
        except Error as e:
            return e

    def average_money_by_household(self,list):
        try:
            self.cursorObj.execute(
                "select household.household_id,round(avg(total_money),2) from billing,household  "
                "where household.household_id=billing.household_id "
                "group by billing.household_id;")
            result = self.cursorObj.fetchall()
            final_results = []
            for i in list:
                for j in result:
                    if i == j[0]:
                        final_results.append((i, j[1]))

            return final_results
        except Error as e:
            return e

    def average_water_by_address(self,list):
        try:
            self.cursorObj.execute(
                "select address.address_id,round(avg(water_consumption),2) as average_money from billing,household,address "
                "where household.household_id=billing.household_id and address.address_id=household.address_id "
                "group by household.address_id;")
            result = self.cursorObj.fetchall()
            final_results = []
            for i in list:
                for j in result:
                    if i == j[0]:
                        final_results.append((i, j[1]))

            return final_results
        except Error as e:
            return e

    def average_water_by_household(self,list):
        try:
            self.cursorObj.execute(
                "select household.household_id,round(avg(water_consumption),2) from billing,household "
                "where household.household_id=billing.household_id "
                "group by billing.household_id;")
            result = self.cursorObj.fetchall()
            final_results = []
            for i in list:
                for j in result:
                    if i == j[0]:
                        final_results.append((i, j[1]))

            return final_results
        except Error as e:
            return e

    def max_billing(self):
        try:
            self.cursorObj.execute("select max(billing_id) from billing")
            result = self.cursorObj.fetchone()
            return result[0]
        except Error as e:
            return e

    def view_bill(self):
        try:
            self.cursorObj.execute("SELECT *, CASE WHEN is_paid = 1 THEN 'Yes' ELSE 'No' END as paid FROM billing")
            results = self.cursorObj.fetchall()
            return results
        except Error as e:
            return e

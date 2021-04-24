import mysql.connector

class MYSQL():
    def __init__(self):
        super(MYSQL, self).__init__()
        self.db_conn = None
        self.db_connectionId = None
        self.db_cursor = None

        self.db_databasesList = None
        self.db_tablesList = None

    def getdbconn(self):
        return self.db_conn

    def getdbconnectionid(self):
        return self.db_connectionId

    def getdbcursor(self):
        return self.db_cursor

    def connectToMySQLdb(self,hostname,username,password):
        try:
            self.db_conn=mysql.connector.connect(host=hostname,user=username,passwd=password)
            if(self.db_conn):
                self.db_connectionId=self.db_conn.connection_id
                self.db_cursor=self.db_conn.cursor()
                return self.db_connectionId
        except mysql.connector.Error as err:
            print("Something went wrong: {}".format(err))
            return 0



    def showdatabases(self):
        self.db_databasesList=[]
        self.db_cursor.execute("show databases")
        for cursor in self.db_cursor:
            self.db_databasesList.append(cursor[0])
        return self.db_databasesList

    def createdb(self,dbname):
        flag=0
        if dbname not in self.showdatabases():
            createdbQuery = "create database " + dbname
            self.db_cursor.execute(createdbQuery)
            self.db_conn.commit()
            #print("Database created Successfully :" + dbname)
            self.showdatabases()
            flag=1
        return flag

    def usedb(self,dbname):
        flag=0
        if dbname in self.showdatabases():
            usedbQuery = "use " + dbname
            self.db_cursor.execute(usedbQuery)
            self.db_conn.commit()
            #print("Database selected Successfully : " + dbname)
            flag=1
        return flag

    def showtables(self,dbname):
        self.db_tablesList=[]
        if dbname in self.showdatabases():
            self.db_cursor.execute("show tables")
            for cursor in self.db_cursor:
                self.db_tablesList.append(cursor[0])
        return self.db_tablesList

    def createtable(self,dbname,tbname,columnDataType):
        flag=0
        if dbname in self.showdatabases():
            if tbname not in self.showtables(dbname):
                createtbQuery = "create table " + tbname + "(" + columnDataType + ")"
                #print(createtbQuery)
                self.db_cursor.execute(createtbQuery)
                self.db_conn.commit()
                #print("table created Successfully : " + tbname)
                #if tbname in self.showtables(dbname):
                flag=1
        return flag

    def describetable(self,dbname,tbname):
        tableDescription=[]
        if dbname in self.showdatabases():
            if tbname in self.showtables(dbname):
                describetbQuery = "describe " + tbname
                #print("Description of : " + tbname + " is as follows:\n")
                self.db_cursor.execute(describetbQuery)
                #print("Field Type Null Default")
                tableDescription.append("Field\tType\tNull\tDefault")
                for cursor in self.db_cursor:
                    tableDescription.append("{}\t{}\t{}\t{}".format(cursor[0], cursor[1], cursor[2], cursor[4]))
        return tableDescription

    def insertInTable(self,dbname,tbname,DataValues):
        flag=0
        if dbname in self.showdatabases():
            if tbname in self.showtables(dbname):
                #describetb(tablename)
                InsertintbQuery = "insert into " + tbname + " values(" + DataValues + ")"
                self.db_cursor.execute(InsertintbQuery)
                self.db_conn.commit()
                #print("Data Inserted in " + tbname + "\n")
                flag=1
        return flag

    def showAllTableData(self,dbname,tbname):
        tableDataList=[]
        if dbname in self.showdatabases():
            if tbname in self.showtables(dbname):
                print("Data in table : " + tbname)
                showdatatbQuery = "select * from " + tbname
                self.db_cursor.execute(showdatatbQuery)
                for cursor in self.db_cursor:
                    tableDataList.append("{} {}".format(cursor[0], cursor[1]))
        return tableDataList

    def showAllTableDataFetchall(self,dbname,tbname):
        if dbname in self.showdatabases():
            if tbname in self.showtables(dbname):
                print("Data in table : " + tbname)
                showdatatbQuery = "select * from " + tbname
                self.db_cursor.execute(showdatatbQuery)

        return self.db_cursor.fetchall()

    def droptable(self,dbname,tbname):
        flag=0
        if dbname in self.showdatabases():
            if tbname in self.showtables(dbname):
                if(self.usedb(dbname)):
                    droptbQuery="DROP TABLE IF EXISTS "+tbname
                    self.db_cursor.execute(droptbQuery)
                    flag=1
        return flag



    def dropdatabase(self,dbname):
        flag=0
        if dbname in self.showdatabases():
            dropdbQuery = "drop database " + dbname
            self.db_cursor.execute(dropdbQuery)
            self.db_conn.commit()
            #print("Database deleted Successfully : " + dbname)
            flag=1
        return flag

    def closeConnection(self):
        self.db_conn.close()

    def UserQuery(self,query):

        uQuery = query
        uq=query.split(" ")
        self.db_cursor.execute(uQuery)
        if uq[0].lower() in ["insert","update","delete"]:
            self.db_conn.commit()
        #if else if finding type of query
        '''
        showdatabases
        create database
        use
        showtables
        create table
        describe
        select
        insert : commit
        update : commit
        delete : commit
        dropdb
        droptb
        '''

def trymain():
    sql = MYSQL()
    # Testcase 1,2
    if (sql.connectToMySQLdb('localhost', 'root', '') > 0):
        print("MySQL connected")
    # Testcase 3
    print("Database List\n", sql.showdatabases())
    # Testcase 4,5
    if (sql.createdb('pccoercse')):
        print("Database Created")
        print("Database List\n", sql.showdatabases())

    if (sql.usedb('pccoercse')):
        print("Selected Database")

    print("Table List\n", sql.showtables('pccoercse'))

    if (sql.createtable('pccoercse', 'BE', str("ID int, Name varchar(20)"))):
        print("Created Table")
        print("Table List\n", sql.showtables('pccoercse'))

    print("Table Description \n", sql.describetable('pccoercse', 'BE'.lower()))

    if (sql.insertInTable('pccoercse', 'BE'.lower(), "1 ,'Akash'")):
        print("Data Inserted")
    #insert many

    print("Table Data \n", sql.showAllTableData('pccoercse', 'BE'.lower()))

    if (sql.dropdatabase('pccoercse')):
        print("Database deleted")

    sql.closeConnection()

def nothing():
    pass

if __name__ == '__main__':
    #trymain()
    nothing()



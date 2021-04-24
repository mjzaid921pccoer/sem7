import unittest
from AppBackendMySQL import *

sql = MYSQL()
dbname='pccoercse'
tbname='be'
columnDataType="ID int, Name varchar(20)"
data1="1 ,'Akash'"

class MyTestCase(unittest.TestCase):
    def test_a0something(self):
        Expected=True
        Actual=True
        self.assertEqual(Expected,Actual)

    def test_a1connectToMySQLdb(self):
        status=sql.connectToMySQLdb('localhost', 'root', '')
        self.assertTrue(status>0,"Connected Successfully to MySQL")

    def test_a3showdatabases(self):
        #checking datatype list
        self.assertEqual(True,isinstance(sql.showdatabases(), list))

    def test_a4showdatabases(self):
        #checking size of list
        self.assertEqual(True,len(sql.showdatabases())>0)

    def test_a5createdb(self):
        self.assertEqual(1,sql.createdb(dbname))
        self.assertEqual(True,dbname in sql.showdatabases())

    def test_a6createdb(self):
        self.assertEqual(0,sql.createdb(dbname))
        self.assertEqual(True,dbname in sql.showdatabases())

    def test_a7usedb(self):
        self.assertEqual(1,sql.usedb(dbname))

    def test_a8usedb(self):
        self.assertEqual(0, sql.usedb("InvalidDatabase"))

    def test_a9showtables(self):
        self.assertEqual(True, isinstance(sql.showtables(dbname), list))

    def test_b0createtable(self):
        self.assertEqual(1,sql.createtable(dbname, tbname, columnDataType))

    def test_b1createtable(self):
        self.assertEqual(0, sql.createtable(dbname, tbname, columnDataType))

    def test_b2describetable(self):
        self.assertEqual(True, isinstance(sql.describetable(dbname, tbname), list))
        self.assertEqual(True, len(sql.describetable(dbname, tbname))>0)

    def test_b3insertInTable(self):
        self.assertEqual(True,sql.insertInTable(dbname, tbname, data1))

    def test_z8dropdatabase(self):
        self.assertEqual(True,sql.dropdatabase(dbname))

    def test_z9dropdatabase(self):
        self.assertEqual(False,sql.dropdatabase("InvalidDatabase"))


if __name__ == '__main__':
    unittest.main()

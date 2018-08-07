import pymysql
from DBUtils.PooledDB import PooledDB
"""
    mysql 连接池
"""
"""
mysqlInfo:数据库的配置文件
"""
mysqlInfo={
    'host':"localhost",
    'port' :  3306,
    'user' :  "root",
    'passwd' :  "admin",
    'db' :  "oneticket",
    'charset' :  "utf8"
}
class MySqlConn(object):

    __pool = None

    def __init__(self):
        # 构造函数，创建数据库连接、游标
        self.coon = MySqlConn.getmysqlconn()
        self.cur = self.coon.cursor(cursor=pymysql.cursors.DictCursor)

    # 数据库连接池连接
    @staticmethod
    def getmysqlconn():
        if MySqlConn.__pool is None:
            __pool = PooledDB(creator=pymysql, mincached=1, maxcached=20, host=mysqlInfo['host'], user=mysqlInfo['user'], passwd=mysqlInfo['passwd'], db=mysqlInfo['db'], port=mysqlInfo['port'], charset=mysqlInfo['charset'])
            # print(__pool)
        return __pool.connection()

    # 插入\更新\删除sql
    def op_insert(self, sql):
        print('op_insert', sql)
        insert_num = self.cur.execute(sql)
        print('mysql sucess ', insert_num)
        self.coon.commit()
        return insert_num

    # 查询
    def op_select(self, sql):
        # print('op_select', sql)
        self.cur.execute(sql)  # 执行sql
        select_res = self.cur.fetchone()  # 返回结果为字典
        print('op_select', select_res)
        return select_res

    #释放资源
    def dispose(self):
        self.coon.close()
        self.cur.close()

if __name__ == '__main__':
    #申请资源
    MC = MySqlConn()

    sql = "select * from orderInfo "
    res = MC.op_select(sql)
    #释放资源
    MC.dispose()

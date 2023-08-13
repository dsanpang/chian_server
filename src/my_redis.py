#!/usr/bin/env python

import redis


class MyRedis:

    def __init__(self, host, port, password):
        self.host = host
        self.port = port
        """每一个数据库实例管理一个连接池"""
        self.pool = redis.ConnectionPool(host=host, port=port, db=0, password=password, decode_responses=True)
        self.conn = redis.Redis(connection_pool=self.pool)

    def AllKeys(self):
        rd = redis.StrictRedis(connection_pool=self.pool)
        return rd.keys()

    def set(self, key, value):
        # 创建一个通道支持事务
        # pipe = self.conn.pipeline(transaction=True)

        # 写入一条数据
        return self.conn.set(key, value)

        # 执行
        # pipe.execute()

    def get(self, key):
        return self.conn.get(key)

    def delete(self, key):
        return  self.conn.delete(key)

    # 在最左边添加值conn.lpush('li', 11,22,33)
    def L_Push(self, key, values):
        return self.conn.lpush(key, values)

    def R_Push(self, key, values):
        return self.conn.rpush(key, values)

    def len(self, key):
        return self.conn.llen(key)

    def getRange(self, key, start, end):
        return self.conn.getrange(key, start, end)

    # 通过索引获取列表中的元素，可以使用负数下标，以 -1 表示列表的最后一个元素
    def LIndex(self, key, index):
        return self.conn.lindex(key, index)

    # 移出并获取列表的左侧第一个元素 如果列表没有元素会阻塞列表直到等待超时或发现可弹出元素为止
    def BLPop(self, key):
        if self.len(key) > 0:
            return self.conn.blpop(key)
        else:
            return []

    # 移出并获取列表的右侧第一个元素 如果列表没有元素会阻塞列表直到等待超时或发现可弹出元素为止
    def BRPop(self, key):
        if self.len(key) > 0:
            return self.conn.brpop(key)
        else:
            return []

    # 列表 key 中指定区间内的元素
    def page(self, key, page=1, size=10):
        start = (page - 1) * (size - 1)
        end = start + (size - 1)
        return self.conn.lrange(key, start, end)

    # 删除name集合中的values数据
    def sRem(self, key, values):
        return self.conn.srem(key, values)

    # 移除列表中与参数 VALUE 相等的元素，
    # count > 0 : 从表头开始向表尾搜索，移除与 VALUE 相等的元素，数量为 COUNT 。
    # count < 0 : 从表尾开始向表头搜索，移除与 VALUE 相等的元素，数量为 COUNT 的绝对值。
    # count = 0 : 移除表中所有与 VALUE 相等的值。
    # 返回被移除元素的数量。 列表不存在时返回 0
    def LRem(self, key, count, value):
        return self.conn.lrem(key, count, value)

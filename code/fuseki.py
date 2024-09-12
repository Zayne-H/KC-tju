"""
连接fuseki服务器
"""
from SPARQLWrapper import SPARQLWrapper, JSON
from collections import OrderedDict


class JenaFuseki:
    def __init__(self, endpoint_url='http://0.0.0.0:3030/kg_demo_movie/query'):  # 这里要改
        self.sparql_conn = SPARQLWrapper(endpoint_url)

    def get_sparql_result(self, query):
        # 设置要执行的SPARQL查询字符串
        self.sparql_conn.setQuery(query)

        # 设置查询结果的返回格式为JSON，这样结果可以方便地在多种编程环境中使用
        self.sparql_conn.setReturnFormat(JSON)

        # 执行查询并返回结果
        # convert()方法可能是将查询结果从内部格式转换为JSON格式
        return self.sparql_conn.query().convert()

    @staticmethod
    def parse_result(query_result):
        """
        解析返回的结果
        :param query_result:
        :return:
        """
        try:
            query_head = query_result['head']['vars']
            query_results = list()
            for r in query_result['results']['bindings']:
                temp_dict = OrderedDict()
                for h in query_head:
                    temp_dict[h] = r[h]['value']
                query_results.append(temp_dict)
            return query_head, query_results
        except KeyError:
            return None, query_result['boolean']

    def print_result_to_string(self, query_result):
        """
        直接打印结果，用于测试
        :param query_result:
        :return:
        """
        query_head, query_result = self.parse_result(query_result)

        if query_head is None:
            if query_result is True:
                print('Yes')
            else:
                print('False')
        else:
            for h in query_head:
                print(h, ' ' * 5, end="")
            print()
            for qr in query_result:
                for _, value in qr.items():
                    print(value, ' ', end="")
                print()

    def get_sparql_result_value(self, query_result):
        """
        用列表存储结果的值
        :param query_result:
        :return:
        """
        query_head, query_result = self.parse_result(query_result)
        if query_head is None:
            return query_result
        else:
            values = list()
            for qr in query_result:
                for _, value in qr.items():
                    values.append(value)
            return values

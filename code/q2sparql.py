import question,word
'''
将自然语言问题处理为sparql语句。将自然语言填空到模板sparql中
需要：
question.py：提供问题模板，并编写sparql语句模板
word.py：将自然语言切割成可用的word对象，以填入模板
'''



class Question2Sparql:
    def __init__(self, dict_paths):
        self.tw = word.Tagger(dict_paths)
        self.rules = question.rules

    def get_sparql(self, question):
        """
        进行语义解析，找到匹配的模板，返回对应的SPARQL查询语句
        :param question:
        :return:
        """
        word_objects = self.tw.get_word_objects(question)
        queries_dict = dict()

        for rule in self.rules:
            query, num = rule.apply(word_objects)

            if query is not None:
                queries_dict[num] = query

        if len(queries_dict) == 0:
            return None
        elif len(queries_dict) == 1:
            return list(queries_dict.values())[0]
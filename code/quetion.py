# encoding UTF-8
"""
这是一个多行注释。
你可以在这里写很多行，
它们都不会被执行。
"""
'''
本代码设置问题模板。将自然语言问题转化为可查询的SPARQL语句
模板内容如下：
1.某人
'''
from refo import finditer, Predicate, Star, Any, Disjunction
import re

SPARQL_PREXIX = u"""
PREFIX : <http://www.kgdemo.com#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
"""

SPARQL_SELECT_TEM = u"{prefix}\n" + \
                    u"SELECT DISTINCT {select} WHERE {{\n" + \
                    u"{expression}\n" + \
                    u"}}\n"

SPARQL_COUNT_TEM = u"{prefix}\n" + \
                   u"SELECT COUNT({select}) WHERE {{\n" + \
                   u"{expression}\n" + \
                   u"}}\n"

SPARQL_ASK_TEM = u"{prefix}\n" + \
                 u"ASK {{\n" + \
                 u"{expression}\n" + \
                 u"}}\n"


class W(Predicate):
    # 根据模式匹配单词的文本(token)和词性(pos);

    def __init__(self, token=".*", pos=".*"):
        self.token = re.compile(token + "$")
        self.pos = re.compile(pos + "$")
        super(W, self).__init__(self.match)

    def match(self, word):
        m1 = self.token.match(word.token)
        m2 = self.pos.match(word.pos)
        return m1 and m2


class Rule(object):
    def __init__(self, condition_num, condition=None, action=None):
        assert condition and action
        self.condition = condition
        self.action = action
        self.condition_num = condition_num

    def apply(self, sentence):
        matches = []
        for m in finditer(self.condition, sentence):
            i, j = m.span()
            matches.extend(sentence[i:j])

        return self.action(matches), self.condition_num


class KeywordRule(object):
    def __init__(self, condition=None, action=None):
        assert condition and action
        self.condition = condition
        self.action = action

    def apply(self, sentence):
        matches = []
        for m in finditer(self.condition, sentence):
            i, j = m.span()
            matches.extend(sentence[i:j])
        if len(matches) == 0:
            return None
        else:
            return self.action()

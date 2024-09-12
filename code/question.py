from refo import finditer, Predicate, Star, Any, Disjunction
import re

# encoding UTF-8
"""
这是一个多行注释。
你可以在这里写很多行，
它们都不会被执行。
"""
'''
本代码设置问题模板。将自然语言问题转化为可查询的SPARQL语句
模板内容如下：
1. XX会议的参会人员有谁？
2. XX会议包括什么内容？
3. XX会议发生于什么时间？
4. XX会议举办于什么地点？
5. XX人物就职于什么组织？
6. XX决议通过的内容有几个？
7. XX决议通过XX内容吗？
8. XX会议发生于XX时间吗？
9. XX人物就职于XX组织吗？
'''

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


# class KeywordRule(object):
#     def __init__(self, condition=None, action=None):
#         assert condition and action
#         self.condition = condition
#         self.action = action
#
#     def apply(self, sentence):
#         matches = []
#         for m in finditer(self.condition, sentence):
#             i, j = m.span()
#             matches.extend(sentence[i:j])
#         if len(matches) == 0:
#             return None
#         else:
#             return self.action()


class QuestionSet:
    def __init__(self):
        pass

    @staticmethod
    def meeting_attendees_question(word_objects):
        """
        XX会议的参会人员有谁？
        :param word_objects:
        :return:
        """
        select = u"?attendee"
        sparql = None
        for w in word_objects:
            if w.pos == pos_meeting:
                e = u"?meeting qap:参会人员 ?attendee .\n" \
                    u"FILTER (str(?meeting) = 'http://www.kbqa.com/{meeting}')".format(meeting=w.token)

                sparql = SPARQL_SELECT_TEM.format(prefix=SPARQL_PREXIX,
                                                  select=select,
                                                  expression=e)
                break
        return sparql

    @staticmethod
    def meeting_content_question(word_objects):
        """
        XX会议包括什么内容？
        :param word_objects:
        :return:
        """
        select = u"?content"
        sparql = None
        for w in word_objects:
            if w.pos == pos_meeting:
                e = u"?meeting qap:包括 ?content .\n" \
                    u"FILTER (str(?meeting) = 'http://www.kbqa.com/{meeting}')".format(meeting=w.token)

                sparql = SPARQL_SELECT_TEM.format(prefix=SPARQL_PREXIX,
                                                  select=select,
                                                  expression=e)
                break
        return sparql

    @staticmethod
    def meeting_time_question(word_objects):
        """
        XX会议发生于什么时间？
        :param word_objects:
        :return:
        """
        select = u"?time"
        sparql = None
        for w in word_objects:
            if w.pos == pos_meeting:
                e = u"?meeting qap:发生于 ?time .\n" \
                    u"FILTER (str(?meeting) = 'http://www.kbqa.com/{meeting}')".format(meeting=w.token)

                sparql = SPARQL_SELECT_TEM.format(prefix=SPARQL_PREXIX,
                                                  select=select,
                                                  expression=e)
                break
        return sparql

    @staticmethod
    def meeting_location_question(word_objects):
        """
        XX会议举办于什么地点？
        :param word_objects:
        :return:
        """
        select = u"?location"
        sparql = None
        for w in word_objects:
            if w.pos == pos_meeting:
                e = u"?meeting qap:举办于 ?location .\n" \
                    u"FILTER (str(?meeting) = 'http://www.kbqa.com/{meeting}')".format(meeting=w.token)

                sparql = SPARQL_SELECT_TEM.format(prefix=SPARQL_PREXIX,
                                                  select=select,
                                                  expression=e)
                break
        return sparql

    @staticmethod
    def person_organization_question(word_objects):
        """
        XX人物就职于什么组织？
        :param word_objects:
        :return:
        """
        select = u"?organization"
        sparql = None
        for w in word_objects:
            if w.pos == pos_person:
                e = u"?person qap:就职于 ?organization .\n" \
                    u"FILTER (str(?person) = 'http://www.kbqa.com/{person}')".format(person=w.token)

                sparql = SPARQL_SELECT_TEM.format(prefix=SPARQL_PREXIX,
                                                  select=select,
                                                  expression=e)
                break
        return sparql

    @staticmethod
    def resolution_content_count_question(word_objects):
        """
        XX决议通过的内容有几个？
        :param word_objects:
        :return:
        """
        select = u"?content"
        sparql = None
        for w in word_objects:
            if w.pos == pos_resolution:
                e = u"?resolution qap:包括 ?content .\n" \
                    u"FILTER (str(?resolution) = 'http://www.kbqa.com/{resolution}')".format(resolution=w.token)

                sparql = SPARQL_COUNT_TEM.format(prefix=SPARQL_PREXIX,
                                                 select=select,
                                                 expression=e)
                break
        return sparql

    @staticmethod
    def meeting_content_count_question(word_objects):
        """
        XX会议包括的内容有几个？
        :param word_objects:
        :return:
        """
        select = u"?content"
        sparql = None
        for w in word_objects:
            if w.pos == pos_meeting:
                e = u"?meeting qap:包括 ?content .\n" \
                    u"FILTER (str(?meeting) = 'http://www.kbqa.com/{meeting}')".format(meeting=w.token)

                sparql = SPARQL_COUNT_TEM.format(prefix=SPARQL_PREXIX,
                                                 select=select,
                                                 expression=e)
                break
        return sparql

    @staticmethod
    def resolution_passed_question(word_objects):
        """
        XX决议通过XX内容吗？
        :param word_objects:
        :return:
        """
        sparql = None
        for w in word_objects:
            if w.pos == pos_resolution:
                e = u"?resolution qap:通过 ?content .\n" \
                    u"FILTER (str(?resolution) = 'http://www.kbqa.com/{resolution}')".format(resolution=w.token)

                sparql = SPARQL_ASK_TEM.format(prefix=SPARQL_PREXIX, expression=e)
                break
        return sparql

    @staticmethod
    def meeting_happened_at_time_question(word_objects):
        """
        XX会议发生于XX时间吗？
        :param word_objects:
        :return:
        """
        sparql = None
        for w in word_objects:
            if w.pos == pos_meeting:
                e = u"?meeting qap:发生于 'http://www.kbqa.com/{time}' .\n" \
                    u"FILTER (str(?meeting) = 'http://www.kbqa.com/{meeting}')".format(meeting=w.token, time=w.token)

                sparql = SPARQL_ASK_TEM.format(prefix=SPARQL_PREXIX, expression=e)
                break
        return sparql

    @staticmethod
    def person_employed_at_organization_question(word_objects):
        """
        XX人物就职于XX组织吗？
        :param word_objects:
        :return:
        """
        sparql = None
        for w in word_objects:
            if w.pos == pos_person:
                e = u"?person qap:就职于 'http://www.kbqa.com/{organization}' .\n" \
                    u"FILTER (str(?person) = 'http://www.kbqa.com/{person}')".format(person=w.token,
                                                                                     organization=w.token)

                sparql = SPARQL_ASK_TEM.format(prefix=SPARQL_PREXIX, expression=e)
                break
        return sparql


# 定义关键词
pos_meeting = "pm"
pos_person = "pp"
pos_resolution = "pr"

# 用于装载Rule指令
person_entity = (W(pos=pos_person))
meeting_entity = (W(pos=pos_meeting))
resolution_entity = (W(pos=pos_resolution))
_time = (W("时间"))
contain_content = (W("包含"))
held = (W("举办"))
engaged = (W("就职"))
conference = (W("会议") | W("决议"))
announce = (W("宣布"))
count = (W("多少") | W("几个"))
judge = (W("么") | W("吗"))
yon = (W("是否") | W("有没有"))
occurred = (W("发生"))
worked = (W("就职"))
organization = (W("组织"))
'''
本代码设置问题模板。将自然语言问题转化为可查询的SPARQL语句
模板内容如下：
1. XX会议的参会人员有谁？
2. XX会议包括什么内容？
3. XX会议发生于什么时间？
4. XX会议举办于什么地点？
5. XX人物就职于什么组织？
6. XX决议通过的内容有几个？
7. XX决议通过XX内容吗？
8. XX会议发生于XX时间吗？
9. XX人物就职于XX组织吗？
'''
rules = [
    Rule(condition_num=2, condition=meeting_entity + Star(Any(), greedy=False) + pos_person + Star(Any(), greedy=False),
         action=QuestionSet.meeting_attendees_question)
    , Rule(condition_num=3,
           condition=meeting_entity + Star(Any(), greedy=False) + contain_content + Star(Any(), greedy=False),
           action=QuestionSet.meeting_content_question)
    , Rule(condition_num=4, condition=meeting_entity + Star(Any(), greedy=False) + _time + Star(Any(), greedy=False),
           action=QuestionSet.meeting_time_question)
    , Rule(condition_num=4, condition=meeting_entity + Star(Any(), greedy=False) + held + Star(Any(), greedy=False),
           action=QuestionSet.meeting_location_question)
    , Rule(condition_num=2, condition=person_entity + Star(Any(), greedy=False) + engaged + Star(Any(), greedy=False),
           action=QuestionSet.person_employed_at_organization_question)
    , Rule(condition_num=2,
           condition=meeting_entity + conference + Star(Any(), greedy=False) + announce + (
                   count | Star(Any(), greedy=False)),
           action=QuestionSet.meeting_content_count_question)
    , Rule(condition_num=3, condition=meeting_entity + conference + (yon | Star(Any(), greedy=False))
                                      + Star(Any(), greedy=False) + judge,
           action=QuestionSet.resolution_passed_question)
    , Rule(condition_num=2, condition=meeting_entity + occurred + Star(Any(), greedy=False) + _time
           , action=QuestionSet.meeting_happened_at_time_question)
    , Rule(condition_num=3,
           condition=person_entity + Star(Any(), greedy=False) + worked + Star(Any(), greedy=False) + organization
           , action=QuestionSet.person_organization_question)
]

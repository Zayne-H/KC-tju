'''
功能：使用jieba切割自然语言，添加字典，并返回word对象的列表
'''
import jieba
import jieba.posseg as pseg


class Word(object):
    def __init__(self, token, pos):
        self.token = token
        self.pos = pos


class Tagger:
    def __init__(self, dict_paths):
        # TODO 加载外部词典
        for p in dict_paths:
            jieba.load_userdict(p)
            # 将我们自己的字典导入到jieba字典中

        # TODO jieba不能正确切分的词语，我们人工调整其频率。
        # jieba.suggest_freq(('喜剧', '电影'), True)

    @staticmethod
    def get_word_objects(sentence):
        # type: (str) -> list
        """
        把自然语言转为Word对象
        :param sentence:
        :return:
        """
        return [Word(word, tag) for word, tag in pseg.cut(sentence)]


# TODO 用于测试
# if __name__ == '__main__':
#     tagger = Tagger(['./external_dict/movie_title.txt', './external_dict/person_name.txt'])
#     while True:
#         s = input('>>')
#         for i in tagger.get_word_objects(s):
#             print(i.token, i.pos)
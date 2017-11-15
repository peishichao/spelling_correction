# coding:utf-8

import re
from collections import Counter


def words(text):
    return re.findall(r'\w+', text.lower())


'''
语言模型：我们通过统计一个百万级词条的文本big.txt中各单词出现的频率来估计P(w)，
它的数据来源于古腾堡项目中公共领域的书摘，以及维基词典中频率最高的词汇，
还有英国国家语料库，函数words(text)将文本分割为词组，
并统计每个词出现的频率保存在变量WORDS中，P基于该统计评估每个词的概率：
'''
# 统计词频
WORDS = Counter(words(open('big.txt').read()))


def P(word, N=sum(WORDS.values())):
    """词'word'的概率"""
    return float(WORDS[word]) / N

'''
调用correction(w)函数将试图选出对于词w最有可能的拼写纠正单词，
概率学上我们是无法预知应该选择哪一个的（例如，"lates"应该被纠正为"late"还是"latest"或"latters"...？）。
对于给定的原始词w，我们试图在所有可能的候选集合中，找出一个概率最大的修正结果c。
'''
def correction(word):
    """最有可能的纠正候选词"""
    return max(candidates(word), key=P)


def candidates(word):
    """生成拼写纠正词的候选集合"""
    return (known([word]) or known(edits1(word)) or known(edits2(word)) or [word])

'''
然而，如果我们限制单词为已知(known，译者：即存在于WORDS字典中的单词)，
那么这个单词集合将显著缩小：
'''
def known(words):
    """'words'中出现在WORDS集合的元素子集"""
    return set(w for w in words if w in WORDS)



'''
该程序的4个部分：
    1.选择机制：在Python中，带key的max()函数即可实现argmax的功能。
    2.候选模型：先介绍一个新概念：对一个单词的简单编辑是指：
    删除(移除一个字母)、置换(单词内两字母互换)、替换(单词内一个字母改变)、插入(增加一个字母)。
    函数edits1(word)返回一个单词的所有简单编辑（译者：称其编辑距离为1）的集合，
    不考虑编辑后是否是合法单词:
'''
def edits1(word):
    """与'word'的编辑距离为1的全部结果"""
    letters    = 'abcdefghijklmnopqrstuvwxyz'
    splits     = [(word[:i], word[i:])     for i in range(len(word) + 1)]
    deletes    = [L + R[1:]                for L, R in splits if R]
    transposes = [L + R[1] + R[0] + R[2:]  for L, R in splits if len(R) > 1]
    replaces   = [L + c + R[1:]            for L, R in splits for c in letters]
    inserts    = [L + c + R                for L, R in splits for c in letters]
    return set(deletes + transposes + replaces + inserts)

'''
我们也需要考虑经过二次编辑得到的单词
（译者：“二次编辑”即编辑距离为2，此处作者巧妙运用递归思想，
将函数edits1返回集合里的每个元素再次经过edits1处理即可得到），
这个集合更大，但仍然只有很少一部分是已知单词：
'''
def edits2(word):
    """与'word'的编辑距离为2的全部结果"""
    return (e2 for e1 in edits1(word) for e2 in edits1(e1))

if __name__ == "__main__":
    print(correction('korrectud'))
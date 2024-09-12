# KC-tju
基于模板匹配的知识库查询系统

文件夹介绍：
data:用于存放查询所需要的csv文件以及转化来的外部字典
  csv2txt:将单列csv文件（仅一种实体）转换为txt文件并插入分词标记
code:项目的核心代码
  p2sparql:将自然语言重构为可使用的sparql查询语句
  question:设计问题模板，并编写sparql语句模板
  word:导入外部字典，将传入的自然语言切割
  main:主程序

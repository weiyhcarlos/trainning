# -*- coding: UTF-8 -*-

#在输入最后追加一个空行
def lines(file):
    for line in file:yield line
    yield '\n'

#将输入按照空行分割成块
def blocks(file):
    block = []
    for line in lines(file):
        if line.strip():
            block.append(line)
        elif block:
            yield ''.join(block).strip()
            block = []

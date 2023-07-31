from tqdm import trange
import pickle
from prettytable import PrettyTable
import time

print("Loading...")
with open(r"./yuedict.pickle", "rb") as f:
    yuedict = pickle.load(f)
print("广州音字典加载成功!")
with open(r"./vsqxDict.pickle", "rb") as f:
    vsqxdict = pickle.load(f)
with open(r"./vsqxDict2.pickle", "rb") as f:
    vsqxdictb = pickle.load(f)
print("VOCALOID发音符号字典加载成功!")
tab = PrettyTable(["字", "粤语拼音", "发音符号"])


def find(text):
    o = ''
    for i in yuedict.items():
        spe = 0
        if text in i[0]:
            for n in "‘’“”：；，。、·~？（）【】":
                if n in i[0]:
                    spe = spe+i[0].count(n)
            try:
                o = i[1][i[0].index(text)-spe]
                break
            except:
                pass
    if o.startswith("{"):
        o = o[1:]
    if o.endswith("}"):
        o = o[:len(o)-1]
    return o


def conv(text, tab):
    yin = ""
    output = []
    voices = {}
    yin = find(text)
    yue_word = yin[0:len(yin)-1]
    tmp = []
    for x in range(len(yue_word)+1):
        for y in range(len(yue_word)+1):
            tmp.append(yue_word[x:y])
    for i in list(set(tmp)):
        try:
            voices[i] = (vsqxdict[i])
        except:
            try:
                voices[i] = (vsqxdictb[i])
            except:
                pass
    tmp = voices
    for a in list(voices.items()):
        for b in list(voices.items()):
            if a[0] in b[0] and a[0] != b[0]:
                try:
                    del tmp[a[0]]
                except:
                    pass
    nums = {}
    n = []
    for i in list(voices.items()):
        nums[(yin.index(i[0]))] = i[1]
        n.append(yin.index(i[0]))
    n.sort()
    for i in n:
        output.append(nums[i])
    out = ''
    for o in output:
        out = out+" "+o
    if out != "":
        tab.add_row([text, yin, out])
        return True


text = str(input("请输入需要转换的文字:"))
f = time.time()
o = []
for i in trange(len(text)):
    o.append(conv(text[i], tab))
print(tab)
print("耗时:{}s".format(time.time()-f))
print("输入{}字，共翻译{}字,翻译率{}%".format(
    len(text), o.count(True), o.count(True)/len(text)*100))

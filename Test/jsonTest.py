import json
import collections as cl

def main():
    name_list = ["honoka", "eri", "kotori", "umi", "rin", "maki", "nozomi", "hanayo", "niko"]
    fw = open('../data/data.json', 'w')
    tmpDic = json.load(fw)
    ys = json.dump(tmpDic)

    height = [157,162,159,159,155,161,159,156,154]
    BWH = [[78, 58, 82],[88, 60, 84],[80, 58, 80],[76, 58, 80],
           [75, 59, 80],[78, 56, 83],[90, 60, 82],[82, 60, 83],[74, 57, 79]]

    ys = cl.OrderedDict()
    for i in range(len(name_list)):
        data = cl.OrderedDict()
        data["BWH"] = BWH[i]
        data["height"] = height[i]

        ys[name_list[i]] = data

    #print("{}".format(json.dumps(ys,indent=4)))

    # fw = open('../data/data.json','w')
    #ココ重要！！
    # json.dump関数でファイルに書き込む
    json.dump(ys,fw,indent=4)

    # f = open("../data/data.json", 'r')
    #
    # # ココ重要！！
    # json_data = json.load(f)  # JSON形式で読み込む
    #
    # name_list = ["honoka", "eri", "kotori", "umi", "rin", "maki", "nozomi", "hanayo", "niko"]
    # for name in name_list:
    #     print("{0:6s} 身長：{1}cm BWH: ".format(name, json_data[name]["height"]), end="\t")
    #     for i in range(len(json_data[name]["BWH"])):
    #         print("{}".format(json_data[name]["BWH"][i]), end="\t")
    #     print()
    fw.close()

if __name__=='__main__':
    # main()
    f = open("../data/data.json", 'r')
    json_data = json.load(f)

    # ココ重要！！
    # インデントありで表示
    # print("{}".format(json.dumps(json_data, indent=4)))

    f.close()

    with open('../data/data.json', mode='w') as f2:
        json_data["pppp"] = {
            "oo":"",
            "":"xvsd"
        }

        f2.write(str(json.dumps(json_data,indent=4)))

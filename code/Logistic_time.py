import numpy as np
import sys
import matplotlib.pyplot as plt
import time
from matplotlib.font_manager import FontProperties
import os


# Logistic映射函数
def logistic_map(mu, x):
    return mu * x * (1 - x)


# 计算 x_{M+1} 到 x_{M+N} 迭代结果并存储到列表中
def diedai_M_to_N(M, N, mu, x_0):
    # 迭代计算 x_M
    x = x_0
    diedai_list = []
    # 先计算到M
    for _ in range(M):
        x = logistic_map(mu, x)

    for _ in range(N):
        x = logistic_map(mu, x)
        diedai_list.append(x)
    return diedai_list


# 存储 x_{M+1} 到 x_{M+N} 到txt文件
def save_diedai_list(M, N, diedai_list):
    file_path1 = "D:/x_M+1~x_M+N_data.txt"
    with open(file_path1, "w") as file:
        for val in diedai_list:
            file.write(str(val) + "\n")
    print(f"x_{M + 1} 到 x_{M + N} 的迭代运算结果已存储至 {file_path1}")


# 对列表数据进行排序
def sort_list(diedai_list):
    sorted_diedai_list = sorted(diedai_list)
    return sorted_diedai_list


# 置乱处理
def scramble(N, sorted_diedai_list, diedai_list):
    scrambled_diedai_list = [0] * N
    for i, val in enumerate(diedai_list):
        j = sorted_diedai_list.index(val)
        scrambled_diedai_list[j] = sorted_diedai_list[i]
    return scrambled_diedai_list


# 将置乱后的数据存入txt文件
def save_scrambled_list(scrambled_diedai_list):
    file_path2 = "D:/scrambled_diedai_data.txt"
    with open(file_path2, "w") as file:
        for val in scrambled_diedai_list:
            file.write(str(val) + "\n")
    print(f"经排序并置乱后的数据已存储至 {file_path2}")


# 判断一个数组中是否有重复元素
def has_repetition(list):
    seen = set()
    flag1 = 0
    for num in list:
        if num in seen:
            if flag1 == 0:
                print("数组中有重复元素！(说明数据不安全也不适用喔，建议换一下μ和x0,稍微换个一下两下就好了😀)\n")
                flag1 = 1
        seen.add(num)
    if flag1 == 0:
        print("数组中没有重复元素！(可以放心进行后续的置乱操作)\n")
    if flag1 == 1:
        find_repetition(list)
    return flag1


def has_repetition2(list):
    seen = set()
    flag1 = 0
    for num in list:
        if num in seen:
            if flag1 == 0:
                flag1 = 1
        seen.add(num)
    return flag1


# 查找重复元素
def find_repetition(list):
    element_positions = {}
    for idx, elem in enumerate(list):
        if elem in element_positions:
            # 如果元素已经在字典中，则说明重复了
            element_positions[elem].append(idx)
        else:
            # 否则将元素添加到字典中
            element_positions[elem] = [idx]

    for elem, positions in element_positions.items():
        if len(positions) > 1:
            print(f"元素{elem}在列表中重复出现，其位置为{', '.join(map(str, positions))}")


# 查找循环第一次出现的位置，并返回循环圈长度
def find_first_position_cycle(list):
    element_positions = {}
    flag1 = 0
    while flag1 == 0:
        for idx, elem in enumerate(list):
            if elem in element_positions:
                if flag1 != 1:
                    flag1 = 1
                    element_positions[elem].append(idx)
            else:
                # 否则将元素添加到字典中
                element_positions[elem] = [idx]
        for elem, positions in element_positions.items():
            if len(positions) > 1:
                return np.abs(positions[1] - positions[0])


# 查找两个数组在相同位置元素是否相同，如果有，就返回这个位置
def find_same_elements_at_same_position(list1, list2):
    positions = []
    for i in range(len(list1)):
        if list1[i] == list2[i]:
            positions.append(i)
    return positions


def generate_lists(N):
    # 创建一个字典来存储列表
    lists = {}
    # 生成N个列表，并自动命名
    for i in range(1, N + 1):
        lists[f'list{i}'] = []
    return lists


# 计算该置乱表的循环阶并存储在列表中
def compute_cycle_length(N, scrambled_diedai_list):
    cycle_lengths = [0] * N  # 存储各元素的循环圈(没用到，不用看)
    scramble_temp1 = [0] * N  # 在置乱过程中需要两个中间数组来存储置乱结果，在置乱过程中对照中间数组和原始数组来求循环圈长度
    scramble_temp2 = [0] * N  # 这是第二个中间数组
    sorted_temp_list = [0] * N  # 每次置乱都需要排序，这是存储排序结果的数组
    flag_list = [0] * N  # 判断该元素是否已经经过置乱回到其初始位置了，如果已经回去了，就不用再求其循环长度了
    # 生成N个列表，用于存放x_i的路径(i从1到N)
    # 创建一个空的字典来存储列表
    lists = generate_lists(N)
    for i in range(1, N + 1):
        lists[f'list{i}'].append(i)
    print("初始的记录元素路径的列表如下：")
    for i in range(1, N + 1):
        print(f'list{i}:', lists[f'list{i}'])
    print("\n")

    # 先对scrambled_diedai_list做一次置乱并存储在scramble_temp1中
    sorted_temp_list = sort_list(scrambled_diedai_list)
    scramble_temp1 = scramble(N, sorted_temp_list, scrambled_diedai_list)
    for i, val in enumerate(scrambled_diedai_list):
        j = scramble_temp1.index(val)
        lists[f'list{i + 1}'].append(j + 1)
        if has_repetition2(lists[f'list{i + 1}']) == 1:
            cycle_lengths[i] = 2
            flag_list[i] = 1

    # 再对scramble_temp1做置乱并存储在scramble_temp2中
    # sorted_temp_list = sort_list(scramble_temp1)
    scramble_temp2 = scramble(N, scramble_temp1, scrambled_diedai_list)

    for i, val in enumerate(scrambled_diedai_list):
        j = scramble_temp2.index(val)
        lists[f'list{i + 1}'].append(j + 1)
        if flag_list[i] != 1:
            if has_repetition2(lists[f'list{i + 1}']) == 1:
                cycle_lengths[i] = 3
                flag_list[i] = 1

    # 接下来就是对scramble_temp1和scramble_temp2重复进行置乱操作，直至flag_list数组全部变为1
    i = 0
    while 0 in flag_list:
        if i % 2 == 0:
            # sorted_temp_list = sort_list(scramble_temp2)
            scramble_temp1 = scramble(N, scramble_temp2, scrambled_diedai_list)
            for i, val in enumerate(scrambled_diedai_list):
                j = scramble_temp1.index(val)
                lists[f'list{i + 1}'].append(j + 1)
                if flag_list[i] != 1:
                    if has_repetition2(lists[f'list{i + 1}']) == 1:
                        cycle_lengths[i] = i + 4
                        flag_list[i] = 1

        if i % 2 != 0:
            # sorted_temp_list = sort_list(scramble_temp1)
            scramble_temp2 = scramble(N, scramble_temp1, scrambled_diedai_list)
            for i, val in enumerate(scrambled_diedai_list):
                j = scramble_temp2.index(val)
                lists[f'list{i + 1}'].append(j + 1)
                if flag_list[i] != 1:
                    if has_repetition2(lists[f'list{i + 1}']) == 1:
                        cycle_lengths[i] = i + 4
                        flag_list[i] = 1

        i += 1
    print("flag_list已全部为1，结束while循环\n")
    # end while
    return lists, cycle_lengths


# 统计有多少种长度的循环圈，每种长度的循环圈有多少个，以及总的循环阶
def cycle_situation_function(list):
    # 使用字典统计每个元素的出现次数
    counts = {}
    count_jie = 0
    for item in list:
        if item in counts:
            counts[item] += 1
        else:
            counts[item] = 1

    # 输出结果
    unique_values = sorted(counts.keys())  # 将唯一值排序
    num_unique_values = len(unique_values)
    print(f"该置乱中共有{num_unique_values}种循环长度，分别为：{', '.join(map(str, unique_values))}")
    for value in unique_values:
        count = counts[value]
        print(f"循环长度为{value}的有{count}个")
        count_jie += count * value
    print("\n")
    print(f"总的循环长度(阶)为：{count_jie}")
    print("\n")
    return count_jie


def main(N, x_0, mu):
    M = 1000

    # 计算x_{M+1} 到 x_{M+N}并存储到列表中
    diedai_list = diedai_M_to_N(M, N, mu, x_0)

    print("x_{M+1}到x_{M+N}的运算结果如下：")
    print(diedai_list)
    print("\n")

    # 下面一段为画图输出混沌情况的，可以在第一次测试中打开看一下，后面ctrl+/在这一段前加上#就行了，不然会输出很多图浪费时间
    #
    # plt.rcParams['font.sans-serif'] = ['SimHei']
    # plt.figure()
    # plt.plot(diedai_list, '.')
    # plt.xlabel('维度')
    # plt.ylabel('混沌值')
    # plt.figure()
    # plt.hist(diedai_list)
    # plt.xlabel('混沌值')
    # plt.ylabel('频数')
    # plt.show()

    # 判断列表中是否有重复元素
    has_repetition(diedai_list)

    # 将M to N计算结果存储到txt文件中，如果不需要存储就把下面一行 # 就行
    # save_diedai_list(M, N, diedai_list)

    # 对列表进行排序
    sorted_diedai_list = sort_list(diedai_list)

    # 根据排序结果对列表进行置乱
    scrambled_diedai_list = scramble(N, sorted_diedai_list, diedai_list)

    # 将置乱后的数据存入txt文件中，如果不需要存储就把下面一行 #  就行
    # save_scrambled_list(scrambled_diedai_list)

    # 计算置乱表的循环阶并存储在列表中
    lists, cycle_lengths = compute_cycle_length(N, scrambled_diedai_list)

    # 输出置乱表的元素路径
    print("以下为结束时各元素的路径：")
    for i in range(1, N + 1):
        print(f'list{i}:', lists[f'list{i}'])
    print("\n")

    # 输出置乱表的循环阶
    cycle_situation = []
    for i in range(N):
        index = find_first_position_cycle(lists[f'list{i + 1}'])
        print(f"置乱表第{i + 1}个元素的循环圈长度为：{index}")
        cycle_situation.append(index)
    print("\n")
    count_jie = cycle_situation_function(cycle_situation)
    return count_jie


if __name__ == "__main__":
    print("欢迎使用Logistic混沌映射！")
    print("================================================")
    # 用户输入 参数
    N = int(input("请输入 N 值(大于200最好哦): "))
    x_0 = float(input("请输入初始值 x_0 (0<x<1): "))
    # 用户输入参数
    mu = float(input("请输入参数μ值 (3.57 < μ < 4): "))
    # 记录程序开始时间
    start_time = time.time()
    main(N, x_0, mu)

    print("================================")
    print("现在需要固定N,更换初始值x0,并计算出平均阶；以及更改N，并作出平均阶-N的曲线；我们把这两步融合一下：")
    # 创建一个空列表
    jie_list = []
    ave_jie_N = []
    num=5
    x_0_list = [0.86, 0.29, 0.61, 0.74, 0.35]
    # 询问用户要输入多少个值
    # num = int(input("请输入要输入的x_0值的数量："))
    # 使用循环获取用户输入的值并添加到列表中
    # for i in range(num):
    #     value = float(input("请输入第 {} 个值(也是在0到1之间哦)：".format(i + 1)))
    #     x_0_list.append(value)

    print("接下来会重复上面的操作，即置乱求循环圈等:\n")
    # 保存原始的 stdout
    original_stdout = sys.stdout
    # 将 stdout 重定向到空文件（即丢弃所有的输出）
    sys.stdout = open('nul', 'w')
    for i in range(num):
        result = main(N, x_0_list[i], mu)
        jie_list.append(result)
    # 恢复原始的 stdout
    sys.stdout = original_stdout
    print(f"各x_0的循环阶为：{jie_list}")
    print(f"平均阶为{sum(jie_list) / num}")
    print("================================")
    print("接下来是利用上述输入的几个x_0,更改N的值，重复上述操作，求出平均阶，并作出平均阶-N的曲线:\n")
    print("我们固定步长为1，将N从N-100到N+100来进行操作，您可以根据自己输入的N以及需求更改N的数量：\n")
    lists_N = generate_lists(200)
    # 保存原始的 stdout
    original_stdout = sys.stdout
    # 将 stdout 重定向到空文件（即丢弃所有的输出）
    sys.stdout = open('nul', 'w')
    for i in range(N - 100, N + 100):
        for j in range(num):
            result = main(i, x_0_list[j], mu)
            lists_N[f'list{i - N + 101}'].append(result)
        ave_jie_N.append(sum(lists_N[f'list{i - N + 101}']) / num)
    # 恢复原始的 stdout
    sys.stdout = original_stdout
    print(f"改变N的平均阶分别为：+{ave_jie_N}")
    print(len(ave_jie_N))
    # 计算程序运行的实际时间（去除用户输入的时间）
    end_time = time.time()
    elapsed_time = end_time - start_time

    print("程序运行的时间为：", elapsed_time, "秒")
    # print("接下来是绘制平均阶-N曲线：")
    # # 计算y-x并绘制曲线
    # N_list = []
    # for i in range(N - 100, N + 100):
    #     N_list.append(i)

    # 设置中文字体，以便显示中文标题
    # plt.rcParams['font.sans-serif'] = ['SimHei']  # 使用黑体作为中文字体
    # plt.rcParams['axes.unicode_minus'] = False  # 解决保存图像是负号'-'显示为方块的问题
    #
    # # 绘制曲线
    # plt.plot(N_list, ave_jie_N, label='平均阶关于N的曲线')
    #
    # # 添加标题和标签
    # plt.title('平均阶关于N的曲线')
    # plt.xlabel('N')
    # plt.ylabel('平均阶')
    #
    # # 添加图例
    # plt.legend()
    #
    # # 显示图形
    # plt.show()

import numpy as np
import sys
from PIL import Image
import random
import math

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



if __name__ == "__main__":
    print("欢迎使用Logistic混沌映射！")
    print("================================================")
    # 用户输入 参数
    # N = int(input("请输入 N 值(大于200最好哦): "))
    # x_0 = float(input("请输入初始值 x_0 (0<x<1): "))
    # 用户输入参数
    mu = float(input("请输入参数μ值 (3.57 < μ < 4): "))


    num = 100
    # 生成100个随机初始种子，范围为0到1，保留两位小数(用户可以自己修改)
    x_0_list = [round(random.uniform(0, 1), 2) for _ in range(100)]
    lists2 = generate_lists(num)

    # 加载图像
    image_path = 'D:/pic.png'
    image = Image.open(image_path)
    image_array = np.array(image)
    print(image_array.size)
    N=math.ceil(image_array.size/num)

    for i in range(1,num+1):
        lists2[f'list{i}']=diedai_M_to_N(1000, N, mu, x_0_list[i-1])
    # 将这num个列表混合并存放在N长的列表中
    merged_list = [x for sublist in zip(*lists2.values()) for x in sublist]

    # 混沌序列
    chaotic_sequence = merged_list
    print(len(merged_list))
    # print(merged_list)
    # N=math.ceil(image_array.size/num)(向上取整) 确保混沌序列的长度足够覆盖图像的所有像素
    if len(chaotic_sequence) < image_array.size:
        raise ValueError("混沌序列的长度不足以覆盖图像的所有像素")

    # 将图像数组转换为一维数组
    image_flat = image_array.flatten()
    # 对其进行置乱
    np.random.shuffle(image_flat)

    # 对每个像素进行加密(使用异或操作将每个像素与混沌序列进行加密)
    encrypted_image_flat = image_flat ^ (np.array(chaotic_sequence[:image_flat.size]) * 255).astype(int)

    # 将加密后的一维数组重新变形为图像数组形状
    encrypted_image_array = encrypted_image_flat.reshape(image_array.shape)

    # 显示加密后的图像
    encrypted_image = Image.fromarray(encrypted_image_array.astype(np.uint8))
    encrypted_image.show()
    # 保存加密后的图像
    encrypted_image.save('D:/encrypted_pic.png')

    # 如果没有对图像的一维数组置乱(即np.random.shuffle(image_flat))，则可以提供解密算法如下，但是需要有先前生成的置乱序列才能够解密
    # 解密：对加密后的图像进行解密
    # decrypted_image_flat = encrypted_image_flat ^ (np.array(chaotic_sequence[:image_flat.size]) * 255).astype(int)
    # decrypted_image_array = decrypted_image_flat.reshape(image_array.shape)
    #
    # # 显示解密后的图像
    # decrypted_image = Image.fromarray(decrypted_image_array.astype(np.uint8))
    # decrypted_image.show()
    # 保存解密后的图像
    # decrypted_image.save('D:/decrypted_pic.png')

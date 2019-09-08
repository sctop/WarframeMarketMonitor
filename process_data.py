# 冒泡排序
def popping(object, key, high_top):
    """
    冒泡排序

    :param object: 要排序的列表，必须为list
    :param key: 排序按照哪个键的值进行排序
    :param high_top: 是冒泡排序(True)还是反冒泡排序(False)呢
    :return:
    """
    temp = object
    done = 0
    while not done:
        done = 1
        pos = 0
        for i in range(len(temp) - 1):
            if not high_top:
                if temp[pos][str(key)] > temp[pos + 1][str(key)]:
                    loop_temp = temp[pos]
                    temp[pos] = temp[pos + 1]
                    temp[pos + 1] = loop_temp
                    done = 0
            elif high_top:
                if temp[pos][str(key)] < temp[pos + 1][str(key)]:
                    loop_temp = temp[pos]
                    temp[pos] = temp[pos + 1]
                    temp[pos + 1] = loop_temp
                    done = 0
            pos += 1
    return temp


# ----------------------------------------------------
# Sorting.reputation函数的专用函数
class reputationFunction:
    def same_price(self, object):
        same_price = []
        for pos in range(len(object)):
            if object[pos] not in same_price:
                current_price = object[pos]
                if not (pos + 1) == len(object):
                    if object[pos + 1] == current_price:
                        same_price.append(current_price)
        return same_price

    def check_same(self, object, key):
        poses = []
        for i in range(len(object)):
            if object[i] == key:
                poses.append(i)
        return poses


# ----------------------------------------------------
# 排序
class Sorting:
    # 对价格排序
    def pricing(self, is_mod, object):
        if is_mod == "mod":
            """
            将相同等级的Mod按价格从低到高进行排序
            """
            # 设置Mod的开始循环的最高等级
            current_rank = 15
            final = []
            for i in range(current_rank + 1):
                same_rank = []
                for info in object:
                    if info["modrank"] == current_rank:
                        same_rank.append(info)
                temp = []
                for info in same_rank:
                    temp.append({"name": info["name"], "price": info["price"]})
                temp = popping(temp, "price", False)

                temp2 = []
                # 重建用户数据
                for info in temp:
                    for current in same_rank:
                        if current["name"] == info["name"]:
                            temp2.append(current)
                            break

                for info in temp2:
                    final.append(info)
                current_rank -= 1
        else:
            temp = []
            for info in object:
                temp.append({"name": info["name"], "price": info["price"]})
            temp = popping(temp, "price", False)

            temp2 = []
            for info in temp:
                for i in object:
                    if i["name"] == info["name"] and (i not in temp2):
                        temp2.append(i)
                        break
            final = temp2

        return final

    # 对信誉排序
    def reputation(self, is_mod, object):
        if is_mod == "mod":
            current_rank = 15
            final = []
            for i in range(current_rank + 1):
                same_rank = []
                for info in object:
                    if info["modrank"] == current_rank:
                        same_rank.append(info)

                mod_prices = []
                for info in same_rank:
                    mod_prices.append(info["price"])

                sameprice = reputationFunction().same_price(mod_prices)

                # 有重复价格才计算
                if len(sameprice) > 0:
                    for i in sameprice:
                        # 找到相同价格的pos
                        temp = reputationFunction().check_same(mod_prices, i)
                        # same_rank中重新填充数据的起始位置
                        start_refill = temp[0]

                        temp2 = []
                        # 遍历相同价格的卖家信息
                        for pos in temp:
                            temp2.append(same_rank[pos])

                        # 根据信誉进行冒泡排序
                        temp3 = popping(temp2, "reputation", True)

                        temp2 = []
                        # 重建卖家信息
                        for info in temp3:
                            for current in same_rank:
                                if current["name"] == info["name"]:
                                    temp2.append(current)
                                    break

                        # 覆盖same_rank信息
                        for pos in range(len(temp2)):
                            current_pos = pos + start_refill  # 将当前位置加上偏值start_refill
                            same_rank[current_pos] = temp2[pos]

                for i in same_rank:
                    final.append(i)
                current_rank -= 1
        else:
            original = object

            prices = []
            for info in object:
                prices.append(info["price"])

            sameprice = reputationFunction().same_price(prices)

            if len(sameprice) > 0:
                for i in sameprice:
                    temp = reputationFunction().check_same(prices, i)
                    start_refill = temp[0]

                    temp2 = []
                    # 遍历相同价格的卖家信息
                    for pos in temp:
                        temp2.append(object[pos])

                    # 根据信誉进行冒泡排序
                    temp3 = popping(temp2, "reputation", True)

                    temp2 = []
                    # 重建卖家信息
                    for info in temp3:
                        for current in object:
                            if current["name"] == info["name"]:
                                temp2.append(current)
                                break

                    # 覆盖original信息
                    for pos in range(len(temp2)):
                        current_pos = pos + start_refill  # 将当前位置加上偏值start_refill
                        original[current_pos] = temp2[pos]
            final = original

        return final

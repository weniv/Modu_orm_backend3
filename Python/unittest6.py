import pdb


def add_to_ten(num):
    result = 0
    for i in range(10):
        result += i
        pdb.set_trace()  # 디버거를 실행합니다. break 포인트입니다.
    return result


add_to_ten(5)

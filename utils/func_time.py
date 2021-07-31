import time


def clock(msg: str = ""):
    """
    函数执行耗时计算机,支持传入msg参数信息用作区分记录
    """

    def decorator(func):
        def func_count_time(*args, **kwargs):
            start_time = time.time()
            result = func(*args, **kwargs)
            end_time = time.time()
            duration = end_time - start_time
            print(f'func<{func.__name__}>  timeCost: {duration} s  msg:{msg} ')
            return result

        return func_count_time

    return decorator

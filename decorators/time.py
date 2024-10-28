from time import time

from loggers import logger


def execution_time(func):
    """
    Calculates the execution time of a function/method.
    :param func:
    :return:
    """

    def wrapper(*args, **kwargs):
        start = time()
        result = func(*args, **kwargs)

        end = time()

        execution = end - start

        logger.info(f"Process executed in: {execution:.2f} secs.")

        return result

    return wrapper

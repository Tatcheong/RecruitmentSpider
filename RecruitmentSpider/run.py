from multiprocessing import Process

from scrapy.cmdline import execute


def main(spider):
    cmd = f'scrapy crawl {spider}'
    execute(cmd.split())


if __name__ == '__main__':
    p1 = Process(target=main, args=('job51',))
    p2 = Process(target=main, args=('lagou',))
    p1.start()
    p2.start()

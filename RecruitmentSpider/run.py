from scrapy.cmdline import execute


def main():
    # cmd = 'scrapy crawl job51 -o 51job1-12.json'
    cmd = 'scrapy crawl lagou -o lagou1-12.json'
    execute(cmd.split())


if __name__ == '__main__':
    main()

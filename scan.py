#!/usr/bin/python
# -*- coding: utf-8 -*-
# Author: vstral
# Date: 2025-09-10 21:40:00

import urllib.request
import urllib.error
import time


def generateTarget(url1, url2):
    """
    预先生成所有等待扫描的目标到wait.txt
    """
    opener = urllib.request.build_opener()
    opener.addheaders = [
        ("User-agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")
    ]

    # 扫描范围为1-255，一次性写入所有目标
    with open("wait.txt", "w", encoding="utf-8") as file:
        for n in range(1, 255):
            nb = str(n)
            # target = '192-168-1-'+nb+'.awd.bugku.cn/'
            target = url1 + nb + url2
            file.write(target + "\n")


def scanTarget(domain_list):
    """
    逐个扫描目标, 发现主机则输出到live.txt
    """
    error_list = set()
    right_list = set()
    url_list = open(domain_list, "r")
    for line in url_list:
        if len(line.strip()):
            line_no_blank = line.strip()
            url = "http://" + line_no_blank
            error_code = ""
            error_reason = ""
            try:
                start = time.perf_counter()
                file = urllib.request.urlopen(url, timeout=2)
                elapsed = time.perf_counter() - start  # 获取访问时长
                print("%s---->%s, 耗时%s" % (line_no_blank, file.getcode(), elapsed))
                right_list.add(line_no_blank)
            except (
                urllib.error.URLError
            ) as e:  # 异常域名会进入except，可以得到出错原因和出错http状态码
                print("%s异常" % line_no_blank)
                if hasattr(e, "code"):
                    print("错误状态码：%s" % e.code)
                    error_code = str(e.code)
                if hasattr(e, "reason"):
                    print("出错原因:%s" % e.reason)
                    error_reason = str(e.reason)
                error_status = error_code + "\t" + error_reason
                error_list.add(
                    line_no_blank + "\t" + error_status + "\n"
                )  # 将所有异常域名存入set集合，会自动去重
    url_list.close()
    print("所有正常域名：")
    outputFile = open("live.txt", "w+")
    for lineone in right_list:
        print(lineone)
        outputFile.write(lineone + "\n")
    outputFile.close()


if __name__ == "__main__":
    url1 = ""
    url1 += input("请输入目标前缀: ")

    url2 = ""
    url2 += input("请输入目标后缀: ")

    generateTarget(url1, url2)
    scanTarget("wait.txt")

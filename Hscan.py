from gevent import monkey
monkey.patch_all()
from sys import version_info
from libs.core.common import banner, set_paths
from libs.parse.cmdline import cmdlineparse
from libs.ports.alive import alive_detect
from libs.ports.portscan import portscan
import gevent
from libs.controller.poc_engine import poc_scan
from libs.core.data import logger, paths, cmdLineOptions, conf
import os
from libs.core.exception import PyVersionException, TargetException1, TargetException2, PocTaskException
from libs.controller.loader import loader, load_poctasks


def main():
    try:
        # 首先判断一下python版本的问题
        if version_info < (3, 6):
            raise PyVersionException

        # 设置一下路径问题
        set_paths(os.path.dirname(os.path.realpath(__file__)))

        # 先输出banner
        print(banner())

        # 解析一下命令行
        cmdLineOptions.update(cmdlineparse().__dict__)
        # print(args)

        loader()

        # 存活探测
        alive_detect()

        # 端口扫描
        portscan()

        # 加载扫描任务
        load_poctasks()

        # poc漏洞扫描
        gevent.joinall([gevent.spawn(poc_scan) for _ in range(0, 100)])

    except PyVersionException as e:
        logger.error("请使用python>=3.6版本")
    except TargetException1:
        logger.error("请使用-u或者-f指定目标")
    except TargetException2:
        logger.error("没有目标存活，如果目前存活，请使用-Pn跳过存活")
    except PocTaskException:
        logger.error("目标未开放端口")


if __name__ == "__main__":
    main()


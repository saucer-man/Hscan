from gevent import monkey

monkey.patch_all()
from sys import version_info
from libs.core.common import banner, set_paths
from libs.parse.cmdline import cmdlineparse
from libs.ports.alive import alive_detect
from libs.ports.portscan import portscan
import time
from libs.controller.poc_engine import run
from libs.core.data import logger, cmdLineOptions, conf
import os
from libs.core.exception import PyVersionException, TargetException1, TargetException2, PocTaskException
from libs.controller.loader import loader, load_poctasks
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def main():
    try:
        conf.start_time = time.time()
        # First determine the version of python
        if version_info < (3, 6):
            raise PyVersionException

        # Set up the path
        set_paths(os.path.dirname(os.path.realpath(__file__)))

        # output banner
        print(banner())

        # Parse command line parameters into cmdLineOptions
        cmdLineOptions.update(cmdlineparse().__dict__)
        # print(args)

        # Load poc, target, concurrent number from parameters, etc.
        loader()

        # Survival host detection
        alive_detect()

        # open port scan
        portscan()

        # load pocs and targets --> tasks
        load_poctasks()

        # Use coroutines for concurrent scans
        run()

        logger.info(f"done with {time.time() - conf.start_time}s")

    except PyVersionException as e:
        logger.error("Please use python> = 3.6 version")
    except TargetException1:
        logger.error("Please use -u or -f to specify the target")
    except TargetException2:
        logger.error("No target survives, if you are currently alive, please use -Pn to skip survival")
    except PocTaskException:
        logger.error("Target has no open ports")


if __name__ == "__main__":
    main()

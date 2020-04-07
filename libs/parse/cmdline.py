import argparse


def cmdlineparse():
    parser = argparse.ArgumentParser(usage='这里写使用方法')

    target = parser.add_argument_group("Target",
                                       "At least one of these options has to be provided to define the target(s)")
    target.add_argument("-u", "--url", dest="url",
                        help="Target URL (e.g. \"http://www.site.com/vuln.php?id=1\")")
    target.add_argument("-f", dest="target_file",
                        help="Scan multiple targets given in a file ")
    engine = parser.add_argument_group("engine", "options for engine")
    engine.add_argument("-t", "--thread", dest="thread",
                        help="thread num to poc scan ")
    engine.add_argument("-timeout", dest="timeout", type=int, default=3,
                        help="timeout")
    engine.add_argument('-Pn', dest="alive_detect", action='store_false',
                        help='alive detect or not')
    engine.add_argument('-Ps', dest="port_scan", action='store_false',
                        help='port scan detect, otherwise all ports will be poc scan')
    engine.add_argument('-pt', '--port_scan_threads', dest="port_scan_threads", type=int, default=200,
                        help='port scan threads, default 200')
    args = parser.parse_args()
    return args
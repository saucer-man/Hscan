import argparse


def cmdlineparse():
    parser = argparse.ArgumentParser(usage='python Hscan.py -u 10.40.80.116')

    target = parser.add_argument_group("Target",
                                       "At least one of these options has to be provided to define the target(s)")
    target.add_argument("-u", "--url", dest="url",
                        help="Target URL (e.g. \"http://www.site.com/vuln.php?id=1\")")
    target.add_argument("-f", dest="target_file",
                        help="Scan multiple targets given in a file ")
    target.add_argument("-p", "--port", dest="port",
                        help="Specify the port to scan")
    engine = parser.add_argument_group("engine", "options for engine")
    engine.add_argument("-t", "--thread", dest="thread", type=int,
                        help="thread num to poc scan")
    engine.add_argument("-timeout", dest="timeout", type=int, default=3,
                        help="timeout")
    engine.add_argument('-Pn', dest="alive_detect", action='store_false',
                        help='alive detect or not')
    engine.add_argument('-Ps', dest="port_scan", action='store_false',
                        help='port scan detect, otherwise all ports will be poc scan')
    engine.add_argument('-pt', '--port_scan_threads', dest="port_scan_threads", type=int,
                        help='port scan threads, default 200')
    general = parser.add_argument_group("general", "general options")
    general.add_argument("-vv", dest="verbose", action='store_true',
                        help = 'more detailed output')
    args = parser.parse_args()
    return args
#!/usr/bin/env python

import optparse
import os

from src import api_server

usage = "python3 %prog start|stop|restart -m/--mode <background execution> -d/--debug <debug mode>"
parser = optparse.OptionParser(usage)
parser.add_option('-m', '--mode', dest='mode', type='string', help='Background execution', default='d')
parser.add_option('-d', '--debug', dest='debug', type='string', help='Debug mode', default='yes')
options, args = parser.parse_args()
# print('options为', options)
# print("后台运行：", options.mode)
# print("调试模式：", options.debug)
# print('args为', args)


# 执行命令
if args and args[0] and args[0] == "start":

    # os.system('pip3 install -r requirements.txt')

    if options.debug == "yes":
        api_server.run(debug=True)
    else:
        api_server.run(debug=False)

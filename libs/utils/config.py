#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Copyright (c) saucerman (https://saucer-man.com)
See the file 'LICENSE' for copying permission
"""

from configparser import ConfigParser

from libs.core.data import paths, logger


class ConfigFileParser:
    @staticmethod
    def _get_option(section, option):
        try:
            cf = ConfigParser()
            cf.read(paths.CONFIG_PATH, encoding='utf-8')
            return cf.get(section=section, option=option)
        except:
            logger.error('Missing essential options, please check your config-file.')
            return ''

    def target_url(self):
        return self._get_option('target', 'url')

    def target_file(self):
        return self._get_option('target', 'file')

    def port(self):
        return self._get_option('target', 'port')

    def poc_list(self):
        return self._get_option('pocs', 'pocs')

    def port_scan_thread(self):
        return self._get_option('engine', 'port_scan_thread')

    def thread(self):
        return self._get_option('engine', 'thread')

    def port_scan(self):
        return self._get_option('engine', 'port_scan')

    def alive_detect(self):
        return self._get_option('engine', 'alive_detect')

    def verbose(self):
        return self._get_option('general', 'verbose')

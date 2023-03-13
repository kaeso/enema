"""
    Enema module (core): Plugin handler
    Copyright (C) 2012 Valeriy Bogachuk
    
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.
"""

import os
from PyQt6 import QtCore


class PluginHandler(QtCore.QObject):

    logSignal = QtCore.pyqtSignal(str)
    
    def __init__(self):
        QtCore.QObject.__init__(self)
        
    #Finding plugins and returning import strings
    def findPlugins(self, plugin_dir):	
        import_strings = []
        for category in os.listdir(plugin_dir):
            if not (category.startswith("__") or category.endswith(".py")):
                for file in os.listdir(plugin_dir + "/" + category):
                    if (file[:2] != "__" and file[:3] != "Ui_" and file[-3:] == ".py"):
                        import_strings.append(plugin_dir + "." + category + "." + file[:-3])

        return import_strings

    #Fetching information from plugins
    def getPluginsInfo(self, import_strings):
        plugins_info = []
        info = {}	
        import_info = {}
    
        for module in import_strings:
            try:
                import_buff = __import__(module, globals(), locals(), ['PLUGIN_NAME', 'PLUGIN_GROUP', 'PLUGIN_CLASS_NAME', 'PLUGIN_DESCRIPTION'], 0)
                info['PLUGIN_NAME'] = import_buff.PLUGIN_NAME
                info['PLUGIN_GROUP'] = import_buff.PLUGIN_GROUP
                info['PLUGIN_CLASS_NAME'] = import_buff.PLUGIN_CLASS_NAME
                info['PLUGIN_DESCRIPTION'] = import_buff.PLUGIN_DESCRIPTION
                plugins_info.append(info)
                info = {}
                import_info[module] = import_buff.PLUGIN_CLASS_NAME
            except Exception as ex:
                module = module.replace(".", "/") + ".py"
                mod_full_path = os.path.abspath(module)
                self.logSignal.emit(" - !!! - \n\n * Can't load plugin '" + mod_full_path + "'\n --> Reason: " + str(ex) + "\n\n - !!! -\n\n")
                
        self.logSignal.emit(" - Total plugins loaded: " + str(len(import_info)))
        return {'plugins_info' : plugins_info,  'import_info' : import_info}
    

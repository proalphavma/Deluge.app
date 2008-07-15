#
# configmanager.py
#
# Copyright (C) 2007 Andrew Resch ('andar') <andrewresch@gmail.com>
# 
# Deluge is free software.
# 
# You may redistribute it and/or modify it under the terms of the
# GNU General Public License, as published by the Free Software
# Foundation; either version 2 of the License, or (at your option)
# any later version.
# 
# deluge is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with deluge.    If not, write to:
# 	The Free Software Foundation, Inc.,
# 	51 Franklin Street, Fifth Floor
# 	Boston, MA    02110-1301, USA.
#
#    In addition, as a special exception, the copyright holders give
#    permission to link the code of portions of this program with the OpenSSL
#    library.
#    You must obey the GNU General Public License in all respects for all of
#    the code used other than OpenSSL. If you modify file(s) with this
#    exception, you may extend this exception to your version of the file(s),
#    but you are not obligated to do so. If you do not wish to do so, delete
#    this exception statement from your version. If you delete this exception
#    statement from all source files in the program, then also delete it here.

import gobject
import os
import os.path

import deluge.common
from deluge.log import LOG as log
from deluge.config import Config

class _ConfigManager:
    def __init__(self):
        log.debug("ConfigManager started..")
        self.config_files = {}
        self.config_directory = deluge.common.get_default_config_dir()
        # Set a 5 minute timer to call save()
        gobject.timeout_add(300000, self.save)

    def __del__(self):
        log.debug("ConfigManager stopping..")
        del self.config_files

    def set_config_dir(self, directory):
        """Sets the config directory"""
        if directory == None:
            return
        log.info("Setting config directory to: %s", directory)
        if not os.path.exists(directory):
            # Try to create the config folder if it doesn't exist
            try:
                os.makedirs(directory)
            except Exception, e:
                log.warning("Unable to make config directory: %s", e)
                
        self.config_directory = directory
    
    def get_config_dir(self):
        log.debug("get_config_dir: %s", self.config_directory)
        return self.config_directory
            
    def close(self, config):
        """Closes a config file."""
        try:
            del self.config_files[config]
        except KeyError:
            pass
            
    def save(self):
        """Saves all the configs to disk."""
        for key in self.config_files.keys():
            self.config_files[key].save()
        # We need to return True to keep the timer active
        return True
        
    def get_config(self, config_file, defaults=None):
        """Get a reference to the Config object for this filename"""
        log.debug("Getting config '%s'", config_file)
        # Create the config object if not already created
        if config_file not in self.config_files.keys():
            self.config_files[config_file] = Config(config_file, defaults, self.config_directory)
        
        return self.config_files[config_file]
        
# Singleton functions
_configmanager = _ConfigManager()

def ConfigManager(config, defaults=None):
    return _configmanager.get_config(config, defaults)

def set_config_dir(directory):
    """Sets the config directory, else just uses default"""
    return _configmanager.set_config_dir(directory)

def get_config_dir(filename=None):
    if filename != None:
        return os.path.join(_configmanager.get_config_dir(), filename)
    else:
        return _configmanager.get_config_dir()
        
def close(config):
    return _configmanager.close(config)
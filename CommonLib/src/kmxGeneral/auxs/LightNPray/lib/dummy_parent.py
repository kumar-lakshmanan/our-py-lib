import os
import sys

from LightNPray.lib import configs
from LightNPray.lib import shared

class DummyParent():

    def __init__(self, APP):
        self.App = APP
        self.Config = configs.AppConfigs('data/setting.ini')
        self.Common = shared.AppShared()
        #self.Config.UpdateAllConfigValues()
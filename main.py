#runs on launch to load / launch the launcher
from tendo import singleton
import sys
#one running instance check

try:
    me = singleton.SingleInstance()
except singleton.SingleInstanceException:
    sys.exit(0)


from launcher import Launcher
import pygame

ENGINE_VERSION = "0.1.1"

pygame.init()

Launcher(ENGINE_VERSION)

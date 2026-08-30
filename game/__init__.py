from core import Unused

# Avoid importing the full game runtime at package import time.
# Some modules import `game.*` packages while the package graph is still being
# initialized, which creates circular import loops. Import the runtime entry
# points lazily from the actual module that needs them instead.
Unused(__name__)


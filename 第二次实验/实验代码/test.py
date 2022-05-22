import time
from progress.bar import Bar

bar = Bar("encrypt",max = 100,suffix = "%(percent)d%%")
for i in bar.iter(range(100)):
    time.sleep(0.01)
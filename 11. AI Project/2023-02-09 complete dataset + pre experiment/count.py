import os
import glob

path = './'
image = glob.glob(os.path.join(path, '*', '*', '*.png'))
xml_paths = glob.glob(os.path.join(path, "*", "*.xml"))
print(xml_paths)
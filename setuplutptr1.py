from distutils.core import setup
from Cython.Build import cythonize

setup(name="LUTptr1",
      ext_modules = cythonize("/home/pi/ip/LUTptr1.pyx")
)
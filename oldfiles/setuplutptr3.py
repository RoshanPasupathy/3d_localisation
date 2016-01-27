from distutils.core import setup
from Cython.Build import cythonize

setup(name="LUTptr3",
      ext_modules = cythonize("/home/pi/ip/LUTptr3.pyx")
)
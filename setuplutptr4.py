from distutils.core import setup
from Cython.Build import cythonize

setup(name="LUTptr4",
      ext_modules = cythonize("/home/pi/ip/LUTptr4.pyx")
)
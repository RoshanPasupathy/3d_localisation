from distutils.core import setup
from Cython.Build import cythonize

setup(name="LUTptr2",
      ext_modules = cythonize("/home/pi/ip/LUTptr2.pyx")
)
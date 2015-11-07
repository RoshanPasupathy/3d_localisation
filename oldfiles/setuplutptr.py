from distutils.core import setup
from Cython.Build import cythonize

setup(name="LUTptr",
      ext_modules = cythonize("/home/pi/ip/LUTptr.pyx")
)
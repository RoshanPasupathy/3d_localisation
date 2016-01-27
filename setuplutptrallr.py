from distutils.core import setup
from Cython.Build import cythonize

setup(name="LUTptrallr",
      ext_modules = cythonize("/home/pi/ip/LUTptr2=allr.pyx")
)
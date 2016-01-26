from distutils.core import setup
from Cython.Build import cythonize

setup(name="sizefile",
      ext_modules = cythonize("/home/pi/ip/testfiles/sizefile.pyx")
)
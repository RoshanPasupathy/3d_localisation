from distutils.core import setup
from Cython.Build import cythonize

setup(name="pointaddress",
      ext_modules = cythonize("/home/pi/ip/testfiles/pointaddress.pyx")
)
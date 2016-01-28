from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext

ext_modules=[Extension("LUTptrallr",["/home/pi/ip/LUTptrallr.pyx"],library_dirs=['.'])]

setup(
    name="LUTptrallsp",
    cmdclass={"build_ext":build_ext},
    ext_modules= ext_modules
)
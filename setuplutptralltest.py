from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext

ext_modules=[Extension("LUTptralltest",["/home/pi/ip/LUTptralltest.pyx"],library_dirs=['.'])]

setup(
    name="LUTptralltest",
    cmdclass={"build_ext":build_ext},
    ext_modules= ext_modules
)
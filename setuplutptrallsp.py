from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext

ext_modules=[Extension("Helloitsme",["/home/pi/ip/LUTptralls.pyx"],library_dirs=['.'],extra_compile_args=["-Ofast"])]

setup(
    name="LUTptrallsp",
    cmdclass={"build_ext":build_ext},
    ext_modules= ext_modules
)
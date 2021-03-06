from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext

ext_modules=[Extension("LUTptralls",["/home/pi/ip/LUTptralls.pyx"],library_dirs=['.'],extra_compile_args=["-Ofast"])]

setup(
    name="LUTptralls",
    cmdclass={"build_ext":build_ext},
    ext_modules= ext_modules
)
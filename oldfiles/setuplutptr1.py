from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext

ext_modules=[Extension("LUTptr1",["/home/pi/ip/LUTptr1.pyx"],library_dirs=['.'],extra_compile_args=["-Ofast"])]

setup(
    name="LUTptr1",
    cmdclass={"build_ext":build_ext},
    ext_modules= ext_modules
)
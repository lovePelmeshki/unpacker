from setuptools import setup, find_packages

setup(
    name='unpacker',
    version='1.0',
    py_modules=['unpacker'],  # unpacker.py — это основной модуль
    install_requires=[
        # Зависимости можно оставить пустыми, так как они будут в requirements.txt
    ],
    entry_points={
        'console_scripts': [
            'unpacker=unpacker:main',  # main — это функция из unpacker.py, которая будет точкой входа
        ],
    },
)

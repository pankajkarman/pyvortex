from setuptools import setup

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
     name='pyvortex',
     version='0.2',
     description='Polar vortex edge detection using Nash criteria',
     long_description=long_description,
     long_description_content_type='text/markdown',
     url='https://github.com/pankajkarman/pyvortex',
     author='Pankaj Kumar',
     author_email='pankaj.kmr1990@gmail.com',
     license='MIT',
     py_modules=['pyvortex'],
     install_requires=[
     "numpy", 'xarray'
     ],
     python_requires=">=3.6",
     setup_requires=['setuptools'],
)

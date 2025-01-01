from setuptools import setup, find_packages
import os

this_directory = os.path.abspath(os.path.dirname(__file__))

long_description = ""
readme_path = os.path.join(this_directory, "readme.md")
if os.path.exists(readme_path):
    with open(readme_path, encoding="utf-8") as f:
        long_description = f.read()

setup(
    name='energy_tariff_scheduler',
    version='0.0.1',
    author='Craig White',
    author_email='dev.craigw@gmail.com',
    description='Schedule actions based on energy tariffs',
    packages=find_packages(exclude=["__tests__"], include=["energy_tariff_scheduler"]),
    install_requires=[
        "pydantic==2.10.4",
        "requests==2.32.3",
        "python-dateutil==2.9.0.post0",
        "apscheduler==3.11.0"
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.10',
    long_description=long_description,
    long_description_content_type="text/markdown",
)
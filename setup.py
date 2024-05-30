from setuptools import setup, find_packages

setup(
    name='mev_agent',
    version='0.1.0',
    author='Luca Nicoli',
    author_email='luca.nicoli.engineer@gmail.com',
    description='MEV agent excercise',
    url='https://github.com/nicoli-luca/mev_agent.git',
    packages=find_packages(),
    install_requires=[
        'numpy',
        'scipy',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)

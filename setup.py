from setuptools import setup, find_packages

setup(
    name='ai-scheduler',
    version='0.0.0',

    description='Task scheduler based on Machine Learning',

    # url='',
    author='Darko Lukic',
    author_email='lukicdarkoo@gmail.com',
    license='MIT',
    keywords='machine learning scheduler DAG',

    # packages=find_packages(exclude=['contrib', 'docs', 'tests']),

    install_requires=['deap'],

    # $ pip install -e .[dev,test]
    extras_require={
        'dev': ['check-manifest'],
        'test': ['coverage'],
    },

    entry_points={
        'console_scripts': [
            'sample=sample:main',
        ],
    },
)


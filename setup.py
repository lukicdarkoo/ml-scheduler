from setuptools import setup, find_packages

setup(
    name='ml-scheduler',
    version='0.0.0',

    description='Task schedulers based on Machine Learning',

    url='https://bitbucket.org/LukicDarkoo/ml-scheduler',
    author='Darko Lukic',
    author_email='lukicdarkoo@gmail.com',
    license='MIT',
    keywords='machine learning schedulers DAG',

    packages=find_packages(exclude=['docs', 'test']),

    install_requires=[
        'deap', 		# Genetic algorithm
        'networkx',		# Graph library
        'matplotlib', 	# Exporting graph (DAG) as image
        'cairocffi'     # Resolves a warning `The Gtk3Agg backend is known to not work on Python 3.x with pycairo`
    ],

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


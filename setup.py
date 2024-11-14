from setuptools import setup, find_packages

setup(
    name='archdatapy',
    version='0.1.0',
    author='W. Christopher Carleton',
    author_email='ccarleton@protonmail.com',
    description='A lightweight package to access R::archdata archaeological datasets in Python',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/yourusername/archdatapy',  # Replace with your actual GitHub repo URL
    packages=find_packages(),
    install_requires=[
        'requests',
        'pyreadr',
        'pandas',
        'pprint',
        'pandas',
        # Add other dependencies if needed
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)

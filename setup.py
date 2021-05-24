from setuptools import setup, find_packages

with open('requirements.txt') as f:
    requirements = f.readlines()

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='gitcomp',
    version='1.0.0',
    author='Anirudh Vaish',
    author_email='anirudhvaish147@gmail.com',
    url='https://github.com/avaish1409/gitcomp',
    description='A python based command line tool to compare Github Users or Repositories.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    license='MIT',
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    entry_points={
        'console_scripts': [
            'gitcomp = gitcomp.__main__:main'
        ]
    },
    project_urls={
        "Bug Tracker": "https://github.com/avaish1409/gitcomp/issues",
        'Documentation': 'https://avaish1409.github.io/gitcomp/',
        'Source': 'https://github.com/avaish1409/gitcomp'
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    keywords='command-line-tools cli gitcomp python package compare git github',
    install_requires=requirements,
    python_requires=">=3",
    zip_safe=False
)

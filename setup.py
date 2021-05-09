from setuptools import setup, find_packages

with open('requirements.txt') as f:
	requirements = f.readlines()

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
		name ='gitcompare',
		version ='1.0.0',
		author ='Anirudh Vaish',
		author_email ='anirudhvaish147@gmail.com',
		url ='https://github.com/avaish1409/gitcompare',
		description ='A python based command line tool to compare Github Users or Repositories.',
		long_description = long_description,
		long_description_content_type ="text/markdown",
		license ='MIT',
        package_dir={"": "src"},
        packages=find_packages(where="src"),
		entry_points ={
			'console_scripts': [
				'gitcompare = gitcompare.__init__:main'
			]
		},
        project_urls={
            "Bug Tracker": "https://github.com/avaish1409/gitcompare/issues",
            'Documentation': 'https://avaish1409.github.io/gitcompare/',
            'Source': 'https://github.com/avaish1409/gitcompare'
        },
		classifiers =(
			"Programming Language :: Python :: 3",
			"License :: OSI Approved :: MIT License",
			"Operating System :: OS Independent",
		),
		keywords ='command-line-tools cli gitcompare python package compare git github',
		install_requires = requirements,
        python_requires=">=3",
		zip_safe = False
)
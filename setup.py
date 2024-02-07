from setuptools import setup 
  
setup( 
    name='robotframework-schemathesis', 
    version='0.1', 
    description='Python wrapper of Schemathesis',
    package_dir={'': 'src'}, 
    packages=['SchemathesisLibrary'], 
    install_requires=[ 
        'robotframework', 
        'schemathesis', 
    ], 
) 
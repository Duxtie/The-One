from setuptools import find_packages, setup

setup(
    name="theorem-challenge-transmogrify-dict",
    version="1.0.0",
    author="Theorem.co",
    author_email="jayson.minard@theorem.co",
    packages=find_packages(),
    test_suite="test",
    install_requires=["pytest-runner"],
    tests_require=[
        "pytest",
        "pytest-timeout",
        "deem.testfixture==0.0.6"
    ],
)
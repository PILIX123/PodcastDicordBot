from setuptools import setup, find_packages

VERSION = "0.1.0"
DESCRIPTION = "A discord bot that can play podcasts"
LONG_DESCRIPTION = "This package will contain everything but main from my discord bot, its a way for me to understand packages"

setup(
    name="PodcastBotDiscord",
    version=VERSION,
    author="Pierre-Luc R.",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=["discord.py",
                      "hvac"
                      "requests",
                      "pyPodcastParser",
                      "sqlalchemy[asyncio]",
                      "aiosqlite",
                      "pytest_mock",
                      "pytest[asyncio]",
                      "pytest-asyncio",
                      "python-dotenv",],
    keywords=["python", "first package"],
)

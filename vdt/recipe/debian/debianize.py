import ConfigParser
import logging
import os

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class Debianize(object):
    @staticmethod
    def get_config():
        path = os.getcwd()
        config = ConfigParser.ConfigParser()
        config.readfp(open('%s/.vdt.recipe.debian.cfg' % path))
        return config

    def __call__(self, *args, **kwargs):
        logger.info("Get configuration")
        config = self.get_config()

        versions_executable = config.get(
            'vdt.recipe.debian', 'versions-executable')
        versions_file = config.get('vdt.recipe.debian', 'versions-file')
        sources_directory = config.get(
            'vdt.recipe.debian', 'sources-directory')
        sources_to_build = config.get('vdt.recipe.debian', 'sources-to-build')

        for src in os.listdir(sources_directory):
            if src in sources_to_build:
                logger.info("Building package for %s" % src)
                command = [
                    "cd %s" % "%s/%s" % (sources_directory, src),
                    "&&",
                    versions_executable,
                    "--plugin=buildout",
                    "--versions-file %s" % versions_file]
                logger.info("Executing commands %s" % " ".join(command))

debianize = Debianize()

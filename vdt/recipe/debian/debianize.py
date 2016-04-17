import ConfigParser
from glob import glob
import logging
import os
import platform
import subprocess

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

SUPPORTED_PLATFORMS = ["ubuntu", "debian"]


class Debianize(object):

    @staticmethod
    def check_platform():
        current_platform = platform.dist()[0].lower()
        return current_platform in SUPPORTED_PLATFORMS

    @staticmethod
    def create_target_directory(directory):
        if not os.path.isdir(directory):
            os.mkdir(directory)

    @staticmethod
    def get_config():
        path = os.getcwd()
        config = ConfigParser.ConfigParser()
        config.readfp(open('%s/.vdt.recipe.debian.cfg' % path))
        return config

    @staticmethod
    def get_build_sources(sources_directory, sources_to_build):
        for src in os.listdir(sources_directory):
            if src in sources_to_build or '*' in sources_to_build:
                yield src

    def __call__(self, *args, **kwargs):
        supported_plaform = self.check_platform()

        if not supported_plaform:
            logger.info(
                "Cannot build .deb packages, your platform is not supported. "
                "Supported platforms: %s" % ", ".join(SUPPORTED_PLATFORMS))
            return False

        config = self.get_config()
        version_executable = config.get(
            'vdt.recipe.debian', 'version-executable')
        version_plugin = config.get('vdt.recipe.debian', 'version-plugin')
        version_extra_args = config.get(
            'vdt.recipe.debian', 'version-extra-args')
        versions_file = config.get('vdt.recipe.debian', 'versions-file')
        sources_directory = config.get(
            'vdt.recipe.debian', 'sources-directory')
        sources_to_build = config.get(
            'vdt.recipe.debian', 'sources-to-build').split('\n')
        target_directory = config.get(
            'vdt.recipe.debian', 'target-directory')

        # create target directory to place our .deb files
        self.create_target_directory(target_directory)

        for src in self.get_build_sources(sources_directory, sources_to_build):
            cwd = "%s/%s" % (sources_directory, src)

            logger.info("Building package for %s" % src)
            build_cmd = [
                version_executable,
                "--plugin=%s" % version_plugin,
                "--versions-file=%s" % versions_file]
            if version_extra_args:
                build_cmd.append(version_extra_args)
            logger.info(
                "Executing command %s from %s" % (
                    " ".join(build_cmd), cwd))
            logger.info(
                subprocess.check_output(build_cmd, cwd=cwd))

            # move deb files to target directory
            deb_files = glob("%s/*.deb" % cwd)
            move_cmd = ["mv"] + deb_files + [target_directory]

            logger.info("Executing command %s" % move_cmd)
            logger.info(
                subprocess.check_output(move_cmd, cwd=cwd))

debianize = Debianize()

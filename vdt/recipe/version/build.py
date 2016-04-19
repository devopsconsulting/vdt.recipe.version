import ConfigParser

from glob import glob

import logging
import os
import platform
import subprocess
import sys

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class Build(object):

    @staticmethod
    def check_platform(target_extension):
        if target_extension == "*.deb":
            current_platform = platform.dist()[0].lower()
            return current_platform in ["ubuntu", "debian"]
        return True

    @staticmethod
    def create_target_directory(directory):
        if not os.path.isdir(directory):
            os.mkdir(directory)

    @staticmethod
    def get_config():
        path = os.getcwd()
        config = ConfigParser.ConfigParser()
        config.readfp(open('%s/.vdt.recipe.version.cfg' % path))
        return config

    @staticmethod
    def get_build_sources(sources_directory, sources_to_build):
        for src in os.listdir(sources_directory):
            if src in sources_to_build or '*' in sources_to_build:
                yield src

    def __call__(self, *args, **kwargs):
        config = self.get_config()

        versions_file = None

        version_executable = config.get(
            'vdt.recipe.version', 'version-executable')
        version_plugin = config.get('vdt.recipe.version', 'version-plugin')
        version_extra_args = config.get(
            'vdt.recipe.version', 'version-extra-args')
        if config.has_option('vdt.recipe.version', 'versions-file'):
            versions_file = config.get(
                'vdt.recipe.version', 'versions-file')
        sources_directory = config.get(
            'vdt.recipe.version', 'sources-directory')
        sources_to_build = config.get(
            'vdt.recipe.version', 'sources-to-build').split('\n')
        build_directory = config.get(
            'vdt.recipe.version', 'build-directory') or ""
        target_extension = config.get(
            'vdt.recipe.version', 'target-extension')
        target_directory = config.get(
            'vdt.recipe.version', 'target-directory')

        supported_plaform = self.check_platform(target_extension)

        if not supported_plaform:
            logger.info(
                "Cannot run version, your platform is not supported.")
            return False

        # create target directory for the build packages
        self.create_target_directory(target_directory)

        for src in self.get_build_sources(sources_directory, sources_to_build):
            cwd = "%s/%s" % (sources_directory, src)

            logger.info("Running 'version' for %s" % src)
            build_cmd = [
                version_executable,
                "--plugin=%s" % version_plugin]

            if versions_file is not None:
                build_cmd.append("--versions-file=%s" % versions_file)

            if version_extra_args:
                build_cmd.append(version_extra_args)

            if len(sys.argv) > 1:
                # add optional command line arguments to version
                build_cmd += sys.argv[1:]

            logger.info(
                "Executing command %s from %s" % (
                    " ".join(build_cmd), cwd))
            logger.info(
                subprocess.check_output(build_cmd, cwd=cwd))

            # sometimes packages are build in a separate directory (fe wheels)
            if build_directory:
                cwd = "%s/%s" % (cwd, build_directory)
            # move created files to target directory
            package_files = glob("%s/%s" % (cwd, target_extension))
            if package_files:
                move_cmd = ["mv"] + package_files + [target_directory]

                logger.info("Executing command %s" % move_cmd)
                logger.info(
                    subprocess.check_output(move_cmd, cwd=cwd))

build = Build()

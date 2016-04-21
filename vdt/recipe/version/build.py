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

    def build(self, config, section):
        build_directory = None
        version_extra_args = None

        version_executable = config.get(section, 'version-executable')
        fpm_editor_executable = config.get(section, 'fpm-editor-executable')
        version_plugin = config.get(section, 'version-plugin')
        if config.has_option(section, 'version-extra-args'):
            version_extra_args = config.get(section, 'version-extra-args')
        sources_directory = config.get(section, 'sources-directory')
        sources_to_build = config.get(section, 'sources-to-build').split('\n')

        if config.has_option(section, 'build-directory'):
            build_directory = config.get(section, 'build-directory')
        target_extension = config.get(section, 'target-extension')
        target_directory = config.get(section, 'target-directory')

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
                "--vdt-fpmeditor-path=%s" % fpm_editor_executable,
                "--plugin=%s" % version_plugin]

            if version_extra_args:
                build_cmd += version_extra_args.split("\n")[1:]

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
                cwd = os.path.join(cwd, build_directory)
            # move created files to target directory
            package_files = glob(os.path.join(cwd, target_extension))
            if package_files:
                move_cmd = ["mv"] + package_files + [target_directory]

                logger.info("Executing command %s" % move_cmd)
                logger.info(
                    subprocess.check_output(move_cmd, cwd=cwd))

    def __call__(self, *args, **kwargs):
        config = self.get_config()
        for section in config.sections():
            logger.info("Building section %s" % section)
            self.build(config, section)

build = Build()

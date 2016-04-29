import argparse
import ConfigParser

from glob import glob

import logging
import os
import platform
import subprocess
import sys

from vdt.version.main import parse_args, run

logger = logging.getLogger(__name__)


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
            logger.debug(
                "Cannot run version, your platform is not supported.")
            return False

        # create target directory for the builded packages
        self.create_target_directory(target_directory)

        # now build each package
        for src in self.get_build_sources(sources_directory, sources_to_build):
            cwd = os.path.join(sources_directory, src)

            logger.debug("Running 'vdt.version' for %s" % src)

            # collect all the arguments
            vdt_args = [
                "--vdt-fpmeditor-path=%s" % fpm_editor_executable,
                "--plugin=%s" % version_plugin]

            if version_extra_args:
                vdt_args += version_extra_args.split("\n")[1:]

            if len(sys.argv) > 1:
                # add optional command line arguments to version
                vdt_args += sys.argv[1:]

            args, extra_args = parse_args(vdt_args)
            logger.debug(
                "calling run with arguments %s from %s" % (
                    " ".join(vdt_args), cwd))

            os.chdir(cwd)
            exit_code = run(args, extra_args)

            if exit_code == 0:
                # sometimes packages are build in a separate directory
                # (fe wheels)
                if build_directory:
                    cwd = os.path.join(cwd, build_directory)
                # move created files to target directory
                package_files = glob(os.path.join(cwd, target_extension))
                if package_files:
                    move_cmd = ["mv"] + package_files + [target_directory]

                    logger.debug("Executing command %s" % move_cmd)
                    logger.debug(
                        subprocess.check_output(move_cmd, cwd=cwd))

    def __call__(self, *args, **kwargs):
        p = argparse.ArgumentParser(
            description="Buildout recipe command to run vdt.version")
        p.add_argument(
            "-v", "--verbose", default=False,
            dest="verbose", action="store_true", help="more output")
        args, extra_args = p.parse_known_args()
        loglevel = logging.DEBUG if args.verbose else logging.INFO
        logging.basicConfig(level=loglevel)

        config = self.get_config()

        for section in config.sections():
            logger.debug("Building section %s" % section)
            self.build(config, section)

build = Build()

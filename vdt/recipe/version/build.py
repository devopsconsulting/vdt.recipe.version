import argparse
import ConfigParser

from glob import glob

import logging
import os
import subprocess

from vdt.version.main import parse_args, run


class Build(object):

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

    def build(self, config, section, cmd_extra_args):
        build_directory = None
        version_extra_args = None
        post_command = None

        version_plugin = config.get(section, 'version-plugin')
        bin_directory = config.get(section, 'bin-directory')

        if config.has_option(section, 'version-extra-args'):
            version_extra_args = config.get(section, 'version-extra-args')

        if config.has_option(section, 'post-command'):
            post_command = config.get(section, 'post-command')

        sources_directory = config.get(section, 'sources-directory')
        sources_to_build = config.get(section, 'sources-to-build').split('\n')

        if config.has_option(section, 'build-directory'):
            build_directory = config.get(section, 'build-directory')

        target_extension = config.get(section, 'target-extension')
        target_directory = config.get(section, 'target-directory')

        # create target directory for the builded packages
        self.create_target_directory(target_directory)

        # add the buildout bin directory to the path
        os.environ['PATH'] = "%s:" % bin_directory + os.environ['PATH']

        # now build each package
        for src in self.get_build_sources(sources_directory, sources_to_build):
            cwd = os.path.join(sources_directory, src)

            logging.info("Running 'vdt.version' for %s" % src)

            # collect all the arguments
            vdt_args = [
                "--plugin=%s" % version_plugin]

            if version_extra_args:
                for row in version_extra_args.split("\n")[1:]:
                    # subprocess.checkoutput wants each argument to be
                    # separate, like ["ls", "-l" "-a"]
                    vdt_args += row.split(" ")

            if cmd_extra_args:
                # add optional command line arguments to version
                vdt_args += cmd_extra_args

            # add target_directory to extra_args
            args, extra_args = parse_args(vdt_args)
            logging.info(
                "calling run with arguments %s from %s" % (
                    " ".join(vdt_args), cwd))

            os.chdir(cwd)
            exit_code = run(args, extra_args)

            if exit_code != 1:
                # sometimes packages are build in a separate directory
                # (fe wheels)
                if build_directory:
                    cwd = os.path.join(cwd, build_directory)
                # move created files to target directory
                package_files = glob(os.path.join(cwd, target_extension))
                if package_files:
                    move_cmd = ["mv"] + package_files + [target_directory]

                    logging.info("Executing command %s" % move_cmd)
                    logging.info(
                        subprocess.check_output(move_cmd, cwd=cwd))

                if post_command:
                    # execute post command in sources directory
                    cwd = os.path.join(sources_directory, src)
                    logging.info("Executing command %s" % post_command)
                    logging.info(subprocess.check_output(
                        post_command, cwd=cwd, shell=True))

    def __call__(self, *args, **kwargs):
        p = argparse.ArgumentParser(
            description="Buildout recipe command to run vdt.version")
        p.add_argument(
            "-v", "--verbose", default=False,
            dest="verbose", action="store_true", help="more output")
        p.add_argument(
            "--section", dest="section", action="store",
            help="Only build a specific section")

        args, extra_args = p.parse_known_args()

        loglevel = logging.DEBUG if args.verbose else logging.INFO
        logging.basicConfig(level=loglevel)

        config = self.get_config()
        sections = config.sections()

        if args.section:
            sections = [args.section]

        for section in sections:
            logging.info("Building section %s" % section)
            self.build(config, section, extra_args)

build = Build()

import ConfigParser
import os


class CreateConfig:
    def __init__(self, buildout, name, options):
        self.buildout = buildout
        self.buildout_dir = buildout['buildout']['directory']
        self.name = name
        self.options = options

    @property
    def config_file(self):
        return os.path.join(self.buildout_dir, ".vdt.recipe.version.cfg")

    def init_config(self):
        # inits or cleans the config
        if not os.path.exists(self.config_file):
            # create file
            cfgfile = open(self.config_file, "w")
            cfgfile.close()
        else:
            with open(self.config_file, "r") as cfgfile:
                config = ConfigParser.ConfigParser()
                config.readfp(cfgfile)
                for section in config.sections():
                    if section not in self.buildout:
                        config.remove_section(section)
            with open(self.config_file, "w") as cfgfile:
                config.write(cfgfile)

    def update(self):
        self.init_config()

        config = ConfigParser.ConfigParser()
        with open(self.config_file, "r") as cfgfile:
            config.readfp(cfgfile)

        if config.has_section(self.name):
            config.remove_section(self.name)
        config.add_section(self.name)

        config.set(
            self.name,
            'version-plugin', self.options.get('version-plugin'))

        version_extra_args = self.options.get('version-extra-args', '')
        if version_extra_args:
            config.set(
                self.name, 'version-extra-args', "\n%s" % version_extra_args)

        post_command = self.options.get('post-command', '')
        if post_command:
            config.set(
                self.name, 'post-command',
                "%s" % post_command.strip("\n"))

        config.set(
            self.name,
            'sources-directory', "%s/src" % self.buildout_dir)
        config.set(
            self.name,
            'sources-to-build', "\n%s" % self.options.get('sources-to-build'))

        if self.options.get('build-directory', ''):
            config.set(
                self.name,
                'build-directory', self.options.get('build-directory'))

        config.set(
            self.name,
            'target-extension', self.options.get('target-extension'))
        config.set(
            self.name,
            'target-directory', self.options.get('target-directory'))

        with open(self.config_file, "w") as cfgfile:
            config.write(cfgfile)
        return ""

    def install(self):
        return self.update()

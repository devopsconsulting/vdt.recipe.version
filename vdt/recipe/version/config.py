import ConfigParser
import os


class CreateConfig:
    def __init__(self, buildout, name, options):
        self.buildout = buildout
        self.buildout_dir = buildout['buildout']['directory']

        self.name = name
        self.options = options

        self.configfile = os.path.join(
            self.buildout_dir, ".vdt.recipe.version.cfg")

    def save(self):
        self.config.write(open(self.configfile, "w"))

    def init(self):
        self.config = ConfigParser.ConfigParser()
        self.config.read(self.configfile)

        for section in self.config.sections():
            if section not in self.buildout:
                self.config.remove_section(section)

        self.save()

    def update(self):
        self.init()

        self.config.read(self.configfile)

        if self.config.has_section(self.name):
            self.config.remove_section(self.name)
        self.config.add_section(self.name)

        self.config.set(
            self.name,
            'version-plugin', self.options.get('version-plugin'))

        self.config.set(
            self.name,
            'bin-directory', "%s/bin" % self.buildout_dir)

        version_extra_args = self.options.get('version-extra-args', '')
        if version_extra_args:
            self.config.set(
                self.name, 'version-extra-args', "\n%s" % version_extra_args)

        post_command = self.options.get('post-command', '')
        if post_command:
            self.config.set(
                self.name, 'post-command',
                "%s" % post_command.strip("\n"))

        self.config.set(
            self.name,
            'sources-directory', "%s/src" % self.buildout_dir)
        self.config.set(
            self.name,
            'sources-to-build', "\n%s" % self.options.get('sources-to-build'))

        if self.options.get('build-directory', ''):
            self.config.set(
                self.name,
                'build-directory', self.options.get('build-directory'))

        self.config.set(
            self.name,
            'target-extension', self.options.get('target-extension'))
        self.config.set(
            self.name,
            'target-directory', self.options.get('target-directory'))

        self.save()

        return ""

    def install(self):
        return self.update()

import ConfigParser


class CreateConfig:
    def __init__(self, buildout, name, options):
        self.buildout = buildout
        self.buildout_dir = buildout['buildout']['directory']
        self.name = name
        self.options = options

    def update(self):
        config = ConfigParser.ConfigParser()

        config.add_section('vdt.recipe.version')

        version_executable = self.options.get(
            'version-executable') or "%s/bin/version" % self.buildout_dir
        config.set(
            'vdt.recipe.version', 'version-executable', version_executable)
        config.set(
            'vdt.recipe.version',
            'version-plugin', self.options.get('version-plugin'))
        config.set(
            'vdt.recipe.version',
            'version-extra-args', self.options.get('version-extra-args'))
        if self.options.get('versions-file'):
            config.set(
                'vdt.recipe.version',
                'versions-file', self.options.get('versions-file'))
        config.set(
            'vdt.recipe.version',
            'sources-directory', "%s/src" % self.buildout_dir)
        config.set(
            'vdt.recipe.version',
            'sources-to-build', "\n%s" % self.options.get('sources-to-build'))
        config.set(
            'vdt.recipe.version',
            'build-directory', self.options.get('build-directory'))
        config.set(
            'vdt.recipe.version',
            'target-extension', self.options.get('target-extension'))
        config.set(
            'vdt.recipe.version',
            'target-directory', self.options.get('target-directory'))

        cfgfile = open("%s/.vdt.recipe.version.cfg" % self.buildout_dir, 'w')
        config.write(cfgfile)
        cfgfile.close()
        return ""

    def install(self):
        return self.update()

import ConfigParser


class CreateConfig:
    def __init__(self, buildout, name, options):
        self.buildout = buildout
        self.buildout_dir = buildout['buildout']['directory']
        self.name = name
        self.versions_file = options.get('versions-file')
        self.sources_to_build = options.get('sources-to-build')

    def update(self):
        config = ConfigParser.ConfigParser()

        config.add_section('vdt.recipe.debian')
        config.set(
            'vdt.recipe.debian',
            'versions-executable', "%s/bin/version" % self.buildout_dir)
        config.set(
            'vdt.recipe.debian', 'versions-file', self.versions_file)
        config.set(
            'vdt.recipe.debian',
            'sources-directory', "%s/src" % self.buildout_dir)
        config.set(
            'vdt.recipe.debian',
            'sources-to-build', "\n%s" % self.sources_to_build)

        cfgfile = open("%s/.vdt.recipe.debian.cfg" % self.buildout_dir, 'w')
        config.write(cfgfile)
        cfgfile.close()

    def install(self):
        self.update()

# vdt.recipe.debian
A recipe which uses `vdt.versionplugin.buildout` to add .deb package building configuration to buildout

Example buildout:

    [buildout]
    parts =
        build-debian-packages
    
    [build-debian-packages]
    recipe = vdt.recipe.debian
    version-plugin = buildout
    version-extra-args = --skip-tag
    versions-file = ${buildout:directory}/profiles/versions.cfg
    sources-to-build =
        my.package
        another.package
    target-directory = ${buildout:directory}/debian-packages

After running the buildout you can generate .deb packages like this:

    bin/debianize


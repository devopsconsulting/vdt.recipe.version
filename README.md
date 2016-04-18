# vdt.recipe.version
A buildout recipe to use vdt.version

Example buildout:

    [buildout]
    parts =
        build-debian-packages
    
    [build-debian-packages]
    recipe = vdt.recipe.version
    version-plugin = buildout
    version-extra-args = --skip-tag
    versions-file = ${buildout:directory}/profiles/versions.cfg
    sources-to-build =
        my.package
        another.package
    target-extension = *.deb
    target-directory = ${buildout:directory}/debian-packages

After running the buildout you can generate .deb packages like this:

    bin/vdt-build


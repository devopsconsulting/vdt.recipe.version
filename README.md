vdt.recipe.version
==================
A buildout recipe to use vdt.version


Example buildout for building .deb packages
-------------------------------------------

Let buildout extend a `versions.cf`g so `vdt.versionplugin.buildout` knows which versions to build:

    [versions]
    zc.buildout = 2.5.0

Configure buildout like the following, including the `--versions-file` argument

    [buildout]
    sources = sources
    parts =
        vdt
        build-debian-packages

    extends = 
        versions.cfg

    extensions =
        mr.developer

    auto-checkout = *

    [sources]
    vdt.recipe.version = git git@github.com:devopsconsulting/vdt.recipe.version.git
    vdt.versionplugine.buildout = git git@github.com:Avira/vdt.versionplugin.buildout.git

    [vdt]
    recipe = zc.recipe.egg:scripts
    eggs = 
        vdt.version
        vdt.versionplugin.buildout
        vdt.recipe.version
    dependent-scripts = true

    [build-debian-packages]
    recipe = vdt.recipe.version
    version-plugin = buildout
    version-extra-args = 
        --skip-tag
        --versions-file=${buildout:directory}/versions.cfg
    sources-to-build =
        vdt.recipe.version
    target-extension = *.deb
    target-directory = ${buildout:directory}/debian-packages

After running the buildout you can generate .deb packages like this:

    bin/vdt-build (<version options>)


Example buildout for building wheels
------------------------------------

    [buildout]
    sources = sources
    parts =
        vdt
        build-wheels

    extensions =
        mr.developer

    auto-checkout = *

    [sources]
    vdt.recipe.version = git git@github.com:devopsconsulting/vdt.recipe.version.git
    vdt.versionplugine.buildout = git git@github.com:Avira/vdt.versionplugin.buildout.git

    [vdt]
    recipe = zc.recipe.egg:scripts
    eggs = 
        vdt.version
        vdt.versionplugin.wheel
        vdt.recipe.version
    dependent-scripts = true

    [build-wheels]
    recipe = vdt.recipe.version
    version-plugin = wheel
    version-extra-args = 
        --skip-tag 
        --build-dependencies
    sources-to-build =
        vdt.recipe.version
    target-extension = *.whl
    build-directory = dist/
    target-directory = ${buildout:directory}/wheels


After running the buildout you can generate wheels like this:

    bin/vdt-build (<version options>)

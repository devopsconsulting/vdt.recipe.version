vdt.recipe.version
==================
A buildout recipe to use `vdt.version`. You will need fpm to build debian packages (https://github.com/jordansissel/fpm). You can have multiple sections so you can build different packages with their own dependencies. Make sure you will run the `bin/vdt-build` command with `fakeroot` when building debian packages.


Example buildout for building .deb and .whl packages
----------------------------------------------------

Let buildout extend a `versions.cfg` so `vdt.versionplugin.buildout` knows which versions to build:

    [versions]
    zc.buildout = 2.5.0

Configure buildout like the following, including the `--versions-file` argument. We also added a wheels section for demonstration purposes.

    [buildout]
    sources = sources
    parts =
        vdt
        build-debian-packages
        build-wheels

    extensions =
        mr.developer

    auto-checkout = *

    [sources]
    vdt.recipe.version = git git@github.com:devopsconsulting/vdt.recipe.version.git
    vdt.versionplugine.buildout = git git@github.com:specialunderwear/vdt.versionplugin.buildout.git branch=bug/nijntje

    [vdt]
    recipe = zc.recipe.egg:scripts
    eggs = 
        vdt.version
        vdt.versionplugin.buildout
        vdt.versionplugin.wheel
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


After running the buildout you can generate .deb packages like this:

    (fakeroot) bin/vdt-build (<version options>)

*************
Release Notes
*************

.. highlight:: console

.. _v0.0.1:

Version 0.0.1
=============

This early access release of the Astra SDK is available only to registered users and for this reason cloning
requires to setup authentication to GitHub.

In order to be able to access the release you need to make sure your GitHub account has been invited
to the `syna-astra Organization <https://github.com/syna-astra>`_ and that you accepted the invitation.
You can check you are able to access the organization by browsing to the `sdk git <https://github.com/syna-astra/sdk>`__.
You can review your organizations by checking your `profile settings <https://github.com/settings/organizations>`__.

Before cloning the sdk you need to setup autentication with the following steps:

1. Create a public/private key pair as described in the `GitHub documentation <https://docs.github.com/en/authentication/connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent#generating-a-new-ssh-key>`__.

2. Add the generated public key to your GitHub profile as described in the `GitHub documentation <https://docs.github.com/en/authentication/connecting-to-github-with-ssh/adding-a-new-ssh-key-to-your-github-account>`__.

In order to be able to access the docker containers you will also need to create a personal access token:

1. Create a *classic* personal access token (PAT) as described in the `GitHub documentation <https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-personal-access-token-classic>`__

2. Ensure the token as the permission ``read:package`` when creating the token

3. When you obtain the token run the following command::
    $ docker login ghcr.io
    Username: <enter your github username>
    Password: <enter the token>

When cloning the ``sdk`` repository git will need to clone it using using a git URL to use this key to authenticate to GitHub to download the Yocto recipes:

1. Ensure you have loaded your ssh-key into the ssh-agent running on your host. For more information check the `GitHub documentation <https://docs.github.com/en/authentication/connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent#adding-your-ssh-key-to-the-ssh-agent>`__.

2. Use the following command line to clone::

    $ git clone --recursive git@github.com:syna-astra/sdk

When starting a build you need to perform these additional steps:

1. Ensure you have loaded your ssh-key into the ssh-agent running on your host (see `GitHub documentation <https://docs.github.com/en/authentication/connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent#adding-your-ssh-key-to-the-ssh-agent>`__

2. Use the following command line when starting the CROPS container::

    $ docker run --rm -it -v $(pwd):$(pwd) \
      -e SSH_AUTH_SOCK -v $SSH_AUTH_SOCK:$SSH_AUTH_SOCK \
      -v $(pwd)/.ssh/known_hosts:/home/pokyuser/.ssh/known_hosts \
      ghcr.io/syna-astra/crops --workdir=$(pwd)

This will ensure that the build environment will have access to the ssh keys when donwloading the sources of the different Astra recipes and that git
inside the container can leverage the ssh known_hosts of your user.


Known issues
------------

During the build the following messages are displayed::

    WARNING: synasdk-tools-native-0.0.1+gitAUTOINC+5b2d1a4ff6-r1 do_unpack: Failed to find a git repository in WORKDIR: /home/astra-test/sdk/build-sl1680/tmp/work/x86_64-linux/synasdk-tools-native/0.0.1+gitAUTOINC+5b2d1a4ff6-r1
    WARNING: synasdk-security-0.0.1+gitAUTOINC+5b2d1a4ff6-r2 do_unpack: Failed to find a git repository in WORKDIR: /home/astra-test/sdk/build-sl1680/tmp/work/sl1680-poky-linux/synasdk-security/0.0.1+gitAUTOINC+5b2d1a4ff6-r2
     linux-firmware-syna-5.15.140-r0 do_package_qa: QA Issue: Recipe LICENSE includes obsolete licenses GPLv2 [obsolete-license]


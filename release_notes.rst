*************
Release Notes
*************

.. highlight:: console

.. _v0.0.1:

Version 0.0.1
=============

This early access release of the Astra SDK is available only to registered users and for this reason cloning
requires to setup authentication to GitHub.

.. note::

    It is recommended to use a Ubuntu 22.04 host to run the following instructions. See :ref:`yocto_prerequisites` for
    more details.

Organization invitation
-----------------------

In order to be able to access the release you need to make sure your GitHub account has been invited
to the `syna-astra Organization <https://github.com/syna-astra>`_ and that you accepted the invitation.
You can check you are able to access the organization by browsing to the `sdk git <https://github.com/syna-astra/sdk>`__.
You can review your organizations by checking your `profile settings <https://github.com/settings/organizations>`__.

Setup authenticated Docker registry access
------------------------------------------

In order to be able to access the docker containers you will also need to create a personal access token:

1. Create a *classic* personal access token (PAT) with ``read:package`` permissions as described in the `GitHub documentation <https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-personal-access-token-classic>`__.

2. After obtaining the token run the following command::

    $ docker login ghcr.io
    Username: <enter your GitHub username>
    Password: <enter the token>


Initial setup of workspace
--------------------------

When first starting a build you need to perform following steps:

1. Create a local directory where your build will be located::

     $ mkdir workspace && cd workspace

2. Create a directory to store the ssh configuration::

     $ mkdir ssh && chmod 700 ssh

2. Use the following command line when starting the CROPS container::

    $ docker run --rm -it -v $(pwd):$(pwd) -v $(pwd)/ssh:/home/pokyuser/.ssh ghcr.io/syna-astra/crops:v0.0.1 --workdir=$(pwd)

3. Create a ssh public/private keypair::

     pokyuser $ ssh-keygen -t ed25519 -C "your_email@example.com"

   To simplify your setup you can leave the passphrase empty, if your IT mandates a passphrase you may do so but you
   will need to `setup an ssh-agent <https://docs.github.com/en/authentication/connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent?platform=linux#adding-your-ssh-key-to-the-ssh-agent>`__.

4. Add the generated public key to your GitHub profile as described in the `GitHub documentation <https://docs.github.com/en/authentication/connecting-to-github-with-ssh/adding-a-new-ssh-key-to-your-github-account?platform=linux&tool=webui>`__.

5. Clone the sdk repository using ssh instead of https::

     $ git clone -b v0.0.1 --recurse-submodules git@github.com:syna-astra/sdk

   This step will also ask you to accept the github host key. You can validate the key using the information found
   in the `GitHub Documentation <https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/githubs-ssh-key-fingerprints>`_.
   This step is important to ensure ``bitbake`` will also be able to successfully connect to GitHub.

Restarting build environment from an existing workspace
-------------------------------------------------------

When starting an existing build environment you must change your directory to the ``workspace`` directory and
start the build environment as follow::

    $ docker run --rm -it -v $(pwd):$(pwd) -v $(pwd)/ssh:/home/pokyuser/.ssh ghcr.io/syna-astra/crops:v0.0.1 --workdir=$(pwd)

The build environment will find the existing ssh key and known host keys from the initial setup.

Known issues
------------

During the build the following messages are displayed::

    WARNING: synasdk-tools-native-0.0.1+gitAUTOINC+5b2d1a4ff6-r1 do_unpack: Failed to find a git repository in WORKDIR: /home/astra-test/sdk/build-sl1680/tmp/work/x86_64-linux/synasdk-tools-native/0.0.1+gitAUTOINC+5b2d1a4ff6-r1
    WARNING: synasdk-security-0.0.1+gitAUTOINC+5b2d1a4ff6-r2 do_unpack: Failed to find a git repository in WORKDIR: /home/astra-test/sdk/build-sl1680/tmp/work/sl1680-poky-linux/synasdk-security/0.0.1+gitAUTOINC+5b2d1a4ff6-r2
     linux-firmware-syna-5.15.140-r0 do_package_qa: QA Issue: Recipe LICENSE includes obsolete licenses GPLv2 [obsolete-license]

These warnings can be ignored.
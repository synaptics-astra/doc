=======================
Qt5 Compilation Guide
=======================

.. highlight:: console

This guide describes how to build the Astra image with Qt5 support enabled. Follow the standard
image build procedure described in :doc:`/quickstart/build_image`, with the single modification
below when setting up the build tree.

Enabling Qt5
============

When sourcing ``setup-environment`` in step 3 of the :doc:`/quickstart/build_image`, prefix the command with
``QT_MAJOR=5``::

    pokyuser@xyz:/path/to/workspace/sdk $ QT_MAJOR=5 . meta-synaptics/setup/setup-environment

.. note::

    Passing ``QT_MAJOR=5`` before sourcing ``setup-environment`` instructs the build system to
    select Qt5 libraries and modules when building packages that depend on Qt.

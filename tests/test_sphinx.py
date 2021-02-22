"""Test the :mod:`sphinx` documentation generation."""

import shutil
from os.path import join, isdir

from sphinx.application import Sphinx

SRCDIR = CONFDIR = 'docs'
OUTDIR = join('tests', 'files', 'build')
DOCTREEDIR = join('tests', 'files', 'build', 'doctrees')


def test_sphinx_build() -> None:
    """Test :meth:`sphinx.application.Sphinx.build`."""
    try:
        app = Sphinx(SRCDIR, CONFDIR, OUTDIR, DOCTREEDIR,
                     buildername='html', warningiserror=True)
        app.build(force_all=True)
    finally:
        if isdir(OUTDIR):
            shutil.rmtree(OUTDIR)

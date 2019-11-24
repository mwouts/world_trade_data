"""Run the README.md, and re-create the index.html if missing"""

import os
from jupytext.cli import jupytext as jupytext_cli, system


def test_execute_readme_and_update_index_html():
    nb_path = os.path.dirname(os.path.abspath(__file__))
    readme = os.path.join(nb_path, '..', 'README.md')
    readme_ipynb = os.path.join(nb_path, '..', 'README.ipynb')
    index = os.path.join(nb_path, '..', 'index.html')

    jupytext_cli([readme, '--execute', '--to', 'ipynb'])
    system('jupyter', 'nbconvert', '--to', 'html', readme_ipynb, '--output', index)

# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'ansible-sdk'
copyright = '2022, Ansible'
author = 'Ansible'
release = '0.0.1'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.intersphinx',
    'sphinx_immaterial',
    'sphinx_immaterial.apidoc.python.apigen'
]

intersphinx_mapping = {
    'python': ('https://docs.python.org/3', None),
}

python_apigen_modules = {
      "ansible_sdk": "api/",
      "ansible_sdk.executors": "api/executors/"
}

# Temporarily ignore "missing reference" warnings with apidoc generation.
nitpicky = True
nitpick_ignore = [
    ('py:class', 'ansible_sdk.executors.base.AnsibleJobExecutorOptionsBase'),
    ('py:class', 'ansible_sdk.executors.subprocess._AnsibleContainerJobOptions'),
    ('py:class', 'ansible_sdk.executors.subprocess._AnsibleContainerJobExecutorBase'),
    ('py:class', 'ansible_sdk._util.dataclass_compat._DataclassReplaceMixin'),
    ('py:class', 'ansible_sdk.executors.subprocess._AnsibleContainerJobExecutorBase'),
    ('py:class', 'ansible_sdk.executors.subprocess._AnsibleContainerJobOptions'),
    ('py:class', 'ansible_sdk.executors.subprocess._AnsibleContainerJobExecutorBase'),
    ('py:class', 'ansible_sdk.executors.subprocess._AnsibleContainerJobOptions'),
    ('py:class', 'ansible_sdk._util.dataclass_compat._DataclassReplaceMixin'),
    ('py:class', 'ansible_sdk.executors.subprocess._AnsibleContainerJobExecutorBase'),
    ('py:class', 'ansible_sdk.executors.subprocess.OptionsT'),
    ('py:class', 'ansible_sdk.executors.subprocess._AnsibleContainerJobOptions'),
    ('py:class', 'ansible_sdk.executors.mesh.AnsibleMeshJobOptions'),
]

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = "ansible"
highlight_language = "YAML+Jinja"

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_immaterial'
html_title = "Ansible SDK API Reference"
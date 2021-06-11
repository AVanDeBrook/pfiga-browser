{{ path_name }}
################################

.. toctree::
    :maxdepth: 2
    :caption: Contents:

    {% for readme in second_level_readmes %}
    {{ readme.path }}
    {% endfor %}

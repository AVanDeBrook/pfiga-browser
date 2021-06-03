{{ folder_name }}
###########################

Below are all the graphics in this folder:

{% for image in images %}

{{ image.name }}: {{ image.description }}

{{ image.name }}: small

.. image:: {{ image.name }}
   :width: {{ image.wdith.small }}

{{ image.name }}: large

.. image:: {{ image.name }}
   :width: {{ image.width.large }}

{% endfor %}

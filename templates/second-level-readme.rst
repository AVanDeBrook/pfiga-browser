{% for image in images %}
**{{ image.name }}**. {{ image.description }}

.. image:: {{ image.uri }}
   :width: {{ image.width }}

{% endfor %}

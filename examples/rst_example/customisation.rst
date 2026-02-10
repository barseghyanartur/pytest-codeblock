Customisation
=============
Customisation examples.

.. External references
.. _openai: https://github.com/openai/openai-python
.. _moto: https://docs.getmoto.org
.. _fake.py: https://github.com/barseghyanartur/fake.py

`fake.py`_ example for `.. code-block::` directive
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. code-block:: rst

    .. pytestmark: fakepy
    .. code-block:: python
        :name: test_create_pdf_file

        from fake import FAKER

        file = FAKER.pdf_file()

        assert file.data["storage"].exists(str(file))

`moto`_ example for `.. code-block::` directive
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. code-block:: rst

    .. pytestmark: aws
    .. code-block:: python
        :name: test_create_bucket

        import boto3

        s3 = boto3.client("s3", region_name="us-east-1")
        s3.create_bucket(Bucket="my-bucket")
        assert "my-bucket" in [b["Name"] for b in s3.list_buckets()["Buckets"]]

`openai`_ example for `.. code-block::` directive
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. code-block:: rst

    .. pytestmark: xfail
    .. pytestmark: openai
    .. code-block:: python
        :name: test_tell_me_a_joke

        from openai import OpenAI

        client = OpenAI()
        completion = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "developer", "content": "You are a famous comedian."},
                {"role": "user", "content": "Tell me a joke."},
            ],
        )

        assert isinstance(completion.choices[0].message.content, str)

`fake.py`_ example for `.. literalinclude::` directive
------------------------------------------------------
.. code-block:: rst

    .. pytestmark: fakepy
    .. literalinclude:: examples/python/create_pdf_file_example.py
        :name: test_li_create_pdf_file

`moto`_ example for `.. literalinclude::` directive
---------------------------------------------------
.. code-block:: rst

    .. pytestmark: aws
    .. literalinclude:: examples/python/create_bucket_example.py
        :name: test_li_create_bucket

`openai`_ example for `.. literalinclude::` directive
-----------------------------------------------------

.. code-block:: rst

    .. pytestmark: openai
    .. literalinclude:: examples/python/tell_me_a_joke_example.py
        :name: test_li_tell_me_a_joke

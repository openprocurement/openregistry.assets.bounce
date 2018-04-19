Overview
========

openregistry.assets.bounce contains the description of the Registry Data Base.

Features
--------

* Asset represents the initial information of an object to be privatized.
* The object to be created should be switched from `draft` to `pending`.
* Asset is being created with the automatically added `documentType: cancellationDetails`. 
* Asset is a complicated entity the components of which are marked as items.
* For the asset to be deleted, the specific document (`documentType: cancellationDetails`) has to be attached.

Conventions
-----------

API accepts `JSON <http://json.org/>`_ or form-encoded content in
requests.  It returns JSON content in all of its responses, including
errors.  Only the UTF-8 character encoding is supported for both requests
and responses.

All API POST and PUT requests expect a top-level object with a single
element in it named `data`.  Successful responses will mirror this format. 
The data element should itself be an object, containing the parameters for
the request.

If the request was successful, we will get a response code of `201`
indicating the object was created.  That response will have a data field at
its top level, which will contain complete information on the new auction,
including its ID.

If something went wrong during the request, we'll get a different status
code and the JSON returned will have an `errors` field at the top level
containing a list of problems.  We look at the first one and print out its
message.

---------------------

Project status
--------------

The project has pre alpha status.

The source repository for this project is on GitHub: 
https://github.com/openprocurement/openregistry.assets.bounce  

Documentation of related packages
---------------------------------

* `OpenProcurement API <http://api-docs.openprocurement.org/en/latest/>`_

API stability
-------------

API is relatively stable. The changes in the API are communicated via `Open Procurement API
<https://groups.google.com/group/open-procurement-api>`_ maillist.

Change log
----------

0.1
~~~

Not Released

 - Set up general build, testing, deployment, and ci framework.
 - Creating/modifying asset

Next steps
----------
You might find it helpful to look at the :ref:`tutorial`, or the
:ref:`reference`.

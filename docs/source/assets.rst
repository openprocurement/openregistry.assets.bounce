.. Kicking page rebuild 2014-10-30 20:55:46
.. _assets:

Retrieving Asset Information
=============================

Getting list of all assets
--------------------------


   Getting list of all assets.

   **Example request**:

   .. sourcecode:: http

   GET /api/0/assets HTTP/1.0
   Host: lb.api-sandbox.registry.ea2.openprocurement.net

   **Example response**:

   .. sourcecode:: http

      Response: 200 OK
      Content-Type: application/json
      X-Content-Type-Options: nosniff

      {
        "next_page": {
          "path": "/api/2.4/assets?offset=2018-05-22T13%3A39%3A54.510132%2B03%3A00", 
          "uri": "http://lb.api-sandbox.registry.ea2.openprocurement.net/api/2.4/   assets?offset=2018-05-22T13%3A39%3A54.510132%2B03%3A00", 
          "offset": "2018-05-22T13:39:54.510132+03:00"
        }, 
        "data": [
          {
            "id": "5c8cd4c766c74f60b25b2b9cdbfb8ef7", 
            "dateModified": "2018-05-22T13:39:54.510132+03:00"
          }
        ]
      }


   :query offset: offset number
   :query limit: limit number. default is 100
   :reqheader Authorization: optional OAuth token to authenticate
   :statuscode 200: no error
   :statuscode 404: endpoint not found

Sorting
~~~~~~~
Assets returned are sorted by modification time.

Limiting number of Assets returned
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

You can control the number of `data` entries in the assets feed (batch
size) with `limit` parameter. If not specified, data is being returned in
batches of 100 elements.

Batching
~~~~~~~~

The response contains `next_page` element with the following properties:

:offset:
    This is the parameter you have to add to the original request you made
    to get next page.

:path:
    This is path section of URL with original parameters and `offset`
    parameter added/replaced above.

:uri:
    The full version of URL for next page.

If next page request returns no data (i.e. empty array) then there is little
sense in fetching further pages.

Synchronizing
~~~~~~~~~~~~~

It is often necessary to be able to syncronize central database changes with
other database (we'll call it "local").  The default sorting "by
modification date" together with Batching mechanism allows one to implement
synchronization effectively.  The synchronization process can go page by
page until there is no new data returned.  Then the synchronizer has to
pause for a while to let central database register some changes and attempt
fetching subsequent page.  The `next_page` guarantees that all changes
from the last request are included in the new batch.

The safe frequency of synchronization requests is once per 5 minutes.
 
Reading the individual asset information
-----------------------------------------

.. http:get:: /assets/{uuid4:id}

   Getting asset details.

   **Example request**:

   .. sourcecode:: http

    GET /api/2.4/assets/2f684c8a57f447768a5a451e2e8e5892 HTTP/1.0
    Host: lb.api-sandbox.registry.ea2.openprocurement.net

   **Example response**:

   .. sourcecode:: http

   Response: 200 OK
   Content-Type: application/json

   {
     "data": {
       "status": "pending", 
       "assetType": "bounce", 
       "documents": [
         {
           "title": "Інформація про оприлюднення інформаційного повідомлення", 
           "url": "https://prozorro.sale/info/ssp_details ", 
           "documentOf": "asset", 
           "datePublished": "2018-05-22T13:39:54.423035+03:00", 
           "documentType": "informationDetails", 
           "dateModified": "2018-05-22T13:39:54.423082+03:00", 
           "id": "e5796e629edd4477a730aa732a425f9d"
         }
       ], 
       "description": "Опис землі для космодрому", 
       "title": "Земля для космодрому", 
       "assetID": "UA-AR-DGF-2018-05-22-000001", 
       "items": [
         {
           "registrationDetails": {
             "status": "unknown"
           }, 
           "description": "футляри до державних нагород", 
           "classification": {
             "scheme": "CAV-PS", 
             "description": "Description", 
             "id": "06121000-6"
           }, 
           "additionalClassifications": [
             {
               "scheme": "UA-EDR", 
               "description": "папір і картон гофровані, паперова й картонна тара", 
               "id": "17.21.1"
             }
           ], 
           "address": {
             "countryName": "Ukraine"
           }, 
           "id": "ca254ba6052947539d7bb26aaa163e8d", 
           "unit": {
             "code": "code"
           }, 
           "quantity": 5.0001
         }, 
         {
           "registrationDetails": {
             "status": "unknown"
           }, 
           "description": "футляри до державних нагород", 
           "classification": {
             "scheme": "CAV-PS", 
             "description": "Description", 
             "id": "06121000-6"
           }, 
           "additionalClassifications": [
             {
               "scheme": "UA-EDR", 
               "description": "папір і картон гофровані, паперова й картонна тара", 
               "id": "17.21.1"
             }
           ], 
           "address": {
             "countryName": "Ukraine"
           }, 
           "id": "1a1cf1d83a424e7284976caef828d680", 
           "unit": {
             "code": "code"
           }, 
           "quantity": 5.0001
         }
       ], 
       "dateModified": "2018-05-22T13:39:54.429965+03:00", 
       "owner": "broker", 
       "date": "2018-05-22T13:39:54.422540+03:00", 
       "decisions": [
         {
           "decisionDate": "2018-05-22T13:39:53.504199+03:00", 
           "decisionID": "1111-4"
         }
       ], 
       "id": "5c8cd4c766c74f60b25b2b9cdbfb8ef7", 
       "assetCustodian": {
         "contactPoint": {
           "name": "Державне управління справами", 
           "telephone": "0440000000"
         }, 
         "identifier": {
           "scheme": "UA-EDR", 
           "id": "00037256", 
           "uri": "http://www.dus.gov.ua/"
         }, 
         "name": "Державне управління справами", 
         "address": {
           "postalCode": "01220", 
           "countryName": "Україна", 
           "streetAddress": "вул. Банкова, 11, корпус 1", 
           "region": "м. Київ", 
           "locality": "м. Київ"
         }
       }
     }
   }


   :reqheader Authorization: optional OAuth token to authenticate
   :statuscode 200: no error
   :statuscode 404: asset not found
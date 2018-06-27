.. . Kicking page rebuild 2014-10-30 17:00:08
.. include:: defs.hrst

.. index:: Asset, Period, Date, Item, Documents

.. _asset:

Asset
=====

Schema
------

:id:
    string, auto-generated, read-only
    
:assetID:
   string, auto-generated, read-only

   The asset identifier to refer to in the `paper` documentation. 

   |ocdsDescription|
   AssetID is included to make the flattened data structure more convenient.
   
:date:
    string, auto-generated, read-only
    
    The date of asset creation/undoing.

:owner:  
    string, auto-generated, read-only

    The entity whom the asset has been created by.
    
:dateModified:
    string, auto-generated, read-only
    
    |ocdsDescription|
    Date when the asset was last modified.
    
:rectificationPeriod:
    :ref:`Period`, auto-generated

    Period during which the owner of an asset can edit it.

:status:
    string, required
    
    The asset status within the Registry.

    Possible values are:

    * `draft`

    * `pending`

    * `verification`

    * `active`

    * `complete`

    * `deleted`
    
:relatedLot:
    string, required in `active` status
    
    ID of the related Lot.
    
:title:
    string, multilingual, required
    
    * Ukrainian by default (required) - Ukrainian title
    
    * ``title_en`` (English) - English title
    
    * ``title_ru`` (Russian) - Russian title
    
    Oprionally can be mentioned in English/Russian.
    
:description:
    string, multilingual, required
    
    |ocdsDescription|
    A description of the goods, services to be provided.
    
    * Ukrainian by default - Ukrainian decription
    
    * ``decription_en`` (English) - English decription
    
    * ``decription_ru`` (Russian) - Russian decription
    
:documents:
    array of :ref:`Documents`
    
    |ocdsDescription|
    All related documents and attachments.
    
:assetCustodian:
   :ref:`Organization`, required

   The entity managing the asset.

:assetHolder:
   :ref:`Organization`, optional

   The entity whom the asset was used to be owned by.
    
:decisions:
    array of :ref:`Decisions`, required

:item:
    array of :ref:`item`, required

:mode:
    optional

    The additional parameter with a value `test`.

:assetType:
    string, required

    Type of the given asset. The only value is `domain`.
    
:sandboxParameters:
   string, optional

   Parameter that accelerates auction periods. Set quick, accelerator=1440 as text value for `sandboxParameters` for the time frames to be reduced in 1440 times.

.. _decisions:

Decisions
=========

Schema
------

:title:
    string, multilingual, optional
    
    * Ukrainian by default (optional) - Ukrainian title
    
    * ``title_en`` (English) - English title
    
    * ``title_ru`` (Russian) - Russian title

:decisionOf:
    string, auto-generated

    The given value is `asset`.

:decisionDate:
    :ref:`Date`, required

    |ocdsDescription|
    The date on which the document was first published.

:decisionID:
    string, required

    The decision identifier to refer to in the `paper` documentation. 

.. _period:

Period
=======    

Schema
------

:startDate:
    string, :ref:`Date`

    |ocdsDescription|
    The start date for the period.
    `startDate` should always precede `endDate`.

:endDate:
    string, :ref:`Date`

    |ocdsDescription|
    The end date for the period.

.. _date:

Date
====

Date/time in `ISO 8601 <https://en.wikipedia.org/wiki/ISO_8601#Dates>`_.

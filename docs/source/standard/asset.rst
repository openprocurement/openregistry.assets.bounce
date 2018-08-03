.. . Kicking page rebuild 2014-10-30 17:00:08
.. include:: defs.hrst

.. index:: Asset, Period, Date, Item, Documents

.. _asset:

Asset
=====

Schema
------

:id:
   uuid, auto-generated, read-only

   Internal identifier for this asset.
    
:assetID:
   string, auto-generated, read-only

   The asset identifier to refer to in the `paper` documentation. 

   |ocdsDescription|
   `AssetID` is included to make the flattened data structure more convenient.
   
:date:
    :ref:`Date`, auto-generated, read-only
    
    The date of asset creation/undoing.

:owner:
    string, auto-generated, read-only

    The entity whom the asset has been created by.
    
:dateModified:
    :ref:`Date`, auto-generated, read-only
    
    |ocdsDescription|
    Date when the asset was last modified.
    
:rectificationPeriod:
    :ref:`Period`, auto-generated, read-only

    Period during which the owner of an asset can edit it.

:status:
    string, required
    
    The asset status within the Registry.

    Possible values are:

+-------------------------+-------------------------------------+
|        Status           |            Description              |
+=========================+=====================================+
|  `draft`                | Asset created but not yet available |
+-------------------------+-------------------------------------+
|  `pending`              | Asset entered in the register       |
+-------------------------+-------------------------------------+
|  `verification`         | Asset availability check            |
+-------------------------+-------------------------------------+
|  `active`               | Passes an auction on the asset      |
+-------------------------+-------------------------------------+
|  `complete`             | Asset sold at auction               |
+-------------------------+-------------------------------------+
|  `deleted`              | The asset has been deleted          |
+-------------------------+-------------------------------------+
    
:relatedLot:
    uuid ,auto-generated, read-only
    
    Internal id of the related Lot.
    
:title:
    string, multilingual, required
    
    * Ukrainian by default (required) - Ukrainian title
    
    * ``title_en`` (English) - English title
    
    * ``title_ru`` (Russian) - Russian title
    
    Optionally can be mentioned in English/Russian.
    
:description:
    string, multilingual, required
    
    |ocdsDescription|
    A description of the goods, services to be provided.
    
    * Ukrainian by default - Ukrainian decription
    
    * ``decription_en`` (English) - English decription
    
    * ``decription_ru`` (Russian) - Russian decription
    
:documents:
    Array of :ref:`Documents`, optional
    
    |ocdsDescription|
    All related documents and attachments.
    
:assetCustodian:
   :ref:`Organization`, required

   The entity managing the asset. For a small privatization, the role is carried out by the Privatization Authority.

:assetHolder:
   :ref:`Organization`, optional

   The entity whom the asset was used to be owned by.
    
:decisions:
    Array of :ref:`Decisions`, required

    The decision to privatize the asset. Approval of the terms of sale of the lot.

:items:
    Array of :ref:`items`, required

    |ocdsDescription|
    The goods, services, and any intangible outcomes in this contract.

:mode:
    string, optional

    The additional parameter with a value `test`.

:assetType:
    string, required

    Type of the given asset. The only value is `domain`.
    
:sandboxParameters:
   string, optional

   Parameter that accelerates asset periods. Set quick, accelerator=1440 as text value for `sandboxParameters` for the time frames to be reduced in 1440 times.

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
======

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

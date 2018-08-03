.. _acceleration:

Acceleration mode for sandbox
=============================

If you want to experiment with assets, you can use acceleration mode and start your assets name "TESTING".

Acceleration mode was developed to enable testing in the sandbox and to reduce time frames of the periods. 

To enable acceleration mode you will need to:
    * add additional parameter `mode` with a value ``test``;
    * set ``quick, accelerator=1440`` as text value for `sandboxParameters`. This parameter will accelerate auction periods. The number 1440 shows that restrictions and time frames will be reduced in 1440 times.

**This mode will work only in the sandbox**.

.............................

Synchronization
~~~~~~~~~~~~~~~

* During normal auction synchronization via ``/auctions`` test auctions are not visible.

* To get test auctions synchronize via ``/auctions?mode=test``.

* If you synchronize via ``/auctions?mode=all``, then you will get all auctions.

* Auction mode can be set only on lot creation (lots.auctions) phase, it can not be set later.

.. note:: Can not be used for assets.

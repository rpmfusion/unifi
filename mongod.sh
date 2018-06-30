#!/bin/bash
#
# Workaround script for MongoDB 3.6 no longer accepting --nohttpinterface.
#
exec /usr/bin/mongod ${*//--nohttpinterface/}

# SSURGOOnDemand-SQLite
 NCSS soil survey aggregation engine for SSURGO SQLite or Geoppackage databases
 
This tool uses python to generate soi property or interpretation information by aggregating the tables in a SQLite or Geoppackage SSURGO template database.  It leverages the tkinter libraries native to python giving the tools a GUI interface.  It is a companion application to SSURGO portal which builds the required template databases.  All of the information derived from the tools are dependent on what is in the input database and thus an internet connection is not required.  Soils data is annually updated around October 1.  Any changes made to Web Soil Survey information need to be reqcquired to be current.  While rare, out-of-cycle refreshes to soil survey areas do happen.

In order to properly use these tools a user must understand the concept of soil mapunit aggregation.

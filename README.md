# TCE download
Download .tcz extenstions from the outside of the Tiny Core Linux

# How to use
1. Add the packages you need to download into download.lst file
2. Run "python3 tce-download.py"
This would generate "/tce/onboot.lst" and populate "/tce/optional/" with your packages<br>
You can than burn TinyCore.iso onto the USB flash drive, copy /tce folder to it<br>
and specify the boot codes like: "waitusb=5 tce=sdb"<br>
You should have your packages loaded on boot.

# Credits
Thanks to Juanito from TinyCoreLinux team for support on forum.

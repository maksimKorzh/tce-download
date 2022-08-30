# TCE download
Download .tcz extensions from the outside of the Tiny Core Linux

# How to use
1. Add the packages you need to download into download.lst file
2. Optionally alter "MIRROR" variable in the "tce-download.py"
3. Run "python3 tce-download.py"<br><br>
This would generate "/tce/onboot.lst" and populate "/tce/optional/" with your packages<br>
You can than burn TinyCore.iso onto the USB flash drive, copy /tce folder to it<br>
and specify the boot codes like: "waitusb=5 tce=sdb"<br>
You should have your packages loaded on boot after.

# Video demo
https://www.youtube.com/watch?v=bAY2xAUv5YQ

# Credits
Thanks to Juanito from TinyCoreLinux team for support on forum.

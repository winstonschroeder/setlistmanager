# Tutorial for using "SainSmart st7735 1.8" or "KMR-1.8 spi" display

since raspbian 5.4 module fbtft_device is no longer supported, instead the use of device tree overrides became mandatory see https://www.gtkdb.de/index_36_3100.html

Basically the generation of a device tree overlay consists of three steps:

1. Create a device tree configuration file
2. Compile this file with device tree compiler and store it to /boot/overlays/ directory
3. Append the overlay to /boot/config.txt file -> add line dtoverlay=<dts file name>

Make sure that GPIO pins for SPI are assigned correctly or adjust .dts file. DC=>GPIO24 RESET=>GPIO25

## SaintSmart device

For SaintSmart device use the following commands:

```
echo "/* Device tree overlay for ST7735R */

/dts-v1/; /plugin/;

/ { compatible = "brcm,bcm2835", "brcm,bcm2708", "brcm,bcm2709";

fragment@0 { target = <&spi0>; **overlay** { status = "okay"; }; };

fragment@1 { target = <&spidev0>; **overlay** { status = "disabled"; }; };

fragment@2 { target = <&gpio>; **overlay** { st7735r_display_pins: st7735r_display_pins { brcm,pins = <24 25>; brcm,function = <1 1>; brcm,pull = <0 0>; }; }; };

fragment@3 { target = <&spi0>; overlay { /* needed to avoid dtc warning */ #address-cells = <1>; #size-cells = <0>;

  st7735rdisplay: st7735r-display@0{
    compatible = "jianda,jd-t18003-t01", "sitronix,st7735r";
    reg = <0>;
    pinctrl-names = "default";
    pinctrl-0 = <&st7735r_display_pins>;

    spi-max-frequency = <32000000>;
    rotation = <0>;
    fps = <20>;
    height = <160>;
    width = <128>;
    buswidth = <8>;
    reset-gpios = <&gpio 25 0>;
    dc-gpios = <&gpio 24 0>;
    debug = <0>;
  };
};
};
overrides { speed = <&st7735rdisplay>,"spi-max-frequency:0"; rotate = <&st7735rdisplay>,"rotation:0"; fps = <&st7735rdisplay>,"fps:0"; debug = <&st7735rdisplay>,"debug:0"; }; };" > ~/st7735r.dts
```

... and compile it: `sudo dtc -@ -I dts -O dtb -o /boot/overlays/st7735r.dtbo ~/st7735r.dts`

Finally append to config: `echo "dtoverlay=st7735r" >> /boot/config.txt`

## KMR-1.8 spi device

**TODO:** following file is still buggy. Fix name changes where appropriate.

```
echo "/* Device tree overlay for ST7735R */

/dts-v1/; /plugin/;

/ { compatible = "brcm,bcm2835", "brcm,bcm2708", "brcm,bcm2709";

fragment@0 { target = <&spi0>; **overlay** { status = "okay"; }; };

fragment@1 { target = <&spidev0>; **overlay** { status = "disabled"; }; };

fragment@2 { target = <&gpio>; **overlay** { st7735r_display_pins: st7735r_display_pins { brcm,pins = <24 25>; brcm,function = <1 1>; brcm,pull = <0 0>; }; }; };

fragment@3 { target = <&spi0>; **overlay** { /\* needed to avoid dtc warning \*/ #address-cells = <1>; #size-cells = <0>;


  st7735rdisplay: st7735r-display@0{
    compatible = "jianda,jd-t18003-t01", "sitronix,st7735r";
    reg = <0>;
    pinctrl-names = "default";
    pinctrl-0 = <&st7735r_display_pins>;

    spi-max-frequency = <32000000>;
    rotation = <270>;
    fps = <20>;
    height = <128>;
    width = <160>;
    buswidth = <8>;
    reset-gpios = <&gpio 25 0>;
    dc-gpios = <&gpio 24 0>;
    debug = <0>;
  };
};

};

**overrides** { speed = <&st7735rdisplay>,"spi-max-frequency:0"; rotate = <&st7735rdisplay>,"rotation:0"; fps = <&st7735rdisplay>,"fps:0"; debug = <&st7735rdisplay>,"debug:0"; }; };" > \~/kmr-1.8.dts

```

... and compile it: `sudo dtc -@ -I dts -O dtb -o /boot/overlays/kmr-1.8.dtbo ~/kmr-1.8.dts`

Finally append to config: `sudo echo "dtoverlay=kmr-1.8" >> /boot/config.txt`

# Tutorial on using raspbian desktop with autologin

First install default desktop manager with:

```
sudo apt-get install raspberrypi-ui-mods
```

Then change ownership of \~/.Xauthority from root to pi or corresponding user if not pi is used:

```
chown pi:pi /home/pi/.Xauthority  
```

# Tutorial running python app on startup

First create a script */home/pi/pystarter.sh* (any other directory is also sufficient).

Content of this file is something like:

```
if [ $# -ge 1 ]; then
        app="$(which $1)"
        openbox="$(which openbox)"
        tmpapp="/tmp/tmpapp.sh"
        DISPLAY=:1.0
        echo -e "${openbox} &\n${app}" > ${tmpapp}
        echo "starting ${app}"
#        xinit ${app} -- :0 vt1 -xf86config xorg-app.conf || exit 1
        xinit ${app} -- :0 -xf86config xorg-app.conf vt$XDG_VTNR || exit 1
else
        echo "not a valid argument"
fi
```

In this script an extra xorg configuration file is included. If there are no needs for extra configurations simply create an empty file as */etc/X11/xorg-app.conf*.

Make the file executable:

```
sudo chmod +x /home/pi/pystart.sh
```

Next edit */etc/rc.local* and add an extra line at the end of it but befort last line "exit 0":

```
sudo /home/pi/pystarter.sh /home/pi/<pthon-script-to-be-run>.py
```

**Note:** This setup assumes, that first line of the script must be *#!/usr/bin/python* and the file has to be executable as well.

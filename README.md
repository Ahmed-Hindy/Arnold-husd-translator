# HtoA Obj Lights to Solaris Translator

Translates Obj Arnold lights into Solaris USD prims.

![img.png](images/img.png)
image compares Arnold ROP render (bot) and Arnold Solaris (top) Renders using Arnold lights made in OBJ.

## Features
- Translates Arnold Obj lights into Solaris USD prims.
- Translates all its properties into renderer-agnostic USD attributes.


## Installation
- Copy folder [husdplugins](husdplugins) into "C:/Users/$USERNAME/Documents/houdini20.5/" or whatever Houdini version you are using.\


## Usage
- restart Houdini, then in a Solaris scene, drop a 'Scene Import (Lights)' LOP node.\
- It will now import all Obj Arnold Lights into the Solaris scene.


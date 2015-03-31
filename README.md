# ![http://i750.photobucket.com/albums/xx149/perezmu/duplicatesmanager-2.png](http://i750.photobucket.com/albums/xx149/perezmu/duplicatesmanager-2.png) `                     `  DUPLICATES MANAGER FOR [COMICRACK](http://comicrack.cyolito.com) #

---

## NEW VERSION 0.9 ##

### Updated  with NEW RULES, see the [rules wiki](http://code.google.com/p/comicrack-duplicates-manager/wiki/RulesFileSyntax) ###

```
v0.9 -> 

   Added:    - New rules: 
                    - scan keep/remove
             - New toolbar icon
             - Fix for typos and rare crash
```
[Complete CHANGELOG](http://code.google.com/p/comicrack-duplicates-manager/wiki/Changelog)

---


### IMPORTANT NOTICE (UPDATED AS OF VERSION 0.5) ###
Since I do not want to mess with your files & library before we are sure this thing works right,
|**the script out of the box will not move or remove any comic, just log what it would do in the logfile. To enable the actual processing of files you need to  add the values  true for the variables `MOVEFILES` and `REMOVEFROMLIB`** in the **dmrules.dat** file. See the [Configuration Options](http://code.google.com/p/comicrack-duplicates-manager/wiki/UserConfiguration?ts=1297328384&updated=UserConfiguration) Wiki page for details.|
|:------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|


---


This script is an addon to comicrack that identifies duplicated ecomics and follows a set of user defined rules to remove unwanted dupes. It is designed with the 0-days in mind, but should prove useful in other scenarios.

The script reads a file (**dmrules.dat**) from the directory where it is installed, that contains, both user options, and a series of rules to manage the duplicate files. Duplicate files that meet the criteria expressed in the rules are **moved** to a dump directory (not deleted) and removed from the comicrack library (default dump directory is `C:\_dupes_`). This directory also holds a logfile (**logfile.log**) that details the process followed on your comics

So, the first thing you want to do is read the rules (see wiki) and edit your custom **dmrules.dat** file.

Wiki Index:

  * [Overview](http://code.google.com/p/comicrack-duplicates-manager/wiki/Overview?ts=1297338327&updated=Overview): You need to read this first!!!!
  * Rules are explained in detail in the Wiki: [Rules Syntax](http://code.google.com/p/comicrack-duplicates-manager/wiki/RulesFileSyntax).
  * Then you can go to the [Tips and Examples](http://code.google.com/p/comicrack-duplicates-manager/wiki/TipsAndTricks?ts=1297265175&updated=TipsAndTricks) page.
  * User defined variables are described in the [Configuration Options](http://code.google.com/p/comicrack-duplicates-manager/wiki/UserConfiguration?ts=1297328384&updated=UserConfiguration)  page.
  * Credits for people who have (not necessary knowingly) contributed to this project in [the credits](http://code.google.com/p/comicrack-duplicates-manager/wiki/FellowCredits) page
  * Screenshot and example files at [this wiki page](http://code.google.com/p/comicrack-duplicates-manager/wiki/ScreenshotExample)
  * Changelog is in [this other page](http://code.google.com/p/comicrack-duplicates-manager/wiki/Changelog)

Discussion is provided in the [comicrack support forum](http://comicrack.cyolito.com/forum/13-scripts/12076-duplicates-manager#12076)


---


Cheers!!!!! ![http://comicrack.cyolito.com/media/kunena/avatars/resized/size72/users/avatar195.jpg](http://comicrack.cyolito.com/media/kunena/avatars/resized/size72/users/avatar195.jpg)
#PyOne - Help
##Kumaresan - Nov 18 2017

### Index
##### [About PyOne]
##### First time runner steps
##### Important Points

##### About PyOne

The PyOne - Kumar's experimental project for rapid automation of frequent windows activities. Kind of swiss knife for developers. Got some ideas for it? Share with me kaymatrixgmail.com.

##### First time runner setup

- delete 'config.ini' file if present
- make sure no 'argument' attach to exe
- start the app and close the app
- will create 'userScripts' and config.ini
- setup 4 digit secret code and attach to argument of this exe
- start the app again
- open new file and run below command print(dev.encrypt('4132'))
- get the value displayed in output 
- paste that value in 'config.ini' file for below mentioned setting decryptValue=9687
- make sure to add double quote for your value
eg: 
decryptValue=";67|8"
- save the config

##### Important Points

- Config files: All path/url type configs should use special care while using special characters in it. ``(eg. \ should be \\)`` 
- ``print(dev.encrypt('4132'))`` execute this and get the code and add it to config file


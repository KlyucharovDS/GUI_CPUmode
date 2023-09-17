# Atributes:
if application run without any arguments then
it will start in GUI mode.

## optional:
* -m regime_name, --set_mode regime_name:
  * performance
  * ondemand
  * conservative
  * powersave
  * userspace
* -f,--set_freq NUMBER set current frequency in KHz
* -p, --period SEC [from 0.1 to 3600]. 
If this argument is used, then the application
checks the current state of the processor each
__period_seconds and sets their parameters if they have changed.
You may exit from application then will press 'q' key.
* --fmax NUMBER max frequency in KHz 
* --fmin NUMBER min frequency in KHz
* --get_freq  -available frequency of target CPU
* --get_mode  -available regime of target CPU
* --info      -print full information about CPUs

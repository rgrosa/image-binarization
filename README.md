# image-binarization
Script to binarize images 

## Flags:

-f file list you want to proccess

-c apply close operation (dilation + erosion)

## Execution example:

binarize example image:
```
python process.py -f example/9.png
```

applying close operation:

```
python process.py -f example/9.png -c true
```

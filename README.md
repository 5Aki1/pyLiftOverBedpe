# pyLiftOverBedpe

A simple python3 wrapper for the liftOver tool that allows users to liftOver BEDPE files from one genome build to another.



Requires the pyliftover package and a liftOver chain file.

### Usage

```
python pyLiftOverBedpe.py -i input.bedpe -o output.bedpe -c hg19ToHg38.over.chain
````

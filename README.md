# Coderdojo Certificate Generator 

## How to run
Script.py consists of three functions
- readFile()
- createCerts()
- sendEmails()
Recommended to comment out sendEmails() and generate certificates first to ensure they are created properly, then run again with createCerts() commented out to just send the emails

## How it works
- Uses latex to read in a pdf template of the certificate then a shell script to find and replace the name as well as compile.
    - The python script manages the certificates and ninjas using the array index they were read in on, I tried naming the certificate.pdf the ninja's name but that kinda messed everything up because some of names are tricky.
    - Using the index is easier for validating anyway since you can see any numbers that arent there
- Emails parent certificate with attached message

## Requirements 
- Python3.6
- latex installed
- Calibri font installed - this is a bit of a pain for linux systems so if you want change it in the Template.tex
- Don't change any filenames btw i hardcoded all of them
    - Generator.sh - for compiling the latex and doing the name replacement
    - CertificateTemplate.pdf
    - Template.tex



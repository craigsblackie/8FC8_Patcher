# 8FC8 BIOS Patcher

## What this does
This script patches a Dell BIOS file to put it into **manufacturing mode**.

In most cases this:
- Removes the BIOS password  
- Keeps existing settings intact  
- Still allows systems with BitLocker to boot  
- Enables changing the Service Tag  

## Usage
```bash
python 8FC8_patcher.py <bios.bin>
```
## Output

If successful, a patched file will be created:

```bash
patched_<original_filename>
```
## Warning

Flashing a modified BIOS can brick a device. Use at your own risk.

#!/usr/bin/env bash
# Rebuild corpus/tds. Vendors that block automated fetches (ST, Microchip, TME,
# LCSC) are absent by necessity. Files that 403 or return HTML are skipped.
set -u
cd "$(dirname "$0")/../corpus/tds" 2>/dev/null || { mkdir -p ../corpus/tds && cd ../corpus/tds; }
dl(){ [ -f "$2" ] && return 0
      curl -sL -A "Mozilla/5.0 (X11; Linux x86_64)" -o "$2" "$1" 2>/dev/null
      s=$(stat -c%s "$2" 2>/dev/null || echo 0)
      if [ "$s" -lt 15000 ] || ! head -c 5 "$2" | grep -q '%PDF'; then rm -f "$2"; echo "skip $2"; fi; }
for p in BC817_SER PMEG3020EP PBSS4350X 74LVC1G14 PESD5V0X1BL 74HC_HCT595 1N4148_1N4448; do
  dl "https://assets.nexperia.com/documents/data-sheet/${p}.pdf" "nexperia_${p}.pdf"; done
for t in tlv9061 ina226 tca9548a tps61023 lmv321 sn74lvc1g08 ucc27517 tps54331; do
  dl "https://www.ti.com/lit/ds/symlink/${t}.pdf" "ti_${t}.pdf"; done
dl "https://www.infineon.com/dgdl/Infineon-IRLZ44N-DataSheet-v01_01-EN.pdf?fileId=5546d462533600a4015355d5f0a91480" irlz44n_infineon.pdf
dl "https://www.bosch-sensortec.com/media/boschsensortec/downloads/datasheets/bst-bme280-ds002.pdf" bme280_bosch.pdf
dl "https://www.vishay.com/docs/83725/4n25.pdf" 4n25_vishay.pdf
dl "https://www.we-online.com/components/products/datasheet/150080BS75000.pdf" led_wurth.pdf
dl "https://www.we-online.com/components/products/datasheet/7447709100.pdf" wurth_7447709100.pdf
dl "https://www.diodes.com/assets/Datasheets/AP2114.pdf" diodes_ap2114.pdf
dl "https://www.diodes.com/assets/Datasheets/DMN2075U.pdf" diodes_dmn2075u.pdf
echo "corpus: $(ls *.pdf | wc -l) files"

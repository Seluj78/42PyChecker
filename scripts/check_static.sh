#@IgnoreInspection BashAddShebang
#    Copyright (C) 2018 Jules Lasne <jules.lasne@gmail.com>
#    See full notice in `LICENSE'
TOTAL=$(find "$1" -type f -name "*.c")
OLDIFS=${IFS}
IFS=$'\n'
if [ "${TOTAL}" == "" ]
then
  printf "Files not found"
else
  for i in $(find "$1" -type f -name "*.c")
    do
        FILEN=$(basename "$i")
        awk -v FILEN="${FILEN}" -v FILEN2="${FILEN}" 'BEGIN \
        { \
        OFS = ""
        sub(/\.c/, "", FILEN)
        } \
        $0 ~ /^[a-z_]+[	 ]+\**[a-z_]*\(.*/ \
        { \
        gsub (/^[a-z_]*[	 ]+\**/, "")
        gsub (/ *\(.*$/, "")
        if ($1 != FILEN) \
        { \
            print FILEN2, " (line ", NR, ") : ", $0, "() should be declared as static" \
          } \
        }' "$i"
    done
fi
IFS=${OLDIFS}
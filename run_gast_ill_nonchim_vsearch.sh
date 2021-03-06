#!/bin/bash

title="Illumina gast. Run on grendel."
prompt="Please select a file name pattern:"
#options=("*.unique.nonchimeric.fa" "*.unique.nonchimeric.fa for Fungi (ITS1)" "*-PERFECT_reads.fa.unique" "*-PERFECT_reads.fa.unique for Archaeae" "*MAX-MISMATCH-3.unique")
options=("*.unique.nonchimeric.fa v4v5" "*.unique.nonchimeric.fa Euk v4" "*.unique.nonchimeric.fa Fungi ITS1" "*-PERFECT_reads.fa.unique" "*-PERFECT_reads.fa.unique for Archaeae" "*MAX-MISMATCH-3.unique")

echo "$title"
PS3="$prompt "
ITS_OPTION=""
select opt in "${options[@]}"; do 

    case "$REPLY" in

#    "*.unique.nonchimeric.fa" )   NAME_PAT=$REPLY; UDB_NAME=refv4v5; echo "You picked option $REPLY"; break;;
    "*.unique.nonchimeric.fa v4v5" )   NAME_PAT="*.unique.nonchimeric.fa"; UDB_NAME=refv4v5; echo "You picked option $REPLY"; break;;
    "*.unique.nonchimeric.fa Euk v4" )   NAME_PAT="*.unique.nonchimeric.fa"; UDB_NAME=refv4e; echo "You picked option $REPLY"; break;;
    "*.unique.nonchimeric.fa Fungi ITS1" )   NAME_PAT="*.unique.nonchimeric.fa"; UDB_NAME=refits1; ITS_OPTION=" -full "; echo "You picked option $REPLY"; break;;
    "*-PERFECT_reads.fa.unique" ) NAME_PAT=$REPLY; UDB_NAME=refv6;   echo "You picked option $REPLY"; break;;
    "*-PERFECT_reads.fa.unique for Archaeae" ) NAME_PAT="*-PERFECT_reads.fa.unique"; UDB_NAME=refv6a;   echo "You picked option $REPLY"; break;;
    "*MAX-MISMATCH-3.unique" ) NAME_PAT=$REPLY; UDB_NAME=refv6long;   echo "You picked option $REPLY"; break;;

    1 ) NAME_PAT="*.unique.nonchimeric.fa";        UDB_NAME=refv4v5; echo "You picked option $REPLY"; break;;
    2 ) NAME_PAT="*.unique.nonchimeric.fa";        UDB_NAME=refv4e; echo "You picked option $REPLY"; break;;
    3 ) NAME_PAT="*.unique.nonchimeric.fa";        UDB_NAME=refits1; ITS_OPTION=" -full "; echo "You picked option $REPLY"; break;;
    4 ) NAME_PAT=${options[3]};                    UDB_NAME=refv6; echo "You picked option $REPLY"; break;;
    5 ) NAME_PAT="*-PERFECT_reads.fa.unique";      UDB_NAME=refv6a; echo "You picked option $REPLY"; break;;
    6 ) NAME_PAT=${options[5]};                    UDB_NAME=refv6long; echo "You picked option $REPLY"; break;;

    # $(( ${#options[@]}+1 )) ) echo "Goodbye!"; break;;
    *) echo "Invalid option. Try another one."; continue;;

    esac

done

echo "UDB_NAME = $UDB_NAME.udb"
echo "ITS_OPTION = $ITS_OPTION"
echo "NAME_PAT = $NAME_PAT"
echo "Files number: = `echo $NAME_PAT | wc -w`"

for file in $NAME_PAT
do
  echo "============="
  #echo $file
  echo "clusterize /workspace/ashipunova/test_vsearch/gast_ill_vsearch.pl -saveuc -nodup $ITS_OPTION -in $file -db /xraid2-2/g454/blastdbs/gast_distributions/$UDB_NAME.fa -rtax /xraid2-2/g454/blastdbs/gast_distributions/$UDB_NAME.tax -out $file.gast"
  clusterize /workspace/ashipunova/test_vsearch/gast_ill_vsearch.pl -saveuc -nodup $ITS_OPTION -in $file -db /xraid2-2/g454/blastdbs/gast_distributions/$UDB_NAME.fa -rtax /xraid2-2/g454/blastdbs/gast_distributions/$UDB_NAME.tax -out $file.gast

done

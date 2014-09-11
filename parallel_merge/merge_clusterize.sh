#!/bin/bash

title="Merging files with merge-illumina-pairs in parallel, run on a cluster"
prompt="Please select a dna region:"
options=("v4v5" "ITS1")

echo "$title"
PS3="$prompt "
select opt in "${options[@]}"; do 

    case "$REPLY" in

    "v4v5" ) DNA_REGION=$REPLY;        ADD_ARG="";                          echo "You picked option 'v4v5'"; break;;
    "ITS1" ) DNA_REGION=$REPLY;        ADD_ARG=" --marker-gene-stringent "; echo "You picked option 'ITS1'"; break;;
    1 )      DNA_REGION=${options[0]}; ADD_ARG="";                          echo "You picked option 'v4v5'"; break;;
    2 )      DNA_REGION=${options[1]}; ADD_ARG=" --marker-gene-stringent "; echo "You picked option 'ITS1'"; break;;

    *) echo "Invalid option. Try another one."; continue;;

    esac
done

ini_count=`ls *.ini | wc -l`
echo "Number of ini files: $ini_count" 
ini_list=(`ls *.ini`)
#echo $ini_list

username=`whoami`
echo "When each job is done an email will be sent to $username@mbl.edu"

script_name=$(basename "$0")
#echo $script_name
#echo "==="

cat << InputComesFromHERE > $script_name.sge_script.sh
#!/bin/bash
 
#$ -cwd
#$ -S /bin/bash
#$ -N $script_name
# Giving the name of the output log file
#$ -o $script_name.sge_script.sh.log
# Combining output/error messages into one file
#$ -j y
# Send mail to these users
#$ -M $username@mbl.edu
# Send mail at job end; -m eas sends on end, abort, suspend.
#$ -m eas
#$ -t 1-$ini_count
# Now the script will iterate $ini_count times.

  ini_list1=(${ini_list[@]})
  echo $ini_list1
  i=\$(expr \$SGE_TASK_ID - 1)
  #echo \$i
  source ~/.bashrc
  module load bioware

  echo "merge-illumina-pairs --enforce-Q30-check $ADD_ARG \${ini_list1[\$i]}"
  merge-illumina-pairs --enforce-Q30-check $ADD_ARG \${ini_list1[\$i]}


InputComesFromHERE

chmod u+x $script_name.sge_script.sh

#Now run ./merge_clusterize.sh; qsub merge_clusterize.sh.sge_script.sh

import os
# before testing, 
# export USER=user
# export PASS=pass
os.system("python3 cf.py -u $USER -p $PASS -f test_sample.py -i 1073 -x A") 
os.system("python3 cf.py -u $USER -p $PASS -f test_sample.py -m g -i 101964 -x A") 
os.system("python3 cf.py -u $USER -p $PASS -f test_sample.py -m c -i 1073 -x B") 

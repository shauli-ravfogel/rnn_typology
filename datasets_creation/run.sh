#!/bin/bash

dataset="dev"
agreement_marker="na-d"
add_cases=0
order="vos"
nsubj=1
dobj=1
iobj=1
mark_verb=0
filter_no_attractor=0
filter_attractor=0
filter_obj=0
filter_no_obj=0
filter_obj_att=0
filter_no_obj_att=0

python main.py --dataset $dataset --agreement-marker $agreement_marker --add-cases $add_cases --order $order --nsubj $nsubj --dobj $dobj --iobj $iobj --mark-verb $mark_verb --filter-no-att $filter_no_attractor --filter-att $filter_attractor --filter-obj $filter_obj --filter-no-obj $filter_no_obj --filter-obj-att $filter_obj_att --filter-no-obj-att $filter_no_obj_att

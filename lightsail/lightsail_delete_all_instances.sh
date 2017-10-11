#!/bin/bash

instance_names=$(aws lightsail get-instances | jq -r '.instances[].name')

for instance_name in $instance_names
do
    echo $instance_name
    aws lightsail delete-instance --instance-name $instance_name
done

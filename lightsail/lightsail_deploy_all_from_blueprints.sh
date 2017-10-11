#!/bin/bash

NAME_PREFIX="georges"

blueprints=$(aws lightsail get-blueprints)
blueprint_ids=$(echo $blueprints |jq '.blueprints[].blueprintId' --raw-output)
blueprint_names=$(echo $blueprints |jq '.blueprints[].name' --raw-output)

for blueprint_id in $blueprint_ids
do
    blueprint_name=$(echo $blueprints | jq -r --arg BLUEPRINT_ID "$blueprint_id" '.blueprints[] | select(.blueprintId==$BLUEPRINT_ID) | .name')
    my_name=$(echo "$NAME_PREFIX-$blueprint_name" | tr ' ' '-')
    echo "creating new instance:"
    echo "  name: $my_name"
    echo "  blueprint: $blueprint_id"
    
    status=$(aws lightsail create-instances \
	--instance-names "$my_name" \
	--availability-zone ap-southeast-2a \
	--blueprint-id $blueprint_id \
	--bundle-id nano_1_2 |  jq -r '.operations[] .status')

    echo "  status: $status"
    echo ""
done

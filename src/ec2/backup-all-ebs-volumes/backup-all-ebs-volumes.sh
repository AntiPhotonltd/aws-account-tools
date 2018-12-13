#!/usr/bin/env bash

timestamp=$(date -u "+%Y-%m-%dT%H:%M:%S")

function backup {
    local volume=$1
    local name=$2
    local description=$3
    local snapshot, json

    snapshot=$(aws --region "${REGION}" ec2 create-snapshot --volume-id "${volume}" --description "${description}" | jq '.SnapshotId' | tr -d '"')

    json=$(cat <<-EOF
    {
        "Resources": [
            "${snapshot}"
        ],
        "Tags": [
            {
                "Key": "Name",
                "Value": "${name}"
            },
            {
                "Key": "Description",
                "Value": "${description}"
            },
            {
                "Key": "CreatedBy",
                "Value": "AutomatedBackup"
            }
        ]
    }
EOF
) #the EOF and closing parenthesis can't be indented!

    aws --region "${REGION}" ec2 create-tags --cli-input-json "${json}"
}

aws ec2 describe-volumes --region "${REGION}" --query 'Volumes[*].[Attachments[*].[VolumeId]]' --output text | while read -r volume
do
        backup "${volume}" "volume-${timestamp}" "${volume} backup taken at ${timestamp}"
done


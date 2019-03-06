#!/usr/bin/env bash

REGION='eu-west-1'
NAME_TAG='WolfTest'

#
# Where is the instance located?
#
#INSTANCE_AZ=$(curl http://169.254.169.254/latest/meta-data/placement/availability-zone)
INSTANCE_AZ='eu-west-1c'

#
# First we find the EBS volume.
#
ID_AZ=$(aws ec2 --region "${REGION}" describe-volumes --filters Name=tag-key,Values="Name" Name=tag-value,Values="${NAME_TAG}" --query 'Volumes[*].{ID:VolumeId, AZ:AvailabilityZone}' --output text)

if [[ -z "${ID_AZ}" ]]; then
    echo "Failed to find the volume - aborting"
    exit 1
fi

#
# Extract the 2 parts
#
VOLUME_AZ=$(echo "${ID_AZ}" | cut -f1)
VOLUME_ID=$(echo "${ID_AZ}" | cut -f2)

if [[ "${INSTANCE_AZ}" == "${VOLUME_AZ}" ]]; then
    echo "Instance and volume are n the same AZ - aborting"
    exit 1
fi

#
# Create a snapshot and wait till it is complete
#
SNAPSHOT_ID=$(aws ec2 create-snapshot --volume-id "${VOLUME_ID}" --description "Migration snapshot for ${VOLUME_ID}" --query 'SnapshotId' --output text)

#
# aws ec2 wait 'can' timeout hence the loop but in most cases that shouldn't happen.
#
while [ "${exit_status}" != "0" ]
do
    SNAPSHOT_STATE="$(aws ec2 describe-snapshots --filters Name=snapshot-id,Values="${SNAPSHOT_ID}" --query 'Snapshots[0].State')"
    SNAPSHOT_PROGRESS="$(aws ec2 describe-snapshots --filters Name=snapshot-id,Values="${SNAPSHOT_ID}" --query 'Snapshots[0].Progress')"
    echo "### Snapshot id ${SNAPSHOT_ID} creation: state is ${SNAPSHOT_STATE}, ${SNAPSHOT_PROGRESS}%..."

    aws ec2 wait snapshot-completed --snapshot-ids "${SNAPSHOT_ID}"
    exit_status="$?"
done

#
# Create the new volume and wait till it is ready
#
NEW_VOLUME_ID=$(aws ec2 create-volume --region "${REGION}" --availability-zone "${INSTANCE_AZ}" --snapshot-id "${SNAPSHOT_ID}" --volume-type gp2 --tag-specifications "ResourceType=volume,Tags=[{Key=Name,Value=${NAME_TAG}2}]" --query 'VolumeId' --output text)

#
# aws ec2 wait 'can' timeout hence the loop but in most cases that shouldn't happen.
#
while [ "${exit_status}" != "0" ]
do
    VOLUME_STATE=$(aws ec2 describe-volumes --volume-ids "${NEW_VOLUME_ID}" --query 'Volumes[*].State' --output text)
    echo "### Volume id ${NEW_VOLUME_ID} creation: state is ${VOLUME_STATE}, ${SNAPSHOT_PROGRESS}%..."

    aws ec2 wait volume-available --volume-ids "${NEW_VOLUME_ID}"
    exit_status="$?"
done


#
# Now we clean up
#

aws ec2 delete-snapshot --snapshot-id "${SNAPSHOT_ID}"

aws ec2 delete-volume --volume-id "${VOLUME_ID}"

#
# End of script
#

#!/bin/zsh
repo_root=$(git rev-parse --show-toplevel)
cd $repo_root

aws_profile="DataTeam"
image_name="amazon/aws-stepfunctions-local"
image_tag="latest"
container_name="stepfunctions-local"
port=8083
local_mock_config="./step_functions/local_testing/mock_config.json"
container_mock_config="/home/StepFunctionsLocal/MockConfigFile.json"
endpoint="http://localhost:$port"
test_case="POCTest"

if [ -z $(docker images -q $image_name:$image_tag) ]; then
    echo "Pulling image $image_name:$image_tag"
    docker pull $image_name:$image_tag
fi

if [ $(docker ps -a -f name=$container_name --format "{{.Names}}") ]
then
    echo "Deleting existing container $container_name"
    docker stop $container_name
    docker rm $container_name
fi

echo "Starting container $container_name"
docker run -d --name $container_name -p $port:$port \
	--mount type=bind,readonly,source=$local_mock_config,destination=$container_mock_config \
    -e SFN_MOCK_CONFIG=$container_mock_config \
    $image_name:$image_tag

echo "Creating State Machine"
state_machine_detail=$(
    aws --profile $aws_profile stepfunctions create-state-machine \
        --endpoint $endpoint \
        --definition file://step_functions/local_testing/state_machine_definition.json \
        --name "TestStateMachine" \
        --role-arn "arn:aws:iam::012345678901:role/DummyRole"
)
exit 0

echo $state_machine_detail
echo "Getting State Machine ARN"
state_machine_arn=$(
    echo $state_machine_detail | \
    python3 -c "import sys, json; print(json.load(sys.stdin)['stateMachineArn'])"
)

python3 step_functions/execute_state_machine_local.py \
    --aws-profile $aws_profile \
    --endpoint-url $endpoint\
    --state-machine-arn $state_machine_arn \
    --test-case $test_case \

echo "Stopping container $container_name"
docker stop $container_name
docker rm $container_name

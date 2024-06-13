#!/bin/zsh
aws_profile="DataTeam"
image_name="amazon/aws-stepfunctions-local"
image_tag="latest"
container_name="stepfunctions-local"
port=8083
mock_config_path="/home/StepFunctionsLocal/MockConfigFile.json"

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
	--mount type=bind,readonly,source=./mock_config.json,destination=$mock_config_path \
    -e SFN_MOCK_CONFIG=$mock_config_path \
    $image_name:$image_tag

echo "Creating State Machine"
state_machine_detail=$(
    aws --profile $aws_profile stepfunctions create-state-machine \
        --endpoint "http://localhost:$port" \
        --definition file://state_machine_definition.json \
        --name "TestStateMachine" \
        --role-arn "arn:aws:iam::012345678901:role/DummyRole"
)

echo $state_machine_detail
echo "Getting State Machine ARN"
state_machine_arn=$(
    echo $state_machine_detail | \
    python3 -c "import sys, json; print(json.load(sys.stdin)['stateMachineArn'])"
)

echo "Starting Execution"
execution_detail=$(
    aws --profile $aws_profile stepfunctions start-execution \
        --endpoint "http://localhost:$port" \
        --state-machine-arn $state_machine_arn#POCTest \
        --name "test"
)

echo "Getting Execution ARN"
execution_arn=$(
    echo $execution_detail | \
    python3 -c "import sys, json; print(json.load(sys.stdin)['executionArn'])"
)

echo "aws --profile DataTeam stepfunctions describe-execution --endpoint http://localhost:$port --execution-arn $execution_arn"

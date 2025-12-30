import urllib.request
import urllib.parse
import os
import json
from typing import Any, Optional

AwsSessionToken = os.getenv("AWS_SESSION_TOKEN", "")


def is_aws_session_token_available() -> bool:
    return bool(AwsSessionToken)


def _get_aws_ssm_parameter(parameter_name: str, aws_session_token) -> Any:
    print(f"Fetching SSM parameter: {parameter_name}")
    url_encoded_name = urllib.parse.quote_plus(parameter_name, encoding="utf-8")
    request = urllib.request.Request(
        f"http://localhost:2773/systemsmanager/parameters/get?name={url_encoded_name}&withDecryption=true"
    )
    request.add_header("X-Aws-Parameters-Secrets-Token", aws_session_token)
    json_value = urllib.request.urlopen(request).read()

    return json.loads(json_value)


def get_aws_ssm_parameter_value(
    parameter_name: str, aws_session_token: str = AwsSessionToken
) -> Optional[str]:
    parameter = _get_aws_ssm_parameter(
        parameter_name=parameter_name,
        aws_session_token=aws_session_token,
    ).get("Parameter", {})

    if "Value" not in parameter:
        raise KeyError(f"Parameter {parameter_name} does not have a Value field")

    return parameter.get("Value")

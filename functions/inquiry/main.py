import boto3
import json
import logging
import os

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def handler(event, context):
    params = json.loads(event["body"])
    logger.info(params)

    name = params["name"] or "-"
    mail = params["mail"] or "-"
    corporation = params["corporation"] or "-"
    division = params["division"] or "-"
    types = params["types"] or []
    comment = params["comment"] or "-"

    body = []
    body.append("お問い合わせがありました")
    body.append("")
    body.append("名前: " + name)
    body.append("メール: " + mail)
    body.append("会社: " + corporation)
    body.append("部署: " + division)
    body.append("項目: " + "、".join(types) or "-")
    body.append("内容: " + comment)

    client = boto3.client("ses", region_name=os.environ["REGION"])
    client.send_email(
        Source=os.environ["FROM_MAIL"],
        Destination={
            "ToAddresses": ["general-all@befool.co.jp"],
        },
        Message={
            "Subject": {
                "Data": "お問い合わせ",
            },
            "Body": {
                "Text": {
                    "Data": "\n".join(body),
                },
            },
        }
    )

    return {
        "statusCode": 200,
        "body": json.dumps({"status": "ok"}),
    }

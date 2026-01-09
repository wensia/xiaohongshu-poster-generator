#!/usr/bin/env python3
"""Update Feishu Bitable records with uploaded file tokens."""

import requests

# Feishu credentials
APP_ID = "cli_a9a7190fef38dbb5"
APP_SECRET = "CyANTKyK1HhZ569m9vasodAGqsjKwh1u"
APP_TOKEN = "Qt6Qbzzy6aWBgassGQhcUU5vngc"
TABLE_ID = "tblyDtUqcfFMaDfO"

# File tokens from previous upload
RECORDS_DATA = {
    "射手遇到射手": {
        "record_id": "recv7JnzUE6bIV",
        "file_tokens": [
            "ORJTbJzRCotomuxtsuIc0DqVnbb",
            "NsRsbkohRo4sxXxWNV8cVPZznbh",
            "FFp9byqz5ojKvPxBa3HcBY56nTc",
            "F54Obm4KKoTvXxxs2oOcaGhKn4b",
            "R0HVbkXyCoa4YyxLW6ecDRwenXc",
            "LYaqbkAwZoAJJMxty86ceVKqnbb",
            "NWBybwfaEoOipJxWFoucF7KonIc",
        ]
    },
    "射手遇到摩羯": {
        "record_id": "recv7JnAjeTj6s",
        "file_tokens": [
            "B419b3BtKoSgpHxLvg0c3t96nhe",
            "HIqJbYiRIoAGOWxjOe6c3YSOnae",
            "VYiFbkwxvoPxbWx8JRMcvV0Qn3b",
            "NJbZbGIXto88PmxNcEGcjc1vnWh",
            "KvsRb6PztopgwXxKdvrcU1sGnUg",
            "BlcebTtU1o6CavxTbpZcsmzhnud",
            "L0fMbzf9zozQsqxVb7YcSI8CnFe",
        ]
    },
    "射手遇到水瓶": {
        "record_id": "recv7JnAJaLx8y",
        "file_tokens": [
            "PuU2bKTjaohe5yxMRaxcxZ2Cntc",
            "KKxPbobbnor7E8xexFqc1wh0ncg",
            "AX1ebeqyLoDJoDxrWVfc06FtnCh",
            "AYeebRYAdoAj2TxDYW6cmOxJneb",
            "TLf5bixlWoTSwPxIdmDc8dgInMb",
            "NYz0bIjcUoe6o6xStyVcmzR4nOc",
            "FgYlbWO6YoAg2ixRDkscBXMKnPe",
        ]
    },
    "射手遇到双鱼": {
        "record_id": "recv7JnB7dSbcX",
        "file_tokens": [
            "Akgub6O8aoq8uIxiI2VcKkiknge",
            "WFTYbDppzoKjpFxpY3ycDZrCn6b",
            "XeJCbsVjdoSwPmxEpnpcvGKHnXb",
            "N877b81smowjivxcf1KcRKfenvb",
            "QbdFbiy8OoEytKxfk4Acqr0gnLg",
            "RpxubhgJPoke5Tx5C86ca0xcnQd",
            "FA6xbvAayoIanqxhnZIczrdmn8b",
        ]
    },
}


def get_tenant_access_token():
    """Get tenant access token from Feishu."""
    url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
    resp = requests.post(url, json={"app_id": APP_ID, "app_secret": APP_SECRET})
    data = resp.json()
    if data.get("code") != 0:
        raise Exception(f"Failed to get token: {data}")
    return data["tenant_access_token"]


def update_record(token, record_id, file_tokens):
    """Update Feishu Bitable record with file attachments."""
    url = f"https://open.feishu.cn/open-apis/bitable/v1/apps/{APP_TOKEN}/tables/{TABLE_ID}/records/{record_id}"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }

    # Prepare attachment field with file tokens
    attachments = [{"file_token": ft} for ft in file_tokens]

    data = {
        "fields": {
            "生成图片": attachments,
            "已生成": True,  # This is a checkbox field
        }
    }

    resp = requests.put(url, headers=headers, json=data)
    result = resp.json()
    if result.get("code") != 0:
        raise Exception(f"Update record failed: {result}")
    return result


def main():
    print("Getting tenant access token...")
    token = get_tenant_access_token()
    print(f"Token obtained: {token[:20]}...")

    for title, data in RECORDS_DATA.items():
        print(f"\n=== Updating: {title} ===")
        record_id = data["record_id"]
        file_tokens = data["file_tokens"]

        print(f"  Record ID: {record_id}")
        print(f"  Files: {len(file_tokens)}")

        try:
            update_record(token, record_id, file_tokens)
            print(f"  SUCCESS: Record updated!")
        except Exception as e:
            print(f"  ERROR: {e}")

    print("\n=== Done ===")


if __name__ == "__main__":
    main()

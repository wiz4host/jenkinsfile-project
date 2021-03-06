import json

dictionary = {
  "sweaglekeyname": {
    "pipeline-params": {
      "GIT_REPO": "<gitrepo>",
      "TFEADDRESS": "<tfe_addr>",
      "WORKSPACE_ID": "<wid>",
      "BEARER_TOKEN": "<bearer_token>",
      "ORGANIZATION_NAME": "<org_name>"
    },
    "tfe-vars": {
      "ARM_CLIENT_ID": "ACI",
      "ARM_CLIENT_SECRET": "ACS",
      "ARM_SUBSCRIPTION_ID": "ASI",
      "ARM_TENANT_ID": "ATI"
    }
  }
}

jd = json.dumps(dictionary, indent=4)

print(jd,  file=open('sweagle.json', 'wt'))

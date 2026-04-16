#!/bin/bash
# stgaws 
# stgaws e2e-stage-AGENTV2-std
WO_API_ENDPOINT=https://api.us-south.watson-orchestrate.cloud.ibm.com/instances/12c90aa8-f739-4139-b8ca-804fba505f15

WO_JWT=`curl -X POST "https://iam.platform.saas.ibm.com/siusermgr/api/1.0/apikeys/token" -H "Content-Type: application/json" -d '{ "apikey":"nBVbljAN2t6ZpQ4Qnv_9RsyMe1ezl4oayxtdS6N_MKqV"}' | jq .token | tr -d '"'`

# agent GailMarie_SIP...
AGENT_ID=c3792ad4-2a4e-440f-a448-5f532bc9cfca


#update settings
curl --request PATCH \
  --url ${WO_API_ENDPOINT}/v1/orchestrate/agents/${AGENT_ID} \
  --header 'content-type: application/json' \
  --header "Authorization: Bearer ${WO_JWT}" \
  --data '{ "additional_properties": { "realtime_agent_settings": { "enabled": true } } }' --output ./aws_patch.out


#confirm settings
curl --request GET \
  --url ${WO_API_ENDPOINT}/v1/orchestrate/agents/${AGENT_ID} \
  --header 'content-type: application/json' \
  --header "Authorization: Bearer ${WO_JWT}" | jq '.additional_properties'

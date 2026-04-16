
# cloud staging
# instance name = gdburati-wxo-stg-std-AgentV2-20250422
WO_API_ENDPOINT=https://api.us-south.watson-orchestrate.test.cloud.ibm.com/instances/556e7294-8858-4169-8070-bfd94957d330

WO_JWT=`curl -X POST https://iam.test.cloud.ibm.com/identity/token --header 'Content-Type: application/x-www-form-urlencoded' --header 'Accept: application/json' --data-urlencode 'grant_type=urn:ibm:params:oauth:grant-type:apikey' --data-urlencode 'apikey=TaFxnQ2lpOnQ1ou4RuNRAEbyba9KvJG98vJu5J9UdmFn'| jq .access_token | tr -d '"'`

# agent
AGENT_ID=4a83f55d-08e3-42f3-bc47-60af0d05c81e
AGENT_ID=b53a46ed-2419-4454-a88b-997431864df4

curl --request PATCH \
  --url ${WO_API_ENDPOINT}/v1/orchestrate/agents/${AGENT_ID} \
  --header 'content-type: application/json' \
  --header "Authorization: Bearer ${WO_JWT}" \
  --data '{"additional_properties": { "realtime_agent_settings": { "enabled": true } } }' --output ./ibmc_patch.out

curl --request GET \
  --url ${WO_API_ENDPOINT}/v1/orchestrate/agents/${AGENT_ID} \
  --header 'content-type: application/json' \
  --header "Authorization: Bearer ${WO_JWT}" \
  --data '{"additional_properties": { "realtime_agent_settings": { "enabled": true } } }' --output ./ibmc_get.json

# spam_poc


This is a POC for a bug bounty where the app uses a graphql endpoint for user managment. In this instance there is no rate limiting or target restrictions on emails that are sent for verification of email. This poses external risk for the company hosting it from abuse reports and as well a potential service degredation of the app itself, possibly even complete DoS. 

# Kottos
[![Build Status](https://travis-ci.org/rofinn/kottos.svg?branch=master)](https://travis-ci.org/rofinn/kottos)
[![codecov](https://codecov.io/gh/rofinn/kottos/branch/master/graph/badge.svg)](https://codecov.io/gh/rofinn/kottos)

A library for building distributed applications for reading and processing sensor data.

## Deploying Kottos on AWS Greengrass

Let's start by pulling down this repo and navigating to the greengrass directory:
```shell
> git clone https://github.com/rofinn/kottos
Cloning into 'kottos'...
remote: Enumerating objects: 68, done.
remote: Counting objects: 100% (68/68), done.
remote: Compressing objects: 100% (46/46), done.
remote: Total 81 (delta 21), reused 58 (delta 15), pack-reused 13
Unpacking objects: 100% (81/81), done.

### Greengrass Core Setup

> cd kottos/greengrass
```

Now let's setup our certs for the greengrass core device.
```shell
> mkdir certs

> cd certs

> export AWS_PROFILE="private:admin"  # Or whatever your aws profile is named (can ignore if you just have 1 default account profile)

> ACCOUNT_ID=$(aws sts get-caller-identity --output text --query 'Account')

> aws iot create-keys-and-certificate --certificate-pem-outfile kottos.cert.pem --public-key-outfile kottos.key.priv --private-key-outfile kottos.key.pub --region us-east-1
{
    "certificateArn": "arn:aws:iot:us-east-1:xxxxxxxxxxxx:cert/fozeaarve3uitwhypkncbefg7icdlol8a0ememf6sbwiabk9p1uk2ecqgv0vkqmz",
    "certificatePem": "-----BEGIN CERTIFICATE-----\n
    ...\n-----END CERTIFICATE-----\n",
    "keyPair": {
        "PublicKey": "-----BEGIN PUBLIC KEY-----\n...\n-----END PUBLIC KEY-----\n",
        "PrivateKey": "-----BEGIN RSA PRIVATE KEY-----\n...\n-----END RSA PRIVATE KEY-----\n"
    },
    "certificateId": "fozeaarve3uitwhypkncbefg7icdlol8a0ememf6sbwiabk9p1uk2ecqgv0vkqmz"
}

> wget -O certs/root.ca.pem https://www.amazontrust.com/repository/AmazonRootCA1.pem
--2019-03-06 19:55:17--  https://www.amazontrust.com/repository/AmazonRootCA1.pem
Resolving www.amazontrust.com (www.amazontrust.com)... 99.84.194.99, 99.84.194.95, 99.84.194.55, ...
Connecting to www.amazontrust.com (www.amazontrust.com)|99.84.194.99|:443... connected.
HTTP request sent, awaiting response... 200 OK
Length: 1188 (1.2K) [text/plain]
Saving to: ‘root.ca.pem’

root.ca.pem                       100%[=============================================================>]   1.16K  --.-KB/s    in 0s

2019-03-06 19:55:17 (49.3 MB/s) - ‘root.ca.pem’ saved [1188/1188]

```
Now we're going to generate our config which will tell the greengrass core daemon how to connect to our AWS account.
```shell
> cd ..

> mkdir config

> aws iot describe-endpoint --endpoint-type iot:Data-ATS --profile private:admin --region us-east-1
{
    "endpointAddress": "a3g6t1v1pdxiv8-ats.iot.us-east-1.amazonaws.com"
}

> IOT_ENDPOINT="a3g6t1v1pdxiv8-ats.iot.us-east-1.amazonaws.com"

> cat <<EOF >> config.json
{
  "coreThing" : {
    "caPath" : "root.ca.pem",
    "certPath" : "kottos.cert.pem",
    "keyPath" : "kottos.key.priv",
    "thingArn" : "arn:aws:iot:us-east-1:${ACCOUNT_ID}:thing/KottosCore",
    "iotHost" : "$IOT_ENDPOINT",
    "ggHost" : "greengrass-ats.iot.us-east-1.amazonaws.com",
    "keepAlive" : 600
  },
  "runtime" : {
    "cgroup" : {
      "useSystemd" : "yes"
    }
  },
  "managedRespawn" : false,
  "crypto" : {
    "principals" : {
      "SecretsManager" : {
        "privateKeyPath" : "file:///greengrass/certs/kottos.key.priv"
      },
      "IoTCertificate" : {
        "privateKeyPath" : "file:///greengrass/certs/kottos.key.priv",
        "certificatePath" : "file:///greengrass/certs/kottos.cert.pem"
      }
    },
    "caPath" : "file:///greengrass/certs/root.ca.pem"
  }
}
EOF
```

#### Docker Container

Pull down Amazon's greengrass docker image
```shell
> docker pull amazon/aws-iot-greengrass
Using default tag: latest
latest: Pulling from amazon/aws-iot-greengrass
f64ae36417d7: Already exists
7a9fbf62ebb0: Pull complete
831de7411b28: Pull complete
28c83296164b: Pull complete
bb4e136434c1: Pull complete
562503760045: Pull complete
Digest: sha256:51bd4b1aceb58deaec3332613c6f56b701657380a112f77928c1790210e137df
Status: Downloaded newer image for amazon/aws-iot-greengrass:latest
```

Now run the greengrass core docker image from the `greengrass` directory within the kottos.
```shell
> docker run --rm --init -it --name greengrass --entrypoint /greengrass-entrypoint.sh -v "$PWD/certs":/greengrass/certs -v "$PWD/config":/greengrass/config -p 883:883 aws-greengrass:latest
Setting up greengrass daemon
Validating hardlink/softlink protection
Waiting for up to 40s for Daemon to start

Greengrass successfully started with PID: 15
```

From this point on you can leave this docker container running and deploy code to it via the
greengrass interface.

#### Raspberry Pi

N/A

### Bundling Kottos

I WAS HERE!

### Create our CloudFormation Stack

TODO

### Deploy Kottos Lambda to Greengrass Core container

TODO

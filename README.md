# docker-selenium-lambda

This is minimum demo of headless chrome and selenium on container image on AWS Lambda

This image goes with these versions.

- Python 3.8
- serverless-chrome v1.0.0-55
  - chromium 69.0.3497.81 (stable channel) for amazonlinux:2017.03
- chromedriver 2.43
- selenium 3.141.0 (latest)

### Running the auto check

```bash
$ sls login
$ sls config credentials --provider aws --key ~ --secret ~
$ YOUR_REGION=ap-northeast-2
$ sls deploy --region $YOUR_REGION
```

아마도 별도로 aws 들어가서 trigger 추가해줘야할듯
아니면 sls로 추가 가능한거 있는지 찾아보거나..

### Contribution

I'm trying run latest Chrome but having difficulties. Please check out other branches and issues.

### Side Project

If you don't want to create functions each time for each purpose, Please check out [pythonista-chromeless](https://github.com/umihico/pythonista-chromeless)

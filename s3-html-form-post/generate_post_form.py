#!/usr/bin/env python

import sys
import os
import base64
import hmac, hashlib

from jinja2 import Template

if len(sys.argv) != 2:
    print 'usage: python ' + sys.argv[0] + ' <BUCKET_NAME>'
    sys.exit()

AWS_ACCESS_KEY = os.environ['AWS_ACCESS_KEY_ID']
AWS_SECRET_ACCESS_KEY = os.environ['AWS_SECRET_ACCESS_KEY']
BUCKET = sys.argv[1]

with open('policy_doc.json', 'r') as policy_f:
    policy = base64.b64encode(policy_f.read())
    signature = base64.b64encode(hmac.new(AWS_SECRET_ACCESS_KEY, policy, hashlib.sha1).digest())

    with open('template.index.html') as template_f:
        template = Template(template_f.read())
        tmp = template.render(
                            bucket=BUCKET,
                            signature=signature,
                            policy=policy,
                            aws_key=AWS_ACCESS_KEY)
        print tmp

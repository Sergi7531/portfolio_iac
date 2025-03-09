#!/usr/bin/env python3
import os
from dotenv import load_dotenv

import aws_cdk as cdk

from portfolio_iac.portfolio_iac_stack import PortfolioIacStack

load_dotenv()

app = cdk.App()
PortfolioIacStack(app, "PortfolioIacStack",
                  env=cdk.Environment(account=os.environ.get('CDK_DEFAULT_ACCOUNT'),
                                      region=os.environ.get('CDK_DEFAULT_REGION'))
                  )

# For more information, see https://docs.aws.amazon.com/cdk/latest/guide/environments.html
app.synth()

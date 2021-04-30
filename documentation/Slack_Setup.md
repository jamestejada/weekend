[Back to Main README](../README.md#capradio-weekend-programming-bot)

# Slack Workflow Setup

1. Open your Slack workspace and click on the Lightning Icon (found at the bottom left of the your message box). Then click on `Open Workflow Builder`. 
![Click on Lightning Icon and then click on Open Workflow Builder](../images/access_workflow_builder.png)

1. Click `Create` to create a new workflow and name your workflow. I've chosen the name `Tutorial Bot` as an example.
![Click Create to create a new workflow.](../images/create_workflow.png)

1. After naming your workflow, choose `Webhook` from the next menu. 
![Select Webhook Workflow](../images/select_webhook_workflow.png)

1. Select `Add Variable`.
![Add Variables](../images/add_variables.png)

1. Add variable names using this window. They will both be of `Data type: Text`. We will be adding two variables:
    - `show_name`
    - `missing_file_list`
![Add both variables](../images/create_keys.png)

1. After you have entered both, click `Next` and you will be brought back to the Workflow Builder screen. Click on `Add Step`.
![Add Step](../images/workflow_add_step.png)

1. Add `Send a message`.
![Send a message](../images/add_send_message.png)

1. Choose the channel which this workflow will notify, and create a notification message using the variables we have created.
![Build your message using the variables](../images/build_message.png)

1. Publish your new workflow! Be sure to copy the address for the webhook and paste it into your `.env` file. Do not share this webhook or people may be able to send strange or hilarious messages into your slack channel. 

[Back to Main README](../README.md#capradio-weekend-programming-bot)

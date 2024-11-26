# Usage

## How to generate the resume?

Before you generate the resume, you need to generate the `data.json` file. This file contains all the information about you that will be used to generate the resume.

### Step 1: Generate `data.json`

The json follow a custom schema. You can find the schema & the details about the fields in the [schema](./data-json.md) file.

### Step 2: Generate the resume

There are two ways to generate the resume:

=== ":octicons-discussion-duplicate-16: GitHub Issues"

    Once you have the `data.json` file, you can create a new issue in the [repository](https://github.com/ragarwalll/rahul-resume/issues) or use the already created issue [here](https://github.com/ragarwalll/rahul-resume/issues/8)

    Now, all you need to do is comment `/trigger` & upload the `data.json` file. The bot will take care of the rest.

=== ":octicons-git-pull-request-16: GitHub Pull Requests"

    You can also create a fork, add the `data.json` file in the root of the respository, and create a pull request. The bot will take care of the rest.

### Step 3: Download the resume

Once the bot has generated the resume, you can download the resume from the comment added by the bot in the issue or the pull request.

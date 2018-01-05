# Cli tool for clone/restore AWS RDS cluster/instances.

Tool required for human users to be able clone RDS Cluster/Instance for blue/green deployment and also restore in case of disaster recovery scenarios.

## Getting Started

First of all clone this repo and change into that directory.

```
$ git clone https://github.com/adeelahmad84/aws_rds_cli.git
$ cd aws_rds_cli
```

### Prerequisites

The installation into a virtualenv is heavily recommended.


### Installing

You would need to install the dependancies using the following command

```
$ virtualenv venv
$ . venv/bin/activate
$ pip install --editable .
```

The script will be executabe and can be called as you would using a cli environment.

### Usage

To test to see if your script has been installed properly type `rds --help` you should expect to see:

```
$ rds --help

Usage: rds [OPTIONS] COMMAND [ARGS]...

  Command Line Tool to clone and restore RDS DB instance or cluster for
  Blue-Green deployments.  Please the sub commands below.  You can also use
  the options below to get more help.

  NOTE: Please ensure the RDS instance ID is stored in your environment
  variable as DBINSTANCEID

Options:
  --help  Show this message and exit.

Commands:
  clone   Prints the ARN of the snapshot to stdout.
  deploy  Deploy new DB from snapshot and print ARN to...
```

If you run the help switch on each command you see the following:

```
$ rds clone --help

Usage: rds clone [OPTIONS]

  Prints the ARN of the snapshot to stdout.

  NOTE: Please ensure the RDS instance ID is stored in your environment
  variable as DBINSTANCEID

Options:
  --instance_id TEXT  Retrieved from ENV
  --help              Show this message and exit.




$ rds deploy --help

Usage: rds deploy [OPTIONS]

  Deploy new DB from snapshot and print ARN to stdout.

  NOTE: Please ensure the RDS instance ID is stored in your environment
  variable as DBINSTANCEID

Options:
  --instance_id TEXT  The ID of the DB Instance.
  --new_db_id TEXT    The ID of the new DB.
  --help              Show this message and exit.

```
## Running the tests

Explain how to run the automated tests for this system

### Break down into end to end tests

Explain what these tests test and why

```
Give an example
```

### And coding style tests

Explain what these tests test and why

```
Give an example
```

## Deployment

Add additional notes about how to deploy this on a live system

## Built With

Python2.7 and using Click framework

## Contributing

Please read CONTRIBUTING.md for details on our code of conduct, and the process for submitting pull requests to us.

## Versioning

To be determined.

## Authors

* **Adeel Ahmad** - *Initial work* - [adeelahmad84](https://github.com/adeelahmad84)


## License

This project is licensed under the MIT License - see the LICENSE.md file for details

## Acknowledgments

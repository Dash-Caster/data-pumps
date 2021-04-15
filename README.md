
<!-- PROJECT SHIELDS -->
[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]



<!-- PROJECT LOGO -->
<br />
<p align="center">
  <a href="https://www.dashcaster.com/">
    <img src="images/logo-light.svg" alt="Logo" width="240">
  </a>

  <h3 align="center">DashCaster Data Pumps</h3>

  <p align="center">
    A collection of free, open-source data pumps to use with DashCaster boards.
    <br />
    <a href="#table-of-contents"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://www.dashcaster.com/">View Demo</a>
    ·
    <a href="https://github.com/Dash-Caster/data-pumps/issues">Report Bug</a>
    ·
    <a href="https://github.com/Dash-Caster/data-pumps/issues">Request Feature</a>
  </p>
</p>



<!-- TABLE OF CONTENTS -->
<h2 id="table-of-contents">Table of Contents</h2>

- [About The Project](#about-the-project)
- [About This Repository](#about-this-repository)
  - [Built With](#built-with)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Quickstart](#quickstart)
- [List of services](#list-of-services)
- [Usage](#usage)
    - [Running services using Docker-Compose](#running-services-using-docker-compose)
    - [Running a service as a standalone Docker container](#running-a-service-as-a-standalone-docker-container)
    - [Running a service locally without Docker](#running-a-service-locally-without-docker)
- [License](#license)
- [Contact](#contact)



<!-- ABOUT THE PROJECT -->
## About The Project

[![DashCaster Screenshot][product-screenshot]](https://www.dashcaster.com/)

[DashCaster](https://www.dashcaster.com/) helps you create fast & effortless visual reports to summarize, track, and share your project data in real-time with less time and effort.

## About This Repository
This repository contains a collection of free, open-source data pumps to use with DashCaster boards to make reporting effortless. 


### Built With

* Python
* Docker


<!-- GETTING STARTED -->
## Getting Started

This guide will get the data pump services up and running on your environment.

### Prerequisites

* Install [Docker](https://www.docker.com/)


### Quickstart

1. Clone the repo
   ```sh
   git clone https://github.com/Dash-Caster/data-pumps.git
   ```
2. Configure the `<service_name>/.env` file according to your desired service name which you want to run. More details can be found in [List of services](#list-of-services).
   
3. Run `docker-compose up -d <service_name>` from project root to run the desired service.

## List of services
This repository contains the following data pump services for DashCaster boards.

|       Service name            |         Description |       Configuration         |
|-----------------------------------|---------------------------------|-------------|
| [demo_data](https://github.com/Dash-Caster/data-pumps/demo_data) | A simple service that takes in a list of numbers and pushes each number periodically to your DashCaster board.| Edit `demo_data/.env` file according to [these instructions](https://github.com/Dash-Caster/data-pumps/demo_data#configuration). |
| [running_ec2_instances](https://github.com/Dash-Caster/data-pumps/running_ec2_instances) | This service takes in AWS credentials, a list of regions and pushes the count of running AWS EC2 instances across the given regions to your DashCaster board.| Edit `running_ec2_instances/.env` file according to [these instructions](https://github.com/Dash-Caster/data-pumps/running_ec2_instances#configuration). |
| [sqs_queue_messages](https://github.com/Dash-Caster/data-pumps/sqs_queue_messages) | This service takes in AWS credentials, an SQS queue name and region, and pushes the count of the messages in the queue to your DashCaster board.| Edit `sqs_queue_messages/.env` file according to [these instructions](https://github.com/Dash-Caster/data-pumps/sqs_queue_messages#configuration). |
| [current_aws_bill](https://github.com/Dash-Caster/data-pumps/current_aws_bill) | This service takes in AWS credentials and pushes the current estimated MTD bill to your DashCaster board.| Edit `current_aws_bill/.env` file according to [these instructions](https://github.com/Dash-Caster/data-pumps/current_aws_bill#configuration). |
| [rds_data_api_query](https://github.com/Dash-Caster/data-pumps/rds_data_api_query) | This service takes in AWS credentials, RDS instance details, and an SQL query, and pushes the value returned by the query to your DashCaster board.| Edit `rds_data_api_query/.env` file according to [these instructions](https://github.com/Dash-Caster/data-pumps/rds_data_api_query#configuration). |
| [web_scraped_value](https://github.com/Dash-Caster/data-pumps/web_scraped_value) | This service takes in the URL of a webpage and an Xpath selector, and pushes the value scraped from the Xpath selector to your DashCaster board.| Edit `web_scraped_value/.env` file according to [these instructions](https://github.com/Dash-Caster/data-pumps/web_scraped_value#configuration). |
| [dynamodb_query](https://github.com/Dash-Caster/data-pumps/dynamodb_query) | This service takes in AWS credentials and a DynamoDB query, and pushes the value returned by the query to your DashCaster board.| Edit `dynamodb_query/.env` and `dynamodb_query/arguments.json` files according to [these instructions](https://github.com/Dash-Caster/data-pumps/dynamodb_query#configuration). |
| [open_pull_requests](https://github.com/Dash-Caster/data-pumps/open_pull_requests) | This service takes in a Github organization, user, or repository URL, and pushes the number of total open PRs to your DashCaster board. | Edit `open_pull_requests/.env` file according to [these instructions](https://github.com/Dash-Caster/data-pumps/open_pull_requests#configuration). |

<!-- USAGE EXAMPLES -->
## Usage

#### Running services using Docker-Compose
To run a data pump service using Docker-Compose, configure the `<service_name>/.env` file for the desired service, and run:
```bash
docker-compose up -d <service_name>
```
<br>

Multiple data pump services can be run by configuring the `<service_name>/.env` file for each service, and running:

```bash
docker-compose up -d <service_name:1> <service_name:2> ...
```

#### Running a service as a standalone Docker container

A data pump can be run as a standalone Docker container. Before trying to run a service as a stand-alone container, please configure the service as specified in [List of services](#list-of-services) or the service README.
* Navigate to the service directory using `cd <service_name>`

**Build**

From the `<service_name>` directory, build the Docker container for a service using
```
docker build -t <service_name> .
```
Where `service_name` is the name of the service you want to run.

**Run**

After building a container for `<service_name>`, from the `<service_name>` directory, run the Docker container for this service using
```bash
docker run -d -v $PWD/../common:/app/common --env-file=.env <service_name>:latest
```
Where `service_name` is the name of the service you want to run.

#### Running a service locally without Docker

[Python](https://www.python.org/downloads/) should be installed to run a service locally without Docker.
* Navigate to the service directory.
  ```bash
  cd <service_name>
  ```
  where `service_name` is the name of the service.
<br>

* Create and activate a fresh virtual environment in `service_name` directory.
  ```bash
  python -m virtualenv venv
  source venv/bin/activate
  ```
<br>

* Activate the virtual environment and run:
  ```bash
  pip install -r requirements.txt
  export $(cat .env | xargs) && python service.py
  ```


<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE` for more information.



<!-- CONTACT -->
## Contact

Project Link: [https://github.com/Dash-Caster/data-pumps](https://github.com/Dash-Caster/data-pumps)


<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/Dash-Caster/data-pumps.svg?style=for-the-badge
[contributors-url]: https://github.com/Dash-Caster/data-pumps/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/Dash-Caster/data-pumps.svg?style=for-the-badge
[forks-url]: https://github.com/Dash-Caster/data-pumps/network/members
[stars-shield]: https://img.shields.io/github/stars/Dash-Caster/data-pumps.svg?style=for-the-badge
[stars-url]: https://github.com/Dash-Caster/data-pumps/stargazers
[issues-shield]: https://img.shields.io/github/issues/Dash-Caster/data-pumps.svg?style=for-the-badge
[issues-url]: https://github.com/Dash-Caster/data-pumps/issues
[license-shield]: https://img.shields.io/github/license/Dash-Caster/data-pumps.svg?style=for-the-badge
[license-url]: https://github.com/Dash-Caster/data-pumps/blob/master/LICENSE.txt
[product-screenshot]: ./images/Screenshot.png

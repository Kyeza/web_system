[![Build Status](https://travis-ci.com/Kyeza/web_system.svg?branch=uganda-master)](https://travis-ci.com/Kyeza/web_system)

# PAYROLL SYSTEM

A Human resource system for Employee management and a Payroll system that enables an organisation manage process 
payments, reconciliation between different payroll periods, email functionality of reports to Employees among others.
<br>
The System is customizable to an organizations needs and any changes can be made as required. 

## Getting Started

### Summary of system features
* Support for automated employee contract renewals
* Authentication of comapny employees
* Calculating months payroll enumarations for different taxes for employess
* Automated emailing of monthly payslips to users
* Generation of numerous financial reports e.g Bank reports, PAYE reports, Reconcilation reports
* Reconciliation of ledgers for different monthly reports
* Automated remainders for birtdays and messaging to employess with custom messages

### Installation
* Ensure you system has Make to read Make files for easy deployment.

* Create .env files and provide the following enviroment variables
    MYSQL_DATABASE=database_name
    MYSQL_USER=database_user
    MYSQL_PASSWORD=database_password
    MYSQL_ROOT_PASSWORD=database_password
    DEBUG=False/True
    SECRET_KEY=secret_app_key
    MYSQL_HOST=database_host
    DEFAULT_FROM_EMAIL=default_email_sender
    EMAIL_HOST_PASSWORD=email_host_password
    EMAIL_HOST_USER=email_host_user
    EMAIL_USE_TLS=True/False
    EMAIL_PORT=email_host_port
    EMAIL_HOST=email_host
    EMAIL_BACKEND=email_host_backend
    EMAIL_BACKEND=email_host_backend
    
  * Run the following command to deploy the application
    $ make deploy - builds and runs docker container
    $ make migrate - makes migrations and also runs the migrate command
    $ make logs - to view system logs
    
  * Run the following command to run tests
    $ make test 

## Built With

* [Django](http://www.dropwizard.io/1.0.2/docs/) - The web framework used
* [pip](https://maven.apache.org/) - Dependency Management
* [Python](https://rometools.github.io/rome/) - Developemt language 

## Developer

* **Kyeza Arnold** - *Initial work* - [HR SYSTEM](https://github.com/Kyeza/web_system)

## License

Copyright (c) 2019 [Kyeza Arnold](https://github.com/Kyeza)

## Acknowledgments

* Peter Omedo (Project designer)

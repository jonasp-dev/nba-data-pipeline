# NBA Data Processing Pipeline

This repository contains a microservice-based architecture designed to process NBA game data stored in an S3 bucket. The pipeline involves the following core processes:

- **Normalization**: Standardizing the raw JSON data from the S3 bucket.
- **Transformation**: Modifying and restructuring the data as needed.
- **Insertion**: Storing the processed data into a PostgreSQL database for further analysis.

## Architecture Overview

The pipeline is built using a **microservice architecture** that includes the following components:

- **S3 Bucket**: Contains the raw JSON data of NBA games.
- **RabbitMQ**: Acts as the message broker for communication between the services.
- **Worker Service**: A service that processes the data in multiple stages (Normalization, Transformation, Insertion).
- **PostgreSQL Database**: Stores the transformed data for further use.
- **Docker Compose**: Manages the orchestration of all services.

## Project Structure
/nba-data-pipeline 
│ 
├── docker-compose.yml # Docker Compose configuration file 
├── services │ 
    ├── worker-service/ # Service for processing data │ 
    ├── postgres/ # PostgreSQL container │ 
└── rabbitmq/ # RabbitMQ container 
└── README.md # Project documentation

Before running the pipeline, make sure you have the following installed:

- **Docker** (for containerization)
- **Docker Compose** (for service orchestration)

## Getting Started

Follow these steps to set up and run the NBA data processing pipeline locally.

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/nba-data-pipeline.git
cd nba-data-pipeline
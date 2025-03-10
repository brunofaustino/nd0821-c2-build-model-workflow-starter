#!/usr/bin/env python
"""
Performs basic cleaning on the data and save the results in Weights & Biases
"""
import argparse
import logging
import wandb
import pandas as pd


logging.basicConfig(level=logging.INFO, format="%(asctime)-15s %(message)s")
logger = logging.getLogger()


def go(args):

    run = wandb.init(job_type="basic_cleaning")
    run.config.update(args)

    # Download input artifact. This will also log that this script is using this
    # particular version of the artifact
    # artifact_local_path = run.use_artifact(args.input_artifact).file()

    ######################
    # YOUR CODE HERE     #
    ######################
    logger.info(f"Download artifact {args.input_artifact}")
    # run = wandb.init(project="nyc_airbnb", group="eda", save_code=True)
    local_path = wandb.use_artifact("sample.csv:latest").file()
    df = pd.read_csv(local_path)

    logger.info(f"Clean up dataset")
    # Drop outliers
    idx = df['price'].between(args.min_price, args.max_price)
    df = df[idx].copy()

    # This will drop rows in the dataset that are not in the proper geolocation.
    idx = df['longitude'].between(-74.25, -73.50) & df['latitude'].between(40.5, 41.2)
    df = df[idx].copy()

    # Convert last_review to datetime
    df['last_review'] = pd.to_datetime(df['last_review'])
    df.to_csv("clean_sample.csv", index=False)

    logger.info(f"Uploading Artifact {args.output_artifact}")
    artifact = wandb.Artifact(
        args.output_artifact,
        type=args.output_type,
        description=args.output_description,
    )
    artifact.add_file("clean_sample.csv")
    run.log_artifact(artifact)

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="This steps cleans the data")

    parser.add_argument(
        "--input_artifact",
        type=str,
        help='Input artifact name',
        required=True
    )

    parser.add_argument(
        "--output_artifact",
        type=str,
        help='Output artifact name',
        required=True
    )

    parser.add_argument(
        "--output_type",
        type=str,
        help='Output artifact type',
        required=True
    )

    parser.add_argument(
        "--output_description",
        type=str,
        help='Output artifact description',
        required=True
    )

    parser.add_argument(
        "--min_price",
        type=float,
        help='Minimum price input artifact data',
        required=True
    )

    parser.add_argument(
        "--max_price",
        type=float,
        help='Maximum price output artifact data',
        required=True
    )

    args = parser.parse_args()

    go(args)

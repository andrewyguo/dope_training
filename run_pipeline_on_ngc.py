# This script is intended to make it easier to run the training, inference, and evaluation pipeline on NGC

if __name__ == "__main__":

    import argparse
    import subprocess

    parser = argparse.ArgumentParser()

    parser.add_argument("--endpoint", "--endpoint_url", type=str, required=True)
    parser.add_argument(
        "--batchsize", "--batch_size", type=int, default=32, help="input batch size"
    )
    parser.add_argument(
        "--train_buckets",
        nargs="+",
        help="s3 buckets containing training data. Can list multiple buckets separated by a space.",
        required=True
    )
    parser.add_argument(
        "--output_bucket",
        default="output_bucket",
        help="Name of the bucket to write output to.",
        required=True
    )
    parser.add_argument(
        "--num_gpus", type=int, help="number of GPUs to be used in training.", default=1
    )
    parser.add_argument(
        "--epochs",
        type=int,
        default=60,
        help="Number of epochs to train for",
    )
    parser.add_argument(
        "--object",
        required=True,
        help='Object to train network for. Must match "class" field in groundtruth .json file. For best performance, only put one object of interest.',
    )
    parser.add_argument(
        "--inference_bucket",
        required=True,
        help="Bucket that stores inference data.",
    )

    opt = parser.parse_args()
    opt.train_buckets = " ".join(opt.train_buckets)
    train_command = ["python", "-m", "torch.distributed.launch", f"--nproc_per_node={opt.num_gpus}", "train.py"]
    train_command += ["--use_s3"]
    train_command += ["--endpoint", f"{opt.endpoint}"]
    train_command += ["--train_buckets", f"{opt.train_buckets}"]
    train_command += ["--object", f"{opt.object}"]
    train_command += ["--batchsize", f"{opt.batchsize}"]
    # 1 epoch on n GPUs is equivalent to n epochs on 1 GPU
    train_command += ["--epochs", f"{opt.epochs // opt.num_gpus }"]
    # train_command.append(f"--train_buckets {opt.train_buckets}")
    # train_command.append(f"--object {opt.object}")
    # train_command.append(f"--batchsize {opt.batchsize}")
    # train_command.append(f"--epochs {opt.epochs // opt.num_gpus}") 

    print(train_command)
    subprocess.call(train_command)
    
    subprocess.run("mkdir output/inference_data")
    subprocess.run(f"s3cmd sync s3://{opt.inference_data} output/inference_data")

    subprocess.call("cd inference/")
    inference_command = ["python inference/inference.py"]
    inference_command.append("--weights output/weights")
    inference_command.append("--data output/inference_data")
    inference_command.append(f"--object {opt.object}")

    subprocess.call(inference_command)

    subprocess.call("cd ../evaluate/")
    evaluate_command = ["python evaluate.py"]
    evaluate_command.append("--data_prediction inference/output")
    evaluate_command.append("--data output/inference_data")
    evaluate_command.append("--outf output/")
    evaluate_command.append("--cuboid")

    subprocess.call(evaluate_command)

    subprocess.call("cd ../")
    subprocess.call(f"s3cmd mb s3://{opt.output_bucket}")
    subprocess.call(f"s3cmd sync output/ s3://{opt.output_bucket}")
    
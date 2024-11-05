import os
import json
import argparse
from utils import process


parser = argparse.ArgumentParser(description="Wallpaper Engine 壁纸提取器")
parser.add_argument(
    "--input",
    "-i",
    type=str,
    required=True,
    help="Wallpaper Engine workshop的路径",
)
parser.add_argument(
    "--recover", "-r", action="store_true", default=False, help="是否恢复上次失败的任务"
)
parser.add_argument(
    "--output", "-o", type=str, required=True, help="提取到的壁纸的保存路径"
)
parser.add_argument(
    "--parallel", "-p", type=int, default=os.cpu_count(), help="并行处理数量"
)
parser.add_argument("--retry", type=int, default=1, help="重试次数")
args = parser.parse_args()


if __name__ == "__main__":
    output_base = args.output
    origin_path = args.input

    if args.recover:
        if os.path.exists(os.path.join(output_base, "failed.json")):
            with open(
                os.path.join(output_base, "failed.json"), "r", encoding="utf-8"
            ) as f:
                target_ids = json.load(f)
                assert isinstance(target_ids, list), "failed.json 格式错误"
        else:
            print("没有失败的任务记录, 请先运行一次正常的任务")
            exit(0)
    else:
        target_ids = os.listdir(origin_path)
        target_ids = [
            item
            for item in target_ids
            if os.path.isdir(os.path.join(origin_path, item))
        ]

    failed = []
    processed_list = []
    origin_metadata = []
    if os.path.exists(os.path.join(output_base, "metadata.json")):
        with open(
            os.path.join(output_base, "metadata.json"), "r", encoding="utf-8"
        ) as f:
            origin_metadata = json.load(f)
            assert isinstance(origin_metadata, list), "metadata.json 格式错误"
            processed_list.extend(item["ID"] for item in origin_metadata)

    target_ids = list(set(target_ids) - set(processed_list))

    metadata, failed = process(origin_path, target_ids, output_base, args.parallel)

    metadata += origin_metadata

    if len(failed) != 0:
        print("重试中...")
        for _ in range(args.retry):
            retry_metadata, failed = process(origin_path, failed, output_base, args.parallel)

            metadata += retry_metadata

            if len(failed) == 0:
                break
    with open(os.path.join(output_base, "metadata.json"), "w", encoding="utf-8") as f:
        json.dump(metadata, f, ensure_ascii=False, indent=4)

    if len(failed) != 0:
        with open(os.path.join(output_base, "failed.json"), "w", encoding="utf-8") as f:
            json.dump(failed, f, ensure_ascii=False, indent=4)

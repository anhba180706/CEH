#!/usr/bin/env python3
"""CEH v13 Extended Toolkit - Entry point."""
import argparse
import sys
import yaml
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

from core.logger import get_logger
from core.orchestrator import Orchestrator
from modules import report

LOG = get_logger("ceh.main")


def load_config(path):
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def list_modules():
    modules_dir = Path(__file__).parent / "modules"
    print("Các module có sẵn:")
    for p in sorted(modules_dir.glob("m*.py")):
        print(f"  - {p.stem}")


def main():
    ap = argparse.ArgumentParser(
        description="CEH v13 Extended Toolkit (Modules 02-11)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ví dụ:
  python main.py scan example.com
  python main.py scan 192.168.1.10 --modules m03_scanning,m04_enumeration
  python main.py scan example.com --no-parallel --config config.yaml
  python main.py list
        """)
    sub = ap.add_subparsers(dest="cmd", required=True)

    scan = sub.add_parser("scan", help="Chạy quét mục tiêu")
    scan.add_argument("target", help="Domain hoặc IP")
    scan.add_argument("--config", default="config.yaml")
    scan.add_argument("--modules", help="Danh sách module, cách nhau bởi dấu phẩy")
    scan.add_argument("--no-parallel", action="store_true",
                      help="Chạy tuần tự thay vì song song")
    scan.add_argument("--out", default=None, help="Thư mục output")

    sub.add_parser("list", help="Liệt kê module có sẵn")

    args = ap.parse_args()

    if args.cmd == "list":
        list_modules()
        return

    # Load config
    cfg_path = Path(args.config)
    cfg = load_config(cfg_path) if cfg_path.exists() else {"modules": {}}

    # Chọn module
    modules = (args.modules.split(",") if args.modules
               else cfg.get("enabled_modules", []))

    LOG.info(f"Target  : {args.target}")
    LOG.info(f"Modules : {', '.join(modules)}")
    LOG.info("=" * 60)

    # Chạy
    orch = Orchestrator(args.target,
                        cfg,
                        parallel=not args.no_parallel,
                        max_workers=cfg.get("general", {}).get("threads", 3))
    results = orch.run(modules)

    # Báo cáo
    out_dir = args.out or cfg.get("general", {}).get("output_dir", "./output")
    json_path, html_path = report.save_reports(args.target, results, out_dir)
    LOG.info("=" * 60)
    LOG.info(f"[✓] JSON : {json_path}")
    LOG.info(f"[✓] HTML : {html_path}")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        LOG.warning("Đã hủy bởi người dùng.")
        sys.exit(130)
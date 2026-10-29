import importlib
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from core.logger import get_logger


class Orchestrator:
    """Chạy nhiều module, có thể song song."""

    def __init__(self, target, config, parallel=True, max_workers=3):
        self.target = target
        self.config = config
        self.parallel = parallel
        self.max_workers = max_workers
        self.logger = get_logger("ceh.orchestrator")

    def _load_module(self, module_name):
        mod = importlib.import_module(f"modules.{module_name}")
        return mod.Module

    def run(self, modules):
        results = {}
        tasks = []

        for m in modules:
            try:
                cls = self._load_module(m)
                cfg = self.config.get("modules", {}).get(m, {})
                instance = cls(self.target, cfg)
                tasks.append((m, instance))
            except Exception as e:
                self.logger.error(f"Không load được module {m}: {e}")
                results[m] = {"error": str(e)}

        if self.parallel:
            with ThreadPoolExecutor(max_workers=self.max_workers) as pool:
                future_map = {pool.submit(inst.run): name for name, inst in tasks}
                for fut in as_completed(future_map):
                    name = future_map[fut]
                    t0 = time.time()
                    try:
                        results[name] = fut.result()
                        self.logger.info(
                            f"[✓] {name} xong trong {time.time()-t0:.1f}s")
                    except Exception as e:
                        self.logger.error(f"[✗] {name} lỗi: {e}")
                        results[name] = {"error": str(e)}
        else:
            for name, inst in tasks:
                try:
                    results[name] = inst.run()
                except Exception as e:
                    results[name] = {"error": str(e)}

        return results
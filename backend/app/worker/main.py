from rq import Connection, Worker

from app.core.config import get_settings


def main() -> None:
    settings = get_settings()
    with Connection():
        worker = Worker([settings.task_queue_name], name="flow-worker")
        worker.work()


if __name__ == "__main__":
    main()

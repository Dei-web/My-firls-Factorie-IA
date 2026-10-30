from adapters.inbound.cli import run_cli
from adapters.inbound.telegram_bot import run_telegram_bot


def main() -> None:
    # run_telegram_bot()
    run_cli()


if __name__ == "__main__":
    main()

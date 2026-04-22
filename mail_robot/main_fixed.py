def main():
    """
    Main function to run the mail checking process.

    Flow:
    1. Setup database schema
    2. Check for command-line arguments
    3. Run mail check for all accounts if no args provided
    """
    setup_database()
    logging.info("[MAIN] Database schema initialized.")

    parser = argparse.ArgumentParser(
        prog="check_mail.py",
        description="Mail Robot: Автоматизированный Проверщик Почты (CLI)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    parser.add_argument(
        "-h", "--help", action="store_true", help="Show this help message and exit"
    )
    parser.add_argument(
        "-get", action="store_true", help="Sync + Update DB (download new mail to DB)"
    )
    parser.add_argument(
        "-check", action="store_true", help="Get unread emails as JSON (stdout)"
    )
    parser.add_argument(
        "-all", action="store_true", help="Get all emails from DB (for debugging)"
    )

    group = parser.add_argument_group("Read & Mark Commands")
    group.add_argument(
        "-read", type=int, help="Read specific email by ID (full content)"
    )
    group.add_argument("-mark-read", type=int, help="Mark email as read by ID")

    args = parser.parse_args()

    # Check for empty run (no flags provided via sys.argv)
    # Use sys.argv to detect if any action flags were actually passed
    action_flags = [arg for arg in sys.argv[1:] if arg.startswith("-") and 
                    (arg in ['-get', '-check', '-all', '-h', '--help'] or 
                     (arg.startswith('-read') and arg != '-read') or
                     (arg.startswith('-mark-read') and arg != '-mark-read'))]

    if not action_flags:
        print(
            "Приложение запущено без команд. Используйте `-help` или `-h` для просмотра списка доступных команд."
        )
        return

    # Process flags
    if args.help or '-h' in action_flags or '--help' in action_flags:
        show_help()
        return

    if args.all:
        all_emails = get_unread_emails()
        print(json.dumps(all_emails, indent=2))
        return

    if args.get:
        run_full_check()
        return

    if args.check:
        unread_emails = get_unread_emails()
        print(json.dumps(unread_emails, indent=2))
        return

    if hasattr(args, "read") and args.read:
        email_data = get_email_full(args.read)
        if email_data:
            print(json.dumps(email_data, indent=2))
        else:
            print(f"[ERROR] Email with ID {args.read} not found")
        return

    if hasattr(args, "mark_read") and args.mark_read:
        success = mark_email_read(args.mark_read)
        if success:
            print(f"[SUCCESS] Email with ID {args.mark_read} marked as read")
        else:
            print(f"[ERROR] Email with ID {args.mark_read} not found")
        return

    # Default: run mail check for all accounts in DB
    run_full_check()


if __name__ == "__main__":
    main()

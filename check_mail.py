#!/usr/bin/env python3
"""
Mail Robot - Email Checker with SQLite Storage

USAGE:
    python check_mail.py              - Run mail check for all accounts
    python check_mail.py add "email" "password" "server" "port" "ssl"
    python check_mail.py list         - List all configured accounts
    python check_mail.py remove "email"
    python check_mail.py help         - Show this help message
"""

import email
import imaplib
import logging
import sqlite3
import sys
from datetime import datetime
from email.header import decode_header
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple
from typing import Tuple as TP

# =============================================================================
# CONFIGURATION
# =============================================================================
BASE_DIR = Path(__file__).parent
DB_FILE = BASE_DIR / "mail_check.db"
LOG_FILE = BASE_DIR / "mail_check.log"


# =============================================================================
# LOGGING SETUP
# =============================================================================
def setup_logging():
    """Configure logging to both console and file."""
    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setFormatter(
        logging.Formatter(fmt="%(levelname)s: %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
    )

    file_handler = logging.FileHandler(LOG_FILE, encoding="utf-8")
    file_handler.setFormatter(
        logging.Formatter(
            fmt="%(asctime)s: %(levelname)s: %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
        )
    )

    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)
    root_logger.addHandler(stream_handler)
    root_logger.addHandler(file_handler)

    return root_logger


root_logger = setup_logging()


# =============================================================================
# DATABASE MANAGEMENT - ACCOUNTS (SQLite)
# =============================================================================
def setup_database():
    """Ensures the database and the necessary tables exist."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS accounts (
            email TEXT PRIMARY KEY,
            password TEXT NOT NULL,
            imap_server TEXT NOT NULL,
            imap_port INTEGER NOT NULL,
            imap_security TEXT NOT NULL,
            last_checked_date TEXT
        )
    """)
    conn.commit()
    conn.close()


def add_or_update_account(account_info: Dict[str, Any]) -> bool:
    """
    Adds a new account or updates an existing one in the database.

    Args:
        account_info: Dictionary containing email, password, imap_server,
                      imap_port, imap_security

    Returns:
        True if successful, False otherwise
    """
    required_fields = ["email", "password", "imap_server", "imap_port", "imap_security"]
    missing = [f for f in required_fields if f not in account_info]

    if missing:
        logging.warning(f"[DB] Missing fields: {missing}")
        return False

    email = account_info["email"]
    password = account_info["password"]
    imap_server = account_info["imap_server"]
    imap_port = int(account_info["imap_port"])
    imap_security = account_info["imap_security"].lower()

    conn = sqlite3.connect(DB_FILE)
    try:
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT OR REPLACE INTO accounts (
                email, password, imap_server, imap_port, imap_security, last_checked_date
            ) VALUES (?, ?, ?, ?, ?, NULL)
        """,
            (email, password, imap_server, imap_port, imap_security),
        )
        logging.info(f"[DB] Account {email} added/updated to database.")
        conn.commit()
        conn.close()
        return True
    except sqlite3.Error as e:
        logging.error(f"[DB] Database error: {e}")
        conn.close()
        return False


def update_checked_date(email: str, date_str: str):
    """Updates the last checked date for an account."""
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute(
            """UPDATE accounts SET last_checked_date = ? WHERE email = ?""",
            (date_str, email),
        )
        conn.commit()
        if cursor.rowcount == 0:
            logging.warning(f"[DB] No account found for {email} to update.")


def delete_account(email: str) -> bool:
    """Deletes an account from the database."""
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM accounts WHERE email = ?", (email,))
        conn.commit()
        return cursor.rowcount > 0


def get_all_accounts() -> List[Dict[str, Any]]:
    """Retrieves all accounts from the database."""
    accounts = []
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT email, password, imap_server, imap_port, imap_security, last_checked_date
            FROM accounts
        """)
        for row in cursor.fetchall():
            accounts.append(
                dict(
                    zip(
                        [
                            "email",
                            "password",
                            "imap_server",
                            "imap_port",
                            "imap_security",
                            "last_checked_date",
                        ],
                        row,
                    )
                )
            )
    return accounts


# =============================================================================
# HELP TEXT
# =============================================================================
HELP_TEXT = """

Mail Robot - Email Checker

USAGE:
    python check_mail.py              - Run mail check for all accounts
    python check_mail.py add "email" "password" "server" "port" "ssl"
    python check_mail.py list         - List all configured accounts
    python check_mail.py remove "email"
    python check_mail.py help         - Show this help message

ARGUMENTS FOR 'add' command:
    email      - Full email address (e.g., user@example.com)
    password   - Email account password
    server     - IMAP server address (e.g., imap.gmail.com)
    port       - IMAP port (typically 993 for SSL)
    ssl/tls    - Security type: 'ssl', 'starttls', or 'tls'

EXAMPLES:

    Add Google account:
        python check_mail.py add "user@gmail.com" "mypassword" \\
                                "imap.gmail.com" "993" "ssl"

    Add account with STARTTLS:
        python check_mail.py add "user@example.com" "pass123" \\
                                "imap.example.com" "143" "starttls"

    List accounts:
        python check_mail.py list

    Remove account:
        python check_mail.py remove "user@example.com"


SETTINGS:
    - Accounts are stored in: {DB_FILE}
    - Logs are written to:    {LOG_FILE}

AUTHOR: Mail Robot | Version: 1.0
"""


# =============================================================================
# CORE MAIL CHECKING LOGIC
# =============================================================================
def connect_imap(imap_server: str, imap_port: int, imap_security: str):
    """
    Connects to the IMAP server using the specified security method.
    Supports 'ssl' and 'starttls'.
    """
    if imap_security == "starttls":
        mail = imaplib.IMAP4(imap_server, imap_port)
        mail.starttls()
    else:
        mail = imaplib.IMAP4_SSL(imap_server, imap_port)
    return mail


def check_mail(
    account_info: Dict[str, Any],
) -> Tuple[Dict[str, Any], Optional[imaplib.IMAP4]]:
    """
    Connects to the IMAP server, authenticates, and fetches all available mail details.

    Returns:
        A tuple of (results_dict, imap_connection) for proper cleanup.
    """
    email_address = account_info["email"]
    password_raw = account_info["password"]
    imap_server = account_info["imap_server"]
    imap_port = account_info["imap_port"]
    imap_security = account_info["imap_security"]

    if not password_raw:
        logging.error(f"[WARNING] No password found for {email_address}.")
        return {"error": f"No password configured for account."}, None

    logging.info(f"[CONN] --- Connecting to {imap_server} for {email_address} ---")

    try:
        mail = connect_imap(imap_server, imap_port, imap_security)
        logging.info("[CONN] Attempting to log in...")
        mail.login(email_address, password_raw)
        logging.info("[CONN] Successfully logged in.")

        try:
            mail.select("INBOX")
            logging.info("[CONN] INBOX selected successfully.")
        except imaplib.IMAP4.error as e:
            logging.warning(f"[CONN] Could not select INBOX: {e}")

        search_query = "ALL"
        logging.info(f"[CONN] Searching for: {search_query}")

        status, messages = mail.search(None, "ALL", search_query)

        if status != "OK":
            logging.error(
                f"[CONN] Failed to search for messages. IMAP status: {status}"
            )
            return {
                "error": f"Failed to search for messages. IMAP status: {status}"
            }, mail

        message_ids = messages[0].split()
        logging.info(f"[CONN] Found {len(message_ids)} total messages in the mailbox.")

        all_messages = []
        for msg_id in message_ids[:3]:  # Limit to 3 for display
            status, data = mail.fetch(msg_id, "(RFC822)")
            if status != "OK":
                continue

            raw_message = data[0][1]
            msg = email.message_from_bytes(raw_message)

            try:
                subject_bytes = msg["subject"]
                decoded_part = decode_header(subject_bytes)[0]
                subject = (
                    decoded_part.decode("utf-8", errors="ignore")
                    if isinstance(decoded_part, bytes)
                    else decoded_part
                )
                subject = subject.strip()
            except Exception:
                subject = str(subject_bytes)

            date_header = msg["date"]

            message_details = {
                "subject": subject,
                "sender": msg["from"],
                "date": date_header,
                "msg_id": msg_id,
            }
            all_messages.append(message_details)

        logging.info(f"[CONN] Parsed {len(all_messages)} messages (showing first 3).")

        mail.logout()
        logging.info("[CONN] Logged out and connection closed.")

        return {"messages": all_messages, "total_messages": len(message_ids)}, mail

    except imaplib.IMAP4.error as e:
        logging.error(f"[CONN] Authentication or Connection Error: {e}")
        return {"error": f"IMAP Error: {e}"}, mail
    except Exception as e:
        logging.error(f"[CONN] An unexpected error occurred: {e}")
        return {"error": f"Unexpected Error: {e}"}, mail


# =============================================================================
# MAIN EXECUTION
# =============================================================================
def show_help():
    """Print help message and exit."""
    print(HELP_TEXT.format(DB_FILE=DB_FILE, LOG_FILE=LOG_FILE))


def show_accounts():
    """Show all configured accounts."""
    accounts = get_all_accounts()
    if not accounts:
        print("\n=== No accounts configured ===")
        print(
            "Run: python check_mail.py add 'email' 'password' 'server' 'port' 'ssl'\n"
        )
        return

    for i, acc in enumerate(accounts, 1):
        checked = acc.get("last_checked_date", "never") or "never"
        print(f"  {i}. {acc['email']}")
        print(
            f"     Server: {acc['imap_server']}:{acc['imap_port']} ({acc['imap_security']})"
        )
        print(f"     Last checked: {checked}")


def run_full_check():
    """Run mail check for all accounts in database."""
    all_results = []
    accounts_list = get_all_accounts()

    if not accounts_list:
        logging.info("[MAIN] No accounts found in database. Add an account first.")
        logging.info(
            f"[MAIN] Run: python {sys.argv[0]} add 'email' 'password' 'server' 'port' 'ssl'"
        )
        return

    logging.info("[MAIN] === STARTING MAIL CHECKING PROCESS ===")
    logging.info("[MAIN] ======================================================")

    for index, account in enumerate(accounts_list):
        logging.info("[MAIN] -------------------------------------------")
        logging.info(
            f"[MAIN] Processing account {index + 1} of {len(accounts_list)}..."
        )
        logging.info(f"[MAIN]   Email: {account['email']}")

        mail_data, _ = check_mail(account)
        all_results.append({"email": account["email"], "data": mail_data})

        current_date = datetime.now().strftime("%Y-%m-%d")
        update_checked_date(account["email"], current_date)

    logging.info("[MAIN] ======================================================")
    logging.info("[MAIN] === ALL EMAIL CHECKING COMPLETE ===")
    logging.info("[MAIN] ======================================================")

    for result in all_results:
        email = result["email"]
        data = result["data"]

        logging.info(f"\n[SUMMARY] Account: {email}")
        if "error" in data:
            logging.error(
                f"  [ERROR] FAILED to retrieve mail data. Reason: {data['error']}"
            )
        else:
            logging.info("  [SUCCESS] Successfully retrieved mail data!")
            total = data.get("total_messages", 0)
            logging.info(f"  -> Found {total} total messages in mailbox.")
            messages = data.get("messages", [])
            for i, mail in enumerate(messages[:3]):
                subject = mail.get("subject", "No subject found")
                logging.info(f"  -> Message {i + 1}: Subject='{subject}'")
            if len(messages) > 3:
                logging.info(
                    f"  -> ... and {len(messages) - 3} more messages not shown."
                )

    logging.info("[MAIN] === END OF PROCESS ===")
    logging.info("[MAIN] ======================================================")


def main():
    """
    Main function to run the mail checking process.

    Flow:
    1. Setup database schema
    2. Check for command-line arguments (add/list/remove)
    3. Run mail check for all accounts if no args provided
    """
    # Setup database
    setup_database()
    logging.info("[MAIN] Database schema initialized.")

    # Parse arguments
    args = sys.argv[1:]

    # If no args provided, run mail check for all accounts in DB
    if not args:
        run_full_check()
        return

    if args == ["help"]:
        show_help()
        return

    if args[0] == "add":
        # Add account from command-line arguments
        if len(args) < 6:
            print(
                "\nUsage: python check_mail.py add 'email' 'password' 'server' 'port' 'ssl'\n"
            )
            print(
                "Example: python check_mail.py add 'user@gmail.com' 'pass' 'imap.gmail.com' '993' 'ssl'\n"
            )
            return

        try:
            email = args[1]
            password = args[2]
            imap_server = args[3]
            imap_port = int(args[4])
            imap_security = args[5].lower()

            account_info = {
                "email": email,
                "password": password,
                "imap_server": imap_server,
                "imap_port": imap_port,
                "imap_security": imap_security,
            }

            if add_or_update_account(account_info):
                print(f"\nAccount added: {email}\n")
            else:
                print(f"\nFailed to add account: {email}\n")
        except ValueError:
            print("\nError: Port must be a number (integer)\n")

    elif args[0] == "list" or args[0] == "list-accounts":
        show_accounts()

    elif args[0] == "remove":
        if len(args) < 2:
            print("\nUsage: python check_mail.py remove 'email'\n")
            return

        email = args[1]
        if delete_account(email):
            print(f"\nAccount removed: {email}\n")
        else:
            print(f"\nAccount not found: {email}\n")

    elif args[0] == "check" or args[0] == "run":
        run_full_check()

    else:
        print("\nUsage: python check_mail.py")
        show_help()

    logging.info("[MAIN] === END OF PROCESS ===")


if __name__ == "__main__":
    main()

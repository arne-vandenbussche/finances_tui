#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 13 10:14:13 2025

@author: arnevandenbussche
"""
# TODO: add exception handling
from datetime import date, datetime
import logging
from pathlib import Path
import sqlite3

from environs import Env  # https://pypi.org/project/environs/

from model.transaction import Transaction

env = Env()
env.read_env()  # read .env file if it exists
DATABASE_NAME = env.str("DATABASE")


def is_valid_date(date_string: str) -> bool:
    try:
        datetime.strptime(date_string, "%Y-%m-%d").date()
        return True
    except (TypeError, ValueError):
        return False


def _serialize_date(date_value: date | None) -> str | None:
    if date_value is None:
        return None
    return date_value.isoformat()


def convert_transaction_row_to_object(transaction_row: tuple) -> Transaction:
    logger = logging.getLogger(__name__)
    tr_id = transaction_row[0]

    if is_valid_date(transaction_row[1]):
        tr_date_of_transaction = datetime.strptime(transaction_row[1], "%Y-%m-%d").date()
    else:
        tr_date_of_transaction = date(1000, 1, 1)
        logger.warning("Transaction with id=%s has an invalid date_of_transaction", tr_id)

    tr_bedrag = transaction_row[2]
    tr_payment_method = transaction_row[3]
    tr_partner = transaction_row[4]
    tr_in_out = transaction_row[5]
    tr_description = transaction_row[6]
    tr_invoice_number = transaction_row[7]

    if transaction_row[8] in (None, ""):
        tr_invoice_date = None
    elif is_valid_date(transaction_row[8]):
        tr_invoice_date = datetime.strptime(transaction_row[8], "%Y-%m-%d").date()
    else:
        tr_invoice_date = None
        logger.warning("Transaction with id=%s has an invalid invoice_date", tr_id)

    tr_category = transaction_row[9]
    tr_activity = transaction_row[10]
    tr_actuele_rekeningstand = transaction_row[11]

    return Transaction(
        id=tr_id,
        date_of_transaction=tr_date_of_transaction,
        bedrag=tr_bedrag,
        payment_method=tr_payment_method,
        partner=tr_partner,
        in_out=tr_in_out,
        description=tr_description,
        invoice_number=tr_invoice_number,
        invoice_date=tr_invoice_date,
        category=tr_category,
        activity=tr_activity,
        actuele_rekeningstand=tr_actuele_rekeningstand,
    )


def get_connection() -> sqlite3.Connection:
    logger = logging.getLogger(__name__)
    db_file_name = DATABASE_NAME
    db_directory = Path.cwd()
    full_db_path = db_directory / db_file_name
    is_new_db = not full_db_path.exists()

    # Connect to database. The database will be created if it does not exist.
    conn = sqlite3.connect(full_db_path)
    conn.execute("PRAGMA foreign_keys = ON")
    logger.info("Connecting to database on %s", full_db_path)

    if is_new_db:
        logger.info("Database on %s missing. Creating database.", full_db_path)
        initialize_database(conn)

    return conn


def initialize_database(conn: sqlite3.Connection) -> None:
    cursor = conn.cursor()
    cursor.executescript(
        """CREATE TABLE if not exists transacties (
    id integer primary key,
    date_of_transaction text not null,
    bedrag real not null default 0,
    payment_method integer references payment_method(id),
    partner integer not null references partner(id),
    in_out text CHECK (in_out IN ('in', 'out')) NOT NULL,
    description text,
    invoice_number text,
    invoice_date date,
    category integer not null references categories(id),
    activity integer references activities(id),
    actuele_rekeningstand real
    );

    CREATE TABLE if not exists categories(
    id integer primary key,
    name text not null,
    description text
    );

    CREATE TABLE if not exists activities(
    id integer primary key,
    name text not null,
    description text
    );

    CREATE TABLE if not exists partner(
    id integer primary key,
    name text not null,
    bank_account text,
    description text
    );

    CREATE TABLE if not exists payment_method(
    id integer primary key,
    name text not null,
    description text
    );
    """
    )
    conn.commit()


def get_all_transactions() -> list[Transaction]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM transacties ORDER BY date_of_transaction DESC")
        all_row_transactions = cursor.fetchall()
        return [convert_transaction_row_to_object(transaction) for transaction in all_row_transactions]


def get_transaction_by_id(transaction_id: int) -> Transaction | None:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM transacties WHERE id = ?", (transaction_id,))
        transaction_row = cursor.fetchone()

    if transaction_row:
        return convert_transaction_row_to_object(transaction_row)
    return None


def get_transactions_by_date(transaction_date: date) -> list[Transaction]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM transacties WHERE date_of_transaction = ?",
            (transaction_date.isoformat(),),
        )
        rows = cursor.fetchall()

    return [convert_transaction_row_to_object(row) for row in rows]


def get_transaction_by_description(part_description: str) -> list[Transaction]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM transacties WHERE LOWER(description) LIKE '%' || LOWER(?) || '%'",
            (part_description,),
        )
        rows = cursor.fetchall()

    return [convert_transaction_row_to_object(row) for row in rows]


def save_transaction(transaction: Transaction) -> None:
    with get_connection() as conn:
        cursor = conn.cursor()

        if transaction.id == 0:
            cursor.execute(
                """
            INSERT INTO transacties
            (date_of_transaction, bedrag, payment_method, partner, in_out, description,
            invoice_number, invoice_date, category, activity, actuele_rekeningstand)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
                (
                    _serialize_date(transaction.date_of_transaction),
                    transaction.bedrag,
                    transaction.payment_method,
                    transaction.partner,
                    transaction.in_out,
                    transaction.description,
                    transaction.invoice_number,
                    _serialize_date(transaction.invoice_date),
                    transaction.category,
                    transaction.activity,
                    transaction.actuele_rekeningstand,
                ),
            )
        else:
            cursor.execute(
                """
            UPDATE transacties
            SET date_of_transaction=?, bedrag=?, payment_method=?, partner=?, in_out=?, description=?,
            invoice_number=?, invoice_date=?, category=?, activity=?, actuele_rekeningstand=?
            WHERE id=?
            """,
                (
                    _serialize_date(transaction.date_of_transaction),
                    transaction.bedrag,
                    transaction.payment_method,
                    transaction.partner,
                    transaction.in_out,
                    transaction.description,
                    transaction.invoice_number,
                    _serialize_date(transaction.invoice_date),
                    transaction.category,
                    transaction.activity,
                    transaction.actuele_rekeningstand,
                    transaction.id,
                ),
            )
